import hashlib
from io import IOBase
from os import PathLike
from pathlib import Path
from typing import Any, Literal, overload

import numpy as np


@overload
def _read_file_or_io(
    file: str | PathLike | IOBase, *, decode: Literal[True] = True
) -> list[str]: ...


@overload
def _read_file_or_io(
    file: str | PathLike | IOBase, *, decode: Literal[False]
) -> bytes | Any: ...


def _read_file_or_io(file: str | PathLike | IOBase, *, decode=True):
    if decode:
        if isinstance(file, IOBase):
            file.seek(0)
            return [line.decode("utf-8") for line in file.readlines()]
        else:
            with open(file) as f:
                return f.readlines()
    # decode=False
    elif isinstance(file, IOBase):
        file.seek(0)
        return file.read()
    else:
        with open(file, "rb") as f:
            return f.read()


def assert_two_files_equal_sha(
    file1: str | PathLike | IOBase, file2: str | PathLike | IOBase
):
    """
    Assert that two files are exactly the same.
    """
    sha1 = hashlib.sha1()
    sha2 = hashlib.sha1()
    sha1.update(_read_file_or_io(file1, decode=False))
    sha2.update(_read_file_or_io(file2, decode=False))

    assert (
        sha1.hexdigest() == sha2.hexdigest()
    ), f"{file1} and {file2} have different SHA1 hashes."


def assert_two_npys_within_tolerance(
    npy1: str | PathLike | np.ndarray,
    npy2: str | PathLike | np.ndarray,
    *,
    tolerance=1e-6,
):
    """
    Assert that two npy files are almost the same within a tolerance.
    """
    if isinstance(npy1, str | PathLike):
        nparray1: np.ndarray = np.load(npy1)
    else:
        nparray1 = npy1
    if isinstance(npy2, str | PathLike):
        nparray2: np.ndarray = np.load(npy2)
    else:
        nparray2 = npy2

    assert np.allclose(nparray1, nparray2, atol=tolerance, rtol=tolerance), (
        f"{npy1} and {npy2} have different data."
        f" {nparray1} and {nparray2} are not close."
    )


def assert_two_pdbqt_files_within_tolerance(
    file1: str | PathLike | IOBase, file2: str | PathLike | IOBase, *, tolerance=1e-3
):
    """
    Assert that two pdbqt files are equal under following conditions.

    - ignore the trailing whitespace.
    - 0.001 default tolerance for Orthogonal coordinates for X,Y,Z in Angstroms.
    """
    lines1 = _read_file_or_io(file1)
    lines2 = _read_file_or_io(file2)

    assert len(lines1) == len(lines2), f"{file1} and {file2} have different lengths."

    for line1, line2 in zip(lines1, lines2, strict=True):
        if line1.rstrip() != line2.rstrip():
            if line1.startswith("ATOM") and line2.startswith("ATOM"):
                # Check for Orthogonal coordinates for X,Y,Z in Angstroms
                # https://userguide.mdanalysis.org/stable/formats/reference/pdbqt.html
                coord_1 = (
                    float(line1[30:38]),
                    float(line1[38:46]),
                    float(line1[46:54]),
                )
                coord_2 = (
                    float(line2[30:38]),
                    float(line2[38:46]),
                    float(line2[46:54]),
                )

                for c1, c2 in zip(coord_1, coord_2, strict=True):
                    assert np.isclose(c1, c2, atol=tolerance), (
                        f"{file1} and {file2} have different lines."
                        f" {line1.rstrip()} and {line2.rstrip()} are not equal."
                    )

                line1_except_coord = line1[:30] + line1[54:]
                line2_except_coord = line2[:30] + line2[54:]
                assert line1_except_coord.rstrip() == line2_except_coord.rstrip(), (
                    f"{file1} and {file2} have different lines."
                    f" {line1.rstrip()} and {line2.rstrip()} are not equal."
                )
            else:
                raise AssertionError(
                    f"{file1} and {file2} have different lines."
                    f" {line1.rstrip()} and {line2.rstrip()} are not equal."
                )


def assert_two_pdb_files_within_tolerance(
    file1: str | PathLike | IOBase, file2: str | PathLike | IOBase, *, tolerance=1e-3
):
    """
    Assert that two pdb files are equal under following conditions.

    - ignore the trailing whitespace.
    - 0.001 default tolerance for Orthogonal coordinates for X,Y,Z in Angstroms.

    Note:
        - Currently, the implementation is completely equal to assert_two_pdbqt_files_within_tolerance.
        - It may change and diverge in the future, thus there are two separate functions.
    """
    # ATOM    998  N   PHE B   9      18.937-159.292 -13.075  1.00 30.49           N
    assert_two_pdbqt_files_within_tolerance(file1, file2, tolerance=tolerance)


def assert_two_dirs_within_tolerance(
    dir1: str | PathLike,
    dir2: str | PathLike,
    *,
    tolerance: float = 1e-3,
    filenames_exclude: set[str] | None = None,
):
    """
    Assert that two directories have the same files with almost the same content within tolerance.
    """
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    assert dir1.is_dir()
    assert dir2.is_dir()

    if filenames_exclude is None:
        assert {path.name for path in dir1.iterdir()} == {
            path.name for path in dir2.iterdir()
        }
    else:
        assert {
            path.name for path in dir1.iterdir() if path.name not in filenames_exclude
        } == {
            path.name for path in dir2.iterdir() if path.name not in filenames_exclude
        }

    for file1 in dir1.iterdir():
        if filenames_exclude and file1.name in filenames_exclude:
            continue

        file2 = dir2 / file1.name

        if file1.suffix == ".npy":
            assert_two_npys_within_tolerance(file1, file2, tolerance=tolerance)
        elif file1.suffix == ".pdbqt":
            assert_two_pdbqt_files_within_tolerance(file1, file2, tolerance=tolerance)
        elif file1.suffix == ".pdb":
            assert_two_pdb_files_within_tolerance(file1, file2, tolerance=tolerance)
        elif file1.is_dir():
            assert_two_dirs_within_tolerance(
                file1, file2, tolerance=tolerance, filenames_exclude=filenames_exclude
            )
        else:
            assert_two_files_equal_sha(file1, file2)
