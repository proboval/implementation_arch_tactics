import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix

INPUT_CSV = "arch_detection_metrics/architecture_detection_results_qwen.csv"
OUTPUT_DIR = "arch_detection_metrics/confusion_matrices"

GROUND_TRUTH_COL = "architecture_label"
PREDICTION_COLS = [
    "p1_architecture_label",
    "p2_architecture_label",
    "p3_architecture_label",
    "p4_architecture_label",
]

LABEL_ORDER = [
    "script_based",
    "layered",
    "modular_monolith",
    "monolith",
]


def normalize_label(x):
    if pd.isna(x):
        return ""
    return str(x).strip().lower()


def build_confusion_for_column(df, y_true_col, pred_col, labels):
    temp = df[[y_true_col, pred_col]].copy()
    temp[y_true_col] = temp[y_true_col].apply(normalize_label)
    temp[pred_col] = temp[pred_col].apply(normalize_label)

    temp = temp[
        (temp[y_true_col] != "") &
        (temp[pred_col] != "")
    ].copy()

    y_true = temp[y_true_col].tolist()
    y_pred = temp[pred_col].tolist()

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)

    return cm_df, len(temp)


def save_confusion_csv(cm_df, output_path):
    cm_df.to_csv(output_path, encoding="utf-8-sig")


def save_confusion_heatmap(cm_df, title, output_path):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title(title)
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_CSV)

    if GROUND_TRUTH_COL not in df.columns:
        raise ValueError(f"В CSV нет колонки ground truth: {GROUND_TRUTH_COL}")

    missing_pred_cols = [c for c in PREDICTION_COLS if c not in df.columns]
    if missing_pred_cols:
        raise ValueError(f"В CSV отсутствуют prediction columns: {missing_pred_cols}")

    for pred_col in PREDICTION_COLS:
        cm_df, n_samples = build_confusion_for_column(
            df=df,
            y_true_col=GROUND_TRUTH_COL,
            pred_col=pred_col,
            labels=LABEL_ORDER,
        )

        print("=" * 80)
        print(f"Confusion matrix for: {pred_col}")
        print(f"N samples: {n_samples}")
        print(cm_df)
        print()

        csv_path = os.path.join(OUTPUT_DIR, f"{pred_col}_confusion_matrix.csv")
        png_path = os.path.join(OUTPUT_DIR, f"{pred_col}_confusion_matrix.png")

        save_confusion_csv(cm_df, csv_path)
        save_confusion_heatmap(
            cm_df,
            title=f"Confusion Matrix: {pred_col}",
            output_path=png_path,
        )

        print(f"Saved CSV: {csv_path}")
        print(f"Saved PNG: {png_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
