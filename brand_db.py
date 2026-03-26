#!/usr/bin/env python3
"""URSxClaw 브랜드 아이덴티티 DB — 나노바나나 스타일 생성기"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "brand_identity.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """브랜드 DB 스키마 생성 + 초기 데이터 삽입"""
    conn = get_conn()
    c = conn.cursor()

    # ── 테이블 생성 ──
    c.executescript("""
    CREATE TABLE IF NOT EXISTS brand_core (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        category TEXT DEFAULT 'general',
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS colors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        hex TEXT NOT NULL,
        rgb TEXT,
        usage TEXT,
        theme TEXT DEFAULT 'both',  -- light / dark / both
        role TEXT,  -- primary / secondary / accent / bg / text / etc.
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS typography (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        element TEXT NOT NULL,
        font_family TEXT NOT NULL,
        font_size TEXT,
        font_weight TEXT,
        line_height TEXT,
        letter_spacing TEXT,
        usage TEXT,
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS copy_blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        block_type TEXT NOT NULL,  -- tagline / intro / about / section / closing / cta
        title TEXT,
        body TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        lang TEXT DEFAULT 'ko',
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS voice_tone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attribute TEXT NOT NULL,
        description TEXT NOT NULL,
        do_example TEXT,
        dont_example TEXT,
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS design_tokens (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        category TEXT,  -- spacing / radius / shadow / animation / etc.
        description TEXT,
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS principles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        file_path TEXT,
        asset_type TEXT,  -- logo / icon / pattern / illustration
        format TEXT,
        description TEXT,
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        icon TEXT,
        headline TEXT,
        description TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        updated_at TEXT DEFAULT (datetime('now'))
    );
    """)

    # ── 초기 데이터: brand_core ──
    core_data = {
        # 기본 정보
        "brand_name": ("URSxClaw", "general"),
        "brand_name_kr": ("유알에스 클로", "general"),
        "tagline": ("반복은 맡기고, 당신은 살아가세요.", "general"),
        "tagline_en": ("Delegate the routine. Live your life.", "general"),
        "one_liner": ("URSxClaw는 투자부터 일상의 반복 업무까지, 사람이 하지 않아도 되는 일을 자동화하는 기술 브랜드입니다.", "general"),
        "domain": ("ursxclaw.com", "general"),
        "founder": ("나노바나나", "general"),
        "founded_year": ("2026", "general"),

        # 브랜드 키워드
        "keywords": ("자동화, 투자봇, 반복업무, 트레이딩, 대시보드, 기술브랜드", "identity"),
        "personality": ("담백한, 세련된, 신뢰감, 기술적, 미니멀", "identity"),
        "target_audience": ("시간이 부족한 투자자, 반복 업무에 지친 직장인, 기술 기반 자동화를 원하는 사람", "identity"),

        # 나노바나나 스타일 시그니처
        "style_signature": ("나노바나나", "identity"),
        "style_desc": ("비유 없이 팩트만. 자존감 건드리는 표현 금지. 있는 그대로 보여주되, 담백하고 세련된 톤.", "identity"),

        # 폐 카피 정책
        "copy_policy_no_metaphor": ("비유 사용 금지 — 직접적이고 명확한 표현만", "policy"),
        "copy_policy_no_condescend": ("'초등학생도 이해하는', '누구나 쉽게' 같은 자존감 건드리는 표현 금지", "policy"),
        "copy_policy_tone": ("담백하고 세련된 톤. 과장 금지. 실제 하는 일을 있는 그대로 설명.", "policy"),
    }

    for key, (value, category) in core_data.items():
        c.execute(
            "INSERT OR REPLACE INTO brand_core (key, value, category, updated_at) VALUES (?, ?, ?, datetime('now'))",
            (key, value, category),
        )

    # ── 초기 데이터: colors (나노바나나 + Apple 영감) ──
    colors_data = [
        # 라이트 모드
        ("Pure White", "#FFFFFF", "255,255,255", "주 배경 (라이트)", "light", "background"),
        ("Cloud Gray", "#F5F5F7", "245,245,247", "보조 배경, 카드 (라이트)", "light", "background-secondary"),
        ("Warm Gray", "#F2F2F7", "242,242,247", "섹션 배경 (라이트)", "light", "background-tertiary"),

        # 다크 모드
        ("Deep Black", "#000000", "0,0,0", "주 배경 (다크)", "dark", "background"),
        ("Charcoal", "#1C1C1E", "28,28,30", "카드/섹션 배경 (다크)", "dark", "background-secondary"),
        ("Dark Gray", "#2C2C2E", "44,44,46", "입력 필드, 보조 요소 (다크)", "dark", "background-tertiary"),

        # 브랜드 컬러
        ("URSx Blue", "#007AFF", "0,122,255", "주 강조색 — CTA, 링크, 주요 버튼", "both", "primary"),
        ("Neon Violet", "#5E5CE6", "94,92,230", "보조 강조색 — 다크모드 포인트, 그래프", "both", "secondary"),
        ("Nano Yellow", "#FFD60A", "255,214,10", "나노바나나 시그니처 — 하이라이트, 배지, 강조점", "both", "accent"),

        # 시맨틱
        ("Success Green", "#34C759", "52,199,89", "성공, 수익, 긍정 지표", "both", "semantic-success"),
        ("Alert Red", "#FF3B30", "255,59,48", "경고, 손실, 에러", "both", "semantic-danger"),
        ("Caution Orange", "#FF9500", "255,149,0", "주의, 보류, 경고 (중간)", "both", "semantic-warning"),
        ("Info Cyan", "#5AC8FA", "90,200,250", "정보, 안내, 중립 알림", "both", "semantic-info"),

        # 텍스트
        ("Ink Black", "#1D1D1F", "29,29,31", "본문 텍스트 (라이트)", "light", "text-primary"),
        ("Dim Gray", "#86868B", "134,134,139", "보조 텍스트, 캡션 (라이트)", "light", "text-secondary"),
        ("Snow White", "#F5F5F7", "245,245,247", "본문 텍스트 (다크)", "dark", "text-primary"),
        ("Ash Gray", "#98989D", "152,152,157", "보조 텍스트, 캡션 (다크)", "dark", "text-secondary"),

        # 보더/구분선
        ("Light Border", "#D1D1D6", "209,209,214", "구분선, 보더 (라이트)", "light", "border"),
        ("Dark Border", "#38383A", "56,56,58", "구분선, 보더 (다크)", "dark", "border"),
    ]

    for name, hex_, rgb, usage, theme, role in colors_data:
        c.execute(
            "INSERT OR IGNORE INTO colors (name, hex, rgb, usage, theme, role) VALUES (?, ?, ?, ?, ?, ?)",
            (name, hex_, rgb, usage, theme, role),
        )

    # ── 초기 데이터: typography ──
    typo_data = [
        ("Display (H1)", "-apple-system, 'SF Pro Display', 'Pretendard', sans-serif", "48px", "700", "1.2", "-0.5px", "히어로 섹션, 메인 타이틀"),
        ("Heading (H2)", "-apple-system, 'SF Pro Display', 'Pretendard', sans-serif", "34px", "600", "1.25", "-0.3px", "섹션 제목"),
        ("Subheading (H3)", "-apple-system, 'SF Pro Text', 'Pretendard', sans-serif", "24px", "600", "1.3", "-0.2px", "카드 제목, 소제목"),
        ("Body Large", "-apple-system, 'SF Pro Text', 'Pretendard', sans-serif", "17px", "400", "1.6", "0px", "본문 (강조)"),
        ("Body", "-apple-system, 'SF Pro Text', 'Pretendard', sans-serif", "15px", "400", "1.6", "0px", "기본 본문"),
        ("Caption", "-apple-system, 'SF Pro Text', 'Pretendard', sans-serif", "13px", "400", "1.4", "0px", "보조 텍스트, 타임스탬프"),
        ("Mono", "'SF Mono', 'JetBrains Mono', 'D2Coding', monospace", "14px", "400", "1.5", "0px", "코드, 데이터 수치"),
        ("Button", "-apple-system, 'SF Pro Text', 'Pretendard', sans-serif", "15px", "600", "1.0", "0.5px", "버튼 텍스트"),
        ("Tag/Badge", "-apple-system, 'SF Pro Text', 'Pretendard', sans-serif", "11px", "600", "1.0", "0.5px", "태그, 배지, 라벨"),
    ]

    for el, family, size, weight, lh, ls, usage in typo_data:
        c.execute(
            "INSERT OR IGNORE INTO typography (element, font_family, font_size, font_weight, line_height, letter_spacing, usage) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (el, family, size, weight, lh, ls, usage),
        )

    # ── 초기 데이터: copy_blocks ──
    copy_data = [
        ("tagline", None, "반복은 맡기고, 당신은 살아가세요.", 1),
        ("intro", "브랜드 한 줄 소개", "URSxClaw는 투자부터 일상의 반복 업무까지, 사람이 하지 않아도 되는 일을 자동화하는 기술 브랜드입니다.", 2),
        ("about", "About Us", '우리는 한 가지 질문에서 시작했습니다.\n"매일 같은 일을 반복하면서, 정작 중요한 일에 쓸 시간은 왜 늘 부족할까?"\n차트를 들여다보고, 뉴스를 훑고, 데이터를 정리하고, 알림을 확인하는 일. 하나하나는 사소하지만, 쌓이면 하루를 통째로 잡아먹습니다. URSxClaw는 이 반복의 무게를 기술로 덜어드립니다.\n투자 시장에서는 감정 없이 원칙대로 움직이는 트레이딩 봇이, 일상에서는 정보를 수집하고 정리하고 알려주는 자동화 시스템이 여러분 대신 일합니다. 24시간, 쉬지 않고, 흔들리지 않고.\n복잡한 기술을 이해할 필요는 없습니다. 결과만 확인하세요. 나머지는 저희가 알아서 합니다.', 3),
        ("closing", "클로징", "당신의 시간은 차트 앞에 묶여 있을 만큼 가볍지 않습니다.\nURSxClaw가 일하는 동안, 당신은 당신의 하루를 사세요.", 99),
    ]

    for block_type, title, body, order in copy_data:
        c.execute(
            "INSERT OR IGNORE INTO copy_blocks (block_type, title, body, sort_order) VALUES (?, ?, ?, ?)",
            (block_type, title, body, order),
        )

    # ── 초기 데이터: services ──
    services_data = [
        ("자동 투자", "📈", "잠든 사이에도, 일하는 동안에도.", "검증된 전략 기반의 트레이딩 봇이 시장을 모니터링하고, 정해진 규칙에 따라 매매합니다. 잠든 사이에도, 일하는 동안에도.", 1),
        ("일상 자동화", "⚙️", "반복 작업을 시스템이 대신합니다.", "뉴스 수집, 데이터 정리, 리포트 생성, 알림 전송. 매일 손으로 하던 반복 작업을 시스템이 대신합니다.", 2),
        ("한눈에 보는 대시보드", "📊", "지금 필요한 정보만.", "내 자산과 자동화 현황을 깔끔한 화면 하나로 확인합니다. 복잡한 지표 대신, 지금 필요한 정보만.", 3),
    ]

    for name, icon, headline, desc, order in services_data:
        c.execute(
            "INSERT OR IGNORE INTO services (name, icon, headline, description, sort_order) VALUES (?, ?, ?, ?, ?)",
            (name, icon, headline, desc, order),
        )

    # ── 초기 데이터: principles (우리의 원칙) ──
    principles_data = [
        ("원칙이 감정을 이긴다", "시장이 흔들려도 봇은 흔들리지 않습니다. 미리 세운 규칙이 매 순간의 판단을 대신합니다.", 1),
        ("반복은 기계의 몫이다", "사람은 판단하고 결정하는 일에 집중해야 합니다. 단순 반복은 시스템에게 넘기세요.", 2),
        ("쉬워야 쓸 수 있다", "기술은 복잡해도 경험은 단순해야 합니다. 결과가 눈에 바로 들어오는 것, 그게 우리의 기준입니다.", 3),
    ]

    for title, desc, order in principles_data:
        c.execute(
            "INSERT OR IGNORE INTO principles (title, description, sort_order) VALUES (?, ?, ?)",
            (title, desc, order),
        )

    # ── 초기 데이터: voice_tone ──
    voice_data = [
        ("담백함", "과장하지 않는다. 있는 그대로, 필요한 만큼만 말한다.", "검증된 전략 기반으로 매매합니다.", "혁신적인 AI가 당신의 투자를 완전히 바꿔놓습니다!"),
        ("세련됨", "군더더기 없이 깔끔하다. 문장은 짧고 리듬감이 있다.", "24시간, 쉬지 않고, 흔들리지 않고.", "저희 시스템은 24시간 365일 끊김 없이 안정적으로 가동됩니다."),
        ("존중", "사용자를 가르치지 않는다. '쉬운', '간단한' 같은 평가 표현을 쓰지 않는다.", "결과만 확인하세요. 나머지는 저희가 알아서 합니다.", "초등학생도 이해할 수 있는 쉬운 인터페이스!"),
        ("신뢰감", "기술적 근거를 보여주되, 용어를 나열하지 않는다.", "정해진 규칙에 따라 매매합니다.", "최첨단 알고리즘과 머신러닝 기술을 활용하여..."),
        ("직접적", "비유, 은유 없이 실제 기능과 결과로 말한다.", "뉴스 수집, 데이터 정리, 리포트 생성, 알림 전송.", "마치 당신의 개인 비서처럼, 든든한 조력자가..."),
    ]

    for attr, desc, do_ex, dont_ex in voice_data:
        c.execute(
            "INSERT OR IGNORE INTO voice_tone (attribute, description, do_example, dont_example) VALUES (?, ?, ?, ?)",
            (attr, desc, do_ex, dont_ex),
        )

    # ── 초기 데이터: design_tokens ──
    tokens_data = {
        # 간격
        "spacing-xs": ("4px", "spacing", "최소 간격"),
        "spacing-sm": ("8px", "spacing", "작은 간격"),
        "spacing-md": ("16px", "spacing", "기본 간격"),
        "spacing-lg": ("24px", "spacing", "큰 간격"),
        "spacing-xl": ("32px", "spacing", "섹션 간격"),
        "spacing-2xl": ("48px", "spacing", "대형 섹션 간격"),
        "spacing-3xl": ("64px", "spacing", "히어로/풋터 간격"),

        # 모서리
        "radius-sm": ("8px", "radius", "작은 요소 (태그, 뱃지)"),
        "radius-md": ("12px", "radius", "기본 요소 (버튼, 입력)"),
        "radius-lg": ("16px", "radius", "카드, 모달"),
        "radius-xl": ("24px", "radius", "대형 카드, 히어로 영역"),
        "radius-full": ("9999px", "radius", "원형 (아바타, 아이콘)"),

        # 그림자
        "shadow-sm": ("0 1px 3px rgba(0,0,0,0.08)", "shadow", "미세한 띄움 (카드)"),
        "shadow-md": ("0 4px 12px rgba(0,0,0,0.10)", "shadow", "기본 띄움 (드롭다운, 팝오버)"),
        "shadow-lg": ("0 8px 30px rgba(0,0,0,0.12)", "shadow", "강한 띄움 (모달, 플로팅)"),
        "shadow-glow-blue": ("0 0 20px rgba(0,122,255,0.25)", "shadow", "파란 글로우 (호버, 포커스)"),
        "shadow-glow-yellow": ("0 0 20px rgba(255,214,10,0.30)", "shadow", "노란 글로우 (나노바나나 강조)"),

        # 글라스모피즘
        "glass-blur": ("20px", "glass", "배경 블러 강도"),
        "glass-bg-light": ("rgba(255,255,255,0.72)", "glass", "유리 배경 (라이트)"),
        "glass-bg-dark": ("rgba(28,28,30,0.72)", "glass", "유리 배경 (다크)"),
        "glass-border-light": ("1px solid rgba(255,255,255,0.18)", "glass", "유리 보더 (라이트)"),
        "glass-border-dark": ("1px solid rgba(255,255,255,0.08)", "glass", "유리 보더 (다크)"),

        # 애니메이션
        "transition-fast": ("150ms ease-out", "animation", "빠른 전환 (호버, 토글)"),
        "transition-normal": ("250ms ease-in-out", "animation", "기본 전환"),
        "transition-slow": ("400ms ease-in-out", "animation", "느린 전환 (모달, 페이지)"),
        "transition-spring": ("500ms cubic-bezier(0.34, 1.56, 0.64, 1)", "animation", "스프링 (팝업, 강조)"),
    }

    for key, (value, category, desc) in tokens_data.items():
        c.execute(
            "INSERT OR REPLACE INTO design_tokens (key, value, category, description, updated_at) VALUES (?, ?, ?, ?, datetime('now'))",
            (key, value, category, desc),
        )

    conn.commit()
    conn.close()
    print(f"✅ 브랜드 DB 초기화 완료: {DB_PATH}")
    print(f"   크기: {DB_PATH.stat().st_size / 1024:.1f} KB")


def query(table: str, where: str = None, limit: int = None):
    """범용 조회"""
    conn = get_conn()
    sql = f"SELECT * FROM {table}"
    if where:
        sql += f" WHERE {where}"
    if limit:
        sql += f" LIMIT {limit}"
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def export_json(output_path: str = None):
    """전체 브랜드 DB를 JSON으로 내보내기"""
    conn = get_conn()
    tables = ["brand_core", "colors", "typography", "copy_blocks",
              "voice_tone", "design_tokens", "principles", "services", "assets"]
    data = {}
    for t in tables:
        try:
            rows = conn.execute(f"SELECT * FROM {t}").fetchall()
            data[t] = [dict(r) for r in rows]
        except Exception:
            data[t] = []
    conn.close()

    out = Path(output_path) if output_path else Path(__file__).parent / "export" / "brand_identity.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ JSON 내보내기 완료: {out} ({out.stat().st_size / 1024:.1f} KB)")
    return data


def export_css_variables():
    """디자인 토큰 + 컬러를 CSS 변수로 내보내기"""
    conn = get_conn()

    lines_light = [":root {"]
    lines_dark = ["[data-theme='dark'] {"]

    # 컬러
    colors = conn.execute("SELECT * FROM colors").fetchall()
    for c in colors:
        var_name = f"--color-{c['role']}"
        if c["theme"] == "light":
            lines_light.append(f"  {var_name}: {c['hex']};  /* {c['name']} — {c['usage']} */")
        elif c["theme"] == "dark":
            lines_dark.append(f"  {var_name}: {c['hex']};  /* {c['name']} — {c['usage']} */")
        else:
            lines_light.append(f"  {var_name}: {c['hex']};  /* {c['name']} */")
            lines_dark.append(f"  {var_name}: {c['hex']};  /* {c['name']} */")

    # 디자인 토큰
    tokens = conn.execute("SELECT * FROM design_tokens").fetchall()
    lines_light.append("\n  /* 디자인 토큰 */")
    for t in tokens:
        lines_light.append(f"  --{t['key']}: {t['value']};  /* {t['description']} */")

    lines_light.append("}")
    lines_dark.append("}")

    conn.close()

    css = "/* URSxClaw Brand Identity — Auto-generated */\n\n"
    css += "\n".join(lines_light) + "\n\n" + "\n".join(lines_dark) + "\n"

    out = Path(__file__).parent / "export" / "brand_tokens.css"
    out.write_text(css, encoding="utf-8")
    print(f"✅ CSS 변수 내보내기 완료: {out}")
    return css


def print_summary():
    """브랜드 DB 요약 출력"""
    conn = get_conn()
    tables = {
        "brand_core": "핵심 정보",
        "colors": "컬러 팔레트",
        "typography": "타이포그래피",
        "copy_blocks": "카피 블록",
        "voice_tone": "보이스 & 톤",
        "design_tokens": "디자인 토큰",
        "principles": "원칙",
        "services": "서비스",
        "assets": "에셋",
    }

    print("=" * 50)
    print("  URSxClaw Brand Identity DB")
    print("  나노바나나 스타일")
    print("=" * 50)

    for table, label in tables.items():
        try:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {label:<15} │ {count}건")
        except Exception:
            print(f"  {label:<15} │ 0건")

    print("=" * 50)

    # 태그라인 출력
    row = conn.execute("SELECT value FROM brand_core WHERE key='tagline'").fetchone()
    if row:
        print(f'\n  "{row[0]}"')

    conn.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "export-json":
            export_json()
        elif cmd == "export-css":
            export_css_variables()
        elif cmd == "summary":
            print_summary()
        else:
            print(f"사용법: python brand_db.py [export-json|export-css|summary]")
    else:
        init_db()
        print_summary()
        export_json()
        export_css_variables()
