import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os


# --- Настройки для LaTeX (PGF) ---
def setup_pgf():
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "lualatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })


# --- Загрузка и подготовка данных ---
df = pd.read_csv('improvement_maintainability_experiment_3.csv')
df['mi_before'] = pd.to_numeric(df['mi_before'], errors='coerce')
df['mi_after'] = pd.to_numeric(df['mi_after'], errors='coerce')

# Расчет изменений (NaN в mi_after трактуем как критическое ухудшение)
df['mi_change'] = df['mi_after'] - df['mi_before']


def classify_status(row):
    if pd.isna(row['mi_after']): return 'Regression (Null)'
    if row['mi_change'] > 0: return 'Improved'
    if row['mi_change'] < 0: return 'Degraded'
    return 'Stable'


df['status'] = df.apply(classify_status, axis=1)

output_dir = 'latex_plots'
if not os.path.exists(output_dir): os.makedirs(output_dir)


# --- Функции отрисовки ---

def plot_all():
    # 1. Distribution of MI (Before vs After)
    plt.figure(figsize=(7, 5))
    plt.hist(df['mi_before'].dropna(), bins=15, alpha=0.5, label='Baseline (Before)', color='blue', edgecolor='black')
    plt.hist(df['mi_after'].dropna(), bins=15, alpha=0.5, label='Post-Intervention (After)', color='green',
             edgecolor='black')
    plt.title('Distribution of Maintainability Index')
    plt.xlabel('MI Score')
    plt.ylabel('Frequency')
    plt.legend()
    yield 'mi_distribution'

    # 2. Architecture Distribution
    plt.figure(figsize=(7, 5))
    arch_counts = df['architecture_summary'].value_counts()
    arch_counts.plot(kind='bar', color='gray', edgecolor='black')
    plt.title('Distribution of Repository Architectures')
    plt.xlabel('Architecture Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    yield 'arch_distribution'

    # 3. Top 10 Improvements/Degradations with Tactics
    plt.figure(figsize=(10, 6))
    valid_changes = df.dropna(subset=['mi_change']).sort_values('mi_change')
    top_bottom = pd.concat([valid_changes.head(5), valid_changes.tail(5)])

    # Формируем метку: Имя репозитория + Тактика
    labels = [f"{row['full_name'].split('/')[-1]} ({row['chosen_tactic']})" for _, row in top_bottom.iterrows()]
    colors = ['red' if x < 0 else 'green' for x in top_bottom['mi_change']]

    plt.barh(labels, top_bottom['mi_change'], color=colors, edgecolor='black', alpha=0.8)
    plt.title('Top 10 Maintainability Shifts by Tactic')
    plt.xlabel(r'$\Delta$ MI')
    yield 'top10_shifts'

    # 4. Pie Chart (Improvement Status)
    plt.figure(figsize=(6, 6))
    status_counts = df['status'].value_counts()
    colors_pie = ['#d3d3d3', '#90ee90', '#ffcccb', '#ff0000']  # Stable, Improved, Degraded, Null
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=colors_pie,
            wedgeprops={'edgecolor': 'black'})
    plt.title('Intervention Impact Summary')
    yield 'impact_pie'


# --- Процесс сохранения ---

# 1. Сохраняем PNG (через стандартный Agg)
matplotlib.use('Agg')
for name in plot_all():
    plt.savefig(os.path.join(output_dir, f"{name}.png"), dpi=300, bbox_inches='tight')
    plt.close()

# 2. Сохраняем PGF для LaTeX (если установлен LaTeX)
try:
    setup_pgf()
    for name in plot_all():
        plt.savefig(os.path.join(output_dir, f"{name}.pgf"), bbox_inches='tight')
        plt.close()
    print(f"Success! PNG and PGF files saved to {output_dir}")
except Exception as e:
    print(f"PGF generation failed (likely no LaTeX found), but PNGs are saved. Error: {e}")