from __future__ import annotations
import os
import pandas as pd

# Optional dependencies
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def write_reports(df: pd.DataFrame, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)
    charts_dir = os.path.join(outdir, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    # CSV
    df.to_csv(os.path.join(outdir, "results.csv"), index=False)

    # Summary stats
    summary_lines = []
    summary_lines.append(f"# Eval Summary\n")
    summary_lines.append(f"- Cases: **{len(df)}**\n")
    summary_lines.append(f"- Disagreement rate: **{df['disagreement'].mean():.2%}**\n")

    for col in ["pass_instruction", "pass_correctness", "pass_safety", "pass_style"]:
        summary_lines.append(f"- {col}: **{df[col].mean():.2%}**\n")

    if "pass_json" in df.columns and df["pass_json"].notna().any():
        summary_lines.append(f"- pass_json: **{df['pass_json'].dropna().mean():.2%}**\n")

    # Latency
    if "latency_s" in df.columns:
        summary_lines.append(f"\n## Latency\n")
        summary_lines.append(f"- p50: **{df['latency_s'].median():.3f}s**\n")
        summary_lines.append(f"- p95: **{df['latency_s'].quantile(0.95):.3f}s**\n")

    # Breakdowns
    summary_lines.append("\n## Breakdown by task_type\n")
    bt = df.groupby("task_type")[["pass_instruction","pass_correctness","pass_safety","pass_style"]].mean()
    if HAS_TABULATE:
        summary_lines.append(bt.to_markdown())
    else:
        summary_lines.append(str(bt))
    summary_lines.append("\n\n## Breakdown by language\n")
    bl = df.groupby("language")[["pass_instruction","pass_correctness","pass_safety","pass_style"]].mean()
    if HAS_TABULATE:
        summary_lines.append(bl.to_markdown())
    else:
        summary_lines.append(str(bl))
    summary_lines.append("\n")

    with open(os.path.join(outdir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    # Charts: one per metric (no manual colors)
    if HAS_MATPLOTLIB:
        for metric in ["pass_instruction", "pass_correctness", "pass_safety", "pass_style"]:
            plt.figure()
            df.groupby("task_type")[metric].mean().plot(kind="bar")
            plt.title(f"{metric} by task_type")
            plt.ylabel("pass rate")
            plt.tight_layout()
            plt.savefig(os.path.join(charts_dir, f"{metric}_by_task.png"))
            plt.close()

        # Disagreement chart
        plt.figure()
        df.groupby("task_type")["disagreement"].mean().plot(kind="bar")
        plt.title("disagreement rate by task_type")
        plt.ylabel("rate")
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "disagreement_by_task.png"))
        plt.close()
