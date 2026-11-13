# -*- coding: utf-8 -*-
"""상단 메뉴(상위/하위) 정의. 메뉴를 바꾸려면 이 파일만 고치고 아래 두 스크립트를 실행한다.

  python3 scripts/build_menu_pages.py   # 아직 내용이 없는 하위 페이지(준비 중 안내) 생성
  python3 scripts/apply_nav.py          # 전 페이지 상단 메뉴 갱신

항목 = (이름, 주소). 이미 만들어진 페이지는 그 주소를 쓰고,
없는 페이지는 아래 PLACEHOLDER 주소로 '준비 중' 페이지가 만들어진다(검색 제외).
실제 내용 페이지를 만들 때는 해당 폴더의 index.html 에서 <!-- MENU-PLACEHOLDER --> 줄을 지우면
build_menu_pages.py 가 덮어쓰지 않는다.
"""
BOOKING = "https://booking.naver.com/booking/13/bizes/185044"

MENU = [
    ("지인한의원 소개", [
        ("미션", "/mission/"),
        ("의료진소개", "/about/"),
        ("진료시간", "/#info"),
        ("주차장안내", "/clinic/parking/"),
        ("오시는길", "/#info"),
        ("예약", BOOKING),
    ]),
    ("특별한치료법", [
        ("고농도봉침", "/special/high-dose-bee-venom/"),
        ("약침·매선·도침·정안침", "/treatments/"),
        ("수승화강약침", "/special/suseung-hwagang/"),
        ("의학입문맥진", "/special/uihak-ipmun-maekjin/"),
        ("진단 및 검사", "/special/diagnosis/"),
    ]),
    ("안면마비·삼차신경통", [
        ("안면부 질환", "/facial-palsy/"),
        ("삼차신경통", "/trigeminal-neuralgia/"),
    ]),
    ("자율신경", [
        ("스트레스", "/autonomic/stress/"),
        ("난치", "/autonomic/intractable/"),
        ("수면장애", "/autonomic/sleep/"),
    ]),
    ("내과", [
        ("소화장애", "/digestion/"),
        ("폐기관지", "/internal/respiratory/"),
        ("내분비호르몬", "/internal/endocrine/"),
    ]),
    ("난임여성", [
        ("난임", "/fertility/infertility/"),
        ("산후", "/postpartum/"),
        ("유산후", "/fertility/after-miscarriage/"),
        ("임신", "/fertility/pregnancy/"),
        ("산부인과질환", "/women/"),
    ]),
    ("남성피로", [
        ("발기부전", "/men/erectile-dysfunction/"),
        ("조루", "/men/premature-ejaculation/"),
        ("남성갱년기", "/men/male-menopause/"),
        ("전립선비대", "/men/bph/"),
        ("전립선염", "/men/prostatitis/"),
    ]),
    ("소아", [
        ("성장", "/kids/growth/"),
        ("비만", "/kids/obesity/"),
        ("감기", "/kids/cold/"),
        ("피부아토피", "/kids/atopy/"),
        ("소아신경정신과", "/kids/neuropsychiatry/"),
    ]),
    ("통증", [
        ("교통사고후유증", "/car-accident/"),
        ("질환", "/pain/"),
    ]),
    ("다이어트", [
        ("다이어트한약", "/diet/"),
        ("부분다이어트케어", "/diet/partial-care/"),
    ]),
    ("피부탈모", [
        ("피부질환", "/skin/"),
        ("탈모", "/hair-loss/"),
    ]),
    ("안이비인후과", [
        ("눈", "/eent/eye/"),
        ("귀", "/eent/ear/"),
        ("인후두부위", "/eent/throat/"),
        ("코", "/rhinitis/"),
    ]),
    ("기타", [
        ("기타", "/etc/"),
    ]),
]

# 상위 메뉴 오른쪽에 따로 두는 바로가기
UTIL = [("칼럼", "/columns/"), ("생활한방노트", "/notes/")]
