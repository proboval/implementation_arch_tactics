import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# Создаем папку для сохранения графиков
output_dir = 'maintainability_plots_jpeg'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Настройка стиля графиков
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# --- 1. Загрузка данных ---
print("Загрузка данных...")
df_exp = pd.read_csv('improvement_maintainability_experiment_3.csv')
df_meta = pd.read_csv('maintainability_dataset.csv')

# --- 2. Объединение данных по full_name ---
print("Объединение данных с мета-информацией...")
df = pd.merge(df_exp, df_meta[['full_name', 'stars', 'files_analyzed']], on='full_name', how='left')

# --- 3. Подготовка и очистка данных ---
print("Подготовка данных...")

df['mi_before'] = pd.to_numeric(df['mi_before'], errors='coerce')
df['mi_after'] = pd.to_numeric(df['mi_after'], errors='coerce')

df['mi_change'] = np.where(
    df['mi_after'].isna(),
    -999,
    df['mi_after'] - df['mi_before']
)

def get_improvement_status(row):
    if pd.isna(row['mi_after']):
        return 'Ухудшился (null после)'
    elif row['mi_change'] > 0:
        return 'Улучшился'
    elif row['mi_change'] < 0:
        return 'Ухудшился'
    else:
        return 'Без изменений'

df['improvement_status'] = df.apply(get_improvement_status, axis=1)

median_files = df['files_analyzed'].median()
df['files_analyzed'] = df['files_analyzed'].fillna(median_files)
df['size_category'] = pd.cut(df['files_analyzed'], bins=[0, 10, 50, float('inf')],
                              labels=['Маленький (<10 файлов)', 'Средний (10-50 файлов)', 'Большой (>50 файлов)'])

df['stars'] = df['stars'].fillna(df['stars'].median())

# Создаем фигуру с подграфиками
fig = plt.figure(figsize=(20, 16))

# 1. Распределение maintainability ДО эксперимента
ax1 = fig.add_subplot(3, 3, 1)
ax1.hist(df['mi_before'].dropna(), bins=20, edgecolor='black', color='skyblue', alpha=0.7)
ax1.set_xlabel('Maintainability Index (MI) Before')
ax1.set_ylabel('Repository Count')
ax1.set_title('Maintainability Distribution Before Experiment')
ax1.axvline(df['mi_before'].mean(), color='red', linestyle='dashed', linewidth=1,
            label=f'Среднее: {df["mi_before"].mean():.2f}')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Распределение архитектур
ax2 = fig.add_subplot(3, 3, 2)
arch_counts = df['architecture_summary'].value_counts()
bars = ax2.bar(arch_counts.index, arch_counts.values, color='lightcoral', alpha=0.8)
ax2.set_xlabel('Architecture Type')
ax2.set_ylabel('Count')
ax2.set_title('Architecture Distribution in Dataset')
ax2.tick_params(axis='x', rotation=45)
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom')

# 3. Распределение архитектурных тактик
ax3 = fig.add_subplot(3, 3, 3)
tactic_counts = df['chosen_tactic'].value_counts()
bars = ax3.bar(tactic_counts.index, tactic_counts.values, color='lightgreen', alpha=0.8)
ax3.set_xlabel('Architecture Tactic')
ax3.set_ylabel('Count')
ax3.set_title('Architecture Tactic')
ax3.tick_params(axis='x', rotation=45)
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom')

# 4. Изменение MI по репозиториям (топ изменений)
ax4 = fig.add_subplot(3, 3, 4)
df_plot = df[df['mi_change'] != -999].copy()
df_plot = df_plot[df_plot['mi_change'] != 0].sort_values('mi_change', ascending=True)

if not df_plot.empty:
    top_changes = pd.concat([df_plot.head(10), df_plot.tail(10)])
    short_names = [name[:30] + '...' if len(name) > 30 else name
                   for name in top_changes['full_name']]
    colors = ['red' if x < 0 else 'green' for x in top_changes['mi_change']]
    ax4.barh(short_names, top_changes['mi_change'], color=colors, alpha=0.7)
    ax4.set_xlabel('Diff MI (Δ)')
    ax4.set_title('Top 10 MI improvements and enhancements')
    ax4.axvline(0, color='black', linestyle='-', linewidth=0.5)
