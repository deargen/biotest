# LSP (Language Server Protocol)

- LSP: 프로젝트 전체를 체크해 IDE에서 go to definition, signature (함수 미리보기) 기능 등을 제공합니다.
    - 그 이외의 linter와 비슷한 기능도 일부 구현되기도 합니다. (언어마다 다름)
- IDE에 내장된 경우가 많습니다. (NeoVim, VSCode 내장 기능)

## Python LSP (Pylance, Pyright)

VSCode에서는 pylance, 다른 IDE에서는 오픈소스 버전인 pyright을 사용합니다.

- LSP 기능 이외 Static type checking 기능이 있습니다. C++ 처럼 type을 명확히 지켜줬는지 체크합니다.  
    - 모든 변수, 함수의 type을 적을 필요는 없고, 간단한 경우는 알아서 추측합니다.
    - Inlay hints 기능을 켜서 LSP에서 추측하는 타입이 뭔지 보면서, 잘못된 부분은 명시하면서 코딩해야 좋습니다.

## VSCode settings

VSCode에 type checking 및 inlay hint 적용하기.

- Pylance 플러그인 설치 확인. 기본으로 설치된 경우가 많음. 
- 너무 복잡해지면 안 좋으니 일단 functionReturnTypes, variableTypes 만 사용 (그 외 함수 argument의 type도 볼 수 있음)
- setting.json에 아래 내용 추가
    ```json
    // settings.json
    // { .. } 안에 넣기
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": true,
    "python.analysis.typeCheckingMode": "basic",
    ```

## Pylance 에러 예시

```python
def add_numbers(num1: int, num2: int) -> int:
    return num1 + num2

# Call the function with correct arguments
num = add_numbers(2, 3)

# Call the function with INCORRECT arguments
add1 = 'abc'
result = add_numbers(add1, num)     # 🚨 TYPE ERROR!

# pylance 에러를 무시하기 위해서는 강제로 type을 지정해주면 됩니다.
add1: int = 'abc'                # 🚨 이 라인에서 에러가 한번 나긴 함.
# 하지만, 다음 줄 부터는 add1을 int라 생각하고 pylance가 코드를 파싱함.
result = add_numbers(add1, num)  # ✅ NO TYPE ERROR!
print(result)    # 'abc5'
# result는 int라고 생각함. 이를 억지로 해결하려면 
```

위 처럼 억지로 type을 맞춰서 실행하면, 결국 result는 int라고 생각해 pylance가 프로젝트를 parsing합니다.  

**해결법:**

1. 억지로 해결:
    ```python
    add1 = 'abc'
    result: str = add_numbers(add1, num)
    # 그 다음부터 result는 str이라고 생각됨.
    ```
2. 함수 definition을 변경:
    ```python
    def add_numbers_or_string(var1: int | str, var2: int | str) -> int | str:
        if isinstance(var2, str):
            var1 = str(var1)
        return var1 + var2
    ```

## Type stub

외부 라이브러리의 typing이 문제가 있을 때, 우리가 직접 type stub을 만들어 custom할 수 있습니다.  
프로젝트 루트에서 `typings/패키지명/모듈.pyi`를 만들어 typing을 합니다.  
함수의 body는 `...` 이라고 적고, signature (definition)만 작성합니다.

### 문제 상황 1

EasyDict를 사용하니 key를 implicit하게 만들면 pyright 에러가 남.  
![image](https://github.com/kiyoon/jupynium.nvim/assets/12980409/e82c3964-4f02-42f9-84b1-ff857e3a4a15)

#### 해결

1. 다음과 같이 stub 파일 탬플릿을 작성

```bash
pyright --createstub easydict
```

2. `typings/easydict/__init__.pyi` 에서 class definition 안에 `__getattr__` 함수를 만들어 type hint를 Any로 작성

```python
from typing import Any

class EasyDict(dict):
    # 다른 함수는 생략됨

    # EasyDict({'a': 1}).a 할 때, __getattr__이 호출된다.
    # 타입을 모르기 때문에, Any로 처리한다.
    def __getattr__(self, name: str) -> Any: ...
```

### 문제 상황 2

BioPython 라이브러리의 typing이 너무 안좋아서 에러가 너무 많이 남. 라이브러리가 복잡해서 직접 수정은 힘든 상황.

#### 해결

1. `typings/Bio/__init__.pyi`를 다음과 같이 작성

```python
from typing import Incomplete

def __getattr__(name: str) -> Incomplete: ...
```

모든 Bio 모듈의 변수들은 Incomplete (동적) 타입으로 되어 타입 체크를 건너뜀.

!!! info
    Incomplete type은 Any type과 기능은 동일(alias)  
    하지만, Any는 타입을 전혀 모르는 경우에 사용하고 Incomplete는 타이핑을 하다가 말았을 때 사용함.

2. 일부 typing만 켜고 싶으면 추가도 가능

```python
from typing import Incomplete

def __getattr__(name: str) -> Incomplete: ...
def some_function() -> str: ...
```
