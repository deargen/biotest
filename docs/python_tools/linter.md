# Linter

- **Linter**: 코드 스타일 등 프로젝트에서 정한 룰을 지켰는지 체크하며 간단한 potential bug도 잡아줍니다.
- Formatter와 차이점: 코드 자체 로직이나 함수 등 수정을 권유합니다. 맹신하지 말고 가이드라 생각하고 쓰세요.
- LSP와 차이점:
    1. 속도: LSP는 프로젝트 전체를 분석해 함수 definition 위치 등도 파악하지만 linter는 한 파일만 체크합니다.
    2. Linter는 에러가 주로 스타일 관련이지만 LSP와 겹치는 에러도 있긴 합니다 (예: 사용되지 않은 variable, import 구문).

## Python linter

- flake8: PEP8 스타일 가이드를 지켜주는 파이썬 대표 linter. flake8-bugbear 같은 확장 플러그인도 많습니다.
- **ruff:** flake8 및 인기 플러그인을 전부 rust로 구현한 python linter 및 formatter. 저희 프로젝트에서는 ruff를 사용합니다.
    - 설치가 쉬움: 플러그인 설치가 많은 flake8과 달리 `pip install ruff`로 모든 linter, formatter 기능 사용 가능
    - 빠른 속도: rust로 구현해 속도가 10~100배 빠릅니다.

### Linting 비활성화

Linting 결과를 무시하고 싶은 경우:

1. Line 비활성화: 라인 끝에 `# noqa: D401` 과 같은 주석을 남겨주면 해당 코드(D401)가 비활성화됩니다.
    - `# noqa` 까지만 적으면 모든 에러 코드를 비활성화합니다.
2. File 비활성화: 수정하는 파일 맨 위에 `# flake8: noqa: D401 D402`와 같은 주석을 남기면 파일 전체에서 비활성화합니다.
3. Project 단위 비활성화: `pyproject.toml`에서 `[tools.ruff.lint]` 항목에 `ignore`를 추가합니다.

`pyproject.toml` 예시 (가장 최신 세팅은 pyproject.toml을 직접 참고하세요):

```toml
[tool.ruff]
extend-exclude = [
  "src/ml_project/_version.py",  # CHANGE
]

[tool.ruff.lint]
# OPTIONALLY ADD MORE LATER
select = [
  # flake8
  "E",
  "F",
  "W",
  "B",    # Bugbear
  "D",    # Docstring
  "D213", # Multi-line docstring summary should start at the second line (replace D212)
  "N",    # Naming
  "C4",   # flake8-comprehensions
  "UP",   # pyupgrade
  "SIM",  # simplify
  "RUF",  # ruff-specific
  "RET",  # return
  "PTH",  # path
  "NPY",  # numpy
  "PYI",  # type stubs for pyright/pylance
  "PT",   # pytest

  # Not important
  "T10",  # debug statements
  "T20",  # print statements
]

ignore = [
  "E402",    # Module level import not at top of file
  "D10",     # Missing docstring in public module
  "D200",    # One-line docstring should fit on one line with quotes
  "D212",    # Multi-line docstring summary should start at the first line
  "D417",    # require documentation for every function parameter.
  "D401",    # require an imperative mood for all docstrings.
  "PTH123",  # Path.open should be used instead of built-in open
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.pycodestyle]
# Black or ruff will enforce line length to be 88, except for docstrings and comments.
# We set it to 120 so we have more space for docstrings and comments.
max-line-length = 120

[tool.ruff.lint.isort]
known-third-party = ["wandb"]
```

## VSCode settings

1. CLI commands 설치:  
```bash
conda deactivate
pip3 install --user ruff
```

2. vscode extension에서 **[Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)** 설치
3. Diagnostics, ruff fix 등을 사용 가능. Formatting 설정은 [Formatters](formatters.md) 참고.

## CLI 사용법

```bash
ruff [file]  # lint error 체크
ruff --fix [file]  # fix 적용
ruff --select E --diff [file]  # E 코드 관련 에러를 fix할때 어떻게 될지 diff 출력
```
