# API Reference 페이지

본 template에서는 다음과 같은 방식으로 API Reference 페이지를 생성합니다.  
추가 설정이 필요하지는 않습니다.
    
```yaml title="mkdocs.yml 예시" hl_lines="15-17"
nav:
- Home:
  - Overview: index.md
  - Changelog: changelog.md
- Usage:
  - usage/index.md
  - Theming: usage/theming.md
  - Handlers: usage/handlers.md
  - All handlers:
    - Crystal: https://mkdocstrings.github.io/crystal/
    - Shell: https://mkdocstrings.github.io/shell/
  - Guides:
    - Recipes: recipes.md
    - Troubleshooting: troubleshooting.md
# defer to gen-files + literate-nav
- API reference:
  - mkdocstrings: reference/
```
    
- API reference는 gen-files와 literate-nav 플러그인을 통해 생성.
    - **gen-files**: 빌드 전 파일 생성하는 스크립트 실행 가능
    - **literate-nav**: markdown 파일로 nav 메뉴 동적 설정 가능
    
    ```yaml
    # mkdocs.yml
    plugins:
    - gen-files:
        scripts:
        - scripts/gen_ref_nav.py
    - literate-nav:
        nav_file: SUMMARY.md
    ```
    
    `scripts/gen_ref_nav.py` 실행하면 `reference/` 디렉토리에 API reference 페이지들 자동 생성되며 SUMMARY.md 메뉴(nav) 파일을 만듦.
