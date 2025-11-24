#!/usr/bin/env python3
"""
Bangkok Taxi Analysis - Day vs Night Comparison
Analyzes and visualizes taxi patterns across different time periods
"""

import pandas as pd
import folium
from folium.plugins import HeatMap
import glob

print("=" * 60)
print("🌅🌃 BANGKOK TAXI - DAY vs NIGHT ANALYSIS")
print("=" * 60)

# Load the day/night activity data
print("\n📊 Loading day/night activity data...")
activity_files = glob.glob("output_day_night_activity/part-*.csv")
df = pd.concat([pd.read_csv(f) for f in activity_files])

# Filter to Bangkok area
bangkok = df[(df['lat_bin'] > 13.5) & (df['lat_bin'] < 14.0) &
             (df['lon_bin'] > 100.3) & (df['lon_bin'] < 100.8)]

print(f"✅ Loaded {len(bangkok):,} records")
print(f"\n📈 Records by time period:")
print(bangkok['time_period'].value_counts())

# Analyze DAY period (10:00-16:00)
print("\n" + "=" * 60)
print("🌅 DAY ANALYSIS (10:00-16:00)")
print("=" * 60)

day_data = bangkok[bangkok['time_period'] == 'DAY'].copy()
day_summary = day_data.groupby(['lat_bin', 'lon_bin']).agg({
    'record_count': 'sum',
    'for_hire_light': lambda x: (x == 1).sum()  # Count occupied (for_hire_light=1)
}).reset_index()
day_summary.columns = ['lat_bin', 'lon_bin', 'total_activity', 'occupied_count']
day_summary['available_count'] = day_summary['total_activity'] - day_summary['occupied_count']
day_summary['demand_ratio'] = day_summary['occupied_count'] / (day_summary['available_count'] + 1)

print(f"📍 Total day zones: {len(day_summary):,}")
print(f"🚖 Total day activity: {day_summary['total_activity'].sum():,}")
print(f"\n🔝 Top 5 busiest day zones:")
top_day = day_summary.nlargest(5, 'total_activity')[['lat_bin', 'lon_bin', 'occupied_count', 'total_activity']]
print(top_day)

# Analyze NIGHT period (20:00-02:00)
print("\n" + "=" * 60)
print("🌃 NIGHT ANALYSIS (20:00-02:00)")
print("=" * 60)

night_data = bangkok[bangkok['time_period'] == 'NIGHT'].copy()
night_summary = night_data.groupby(['lat_bin', 'lon_bin']).agg({
    'record_count': 'sum',
    'for_hire_light': lambda x: (x == 1).sum()
}).reset_index()
night_summary.columns = ['lat_bin', 'lon_bin', 'total_activity', 'occupied_count']
night_summary['available_count'] = night_summary['total_activity'] - night_summary['occupied_count']
night_summary['demand_ratio'] = night_summary['occupied_count'] / (night_summary['available_count'] + 1)

print(f"📍 Total night zones: {len(night_summary):,}")
print(f"🚖 Total night activity: {night_summary['total_activity'].sum():,}")
print(f"\n🔝 Top 5 busiest night zones:")
top_night = night_summary.nlargest(5, 'total_activity')[['lat_bin', 'lon_bin', 'occupied_count', 'total_activity']]
print(top_night)

# Create comparison map
print("\n" + "=" * 60)
print("🗺️  CREATING DAY vs NIGHT COMPARISON MAP")
print("=" * 60)

m = folium.Map(location=[13.75, 100.52], zoom_start=12)

# Day activity layer (Blue)
print("\n🌅 Adding day activity layer...")
day_layer = folium.FeatureGroup(name='🌅 Day Activity (10:00-16:00)', show=True)
for _, row in day_summary.nlargest(100, 'total_activity').iterrows():
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=min(row['total_activity']/100, 15),
        color='blue',
        fill=True,
        fillOpacity=0.5,
        popup=f"""
            <b>Day Activity Zone</b><br>
            📍 {row['lat_bin']:.3f}, {row['lon_bin']:.3f}<br>
            🚖 Occupied: {row['occupied_count']}<br>
            🚕 Available: {row['available_count']}<br>
            📊 Total Activity: {row['total_activity']}<br>
            📈 Demand Ratio: {row['demand_ratio']:.1f}
        """,
        tooltip=f"Day: {row['total_activity']} trips"
    ).add_to(day_layer)
