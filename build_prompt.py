#!/usr/bin/env python3
"""Assemble and self-check the 宝可梦朱紫 image-prompt template.

Usage:
  python3 build_prompt.py --place 杭州·苏堤 --region 浙江·杭州 \
      --elements 六桥烟柳,长堤,湖面 --action 训练家在堤边投出精灵球 \
      --state 捕捉 --pokemon 美纳斯 --parts 洛托姆图鉴,友好商店招牌
  python3 build_prompt.py --check prompt.txt
Windows: py -3 build_prompt.py ...
"""

import argparse
import re
import sys

ANCHOR = "宝可梦朱紫原版实机游戏截图复刻"
STYLE = ("画风：Nintendo Switch 宝可梦 朱／紫 开放世界实机截图风格；"
         "不要电影 CG、不要写实摄影、不要动画番剧赛璐璐截图、不要厚涂同人插画")
DEFAULT_LOOK = "朱紫默认造型，学院制服训练家 + 同行宝可梦"
WILD_LOOK = "朱紫默认造型，野生宝可梦场景，无训练家"
UI_LINE = ("地名 UI 文字（区域发现）：中间「{place}」 / 下方「{region}」；"
           "单行圆润白字带细描边、淡入、无矩形边框、无深色底纹")
HUD_LINE = "HUD：按朱紫原版「{state}」界面自然出现，不堆满"
TEXT_LINE = "文字：所有可读 UI 使用简体中文，措辞用原版游戏文案，如「野生的…出现了！」「快扔球！」"

STATES = ("探索移动", "野生遭遇", "捕捉", "太晶对战", "野餐料理")
LARGE_POKEMON = ("故勒顿", "基拉尼", "卡比兽", "暴鲤龙", "快龙")
KNOWN_POKEMON = ("皮卡丘 伊布 喷火龙 妙蛙种子 杰尼龟 小火龙 耿鬼 路卡利欧 美纳斯 沙奈朵 "
                 "暴鲤龙 化石翼龙 快龙 卡比兽 新叶喵 呆火鳄 润水鸭 故勒顿 基拉尼").split()
TERA_TYPES = ("普通 火 水 草 电 冰 格斗 毒 地面 飞行 超能力 虫 岩石 幽灵 龙 恶 钢 妖精").split()
INGAME_PLACES = ("帕底亚 酿光市 星尘镇 染勿朵 钵卷 卡洛斯 丰缘 神奥 合众 伽勒尔 洗翠 Paldea "
                 "Mesagoza Levincia Cascarrafa Alfornada Montenevera").split()
POSITION_WORDS = ("左上", "右上", "左下", "右下", "屏幕", "居中", "角落", "边缘", "垂直排列", "紧贴")
SHAPE_WORDS = ("圆形", "圆角", "矩形", "弧形", "六边形", "正圆", "边框", "底纹", "刻度")
COUNT_WORDS = (r"\d+\s*[个颗格条只]", r"Lv\.?\s*\d+", r"HP\s*剩", r"\d+\s*星")
REALISM_WORDS = ("写实", "真实材质", "质感", "毛发细节", "HDR", "光线追踪", "体积光", "焦段", "微距", "85mm")
BODY_WORDS = ("重心", "指尖", "最后一帧", "倾斜", "肌肉", "瞳孔", "半展开", "离手", "蓄力")
BODY_PATTERNS = (r"\d+\s*度", r"\d+\s*厘米", r"\d+\s*%\s*展开")
ENGLISH_UI_WORDS = (r"\bWILD\b", r"\bAPPEARED\b", r"\bBATTLE\b", r"\bRUN\b", r"\bTHROW\b",
                    r"\bPOKEMON\b", r"\bDEX\b", r"\bRAID\b", r"\bTERA\b", r"\bATTACK\b", r"\bEXAMINE\b")
BANNED_EXTRA = ("二维码", "emoji", "水印", "Logo", "一群", "宣传")


