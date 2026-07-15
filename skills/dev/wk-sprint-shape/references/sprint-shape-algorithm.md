# sprint-shape 算法细节

本文是 [SKILL.md](../SKILL.md) 的算法附录,详细描述 Step 4-6 的内部实现。

## §1 依赖图构建

### 1.1 数据源

**显式依赖**(优先):

`tasks.md §1.1/§1.2` 实现细节中如有"依赖:"字段,直接采用:

```markdown
- **UC-04-05** [P1] 用户密码强度校验
  - **实现细节**:
    - 依赖: UC-04-01(用户认证核心)
    - 路径: src/auth/validator.ts
```

**推断依赖**(次优):

扫描实现细节里的 UC/IF 编号交叉引用:

```markdown
- **UC-05-02** [P3] 批量导入 UI
  - **实现细节**:
    - 复用 IF-03-02 的解析逻辑
    - 调用 IF-05-01 的批处理接口
```

提取:
- 引用 IF-03-02 → UC-05-02 依赖 IF-03-02(推断)
- 调用 IF-05-01 → UC-05-02 依赖 IF-05-01(推断)

### 1.2 图结构

```python
# 伪代码
graph = {
  "UC-04-05": ["UC-04-01"],         # 前驱
  "UC-05-02": ["IF-03-02", "IF-05-01"],
  "IF-05-01": ["UC-05-01"],          # 同主题配对
  ...
}
```

### 1.3 拓扑排序(Kahn's algorithm)

```python
def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for dep in graph[node]:
            in_degree[node] += 1
    
    queue = [n for n in graph if in_degree[n] == 0]
    result = []
    while queue:
        n = queue.pop(0)
        result.append(n)
        for m in graph:
            if n in graph[m]:
                in_degree[m] -= 1
                if in_degree[m] == 0:
                    queue.append(m)
    return result
```

### 1.4 Scaffold 完整性检查

对新 Sprint 内所有 task,检查其前驱:

| 前驱状态 | 处理 |
| --- | --- |
| 在新 Sprint 内 | ✓ 同一 Sprint 内处理 |
| 历史 Sprint 已 [x] | ✓ 已完成 |
| 在 §2 Backlog(P0/P1) | ⚠ 警告,建议纳入同 Sprint |
| 在 §2 Backlog(P2/P3) | ✓ 可接受,记录为技术债 |
| 不在 tasks.md 定义 | ✗ 错误,提示用户修正 |

## §2 主题聚类

### 2.1 中文分词

简化版:用 jieba 或简单正则切词;提取名词短语。

### 2.2 关键词提取

每个 UC/IF 取:
- **标题**分词结果(权重 ×2)
- **agile 三段式**(作为/我希望/以便)分词(权重 ×1)
- **实现细节**前 3 个 bullet(权重 ×0.5)

### 2.3 聚类(K-means 简化版)

```python
from collections import Counter

def cluster(tasks):
    keywords = Counter()
    for t in tasks:
        for kw in t.keywords:
            keywords[kw] += t.weight
    return keywords.most_common(5)  # top 5 主题
```

主导主题 = 频次最高的关键词。

### 2.4 代号生成(Ubuntu 风格)

基于主导主题 + 同义词替换:

| 主题关键词 | 代号候选 |
| --- | --- |
| 批量导入 | bulk-onboard |
| 用户认证 | auth-fortify |
| 性能优化 | perf-tune |

**生成规则**:
1. 取主导主题 → 英文翻译(查表 or 简单翻译)
2. 副词修饰(可选):"fortify" / "boost" / "streamline"
3. 全小写 + 短横线连接

**用户可覆盖**:skill 提议代号,用户在 Step 2 澄清时替换。

## §3 Sprint 挑选启发式

### 3.1 容量估算

默认 2 周 = 10 工作日 = 80 小时。粗估每个 task:

| 复杂度 | 实现细节条数 | 预估工时 |
| --- | --- | --- |
| 简单 | ≤ 2 | 0.5 天 |
| 中等 | 3-5 | 1 天 |
| 复杂 | 6-10 | 2 天 |
| 架构级 | > 10 或涉及多模块 | 3 天 |

### 3.2 挑选算法

