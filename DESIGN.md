---
name: 회의록 STT 요약
description: STT 회의 텍스트를 구조화된 결정사항·액션아이템으로 바꿔 보여주는 내부 도구
colors:
  primary: "#4f46e5"
  primary-hover: "#4338ca"
  primary-active: "#3730a3"
  primary-soft-bg: "#eeedfc"
  primary-soft-text: "#4338ca"
  bg: "#f6f6fb"
  surface: "#ffffff"
  border: "#e5e5ef"
  text: "#17172b"
  text-secondary: "#6b6b84"
  text-tertiary: "#9494ab"
  neutral-soft-bg: "#eeeef3"
  neutral-soft-text: "#5a5a70"
  danger: "#c81e1e"
  danger-soft-bg: "#fdeeee"
  danger-soft-text: "#9a1c1c"
typography:
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
  title:
    fontSize: "20px"
    fontWeight: 700
    letterSpacing: "-0.01em"
  label:
    fontSize: "13px"
    fontWeight: 600
rounded:
  sm: "6px"
  md: "10px"
  lg: "14px"
spacing:
  1: "4px"
  2: "8px"
  3: "12px"
  4: "16px"
  5: "24px"
  6: "32px"
  7: "48px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  badge:
    backgroundColor: "{colors.neutral-soft-bg}"
    textColor: "{colors.neutral-soft-text}"
    rounded: "999px"
    padding: "0 8px"
    height: "22px"
---

# Design System: 회의록 STT 요약

## Overview

**Creative North Star: "The Structured Notepad"**

이 앱은 STT로 받아쓴 회의 텍스트를 붙여넣으면, LLM이 결정사항·액션아이템으로 정리해 보여주는 2인 미니 프로젝트다. 사용자는 "일을 완료"하러 오는 것이지 브랜드를 경험하러 오는 게 아니다 (**Mode: Operate**) — 그래서 표현보다 스캔 용이성과 일관성이 우선이다.

색은 액센트 인디고 하나로 제한하고 나머지는 전부 중립 회색조로 눌러서, 정보(제목·날짜·결정사항·담당자·기한)가 색보다 먼저 눈에 들어오게 했다. 장식은 거의 없다 — 카드, 배지, 여백만으로 위계를 만든다. 라이트/다크 모두 처음부터 1급 시민으로 설계했다(시스템 설정을 따름).

**Key Characteristics:**
- 인디고 액센트 하나 + 중립 회색 스케일(디자인당 액센트 색 1개 원칙)
- 카드(`.panel`) 기반 콘텐츠 그룹핑, 장식적 테두리·그림자 없음
- 상태(회의록/회의록아님)는 항상 pill 배지로, 텍스트만으로 전달하지 않음
- 다크모드는 대체 테마가 아니라 처음부터 설계된 동등한 모드

## Colors

인디고 액센트 하나 + 중립 회색조. 상태(성공/위험)만 별도 색을 쓴다.

### Primary
- **Indigo** (`#4f46e5` / dark: `#818cf8`): 유일한 액센트. 주요 버튼, 활성 네비게이션, 배지, 포커스 링, 결정사항 불릿 마커에만 쓴다. 화면의 10% 이내로 유지한다.

### Neutral
- **Ink** (`#17172b` / dark: `#eeeef6`): 본문 텍스트.
- **Slate** (`#6b6b84` / dark: `#a4a4bc`): 보조 텍스트 — 라벨, 날짜, 빈 상태 문구, 테이블 헤더. 실사용 대비비를 만족하는 가장 옅은 텍스트 톤(4.5:1 이상).
- **Mist** (`#9494ab` / dark: `#7a7a95`): 텍스트 대비가 필요 없는 곳(호버 테두리)과 비활성 버튼 전용. **본문/라벨 텍스트에는 쓰지 않는다** — WCAG AA(4.5:1)를 만족하지 못한다.
- **Paper** (`#f6f6fb` / dark: `#131320`): 페이지 배경.
- **Card** (`#ffffff` / dark: `#1b1b2c`): 패널·카드 배경.
- **Hairline** (`#e5e5ef` / dark: `#2c2c40`): 테두리·구분선.

### Named Rules
**The One Accent Rule.** 인디고는 primary 액션과 "현재 상태"를 가리킬 때만 쓴다. 두 번째 강조색을 추가하고 싶으면 먼저 회색조 위계로 해결할 수 있는지 확인한다.

**The No-Tertiary-Text Rule.** `text-tertiary`(Mist)는 작은 본문 텍스트에 쓰지 않는다 — 대비 감사에서 실패해 `text-secondary`(Slate)로 전부 교체했다. 새 텍스트 요소는 기본적으로 `text-secondary`를 쓰고, `text-tertiary`는 비-텍스트 장식이나 비활성 상태 전용으로 남긴다.

## Typography

**Body Font:** 시스템 산세리프 스택 (`-apple-system, BlinkMacSystemFont, "Segoe UI", "Malgun Gothic", "Apple SD Gothic Neo", system-ui, sans-serif`) — 한/영 혼용 텍스트가 많은 내부 도구라 커스텀 폰트보다 각 OS의 기본 한글 폰트를 그대로 쓰는 쪽을 선택했다.

**Character:** 장식 없는 실용적 타이포. 크기 차이보다 굵기·색·자간으로 위계를 만든다.

### Hierarchy
- **Title** (700, 20px, -0.01em): 페이지 h1.
- **Headline** (700, 17px): 섹션 h2 (회의 제목 등).
- **Eyebrow-label** (700, 14px, uppercase, 0.04em, `text-secondary`): h3 — "결정사항", "액션아이템" 같은 그룹 라벨.
- **Body** (400, 15px, line-height 1.6): 본문 기본값.
- **Label** (600, 13px, `text-secondary`): 폼 라벨.
- **Meta** (400, 13px): 배지 옆 날짜, 목록 행 날짜.

