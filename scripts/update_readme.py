from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

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


files = solution_files()

readme = README.read_text(encoding="utf-8")
readme = replace_section(readme, "<!-- STATS:START -->", "<!-- STATS:END -->", make_stats(files))
readme = replace_section(readme, "<!-- LANG:START -->", "<!-- LANG:END -->", make_language_table(files))
readme = replace_section(readme, "<!-- RECENT:START -->", "<!-- RECENT:END -->", make_recent(files))
README.write_text(readme, encoding="utf-8")