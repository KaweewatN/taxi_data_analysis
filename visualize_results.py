"""
Visualize Day/Night Taxi Analysis Results
Creates interactive maps and summary statistics
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("📊 Loading results...")

# Load night demand zones
demand_files = glob.glob("output_night_demand_zones/part-*.csv")
demand = pd.concat([pd.read_csv(f) for f in demand_files if Path(f).stat().st_size > 100])
print(f"✅ Loaded {len(demand):,} night demand zones")

# Load day/night activity (sample first part only to avoid memory issues)
activity_files = glob.glob("output_day_night_activity/part-*.csv")[:3]  # First 3 parts
activity = pd.concat([pd.read_csv(f) for f in activity_files])
print(f"✅ Loaded {len(activity):,} activity records (sample)")

# ============================================
# 1. SUMMARY STATISTICS
# ============================================
print("\n" + "="*60)
print("📈 SUMMARY STATISTICS")
print("="*60)

print("\n🌃 TOP 10 NIGHT HIGH-DEMAND ZONES:")
print("(High occupied count, low available taxis)")
top_demand = demand.nlargest(10, 'demand_supply_ratio')[
    ['lat_bin', 'lon_bin', 'occupied_count', 'available_count', 'demand_supply_ratio']
]
print(top_demand.to_string(index=False))

print("\n📊 Activity by Time Period:")
time_summary = activity.groupby('time_period')['record_count'].sum().sort_values(ascending=False)
print(time_summary)

print("\n🚖 Activity by Taxi Status:")
status_summary = activity.groupby('for_hire_light')['record_count'].sum()
status_labels = {0: 'Occupied', 1: 'Available'}
for status, count in status_summary.items():
    print(f"  {status_labels.get(status, status)}: {count:,}")

# ============================================
# 2. VISUALIZATIONS
# ============================================
print("\n📊 Creating visualizations...")

# Figure 1: Night Demand Zones Heatmap
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top left: Demand zones scatter
ax1 = axes[0, 0]
scatter = ax1.scatter(demand['lon_bin'], demand['lat_bin'], 
                     c=demand['demand_supply_ratio'], 
                     s=demand['occupied_count']/10,
                     cmap='YlOrRd', alpha=0.6, edgecolors='black', linewidth=0.5)
ax1.set_xlabel('Longitude', fontsize=12)
ax1.set_ylabel('Latitude', fontsize=12)
ax1.set_title('Night High-Demand Zones\n(Size = occupied count, Color = demand/supply ratio)', 
              fontsize=14, fontweight='bold')
plt.colorbar(scatter, ax=ax1, label='Demand/Supply Ratio')
ax1.grid(True, alpha=0.3)

# Top right: Top 20 demand zones bar chart
ax2 = axes[0, 1]
top_20 = demand.nlargest(20, 'demand_supply_ratio').copy()
top_20['location'] = top_20['lat_bin'].astype(str) + ', ' + top_20['lon_bin'].astype(str)
top_20 = top_20.sort_values('demand_supply_ratio')
ax2.barh(range(len(top_20)), top_20['demand_supply_ratio'], color='crimson')
ax2.set_yticks(range(len(top_20)))
ax2.set_yticklabels(top_20['location'], fontsize=8)
ax2.set_xlabel('Demand/Supply Ratio', fontsize=12)
ax2.set_title('Top 20 Highest Demand Zones (Night)', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Bottom left: Activity by time period
ax3 = axes[1, 0]
time_counts = activity.groupby('time_period')['record_count'].sum().sort_values()
colors = {'DAY': 'gold', 'NIGHT': 'navy', 'OTHER': 'gray'}
bar_colors = [colors.get(tp, 'gray') for tp in time_counts.index]
ax3.bar(time_counts.index, time_counts.values, color=bar_colors, edgecolor='black')
ax3.set_ylabel('Total Records', fontsize=12)
ax3.set_title('Activity Count by Time Period', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
for i, v in enumerate(time_counts.values):
    ax3.text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

# Bottom right: Occupied vs Available
ax4 = axes[1, 1]
status_counts = activity.groupby('for_hire_light')['record_count'].sum()
labels = ['Occupied (0)', 'Available (1)']
colors_status = ['#ff6b6b', '#4ecdc4']
wedges, texts, autotexts = ax4.pie(status_counts.values, labels=labels, autopct='%1.1f%%',
                                     colors=colors_status, startangle=90,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'})
ax4.set_title('Taxi Status Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('analysis_summary.png', dpi=300, bbox_inches='tight')
print("✅ Saved: analysis_summary.png")

# Figure 2: Spatial distribution map
fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Filter Bangkok area (approximate bounds)
bangkok_activity = activity[(activity['lat_bin'] > 13.5) & (activity['lat_bin'] < 14.0) &
                           (activity['lon_bin'] > 100.3) & (activity['lon_bin'] < 100.8)]

# Aggregate by location
location_counts = bangkok_activity.groupby(['lat_bin', 'lon_bin'])['record_count'].sum().reset_index()

scatter = ax.scatter(location_counts['lon_bin'], location_counts['lat_bin'],
                    c=location_counts['record_count'],
                    s=location_counts['record_count']/100,
                    cmap='plasma', alpha=0.6, edgecolors='black', linewidth=0.5)
ax.set_xlabel('Longitude', fontsize=14)
ax.set_ylabel('Latitude', fontsize=14)
ax.set_title('Bangkok Taxi Activity Heatmap\n(Size and color = activity count)', 
            fontsize=16, fontweight='bold')
plt.colorbar(scatter, ax=ax, label='Activity Count')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('bangkok_heatmap.png', dpi=300, bbox_inches='tight')
print("✅ Saved: bangkok_heatmap.png")

# Figure 3: Day vs Night comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for idx, period in enumerate(['DAY', 'NIGHT']):
    ax = axes[idx]
    period_data = activity[activity['time_period'] == period]
    
    if len(period_data) > 0:
        location_agg = period_data.groupby(['lat_bin', 'lon_bin'])['record_count'].sum().reset_index()
        # Filter Bangkok area
        location_agg = location_agg[(location_agg['lat_bin'] > 13.5) & (location_agg['lat_bin'] < 14.0) &
                                   (location_agg['lon_bin'] > 100.3) & (location_agg['lon_bin'] < 100.8)]
        
        scatter = ax.scatter(location_agg['lon_bin'], location_agg['lat_bin'],
                           c=location_agg['record_count'],
                           s=location_agg['record_count']/50,
                           cmap='YlOrRd' if period == 'DAY' else 'Blues',
                           alpha=0.7, edgecolors='black', linewidth=0.5)
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title(f'{period} Activity Hotspots', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax, label='Activity Count')
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('day_vs_night_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Saved: day_vs_night_comparison.png")

# ============================================
# 3. EXPORT SUMMARY CSV
# ============================================
print("\n💾 Exporting summary data...")

# Export top demand zones
top_demand.to_csv('summary_top_demand_zones.csv', index=False)
print("✅ Saved: summary_top_demand_zones.csv")

# Export time period summary
time_summary.to_csv('summary_time_periods.csv', header=True)
print("✅ Saved: summary_time_periods.csv")

print("\n" + "="*60)
print("✅ VISUALIZATION COMPLETE!")
print("="*60)
print("\nGenerated files:")
print("  📊 analysis_summary.png - Overview with 4 charts")
print("  🗺️  bangkok_heatmap.png - Spatial activity distribution")
print("  🌓 day_vs_night_comparison.png - Day vs Night side-by-side")
print("  📋 summary_top_demand_zones.csv - Top demand zones data")
print("  📋 summary_time_periods.csv - Activity by time period")
print("\n💡 Open the PNG files to view the visualizations!")
