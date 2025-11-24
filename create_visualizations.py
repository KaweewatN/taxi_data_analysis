"""
Create visualizations for taxi analysis
Requires: pip3 install pandas matplotlib seaborn folium
"""
import pandas as pd
import glob

print("🎨 Creating visualizations...")
print("\nChoose visualization method:")
print("1. Folium Interactive Map (HTML - works without pandas install)")
print("2. Full visualization suite (requires pandas, matplotlib, seaborn)")
print("\nTrying Folium first (most compatible)...\n")

# ============================================
# FOLIUM INTERACTIVE MAP (No pandas required for viewing)
# ============================================

try:
    import folium
    from folium.plugins import HeatMap, MarkerCluster
    
    print("📍 Creating Folium interactive maps...")
    
    # Load data
    demand_files = glob.glob("output_night_demand_zones/part-*.csv")
    demand_data = []
    for f in demand_files:
        df = pd.read_csv(f)
        demand_data.append(df)
    demand = pd.concat(demand_data, ignore_index=True)
    
    # Filter Bangkok area
    demand_bkk = demand[(demand['lat_bin'] > 13.5) & (demand['lat_bin'] < 14.0) &
                        (demand['lon_bin'] > 100.3) & (demand['lon_bin'] < 100.8)]
    
    # Load taxi deserts
    desert_files = glob.glob("output_taxi_deserts/part-*.csv")
    deserts_data = []
    for f in desert_files:
        df = pd.read_csv(f)
        deserts_data.append(df)
    deserts = pd.concat(deserts_data, ignore_index=True)
    
    # ============================================
    # MAP 1: Night Demand Zones
    # ============================================
    m1 = folium.Map(location=[13.75, 100.52], zoom_start=12, tiles='OpenStreetMap')
    
    # Add demand zones as circles
    for _, row in demand_bkk.nlargest(100, 'demand_supply_ratio').iterrows():
        folium.CircleMarker(
            location=[row['lat_bin'], row['lon_bin']],
            radius=min(row['occupied_count']/30, 15),
            color='red' if row['demand_supply_ratio'] > 100 else 'orange',
            fill=True,
            fillOpacity=0.6,
            popup=f"""
                <b>Night Demand Zone</b><br>
                Location: {row['lat_bin']:.3f}, {row['lon_bin']:.3f}<br>
                Occupied: {row['occupied_count']}<br>
                Available: {row['available_count']}<br>
                Demand Ratio: {row['demand_supply_ratio']:.0f}
            """,
            tooltip=f"Demand: {row['demand_supply_ratio']:.0f}"
        ).add_to(m1)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 220px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                padding: 10px">
    <p><b>Night Demand Zones</b></p>
    <p><span style="color:red;">●</span> Extreme Demand (>100)</p>
    <p><span style="color:orange;">●</span> High Demand</p>
    <p>Size = Occupied taxi count</p>
    </div>
    '''
    m1.get_root().html.add_child(folium.Element(legend_html))
    
    m1.save('map1_night_demand.html')
    print("✅ Saved: map1_night_demand.html")
    
    # ============================================
    # MAP 2: Taxi Deserts
    # ============================================
    m2 = folium.Map(location=[13.75, 100.52], zoom_start=11, tiles='CartoDB positron')
    
    # Add desert zones
    for _, row in deserts.iterrows():
        folium.CircleMarker(
            location=[row['lat_bin'], row['lon_bin']],
            radius=min(row['unhired_count']/5, 12),
            color='purple',
            fill=True,
            fillOpacity=0.7,
            popup=f"""
                <b>Taxi Desert Zone</b><br>
                Location: {row['lat_bin']:.3f}, {row['lon_bin']:.3f}<br>
                Unhired Taxis: {row['unhired_count']}<br>
                Total Activity: {row['total_count']}<br>
                Desert Score: {row['desert_score']*100:.1f}%
            """,
            tooltip=f"Desert: {row['desert_score']*100:.0f}%"
        ).add_to(m2)
    
    m2.save('map2_taxi_deserts.html')
    print("✅ Saved: map2_taxi_deserts.html")
    
    # ============================================
    # MAP 3: Combined Overview
    # ============================================
    m3 = folium.Map(location=[13.75, 100.52], zoom_start=12, tiles='OpenStreetMap')
    
    # Add demand zones layer
    demand_layer = folium.FeatureGroup(name='Night Demand Zones')
    for _, row in demand_bkk.nlargest(50, 'demand_supply_ratio').iterrows():
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
    desert_layer = folium.FeatureGroup(name='Taxi Deserts')
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
    
    # Add layer control
    folium.LayerControl().add_to(m3)
    
    m3.save('map3_combined.html')
    print("✅ Saved: map3_combined.html")
    
    print("\n" + "="*60)
    print("✅ INTERACTIVE MAPS CREATED!")
    print("="*60)
    print("\nOpen these HTML files in your browser:")
    print("  🗺️  map1_night_demand.html - Night demand zones")
    print("  🗺️  map2_taxi_deserts.html - Taxi desert zones")
    print("  🗺️  map3_combined.html - Combined view with layers")
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("\n📦 Install required packages:")
    print("   pip3 install folium pandas")
    print("\nThen run this script again.")

print("\n" + "="*60)
print("💡 NEXT STEPS:")
print("="*60)
print("\n1. Open the HTML files in your browser")
print("2. For professional visualizations, try:")
print("   • Kepler.gl: pip3 install keplergl")
print("   • QGIS: https://qgis.org (free GIS software)")
print("   • Tableau Public: https://public.tableau.com")
print("\n3. For static charts (papers/reports):")
print("   pip3 install matplotlib seaborn")
print("   Then create custom charts using the summary CSV files")
