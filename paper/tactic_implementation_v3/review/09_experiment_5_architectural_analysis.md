# Анализ архитектурных изменений в Experiment 5

## Обзор данных

- **Репозиториев в dataset.csv**: 57 (все Python-бэкенды)
- **Стартовало**: 56 репозиториев (3 архитектурных типа: script_based, layered, modular_monolith)
- **Успешно выполнились** (before + after static analysis): 42 репозитория
- **Показали ΔMI > 0**: 18 репозиториев
- **Улучшили avg_fan_out**: 15 репозиториев

---

## 1. Какие архитектурные метрики доступны

В артефактах static_analysis собираются три уровня метрик:

### 1.1 Code-level (MI)
- **radon_mi.json** — per-file MI score (Raw)
- **code_maintainability.json** — mi_avg, mi_min, files_analyzed

### 1.2 Architecture proxies
- **architecture_proxies.json**:
  - `python_files` — количество .py файлов
  - `packages` — количество директорий с `__init__.py`
  - `max_directory_depth` — максимальная глубина вложенности
  - `avg_files_per_package`
  - `imports_graph` — граф импортов (кто кого импортит)
  - Из imports_graph можно вычислить: пакетный tangle, циклические зависимости, coupling intensity

### 1.3 Architecture maintainability
- **architecture_maintainability.json**:
  - `packages` — количество пакетов
  - `avg_fan_out` — среднее количество внешних импортов на файл
  - `max_directory_depth` — глубина иерархии
  - `factors` — качественные метки проблем: C1 (concentration), C2 (lack of modularity), A3 (low architectural clarity), T4 (testability), A1 (analyzability)

### 1.4 Documentation
- **documentation_maintainability.json** — покрытие docstring'ами

---

## 2. Фактические архитектурные изменения

### 2.1 Изменение avg_fan_out

| Тип | Δ avg_fan_out | Что произошло |
|-----|--------------|---------------|
| **Paper2Rebuttal** | **12.6 → 10.5 (-2.1)** | 3 новых файла (pdf_converter.py, arxiv_client.py, llm_orchestrator.py), изоляция cross-cutting concerns |
| **webapp-color** | **5.0 → 3.33 (-1.67)** | 2 новых файла (color.py, config.py), разделение одного монолитного app.py |
| **spam-api-free-fire** | **5.0 → 3.6 (-1.4)** | 1 новый файл (crypto.py), выделение crypto-логики |
| **fastapi-whisper-ollama** | **2.0 → 1.56 (-0.44)** | Файл strategies.py, extract strategy pattern |
| Остальные 11 repos | −0.44 до −0.01 | Минорные улучшения coupling |

**Ключевой вывод**: fan-out улучшается ТОЛЬКО когда создаются новые файлы и импорты перераспределяются. Для layered и modular_monolith с уже сложившейся структурой fan-out практически не меняется.

### 2.2 Изменение файловой структуры

| Δ files | Репозиториев | Характер изменений |
|---------|-------------|-------------------|
| +7 | 1 (whoogle-search) | Экстракция search_strategies — проблема: код сгенерирован, но MI не изменился |
| +3 | 1 (Paper2Rebuttal) | Экстракция pdf_converter, arxiv_client, llm_orchestrator — реальная декомпозиция |
| +2 | 7 repos | Типичное разбиение одного файла на 2-3 |
| +1 | 18 repos | Минимальное изменение |
| 0 | 15 repos | Код не сгенерирован (ошибки API, invalid step, превышение контекста) |

**Файлы добавляются, но глубина директорий (max_directory_depth) изменилась только в 2 из 42 случаев** (HerokuFreeProxy: 2→3, autoforge: 3→4). Пакеты (`packages`) не изменились нигде.

### 2.3 Изменение Maintainability Index по архитектурным типам

| Архитектура | n | Средний ΔMI | Улучшилось | Худшее |
|------------|---|------------|-----------|--------|
| **script_based** | 8 | **+4.91** | 4/8 | разбиение монолита даёт большой прирост |
| **modular_monolith** | 34 | +0.58 | 9/34 | основной массив, слабый эффект |
| **layered** | 13 | +0.25 | 6/13 | минимальный эффект |
| **monolith** | 1 | 0.0 | 0/1 | не зашёл |

**script_based** доминирует по ΔMI, потому что у них низкая база (1 файл, mi=0-69). Улучшение — арифметический артефакт: при разбиении Halstead Volume уменьшается, и MI растёт механически (подтверждает критику DA C2).

### 2.4 Что произошло с индексами MI — анализ по тактикам

| Тактика | n | Средний ΔMI | Комментарий |
|---------|---|------------|------------|
| **Decomposability** | 24 | **+1.75** | Самый сильный эффект за счёт script_based |
| **Localized Modification** | 18 | +1.16 | В основном modular_monolith |
| **Reduced Coupling** | 6 | −0.08 | Ни одного успешного улучшения |

