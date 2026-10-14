from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

LABEL_MAT = "(a) Matrix + array"
LABEL_ADJ = "(b) Adj. list + min-heap"
COLOR_MAT = "#d1495b"
COLOR_ADJ = "#00798c"
OUT_DIR = "data/results"
CSV_PATH = "data/results/runtimes.csv"
DIRECTED = True


def load(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"num_vertices": "V", "num_edges": "E"})
    df = df.groupby(["V", "E"], as_index=False)[["runtime_mat", "runtime_adj"]].mean()
    max_e = df["V"] * (df["V"] - 1) / (1 if DIRECTED else 2)
    df["density"] = df["E"] / max_e
    return df


def save(fig, out, name, fmt):
    path = out / f"{name}.{fmt}"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {path}")


def plot_time_vs_V(df, out, fmt):
    """
    Graph 1: time vs V, one panel per density band.
    """
    n_bands = min(5, df["density"].nunique())

    if n_bands < 1:
        return

    if n_bands == 1:
        df = df.assign(band="all densities")

    else:
        df = df.assign(band=pd.qcut(df["density"], n_bands, duplicates="drop"))

    bands = df["band"].unique()
    fig, axes = plt.subplots(1, len(bands), figsize=(5 * len(bands), 4.2), squeeze=False)
    
    for ax, band in zip(axes[0], sorted(bands, key=str)):
        d = df[df["band"] == band].groupby("V", as_index=False).mean(numeric_only=True)
        ax.plot(d["V"], d["runtime_mat"], "o-", color=COLOR_MAT, label=LABEL_MAT)
        ax.plot(d["V"], d["runtime_adj"], "s-", color=COLOR_ADJ, label=LABEL_ADJ)
        title = band if isinstance(band, str) else f"density {band.left:.3f}–{band.right:.3f}"
        ax.set_title(title)
        ax.set_xlabel("|V|")
        ax.set_ylabel("Runtime (s)")
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle("Runtime vs |V| by graph density")
    save(fig, out, "1_time_vs_V", fmt)


def plot_time_vs_E(df, out, fmt):
    """Graph 2: time vs E at fixed V — shows the crossover."""
    counts = df.groupby("V")["E"].nunique()
    vs = counts[counts >= 3].index.tolist()
    if not vs:
        print("  skipped time_vs_E: no V value has 3+ different edge counts")
        return
    vs = vs[-4:]
    fig, axes = plt.subplots(1, len(vs), figsize=(5 * len(vs), 4.2), squeeze=False)
    for ax, v in zip(axes[0], vs):
        d = df[df["V"] == v].sort_values("E")
        ax.plot(d["E"], d["runtime_mat"], "o-", color=COLOR_MAT, label=LABEL_MAT)
        ax.plot(d["E"], d["runtime_adj"], "s-", color=COLOR_ADJ, label=LABEL_ADJ)
        # Mark the first point where the heap version becomes slower.
        slower = d[d["runtime_adj"] > d["runtime_mat"]]
        if not slower.empty and len(slower) < len(d):
            x_cross = slower["E"].iloc[0]
            ax.axvline(x_cross, ls="--", color="grey", alpha=0.7)
            ax.text(x_cross, 0.5, " crossover", transform=ax.get_xaxis_transform(),
                    rotation=90, va="center", ha="left", fontsize=9, color="grey")
        ax.set_title(f"|V| = {v}")
        ax.set_xlabel("|E|")
        ax.set_ylabel("Runtime (s)")
        ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 3))
        ax.grid(alpha=0.3)
        ax.legend(loc="upper left", fontsize=9)
    fig.suptitle("Runtime vs |E| at fixed |V|")
    save(fig, out, "2_time_vs_E", fmt)


