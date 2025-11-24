from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("BangkokTaxiDayNight") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("✅ Spark started")
print(f"🚀 Spark master: {spark.sparkContext.master}")
print(f"📊 Default parallelism: {spark.sparkContext.defaultParallelism}")

# 🔹 1. LOAD DATA
df = spark.read.parquet("processed_taxi_data_fixed.parquet")
print("Row count:", df.count())
df.printSchema()

# 👉 CHANGE THESE if your column names differ
TIMESTAMP_COL = "timestamp"      # e.g. "timestamp" or "ts"
LAT_COL       = "lat"            # e.g. "latitude"
LON_COL       = "lon"            # e.g. "longitude"
STATUS_COL    = "for_hire_light" # 0 = occupied, 1 = vacant (adjust if needed)
VEH_COL       = "vehicle_id"

# 🔹 2. TIME FEATURES
df = df.withColumn("ts", F.to_timestamp(F.col(TIMESTAMP_COL)))
df = df.withColumn("hour", F.hour("ts"))

df = df.withColumn(
    "time_period",
    F.when((F.col("hour") >= 10) & (F.col("hour") < 16), "DAY")   # 10:00–16:00
     .when((F.col("hour") >= 20) | (F.col("hour") < 2), "NIGHT") # 20:00–02:00
     .otherwise("OTHER")
)

# 🔹 3. SPATIAL GRID → simple ~100m grid using rounded lat/lon
df = df.withColumn("lat_bin", F.round(F.col(LAT_COL), 3)) \
       .withColumn("lon_bin", F.round(F.col(LON_COL), 3))

print("🔍 Example with time & bins:")
df.select(TIMESTAMP_COL, "hour", "time_period", "lat_bin", "lon_bin").show(10, False)

# 🔹 4. CHECK FOR_HIRE_LIGHT DISTRIBUTION
print("\n📊 for_hire_light value distribution:")
df.groupBy(STATUS_COL).count().orderBy(STATUS_COL).show()

# NOTE: vehicle_id is now a sequential number (0, 1, 2...) because original data was corrupted
# This means we can't track individual vehicles for transitions!
# We need the ORIGINAL vehicle_id column to track status changes per taxi

print("\n⚠️  WARNING: vehicle_id was regenerated as sequential numbers during data fix.")
print("⚠️  Cannot track individual taxi transitions without original vehicle IDs.")
print("⚠️  Switching to spatial analysis only (no pickup/dropoff transitions).\n")

# Instead of transitions, let's analyze spatial patterns by status
print("🗺️  Analyzing spatial patterns by availability status...")

available_trips = df.filter(F.col(STATUS_COL) == 1).select("lat_bin", "lon_bin", "time_period")
occupied_trips = df.filter(F.col(STATUS_COL) == 0).select("lat_bin", "lon_bin", "time_period")

# =====================================================
#   TASK 1 — DAY/NIGHT ACTIVITY HOTSPOTS (BY STATUS)
# =====================================================

activity_stats = df.groupBy("lat_bin", "lon_bin", "time_period", STATUS_COL) \
    .agg(F.count("*").alias("record_count"))

activity_stats.write.mode("overwrite").csv("output_day_night_activity", header=True)
print("🔥 Exported day/night activity patterns → output_day_night_activity/")

# =====================================================
#   TASK 2 — OCCUPIED vs AVAILABLE ZONES (NIGHT)
# =====================================================

night_data = df.filter(F.col("time_period") == "NIGHT")

occupied_cnt = night_data.filter(F.col(STATUS_COL) == 0).groupBy("lat_bin", "lon_bin") \
    .agg(F.count("*").alias("occupied_count"))

available_cnt = night_data.filter(F.col(STATUS_COL) == 1).groupBy("lat_bin", "lon_bin") \
    .agg(F.count("*").alias("available_count"))

night_zones = occupied_cnt.join(
    available_cnt, on=["lat_bin", "lon_bin"], how="outer"
).fillna(0, subset=["occupied_count", "available_count"])

night_zones = night_zones.withColumn(
    "demand_supply_ratio",
    F.col("occupied_count") / (F.col("available_count") + F.lit(1))
)

# High demand_supply_ratio = many occupied, few available = high demand area
high_demand = night_zones.filter(F.col("occupied_count") >= 20) \
    .orderBy(F.desc("demand_supply_ratio"))

high_demand.write.mode("overwrite").csv("output_night_demand_zones", header=True)
print("🔥 Exported night high-demand zones → output_night_demand_zones/")