day_layer.add_to(m)

# Night activity layer (Orange/Red)
print("🌃 Adding night activity layer...")
night_layer = folium.FeatureGroup(name='🌃 Night Activity (20:00-02:00)', show=True)
for _, row in night_summary.nlargest(100, 'total_activity').iterrows():
    color = 'red' if row['demand_ratio'] > 50 else 'orange'
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=min(row['total_activity']/100, 15),
        color=color,
        fill=True,
        fillOpacity=0.5,
        popup=f"""
            <b>Night Activity Zone</b><br>
            📍 {row['lat_bin']:.3f}, {row['lon_bin']:.3f}<br>
            🚖 Occupied: {row['occupied_count']}<br>
            🚕 Available: {row['available_count']}<br>
            📊 Total Activity: {row['total_activity']}<br>
            📈 Demand Ratio: {row['demand_ratio']:.1f}
        """,
        tooltip=f"Night: {row['total_activity']} trips"
    ).add_to(night_layer)
night_layer.add_to(m)

# Day-only zones (zones busy in day but quiet at night)
print("☀️  Identifying day-dominant zones...")
day_coords = set(zip(day_summary['lat_bin'], day_summary['lon_bin']))
night_coords = set(zip(night_summary['lat_bin'], night_summary['lon_bin']))
day_only = day_summary[day_summary.apply(lambda r: (r['lat_bin'], r['lon_bin']) not in night_coords, axis=1)]

day_only_layer = folium.FeatureGroup(name='☀️ Day-Only Zones', show=False)
for _, row in day_only.nlargest(50, 'total_activity').iterrows():
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=8,
        color='green',
        fill=True,
        fillOpacity=0.6,
        popup=f"Day-only zone: {row['total_activity']} activity",
        tooltip="Day-dominant area"
    ).add_to(day_only_layer)
day_only_layer.add_to(m)

# Night-only zones
print("🌙 Identifying night-dominant zones...")
night_only = night_summary[night_summary.apply(lambda r: (r['lat_bin'], r['lon_bin']) not in day_coords, axis=1)]

night_only_layer = folium.FeatureGroup(name='🌙 Night-Only Zones', show=False)
for _, row in night_only.nlargest(50, 'total_activity').iterrows():
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=8,
        color='purple',
        fill=True,
        fillOpacity=0.6,
        popup=f"Night-only zone: {row['total_activity']} activity",
        tooltip="Night-dominant area"
    ).add_to(night_only_layer)
night_only_layer.add_to(m)

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)

m.save('map_day_night_comparison.html')
print("✅ Saved: map_day_night_comparison.html")

# Summary statistics
print("\n" + "=" * 60)
print("📊 SUMMARY STATISTICS")
print("=" * 60)
print(f"\n🌅 Day zones (10:00-16:00): {len(day_summary):,}")
print(f"   Total activity: {day_summary['total_activity'].sum():,}")
print(f"   Avg activity per zone: {day_summary['total_activity'].mean():.0f}")

print(f"\n🌃 Night zones (20:00-02:00): {len(night_summary):,}")
print(f"   Total activity: {night_summary['total_activity'].sum():,}")
print(f"   Avg activity per zone: {night_summary['total_activity'].mean():.0f}")

print(f"\n☀️  Day-only zones: {len(day_only):,} ({len(day_only)/len(day_summary)*100:.1f}%)")
print(f"🌙 Night-only zones: {len(night_only):,} ({len(night_only)/len(night_summary)*100:.1f}%)")

overlap = len(day_coords & night_coords)
print(f"🔄 Overlap (active both periods): {overlap:,}")

print("\n" + "=" * 60)
print("✅ ANALYSIS COMPLETE!")
print("=" * 60)
print("\n📁 Generated file:")
print("   • map_day_night_comparison.html")
print("\n🗺️  Map layers:")
print("   🌅 Blue circles = Day activity")
print("   🌃 Orange/Red circles = Night activity")
print("   ☀️  Green circles = Day-only zones")
print("   🌙 Purple circles = Night-only zones")
print("\n💡 Toggle layers on/off to compare patterns!")
print("=" * 60)
