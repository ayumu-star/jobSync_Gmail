# app/services/company_parser.py
import re

# よく出る会社名のパターン
COMPANY_SUFFIX_PATTERNS = [
    r"(株式会社[\u4E00-\u9FFFＡ-ＺA-Z0-9ぁ-んァ-ンー・\s]+)",   # 株式会社○○
    r"([\u4E00-\u9FFFＡ-ＺA-Z0-9ぁ-んァ-ンー・\s]+株式会社)",   # ○○株式会社
    r"([\u4E00-\u9FFFＡ-ＺA-Z0-9ぁ-んァ-ンー・\s]+(株))",        # ○○(株)
]

BRACKET_PAT = re.compile(r"[【\[](.+?)[\】\]]")

def _clean_company_name(name: str) -> str:
    if not name:
        return ""
    # 不要な全角スペースや前後の空白を削る
    name = name.replace("　", " ").strip()
    # 末尾の記号類を軽く削る
    name = re.sub(r"[\s\-・]+$", "", name)
    return name

def _from_display_name(from_address: str) -> str | None:
    """
    "○○株式会社 採用担当" <xxx@example.com> みたいな From から会社名っぽいところだけ抜く
    """
    if not from_address:
        return None

    # "表示名" <mail> の「表示名」部分だけ抜く
    m = re.match(r'"?([^"]+)"?\s*<.*>', from_address)
    display = m.group(1) if m else from_address

    # 「採用担当」「人事部」などの役職っぽい部分を削る
    display = re.sub(r"(採用担当|人事部|キャリア採用グループ|採用チーム|運営事務局).*", "", display)

    # 会社名パターンでマッチを狙う
    for pat in COMPANY_SUFFIX_PATTERNS:
        m2 = re.search(pat, display)
        if m2:
            return _clean_company_name(m2.group(1))

    # うまく取れなかったらそのまま（長すぎる場合は捨ててもOK）
    if 2 <= len(display) <= 40:
        return _clean_company_name(display)

    return None


def extract_company_name(subject: str | None, body: str | None, from_address: str | None) -> str | None:
    """
    件名・本文・Fromから「会社名らしきもの」を推定して返す。
    見つからなければ None。
    """
    text_list = [subject or "", body or ""]

    # 1) 件名 / 本文の【○○】の中身から会社名パターンを探す
    for text in text_list:
        for bracket in BRACKET_PAT.findall(text):
            for pat in COMPANY_SUFFIX_PATTERNS:
                m = re.search(pat, bracket)
                if m:
                    return _clean_company_name(m.group(1))

    # 2) 件名全体から直接マッチを探す
    for pat in COMPANY_SUFFIX_PATTERNS:
        m = re.search(pat, subject or "")
        if m:
            return _clean_company_name(m.group(1))

    # 3) 本文フッター（署名）などから探す（最後の数行だけ見るなどでもOK）
    if body:
        lines = body.splitlines()
        tail = "\n".join(lines[-10:])  # 下10行くらい
        for pat in COMPANY_SUFFIX_PATTERNS:
            m = re.search(pat, tail)
            if m:
                return _clean_company_name(m.group(1))

    # 4) 最後の手段として From の表示名から推定
    company_from_sender = _from_display_name(from_address or "")
    if company_from_sender:
        return company_from_sender

    return None