else:
    ax4.text(0.5, 0.5, 'No data on changes', ha='center', va='center')
    ax4.set_title('Changing MI by repository')

# 5. Среднее изменение MI по архитектурам
ax5 = fig.add_subplot(3, 3, 5)
arch_avg_change = df[df['mi_change'] != -999].groupby('architecture_summary')['mi_change'].mean().sort_values()
arch_avg_change.plot(kind='barh', ax=ax5, color='mediumpurple', alpha=0.8)
ax5.set_xlabel('Average change in MI')
ax5.set_title('Average Change in MI by Architecture Type')
ax5.axvline(0, color='black', linestyle='-', linewidth=0.5)

# 6. Изменение MI по размеру проекта
ax6 = fig.add_subplot(3, 3, 6)
size_avg_change = df[df['mi_change'] != -999].groupby('size_category')['mi_change'].mean()
size_avg_change.plot(kind='bar', ax=ax6, color=['gold', 'cyan', 'lightpink'], alpha=0.8)
ax6.set_ylabel('Average change in MI')
ax6.set_title('Average Change in MI by Project Size')
ax6.axhline(0, color='black', linestyle='-', linewidth=0.5)
ax6.tick_params(axis='x', rotation=15)

# 7. Изменение MI по количеству звезд (scatter plot)
ax7 = fig.add_subplot(3, 3, 7)
df_scatter = df[df['mi_change'] != -999]
scatter = ax7.scatter(df_scatter['stars'], df_scatter['mi_change'],
                      c=df_scatter['mi_before'], cmap='viridis',
                      alpha=0.6, edgecolors='black', linewidth=0.5, s=30)
ax7.set_xlabel('Количество Звезд')
ax7.set_ylabel('Changes MI (Δ)')
ax7.set_title('Dependence of MI change on the number of stars')
ax7.axhline(0, color='red', linestyle='--', linewidth=0.5, alpha=0.5)
ax7.set_xscale('log')
plt.colorbar(scatter, ax=ax7, label='MI До')

# 8. Доля улучшившихся/ухудшившихся (круговая диаграмма)
ax8 = fig.add_subplot(3, 3, 8)
status_counts = df['improvement_status'].value_counts()
colors_map = {
    'Улучшился': '#90EE90',
    'Ухудшился': '#FFA07A',
    'Без изменений': '#D3D3D3',
    'Ухудшился (null после)': '#FF6347'
}
colors = [colors_map.get(status, '#87CEEB') for status in status_counts.index]
wedges, texts, autotexts = ax8.pie(status_counts.values,
                                     labels=status_counts.index,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=colors)
for autotext in autotexts:
    autotext.set_color('white')
ax8.set_title('Статус улучшения Maintainability')

# 9. Репозитории с ухудшением (null после)
ax9 = fig.add_subplot(3, 3, 9)
df_null = df[df['mi_after'].isna()].head(15)
if not df_null.empty:
    short_names = [name[:35] + '...' if len(name) > 35 else name
                   for name in df_null['full_name']]
    y_pos = range(len(df_null))
    bars = ax9.barh(y_pos, [1] * len(df_null), color='darkred', alpha=0.7)
    ax9.set_yticks(y_pos)
    ax9.set_yticklabels(short_names, fontsize=8)
    ax9.set_title(f'Репозитории с ухудшением (null после): {len(df_null)}')
    ax9.set_xlabel('Факт ухудшения')
    ax9.set_xticks([])
else:
    ax9.text(0.5, 0.5, 'Нет репозиториев с null', ha='center', va='center')
    ax9.set_title('Репозитории с ухудшением (null после)')

