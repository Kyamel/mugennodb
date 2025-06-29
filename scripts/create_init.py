import os
import sys


def create_inits(path: str, allowed_roots: list[str]) -> None:
    allowed_roots = [os.path.normpath(os.path.join(path, ar)) for ar in allowed_roots]

    for current_root, dirs, files in os.walk(path):
        norm_root = os.path.normpath(current_root)

        if any(norm_root.startswith(ar) for ar in allowed_roots):
            if "__init__.py" not in files:
                path = os.path.join(current_root, "__init__.py")
                with open(path, "w", encoding="utf-8") as f:
                    pass
                print(f"Criado {path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Uso: python create_init.py <root_path> [allowed_folder1 allowed_folder2 ...]"
        )
        sys.exit(1)

    root_path = sys.argv[1]
    allowed = sys.argv[2:] if len(sys.argv) > 2 else ["mugennodb", "mugennocore"]

    create_inits(root_path, allowed)
