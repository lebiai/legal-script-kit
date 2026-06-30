#!/usr/bin/env python3
"""
律师口播文案自查引擎 (V5)
==========================
检查项：
  1. ✅ 化名规则 — 无"张先生/李女士"等无辨识度代称
  2. ✅ 钩子标注 — 必须标注 🎣 爆款钩子
  3. ✅ 律师立场 — 含 <lawyer_stance> 标签
  4. ✅ "我们"原则 — 使用"我们/我"而非"律师"自称
  5. ✅ 立场一致性 — 前后态度统一
  6. ✅ 字数范围 — ≤400 字（超过建议拆集）
  7. ✅ 预估时长标注
  8. ✅ 元数据行完整性
  9. ✅ 钩子长度 ≤18 字
  10. ✅ 连接句存在

用法:
  python3 scripts/validate_script.py [path-to-markdown]
  直接运行自动选最新文件
"""
import re, os, sys
from pathlib import Path

SCRIPTS_DIR = Path.home() / "Desktop" / "律师" / "口播视频" / "口播文案"
FALLBACK_DIR = Path.home() / "Desktop" / "律师" / "口播视频" / "口播文案"

FORBIDDEN_NAMES = ["张先生", "李女士", "王先生", "王女士", "赵先生", "赵女士",
                   "刘先生", "刘女士", "陈先生", "陈女士", "杨先生", "杨女士"]

REQUIRED_META = ["核心观点", "来源案件", "人设风格", "总字数", "预估时长", "适配平台", "爆款钩子"]
THIRD_PERSON = ["律师说", "李律师说", "律师认为", "李律师认为"]


