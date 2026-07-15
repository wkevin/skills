---
name: wkevin-srt-translate
description: 将 SRT 字幕文件拆分为多个片段，生成并行翻译 subagents 进行翻译，最后拼接结果。在用户提供 SRT 文件进行翻译或要求翻译字幕时使用。
version: 1.0
---

# /srt-translate

使用并行 AI subagents 实现，无需 agent 间协调，翻译 SRT 字幕文件，然后将结果拼接成单个输出文件。

## 用法

```
/srt-translate <file.srt> [--workers <worker-number>] [--output <output_file>] [--max-entries <max-entries-number>]
```

## 参数

- `file.srt` — 源 SRT 文件路径（必填）
- `--workers <worker-number>` — 并行 worker 数（默认：3）
- `--output <file>` — 输出文件路径（默认：`original_CN.srt`）
- `--max-entries <max-entries-number>` — 拆分时每个部分最多的条目数量（默认 200）

## 工作流程

### 第 1 步 — 分析并拆分 Chunk

1. 读取 SRT 文件并统计总条目数。
2. 使用以下命令准确计数条目（每个条目编号独立一行，且后面紧跟时间轴行）：
   ```bash
   awk '/^[0-9]+$/ {count++} END{print count}' /path/to/file.srt
   ```
   **注意**：不要使用 `grep -c "^[0-9]*$"` 计数，因为时间轴行（如 `00:00:03,274 --> 00:00:05,294`）也包含数字，会导致错误计数。
3. 根据总条目数，拆分出若干部分（Chunk），每个 Chunk 满足以下 Rule：
   - 拆分时条目要完整切分，绝不在条目中间断开。
   - 每部分条目不要太少：建议 100 - `max-entries-number` 条之间。
   - 拆分时保证边界的条目中，其文本与前面条目中文本组成一个完整的句子，不要把一句话拆分到不同的部分中。
4. **验证**：
   - 检查每个 chunk 的： start_entry >= 1，end_entry <= 总条目数，确保范围合法。
   - 最高条目编号与总条目数是否一致。

### 第 2 步 — 并行启动翻译 agents

使用 `Agent` tool 启动 `worker-number` 个并行 subagent（`run_in_background: true`），形成循环使用的 subagent 资源池，依次把每个部分传递给 subagent ：

- 源文件路径
- 需要翻译的具体条目标号范围（如 `1-100``）
- 目标语言（默认中文）
- Rules:
  - 不允许修改条目编号和时间轴信息
  - 保留条目中3者（编号、时间轴信息、文本）在一起，不拆开
  - 完成前检查是否英文句子（单词、短语、个别短句不算）都被翻译成了中文，如果仍存在英文句子则不要结束，而要继续翻译。

```json
{
  "description": "翻译 SRT 片段 (1-100)",
  "prompt": "翻译 SRT 字幕文件 /path/to/file.srt 中的第 1-100 条目，目标语言为中文。翻译完成后将结果写入 /path/to/output_1_100.srt。",
  "run_in_background": true,
  "subagent_type": "general-purpose"
}
```

每个 subagent 完成后，继续把待翻译的部分传递给空闲的 subagent,直到所有部分翻译完成。

### 第 3 步 — 收集结果

等待所有 background agents 完成（通过任务通知或主动检查）。

### 第 4 步 — 拼接并验证

1. 按顺序拼接所有片段输出到最终文件
2. 重新编号条目（确保连续编号）
3. 验证条目数量与原始文件一致
4. 如有任何片段失败，手动翻译该片段并追加

### 第 5 步 — 清理

拼接完成后，所有 background agents 自动结束，无需手动清理。

如需强制终止未完成的 agent，使用 `TaskStop` tool。

## 输出格式

最终翻译的 SRT 文件保留：

- 原始时间轴信息（`HH:MM:SS,mmm --> HH:MM:SS,mmm`）
- 条目编号（连续）
- 条目之间的空行

## 错误处理

| 失败情况               | 处理方式                           |
| ---------------------- | ---------------------------------- |
| Subagent 启动失败      | 回退到手动翻译该片段               |
| Subagent 无响应        | 使用可用结果继续；手动翻译缺失片段 |
| 最终输出条目数量不匹配 | 识别缺失范围，手动翻译并追加到文件 |

## 示例

```
/srt-translate @/path/to/video.srt [--workers 4] [--output "/path/to/video_CN.srt"]
```

这会将 `video.srt` 启动 4 个并行 translator agents，根据条目数量自行决定每部分拆分条目数量（100-`max-entries-number`之间），等待所有翻译完成，拼接为 `video_CN.srt`，最后验证条目完整性。
