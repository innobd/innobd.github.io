export const locales = ['en', 'ko'] as const;
export type Lang = (typeof locales)[number];
export const defaultLang: Lang = 'ko';

export const ui = {
  en: {
    'nav.home': 'Home',
    'nav.research': 'Research',
    'nav.pi': 'PI',
    'nav.team': 'People',
    'nav.publications': 'Publications',
    'nav.news': 'News',
    'nav.join': 'Join',
    'nav.contact': 'Contact',
    'lang.switch': '한국어',
    'lang.switchAria': 'Switch to Korean',
    'home.researchTitle': 'What we work on',
    'home.researchLead': 'One goal: make advanced biotherapeutics reach the right cells.',
    'home.newsTitle': 'Recent news',
    'home.pubsTitle': 'Selected publications',
    'home.joinTitle': 'Join the lab',
    'home.seeAll': 'See all',
    'home.explore': 'Explore research',
    'home.openings': 'Open positions',
    'research.title': 'Research',
    'research.lead': 'Delivery platforms and the methods we use to judge them.',
    'research.track.platform': 'Delivery platforms',
    'research.track.method': 'Evaluation methods',
    'pi.title': 'PI',
    'team.title': 'People',
    'team.pi': 'Principal investigator',
    'team.postdoc': 'Postdoctoral researchers',
    'team.phd': 'Ph.D. students',
    'team.ms': 'M.S. students',
    'team.undergrad': 'Undergraduate researchers',
    'team.alumni': 'Alumni',
    'pubs.title': 'Publications',
    'pubs.lead': 'Peer-reviewed articles from the lab and from collaborations.',
    'pubs.empty': 'Our publication list is being prepared. View the existing list below.',
    'pubs.doi': 'DOI',
    'pubs.pdf': 'PDF',
    'pubs.article': 'Article',
    'pubs.openAccess': 'Open Access',
    'news.title': 'News',
    'news.type.grant': 'Grant',
    'news.type.honor': 'Honor',
    'news.type.talk': 'Talk',
    'news.type.paper': 'Paper',
    'news.type.news': 'News',
    'join.title': 'Join',
    'join.howTitle': 'How to apply',
    'contact.title': 'Contact',
    'contact.email': 'Email',
    'contact.phone': 'Phone',
    'contact.address': 'Address',
    'footer.rights': 'All rights reserved.',
  },
  ko: {
    'nav.home': '홈',
    'nav.research': '연구',
    'nav.pi': 'PI',
    'nav.team': '멤버',
    'nav.publications': '논문',
    'nav.news': '지난 소식',
    'nav.join': '모집',
    'nav.contact': '연락처',
    'lang.switch': 'English',
    'lang.switchAria': '영어로 전환',
    'home.researchTitle': '연구 주제',
    'home.researchLead': '하나의 목표. 첨단 바이오의약품이 정확한 세포에 도달하게 하는 것.',
    'home.newsTitle': '최근 소식',
    'home.pubsTitle': '주요 논문',
    'home.joinTitle': '함께 연구하기',
    'home.seeAll': '전체 보기',
    'home.explore': '연구 살펴보기',
    'home.openings': '모집 안내',
    'research.title': '연구',
    'research.lead': '전달 플랫폼, 그리고 그것을 평가하는 방법.',
    'research.track.platform': '전달 플랫폼',
    'research.track.method': '평가 기술',
    'pi.title': 'PI',
    'team.title': '멤버',
    'team.pi': '연구책임자',
    'team.postdoc': '박사후연구원',
    'team.phd': '박사과정',
    'team.ms': '석사과정',
    'team.undergrad': '학부연구생',
    'team.alumni': '졸업생',
    'pubs.title': '논문',
    'pubs.lead': '연구실과 공동연구에서 발표한 학술 논문입니다.',
    'pubs.empty': '논문 목록을 정리하고 있습니다. 아래에서 기존 논문 목록을 확인하실 수 있습니다.',
    'pubs.doi': 'DOI',
    'pubs.pdf': 'PDF',
    'pubs.article': '논문',
    'pubs.openAccess': '오픈 액세스',
    'news.title': '지난 소식',
    'news.type.grant': '과제',
    'news.type.honor': '수상',
    'news.type.talk': '발표',
    'news.type.paper': '논문',
    'news.type.news': '소식',
    'join.title': '모집',
    'join.howTitle': '지원 방법',
    'contact.title': '연락처',
    'contact.email': '이메일',
    'contact.phone': '전화',
    'contact.address': '주소',
    'footer.rights': 'All rights reserved.',
  },
} as const;

export type UIKey = keyof (typeof ui)['en'];

export function t(lang: Lang) {
  return (key: UIKey): string => ui[lang][key] ?? ui[defaultLang][key];
}

/** 이중언어 필드 {en, ko} 에서 현재 언어 값을 꺼냅니다. 비어 있으면 영어로 대체. */
export function pick(lang: Lang, field: { en?: string; ko?: string } | string | undefined): string {
  if (!field) return '';
  if (typeof field === 'string') return field;
  return field[lang] || field.en || field.ko || '';
}

/** Resolve links and uploaded images for both user and project sites. */
const base = import.meta.env.BASE_URL.replace(/\/$/, '');
export function asset(path: string): string {
  if (/^(https?:|mailto:|tel:|#)/i.test(path)) return path;
  return `${base}/${path.replace(/^\//, '')}`;
}
export function href(lang: Lang, path: string): string {
  const [route, hash] = path.split('#');
  const clean = route.replace(/^\/+|\/+$/g, '');
  return asset(`${lang === 'en' ? 'en/' : ''}${clean ? clean + '/' : ''}`) + (hash ? `#${hash}` : '');
}
export function switchPath(lang: Lang, pathname: string): string {
  const local = base && (pathname === base || pathname.startsWith(base + '/')) ? pathname.slice(base.length) : pathname;
  return href(lang === 'ko' ? 'en' : 'ko', local.replace(/^\/en(?=\/|$)/, '') || '/');
}

export function formatDate(lang: Lang, iso: string): string {
  const d = new Date(iso + 'T00:00:00');
  if (lang === 'ko') return `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일`;
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
}
