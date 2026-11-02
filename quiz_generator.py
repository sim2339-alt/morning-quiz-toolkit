#!/usr/bin/env python3
"""
초등 아침 활동 창의 퀴즈 & 두뇌 스트레칭 자동 생성기
작성자: 몽실이 (for 이신엽 선생님)
"""

import random

QUIZ_DATABASE = [
    {
        "category": "초성 퀴즈",
        "question": "교실에서 매일 보는 이것! [ㅊ ㅍ]",
        "hint": "선생님이 글씨를 쓰시는 곳이에요.",
        "answer": "칠판"
    },
    {
        "category": "초성 퀴즈",
        "question": "공부할 때 꼭 필요한 학용품! [ㅈ ㄱ]",
        "hint": "틀린 글씨를 지울 때 써요.",
        "answer": "지우개"
    },
    {
        "category": "넌센스 퀴즈",
        "question": "세상에서 가장 착한 사자는?",
        "hint": "도덕적인 사자예요.",
        "answer": "자원봉사자"
    },
    {
        "category": "넌센스 퀴즈",
        "question": "왕이 넘어지면 무엇이 될까요?",
        "hint": "두 글자예요.",
        "answer": "킹콩"
    },
    {
        "category": "넌센스 퀴즈",
        "question": "신발이 화가 나면?",
        "hint": "신발의 한 종류예요.",
        "answer": "신발끈"
    },
    {
        "category": "두뇌 스트레칭 (수학)",
        "question": "어떤 수에 5를 더하고 2를 곱했더니 24가 되었습니다. 어떤 수는?",
        "hint": "거꾸로 계산해 보세요: 24 ÷ 2 - 5",
        "answer": "7"
    },
    {
        "category": "두뇌 스트레칭 (수학)",
        "question": "시계 바늘이 3시를 가리킬 때, 시침과 분침이 이루는 각도는 몇 도일까요?",
        "hint": "직각이에요.",
        "answer": "90도"
    },
    {
        "category": "창의력 연상 퀴즈",
        "question": "사과, 딸기, 소방차, 우체통의 공통점은 무엇일까요?",
        "hint": "눈으로 보이는 특징이에요.",
        "answer": "빨간색이다"
    },
    {
        "category": "창의력 연상 퀴즈",
        "question": "바늘은 있지만 실은 없고, 숫자는 있지만 글자는 없고, 얼굴은 있지만 입은 없는 것은?",
        "hint": "시간을 알려줘요.",
        "answer": "시계"
    }
]

def generate_morning_quiz(count=3):
    selected = random.sample(QUIZ_DATABASE, min(count, len(QUIZ_DATABASE)))
    print("=" * 45)
    print("   ☀️ 오늘 아침 두뇌 활짝 퀴즈 타임! ☀️")
    print("=" * 45)
    for i, q in enumerate(selected, 1):
        print(f"\n[문제 {i}] ({q['category']})")
        print(f"Q: {q['question']}")
        print(f"💡 힌트: {q['hint']}")
        print(f"👉 정답: {q['answer']}")
    print("\n" + "=" * 45)
    print("   오늘도 즐겁고 힘찬 하루 보내세요! 🎉")
    print("=" * 45)

if __name__ == "__main__":
    generate_morning_quiz(3)
