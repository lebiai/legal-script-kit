# Legal Script Kit — 律师案例转口播文案

将判决书、案情材料转化为短视频口播文案的 Codex Skill。

内置爆款钩子体系（8 种钩子手法）、5 种文案类型（分享/分析/吃瓜/观点/观点干货版）、3 种人设风格。

## 安装

```bash
# 通过 GitHub 克隆到本地 Codex skills 目录
git clone https://github.com/lebiai/legal-script-kit.git ~/.codex/skills/legal-script-kit
```

或直接复制 `skill-lawyer-case-to-script/` 到 `~/.codex/skills/` 下。

## 使用

在 Codex 中触发：

```
使用 $skill-lawyer-case-to-script 将下面的案件材料转化为口播文案。
【案件材料】
...
```

## 结构

```
legal-script-kit/
├── skill-lawyer-case-to-script/
│   ├── SKILL.md                    ← 入口文件
│   ├── agents/openai.yaml          ← 配置
│   ├── workflow/                   ← 撰写流程（5步）
│   ├── rules/                      ← 核心规则
│   ├── references/                 ← 参考资料
│   ├── scripts/                    ← 工具脚本
│   ├── modules/                    ← 功能模块
│   └── output/                     ← 输出模板
├── README.md
└── .gitignore
```

## 关联项目

- [attorney-skills](https://github.com/lebiai/attorney-skills) — 律师案件分析 + 诉讼策略 Skill
- skill-lawyer-case-video — 口播文案 → Grok 视频提示词（Coming Soon）
