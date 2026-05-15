from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
OUT = ROOT / "docs" / "scripts.md"

script_files = sorted(SCRIPTS_DIR.glob("*.sh"))

lines = []
lines.append("# 스크립트 내용\n")
lines.append("이 페이지는 `scripts/` 폴더에 있는 실행 스크립트 내용을 모아 보여줍니다.\n")
lines.append("수정 후에는 아래 명령으로 이 문서를 다시 생성할 수 있습니다.\n")
lines.append("```bash\npython3 generate_scripts_doc.py\n```\n")

for path in script_files:
    rel = path.relative_to(ROOT)
    lines.append(f"\n## `{rel}`\n")
    lines.append("```bash")
    lines.append(path.read_text(encoding="utf-8").rstrip())
    lines.append("```")
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"generated: {OUT}")