**Decomposability** даёт ΔMI = 1.75 в среднем, но эффект двойной: настоящая декомпозиция (Paper2Rebuttal, ΔMI=18.1) + механическое разбиение (webapp-color, ΔMI=21.9).

**Localized Modification** показывает результаты на modular_monolith (5/11 improved), но ΔMI редко превышает 1.0.

**Reduced Coupling** полностью провалился — ни одного репозитория с положительным ΔMI > 0.1.

---

## 3. Детальный разбор архитектурных находок

### 3.1 Paper2Rebuttal — единственный случай реального архитектурного рефакторинга

| Метрика | Before | After | Δ |
|---------|--------|-------|---|
| python_files | 5 | 8 | +3 |
| avg_fan_out | 12.6 | 10.5 | −2.1 |
| mi_avg | 19.4 | 37.5 | +18.1 |
| mi_min | 0.0 | 0.0 | 0 |
| max_directory_depth | 1 | 1 | 0 |

Что произошло:
- **tools.py** (500+ строк, PDF + arXiv + utils) → `pdf_converter.py` выделен, `tools.py` импортирует его
- **arxiv.py** (300+ строк) → `arxiv_client.py` выделен, ответственность сужена
- **rebuttal_service.py** (500+ строк) → `llm_orchestrator.py` выделен

**Это настоящее архитектурное улучшение**: разделение ответственности, уменьшение связанности, изоляция cross-cutting concerns. Факторы C1 и C2 остались, но A3 мог бы быть снят при более детальном анализе.

### 3.2 webapp-color — механическое разбиение (подтверждение DA C2)

| Метрика | Before | After | Δ |
|---------|--------|-------|---|
| python_files | 1 | 3 | +2 |
| avg_fan_out | 5.0 | 3.33 | −1.67 |
| mi_avg | 69.3 | 91.2 | +21.9 |
| mi_min | 69.3 | 73.7 | +4.4 |

Что произошло:
- `app.py` (2259 байт, 1 файл) → `app.py` + `color.py` + `config.py`
- Halstead Volume уменьшился за счёт того, что код размазан по 3 файлам
- MI нового `color.py` = 100.0, `config.py` = 100.0 (тривиальные файлы)
- **Архитектурной ценности нет**: пакетов 0, глубина 1, структура плоская

Это именно то, на что указывает DA C2: MI растёт арифметически от разбиения, а не от архитектурного улучшения.

### 3.3 spam-api-free-fire — аналогично webapp-color

| Метрика | Before | After | Δ |
|---------|--------|-------|---|
| python_files | 4 | 5 | +1 |
| avg_fan_out | 5.0 | 3.6 | −1.4 |
| mi_avg | 67.2 | 76.6 | +9.4 |

Выделен `crypto.py` — полезно, но это code-level изменение.

### 3.4 fastapi-whisper-ollama — интересный случай

| Метрика | Before | After | Δ |
|---------|--------|-------|---|
| avg_fan_out | 2.0 | 1.56 | −0.44 |
| mi_avg | 87.6 | 88.95 | +1.36 |

Создан `strategies.py` — паттерн Strategy. Это реальный рефакторинг, но на маленьком coupling эффект малозаметен.

### 3.5 whoogle-search — ложная декомпозиция

| Метрика | Before | After | Δ |
|---------|--------|-------|---|
| python_files | 39 | 46 | +7 |
| avg_fan_out | 4.46 | 4.30 | −0.15 |
| mi_avg | 66.77 | 67.17 | +0.40 |

Добавлено 7 файлов, но MI почти не изменился. Файлы `search_strategies.py` генерировались многократно (step_0..step_8 в логах), но pipeline не справился с интеграцией. Импорт `self` появился (см. subgen → subgen в imports_graph after), что указывает на циклический импорт, созданный LLM.

---

## 4. Доказательства для review

### 4.1 DA C1: MI не измеряет архитектуру

**Подтверждается данными**. Сравним repos с одинаковым ΔMI:

| Репозиторий | ΔMI | Δ fan_out | Δ файлов | Архитектурная ценность |
|------------|-----|-----------|---------|----------------------|
| webapp-color | +21.9 | −1.67 | +2 | Низкая (механическое разбиение) |
| Paper2Rebuttal | +18.1 | −2.10 | +3 | Высокая (настоящая декомпозиция) |

MI не различает эти случаи. Оба показывают "improved", хотя природа изменений разная.

Более того:
- **whale**: whoogle-search добавил 7 файлов, ΔMI = +0.40 (фактически ноль)
- **minnow**: subgen добавил 1 файл, ΔMI = +7.93

Изменение MI определяется не архитектурной ценностью, а *базовым размером файлов* до разбиения.

### 4.2 DA C2: File splitting trivially improves MI

**Подтверждается**. Корреляция ΔMI с Δ файлов:

| Δ файлов | Repos | Средний ΔMI |
|----------|-------|------------|
| +2 или больше | 9 | +4.51 |
| +1 | 18 | +0.72 |
| 0 | 15 | +0.0 |

