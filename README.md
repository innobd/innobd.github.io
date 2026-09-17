# InnoBD Lab 홈페이지 — 처음 사용하는 분께

이 폴더는 GitHub에 올릴 홈페이지 원본입니다. ZIP 파일 자체가 아니라 **압축을 푼 폴더 안의 파일들**을 올립니다.

## 세 가지 이름만 기억하세요
- **GitHub**: 홈페이지 글·사진과 수정 이력을 보관하는 서랍입니다. 저장소(repository)는 그 안의 폴더입니다.
- **GitHub Pages**: 그 파일로 만든 홈페이지를 인터넷에 보여줍니다.
- **Pages CMS**: 글·사진을 입력하는 편집 화면입니다. 평소에는 여기만 사용하면 됩니다.

방문자는 홈페이지를 보고, 관리자는 홈페이지 아래의 **관리자 편집**을 눌러 로그인합니다.
Google Sites의 화면 배치 편집과 달리, 정해진 칸에 글과 사진을 넣는 방식입니다.

## 1. 처음 인터넷에 올리기
1. https://github.com 에 가입합니다. 사용자 이름을 메모해 두세요.
2. 오른쪽 위 + → New repository를 누릅니다.
3. 이름에 **내사용자이름.github.io**를 입력합니다. 예: 계정이 `byunlab`이면 `byunlab.github.io`. `innobdlab.github.io`는 계정 이름이 `innobdlab`일 때만 해당 주소가 됩니다.
4. 무료로 시작하려면 Public을 선택합니다. 이 저장소의 파일은 공개됩니다. 비밀번호·API 키·비공개 연구자료는 넣지 않습니다.
5. Add README를 켜고 Create repository를 누릅니다.
6. Add file → Upload files를 누릅니다. 이 폴더 **안에 있는 모든 파일과 폴더**를 끌어 넣습니다. innobd-site 폴더 자체를 한 겹 더 넣거나 ZIP만 올리면 안 됩니다.
7. 업로드 목록에서 `.github/workflows/deploy.yml`, `.pages.yml`, `package.json`, `pnpm-lock.yaml`, `src`, `public`이 포함되었는지 확인한 뒤 Commit changes를 누릅니다. 점(.)으로 시작하는 파일도 필요합니다.
8. Settings → Pages → Build and deployment → Source에서 **GitHub Actions**를 선택합니다.
9. Actions → Deploy to GitHub Pages → Run workflow를 누릅니다. 첫 업로드 때 실패한 기록이 있어도 설정 후 새로 실행하면 됩니다.
10. 초록색 완료 표시가 나오면 Settings → Pages → Visit site를 누릅니다. 첫 배포는 몇 분 걸릴 수 있습니다.

저장소 이름을 `lab-website` 등으로 정해도 됩니다. 이때 주소는 `https://내사용자이름.github.io/lab-website/`입니다. 수정본은 주소 경로를 자동 처리합니다.

## 2. 코딩 없이 글과 사진 수정하기
1. 홈페이지 맨 아래 관리자 편집 → 편집기 열기를 누릅니다.
2. https://app.pagescms.org 에서 GitHub 계정으로 로그인합니다.
3. GitHub App 설치 안내에서 이 홈페이지 저장소를 선택합니다.
4. 저장소와 `main`을 열면 소식·구성원·논문·연구 주제·연구실 기본정보·모집 안내가 보입니다.
5. 수정하고 Save를 누릅니다. 반영에는 최대 약 10분이 걸릴 수 있습니다. 현재 한국어·영어는 각각 입력합니다.

### 자주 하는 수정
| 하고 싶은 일 | 편집 메뉴 |
|---|---|
| 첫 화면 큰 문구 변경 | 연구실 기본정보 → 홈 화면 문구 |
| 교수·학생 사진 올리기 | 구성원 → 해당 사람 → 사진 |
| 수상·학회 소식 추가 | 소식 → 항목 추가 → 날짜·종류·내용 |
| 날짜를 정확히 모를 때 | 날짜에 해당 연도 1월 1일 입력, 날짜 표시 범위는 연도만 표시 |
| 새 논문 추가 | 논문 → 제목·저자·저널·연도 입력 |
| 첫 화면에 논문 표시 | 논문의 홈 화면 대표 논문으로 표시 켜기 |
| 모집 문구 변경 | 모집 안내 |

구성원·연구 주제의 고유 ID는 `junho-byun`처럼 영어 소문자와 하이픈으로 중복 없이 적습니다.
사진은 편집기에서 업로드하면 됩니다. 색상·전체 배치 변경은 제작 파일 수정이 필요합니다.

## 3. 공개 전에 내용 확인
- 영문 구성원 이름은 원본 초안에 추정 표기가 포함되어 있습니다. 본인에게 확인하세요.
- 연락처·주소는 기존 Google Sites Contact 페이지에 맞췄습니다. 현재 정보인지 확인하세요.
- 소식의 정확한 월일은 기존 사이트에서 확인되지 않아 연도만 보이게 했습니다. 초안의 날짜값 자체는 남아 있습니다.
- 현재 사진 파일은 제공되지 않았으므로 이름 이니셜을 표시합니다.
- 논문 데이터는 원본이 빈 목록이어서, 기존 Google Sites 논문 목록으로 연결했습니다. 편집기에서 검증된 논문을 추가하면 새 목록이 나타납니다.
- 원본의 모집·지원금·참여 조건은 현재 공고와 일치하는지 확인되지 않아 문의 안내로 정리했습니다.
- 교수 소개·2026년 편집위원 소식 등 원본 초안의 사실도 공개 전에 최종 확인하세요.

기존 Google Sites는 새 사이트의 글·사진·연락처 확인이 끝날 때까지 유지하세요. 이전 완료 후 기존 첫 화면에 새 주소를 안내하면 됩니다.

## 4. 저장했는데 바뀌지 않을 때
1. 편집기에서 main을 수정했는지 확인합니다.
2. GitHub Actions에서 가장 최근 Deploy to GitHub Pages가 초록색인지 확인합니다.
3. 빨간색이면 해당 실행을 열어 오류 화면을 복사해 도움을 요청하세요. 내용 검사 실패 시 기존 배포는 유지됩니다.
4. 초록색이면 몇 분 기다린 뒤 Ctrl+F5로 새로고침합니다.

## 5. 나중에 자동화하기
Dropbox·Slack·Claude·PubMed는 아직 연결하지 않았습니다. 원본의 자동화 코드는 초안으로 보관했고 정기 실행은 제외했습니다.
권장 순서는 **수동 편집 안정화 → 자동 초안 작성 → 담당자 확인 후 게시 → 알림**입니다.
자세한 연결 전 검토사항은 docs/AUTOMATION.md에 있습니다. API 사용료는 홈페이지 호스팅과 별도입니다.

## 개발자용
Node 24와 pnpm 11.19.0 사용. `pnpm install --frozen-lockfile`, `pnpm run build`, `pnpm dev`.
`pnpm run check`는 콘텐츠 검사입니다. `SITE_URL`, `SITE_BASE`로 별도 도메인/경로를 지정할 수 있습니다. GitHub 배포는 Pages 설정에서 값을 읽습니다.

## 공식 안내
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://pagescms.org/docs/configuration/content/
- https://pagescms.org/docs/configuration/fields/select/
