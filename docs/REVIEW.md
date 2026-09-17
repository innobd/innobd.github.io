# 검토 및 수정 기록

2026-09-18. innobd-site-ready.zip를 기준으로 수정했습니다. Dropbox 원본은 변경하지 않았습니다.

수정: 프로젝트 경로 지원, Pages 주소 자동 적용, 박사후연구원 표시, 이미지 경로, 관리자 편집 안내, 본문 바로가기, 대비 개선, 대표 논문 연도 정렬, 저자 HTML 삽입 제거, 게시 전 콘텐츠 검사.
확인되지 않은 자동화 성공 설명을 제거하고 개발용 초안과 실제 운영 경로를 구분했습니다. CMS의 실계정 로그인·저장과 GitHub 실제 배포는 계정 연결 후 확인해야 합니다.
참고 사이트의 큰 제목·구분선·연구/소식 구성에서 착안하되, InnoBD의 청록·보라와 전달체 그림을 유지했습니다.

참조: https://sites.google.com/view/byun-lab , https://sites.google.com/view/byun-lab/contact , https://joonanlab.github.io/

원본 innobd-site.zip과 최종 수정본 사이에 변경된 기존 파일:
- .pages.yml
- astro.config.mjs
- package.json
- README.md
- .github\workflows\deploy.yml
- .github\workflows\sync.yml
- scripts\__pycache__\ingest.cpython-312.pyc
- scripts\__pycache__\lib.cpython-312.pyc
- scripts\__pycache__\notify_slack.cpython-312.pyc
- scripts\__pycache__\sync_dropbox.cpython-312.pyc
- scripts\__pycache__\sync_pubmed.cpython-312.pyc
- scripts\__pycache__\sync_slack.cpython-312.pyc
- src\components\Footer.astro
- src\components\NewsList.astro
- src\components\PubList.astro
- src\data\join.json
- src\data\lab.json
- src\data\members.json
- src\data\news.json
- src\i18n\ui.ts
- src\layouts\Base.astro
- src\styles\global.css
- src\components\pages\Home.astro
- src\components\pages\Publications.astro
- src\components\pages\Team.astro

검증: Node 24 / Astro 7.3.2 빌드 성공. 루트 주소와 /lab-website/ 주소 각각 16개 페이지 및 내부 참조 214개 검사 통과. 모바일 메뉴·한영 전환·관리자 안내·데스크톱 화면 확인. Pages CMS 6개 편집 메뉴와 배포 설정 YAML 구문 검사 통과. 실제 GitHub 배포 및 CMS 계정 연결 테스트는 미실시.
