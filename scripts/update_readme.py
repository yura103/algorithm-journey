from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "assets"
CLOVER = ASSETS / "algorithm-clover.svg"

PLATFORMS = ["백준", "프로그래머스", "LeetCode"]

EXT_LANG = {
    ".py": "Python",
    ".js": "JavaScript",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".sql": "SQL",
}

LANG_PALETTES = {
    "Python": ["#BBDEFB", "#64B5F6", "#1E88E5", "#0D47A1"],
    "C++": ["#C8E6C9", "#81C784", "#43A047", "#1B5E20"],
    "Java": ["#FFCDD2", "#E57373", "#E53935", "#B71C1C"],
    "JavaScript": ["#FFF9C4", "#FFF176", "#FDD835", "#F57F17"],
    "SQL": ["#E1BEE7", "#BA68C8", "#8E24AA", "#4A148C"],
    "C": ["#CFD8DC", "#90A4AE", "#546E7A", "#263238"],
}


def solution_files():
    files = []

    for platform in PLATFORMS:
        base = ROOT / platform

        if base.exists():
            for file in base.rglob("*"):
                if file.is_file() and file.suffix in EXT_LANG:
                    files.append(file)

    return files


def replace_section(text, start, end, content):
    if start not in text or end not in text:
        return text

    return text.split(start)[0] + start + "\n" + content + "\n" + end + text.split(end)[1]


def make_stats(files):
    platform_count = Counter()

    for file in files:
        relative = file.relative_to(ROOT)
        platform_count[relative.parts[0]] += 1

    lines = [f"- 총 풀이 수: **{len(files)}문제**"]

    for platform in PLATFORMS:
        if platform_count[platform] > 0:
            lines.append(f"- {platform}: **{platform_count[platform]}문제**")

    return "\n".join(lines)


def make_language_table(files):
    lang_count = Counter()

    for file in files:
        lang_count[EXT_LANG[file.suffix]] += 1

    total = sum(lang_count.values())

    if total == 0:
        return "아직 풀이가 없습니다."

    lines = [
        "| Language | Count | Ratio |",
        "|---|---:|---:|",
    ]

    for lang, count in lang_count.most_common():
        ratio = round(count / total * 100)
        bar = "█" * max(1, ratio // 10)
        lines.append(f"| {lang} | {count} | {bar} {ratio}% |")

    return "\n".join(lines)


def make_recent(files):
    recent = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]

    if not recent:
        return "- 아직 풀이가 없습니다."

    return "\n".join(f"- `{file.relative_to(ROOT)}`" for file in recent)


def color_by_intensity(lang, count):
    colors = LANG_PALETTES.get(
        lang,
        ["#ECEFF1", "#B0BEC5", "#78909C", "#455A64"]
    )

    return colors[min(count, 4) - 1]


def make_grass(files):
    ASSETS.mkdir(exist_ok=True)

    by_day = defaultdict(list)

    for file in files:
        day = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")
        lang = EXT_LANG[file.suffix]
        by_day[day].append((file, lang))

    days = sorted(by_day.keys())[-35:]

    cell_w = 64
    cell_h = 64
    cols = 7
    rows = max(1, (len(days) + cols - 1) // cols)

    width = cols * cell_w + 20
    height = rows * cell_h + 54

    # 하트의 뾰족한 끝이 (0, 0)에 있고, 둥근 부분이 위쪽에 있는 형태
    # 이 하트를 같은 중심점에서 0/90/180/270도 회전시켜 네잎클로버를 만듦
    heart_path = (
        "M 0,0 "
        "C -11,-11 -23,-17 -23,-30 "
        "C -23,-45 -5,-48 0,-36 "
        "C 5,-48 23,-45 23,-30 "
        "C 23,-17 11,-11 0,0 Z"
    )

    items = []

    for idx, day in enumerate(days):
        x = 10 + (idx % cols) * cell_w
        y = 36 + (idx // cols) * cell_h

        center_x = x + 32
        center_y = y + 32

        lang_count = Counter(lang for _, lang in by_day[day])

        if len(lang_count) == 1:
            only_lang = next(iter(lang_count))
            leaves = [only_lang] * 4
        else:
            leaves = []

            for lang, count in lang_count.most_common():
                leaves.extend([lang] * count)

            leaves = leaves[:4]

            while len(leaves) < 4:
                leaves.append(None)

        tooltip_lines = [day]

        for lang, count in lang_count.most_common():
            tooltip_lines.append(f"{lang}: {count}문제")

        tooltip = "&#10;".join(tooltip_lines)

        clover = [f'<g><title>{tooltip}</title>']

        # 줄기
        clover.append(
            f'<line x1="{center_x}" y1="{center_y + 8}" '
            f'x2="{center_x}" y2="{center_y + 24}" '
            f'style="stroke:#6D4C41;stroke-width:2;stroke-linecap:round;" />'
        )

        for leaf_lang, rotation in zip(leaves, [0, 90, 180, 270]):
            if leaf_lang is None:
                color = "#E0E0E0"
            else:
                color = color_by_intensity(leaf_lang, lang_count[leaf_lang])

            clover.append(
                f'<path d="{heart_path}" '
                f'transform="translate({center_x},{center_y}) rotate({rotation}) scale(0.55)" '
                f'style="fill:{color};stroke:#ffffff;stroke-width:1.2;" />'
            )

        clover.append("</g>")
        items.append("".join(clover))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    text {{ font-family: Arial, sans-serif; font-size: 12px; fill: #333; }}
  </style>
  <text x="10" y="20">Algorithm Clover</text>
  {''.join(items)}
</svg>
'''

    CLOVER.write_text(svg, encoding="utf-8")


files = solution_files()

readme = README.read_text(encoding="utf-8")
readme = replace_section(readme, "<!-- STATS:START -->", "<!-- STATS:END -->", make_stats(files))
readme = replace_section(readme, "<!-- LANG:START -->", "<!-- LANG:END -->", make_language_table(files))
readme = replace_section(readme, "<!-- RECENT:START -->", "<!-- RECENT:END -->", make_recent(files))
README.write_text(readme, encoding="utf-8")

make_grass(files)