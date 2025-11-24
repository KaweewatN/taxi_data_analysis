"""
Fix the parquet file - columns are mis-mapped:
- vehicle_id column actually contains LATITUDE
- lat column actually contains TIMESTAMP (as string)
- timestamp column is corrupted
- Need to regenerate proper vehicle_id and convert timestamp
"""
import pyarrow.parquet as pq
import pyarrow as pa
import pyarrow.compute as pc

print("📖 Reading original parquet...")
table = pq.read_table('processed_taxi_data.parquet')

print(f"✅ Loaded {table.num_rows:,} rows")

# Create corrected columns
print("\n🔧 Remapping columns...")

# The 'lat' column contains timestamp strings - parse them
print("  - Parsing timestamp from 'lat' column...")
lat_as_timestamp_col = table.column('lat')
# Convert string timestamps to actual timestamps
timestamp_fixed = pc.strptime(lat_as_timestamp_col, format='%Y-%m-%d %H:%M:%S', unit='ms')

# The 'vehicle_id' column actually contains latitude!
print("  - Using 'vehicle_id' as latitude...")
lat_fixed = table.column('vehicle_id')

# lon is correct
lon_fixed = table.column('lon')

# We don't have the real vehicle_id, so we'll need to create a placeholder or drop it
# For now, let's create a sequential ID or use row number
print("  - Generating placeholder vehicle_id...")
vehicle_id_fixed = pa.array(range(table.num_rows), type=pa.int64())

# Build new table with correct column mapping
print("\n🔧 Building corrected table...")
new_table = pa.table({
    'timestamp': timestamp_fixed,
    'vehicle_id': vehicle_id_fixed,
    'lon': lon_fixed,
    'lat': lat_fixed,
    'speed': table.column('speed'),
    'for_hire_light': table.column('for_hire_light'),
    'engine_acc': table.column('engine_acc'),
    'gpsvalid': table.column('gpsvalid'),
    'hour_of_day': table.column('hour_of_day'),
    'day_of_week': table.column('day_of_week'),
    'is_weekend': table.column('is_weekend'),
    'passenger_status': table.column('passenger_status')
})

print("\nNew schema:")
print(new_table.schema)

# Write the fixed parquet file
output_file = 'processed_taxi_data_fixed.parquet'
print(f"\n💾 Writing to {output_file}...")
pq.write_table(new_table, output_file, compression='snappy')

print(f"✅ Done! File saved as {output_file}")
print(f"📊 Rows: {new_table.num_rows:,}")

# Show sample
print("\n📋 Sample of first 3 rows:")
for i in range(3):
    print(f"\nRow {i}:")
    print(f"  timestamp: {new_table.column('timestamp')[i]}")
    print(f"  vehicle_id: {new_table.column('vehicle_id')[i].as_py()}")
    print(f"  lon: {new_table.column('lon')[i].as_py()}")
    print(f"  lat: {new_table.column('lat')[i].as_py()}")
    print(f"  speed: {new_table.column('speed')[i].as_py()}")

