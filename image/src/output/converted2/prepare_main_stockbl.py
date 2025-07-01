#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import Htparam, L_ophis, L_artikel

def prepare_main_stockbl():

    prepare_cache ([Htparam, L_artikel])

    p_999 = False
    p_43 = False
    p_log1080 = False
    p_int1080 = 0
    p_2000 = False
    p_269 = None
    p_1035 = None
    p_224 = None
    p_221 = None
    p_852 = 0
    avail_l_ophis = False
    htparam = l_ophis = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_999, p_43, p_log1080, p_int1080, p_2000, p_269, p_1035, p_224, p_221, p_852, avail_l_ophis, htparam, l_ophis, l_artikel

        return {"p_999": p_999, "p_43": p_43, "p_log1080": p_log1080, "p_int1080": p_int1080, "p_2000": p_2000, "p_269": p_269, "p_1035": p_1035, "p_224": p_224, "p_221": p_221, "p_852": p_852, "avail_l_ophis": avail_l_ophis}

    def add_sunits():

        nonlocal p_999, p_43, p_log1080, p_int1080, p_2000, p_269, p_1035, p_224, p_221, p_852, avail_l_ophis, htparam, l_ophis, l_artikel

        sbuff = None
        Sbuff =  create_buffer("Sbuff",L_artikel)

        l_artikel = db_session.query(L_artikel).first()
        while None != l_artikel:

            if not matches(l_artikel.herkunft,r"*;*"):

                sbuff = get_cache (L_artikel, {"_recid": [(eq, l_artikel._recid)]})
                sbuff.herkunft = sbuff.herkunft + ";;"
                pass

            curr_recid = l_artikel._recid
            l_artikel = db_session.query(L_artikel).filter(L_artikel._recid > curr_recid).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 999)]})
    p_999 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    p_43 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1080)]})
    p_log1080 = htparam.flogical
    p_int1080 = htparam.paramgruppe
    p_2000 = get_output(htplogic(2000))
    p_269 = get_output(htpdate(269))
    p_1035 = get_output(htpdate(1035))
    p_224 = get_output(htpdate(224))
    p_221 = get_output(htpdate(221))
    p_852 = get_output(htpint(852))

    l_ophis = db_session.query(L_ophis).first()

    if l_ophis:
        avail_l_ophis = True

    l_artikel = db_session.query(L_artikel).first()

    if l_artikel and not matches(l_artikel.herkunft,r"*;*"):
        add_sunits()

    return generate_output()