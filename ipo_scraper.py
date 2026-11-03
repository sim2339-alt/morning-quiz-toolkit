#!/usr/bin/env python3
"""
38커뮤니케이션 공모주 청약 및 신규 상장 일정 자동 수집기
오픈소스: jiunbae/gong-mo 기반 커스텀 제작
사용자: 이신엽 님 전용 공모주 알리미
"""

import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("euc-kr", errors="replace")

def get_upcoming_subscriptions():
    """청약 예정 및 진행 중인 공모주 목록"""
    url = "http://www.38.co.kr/html/fund/index.htm?o=k"
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    items = []
    # 38커뮤니케이션 공모청약일정 테이블 파싱
    for tr in soup.find_all("tr"):
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) >= 6:
            name = tds[0]
            schedule = tds[1]
            fixed_price = tds[2] if tds[2] != "-" else "미확정"
            hope_price = tds[3]
            underwriter = tds[5]
            
            # 유효한 행인지 검증 (종목명 길이가 적절하고 날짜 형식 'YYYY.MM.DD' 포함)
            if 1 < len(name) < 25 and "~" in schedule and "202" in schedule:
                if not any(skip in name for skip in ["종목명", "공모뉴스", "공모주일정", "Home", "신규상장"]):
                    items.append({
                        "name": name,
                        "schedule": schedule,
                        "fixed_price": fixed_price,
                        "hope_price": hope_price,
                        "underwriter": underwriter
                    })
    return items

def get_upcoming_listings():
    """신규 상장 예정 공모주 목록"""
    url = "http://www.38.co.kr/html/fund/index.htm?o=nw"
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    items = []
    for tr in soup.find_all("tr"):
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) >= 8:
            name = tds[0]
            listing_date = tds[1]
            price = tds[4]
            status = tds[8] if len(tds) > 8 else ""
            if 1 < len(name) < 25 and "/" in listing_date and "202" in listing_date:
                if not any(skip in name for skip in ["기업명", "공모뉴스", "Home", "신규상장", "1[2]"]):
                    items.append({
                        "name": name,
                        "listing_date": listing_date,
                        "price": price,
                        "status": status
                    })
    return items

def get_summary_text():
    output = []
    output.append("=" * 55)
    output.append("   📈 38커뮤니케이션 공모주 청약 & 상장 실시간 일정")
    output.append(f"   (수집 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')})")
    output.append("=" * 55)
    
    output.append("\n[🔔 다가오는 신규 상장 일정]")
    listings = get_upcoming_listings()
    for item in listings[:6]:
        status_tag = f"[{item['status']}]" if item['status'] else ""
        output.append(f"• {item['listing_date']} | {item['name']} (공모가 {item['price']}원) {status_tag}")
        
    output.append("\n[📝 청약 예정 및 진행 종목 (최신 6건)]")
    subs = get_upcoming_subscriptions()[:6]
    for item in subs:
        price_str = f"확정 {item['fixed_price']}원" if item['fixed_price'] != "미확정" else f"희망 {item['hope_price']}원"
        output.append(f"• {item['schedule']} | {item['name']} ({price_str}) | 주관: {item['underwriter']}")
        
    output.append("\n" + "=" * 55)
    return "\n".join(output)

if __name__ == "__main__":
    print(get_summary_text())