class ScriptValidator:
    def __init__(self, text: str, filepath: str):
        self.text = text
        self.filepath = filepath
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed: list[str] = []

    def add_error(self, msg): self.errors.append(f"  ✗ {msg}")
    def add_warning(self, msg): self.warnings.append(f"  ⚠ {msg}")
    def add_pass(self, msg): self.passed.append(f"  ✓ {msg}")

    def check_01_anonymization(self):
        # Check forbidden name patterns
        found_named = [n for n in FORBIDDEN_NAMES if n in self.text]
        # Also check for 化名 patterns like 老X, 小X
        # 化名模式: 老+姓氏(常见姓) 或 小+姓氏
        # 化名模式: 老+姓氏 或 小+姓氏
        surname_pattern = r'(?:老|小)(?:张|李|王|赵|刘|陈|杨|黄|周|吴|徐|孙|马|胡|朱|郭|何|罗|高|林|梁|宋|郑|谢|韩|唐|冯|董|程|曹|袁|邓|许|傅|沈|曾|彭|吕|苏|卢|蒋|蔡|贾|丁|魏|薛|叶|阎|余|潘|杜|戴|夏|钟|汪|田|任|姜|范|方|石|姚|谭|廖|邹|熊|金|陆|郝|孔|白|崔|康|毛|邱|秦|江|史|顾|侯|邵|孟|龙|万|段|漕|钱|汤|尹|黎|易|常|武|乔|贺|赖|龚|文)'
        found_pattern = re.findall(surname_pattern, self.text)
        found = found_named + found_pattern
        if found:
            self.add_error(f"出现人物名称: {set(found)}（使用'当事人'/'他'/'她'替代）")
        else:
            self.add_pass("当事人规则: 无人物名称")

    def check_02_hook(self):
        if "🎣" in self.text and "爆款钩子" in self.text:
            m = re.search(r'🎣\s*爆款钩子[：:]\s*([A-Z]\s*\+?\s*[A-Z]*)', self.text)
            if m:
                self.add_pass(f"钩子标注完整: {m.group(1)}")
            else:
                self.add_warning("找到 🎣 但格式不规范")
        else:
            self.add_error("缺少 🎣 爆款钩子 标注")

    def check_03_stance(self):
        if "<lawyer_stance>" in self.text and "</lawyer_stance>" in self.text:
            required = ["our_client", "opponent", "attitude_toward_client",
                        "core_belief", "battle_cry"]
            missing = [f for f in required if f"<{f}>" not in self.text]
            if missing:
                self.add_warning(f"立场卡缺少字段: {missing}")
            else:
                self.add_pass("律师立场卡完整")
        else:
            self.add_warning("缺少 <lawyer_stance> 立场卡")

    def check_04_first_person(self):
        found_third = [p for p in THIRD_PERSON if p in self.text]
        if found_third:
            self.add_error(f"使用第三人称自称: {found_third}")
        else:
            self.add_pass('"我们"原则: 未使用第三人称')

    def check_05_stance_consistency(self):
        styles = re.findall(r'人设风格[：:]\s*([^\|\n]+)', self.text)
        if len(set(styles)) <= 1:
            self.add_pass("人设风格一致")
        else:
            self.add_error(f"人设风格不统一: {set(styles)}")

    def check_06_word_count(self):
        if "## 口播文案" in self.text:
            script_part = self.text.split("## 口播文案")[-1]
        else:
            script_part = self.text
        cn_chars = re.findall(r'[\u4e00-\u9fff]', script_part)
        count = len(cn_chars)
        if count > 400:
            self.add_warning(f"文案 {count} 字 > 400，建议拆集")
        else:
            self.add_pass(f"文案 {count} 字 (≤400 ✅)")

    def check_07_duration(self):
        if "预估时长" in self.text:
            m = re.search(r'预估时长[：:]\s*(\d+)秒', self.text)
            if m:
                self.add_pass(f"时长标注: {m.group(1)}秒")
            else:
                self.add_warning("时长格式不标准")
        else:
            self.add_warning("缺少预估时长")

    def check_08_metadata(self):
        missing = [m for m in REQUIRED_META if m not in self.text]
        if missing:
            self.add_warning(f"元数据缺少: {missing}")
        else:
            self.add_pass("元数据行完整")

    def check_09_hook_length(self):
        # Extract first sentence after ## 口播文案 that starts with 你
        if "## 口播文案" in self.text:
            script_part = self.text.split("## 口播文案", 1)[1]
            # Find first line starting with 你 (not bullet or code)
            for line in script_part.split("\n"):
                line = line.strip()
                if line.startswith("你") and not line.startswith("```"):
                    # Extract up to first sentence boundary (.!？。！)
                    hook = re.split(r'[。！？.!]', line)[0]
                    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', hook))
                    if cn_chars > 18:
                        self.add_error(f"钩子句 {cn_chars} 字 > 18字限制: 「{hook.strip()[:25]}…」")
                    else:
                        self.add_pass(f"钩子句 {cn_chars} 字 (≤18 ✅): 「{hook.strip()[:25]}」")
                    return
            self.add_warning("未找到以'你'开头的钩子句")
        else:
            self.add_warning("未找到 ## 口播文案 分区")

    def check_10_hook_connector(self):
        # Check that the second sentence is a connection sentence
        if "## 口播文案" in self.text:
            script_part = self.text.split("## 口播文案", 1)[1]
            lines = [l.strip() for l in script_part.split("\n") if l.strip() and not l.startswith("```")]
            for i, line in enumerate(lines):
                if line.startswith("你"):
                    # Check next non-empty line
                    for j in range(i+1, min(i+3, len(lines))):
                        next_line = lines[j]
                        if any(k in next_line for k in ["是不是", "觉得", "以为", "很多人", "大部分人", "大多数",
                            "90%", "所有人", "大家都", "谁不", "你想想", "你仔细想"]):
                            self.add_pass(f"连接句存在")
                            return
                        elif next_line.startswith("你") or next_line.startswith("法院"):
                            # Another hook-like sentence, not a connector
                            continue
                        else:
                            break
                    self.add_warning("钩子后缺少连接句（'你是不是也这么想的？'）")
                    return
            self.add_warning("未找到以'你'开头的钩子")
        else:
            self.add_warning("未找到 ## 口播文案 分区")

    def report(self) -> bool:
        name = Path(self.filepath).stem
        print(f"\n{'='*60}")
        print(f"📋 文案自查报告 — {name}")
        print(f"📁 {self.filepath}")
        print(f"{'='*60}")
        print()

        for fn in [self.check_01_anonymization, self.check_02_hook,
                    self.check_03_stance, self.check_04_first_person,
                    self.check_05_stance_consistency, self.check_06_word_count,
                    self.check_07_duration, self.check_08_metadata,
                    self.check_09_hook_length, self.check_10_hook_connector]:
            fn()

        print(f"\n{'─'*60}")
        print(f"📊 结果汇总 (10/10 项检查)")
        print(f"{'─'*60}")
        for p in self.passed: print(p)
        for w in self.warnings: print(w)
        for e in self.errors: print(e)

        total = len(self.passed) + len(self.warnings) + len(self.errors)
        print(f"\n  通过: {len(self.passed)} | 警告: {len(self.warnings)} | "
              f"错误: {len(self.errors)} | 总计: {total}")
        print(f"{'='*60}")
        return len(self.errors) == 0


def main():
    if len(sys.argv) < 2:
        for d in [SCRIPTS_DIR, FALLBACK_DIR]:
            if d.exists():
                files = sorted(d.glob("*.md"))
                if files:
                    paths = [str(files[-1])]
                    break
        else:
            print("用法: python3 validate_script.py <path-to-markdown>")
            sys.exit(1)
    else:
        paths = [os.path.expanduser(p) for p in sys.argv[1:]]

    all_pass = True
    for path in paths:
        if not os.path.exists(path):
            print(f"文件不存在: {path}")
            all_pass = False
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if not ScriptValidator(text, path).report():
            all_pass = False
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
