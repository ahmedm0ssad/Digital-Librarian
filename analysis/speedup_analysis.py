import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def load_benchmark(csv_path):
    df = pd.read_csv(csv_path)
    print("data loaded successfully:")
    print(df)

    # Calculate speedup relative to baseline (1 reducer)
    baseline_time = df[df['reducers'] == 1]['execution_time_seconds'].values[0]
    df['speedup'] = baseline_time / df['execution_time_seconds']

    return df
def plot_speedup(df, output_path):

    df_result = df.copy()
    df_result['cluster_size'] = df_result['reducers']
    
    results_text = ""
    results_text += "="*60 + "\n"
    results_text += "EXECUTION TIME VS CLUSTER SIZE\n"
    results_text += "="*60 + "\n"
    results_text += "reducers  execution_time_seconds  speedup\n"
    for _, row in df_result.iterrows():
        results_text += f"{int(row['reducers'])}         {row['execution_time_seconds']:.1f}                     {row['speedup']:.2f}x\n"

    print("\n" + "="*60)
    print("EXECUTION TIME VS CLUSTER SIZE")
    print("="*60)
    print("reducers  execution_time_seconds  speedup")
    for _, row in df_result.iterrows():
        print(f"{int(row['reducers'])}         {row['execution_time_seconds']:.1f}                     {row['speedup']:.2f}x")
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_result['cluster_size'], df_result['execution_time_seconds'], 'bo-', linewidth=2, markersize=10, label='execution time')

    plt.xlabel('number of reducers', fontsize=12)
    plt.ylabel('execution time (seconds)', fontsize=12)
    plt.title('scalability analysis: execution time vs reducers', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()

    for _, row in df_result.iterrows():
        plt.annotate(f'{row["execution_time_seconds"]:.1f}s',
                    (row['cluster_size'], row['execution_time_seconds']),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center',
                    fontsize=10)

    plt.xticks(df_result['cluster_size'])

    plt.ylim(0, max(df_result['execution_time_seconds']) * 1.2)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\ngraph saved to: {output_path}")

    return df_result, results_text

def analyze_efficiency(df_result):
    baseline = df_result[df_result['reducers'] == 1]['execution_time_seconds'].values[0]
    
    results_text = "\n" + "="*60 + "\n"
    results_text += "EFFICIENCY ANALYSIS\n"
    results_text += "="*60 + "\n"
    
    print("\n" + "="*60)
    print("EFFICIENCY ANALYSIS")

    print("="*60)
    
    for _, row in df_result.iterrows():
        if row['reducers'] > 1:
            speedup = row['speedup']
            efficiency = (speedup / row['reducers']) * 100
            overhead = 100 - efficiency
            line = f"{int(row['reducers'])} reducers: {efficiency:.1f}% efficient, {overhead:.1f}% overhead"
            line2 = f"   speedup: {speedup:.2f}x (ideal: {row['reducers']:.0f}x)"

            print(line)
            print(line2)

            results_text += line + "\n"
            results_text += line2 + "\n"
    
    if len(df_result) >= 2 and 2 in df_result['reducers'].values:
        t1 = baseline
        t2 = df_result[df_result['reducers'] == 2]['execution_time_seconds'].values[0]
        
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
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "results", "benchmark_results.csv")
    output_path = os.path.join(script_dir, "results", "speedup_graph.png")
    results_file = os.path.join(script_dir, "results", "speedup_results.txt")
    
    print(f"results will be saved to: {results_file}")
    
    if not os.path.exists(csv_path):
        print(f"Error: csv file not found: {csv_path}")
        print("Run benchmark.sh first to generate results.")
        exit(1)

    try:
        df = load_benchmark(csv_path)
        df_result, speedup_text = plot_speedup(df, output_path)
        efficiency_text = analyze_efficiency(df_result)
        
        final_results = speedup_text + efficiency_text
        final_results += "\n" + "="*60 + "\n"
        final_results += "analysis complete\n"
        final_results += "="*60 + "\n"

        print("\n" + "="*60)
        print("analysis complete")
        print("="*60)

        # Ensure results directory exists
        os.makedirs(os.path.dirname(results_file), exist_ok=True)

        with open(results_file, 'w', encoding='utf-8') as f:
            f.write(final_results)

        print(f"\nresults saved to: {results_file}")
        print(f"graph saved to: {output_path}")

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        exit(1)