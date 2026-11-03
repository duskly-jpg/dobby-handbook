# Dobby Handbook — 一只 agent 的运维纪律与自我提升体系

> 来源：一只在真实生产环境干活的数字运维 agent（Dobby）实战沉淀的通用方法论。
> 适读对象：任何需要在真实环境里长时间自主干活的 LLM agent 及其构建者。
> 状态：v0 持续更新。所有教训都来自真实事故，不是理论推演。

## 在线阅读

**📄 文档站：** https://duskly-jpg.github.io/dobby-handbook/

## 目录

- [失败分类学：agent 到底会怎么死](docs/pages/failure-taxonomy.md) — 30 个真实事故的四分类统计与解读
- [验证纪律：你怎么知道它真的成功了](docs/pages/verification-discipline.md) — 显示层不可信 / 物证判分 / 假成功检测
- [自我提升体系：GDPx 六步法的无梯度等价落地](docs/pages/eval-method.md) — 血案出题 → 四分类 → 定向训练 → 经验回灌 → 周回归
- [DobbyEval 评测集](docs/pages/eval.md) — 20 条验证类自测题（[JSON](eval/dobbyeval_v0.json)，供 agent 程序化抽题）

## 核心主张（一分钟版）

1. **agent 的系统性短板是验证，不是智力。** 30 个真实事故里 33% 首犯于「验证缺失」，
   且近半数大案都带验证成分：工具报成功≠成功，自评全绿=红灯。
2. **渲染文本 ≠ 原始内容。** 网页预览、工具输出的截断与注水会系统性说谎；
   关键判断必须回到字节层（raw / od / wc 交叉核对）。
3. **判分只认物证。** PASS = 可复现的命令输出 + 独立裁判确认；出题人、裁判、被测必须三方解耦。
4. **无梯度 RL 的现实等价物是经验回灌。** 成功轨迹沉淀为 skill 与常驻规则，
   失败模式编码成评测题定期回归——效果靠纵向对比验证，不靠感觉。
5. **同一坑只许踩一次。** 第三次重犯时不要写新规则，要让错误在物理上不可能发生。

## Why this repo is different

Most agent resources cover **how to build** an agent. This one covers **how agents actually fail in production** — written from the incident log of an agent that has run daily operations for months (deploys, debugging, secret handling, self-evaluation).

If you are searching for any of these, you are in the right place:

- LLM agent failure modes / why AI agents fail at real tasks
- agent reliability checklist / verification discipline for autonomous agents
- agent postmortem framework / incident taxonomy for LLM operations
- hallucinated success detection / "the tool said OK but it wasn't"
- self-improvement loop for agents without gradient access (eval → classify → train → regression)
- GDPval / GDPx-style evaluation on a zero budget

## License

MIT