plt.suptitle('Анализ эксперимента по улучшению Maintainability', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

# Сохраняем общий график
plt.savefig(f'{output_dir}/all_plots_combined.jpg', dpi=300, bbox_inches='tight')
print(f"Общий график сохранен в {output_dir}/all_plots_combined.jpg")

# Сохраняем отдельные графики
print("\nСохранение отдельных графиков...")

# График 1
plt.figure(figsize=(10, 6))
plt.hist(df['mi_before'].dropna(), bins=20, edgecolor='black', color='skyblue', alpha=0.7)
plt.xlabel('Индекс Поддерживаемости (MI) До')
plt.ylabel('Количество репозиториев')
plt.title('Распределение Maintainability До Эксперимента')
plt.axvline(df['mi_before'].mean(), color='red', linestyle='dashed', linewidth=1,
            label=f'Среднее: {df["mi_before"].mean():.2f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}/plot1_mi_distribution.jpg', dpi=300)
plt.close()

# График 2
plt.figure(figsize=(10, 6))
arch_counts = df['architecture_summary'].value_counts()
bars = plt.bar(arch_counts.index, arch_counts.values, color='lightcoral', alpha=0.8)
plt.xlabel('Тип Архитектуры')
plt.ylabel('Количество')
plt.title('Распределение Архитектур в Датacете')
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig(f'{output_dir}/plot2_architecture_distribution.jpg', dpi=300)
plt.close()

# График 3
plt.figure(figsize=(12, 6))
tactic_counts = df['chosen_tactic'].value_counts()
bars = plt.bar(tactic_counts.index, tactic_counts.values, color='lightgreen', alpha=0.8)
plt.xlabel('Архитектурная Тактика')
plt.ylabel('Количество')
plt.title('Используемые Архитектурные Тактики')
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig(f'{output_dir}/plot3_tactics_distribution.jpg', dpi=300)
plt.close()

# График 4
plt.figure(figsize=(12, 8))
df_plot = df[df['mi_change'] != -999].copy()
df_plot = df_plot[df_plot['mi_change'] != 0].sort_values('mi_change', ascending=True)

if not df_plot.empty:
    top_changes = pd.concat([df_plot.head(10), df_plot.tail(10)])
    short_names = [name[:40] + '...' if len(name) > 40 else name
                   for name in top_changes['full_name']]
    colors = ['red' if x < 0 else 'green' for x in top_changes['mi_change']]
    plt.barh(short_names, top_changes['mi_change'], color=colors, alpha=0.7)
    plt.xlabel('Изменение MI (Δ)')
    plt.title('Топ-10 улучшений и ухудшений MI')
    plt.axvline(0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig(f'{output_dir}/plot4_top_changes.jpg', dpi=300)
plt.close()

# График 5
plt.figure(figsize=(10, 6))
arch_avg_change = df[df['mi_change'] != -999].groupby('architecture_summary')['mi_change'].mean().sort_values()
arch_avg_change.plot(kind='barh', color='mediumpurple', alpha=0.8)
plt.xlabel('Среднее изменение MI')
plt.title('Среднее изменение MI по Типу Архитектуры')
plt.axvline(0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig(f'{output_dir}/plot5_avg_change_by_architecture.jpg', dpi=300)
plt.close()

# График 6
plt.figure(figsize=(10, 6))
size_avg_change = df[df['mi_change'] != -999].groupby('size_category')['mi_change'].mean()
size_avg_change.plot(kind='bar', color=['gold', 'cyan', 'lightpink'], alpha=0.8)
plt.ylabel('Среднее изменение MI')
plt.title('Среднее изменение MI по Размеру Проекта')
plt.axhline(0, color='black', linestyle='-', linewidth=0.5)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(f'{output_dir}/plot6_avg_change_by_size.jpg', dpi=300)
plt.close()

# График 7
plt.figure(figsize=(10, 6))
df_scatter = df[df['mi_change'] != -999]
scatter = plt.scatter(df_scatter['stars'], df_scatter['mi_change'],
                      c=df_scatter['mi_before'], cmap='viridis',
                      alpha=0.6, edgecolors='black', linewidth=0.5, s=30)
plt.xlabel('Количество Звезд')
plt.ylabel('Изменение MI (Δ)')
plt.title('Зависимость изменения MI от количества звезд')
plt.axhline(0, color='red', linestyle='--', linewidth=0.5, alpha=0.5)
plt.xscale('log')
plt.colorbar(scatter, label='MI До')
plt.tight_layout()
plt.savefig(f'{output_dir}/plot7_change_vs_stars.jpg', dpi=300)
plt.close()

# График 8
plt.figure(figsize=(10, 8))
status_counts = df['improvement_status'].value_counts()
colors_map = {
    'Улучшился': '#90EE90',
    'Ухудшился': '#FFA07A',
    'Без изменений': '#D3D3D3',
    'Ухудшился (null после)': '#FF6347'
}
colors = [colors_map.get(status, '#87CEEB') for status in status_counts.index]
wedges, texts, autotexts = plt.pie(status_counts.values,
                                     labels=status_counts.index,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=colors)
for autotext in autotexts:
    autotext.set_color('white')
plt.title('Статус улучшения Maintainability')
plt.tight_layout()
plt.savefig(f'{output_dir}/plot8_improvement_status_pie.jpg', dpi=300)
plt.close()

# График 9
plt.figure(figsize=(12, 8))
df_null = df[df['mi_after'].isna()].head(15)
if not df_null.empty:
    short_names = [name[:45] + '...' if len(name) > 45 else name
                   for name in df_null['full_name']]
    y_pos = range(len(df_null))
    bars = plt.barh(y_pos, [1] * len(df_null), color='darkred', alpha=0.7)
    plt.yticks(y_pos, short_names)
    plt.title(f'Репозитории с ухудшением (null после): {len(df_null)}')
    plt.xlabel('Факт ухудшения')
    plt.xticks([])
    for i, (bar, name) in enumerate(zip(bars, df_null['full_name'])):
        plt.text(0.5, i, '✗', ha='center', va='center', color='white', fontsize=12)
else:
    plt.text(0.5, 0.5, 'Нет репозиториев с null', ha='center', va='center')
    plt.title('Репозитории с ухудшением (null после)')
plt.tight_layout()
plt.savefig(f'{output_dir}/plot9_null_after_repos.jpg', dpi=300)
plt.close()

# График 10
plt.figure(figsize=(10, 6))
df_delta = df[df['mi_change'] != -999]['mi_change']
plt.hist(df_delta, bins=20, edgecolor='black', color='teal', alpha=0.7)
plt.axvline(0, color='red', linestyle='--', label='Ноль', alpha=0.7)
plt.axvline(df_delta.mean(), color='blue', linestyle='-',
            label=f'Среднее Δ: {df_delta.mean():.2f}', alpha=0.7)
plt.xlabel('Изменение индекса поддерживаемости (ΔMI)')
plt.ylabel('Количество репозиториев')
plt.title('Распределение силы изменений Maintainability')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}/plot10_delta_distribution.jpg', dpi=300)
plt.close()

# График 11
plt.figure(figsize=(10, 6))
df_box = df[df['mi_after'].notna()].copy()
data_to_plot = [df_box['mi_before'], df_box['mi_after']]
bp = plt.boxplot(data_to_plot, labels=['До эксперимента', 'После эксперимента'],
                  patch_artist=True)
colors_box = ['lightblue', 'lightgreen']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
for whisker in bp['whiskers']:
    whisker.set_color('black')
for cap in bp['caps']:
    cap.set_color('black')
for median in bp['medians']:
    median.set_color('red')
plt.ylabel('Индекс поддерживаемости (MI)')
plt.title('Сравнение MI до и после эксперимента')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}/plot11_before_after_boxplot.jpg', dpi=300)
plt.close()

print(f"\nВсе графики сохранены в папку: {output_dir}/")
print("\n--- Статистика ---")
print(f"Всего проектов в эксперименте: {len(df)}")
print(f"Проектов, где mi_after отсутствует (ухудшение): {df['mi_after'].isna().sum()}")
print(f"Проектов, которые улучшились: {len(df[df['mi_change'] > 0])}")
print(f"Проектов, которые ухудшились: {len(df[df['mi_change'] < 0])}")
print(f"Проектов без изменений: {len(df[df['mi_change'] == 0])}")
print(f"Среднее изменение MI (без учета null): {df_delta.mean():.2f}")
print(f"Медианное изменение MI: {df_delta.median():.2f}")
print(f"Максимальное улучшение: {df_delta.max():.2f}")
print(f"Максимальное ухудшение: {df_delta.min():.2f}")

