# ai-novel-workflow

AI 长篇小说写作工作流。一套可复用的 skill + 项目模板，用于让 AI 稳定地协助写完一部长篇——**AI 负责执行，作者负责灵魂**。

解决的核心问题：AI 写长篇最常见的三种崩法——写着写着忘了前文设定、擅自编造世界观、未经验证就把稿子当正稿。本工作流用「目录模板化 + 章节循环化 + 事实唯一化」三件事把它们堵住。

---

## 一、安装

### 1.0 先看清目录结构（两个平台通用）

不管装到哪个平台，**外层目录名必须叫 `ai-novel-workflow`，且 `SKILL.md` 必须在它的第一层**：

```
ai-novel-workflow/          ← 目录名 = skill 名，不能改
├── SKILL.md                ← 必需，第一层，不能是 ai-novel-workflow/xxx/SKILL.md
├── scripts/
├── references/
└── assets/
```

平台只扫描 skills 目录的**下一层**。多套一层文件夹、或目录名写成 `ai-novel-workflow-main`（GitHub 下载的 zip 默认名字），都不会被识别——这是装不上最常见的原因。

### 1.1 平台 A：WorkBuddy

| 级别 | 路径 |
|---|---|
| 用户级（所有项目可用，推荐） | `~/.workbuddy/skills/ai-novel-workflow/` |
| 项目级（只当前项目用） | `<项目根>/.workbuddy/skills/ai-novel-workflow/` |

```bash
# 用户级（推荐）
git clone git@github.com:yyl1208/ai-novel-workflow.git ~/.workbuddy/skills/ai-novel-workflow
```

已经 clone 过、或用 zip 装的，注意**去掉 `-main` 后缀**：

```bash
# GitHub 下载的 zip 解压后通常是 ai-novel-workflow-main
unzip ai-novel-workflow.zip -d ~/.workbuddy/skills/
mv ~/.workbuddy/skills/ai-novel-workflow-main ~/.workbuddy/skills/ai-novel-workflow
```

项目级：

```bash
mkdir -p .workbuddy/skills
cp -R ~/.workbuddy/skills/ai-novel-workflow .workbuddy/skills/
```

验证：

```bash
ls ~/.workbuddy/skills/ai-novel-workflow/SKILL.md
```

**怎么用**：直接说人话就行，不用记命令。WorkBuddy 会按 `SKILL.md` 的 description 自动匹配触发：

> 「帮我搭一个小说写作工作流」
> 「按这套工作流写第 5 章」

已安装的 skill 出现在对话的技能列表里，也可以显式点名调用：`/ai-novel-workflow`。新装的 skill 如果没出现在列表里，重开一次对话即可。

### 1.2 平台 B：Codex（CLI / 桌面版）

Codex 自 2025-12 起支持 Agent Skills 规范，目录结构与 WorkBuddy 完全一致，**同一份文件两个平台通用，不需要分别改造**。

| 级别 | 路径 | 优先级 |
|---|---|---|
| 仓库级（当前目录） | `$CWD/.codex/skills/ai-novel-workflow/` | 最高 |
| 仓库级（仓库根） | `$REPO_ROOT/.codex/skills/ai-novel-workflow/` | 中 |
| 用户级（推荐） | `~/.codex/skills/ai-novel-workflow/` | 低 |
| 管理员级 | `/etc/codex/skills/ai-novel-workflow/` | 最低 |

同名冲突时优先级高的覆盖低的。日常写书放**用户级**最省事；要随仓库提交给团队共享才用项目级。

```bash
# 用户级（推荐，所有项目可用）
git clone git@github.com:yyl1208/ai-novel-workflow.git ~/.codex/skills/ai-novel-workflow
```

项目级（随仓库提交，团队共享）——两种放法 Codex 都能扫到，二选一即可：

```bash
mkdir -p .codex/skills && cp -R ~/.codex/skills/ai-novel-workflow .codex/skills/
# 或
mkdir -p .agents/skills && cp -R ~/.codex/skills/ai-novel-workflow .agents/skills/
```

验证：

```bash
ls ~/.codex/skills/ai-novel-workflow/SKILL.md
codex --list-skills          # 看 Codex 是否真的解析成功
```

**怎么用**：Codex 每次启动会扫描 skills 目录并自动加载，装完直接对话即可：

```bash
codex "帮我搭一个小说写作工作流"
codex "按这套工作流写第 5 章"
```

新装的 skill 一般自动检测；若没生效，**重启 Codex 强制重新扫描**一次。也可以用环境变量改目录：`export CODEX_SKILLS_PATH=/path/to/skills`（目录需先存在）。

### 1.3 两个平台都装（推荐做法）

