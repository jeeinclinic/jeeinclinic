# -*- coding: utf-8 -*-
"""상단 메뉴(상위/하위) 정의. 메뉴를 바꾸려면 이 파일만 고치고 아래 두 스크립트를 실행한다.

  python3 scripts/build_menu_pages.py   # 아직 내용이 없는 하위 페이지(준비 중 안내) 생성
  python3 scripts/apply_nav.py          # 전 페이지 상단 메뉴 갱신

항목 = (이름, 주소) 또는 (이름, 주소, [3단계 항목들]). 이미 만들어진 페이지는 그 주소를 쓰고,
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
    ("구안와사·삼차신경통", [
        ("안면부질환", "/facial-palsy/", [
            ("구안와사", "/facial-palsy/"),
            ("삼차신경통", "/trigeminal-neuralgia/"),
            ("얼굴떨림", "/face/tremor/"),
            ("얼굴감각장애", "/face/sensory-disorder/"),
            ("안면비대칭", "/face/asymmetry/"),
        ]),
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
        ("피부질환", "/skin/", [
            ("가려움", "/skin/itching/"),
            ("건선", "/skin/psoriasis/"),
            ("두드러기", "/skin/urticaria/"),
            ("모공각화증", "/skin/keratosis-pilaris/"),
            ("습진", "/skin/eczema/"),
            ("아토피", "/skin/atopy/"),
            ("안면홍조", "/skin/facial-flushing/"),
            ("알레르기성자반증", "/skin/allergic-purpura/"),
            ("양진", "/skin/prurigo/"),
            ("여드름", "/skin/acne/"),
            ("유두습진", "/skin/nipple-eczema/"),
            ("장미색비강진", "/skin/pityriasis-rosea/"),
            ("접촉성피부염", "/skin/contact-dermatitis/"),
            ("주사비", "/skin/rosacea/"),
            ("지루성피부", "/skin/seborrheic/"),
            ("콜린성두드러기", "/skin/cholinergic-urticaria/"),
            ("피부묘기증", "/skin/dermatographism/"),
            ("한포진", "/skin/dyshidrosis/"),
            ("헤르페스", "/skin/herpes/"),
            ("화폐상습진", "/skin/nummular-eczema/"),
        ]),
        ("탈모", "/hair-loss/"),
    ]),
    ("이비인후과", [
        ("눈", "/eent/eye/", [
            ("안구건조", "/eent/eye/dry-eye/"),
            ("유루증", "/eent/eye/tearing/"),
            ("눈떨림", "/eent/eye/eyelid-twitching/"),
            ("안구피로", "/eent/eye/eye-fatigue/"),
            ("눈가려움", "/eent/eye/itchy-eye/"),
        ]),
        ("귀", "/eent/ear/", [
            ("어지럼", "/eent/ear/dizziness/"),
            ("전정신경염", "/eent/ear/vestibular-neuritis/"),
            ("메니에르", "/eent/ear/meniere/"),
            ("이석", "/eent/ear/otolith/"),
            ("이명", "/eent/ear/tinnitus/"),
            ("돌발성난청", "/eent/ear/sudden-hearing-loss/"),
            ("이관질환", "/eent/ear/eustachian-tube/"),
            ("중이염", "/eent/ear/otitis-media/"),
        ]),
        ("인후두부위", "/eent/throat/", [
            ("후두염", "/eent/throat/laryngitis/"),
            ("목젖부음", "/eent/throat/swollen-uvula/"),
            ("편도선염", "/eent/throat/tonsillitis/"),
            ("편도결석", "/eent/throat/tonsil-stones/"),
        ]),
        ("입", "/eent/mouth/", [
            ("입술포진", "/eent/mouth/cold-sore/"),
            ("설염", "/eent/mouth/glossitis/"),
            ("구강건조", "/eent/mouth/dry-mouth/"),
            ("입냄새", "/eent/mouth/bad-breath/"),
            ("혀통증", "/eent/mouth/tongue-pain/"),
        ]),
        ("코", "/rhinitis/", [
            ("비염", "/rhinitis/"),
            ("비중격만곡", "/eent/nose/deviated-septum/"),
            ("부비동염", "/eent/nose/sinusitis/"),
            ("코피", "/eent/nose/nosebleed/"),
            ("코가려움", "/eent/nose/itchy-nose/"),
            ("후비루", "/eent/nose/postnasal-drip/"),
        ]),
    ]),
    ("보약", [
        ("보약", "/boyak/"),
    ]),
]

# 상위 메뉴 오른쪽에 따로 두는 바로가기
UTIL = [("칼럼", "/columns/"), ("생활한방노트", "/notes/")]


def kid(k):
    """하위 항목을 (이름, 주소, 3단계목록)으로 통일."""
    return (k[0], k[1], k[2] if len(k) > 2 else [])
