from pathlib import Path


def print_tree(path: Path, indent: int = 0) -> str:
    tree = ""
    for child in path.iterdir():
        tree += f"{'    ' * indent}{child.name}\n"
        if child.is_dir():
            tree += print_tree(child, indent + 1)
    return tree
