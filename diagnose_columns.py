"""
Diagnose the parquet file column mapping issue
"""
import pyarrow.parquet as pq

table = pq.read_table('processed_taxi_data.parquet')

print("Column names and their first 3 values:\n")
for col_name in table.column_names:
    col = table.column(col_name)
    print(f"\n{col_name} ({col.type}):")
    for i in range(min(3, len(col))):
        try:
            if col_name == 'timestamp':
                val = col[i].value  # nanoseconds
            else:
                val = col[i].as_py()
            print(f"  [{i}] {val}")
        except Exception as e:
            print(f"  [{i}] ERROR: {e}")

print("\n" + "="*60)
print("ANALYSIS:")
print("- timestamp column has value '1' (WRONG - should be actual timestamps)")
print("- lat column has timestamp strings (WRONG - should be latitude floats)")
print("\nLikely issue: The data preprocessing created wrong column mappings.")
print("The 'lat' column appears to contain the actual timestamp data.")
