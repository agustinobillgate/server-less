#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from functions.htpchar import htpchar
from functions.get_vipnrbl import get_vipnrbl

def prepare_telop_1bl():
    vipnr1 = 999999999
    vipnr2 = 999999999
    vipnr3 = 999999999
    vipnr4 = 999999999
    vipnr5 = 999999999
    vipnr6 = 999999999
    vipnr7 = 999999999
    vipnr8 = 999999999
    vipnr9 = 999999999
    ci_date = None
    lineswitch_lic = False
    i_param297 = 0
    ext_char = ""
    avail_gdpr = False

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ci_date, lineswitch_lic, i_param297, ext_char, avail_gdpr

        return {"vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9, "ci_date": ci_date, "lineswitch_lic": lineswitch_lic, "i_param297": i_param297, "ext_char": ext_char, "avail_gdpr": avail_gdpr}

    i_param297 = get_output(htpint(297))
    lineswitch_lic = get_output(htplogic(307))
    ci_date = get_output(htpdate(87))
    ext_char = get_output(htpchar(148))
    avail_gdpr = get_output(htplogic(346))
    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    return generate_output()