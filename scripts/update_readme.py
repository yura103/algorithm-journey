from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "assets"
GRASS = ASSETS / "algorithm-grass.svg"

PLATFORMS = ["백준", "프로그래머스"]

EXT_LANG = {
    ".py": "Python",
    ".js": "JavaScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".sql": "SQL",
}

COLORS = {
    ("백준", "Python"): "#4A90E2",
    ("백준", "JavaScript"): "#F5A623",
    ("백준", "Java"): "#E67E22",
    ("백준", "C++"): "#00599C",
    ("프로그래머스", "Python"): "#2ECC71",
    ("프로그래머스", "JavaScript"): "#F1C40F",
    ("프로그래머스", "SQL"): "#9B59B6",
    ("프로그래머스", "Java"): "#E74C3C",
}

DEFAULT_COLOR = "#95A5A6"


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

    lines = [
        f"- 총 풀이 수: **{len(files)}문제**",
        f"- 백준: **{platform_count['백준']}문제**",
        f"- 프로그래머스: **{platform_count['프로그래머스']}문제**",
    ]

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


def make_grass(files):
    ASSETS.mkdir(exist_ok=True)

    sorted_files = sorted(files, key=lambda f: f.stat().st_mtime)
    cell = 14
    gap = 4
    cols = 20
    rows = 7

    width = cols * (cell + gap) + 20
    height = rows * (cell + gap) + 50

    items = []

    for idx, file in enumerate(sorted_files[-cols * rows:]):
        relative = file.relative_to(ROOT)
        platform = relative.parts[0]
        lang = EXT_LANG[file.suffix]

        x = 10 + (idx // rows) * (cell + gap)
        y = 35 + (idx % rows) * (cell + gap)

        color = COLORS.get((platform, lang), DEFAULT_COLOR)
        title = f"{relative} / {lang}"

        items.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color}">'
            f'<title>{title}</title></rect>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    text {{ font-family: Arial, sans-serif; font-size: 12px; fill: #333; }}
  </style>
  <text x="10" y="20">Algorithm Grass</text>
  {''.join(items)}
</svg>
'''

    GRASS.write_text(svg, encoding="utf-8")


files = solution_files()

readme = README.read_text(encoding="utf-8")
readme = replace_section(readme, "<!-- STATS:START -->", "<!-- STATS:END -->", make_stats(files))
readme = replace_section(readme, "<!-- LANG:START -->", "<!-- LANG:END -->", make_language_table(files))
readme = replace_section(readme, "<!-- RECENT:START -->", "<!-- RECENT:END -->", make_recent(files))
README.write_text(readme, encoding="utf-8")

make_grass(files)