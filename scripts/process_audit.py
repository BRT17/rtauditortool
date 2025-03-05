import pandas as pd
import numpy as np
import sys

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
    # Read the audit CSV
    df = pd.read_csv(file_path)
    
    # Group by worker
    worker_groups = df.groupby('Worker')
    
    # Results dictionary
    results = {}
    
    for worker, group in worker_groups:
        # Calculate ATP (Actual Throughput)
        atp = len(group)
        
        # Randomly select audit tasks (25%, max 8)
        audit_sample = group.sample(n=min(int(atp * 0.25), 8), random_state=42)
        
        # Calculate audit scores
        audit_scores = {
            'CE': audit_sample['CE'].mean(),
            'INT': audit_sample['INT'].mean(),
            'ALI': audit_sample['ALI'].mean()
        }
        
        # Calculate PET and Productivity Score
        # (You'd need to add EPT input mechanism)
        pet = 100  # Placeholder - needs EPT input
        productivity_score = calculate_productivity_score(pet)
        
        # Overall Score Calculation
        overall_score = (audit_scores['CE'] + audit_scores['INT'] + 
                         audit_scores['ALI'] + productivity_score) / 2
        
        results[worker] = {
            'ATP': atp,
            'Audit Scores': audit_scores,
            'Productivity Score': productivity_score,
            'Overall Score': overall_score
        }
    
    # Save results
    result_file = f'results/{file_path.split("/")[-1].replace(".csv", "_results.json")}')
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    process_audit(sys.argv[1])
