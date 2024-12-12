"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

IGNORE_MODULES_EXACT = {}
IGNORE_MODULES_STARTSWITH = {}

nav = mkdocs_gen_files.Nav()
mod_symbol = '<code class="doc-symbol doc-symbol-nav doc-symbol-module"></code>'

src = Path(__file__).parent.parent / "src"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    module_str = ".".join(parts)

    if module_str in IGNORE_MODULES_EXACT or any(
        module_str.startswith(prefix) for prefix in IGNORE_MODULES_STARTSWITH
    ):
        print(f"Skipping module: {module_str}")  # noqa: T201
        continue
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    nav_parts = [f"{mod_symbol} {part}" for part in parts]
    nav[tuple(nav_parts)] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, ".." / path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())