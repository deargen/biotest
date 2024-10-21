# Python logging 모듈

`print()` 쓰지 마세요. 이제부터 `logger.info()`로 대체하세요.

Why?

- 어떤 모듈, 어떤 라인에서 발생한 메시지인지 손쉽게 추적이 됨
- 원하는 LEVEL (DEBUG, INFO, WARNING, ERROR, CRITICAL)을 선택해 출력 가능
- 원하는 모듈을 선택적으로 출력 가능
- 손쉬운 handler 추가
    - 콘솔에 출력
    - 파일로 출력
    - 외부 프로그램에 로그 넘기기

## 사용법
---

로깅 세팅은 프로그램 실행 시 제일 처음 한번만 합니다. 다른 모듈에서는 그냥 logger를 사용하기만 합니다.

### `src/` 안에 있는 import 되는 모듈인 경우

```python hl_lines="1 3 7"
import logging

logger = logging.getLogger(__name__)

def foo():
    # print("Do not use print statements")
    logger.info("Use logging instead!")
```

### `tools/` 안에 있는 실행파일인 경우

`tools/examples/color_logging_main.py` 파일을 template으로 사용.

```python title="tools/examples/color_logging_main.py" hl_lines="7 19"
import rich.traceback

rich.traceback.install(show_locals=True)

import logging

from ml_project.utils import setup_logging

logger = logging.getLogger(__name__)


def main():
    logger.info("This is an info message")
    raise Exception("This is an exception")


if __name__ == "__main__":
    try:
        setup_logging()
        main()
    except Exception:
        logger.exception("Exception occurred")
```

## setup_logging() 함수
---

본 template에서는 logging을 쉽게 설정할 수 있는 함수를 제공합니다.

### ::: ml_project.utils.setup_logging
    options:
        show_root_heading: true

## Tip
---

- VSCode snippet 플러그인을 이용하면 빠르게 타이핑할 수 있습니다. 설정 예시:
    - ld &rarr; `logger.debug`
    - li &rarr; `logger.info`
    - lw &rarr; `logger.warning`
    - le &rarr; `logger.error`
    - lee &rarr; `logger.exception`
    - lc &rarr; `logger.critical`
    - logger &rarr;
        ```python
        import logging
        logger = logging.getLogger(__name__)
        ```

    
