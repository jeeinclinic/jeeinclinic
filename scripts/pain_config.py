# -*- coding: utf-8 -*-
"""통증 > 질환 : 부위별 분류와 병명 목록. 부위는 위→아래 순서, 병명은 ㄱㄴㄷ 순(자동 정렬).
부위 = (이름, 주소 슬러그, [(병명, 슬러그), ...])
"""
PAIN_PARTS = [
    ("머리·두통", "head", [("편두통", "migraine"), ("긴장성두통", "tension-headache"), ("경추성두통", "cervicogenic-headache"),
        ("후두신경통", "occipital-neuralgia"), ("군발두통", "cluster-headache"), ("만성두통", "chronic-headache")]),
    ("턱관절", "jaw", [("턱관절장애", "tmd"), ("턱관절염", "tmj-arthritis"), ("이갈이·이악물기", "bruxism"),
        ("개구장애", "limited-mouth-opening"), ("턱관절잡음", "tmj-noise")]),
    ("목", "neck", [("목디스크", "cervical-disc"), ("거북목", "forward-head"), ("일자목", "straight-neck"),
        ("경추협착증", "cervical-stenosis"), ("경추염좌", "cervical-sprain"), ("경추성어지럼", "cervicogenic-dizziness")]),
    ("어깨", "shoulder", [("오십견", "frozen-shoulder"), ("회전근개질환", "rotator-cuff"), ("어깨충돌증후군", "shoulder-impingement"),
        ("석회화건염", "calcific-tendinitis"), ("어깨점액낭염", "shoulder-bursitis"), ("관절와순손상", "labrum-tear"),
        ("견쇄관절염", "ac-joint-arthritis")]),
    ("등·견갑골", "upper-back", [("견갑골내측통증", "medial-scapular-pain"), ("견갑골운동장애", "scapular-dyskinesis"),
        ("능형근통증", "rhomboid-pain"), ("상부승모근통증", "upper-trapezius-pain"), ("흉추통증", "thoracic-pain"),
        ("흉추디스크", "thoracic-disc"), ("등 근막통증증후군", "back-myofascial-pain"), ("라운드숄더", "round-shoulder")]),
    ("가슴·갈비뼈", "chest", [("늑연골염", "costochondritis"), ("늑골염좌", "rib-sprain"), ("늑간근통증", "intercostal-muscle-pain"),
        ("늑간신경통", "intercostal-neuralgia"), ("갈비뼈 골절 후 통증", "post-rib-fracture-pain"), ("흉벽통증", "chest-wall-pain"),
        ("비심장성 흉통", "non-cardiac-chest-pain"), ("대흉근통증", "pectoralis-pain")]),
    ("팔·팔꿈치", "arm-elbow", [("테니스엘보", "tennis-elbow"), ("골프엘보", "golfers-elbow"), ("팔꿈치터널증후군", "cubital-tunnel"),
        ("주두점액낭염", "olecranon-bursitis"), ("팔꿈치관절염", "elbow-arthritis"), ("팔저림", "arm-numbness"),
        ("흉곽출구증후군", "thoracic-outlet"), ("상완신경통", "brachial-neuralgia"), ("경추성 팔통증", "cervicogenic-arm-pain"),
        ("팔 근막통증", "arm-myofascial-pain")]),
    ("손목·손", "wrist-hand", [("방아쇠수지", "trigger-finger"), ("손가락관절염", "finger-arthritis"), ("손저림", "hand-numbness"),
        ("엄지손가락통증", "thumb-pain"), ("손가락건초염", "finger-tenosynovitis"), ("손가락염좌", "finger-sprain"),
        ("손목터널증후군", "carpal-tunnel"), ("드퀘르벵병", "de-quervain"), ("손목건초염", "wrist-tenosynovitis"),
        ("TFCC 손상", "tfcc-injury"), ("손목염좌", "wrist-sprain"), ("손목관절염", "wrist-arthritis")]),
    ("허리", "low-back", [("허리디스크", "lumbar-disc"), ("척추관협착증", "spinal-stenosis"), ("좌골신경통", "sciatica"),
        ("급성요추염좌", "acute-lumbar-sprain"), ("만성요통", "chronic-low-back-pain"), ("척추전방전위증", "spondylolisthesis"),
        ("요추분리증", "spondylolysis"), ("요방형근통증", "quadratus-lumborum-pain"), ("측복부 근막통증", "flank-myofascial-pain"),
        ("운동 후 옆구리통증", "post-exercise-flank-pain")]),
    ("골반·고관절", "pelvis-hip", [("천장관절증후군", "si-joint"), ("이상근증후군", "piriformis"), ("꼬리뼈통증", "coccydynia"),
        ("산후골반통", "postpartum-pelvic-pain"), ("고관절충돌증후군", "hip-impingement"), ("골반틀어짐", "pelvic-misalignment")]),
    ("전신·관절·후유증", "whole-body", [("류마티스관절염", "rheumatoid-arthritis"), ("퇴행성관절염", "osteoarthritis"),
        ("통풍", "gout"), ("수술후·외상 후유증", "post-surgery-trauma"), ("골절후유증", "post-fracture"),
        ("골다공증", "osteoporosis"), ("만성통증증후군", "chronic-pain-syndrome"), ("섬유근통", "fibromyalgia")]),
]


def parts():
    """정렬된 [(부위이름, 슬러그, [(병명, 슬러그)])]"""
    return [(n, s, sorted(items, key=lambda x: x[0])) for n, s, items in PAIN_PARTS]
