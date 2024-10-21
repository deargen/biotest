# TODO highlights

- 주석에 있는 `# TODO: ` 등을 하이라이팅해주는 플러그인입니다.
- 다른 collaborator가 꼭 알아야 할 중요한 정보는 쉽게 알아 볼 수 있게 키워드를 통일시켜 하이라이팅해야 합니다.

## VSCode에서 설치

- vscode extension에서 [TODO Highlight v2](https://marketplace.visualstudio.com/items?itemName=jgclark.vscode-todo-highlight) 설치
- setting.json에 아래 내용 추가

```json
"todohighlight.isEnable": true,
"todohighlight.keywords": [
    "FIX:",
    "BUG:",
    "ISSUE:",
    "DEBUG:",
    "REVIEW:",
    "NOTE:",
    "INFO:",
    "TODO:",
    "CHECK:",
    "PERF:",
    "WARN:",
    "WARNING:",
    "TEST:",
],
```

## NeoVim settings

1. [lazy.nvim](https://github.com/folke/lazy.nvim) 플러그인 매니저 설정 (설치)
    - `init.lua` 파일에 설치 스크립트 복사하면 됨

2. lazy.nvim에 [todo-comments.nvim](https://github.com/folke/todo-comments.nvim) 플러그인 추가 및 ruff 설정.

    ```lua
      {
        "folke/todo-comments.nvim",
        cmd = { "TodoTrouble", "TodoTelescope" },
        event = { "BufReadPost", "BufNewFile" },
        dependencies = "nvim-lua/plenary.nvim",
      },
    ```
