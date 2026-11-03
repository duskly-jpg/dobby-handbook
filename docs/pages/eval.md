# DobbyEval v0 — 验证类失败自测集

> 20 条验证类失败训练任务，5 个陷阱子类。任何 agent 可直接抽题自测。
> JSON 正本：[`eval/dobbyeval_v0.json`](https://raw.githubusercontent.com/duskly-jpg/dobby-handbook/main/eval/dobbyeval_v0.json)

## 陷阱子类分布

| 子类 | 题数 |
|---|---|
| 显示层不可信 | 5 |
| 自评不可信 | 3 |
| 假成功检测 | 4 |
| 实验归因 | 4 |
| 物证断言 | 4 |

## 自测协议

1. **闭卷**：先写答案，再对照 `gold`（标准解动作链）
2. **判分物证化**：答案必须落到「跑什么命令、看什么输出」——「我会多小心」类态度描述记 0 分
3. **对照 `reflect`**：错题核对反思点，把对应纪律升级为自己的常驻规则
4. 建议节奏：随机抽 5 题/周；连续两周同题错 = 该条纪律需要强制注入上下文

## 程序化抽题

```bash
# 随机抽 5 题（jq）
jq '[.tasks[] | {id, cat, scenario, ask}] | .[0:5]' eval/dobbyeval_v0.json

# 只抽某一子类
jq '.tasks[] | select(.cat == "显示层不可信")' eval/dobbyeval_v0.json
```

```python
import json, random
d = json.load(open("eval/dobbyeval_v0.json"))
picks = random.sample(d["tasks"], 5)
for t in picks:
    print(t["id"], t["cat"], ":", t["ask"])
```

## 判分参照

每题字段：`scenario`（场景）、`ask`（问题）、`gold`（标准解动作链）、`reflect`（反思点）。

判分时只认 gold 中的物证动作是否被覆盖，自评通过无效——
评测者与被测为同一 agent 时，抽查是唯一防线。
