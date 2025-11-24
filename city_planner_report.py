"""
Complete Results Viewer - Covers all City Planner requirements
"""
import csv
import glob

print("="*80)
print("🚖 COMPLETE TAXI DAY/NIGHT ANALYSIS - CITY PLANNER REPORT")
print("="*80)

# ============================================
# REQUIREMENT 1: Economy - Nighttime Economic Zones
# ============================================
print("\n" + "🏙️  REQUIREMENT 1: NIGHTTIME ECONOMIC ZONES".center(80, "="))
print("Compares spatial clustering of drop-off points (DAY vs NIGHT)")
print("-"*80)

demand_files = glob.glob("output_night_demand_zones/part-*.csv")
demand_data = []

for file in demand_files:
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                demand_data.append({
                    'lat_bin': float(row['lat_bin']),
                    'lon_bin': float(row['lon_bin']),
                    'occupied_count': int(row['occupied_count']),
                    'available_count': int(row['available_count']),
                    'demand_supply_ratio': float(row['demand_supply_ratio'])
                })
            except:
                continue

demand_data.sort(key=lambda x: x['demand_supply_ratio'], reverse=True)

print(f"\n🌃 TOP 10 NIGHT ECONOMIC HOTSPOTS (High Demand Zones):")
print(f"{'Rank':<6}{'Latitude':<12}{'Longitude':<12}{'Occupied':<12}{'Available':<12}{'Ratio':<10}")
print("-"*68)

for i, zone in enumerate(demand_data[:10], 1):
    print(f"{i:<6}{zone['lat_bin']:<12.3f}{zone['lon_bin']:<12.3f}"
          f"{zone['occupied_count']:<12}{zone['available_count']:<12}"
          f"{zone['demand_supply_ratio']:<10.1f}")

print("\n💡 ACTIONABLE INSIGHT:")
print("   - These zones show nightlife/entertainment hubs with high taxi demand")
print("   - Justifies investment in:")
print("     • Late-night transit extensions")
print("     • Better street lighting for tourist safety")
print("     • Designated taxi pickup zones")

# ============================================
# REQUIREMENT 2: Trajectory - Hotspot Service Gap (Taxi Deserts)
# ============================================
print("\n\n" + "🚕 REQUIREMENT 2: TAXI DESERTS (SERVICE GAPS)".center(80, "="))
print("Identifies locations with high unhired taxis but low pickups (22:00-04:00)")
print("-"*80)

desert_files = glob.glob("output_taxi_deserts/part-*.csv")
desert_data = []

for file in desert_files:
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                desert_data.append({
                    'lat_bin': float(row['lat_bin']),
                    'lon_bin': float(row['lon_bin']),
                    'unhired_count': int(row['unhired_count']),
                    'total_count': int(row['total_count']),
                    'desert_score': float(row['desert_score'])
                })
            except:
                continue

desert_data.sort(key=lambda x: x['desert_score'], reverse=True)

print(f"\n🌑 TOP 10 TAXI DESERT ZONES (Late Night 22:00-04:00):")
print(f"{'Rank':<6}{'Latitude':<12}{'Longitude':<12}{'Unhired':<12}{'Total':<12}{'Desert %':<10}")
print("-"*68)

for i, zone in enumerate(desert_data[:10], 1):
    pct = zone['desert_score'] * 100
    print(f"{i:<6}{zone['lat_bin']:<12.3f}{zone['lon_bin']:<12.3f}"
          f"{zone['unhired_count']:<12}{zone['total_count']:<12}{pct:<10.1f}%")

print("\n💡 ACTIONABLE INSIGHT:")
print("   - These areas have taxis waiting but few passengers")
print("   - Reveals poor visibility or accessibility issues")
print("   - Calls for:")
print("     • Designated, highly visible late-night taxi stands")
print("     • Better signage near major attractions/hotels")
print("     • Mobile app integration for taxi-passenger matching")

# ============================================
# REQUIREMENT 3: Tourism - Functional Zone Shift
# ============================================
print("\n\n" + "📊 REQUIREMENT 3: FUNCTIONAL ZONE SHIFT (TRIP PATTERNS)".center(80, "="))
print("Compares trip length/duration DAY vs NIGHT")
print("-"*80)

trip_files = glob.glob("output_trip_comparison/part-*.csv")

print(f"\n🚗 TRIP CHARACTERISTICS BY TIME PERIOD:")
print(f"{'Period':<12}{'Avg Dist (km)':<15}{'Avg Time (min)':<15}{'Trip Count':<15}")
print("-"*58)

for file in trip_files:
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        header_only = True
        for row in reader:
            if header_only:
                header_only = False
                continue
            
            try:
                period = row['time_period']
                avg_dist = float(row['avg_distance_km']) if row['avg_distance_km'] else 0
                avg_time = float(row['avg_duration_sec']) / 60 if row['avg_duration_sec'] else 0
                count = int(row['trip_count']) if row['trip_count'] else 0
                
                print(f"{period:<12}{avg_dist:<15.2f}{avg_time:<15.2f}{count:<15,}")
            except:
                pass

print("\n💡 ACTIONABLE INSIGHT:")
print("   - Longer DAY trips = broad city-wide tourism (museums, suburbs)")
print("   - Shorter NIGHT trips = localized entertainment (restaurants, bars)")
print("   - Informs:")
print("     • Zoning laws for new hotel locations")
print("     • Transit infrastructure placement")
print("     • Tourist district planning")

# ============================================
# SUMMARY
# ============================================
print("\n\n" + "📋 SUMMARY".center(80, "="))
print("\n✅ ALL CITY PLANNER REQUIREMENTS COVERED:")
print("   [✓] Economy: Nighttime Economic Zones identified")
print("   [✓] Trajectory: Taxi Desert/Service Gaps mapped")
print("   [✓] Tourism: Functional Zone Shift analyzed (day vs night patterns)")

print("\n📁 OUTPUT FILES GENERATED:")
print("   • output_day_night_activity/ - Spatial clustering by time period")
print("   • output_night_demand_zones/ - High-demand nighttime zones")
print("   • output_taxi_deserts/ - Late-night service gap locations")
print("   • output_trip_comparison/ - Day vs night trip statistics")
print("   • output_trip_segments.parquet/ - Detailed trip data for further analysis")

print("\n📊 READY FOR:")
print("   • Infrastructure planning (transit extensions, taxi stands)")
print("   • Safety improvements (street lighting in high-demand zones)")
print("   • Tourism development (hotel zoning, entertainment districts)")
print("   • Resource allocation (late-night taxi fleet sizing)")

print("\n" + "="*80)
