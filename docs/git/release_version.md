# 새 버전 Release

어느 정도 stable한 버전이다 싶으면 Actions -> Deploy a new version -> Run workflow -> Version tag 작성 후 Run workflow

![image](https://github.com/kiyoon/jupynium.nvim/assets/12980409/c1520351-67a6-4920-9c29-50864eba80ea)

`.github/workflows/deploy.yml`에 있는 대로, `docs/CHANGELOG.md`, release에 배포, mkdocs 문서 버전 등 생성이 됨.