**Разница в файлах — единственный сильный предиктор ΔMI**.

Для script_based: correlation ≈ 0.95 (все улучшения — разбиение 1 файла).

### 4.3 Что на самом деле изменилось архитектурно (вопреки MI)

Если смотреть на **avg_fan_out** как прокси архитектурного улучшения:

- **Значимые изменения** (Δ fan_out < −0.5): 4 repos — Paper2Rebuttal, webapp-color, spam-api-free-fire, fastapi-whisper-ollama
- **Из них с реальной архитектурной ценностью**: 1 (Paper2Rebuttal)
- **packages не изменились нигде**
- **max_directory_depth изменился в 2/42**

Вывод: pipeline **не меняет архитектуру** в терминах пакетной структуры, иерархии или модульности. Все изменения — code-level.

### 4.4 Reduced Coupling — полностью провальная тактика

| Репозиторий | ΔMI | Результат |
|------------|-----|-----------|
| drf_admin | −0.091 | worsened |
| gemini-superpowers | −1.038 | worsened |
| bilibili-rag | +0.660 | improved (но fan_out −0.08, минимально) |
| crypto-price_service | failed | — |
| sars-fastapi | failed | — |
| easytrader | failed | — |

Reduced Coupling — единственная тактика с отрицательным средним эффектом. LLM не справляется с уменьшением связанности между модулями, вероятно, потому что это требует глобального понимания архитектуры, которого у LLM нет.

---

## 5. Что можно извлечь из данных без новых экспериментов

### 5.1 95% доверительные интервалы для ΔMI
Сырые данные по ΔMI для каждого репозитория есть в improvement_maintainability_dataset.csv. Можно вычислить CI для каждой архитектурной группы и тактики.

### 5.2 Sensitivity analysis (исключение выбросов)
Можно пересчитать Wilcoxon test без webapp-color (+21.98) и Paper2Rebuttal (+18.14). Если значимость пропадёт — результат неустойчив.

### 5.3 Architecture-level метрики из существующих данных
- architecture_proxies.json даёт imports_graph → можно вычислить:
  - **Cyclic Dependency Ratio** (сколько файлов в циклах / всего файлов)
  - **Inter-module Coupling Intensity** (среднее количество внешних импортов на модуль)
  - **Package Tangle Percentage**
  - **Module Cohesion** (косвенно, через ratio imports/exports)
- Данные доступны для 42 repos с before/after

### 5.4 Cost-benefit из логов
- tactic_implementation.log содержит тайминги для каждого шага
- Можно оценить: среднее время на репозиторий, количество LLM вызовов
- architecture_tactic_selection.log содержит timing каждого LLM вызова

---

## 6. Итоговая таблица: архитектурные изменения по репозиториям

| Репозиторий | Архитектура | Тактика | ΔMI | Δ fan_out | Δ files | Архитектурное изменение |
|------------|------------|---------|-----|-----------|---------|----------------------|
| Paper2Rebuttal | modular_monolith | Localized Modification | +18.14 | **−2.10** | +3 | **Да: выделение pdf_converter, arxiv_client, llm_orchestrator** |
| webapp-color | script_based | Decomposability | +21.98 | −1.67 | +2 | Разбиение файла, без архитектурной ценности |
| spam-api-free-fire | script_based | Decomposability | +9.40 | −1.40 | +1 | Разбиение файла |
| fastapi-whisper-ollama | modular_monolith | Decomposability | +1.36 | −0.44 | +1 | Strategy pattern |
| bilibili-rag | layered | Reduced Coupling | +0.66 | −0.08 | +1 | Минимальный эффект |
| claude-engineer | modular_monolith | Localized Modification | +1.30 | −0.06 | +2 | Modifications без архитектурной ценности |
| whoogle-search | modular_monolith | Decomposability | +0.40 | −0.16 | +7 | Добавлены файлы, MI не изменился |
| Остальные 34 | — | — | ~0 | ~0 | 0-2 | **Архитектурно ничего не изменилось** |

---

## 7. Выводы

1. **Единственный случай реального архитектурного улучшения**: Paper2Rebuttal. Δ fan_out = −2.1, +3 файла с чётким разделением ответственности.
2. **MI не различает архитектурные и не-архитектурные изменения** — что подтверждает критику DA C1.
3. **Основной источник ΔMI — механическое разбиение файлов** — подтверждает DA C2.
4. **Packages и max_directory_depth практически не меняются** — pipeline работает на code-level, не architecture-level.
5. **Reduced Coupling не работает** — ни одного значимого улучшения из 6 попыток.
6. **Для layered архитектур pipeline практически бесполезен** — ΔMI средний = +0.25, Δ fan_out ≈ 0.
7. **Из существующих данных можно вычислить architecture-level метрики** (cyclic dependency ratio, coupling intensity, tangle %) через imports_graph.
