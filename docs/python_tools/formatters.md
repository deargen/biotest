# Formatter

- **formatter:** 코드 자체는 바꾸지 않고, 코드 모양을 바꾸어주는 툴.  
    - Why?: 협업 환경에서 룰을 정하지 않으면 conflict가 많이 생겨 resolve하기 힘들며 실질적은 변경사항 리뷰하기 힘듦.
- 포매터 적용으로 인해 코드 로직이 바뀔 확률은 굉장히 적으므로 그냥 IDE에서 format on save 적용시키면 됨.

## Python formatters

### [Black](https://github.com/psf/black): 파이썬 대표 formatter

- line length: 88
    - Why?: 코드가 너무 길면 한 화면에 코드 두개를 띄워 비교하든지, 디버깅을 하느라 UI가 많이 떠 있을 때 읽기 힘듦.
- string은 double quotation (")
- 함수 parameters는 한 줄에 하나씩
- Examples:

    **Before Black:**

    ```python
    def calculate(a_large_number, another_large_number, yet_another_large_number, final_large_number):
        sum_of_first_two=a_large_number+another_large_number
        sum_of_last_two= yet_another_large_number+ final_large_number
        overall_sum =sum_of_first_two +sum_of_last_two
        return overall_sum
    ```

    **After Black:**

    ```python
    def calculate(
        a_large_number,
        another_large_number,
        yet_another_large_number,
        final_large_number,
    ):
        sum_of_first_two = a_large_number + another_large_number
        sum_of_last_two = yet_another_large_number + final_large_number
        overall_sum = sum_of_first_two + sum_of_last_two
        return overall_sum
    ```

### [isort](https://github.com/PyCQA/isort): import 구문 정렬

- 파이썬 내장, third party (pip install 된 모듈), first party (우리 프로젝트) 순서
- 알파벳 순서
- 같은 모듈에서 import 하는 elements 전부 합쳐줌
- Examples:

    **Before isort:**

    ```python
    from my_lib import Object
    import os
    from my_other_lib import run
    import sys
    import ml_project
    from third_lib import Widget
    ```

    **After isort:**

    ```python
    import os
    import sys

    from my_lib import Object
    from my_other_lib import run
    from third_lib import Widget

    import ml_project
    ```

### [ruff](https://github.com/astral-sh/ruff): Rust로 구현한 매우 빠른 black, isort (+ flake8 linter까지)

- Black, isort와 99% 호환성
- 추가로 모든 파일에 required import 추가하는 기능이 있음

```toml
# pyproject.toml
[tool.ruff.lint.isort]
# Python < 3.10에서 typing 호환성 유지
required-imports = [
  "from __future__ import annotations",
]
```

## VSCode settings

1. CLI commands 설치:  
```bash
conda deactivate
pip3 install --user ruff
```

2. vscode extension에서 **[Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)** 설치
3. VSCode settings.json 수정

```json
// settings.json
// { .. } 안에 넣기

"[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true, // 저장할 때마다 formatting
    "editor.codeActionsOnSave": {
        "source.organizeImports": true // 저장할 때마다 import sorting
    },
},
"ruff.organizeImports": true,
```

## NeoVim settings

1. CLI commands 설치:  
    ```bash
    conda deactivate
    pip3 install --user ruff
    ```
2. [lazy.nvim](https://github.com/folke/lazy.nvim) 플러그인 매니저 설정 (설치)
    - `init.lua` 파일에 설치 스크립트 복사하면 됨

3. lazy.nvim에 [conform.nvim](https://github.com/stevearc/conform.nvim) 플러그인 추가 및 ruff 설정.

    ```lua
      {
        "stevearc/conform.nvim",
        event = { "BufWritePre" },
        cmd = { "ConformInfo" },
        keys = {
          {
            -- Customize or remove this keymap to your liking
            "<space>pf",
            function()
              require("conform").format { async = true, lsp_fallback = true }
            end,
            mode = "",
            desc = "Format buffer",
          },
        },
        -- Everything in opts will be passed to setup()
        opts = {
          -- Define your formatters
          formatters_by_ft = {
            python = { "ruff_fix", "ruff_format" },
          },
          -- Set up format-on-save
          format_on_save = { timeout_ms = 2000, lsp_fallback = true },
          -- Customize formatters
          formatters = {
            ruff_fix = {
              -- I: isort
              -- D20, D21: docstring
              -- UP00: upgrade to python 3.10
              -- UP032: f-string over str.format
              -- UP034: extraneous parentheses
              -- ruff:[RUF100]: unused noqa

              -- IGNORED:
              -- ruff:[D212]: multi-line docstring summary should start at the first line (in favor of D213, second line)
              prepend_args = {
                "check",
                "--select",
                "I,D20,D21,UP00,UP032,UP034",
                "--ignore",
                "D212",
              },
            },
          },
        },
        init = function()
          -- If you want the formatexpr, here is the place to set it
          vim.o.formatexpr = "v:lua.require'conform'.formatexpr()"
        end,
      },
    ```

## CLI로 포매팅 하기

```bash
ruff --select I --fix [파일.py]  # isort 적용
ruff format [파일.py]  # black 적용
```

!!! info
    isort는 엄밀히 말하면 프로그램 실행 순서를 변경하기 때문에 formatter가 아님.  
    따라서 ruff에서는 isort linting (I) 코드가 있고 그에 대한 fix가 존재함.
