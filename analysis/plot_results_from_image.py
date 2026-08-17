import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def make_plots(df, out_path):
    pivot_time = df.pivot(index="nodes", columns="reducers", values="time_s").sort_index()
    baseline = df[(df.nodes == 1) & (df.reducers == 2)]["time_s"].iloc[0]

    # speedup and efficiency pivots
    df_speed = df.copy()
    df_speed["speedup"] = baseline / df_speed["time_s"]
    pivot_speed = df_speed.pivot(index="nodes", columns="reducers", values="speedup").sort_index()

    pivot_eff = pivot_speed.copy()
    for col in pivot_eff.columns:
        pivot_eff[col] = pivot_eff[col] / col * 100.0  # percent

    nodes = pivot_time.index.to_list()
    reducers = pivot_time.columns.to_list()
    x = np.arange(len(nodes))
    width = 0.35
    colors = ["#4C72B0", "#55A868"]

    fig, axs = plt.subplots(1, 3, figsize=(16, 5))
    # Execution time (grouped bars)
    ax = axs[0]
    for i, r in enumerate(reducers):
        ax.bar(x + (i - 0.5) * width, pivot_time[r].values, width,
               label=f"{r} reducers", color=colors[i % len(colors)])
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in nodes])
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Execution time (s)")
    ax.set_title("Execution Time")
    ax.grid(alpha=0.2)
    ax.legend(fontsize="small")

    # Speedup (lines)
    ax = axs[1]
    for i, r in enumerate(reducers):
        ax.plot(x + (i - 0.5) * width, pivot_speed[r].values, marker="o",
                linestyle="-", color=colors[i % len(colors)], label=f"{r} reducers")
        for xi, yi in zip(x + (i - 0.5) * width, pivot_speed[r].values):
            ax.annotate(f"{yi:.2f}x", (xi, yi), textcoords="offset points", xytext=(0,6), ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in nodes])
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Speedup (x)")
    ax.set_title("Speedup vs Baseline (1 node, 2 reducers)")
    ax.grid(alpha=0.2)
    ax.legend(fontsize="small")

    # Efficiency (bar percent)
    ax = axs[2]
    for i, r in enumerate(reducers):
        ax.bar(x + (i - 0.5) * width, pivot_eff[r].values, width,
               label=f"{r} reducers", color=colors[i % len(colors)])
        for xi, yi in zip(x + (i - 0.5) * width, pivot_eff[r].values):
            ax.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points", xytext=(0,6), ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in nodes])
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Efficiency (%)")
    ax.set_title("Parallel Efficiency")
    ax.set_ylim(0, 110)
    ax.grid(alpha=0.2)
    ax.legend(fontsize="small")

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    # Data extracted from your image
    data = {
        "nodes": [1, 1, 2, 2, 3, 3],
        "reducers": [2, 3, 2, 3, 2, 3],
        "time_s": [6, 6, 9, 8, 7, 7]
    }
    df = pd.DataFrame(data)
    out_path = os.path.join("analysis", "results", "execution_time_speedup_efficiency.png")
    make_plots(df, out_path)
    print(f"Saved plot to: {out_path}")