def split_list(value):
    return [x.strip() for x in re.split(r"[,，、]", value) if x.strip()]


def build(args):
    look = WILD_LOOK if args.no_trainer else DEFAULT_LOOK
    block = args.block or args.place
    lines = [
        ANCHOR,
        STYLE,
        look,
        "",
        f"帕底亚地图区块：{block}",
        "画面要素：" + "、".join(args.elements),
        f"玩法时刻：{args.action}",
        f"玩法状态：{args.state}",
    ]
    if args.pokemon:
        lines.append("宝可梦：" + "、".join(args.pokemon))
    if args.state == "太晶对战" and args.tera:
        lines.append(f"太晶属性：{args.tera}")
    lines.append("帕底亚元素：" + "、".join(args.parts))
    lines.append(UI_LINE.format(place=args.place, region=args.region))
    lines.append(HUD_LINE.format(state=args.state))
    lines.append(TEXT_LINE)
    return lines


def check(lines):
    problems, warnings = [], []
    text = "\n".join(lines)

    if not (10 <= len(lines) <= 14):
        problems.append(f"行数 {len(lines)} 不在 10-14 行")
    if lines[0] != ANCHOR:
        problems.append(f"第 1 行心锚词不符：{lines[0]!r}")
    style_line = next((l for l in lines if l.startswith("画风：")), None)
    if style_line is None:
        problems.append("缺少 `画风` 行")
    elif style_line != STYLE:
        problems.append("`画风` 行被改写过——只允许实机截图心锚 + 固定反向禁词，不要追加风格串")

    state_line = next((l for l in lines if l.startswith("玩法状态：")), None)
    if state_line is None:
        problems.append("缺少 `玩法状态` 行")
    else:
        state = state_line.split("：", 1)[1].strip()
        if state not in STATES:
            problems.append(f"玩法状态 {state!r} 不在五选一列表：{'/'.join(STATES)}")
        else:
            others = [s for s in STATES if s != state and (s in text)]
            if others:
                problems.append(f"同时出现多个玩法状态：{state} + {'/'.join(others)}")
            hud = next((l for l in lines if l.startswith("HUD：")), None)
            if hud and state not in hud:
                problems.append("HUD 行没有复用同一个玩法状态词")
            if hud and len(hud) > 40:
                warnings.append("HUD 行偏长，理想是 ≤ 1 句方向性说明")

    pokemon_line = next((l for l in lines if l.startswith("宝可梦：")), None)
    if pokemon_line:
        picked = split_list(pokemon_line.split("：", 1)[1])
        if len(picked) > 2:
            problems.append(f"宝可梦 {len(picked)} 只，超过 2 只上限")
        big = [p for p in picked if p in LARGE_POKEMON]
        if len(big) > 1:
            problems.append(f"大型/传说宝可梦 {len(big)} 只，一张图最多 1 只")
        unknown = [p for p in picked if p not in KNOWN_POKEMON]
        if unknown:
            warnings.append(f"译名不在已确认白名单：{'、'.join(unknown)}；不确定就改成「一只图鉴常见宝可梦」")

    ui_line = next((l for l in lines if l.startswith("地名 UI 文字")), None)
    if ui_line:
        for name in ui_names(ui_line):
            for bad in INGAME_PLACES:
                if bad in name:
                    problems.append(f"UI 地名出现游戏内名称「{name}」，含 {bad}")
        if "「" not in ui_line:
            warnings.append("地名 UI 行没有用「」包出可读文案")

    if "太晶" in text:
        state = state_line.split("：", 1)[1].strip() if state_line else ""
        if state != "太晶对战":
            problems.append(f"玩法状态是「{state}」却出现太晶——太晶只在太晶对战状态出现")

    if not style_line:
        style_line = ""
    body = []
    for l in lines:
        if l == style_line or l == ANCHOR:
            continue
        # 地名 UI 行的固定样式段里带「无矩形边框、无深色底纹」，是否定指令，不参与扫描
        if l.startswith("地名 UI 文字"):
            l = l.split("；", 1)[0]
        body.append(l)
    joined_body = "\n".join(body)
    for w in REALISM_WORDS:
        if w in joined_body:
            problems.append(f"画风行以外出现引导写实的词「{w}」")
    for w in BODY_WORDS:
        if w in joined_body:
            problems.append(f"出现身体微观动作描述「{w}」——动作只写动词")
    for pat in BODY_PATTERNS:
        m = re.search(pat, joined_body)
        if m:
            problems.append(f"出现身体微观动作描述「{m.group(0)}」——动作只写动词")
    for w in POSITION_WORDS + SHAPE_WORDS:
        if w in joined_body:
            problems.append(f"HUD/UI 写死了{('方位' if w in POSITION_WORDS else '形状')}词「{w}」")
    for pat in COUNT_WORDS:
        m = re.search(pat, joined_body)
        if m:
            problems.append(f"写死了 HUD 数量或数值「{m.group(0)}」")
    for pat in ENGLISH_UI_WORDS:
        m = re.search(pat, joined_body, re.I)
        if m:
            problems.append(f"出现英文界面词「{m.group(0)}」")
    for w in BANNED_EXTRA:
        if w in joined_body:
            problems.append(f"出现禁用元素「{w}」")

    return problems, warnings


