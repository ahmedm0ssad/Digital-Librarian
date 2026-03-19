import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def load_benchmark(csv_path):
    df = pd.read_csv(csv_path)
    print("data loaded successfully:")
    print(df)
    return df
def plot_execution_time_vs_cluster(df, output_path):
    
    df['cluster_size'] = df['reducers']
    
    results_text = ""
    results_text += "="*60 + "\n"
    results_text += "EXECUTION TIME VS CLUSTER SIZE\n"
    results_text += "="*60 + "\n"
    results_text += "cluster_size  execution_time_seconds\n"
    for _, row in df.iterrows():
        results_text += f"{int(row['cluster_size'])}            {row['execution_time_seconds']:.1f}\n"
    
    print("\n" + "="*60)
    print("EXECUTION TIME VS CLUSTER SIZE")
    print("="*60)
    print("cluster_size  execution_time_seconds")
    for _, row in df.iterrows():
        print(f"{int(row['cluster_size'])}            {row['execution_time_seconds']:.1f}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['cluster_size'], df['execution_time_seconds'], 'bo-', linewidth=2, markersize=10, label='execution time')
    
    plt.xlabel('cluster size (nodes)', fontsize=12)
    plt.ylabel('execution time (seconds)', fontsize=12)
    plt.title('scalability analysis: execution time vs cluster size', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    for _, row in df.iterrows():
        plt.annotate(f'{row["execution_time_seconds"]:.1f}s', 
                    (row['cluster_size'], row['execution_time_seconds']),
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center',
                    fontsize=10)
    
    plt.xticks(df['cluster_size'])
    
    plt.ylim(0, max(df['execution_time_seconds']) * 1.2)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\ngraph saved to: {output_path}")
    
    return results_text

def analyze_efficiency(df):
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
    
    if len(df) >= 3:
        t1 = baseline
        t2 = df[df['reducers'] == 2]['execution_time_seconds'].values[0]
        
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
    current_dir = os.getcwd()
    print(f"current directory: {current_dir}")
    
    csv_path = os.path.join("analysis", "results", "benchmark_results.csv")
    output_path = os.path.join(current_dir, "speedup_graph.png")
    results_file = os.path.join(current_dir, "speedup_results.txt")
    
    print(f"results will be saved to: {results_file}")
    
    if not os.path.exists(csv_path):
        print(f"csv file not found: {csv_path}")
    else:
        df = load_benchmark(csv_path)
        df_result, speedup_text = plot_speedup(df, output_path)
        efficiency_text = analyze_efficiency(df_result)
        
        final_results = speedup_text + efficiency_text
        final_results += "\n" + "="*60 + "\n"
        final_results += "analysis done\n"
        final_results += "="*60 + "\n"
        
        print("\n" + "="*60)
        print("analysis done")
        print("="*60)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write(final_results)
        
        print(f"\nresults saved to: {results_file}")