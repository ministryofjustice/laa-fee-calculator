# -*- coding: utf-8 -*-
BASIC_FEES_MAP = {
    'FXACV': 'AGFS_APPEAL_CON',
    'FXASE': 'AGFS_APPEAL_SEN',
    'FXCBR': 'AGFS_ORDER_BRCH',
    'FXCSE': 'AGFS_COMMITTAL',
    'FXCON': None,
    'GRRAK': 'AGFS_FEE',
    'GRCBR': 'AGFS_FEE',
    'GRDIS': 'AGFS_FEE',
    'FXENP': 'AGFS_FEE',
    'GRGLT': 'AGFS_FEE',
    'FXH2S': 'AGFS_FEE',
    'GRRTR': 'AGFS_FEE',
    'GRTRL': 'AGFS_FEE'
}

FEES_MAP = {
    'BABAF': None,    # special processing
    'BACAV': None,    # needs investigation
    'BADAF': None,
    'BADAH': None,
    'BADAJ': None,
    'BANOC': None,
    'BANDR': None,
    'BANPW': None,
    'BAPPE': None,
    'BAPCM': ('AGFS_MISC_FEES', 'AGFS_PLEA'),
    'BASAF': ('AGFS_MISC_FEES', 'AGFS_STD_APPRNC'),
    'FXALT': None,
    'FXACV': ('AGFS_FEE', 'AGFS_APPEAL_CON'),
    'FXACU': None,
    'FXASE': ('AGFS_FEE', 'AGFS_APPEAL_SEN'),
    'FXASU': None,
    'FXASS': None,
    'FXCBR': None,
    'FXCBU': None,
    'FXCSE': ('AGFS_FEE', 'AGFS_COMMITTAL'),
    'FXCSU': None,
    'FXCON': ('AGFS_MISC_FEES', 'AGFS_CONTEMPT'),
    'FXCCD': None,
    'FXCDU': None,
    'FXENP': None,
    'FXENU': None,
    'FXH2S': None,
    'FXNOC': None,
    'FXNDR': None,
    'FXSAF': ('AGFS_MISC_FEES', 'AGFS_STD_APPRNC'),
    'FXASB': None,
    'GRCBR': None,
    'GRRAK': None,
    'GRDIS': None,
    'GRGLT': None,
    'GRRTR': None,
    'GRTRL': None,
    'INDIS': None,
    'INPCM': None,
    'INRNS': None,
    'INRST': None,
    'INTDT': None,
    'INWAR': None,
    'MIAHU': None,
    'MIAPH': ('AGFS_MISC_FEES', 'AGFS_ABS_PRC_HF'),
    'MIAWU': None,
    'MIAPW': ('AGFS_MISC_FEES', 'AGFS_ABS_PRC_WL'),
    'MISAF': ('AGFS_MISC_FEES', 'AGFS_ABS_PRC_HF'),
    'MIADC3': None,
    'MIADC1': ('AGFS_MISC_FEES', 'AGFS_DMS_DY2_HF'),
    'MIADC4': None,
    'MIADC2': ('AGFS_MISC_FEES', 'AGFS_DMS_DY2_WL'),
    'MIUPL': None,
    'MIDHU': None,
    'MIDTH': ('AGFS_MISC_FEES', 'AGFS_CONFISC_HF'),
    'MIDWU': None,
    'MIDTW': ('AGFS_MISC_FEES', 'AGFS_CONFISC_WL'),
    'MICJA': ('AGFS_EXPENSES', 'AGFS_CJD_FEE'),
    'MICJP': ('AGFS_EXPENSES', 'AGFS_CJD_EXP'),
    'MIDSE': ('AGFS_MISC_FEES', 'AGFS_DEF_SEN_HR'),
    'MIDSU': None,
    'MIEVI': ('AGFS_EVIDPRVFEE', 'AGFS_EVIDPRVFEE'),
    'MIEHU': None,
    'MIAEH': ('AGFS_MISC_FEES', 'AGFS_ADM_EVD_HF'),
    'MIEWU': None,
    'MIAEW': ('AGFS_MISC_FEES', 'AGFS_ADM_EVD_WL'),
    'MIHHU': None,
    'MIHDH': ('AGFS_MISC_FEES', 'AGFS_DISC_HALF'),
    'MIHWU ': None,
    'MIHDW': ('AGFS_MISC_FEES', 'AGFS_DISC_FULL'),
    'MINBR': ('AGFS_MISC_FEES', 'AGFS_NOTING_BRF'),
    'MIPPC': ('AGFS_MISC_FEES', 'AGFS_PAPER_PLEA'),
    'MIPCU': None,
    'MICHU': None,
    'MIPCH': None,
    'MICHW': None,
    'MIPCW': None,
    'MIPIU3': None,
    'MIPIH1': ('AGFS_MISC_FEES', 'AGFS_PI_IMMN_HF'),
    'MIPIH4': None,
    'MIPIH2': ('AGFS_MISC_FEES', 'AGFS_PI_IMMN_WL'),
    'MIRNF': ('AGFS_MISC_FEES', 'AGFS_NOVELISSUE'),
    'MIRNL': ('AGFS_MISC_FEES', 'AGFS_NOVEL_LAW'),
    'MISHR': ('AGFS_MISC_FEES', 'AGFS_SENTENCE'),
    'MISHU': None,
    'MISPF': ('AGFS_MISC_FEES', 'SPECIAL_PREP'),
    'MISAU': None,
    'MITNP': ('AGFS_MISC_FEES', 'AGFS_NOT_PRCD'),
    'MITNU': None,
    'MIUAV3': None,
    'MIUAV1': ('AGFS_MISC_FEES', 'AGFS_UN_VAC_HF'),
    'MIUAV4': None,
    'MIUAV2': ('AGFS_MISC_FEES', 'AGFS_UN_VAC_WL'),
    'MIWPF': ('AGFS_MISC_FEES', 'AGFS_WSTD_PREP'),
    'MIWOA': ('AGFS_MISC_FEES', 'AGFS_WRTN_ORAL'),
    'TRANS': None,
    'WARR': None,
}

REVERSE_FEES_MAP = {v: k for k, v in FEES_MAP.items() if v}


def bill_to_code(bill_type, sub_type):
    """
    return the unique code for a bill_type ans sub_type pair

    :param bill_type: str
    :param sub_type: str
    :return: str
    """
    if bill_type == 'AGFS_FEE' and sub_type in BASIC_FEES_MAP.values():
        return 'BABAF'
    return REVERSE_FEES_MAP[(bill_type, sub_type)]


SCENARIO_MAP = {
    2694: 1,
    2695: 2,
    2696: {1: 3, 2: 13, 3: 13},
    2697: 4,
    2698: 5,
    2699: 6,
    2700: 7,
    2701: 8,
    2702: 9,
    2703: {1: 10, 2: 14, 3: 14},
    2704: 11,
    2705: 12
}


def scenario_ccr_to_id(ccr_id, third):
    scenario = SCENARIO_MAP[int(ccr_id)]
    if isinstance(scenario, dict):
        return scenario[int(third)]
    return scenario
