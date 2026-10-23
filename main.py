
import hashlib
from pathlib import Path


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    try:
        with file_path.open("rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (OSError, PermissionError) as error:
        print(f"Cannot read {file_path}: {error}")
        return None


def find_duplicates(folder_path):
    """Find files having identical content."""
    folder = Path(folder_path).expanduser()

    if not folder.exists():
        print("Error: Folder does not exist.")
        return

    if not folder.is_dir():
        print("Error: The given path is not a folder.")
        return

    hash_map = {}
    total_files = 0

    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue

        total_files += 1
        file_hash = calculate_hash(file_path)

        if file_hash is None:
            continue

        hash_map.setdefault(file_hash, []).append(file_path)

    duplicate_groups = [
        paths for paths in hash_map.values()
        if len(paths) > 1
    ]

    print(f"\nFolder scanned: {folder}")
    print(f"Files checked: {total_files}")

    if not duplicate_groups:
        print("No duplicate files found.")
        return

    print(f"\nDuplicate groups found: {len(duplicate_groups)}")

    for number, paths in enumerate(duplicate_groups, start=1):
        print(f"\nGroup {number}:")

        for path in paths:
            print(f"  {path}")


if __name__ == "__main__":
    folder = input("Enter folder path to scan: ").strip()

    if folder:
        find_duplicates(folder)
    else:
        print("Please enter a valid folder path.")
