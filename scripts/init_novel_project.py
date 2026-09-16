#!/usr/bin/env python3
"""初始化 AI 长篇小说项目：复制全套模板到目标目录，并可选初始化 git 仓库。

用法：
    python3 init_novel_project.py <目标目录> [--no-git] [--force]

行为：
  - 复制 assets/novel-project-templates/ 下全部文件到目标目录（保留目录结构）
  - 默认**不覆盖已存在的文件**（事实唯一/先盘点原则），已存在的会被跳过并列出
  - 复制完成后执行 git init + 首次提交（除非指定 --no-git，或目标目录已是仓库）
  - 输出创建清单 / 跳过的文件 / 下一步待填内容

退出码：0 成功；1 参数或路径错误。
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def copy_templates(src: Path, dst: Path, force: bool):
    """返回 (created, skipped) 两个相对路径列表。"""
    created, skipped = [], []
    for item in sorted(src.rglob("*")):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped.append(str(rel))
            continue
        shutil.copy2(item, target)
        created.append(str(rel))
    return created, skipped


def run_git(target: Path) -> str:
    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=target, capture_output=True, text=True
        )

    if (target / ".git").exists():
        return "目标目录已是 git 仓库，跳过初始化"
    if git("init").returncode != 0:
        return "git init 失败（可能未安装 git）"
    git("add", ".")
    commit = git(
        "commit",
        "-m",
        "初始化：AI长篇小说写作工作流模板\n\n"
        "- 3 总控文件 + 写作规则 + 人物/大纲/追踪全套模板\n"
        "- 章节合同模板 + 正文/待确认/审核与复盘 目录说明\n"
        "- 未包含任何正文内容，等待作者填写资料",
    )
    if commit.returncode != 0:
        return "git init 完成，提交失败（无 user.name/email 或无变更）"
    return "git 仓库已初始化并完成首次提交"


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化 AI 长篇写作工作流项目")
    parser.add_argument("target", help="项目目录路径（不存在会自动创建）")
    parser.add_argument("--no-git", action="store_true", help="不初始化 git 仓库")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件（危险）")
    args = parser.parse_args()

    src = skill_root() / "assets" / "novel-project-templates"
    if not src.is_dir():
        print(f"错误：找不到模板目录 {src}", file=sys.stderr)
        return 1

    dst = Path(args.target).expanduser().resolve()
    dst.mkdir(parents=True, exist_ok=True)

    created, skipped = copy_templates(src, dst, args.force)

    print(f"项目目录：{dst}\n")
    print(f"已创建 {len(created)} 个文件：")
    for f in created:
        print(f"  + {f}")
    if skipped:
        print(f"\n已存在、未覆盖 {len(skipped)} 个文件（先盘点不覆盖原则）：")
        for f in skipped:
            print(f"  - {f}")

    if not args.no_git:
        print(f"\n{run_git(dst)}")

    print("\n下一步（必须由作者填写，AI 不得代填）：")
    print("  1. 01-开书定位.md      七问：读者/类型/情绪/三个为什么")
    print("  2. 02-核心设定.md      七项：一句话故事/冲突/发动机/终局/硬约束")
    print("  3. 人物/主角.md        九要素人物卡")
    print("  4. 大纲/全书大纲.md    终局/对立力量/阶段升级/不可逆节点")
    print("  5. 大纲/滚动细纲       至少填 001—003 章")
    print("\n填写完成后口令：按这套工作流写第 1 章")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
