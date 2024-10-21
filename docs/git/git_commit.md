# Conventional Commits

커밋메시지는 [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)를 따르기

1. fix: `MyDataloader` doesn’t return an image
2. feat: `train_step()`
3. perf: optimise loop in `train_step()`
4. chore: change dependency version in github action
5. docs: readme add demo
6. ci: add black formatting check (깃헙 액션 관련된 것)
7. style: apply black formatter
8. refactor: `train` function to `train_init` and `train_end`
9. test: check return type of `analyze_data`
10. 그 외, breaking change는 fix!: 처럼 느낌표 붙이기
11. 그 외, 자세한 항목은 fix(network): 처럼 괄호안에 카테고리 적기
