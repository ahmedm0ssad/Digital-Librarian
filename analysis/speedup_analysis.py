import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def load_benchmark(csv_path):
    """Load benchmark data from CSV"""
    df = pd.read_csv(csv_path)
    print("data loaded successfully:")
    print(df)
    return df

def save_results_to_file(results_text, output_dir):
    """Save text results to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f"analysis_results_{timestamp}.txt")
    
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write(results_text)
    
    print(f"\nresults saved to: {results_file}")
    return results_file

def plot_speedup(df, output_path):
    """Compute speedup and create visualization"""
    # Get baseline time with 1 reducer
    baseline = df[df['reducers'] == 1]['execution_time_seconds'].values[0]
    
    # Calculate speedup
    df['speedup'] = baseline / df['execution_time_seconds']
    df['ideal_speedup'] = df['reducers']
    
    # Create results text
    results_text = ""
    results_text += "="*60 + "\n"
    results_text += "SPEEDUP ANALYSIS RESULTS\n"
    results_text += "="*60 + "\n"
    results_text += df.to_string(index=False) + "\n"
    results_text += f"\nbaseline time (1 reducer): {baseline:.2f} seconds\n"
    
    # Print to terminal
    print("\n" + "="*60)
    print("SPEEDUP ANALYSIS RESULTS")
    print("="*60)
    print(df.to_string(index=False))
    print(f"\nbaseline time (1 reducer): {baseline:.2f} seconds")
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['reducers'], df['speedup'], 'bo-', linewidth=2, markersize=10, label='actual speedup')
    plt.plot(df['reducers'], df['ideal_speedup'], 'r--', linewidth=2, label='ideal speedup (linear)')
    
    # Add labels and title
    plt.xlabel('number of reducers', fontsize=12)
    plt.ylabel('speedup factor', fontsize=12)
    plt.title('scalability analysis: speedup vs number of reducers', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add value labels on points
    for i, row in df.iterrows():
        plt.annotate(f'{row["speedup"]:.2f}x\n({row["execution_time_seconds"]:.1f}s)', 
                    (row['reducers'], row['speedup']),
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center',
                    fontsize=9)
    
    # Save plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\ngraph saved to: {output_path}")
    
    # Show plot
    plt.show()
    
    return df, results_text

def analyze_efficiency(df):
    """Analyze efficiency and overhead"""
    baseline = df[df['reducers'] == 1]['execution_time_seconds'].values[0]
    
    results_text = "\n" + "="*60 + "\n"
    results_text += "EFFICIENCY ANALYSIS\n"
    results_text += "="*60 + "\n"
    
    print("\n" + "="*60)
    print("EFFICIENCY ANALYSIS")
    print("="*60)
    
    for _, row in df.iterrows():
        if row['reducers'] > 1:
            speedup = row['speedup']
            efficiency = (speedup / row['reducers']) * 100
            overhead = 100 - efficiency
            line = f"{row['reducers']} reducers: {efficiency:.1f}% efficient, {overhead:.1f}% overhead"
            line2 = f"   speedup: {speedup:.2f}x (ideal: {row['reducers']:.0f}x)"
            
            print(line)
            print(line2)
            
            results_text += line + "\n"
            results_text += line2 + "\n"
    
    # Calculate serial fraction using Amdahl's Law
    if len(df) >= 3:
        t1 = baseline
        t2 = df[df['reducers'] == 2]['execution_time_seconds'].values[0]
        
        # Estimate parallelizable fraction from 1->2 speedup
        s = t1/t2
        p = (s - 1)/(s * (1 - 1/2))
        if 0 <= p <= 1:
            results_text += "\n" + "="*60 + "\n"
            results_text += "AMDAHL'S LAW ANALYSIS\n"
            results_text += "="*60 + "\n"
            results_text += f"parallelizable fraction (p): {p*100:.1f}%\n"
            results_text += f"serial fraction (1-p): {(1-p)*100:.1f}%\n"
            results_text += f"maximum theoretical speedup with infinite reducers: {1/(1-p):.2f}x\n"
            
            print("\n" + "="*60)
            print("AMDAHL'S LAW ANALYSIS")
            print("="*60)
            print(f"parallelizable fraction (p): {p*100:.1f}%")
            print(f"serial fraction (1-p): {(1-p)*100:.1f}%")
            print(f"maximum theoretical speedup with infinite reducers: {1/(1-p):.2f}x")
    
    return results_text

if __name__ == "__main__":
    # File paths
    csv_path = os.path.join("results", "benchmark_results.csv")
    output_path = os.path.join("results", "speedup_graph.png")
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"csv file not found: {csv_path}")
    else:
        # Load data
        df = load_benchmark(csv_path)
        
        # Create plot and get results text
        df_result, speedup_text = plot_speedup(df, output_path)
        
        # Analyze efficiency
        efficiency_text = analyze_efficiency(df_result)
        
        # Combine all results
        final_results = speedup_text + efficiency_text
        final_results += "\n" + "="*60 + "\n"
        final_results += "analysis done\n"
        final_results += "="*60 + "\n"
        
        print("\n" + "="*60)
        print("analysis done")
        print("="*60)
        
        # Save results to file
        save_results_to_file(final_results, "results")