"""
Simple Results Viewer - No dependencies required
View taxi analysis results in terminal
"""
import csv
import glob
from collections import defaultdict

print("="*70)
print("🚖 TAXI DAY/NIGHT ANALYSIS RESULTS")
print("="*70)

# ============================================
# 1. NIGHT DEMAND ZONES
# ============================================
print("\n📊 Loading night demand zones...")
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

# Sort by demand_supply_ratio
demand_data.sort(key=lambda x: x['demand_supply_ratio'], reverse=True)

print(f"\n🌃 TOP 20 NIGHT HIGH-DEMAND ZONES:")
print(f"{'Rank':<6}{'Latitude':<12}{'Longitude':<12}{'Occupied':<12}{'Available':<12}{'Demand/Supply':<15}")
print("-"*70)

for i, zone in enumerate(demand_data[:20], 1):
    print(f"{i:<6}{zone['lat_bin']:<12.3f}{zone['lon_bin']:<12.3f}"
          f"{zone['occupied_count']:<12}{zone['available_count']:<12}"
          f"{zone['demand_supply_ratio']:<15.1f}")

# ============================================
# 2. ACTIVITY BY TIME PERIOD
# ============================================
print("\n\n📊 Loading activity data (sample)...")
activity_files = glob.glob("output_day_night_activity/part-*.csv")[:2]  # First 2 parts

time_counts = defaultdict(int)
status_counts = defaultdict(int)
location_counts = defaultdict(int)

for file in activity_files:
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                time_period = row['time_period']
                status = int(row['for_hire_light'])
                count = int(row['record_count'])
                lat = float(row['lat_bin'])
                lon = float(row['lon_bin'])
                
                time_counts[time_period] += count
                status_counts[status] += count
                
                # Bangkok area filter
                if 13.5 < lat < 14.0 and 100.3 < lon < 100.8:
                    location_counts[(lat, lon)] += count
            except:
                continue

print(f"\n⏰ ACTIVITY BY TIME PERIOD:")
print(f"{'Period':<15}{'Record Count':<15}{'Percentage':<15}")
print("-"*45)
total = sum(time_counts.values())
for period in ['DAY', 'NIGHT', 'OTHER']:
    count = time_counts.get(period, 0)
    pct = (count / total * 100) if total > 0 else 0
    print(f"{period:<15}{count:<15,}{pct:<15.1f}%")

print(f"\n🚖 ACTIVITY BY TAXI STATUS:")
print(f"{'Status':<15}{'Record Count':<15}{'Percentage':<15}")
print("-"*45)
status_labels = {0: 'Occupied', 1: 'Available'}
for status in [0, 1]:
    count = status_counts.get(status, 0)
    pct = (count / total * 100) if total > 0 else 0
    label = status_labels.get(status, str(status))
    print(f"{label:<15}{count:<15,}{pct:<15.1f}%")

# Top active locations
print(f"\n🗺️  TOP 15 MOST ACTIVE LOCATIONS (Bangkok area):")
print(f"{'Rank':<6}{'Latitude':<12}{'Longitude':<12}{'Activity Count':<15}")
print("-"*45)

sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
for i, ((lat, lon), count) in enumerate(sorted_locations[:15], 1):
    print(f"{i:<6}{lat:<12.3f}{lon:<12.3f}{count:<15,}")

# ============================================
# 3. EXPORT SUMMARY
# ============================================
print("\n\n💾 Exporting summary files...")

# Export top demand zones
with open('summary_top_demand_zones.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['rank', 'lat_bin', 'lon_bin', 'occupied_count', 
                                           'available_count', 'demand_supply_ratio'])
    writer.writeheader()
    for i, zone in enumerate(demand_data[:50], 1):
        zone['rank'] = i
        writer.writerow(zone)
print("✅ Saved: summary_top_demand_zones.csv (top 50)")

# Export time summary
with open('summary_time_periods.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time_period', 'record_count', 'percentage'])
    for period in ['DAY', 'NIGHT', 'OTHER']:
        count = time_counts.get(period, 0)
        pct = (count / total * 100) if total > 0 else 0
        writer.writerow([period, count, f'{pct:.2f}'])
print("✅ Saved: summary_time_periods.csv")

# Export top locations
with open('summary_top_locations.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['rank', 'lat_bin', 'lon_bin', 'activity_count'])
    for i, ((lat, lon), count) in enumerate(sorted_locations[:100], 1):
        writer.writerow([i, lat, lon, count])
print("✅ Saved: summary_top_locations.csv (top 100)")

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETE!")
print("="*70)
print("\nSummary files created:")
print("  📋 summary_top_demand_zones.csv - Top 50 high-demand zones")
print("  📋 summary_time_periods.csv - Activity by time period")
print("  📋 summary_top_locations.csv - Top 100 active locations")
print("\n💡 You can open these CSV files in Excel or Google Sheets")
print("💡 For maps, use the lat_bin/lon_bin coordinates in mapping tools")
