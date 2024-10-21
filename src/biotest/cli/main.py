# ruff: noqa: T201
from pathlib import Path

import typer

app = typer.Typer(
    no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]}
)


def version_callback(*, value: bool):
    if value:
        from .. import __version__

        print(__version__)
        raise typer.Exit


@app.callback()
def common(
    ctx: typer.Context,
    *,
    version: bool = typer.Option(
        None, "-v", "--version", callback=version_callback, help="Show version"
    ),
):
    pass


@app.command()
def assert_two_files_equal_sha(file1: Path, file2: Path):
    from ..compare_files import assert_two_files_equal_sha

    assert_two_files_equal_sha(file1, file2)


# biotest assert-two-npys-within-tolerance file1.npy file2.npy
# biotest assert-two-pdbqt-files-within-tolerance file1.pdbqt file2.pdbqt
# biotest assert-two-pdb-files-within-tolerance file1.pdb file2.pdb
# biotest assert-two-dirs-within-tolerance dir1 dir2
@app.command()
def assert_two_npys_within_tolerance(file1: Path, file2: Path, tolerance: float = 1e-6):
    from ..compare_files import assert_two_npys_within_tolerance

    assert_two_npys_within_tolerance(npy1=file1, npy2=file2, tolerance=tolerance)


@app.command()
def assert_two_pdbqt_files_within_tolerance(
    file1: Path, file2: Path, tolerance: float = 1e-3
):
    from ..compare_files import assert_two_pdbqt_files_within_tolerance

    assert_two_pdbqt_files_within_tolerance(
        file1=file1, file2=file2, tolerance=tolerance
    )


@app.command()
def assert_two_pdb_files_within_tolerance(
    file1: Path, file2: Path, tolerance: float = 1e-3
):
    from ..compare_files import assert_two_pdb_files_within_tolerance

    assert_two_pdb_files_within_tolerance(file1=file1, file2=file2, tolerance=tolerance)


@app.command()
def assert_two_dirs_within_tolerance(
    dir1: Path,
    dir2: Path,
    tolerance: float = 1e-3,
    filenames_exclude: list[str] | None = None,
):
    from ..compare_files import assert_two_dirs_within_tolerance

    assert_two_dirs_within_tolerance(
        dir1=dir1, dir2=dir2, tolerance=tolerance, filenames_exclude=filenames_exclude
    )


def main():
    app()


if __name__ == "__main__":
    main()