## Layout

단일 컬럼, `max-width: 720px`, 가운데 정렬. 표 형태 데이터(액션아이템)가 있는 화면은 최소 폭(420px) 아래에서 `overflow-x: auto`로 가로 스크롤하고, 페이지 자체는 절대 가로 스크롤하지 않는다. 480px 이하에서 바깥 여백과 h1 크기만 한 단계 줄인다 — 레이아웃 구조 자체는 바꾸지 않는다(반응형 변화를 최소화해 유지보수 부담을 줄임).

간격은 4px 배수 스케일(`--space-1`=4px ~ `--space-7`=48px)을 따른다. 같은 그룹 안 요소는 타이트하게(`space-2`~`space-3`), 서로 다른 섹션은 넉넉하게(`space-5`~`space-6`) 띄운다.

## Elevation & Depth

거의 플랫. 그림자는 카드(`.panel`)에만, 아주 옅게(`--shadow-sm: 0 1px 2px rgba(text, 0.06)`) 쓴다 — 표면을 "들어 올리기" 위해서가 아니라 배경과 카드 경계를 부드럽게 구분하기 위해서다. `--shadow-md`는 정의되어 있지만 현재 어떤 컴포넌트도 소비하지 않는다(향후 모달/팝오버용으로 남겨둠).

### Named Rules
**The Flat-By-Default Rule.** 그림자는 상태 변화(hover 등)에 반응해서가 아니라, 카드가 배경 위에 얹혀 있다는 것을 알려주는 정적 신호로만 쓴다.

## Shapes

라운드 코너 3단계: `sm`(6px, 뱃지 내부 요소 없음), `md`(10px, 버튼·인풋·네비 링크·카드 내부 요소), `lg`(14px, `.panel` 카드). 배지는 완전한 알약형(`999px`). 테두리는 항상 1px, hairline 토큰 하나만 쓴다 — 강조용 두꺼운 테두리나 색 테두리는 쓰지 않는다.

## Components

### Buttons
- **Shape:** `radius-md`(10px), height 40px, 좌우 padding `space-4`(16px).
- **Primary:** 배경 `primary`, 텍스트 흰색. 이 앱에 있는 유일한 버튼 스타일 — secondary/ghost 변형은 아직 없다(필요해지면 이 섹션에 추가할 것).
- **Hover / Active / Disabled:** hover는 `primary-hover`로 배경 전환(120ms), active는 `primary-active` + `scale(0.98)`, disabled는 `neutral-soft-bg` 배경 + `text-tertiary` 텍스트(WCAG 1.4.3 대비 예외 적용 구간).

### Badges
- **Style:** 알약형(`999px`), 22px 높이, 12px bold 텍스트.
- **State:** `data-status` 속성으로 색 결정 — `"회의록"`은 `primary-soft-bg`/`primary-soft-text`, `"회의록아님"`은 `neutral-soft-bg`/`neutral-soft-text`. 매칭되지 않는 값은 기본(`neutral`) 스타일로 폴백한다.

### Cards / Containers
- **Corner Style:** `radius-lg`(14px).
- **Background:** `surface`.
- **Shadow Strategy:** Elevation 섹션의 `shadow-sm` 참고.
- **Border:** 1px `hairline`.
- **Internal Padding:** `space-5`(24px).

### Inputs / Fields
- **Style:** `radius-md`, 1px `hairline` 테두리, 배경은 `bg`(카드보다 한 단계 어둡게 — 입력 영역임을 표시).
- **Focus:** 테두리를 `primary`로 바꾸고 `primary-soft-bg` 색의 3px 링을 바깥에 추가(box-shadow) — 아웃라인을 지우는 대신 대체.
- **Hover:** 테두리만 `text-tertiary`로 살짝 진하게(포커스 전 힌트).

### Navigation
- **Style:** 텍스트 링크형, `radius-md`, 높이 36px. 기본은 `text-secondary`, hover는 `surface` 배경 + `text` 색, 현재 페이지(`aria-current="page"`)는 `primary-soft-bg`/`primary-soft-text`로 고정 강조.

## Do's and Don'ts

### Do:
- **Do** 새 텍스트 요소에는 기본적으로 `text-secondary`를 쓴다(`text-tertiary`는 4.5:1 대비를 만족하지 못함).
- **Do** 상태(성공/실패/분류)는 색 하나로 끝내지 않고 배지·아이콘 등 텍스트/형태로도 같이 전달한다(색맹 사용자 고려).
- **Do** 새 컬러 토큰을 추가하면 라이트·다크 블록 양쪽에 반드시 정의한다 — 한쪽만 정의된 토큰은 다른 테마에서 값이 새어 나간다.
- **Do** 표 형태 데이터는 `.table-scroll` 래퍼로 감싸 좁은 화면에서 페이지 자체가 아니라 표 내부만 가로 스크롤되게 한다.

### Don't:
- **Don't** 같은 데이터를 화면마다 다른 형태로 보여주지 않는다 — 결정사항/액션아이템은 항상 같은 렌더링 로직(`client/js/render.js`)을 거친다. 원시 JSON을 사용자에게 직접 보여주지 않는다.
- **Don't** 두 번째 액센트 컬러를 추가하지 않는다 — 인디고가 유일한 액센트라는 게 이 시스템의 핵심 규칙이다.
- **Don't** `box-shadow`에 하드 오프셋(`Npx Npx 0`)을 쓰지 않는다 — 이 시스템은 네오브루탈리즘 세계관이 아니다.
- **Don't** 카드·리스트 아이템·알림에 컬러 `border-left`/`border-right` 강조를 쓰지 않는다 — 위계는 배경색과 여백으로 만든다.
