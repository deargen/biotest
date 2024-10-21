# 깃헙에서 즉시 formatting하기

Formatting에 관련한 내용은 [Python tools / Formatters](../python_tools/formatters.md) 참고.

VSCode에서 자동 formatting을 적용할 수 있지만, 혹시 적용되지 않은 경우 GitHub Actions 메뉴에서 즉석으로 적용해 커밋 가능.

Actions -> Apply ruff format, isort, and fixes -> Run workflow -> select, ignore code 작성 후 Run workflow

![image](https://github.com/kiyoon/jupynium.nvim/assets/12980409/973fc130-5aa0-4df7-89c7-343a962e5f94)

**Select**

- I: isort 관련 룰을 적용합니다.
- D20,D21: Docstrings 관련 룰을 적용합니다.
- UP00: 옛날 버전 python 구문을 최신 문법으로 고칩니다. 특히 typing 관련해 많이 변경됩니다.

**Ignore**

- D212: Docstring first line 시작하게 하는 코드이나 적용하지 **않습니다.** 대신 D213으로 대체해 두 번째 line에 시작하게 합니다.
