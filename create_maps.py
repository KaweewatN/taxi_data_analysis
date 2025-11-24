#!/usr/bin/env python3
"""
Bangkok Taxi Analysis - Interactive Map Generator
Generates 3 interactive HTML maps using Folium
"""

import pandas as pd
import folium
import glob

print("=" * 60)
print("🗺️  BANGKOK TAXI ANALYSIS - MAP GENERATOR")
print("=" * 60)

# Step 1: Load night demand zones
print("\n📊 Loading data...")
demand_files = glob.glob("output_night_demand_zones/part-*.csv")
demand = pd.concat([pd.read_csv(f) for f in demand_files])
demand_bangkok = demand[(demand['lat_bin'] > 13.5) & (demand['lat_bin'] < 14.0) &
                        (demand['lon_bin'] > 100.3) & (demand['lon_bin'] < 100.8)]

# Load taxi deserts
desert_files = glob.glob("output_taxi_deserts/part-*.csv")
deserts = pd.concat([pd.read_csv(f) for f in desert_files])

print(f"✅ Loaded {len(demand_bangkok):,} night demand zones (Bangkok)")
print(f"✅ Loaded {len(deserts):,} taxi desert zones")
print(f"\n🔝 Top 5 demand zones:")
print(demand_bangkok.nlargest(5, 'demand_supply_ratio')[['lat_bin', 'lon_bin', 'occupied_count', 'demand_supply_ratio']])

# Map 1: Night Demand Zones
print("\n🌃 Creating Map 1: Night Demand Zones...")
m1 = folium.Map(location=[13.75, 100.52], zoom_start=12, tiles='OpenStreetMap')

for _, row in demand_bangkok.nlargest(100, 'demand_supply_ratio').iterrows():
    color = 'red' if row['demand_supply_ratio'] > 100 else 'orange'
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=min(row['occupied_count']/30, 15),
        color=color,
        fill=True,
        fillOpacity=0.6,
        popup=f"""
            <b>Night Demand Zone</b><br>
            📍 Location: {row['lat_bin']:.3f}, {row['lon_bin']:.3f}<br>
            🚖 Occupied: {row['occupied_count']}<br>
            🚕 Available: {row['available_count']}<br>
            📊 Demand Ratio: {row['demand_supply_ratio']:.0f}
        """,
        tooltip=f"Demand: {row['demand_supply_ratio']:.0f}"
    ).add_to(m1)

m1.save('map1_night_demand.html')
print("✅ Saved: map1_night_demand.html")

# Map 2: Taxi Deserts
print("\n🚕 Creating Map 2: Taxi Deserts...")
m2 = folium.Map(location=[13.75, 100.52], zoom_start=11, tiles='CartoDB positron')

for _, row in deserts.iterrows():
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=min(row['unhired_count']/5, 12),
        color='purple',
        fill=True,
        fillOpacity=0.7,
        popup=f"""
            <b>Taxi Desert Zone</b><br>
            📍 Location: {row['lat_bin']:.3f}, {row['lon_bin']:.3f}<br>
            🚕 Unhired Taxis: {row['unhired_count']}<br>
            📊 Total Activity: {row['total_count']}<br>
            ⚠️ Desert Score: {row['desert_score']*100:.1f}%
        """,
        tooltip=f"Desert: {row['desert_score']*100:.0f}%"
    ).add_to(m2)

m2.save('map2_taxi_deserts.html')
print("✅ Saved: map2_taxi_deserts.html")

# Map 3: Combined View
print("\n🗺️  Creating Map 3: Combined View...")
m3 = folium.Map(location=[13.75, 100.52], zoom_start=12)

# Add demand zones layer
demand_layer = folium.FeatureGroup(name='🌃 Night Demand Zones', show=True)
for _, row in demand_bangkok.nlargest(50, 'demand_supply_ratio').iterrows():
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=8,
        color='red',
        fill=True,
        fillOpacity=0.5,
        popup=f"Demand: {row['demand_supply_ratio']:.0f}"
    ).add_to(demand_layer)
demand_layer.add_to(m3)

# Add desert zones layer
desert_layer = folium.FeatureGroup(name='🚕 Taxi Deserts', show=True)
for _, row in deserts.nlargest(30, 'desert_score').iterrows():
    folium.CircleMarker(
        location=[row['lat_bin'], row['lon_bin']],
        radius=6,
        color='blue',
        fill=True,
        fillOpacity=0.5,
        popup=f"Desert: {row['desert_score']*100:.0f}%"
    ).add_to(desert_layer)
desert_layer.add_to(m3)

folium.LayerControl(collapsed=False).add_to(m3)

m3.save('map3_combined.html')
print("✅ Saved: map3_combined.html")

print("\n" + "=" * 60)
print("✅ ALL MAPS CREATED SUCCESSFULLY!")
print("=" * 60)
print("\n📁 Generated files:")
print("   • map1_night_demand.html - Night demand zones")
print("   • map2_taxi_deserts.html - Taxi desert zones")
print("   • map3_combined.html - Combined view with layers")
print("\n💡 To view: Run 'open map1_night_demand.html' or double-click any HTML file")
print("=" * 60)