def plot_normalized(df, out, fmt):
    """Graph 3: runtime divided by the theoretical bound — should level off."""
    d = df.copy()
    d["norm_mat"] = d["runtime_mat"] / d["V"] ** 2
    d["norm_adj"] = d["runtime_adj"] / ((d["V"] + d["E"]) * np.log2(d["V"]))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].scatter(d["V"], d["norm_mat"], color=COLOR_MAT, alpha=0.7)
    axes[0].set_title(LABEL_MAT)
    axes[1].scatter(d["V"], d["norm_adj"], color=COLOR_ADJ, alpha=0.7)
    axes[1].set_title(LABEL_ADJ)
    for ax in axes:
        ax.set_xlabel("|V|")
        ax.set_ylabel("Normalized runtime")
        ax.grid(alpha=0.3)
        ax.set_ylim(bottom=0)
    fig.suptitle("Empirical runtime ÷ theoretical bound")
    save(fig, out, "3_normalized", fmt)


def plot_loglog(df, out, fmt):
    """Graph 4: log-log plots with fitted slopes."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    pairs = [
        (axes[0], df["V"], df["runtime_mat"], COLOR_MAT, LABEL_MAT, "|V|", "expect ≈ 2"),
        (axes[1], df["V"] + df["E"], df["runtime_adj"], COLOR_ADJ, LABEL_ADJ, "|V| + |E|",
         "expect ≈ 1 (+ log factor)"),
    ]
    for ax, x, y, color, label, xlabel, note in pairs:
        mask = (x > 0) & (y > 0)
        x, y = x[mask], y[mask]
        ax.scatter(x, y, color=color, alpha=0.7)
        if len(x) >= 2:
            slope, intercept = np.polyfit(np.log10(x), np.log10(y), 1)
            xs = np.linspace(np.log10(x.min()), np.log10(x.max()), 50)
            ax.plot(10 ** xs, 10 ** (slope * xs + intercept), "--", color="black")
            ax.text(0.04, 0.92, f"slope = {slope:.2f}  ({note})",
                    transform=ax.transAxes, fontsize=9)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Runtime (s)")
        ax.set_title(label)
        ax.grid(alpha=0.3, which="both")
    fig.suptitle("Log-log runtime: slope ≈ growth exponent")
    save(fig, out, "4_loglog", fmt)


def plot_winner_map(df, out, fmt):
    """Graph 5: which implementation wins, by V and density."""
    d = df.copy()
    d["adj_wins"] = d["runtime_adj"] < d["runtime_mat"]
    fig, ax = plt.subplots(figsize=(7, 5))
    for wins, color, label, marker in [(True, COLOR_ADJ, f"{LABEL_ADJ} faster", "s"),
                                       (False, COLOR_MAT, f"{LABEL_MAT} faster", "o")]:
        s = d[d["adj_wins"] == wins]
        ax.scatter(s["V"], s["density"], color=color, label=label, marker=marker, alpha=0.8)
    vs = np.linspace(max(d["V"].min(), 4), d["V"].max(), 200)
    max_e = vs * (vs - 1) / (1 if DIRECTED else 2)
    boundary = np.clip(vs ** 2 / np.log2(vs) / max_e, 0, 1)
    ax.plot(vs, boundary, "k--", label="theory: |E| ≈ |V|² / log|V|")
    ax.set_xlabel("|V|")
    ax.set_ylabel("Density  |E| / max edges")
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
    ax.set_title("Faster implementation by size and density")
    save(fig, out, "5_winner_map", fmt)

 
def main():
    out = Path(OUT_DIR)
    out.mkdir(parents=True, exist_ok=True)
    df = load(CSV_PATH)
    print(f"Loaded {len(df)} (V, E) configurations "
          f"(V {df['V'].min()}–{df['V'].max()}, density {df['density'].min():.3f}–{df['density'].max():.3f})")
 
    for fn in (plot_time_vs_V, plot_time_vs_E, plot_normalized, plot_loglog, plot_winner_map):
        try:
            fn(df, out, "png")
        except Exception as e:  # one bad plot shouldn't stop the rest
            print(f"  {fn.__name__} failed: {e}")
 
    wins = (df["runtime_adj"] < df["runtime_mat"]).mean()
    print(f"Heap version faster in {wins:.0%} of configurations.")


if __name__ == "__main__":
    main()
