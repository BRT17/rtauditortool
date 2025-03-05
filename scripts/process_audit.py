import pandas as pd
import numpy as np
import sys
import json

def calculate_productivity_score(pet):
    if pet < 0:
        return 0
    elif pet < 70:
        return pet * (1 / 70)
    elif pet < 100:
        return 1 + (pet - 70) * (1 / 30)
    elif pet <= 140:
        return 2 + (pet - 100) * (1 / 40)
    else:
        return 3

def process_audit(file_path):
    # Read the audit CSV, being flexible with column names
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Find the worker name column (case-insensitive)
    name_column = None
    for col in df.columns:
        if col.lower() in ['name', 'worker', 'employee']:
            name_column = col
            break

    if name_column is None:
        print("Could not find a column for worker names. Ensure a column is named 'Name', 'Worker', or 'Employee'")
        return

    # Rename the column to 'Worker' for consistency
    df = df.rename(columns={name_column: 'Worker'})

    # Group by worker
    worker_groups = df.groupby('Worker')
    
    # Results dictionary
    results = {}
    
    for worker, group in worker_groups:
        # Calculate ATP (Actual Throughput)
        atp = len(group)
        
        # Randomly select audit tasks (25%, max 8)
        audit_sample = group.sample(n=min(int(atp * 0.25), 8), random_state=42)
        
        # Check if scoring columns exist
        score_columns = {
            'CE': audit_sample['CE'].mean() if 'CE' in audit_sample.columns else None,
            'INT': audit_sample['INT'].mean() if 'INT' in audit_sample.columns else None,
            'ALI': audit_sample['ALI'].mean() if 'ALI' in audit_sample.columns else None
        }
        
        # Calculate PET and Productivity Score
        # (Placeholder - would need EPT input mechanism)
        pet = 100  # Placeholder - needs EPT input
        productivity_score = calculate_productivity_score(pet)
        
        # Overall Score Calculation
        # Only include scores that exist
        existing_scores = [score for score in score_columns.values() if score is not None]
        overall_score = (sum(existing_scores) + productivity_score) / (len(existing_scores) + 1) if existing_scores else productivity_score
        
        results[worker] = {
            'ATP': atp,
            'Audit Scores': score_columns,
            'Productivity Score': productivity_score,
            'Overall Score': overall_score
        }
    
    # Save results
    result_file = f'results/{file_path.split("/")[-1].replace(".csv", "_results.json")}'
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"Audit processed. Results saved to {result_file}")

if __name__ == '__main__':
    process_audit(sys.argv[1])
```
