# Versioneer로 동적 버전 관리

**Why?**

- 연구 코드는 수시로 바뀌므로 Experiment tracking 할 때 버전 정보 로깅이 필수.
- 수동으로 버전 정보를 적기에는 너무 자주 바뀜.
- Git hash를 버전 정보로 사용하기에는 읽기가 어렵고 과거/미래버전 비교가 안됨.

**Solution**

- [**Versioneer**](https://github.com/python-versioneer/python-versioneer): 버전 정보를 git tag에서 읽어와 python project versioning

```python hl_lines="3"
import ml_project

print(ml_project.__version__)
```

```title="out"
0.1.3+40.g1f4adfe.dirty
```

- 마지막 Version tag (0.1.3): git tag 중 v로 시작하는 것을 찾음
- +40: 그 버전 이후 40개의 커밋이 존재
- g1f4adfe: git hash가 `1f4adfe`임
- .dirty: 커밋되지 않은 변경사항이 있음.

## 설치

1. `src/ml_project/__init__.py`, `src/ml_project/_version.py` 가져다 쓰기
2. `pyproject.toml`에 versioneer 관련 섹션 가져다 쓰기

## 비슷한 툴

- `setuptools-scm`: 비슷하긴 하나 한번 pip로 설치할때 버전이 평생 버전이고, 다시 설치를 해야 버전 업데이트됨. versioneer는 동적으로 바뀜. 연구코드는 versioneer가 편할듯.
