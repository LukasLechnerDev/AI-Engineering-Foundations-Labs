from pathlib import Path


def save_html(html: str, path: Path) -> None:
    print("\nStep 9: Saving digest...")
    path.write_text(html, encoding="utf-8")
    print(f"  Saved to: {path.resolve()}")
