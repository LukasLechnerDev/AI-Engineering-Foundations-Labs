from pathlib import Path


def save_html(html: str, path: Path) -> None:
    print("\nStep 6: Saving digest...")
    path.write_text(html, encoding="utf-8")
