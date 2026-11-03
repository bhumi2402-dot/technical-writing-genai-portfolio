
from pathlib import Path
import re

def check_document(file_path):
    content = file_path.read_text(encoding="utf-8")
    issues = []
    lines = content.splitlines()

    # Check main heading
    if not lines or not lines[0].startswith("# "):
        issues.append("Missing main heading")

    # Check common writing issues
    for number, line in enumerate(lines, start=1):
        if line.rstrip() != line:
            issues.append(f"Extra spaces at line {number}")

        if "TODO" in line:
            issues.append(f"Unfinished TODO at line {number}")

    # Check broken local links
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

    for label, link in links:
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue

        target = (file_path.parent / link.split("#")[0]).resolve()

        if not target.exists():
            issues.append(f"Broken link: {link}")

    return issues


def main():
    docs_folder = Path("docs")

    if not docs_folder.exists():
        print("Documentation folder not found.")
        return

    files = list(docs_folder.rglob("*.md"))

    if not files:
        print("No Markdown files found.")
        return

    for file in files:
        print(f"\nChecking: {file}")
        issues = check_document(file)

        if issues:
            for issue in issues:
                print("ERROR:", issue)
        else:
            print("No issues found.")


if __name__ == "__main__":
    main()