def ui_names(ui_line):
    return re.findall(r"「([^」]*)」", ui_line)


def main():
    p = argparse.ArgumentParser(description="宝可梦朱紫提示词组装与自检")
    p.add_argument("--place", help="真实主地名，进入 UI")
    p.add_argument("--region", help="真实上级区域名或主题归属，进入 UI")
    p.add_argument("--block", help="帕底亚地图区块字段值，默认同 --place")
    p.add_argument("--elements", help="画面要素，逗号分隔，3-5 个")
    p.add_argument("--action", help="玩法时刻，一句话")
    p.add_argument("--state", help="玩法状态：" + " / ".join(STATES))
    p.add_argument("--pokemon", help="宝可梦，逗号分隔，最多 2 只")
    p.add_argument("--parts", help="帕底亚元素，逗号分隔，3-6 个")
    p.add_argument("--tera", help="太晶属性，仅太晶对战状态")
    p.add_argument("--no-trainer", action="store_true", help="无训练家的野生场景")
    p.add_argument("--check", metavar="FILE", help="只自检已有提示词文件，不生成")
    args = p.parse_args()

    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if args.check:
        with open(args.check, encoding="utf-8") as fh:
            raw = fh.read()
        lines = [l for l in raw.splitlines() if l.strip()]
    else:
        missing = [n for n in ("place", "region", "elements", "action", "state", "parts")
                   if not getattr(args, n)]
        if missing:
            p.error("缺少参数：" + " ".join("--" + m for m in missing))
        args.elements = split_list(args.elements)
        args.parts = split_list(args.parts)
        args.pokemon = split_list(args.pokemon) if args.pokemon else []
        if not 3 <= len(args.elements) <= 5:
            p.error("--elements 需要 3-5 个关键词")
        if not 3 <= len(args.parts) <= 6:
            p.error("--parts 需要 3-6 个关键词")
        if args.tera and args.tera not in TERA_TYPES:
            p.error("--tera 必须是 18 个属性之一：" + "/".join(TERA_TYPES))
        if args.tera and args.state != "太晶对战":
            p.error("--tera 只在 --state 太晶对战 时使用")
        lines = build(args)
        print("\n".join(lines))
        print()

    problems, warnings = check(lines)
    for w in warnings:
        print(f"warn  {w}", file=sys.stderr)
    for e in problems:
        print(f"fail  {e}", file=sys.stderr)
    if problems:
        return 1
    print(f"ok  {len(lines)} 行，自检通过", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
