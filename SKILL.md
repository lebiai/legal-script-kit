---
name: skill-lawyer-case-to-script
description: 律师案例转口播文案。将判决书、案情材料转化为短视频口播文案，内置爆款钩子体系（8种钩子手法）、5种文案类型（分享/分析/吃瓜/观点/观点干货版）、3种人设风格
---

# 律师案例转口播文案

## Overview

将**原始案例材料**（案情描述、判决书摘要、代理过程回顾等）转化为律师面对镜头口播的文案。

**三条核心原则：**
1. **第一句必须是「你」** — 第一秒让观众知道这事跟他有关
2. **钩子只写一句，≤18字** — 2-3 秒落地，不铺场景
3. **法院结论说人话** — "没戏了"不是"法院不受理"

**与 skill-lawyer-case-video 的关系：**

| Skill | 输入 | 输出 |
|-------|------|------|
| **本skill** | 原始案例材料 | 口播文案 |
| lawyer-case-video | 口播文案 | Grok 视频提示词 |

## 撰写流程

1. **[案件识别与自动推荐](workflow/01-input-processing.md)** — 识别案件类型、自动推荐文案类型和人设
2. **[确定文案类型](workflow/02-script-type.md)** — 5种文案类型选择
3. **[钩子路由](workflow/03-hook-routing.md)** — 8种爆款钩子手法 × 适配矩阵
4. **[撰写口播文案](workflow/04-writing.md)** — 4种类型模板 + 观点干货版心法
5. **[润色与输出](workflow/05-polish-output.md)** — 一致性检查、平台适配、输出格式

## 核心规则与参考

- [爆款公式体系](rules/hook-system.md) — 8种钩子手法 + 适配矩阵
- [人设风格](rules/persona-styles.md) — 3种语气风格定义
- [平台适配](rules/platform-adaptation.md) — 抖音/视频号/小红书差异化
- [质量检查](rules/quality-control.md) — 注意事项 + 自查清单
- [输出格式模板](output/template.md) — 标准输出结构

## 工具与模块

- [验证脚本](scripts/validate_script.py) — 10项自动质量检查
- [反馈模块](modules/feedback.md) — 用户反馈收集
- [保存模板](modules/save-template.md) — 输出模板本地保存

## References

- `references/narrative-templates.md` — 完整撰写规范 + 平台适配细则 + 示例
- `references/design-archive.md` — 设计存档
