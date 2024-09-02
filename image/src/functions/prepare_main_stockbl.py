from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from functions.htpint import htpint
import re
from models import Htparam, L_ophis, L_artikel

def prepare_main_stockbl():
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

    sbuff = None

    Sbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_999, p_43, p_log1080, p_int1080, p_2000, p_269, p_1035, p_224, p_221, p_852, avail_l_ophis, htparam, l_ophis, l_artikel
        nonlocal sbuff


        nonlocal sbuff
        return {"p_999": p_999, "p_43": p_43, "p_log1080": p_log1080, "p_int1080": p_int1080, "p_2000": p_2000, "p_269": p_269, "p_1035": p_1035, "p_224": p_224, "p_221": p_221, "p_852": p_852, "avail_l_ophis": avail_l_ophis}

    def add_sunits():

        nonlocal p_999, p_43, p_log1080, p_int1080, p_2000, p_269, p_1035, p_224, p_221, p_852, avail_l_ophis, htparam, l_ophis, l_artikel
        nonlocal sbuff


        nonlocal sbuff


        Sbuff = L_artikel

        l_artikel = db_session.query(L_artikel).first()
        while None != l_artikel:

            if not re.match(".*;.*",l_artikel.herkunft):

                sbuff = db_session.query(Sbuff).filter(
                        (Sbuff._recid == l_artikel._recid)).first()
                sbuff.herkunft = sbuff.herkunft + ";;"

                sbuff = db_session.query(Sbuff).first()

            l_artikel = db_session.query(L_artikel).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 999)).first()
    p_999 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    p_43 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1080)).first()
    p_log1080 = htparam.flogical
    p_int1080 = htparam.paramgr
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

    if l_artikel and not re.match(".*;.*",l_artikel.herkunft):
        add_sunits()

    return generate_output()