# =====================================================
#   TASK 3 — TAXI DESERTS (High Unhired, Low Service)
#   Areas with many available (for_hire_light=1) taxis
#   but low overall activity = poor pickup service
# =====================================================

print("\n🚕 Identifying Taxi Deserts (late night 22:00-04:00)...")

late_night = df.filter((F.col("hour") >= 22) | (F.col("hour") < 4))

# Count unhired (available) taxis by location
unhired_cnt = late_night.filter(F.col(STATUS_COL) == 1).groupBy("lat_bin", "lon_bin") \
    .agg(F.count("*").alias("unhired_count"))

# Total activity (any status) to measure service level
total_activity = late_night.groupBy("lat_bin", "lon_bin") \
    .agg(F.count("*").alias("total_count"))

taxi_deserts = unhired_cnt.join(total_activity, on=["lat_bin", "lon_bin"], how="inner")

# Desert score: high unhired taxis but low total activity = taxis waiting, no passengers
taxi_deserts = taxi_deserts.withColumn(
    "desert_score",
    F.col("unhired_count") / F.col("total_count")
)

# Filter: locations with at least 10 unhired taxis and >50% unhired rate
deserts = taxi_deserts.filter((F.col("unhired_count") >= 10) & (F.col("desert_score") > 0.5)) \
    .orderBy(F.desc("unhired_count"))

deserts.write.mode("overwrite").csv("output_taxi_deserts", header=True)
print("🌑 Exported taxi desert zones → output_taxi_deserts/")

# =====================================================
#   TASK 4 — TRIP DISTANCE ESTIMATION
#   Calculate approximate distance between consecutive GPS points
#   (Haversine formula for lat/lon distance)
# =====================================================

print("\n📏 Calculating trip distances...")

# Add previous location using window function (ordered by timestamp within each vehicle)
w = Window.partitionBy(VEH_COL).orderBy("ts")

df_with_prev = df.withColumn("prev_lat", F.lag(LAT_COL).over(w)) \
                 .withColumn("prev_lon", F.lag(LON_COL).over(w)) \
                 .withColumn("prev_ts", F.lag("ts").over(w))

# Calculate time difference in seconds
df_with_prev = df_with_prev.withColumn(
    "time_diff_sec",
    F.unix_timestamp("ts") - F.unix_timestamp("prev_ts")
)

# Haversine distance formula (approximate km between two lat/lon points)
# Distance = 2 * R * asin(sqrt(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)))
# R = 6371 km (Earth radius)

df_with_prev = df_with_prev.withColumn(
    "dlat", F.radians(F.col(LAT_COL) - F.col("prev_lat"))
).withColumn(
    "dlon", F.radians(F.col(LON_COL) - F.col("prev_lon"))
).withColumn(
    "a",
    F.pow(F.sin(F.col("dlat") / 2), 2) +
    F.cos(F.radians("prev_lat")) * F.cos(F.radians(LAT_COL)) *
    F.pow(F.sin(F.col("dlon") / 2), 2)
).withColumn(
    "distance_km",
    2 * 6371 * F.asin(F.sqrt(F.col("a")))
)

# Filter valid trips (time_diff < 5 min, distance < 50km to remove outliers)
valid_trips = df_with_prev.filter(
    (F.col("time_diff_sec").isNotNull()) &
    (F.col("time_diff_sec") > 0) &
    (F.col("time_diff_sec") < 300) &  # < 5 minutes
    (F.col("distance_km") > 0) &
    (F.col("distance_km") < 50)  # < 50 km
)

# =====================================================
#   TASK 5 — DAY vs NIGHT TRIP LENGTH COMPARISON
# =====================================================

print("\n📊 Comparing day vs night trip characteristics...")

trip_comparison = valid_trips.groupBy("time_period").agg(
    F.avg("distance_km").alias("avg_distance_km"),
    F.avg("time_diff_sec").alias("avg_duration_sec"),
    F.count("*").alias("trip_count"),
    F.percentile_approx("distance_km", 0.5).alias("median_distance_km"),
    F.percentile_approx("time_diff_sec", 0.5).alias("median_duration_sec")
)

trip_comparison.show()

trip_comparison.write.mode("overwrite").csv("output_trip_comparison", header=True)
print("📈 Exported trip comparison (day vs night) → output_trip_comparison/")

# Also save detailed trip segments for further analysis
trip_segments = valid_trips.select(
    "ts", "time_period", "lat_bin", "lon_bin", "distance_km", "time_diff_sec", STATUS_COL
)

trip_segments.write.mode("overwrite").parquet("output_trip_segments.parquet")
print("💾 Saved trip segments → output_trip_segments.parquet")

spark.stop()
print("✅ Done")