```python
def pick_sprint(sprint_pool, milestone_pool, production_pool, max_days=10):
    selected = []
    total_days = 0
    
    # 1. Sprint pool 必选
    for t in sprint_pool:
        if total_days + t.estimate <= max_days:
            selected.append(t)
            total_days += t.estimate
    
    # 2. Milestone pool 按 scaffold 顺序选
    for t in topological_sort(milestone_pool):
        if total_days + t.estimate <= max_days and 10 <= len(selected) + 1 <= 20:
            selected.append(t)
            total_days += t.estimate
    
    # 3. Production pool 按主题聚类补充
    for t in production_pool:
        if t.theme == dominant_theme(selected):
            if total_days + t.estimate <= max_days and len(selected) < 20:
                selected.append(t)
                total_days += t.estimate
    
    return selected
```

### 3.3 10-20 硬约束

- **下限 10**:低于 10 = sprint 不饱和,Scrum 浪费
- **上限 20**:超过 20 = sprint 失控,无法 retrospective
- 用户可显式覆盖(如"做 30 个"或"少做点 5 个就够")

## §4 三子节拆分算法

### 4.1 首次实现 vs 升级 vs fix

```python
def classify_subtask(task_id, git_log):
    if task_id not in git_log:
        return "首次实现"
    elif has_upgrade_keyword(task.description):  # "upgrade:" / "改进" / "优化"
        return "升级"
    elif has_fix_keyword(task.description):      # "fix:" / "bug" / "NPE" / "崩溃"
        return "bug fix"
    else:
        return "首次实现"  # 默认
```

### 4.2 升级条目格式

```markdown
- [ ] upgrade: {UC/IF ID} {增量改进点}
  - {原条目对比:之前做了什么,这次加什么}
```

### 4.3 bug fix 条目格式

```markdown
- [ ] fix: {UC/IF ID} {缺陷标题}
  - **症状**: {issue 描述}
  - **复现**: {步骤}
  - **修复方向**: {思路}
```

## §5 状态机

```
🟡 Planning → 🔵 Active → 🟢 Done
                          ↓
                       ⚫ Cancelled
```

| 转换 | 触发 | 谁负责 |
| --- | --- | --- |
| 🟡 → 🔵 | 用户说"激活 Sprint N"或显式手动改 | 用户 |
| 🔵 → 🟢 | Sprint 内所有 [ ] 变 [x] | task-dev + 用户确认 |
| 任意 → ⚫ | 用户取消 | 用户 |

**本 skill 不擅自状态推进**:从 🟡 Planning 到 🔵 Active 是业务承诺(开始冲刺),需用户显式确认。

## §6 Version 推断

若用户未指定 Version,skill 按以下规则建议:

1. 读现有 Sprint 段,提取最大 Version
2. 若现有最大 Version 是 `vX.Y`,建议 `vX.(Y+1)`(PATCH 递增)
3. 若 Sprint 涉及架构级改动(架构 IF),建议 `v(X+1).0`(MINOR 递增)
4. 若 Sprint 涉及不兼容变更,建议 `v(X+1).0-rc`(MINOR + rc)

用户可在 Step 2 覆盖。

## §7 与 doc-align 的契约

本 skill 输出必须 pass `wk-doc-align` 的 evaluate 模式,关键检查项:

| doc-align 检查 | 本 skill 输出 |
| --- | --- |
| §1.1.1 Sprint 编号递增 | Step 7 编号冲突检测 |
| §1.1.2 Sprint 代号 | Step 6 主题聚类生成 |
| §1.1.3 起止日期 | Step 2 澄清 |
| §1.1.4 Goal | Step 6 主题聚类生成 |
| §1.1.5 Version 归属 | Step 2 澄清 + §6 推断 |
| §1.1.6 状态 | 默认 🟡 Planning |
| §1.2.1 拆三子节 | Step 6 算法 |
| §1.2.4 引用编号格式 | Step 7 联动校验 |
| §1.4.1 Active ≤ 1 | Step 8 校验 |
| §2.5 Backlog 不与历史重复 | Step 7 §2 清理 |
| §4 跨文件 UC/IF 定义一致 | Step 8 联动校验 |

---

**加载指引**:本文件仅在 sprint-shape 执行 Step 4-6 时按需读取。若用户问"如何规划 sprint" / 直接调用 skill —— 读 [SKILL.md](../SKILL.md)。