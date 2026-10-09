# Codex Skill · 宝可梦朱紫风格图片提示词

输出稳定的「宝可梦 朱／紫 原版实机游戏截图」风格图片提示词。只写提示词，不出图。

结构和 [xiaoTN/zelda-style-image-prompt](https://github.com/xiaoTN/zelda-style-image-prompt) 里的 `zelda-style-image-prompt` 保持一致（`SKILL.md` + `references/` + `evals/`），但视觉规则是按朱紫自己的截图语言重写的，不是把塞尔达那份改个名字。

## 目录结构

```text
├── SKILL.md                                      # 触发条件 + 提示词模板 + 填写规则 + 输出模式
├── references/pokemon-scarlet-violet-visual-style.md   # 完整视觉规范、玩法状态与 HUD 矩阵、地名 UI、元素池、必须避免清单
└── evals/evals.json                              # 3 条测试用例
```

## 安装

```bash
git clone https://github.com/Ryestudio1/pokemon-sv-image-prompt.git

mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/pokemon-scarlet-violet-image-prompt"
cp -R pokemon-sv-image-prompt/. "${CODEX_HOME:-$HOME/.codex}/skills/pokemon-scarlet-violet-image-prompt/"
```

安装到当前项目：

```bash
mkdir -p .codex/skills/pokemon-scarlet-violet-image-prompt
cp -R pokemon-sv-image-prompt/. .codex/skills/pokemon-scarlet-violet-image-prompt/
```

目标目录名必须和 `SKILL.md` frontmatter 里的 `name` 一致（`pokemon-scarlet-violet-image-prompt`），否则 skill 扫描时会对不上。frontmatter 只有 `name` 和 `description` 两个字段，同一份文件可以直接放进 Qoder 的 skills 目录使用。

安装后重启 Codex，让 skill 被重新扫描。

## 使用

```text
使用 pokemon-scarlet-violet-image-prompt，帮我写一个杭州西湖苏堤的宝可梦朱紫风格图片提示词，不用出图。
```

输出示例（直接可交给生图模型）：

```text
宝可梦朱紫原版实机游戏截图复刻
画风：Nintendo Switch 宝可梦 朱／紫 开放世界实机截图风格；不要电影 CG、不要写实摄影、不要动画番剧赛璐璐截图、不要厚涂同人插画
朱紫默认造型，学院制服训练家 + 同行宝可梦

帕底亚地图区块：杭州·西湖苏堤
画面要素：六桥烟柳、长堤、湖面、保俶塔远景、石狮望柱
玩法时刻：训练家在堤边投出精灵球
玩法状态：捕捉
宝可梦：美纳斯
帕底亚元素：洛托姆图鉴、友好商店招牌、观察台、柳树草丛、湖面涟漪
地名 UI 文字（区域发现）：中间「杭州·苏堤」 / 下方「浙江·杭州」；单行圆润白字带细描边、淡入、无矩形边框、无深色底纹
HUD：按朱紫原版「捕捉」界面自然出现，不堆满
文字：所有可读 UI 使用简体中文，措辞用原版游戏文案，如「野生的…出现了！」「快扔球！」
```

## 相对塞尔达原版改了什么

| 字段 | 塞尔达原版 | 本 skill（朱紫） |
| --- | --- | --- |
| 玩法状态 | 靠「耐力轮是否出现」间接表达 | **独立必填字段**，5 选 1，直接决定 HUD |
| HUD | 按动作自然出现 1-3 种 | 按玩法状态出现，HUD 行必须复用同一状态词 |
| 地名 UI | 三段式「发现！」卡 + 短横线装饰 | 两行式区域名浮现（主地名 + 副标题），无三段式 |
| 现代设施 | 转译为驿站 / 木牌 / 机关 / 马车索道 | **保留**并柔化（帕底亚本来就有公路、风车、港口、咖啡馆） |
| 主体数量 | 1 个角色 | 宝可梦 ≤ 2 只，大型 / 传说最多 1 只 |
| 机制边界 | BOTW / TOTK 两版造型切换 | 禁止混用极巨化、超级进化等非朱紫机制 |

「少写」哲学与原仓库一致：角色造型、材质、光线、焦段、身体微观动作一律不写进 prompt；文档里的具体外观描述只作为出图后人工审图的判断依据。

## 已知未验证

`references/` 第 7 节的必须避免清单是按两个游戏的画面语言差异推断出来的，**还没有经过真实出图验证**（塞尔达那份的同类清单是作者实测沉淀的）。跑图后如果发现别的翻车模式，欢迎开 issue 或直接 PR 补充条目。

## 声明

本仓库只包含提示词写作规则和参考文档，不包含游戏原始模型、字体、音频、任天堂或 The Pokémon Company 的官方资源。

本项目与 Nintendo、Game Freak、Creatures、The Pokémon Company、宝可梦 朱／紫（Pokémon Scarlet and Violet）或其权利方没有关联、授权、赞助或背书关系。项目中出现的游戏名称、角色名称和商标仅用于描述提示词风格与兼容场景，相关知识产权归各自权利人。

使用本仓库中的 skill 生成、发布或商用任何内容时，请自行确认是否符合相关平台规则、模型服务条款和知识产权要求。

## License

MIT
