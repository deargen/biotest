# biotest

|  |  |
|--|--|
|[![Ruff](https://img.shields.io/badge/Ruff-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/ruff) |[![Actions status](https://github.com/deargen/biotest/workflows/Style%20checking/badge.svg)](https://github.com/deargen/biotest/actions)|
| [![Ruff](https://img.shields.io/badge/Ruff-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/ruff) | [![Actions status](https://github.com/deargen/biotest/workflows/Linting/badge.svg)](https://github.com/deargen/biotest/actions) |
| [![pytest](https://img.shields.io/badge/pytest-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/pytest-dev/pytest) [![doctest](https://img.shields.io/badge/doctest-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/library/doctest.html) | [![Actions status](https://github.com/deargen/biotest/workflows/Tests/badge.svg)](https://github.com/deargen/biotest/actions) |
| [![uv](https://img.shields.io/badge/uv-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/uv) | [![Actions status](https://github.com/deargen/biotest/workflows/Check%20pip%20compile%20sync/badge.svg)](https://github.com/deargen/biotest/actions) |
|[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)|[![Actions status](https://github.com/deargen/biotest/workflows/Deploy%20MkDocs%20on%20latest%20commit/badge.svg)](https://github.com/deargen/biotest/actions)|

A Python package for testing bioinformatics data. Mainly, it provides a set of functions to compare normal text/binary files, npy files, pdb files, and directories.

## 🛠️ Installation

```bash
pip install biotest
```

## 🚀 Usage

Mainly, use the API with pytest.

```python
from biotest.compare_files import (
    assert_two_files_equal_sha,
    assert_two_npys_within_tolerance,
    assert_two_pdbqt_files_within_tolerance,
    assert_two_pdb_files_within_tolerance,
    assert_two_dirs_within_tolerance,
)

def assert_two_files_sha(file1: str | PathLike | IOBase, file2: str | PathLike | IOBase):
    """
    Assert that two files are exactly the same.
    """
    ...

def assert_two_npys_within_tolerance(
    npy1: str | PathLike | np.ndarray, npy2: str | PathLike | np.ndarray, *, tolerance=1e-6
):
    """
    Assert that two npy files are almost the same within a tolerance.
    """
    ...


def assert_two_pdbqt_files_within_tolerance(
    file1: str | PathLike | IOBase, file2: str | PathLike | IOBase, *, tolerance=1e-3
):
    """
    Assert that two pdbqt files are equal under following conditions.

    - ignore the trailing whitespace.
    - 0.001 default tolerance for Orthogonal coordinates for X,Y,Z in Angstroms.
    """
    ...


def assert_two_pdb_files_within_tolerance(
    file1: str | PathLike | IOBase, file2: str | PathLike | IOBase, *, tolerance=1e-3
):
    """
    Assert that two pdb files are equal under following conditions.

    - ignore the trailing whitespace.
    - 0.001 default tolerance for Orthogonal coordinates for X,Y,Z in Angstroms.
    """
    ...


def assert_two_dirs_within_tolerance(
    dir1: str | PathLike,
    dir2: str | PathLike,
    *,
    tolerance: float = 1e-3,
    filenames_exclude: Sequence[str] | None = None,
):
    """
    Assert that two directories have the same files with almost the same content within tolerance.
    """
    ...
```

Also, you can use the CLI to quickly test the functionality. These merely call the functions above, so they will print the traceback if the assertion fails.

```bash
biotest assert-two-files-equal-sha file1 file2
biotest assert-two-npys-within-tolerance file1.npy file2.npy
biotest assert-two-pdbqt-files-within-tolerance file1.pdbqt file2.pdbqt
biotest assert-two-pdb-files-within-tolerance file1.pdb file2.pdb
biotest assert-two-dirs-within-tolerance dir1 dir2
```