放一份、另一份做软链，更新时只改一处：

```bash
# 先装 WorkBuddy
git clone git@github.com:yyl1208/ai-novel-workflow.git ~/.workbuddy/skills/ai-novel-workflow
# Codex 指向同一份
mkdir -p ~/.codex/skills
ln -s ~/.workbuddy/skills/ai-novel-workflow ~/.codex/skills/ai-novel-workflow
```

更新：

```bash
cd ~/.workbuddy/skills/ai-novel-workflow && git pull
```

> Windows 路径对应：`%USERPROFILE%\.workbuddy\skills\` 与 `%USERPROFILE%\.codex\skills\`。

---

## 二、30 秒搭一个新书项目

```bash
# WorkBuddy
python3 ~/.workbuddy/skills/ai-novel-workflow/scripts/init_novel_project.py "~/Documents/我的新书"

# Codex（换成你的安装路径即可）
python3 ~/.codex/skills/ai-novel-workflow/scripts/init_novel_project.py "~/Documents/我的新书"
```

也可以让 AI 自己跑——直接说「帮我搭一个小说写作工作流」，它会找到这个脚本并执行。

一条命令完成：

- 复制 6 个目录 + 19 个模板文件
- `git init` + 首次提交（提交信息注明"未包含任何正文"）
- 输出待填清单

已存在的文件**默认跳过不覆盖**（先盘点原则）。参数：

| 参数 | 作用 |
|---|---|
| `--no-git` | 不初始化 git |
| `--force` | 覆盖已有文件（危险，慎用） |

---

## 三、完整写小说的过程

### 第 1 步：搭项目

如上，一条命令。产出目录结构：

```
我的新书/
├── 00-项目状态.md      仪表盘：当前章节、必读清单、待确认项、下一步入口
├── 01-开书定位.md      七问：写给谁 / 什么类型 / 什么情绪 / 三个"为什么"
├── 02-核心设定.md      七项：一句话故事 / 冲突 / 剧情发动机 / 终局 / 硬约束
├── 写作规则.md         八条铁律 + 八步循环 + 冷读清单 + 问题分级
├── 人物/               主角卡、配角卡（九要素）、人物关系
├── 大纲/               全书大纲、分卷大纲、滚动细纲（只细化未来 5—12 章）
├── 追踪/               时间线、角色状态、伏笔、资源与权限
├── 正文/               只有通过裁决的章节
├── 待确认/             初稿、修改稿、试验稿
└── 审核与复盘/         章节合同、冷读报告、滚动复盘
```

### 第 2 步：作者填 5 份资料

顺序不能乱，后者依赖前者：

1. **01-开书定位**（七问）——目标读者、主类型、核心情绪、主角初始困境、读者为什么点开 / 读十章 / 读几十万字
2. **02-核心设定**（七项）——一句话故事、主线目标、失败代价、核心冲突、**重复剧情发动机**、终局方向、不可改设定
3. **人物/主角卡**（九要素）——公开目标、当前利益、私下欲望、害怕失去、底线与缺陷、资源与权限、利益冲突、语言指纹、重大刺激反应
4. **全书大纲 + 分卷大纲（卷一）**——终局、对立力量、阶段升级、不可逆节点
5. **滚动细纲**（至少填 001—003 章）

> AI 不代填。资料缺失时 AI 会停下提问，绝不擅自编造主角、世界观或主线。

### 第 3 步：资料自洽检查

填完后 AI 交叉核对：一句话故事 vs 核心冲突、主角欲望 vs 初始困境、剧情发动机 vs 预计篇幅、大纲终局 vs 设定终局、卷一 vs 全书第一阶段、第一章细纲 vs "读者为什么点开"。

### 第 4 步：逐章写作（八步循环）

口令：**「按这套工作流写第 N 章」**

```
01 LOAD     读取资料    00状态必读清单、写作规则、细纲、上一章、人物卡、追踪四件套
02 CHECK    写前检查    冲突 / 缺失 / 时间 / 资源 / 权限，缺一样问一样
03 CONTRACT 章节合同    十问填满，任何一问只能答"为了推进剧情" → 退回细纲
04 DRAFT    写初稿      按场景写，存入「待确认/」，不进正文
05 REVIEW   读者冷读    六问检查，报告记 S1/S2/S3
06 REVISE   修改问题    S1、S2 必须清零
07 UPDATE   回写数据库  时间 / 人物 / 关系 / 伏笔 / 资源 / 下一章必读
08 DECIDE   作者裁决    通过 → 转正 + git 提交；退回 → 改；废稿 → 弃
```

**十问合同**：读者追什么问题？失败失去什么？最值得看的场面？主角主动要完成什么？谁在阻止？关键选择？时间地点人物道具从哪来？有权有能力吗？本章改变什么？章尾什么不可逆新局面？——加问：读者为什么现在点下一章？

**冷读六问**：这是谁为什么这样做？凭什么决定、资源哪来？有没有失忆越权写偏？场景能不能看见？哪里想跳读？章尾追不追？

**问题分级**：S1 设定/动机/逻辑错误（必须清零）、S2 节奏/读感/追读（必须清零）、S3 局部表达（交稿前尽量清零）。

### 第 5 步：裁决与归档

作者说「通过」后，AI 执行：稿件移入 `正文/第NNN章-标题.md` → 删除 `待确认/` 下的副本（**不留双份**）→ git 提交一次 → 回写追踪文件与 00 状态。

### 第 6 步：滚动维护

- **滚动细纲**：永远只保持覆盖未来 5—12 章，写完往前滚
- **滚动复盘**：每 5—10 章一次，三问——保留什么 / 停止什么 / 试验什么
- **设定变更**：正文与设定冲突以正文为准，变更记入 02 登记表；被否决的设定进 00「禁止恢复的旧设定」

---

## 四、四条护栏

1. **先盘点**——不扫描不覆盖，已有正式文件一律保留
2. **不写正文**——搭建阶段只放目录、模板、规则；方向未经作者确认不动笔
3. **事实唯一**——`正文/` 是唯一事实源；`待确认/` 的稿在裁决前不算事实，转正后删除
4. **交付可查**——每次都要报告：创建清单、冲突、待填内容、每章执行顺序

---

## 五、Skill 使用教程

### 触发方式

装好后，在对话中直接说这些话，AI 会自动加载本 skill：

| 你说 | AI 做什么 |
|---|---|
| 「帮我搭一个小说写作工作流」 | 建目录、复制模板、初始化 git、交付四项报告 |
| 「按这套工作流写第 N 章」 | 执行八步循环 |
| 「写一章章节合同」 | 生成十问合同 |
| 「给这一章做冷读」 | 按六问检查并出 S1/S2/S3 报告 |
| 「回写数据库」 | 同步追踪四件套 |
| 「做一次滚动复盘」 | 三问复盘 |

也可以显式调用：`/ai-novel-workflow`（部分客户端支持）。

### 各平台调用差异

| | WorkBuddy | Codex |
|---|---|---|
| 加载时机 | 对话中按语义自动匹配 | 每次启动扫描目录并加载 |
| 触发方式 | 直接说「按这套工作流写第 N 章」 | `codex "按这套工作流写第 N 章"` |
| 显式调用 | `/ai-novel-workflow` | 不支持斜杠命令，写进 `AGENTS.md` 或直接在提示词点名 |
| 装完不生效 | 重开一次对话 | 重启 Codex 强制扫描；`codex --list-skills` 排查 |

Codex 用户建议在仓库根 `AGENTS.md` 里加一行，让每次都能稳定命中：

```markdown
写小说章节时使用 skill `ai-novel-workflow`，按八步循环执行。
```

### 三种工作模式

| 模式 | 何时用 | 核心动作 |
|---|---|---|
| **A 搭建** | 新书立项 | 脚手架脚本 + 模板 + git |
| **B 写作** | 逐章推进 | 八步循环 |
| **C 维护** | 长线运营 | 细纲滚动、复盘、设定变更登记 |

### AI 读哪些文件

```
SKILL.md                          核心流程（触发时必读）
├── references/eight-step-loop.md 八步详细规程（写章节前读）
├── references/template-guide.md  模板用途、填写顺序、自洽检查清单
├── references/platform-notes.md  平台差异、赛道信号、调研方法
├── scripts/init_novel_project.py 脚手架（执行，不读入上下文）
├── OWNERS                        维护者
├── EVAL.yaml                     评测集
└── assets/novel-project-templates/  19 个模板（复制到新项目）
```

采用渐进披露：只有 SKILL.md 常驻上下文，references 按需读取，assets 不读入——省 token。

---

## 六、评测

`EVAL.yaml` 定义 4 个用例（搭建 / 写作 / 缺资料护栏 / 事实唯一归档），每条带 expectations 与分级 rubric（严重 / 普通 / 轻微）。方法参照 Agent Skills 工程实践：对比「有 skill」与「无 skill」，从 **accuracy** 与 **efficiency** 两个维度打分。

首次执行结果见 `EVAL-RESULTS.md`，关键数据：

- 搭建环节：无 skill 约 23 次工具调用、手写 633 行 → 有 skill **1 次调用、手写 0 行**，重复执行零覆盖
- 3 个用例通过，1 个（归档）待首章裁决后复测

---

## 七、License

MIT
