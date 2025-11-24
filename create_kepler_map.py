"""
Create interactive Kepler.gl map for taxi analysis
"""
import pandas as pd
from keplergl import KeplerGl
import glob

print("📊 Loading taxi analysis data...")

# Load night demand zones
demand_files = glob.glob("output_night_demand_zones/part-*.csv")
demand = pd.concat([pd.read_csv(f) for f in demand_files])

# Filter Bangkok area
demand_bangkok = demand[(demand['lat_bin'] > 13.5) & (demand['lat_bin'] < 14.0) &
                        (demand['lon_bin'] > 100.3) & (demand['lon_bin'] < 100.8)]

print(f"✅ Loaded {len(demand_bangkok)} night demand zones in Bangkok")

# Load taxi deserts
desert_files = glob.glob("output_taxi_deserts/part-*.csv")
deserts = pd.concat([pd.read_csv(f) for f in desert_files])

print(f"✅ Loaded {len(deserts)} taxi desert zones")

# Load activity data (sample)
activity_files = glob.glob("output_day_night_activity/part-*.csv")[:2]
activity = pd.concat([pd.read_csv(f) for f in activity_files])
activity_bkk = activity[(activity['lat_bin'] > 13.5) & (activity['lat_bin'] < 14.0) &
                        (activity['lon_bin'] > 100.3) & (activity['lon_bin'] < 100.8)]

print(f"✅ Loaded {len(activity_bkk)} activity records (sample)")

# Create Kepler.gl map
print("\n🗺️  Creating interactive map...")
map_1 = KeplerGl(height=800, data={
    'Night Demand Zones': demand_bangkok,
    'Taxi Deserts': deserts,
    'Activity Heatmap': activity_bkk
})

# Save as HTML
output_file = 'kepler_taxi_analysis.html'
map_1.save_to_html(file_name=output_file)

print("\n" + "="*60)
print("✅ SUCCESS! Interactive map created!")
print("="*60)
print(f"\n📁 File: {output_file}")
print(f"📍 Location: /Users/phonchana/Desktop/SeniorProject/taxi_data_analysis/")
print("\n💡 TO VIEW:")
print(f"   1. Open Finder")
print(f"   2. Navigate to: ~/Desktop/SeniorProject/taxi_data_analysis/")
print(f"   3. Double-click: {output_file}")
print(f"\n   OR just run: open {output_file}")
print("\n🎨 FEATURES:")
print("   • Zoom/pan the map")
print("   • Toggle layers on/off")
print("   • Click points for details")
print("   • Adjust colors and sizes")
print("   • Export as image or share")
print("="*60)
