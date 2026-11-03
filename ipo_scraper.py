#!/usr/bin/env python3
"""
38커뮤니케이션 공모주 청약 및 신규 상장 일정 자동 수집기
오픈소스: jiunbae/gong-mo 기반 커스텀 제작
사용자: 이신엽 님 전용 공모주 알리미
"""

import os
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
    """청약 예정 및 진행 중인 공모주 목록 (오늘 이후 마감 건만 추출, 시작일 오름차순 정렬)"""
    url = "http://www.38.co.kr/html/fund/index.htm?o=k"
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    today_str = datetime.now().strftime("%Y.%m.%d")
    items = []
    
    for tr in soup.find_all("tr"):
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) >= 6:
            name = tds[0]
            schedule = tds[1]
            fixed_price = tds[2] if tds[2] != "-" else "미확정"
            hope_price = tds[3]
            underwriter = tds[5]
            
            if 1 < len(name) < 25 and "~" in schedule and "202" in schedule:
                if not any(skip in name for skip in ["종목명", "공모뉴스", "공모주일정", "Home", "신규상장"]):
                    try:
                        start_str, end_str = schedule.split("~")
                        year = start_str.strip().split(".")[0]
                        full_start = start_str.strip()
                        full_end = f"{year}.{end_str.strip()}"
                        
                        # 오늘 이후에 끝나는 청약만 포함
                        if full_end >= today_str:
                            items.append({
                                "name": name,
                                "schedule": schedule,
                                "start_date": full_start,
                                "end_date": full_end,
                                "fixed_price": fixed_price,
                                "hope_price": hope_price,
                                "underwriter": underwriter
                            })
                    except Exception:
                        continue
                        
    items.sort(key=lambda x: x["start_date"])
    return items

def get_upcoming_listings():
    """신규 상장 예정 공모주 목록 (오늘 이후 상장 또는 예정 상태 건, 상장일 오름차순 정렬)"""
    url = "http://www.38.co.kr/html/fund/index.htm?o=nw"
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    today_slash = datetime.now().strftime("%Y/%m/%d")
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
                    # 오늘 이후 상장이거나, 오늘 상장 예정인 건만 포함
                    is_upcoming = (listing_date > today_slash) or (listing_date == today_slash and status == "예정")
                    if is_upcoming:
                        items.append({
                            "name": name,
                            "listing_date": listing_date,
                            "price": price,
                            "status": status if status else "예정"
                        })
                        
    items.sort(key=lambda x: x["listing_date"])
    return items

def save_markdown_report(output_path="latest_ipo_schedule.md"):
    """최신 공모주 일정을 깔끔한 마크다운 리포트로 저장"""
    listings = get_upcoming_listings()
    subs = get_upcoming_subscriptions()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    md = []
    md.append(f"# 📈 공모주 청약 & 신규 상장 최신 일정")
    md.append(f"> 수집 일시: `{now_str}` (출처: 38커뮤니케이션)\n")
    
    md.append("## 🔔 다가오는 신규 상장 일정")
    md.append("| 상장일 | 종목명 | 공모가 | 상태 | 비고 |")
    md.append("| :--- | :--- | :---: | :---: | :--- |")
    for item in listings:
        note = "⭐ 신엽 님 보유 (107주)" if "아이엠스팩1호" in item["name"] else "-"
        md.append(f"| {item['listing_date']} | **{item['name']}** | {item['price']}원 | `{item['status']}` | {note} |")
        
    md.append("\n## 📝 청약 예정 및 진행 종목")
    md.append("| 청약 기간 | 종목명 | 공모가 (확정/희망) | 주관사 | 일정 구분 |")
    md.append("| :--- | :--- | :---: | :--- | :---: |")
    for item in subs:
        price_str = f"확정 {item['fixed_price']}원" if item["fixed_price"] != "미확정" else f"희망 {item['hope_price']}원"
        today_str = datetime.now().strftime("%Y.%m.%d")
        if item["end_date"] == today_str:
            tag = "오늘 마감"
        elif item["start_date"] <= today_str <= item["end_date"]:
            tag = "진행 중"
        else:
            tag = "청약 예정"
        md.append(f"| {item['schedule']} | **{item['name']}** | {price_str} | {item['underwriter']} | `{tag}` |")
        
    content = "\n".join(md) + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return content

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
        note = " (⭐ 신엽 님 107주 보유)" if "아이엠스팩1호" in item["name"] else ""
        output.append(f"• {item['listing_date']} | {item['name']} (공모가 {item['price']}원) {status_tag}{note}")
        
    output.append("\n[📝 청약 예정 및 진행 종목 (최신 6건)]")
    subs = get_upcoming_subscriptions()[:6]
    for item in subs:
        price_str = f"확정 {item['fixed_price']}원" if item['fixed_price'] != "미확정" else f"희망 {item['hope_price']}원"
        output.append(f"• {item['schedule']} | {item['name']} ({price_str}) | 주관: {item['underwriter']}")
        
    output.append("\n" + "=" * 55)
    return "\n".join(output)

if __name__ == "__main__":
    print(get_summary_text())
    save_markdown_report("latest_ipo_schedule.md")
