<p align="center">
  <img src="https://github.com/lucid-luna/.github/blob/main/profile/assets/Feather.png" width="160" alt="LUNA Plugins Icon"/>
</p>

<h1 align="center">Luna Plugins</h1>
<p align="center">
  <b>자연어 기반 유틸리티 실행을 위한 확장 가능한 플러그인 시스템</b><br/>
  <i>Modular. Controllable. LLM-Driven.</i>
</p>

---

## 🧠 개요

`luna-plugins`는 [L.U.N.A. 프로젝트](https://github.com/lucid-luna)의  
**자연어 기반 도구 실행 기능**을 담당합니다.

> "날씨 알려줘", "계산 좀 해줘", "음악 틀어줘"  
> → LLM이 명령 인식 → 플러그인 실행 → 결과 반환

---

## 🧩 주요 기능

- 🧠 **LLM 연동 도구 호출** (예: `search`, `calculate`, `spotify.play`)
- ⚙️ **FastAPI 기반 REST 엔드포인트 제공**
- 🧱 **모듈형 플러그인 구조 (`tools/` 단위 구성)**
- 🔌 **로컬 또는 HTTP 방식 호출 모두 지원**
- 📚 **프롬프트 기반 자동 도구 사용 예시 제공**

---

## 📦 디렉토리 구조

<pre>
luna-plugins/
├── tools/
│ ├── search/ # 구글/네이버 등 검색 API
│ ├── calculator/ # 수식 계산기
│ ├── spotify/ # 음악 재생 플러그인
│ └── ...
├── server.py # 플러그인 FastAPI 서버
├── plugin_loader.py # 플러그인 로딩 시스템
├── prompt_examples/ # 프롬프트 예시 모음
├── README.md
└── requirements.txt
</pre>

---

## 📌 TODO

- [] Spotify / YouTube / Notion 등 다양한 플러그인 확장
- [] Web 기반 통합 관리 UI 개발
- [] LLM Agent 인터페이스와 연결 (ToolFormer 방식)
- [] 사용자 프롬프트 학습 기반 자동 연결 강화

---

## 🪪 라이선스

Apache License 2.0 © lucid-luna

---

## 🔗 관련 리포지토리

- [luna-core](https://github.com/lucid-luna/luna-core)
- [luna-models](https://github.com/lucid-luna/luna-models)
- [luna-client](https://github.com/lucid-luna/luna-client)
