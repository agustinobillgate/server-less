from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import L_ophis, Htparam

def select_invclosebl():
    fb_close_date = None
    mat_close_date = None
    last_journ_transgl = None
    flag_fb = False
    flag_mat = False
    l_ophis = htparam = None

    ophis_fnb = ophis_mat = None

    Ophis_fnb = L_ophis
    Ophis_mat = L_ophis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_close_date, mat_close_date, last_journ_transgl, flag_fb, flag_mat, l_ophis, htparam
        nonlocal ophis_fnb, ophis_mat


        nonlocal ophis_fnb, ophis_mat
        return {"fb_close_date": fb_close_date, "mat_close_date": mat_close_date, "last_journ_transgl": last_journ_transgl, "flag_fb": flag_fb, "flag_mat": flag_mat}

    fb_close_date = get_output(htpdate(224))
    mat_close_date = get_output(htpdate(221))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1035)).first()
    last_journ_transgl = htparam.fdate

    if fb_close_date == last_journ_transgl:

        ophis_fnb = db_session.query(Ophis_fnb).filter(
                (Ophis_fnb.op_art == 1) &  (get_month(Ophis_fnb.datum) == get_month(fb_close_date)) &  (get_year(Ophis_fnb.datum) == get_year(fb_close_date))).first()

        if ophis_fnb:
            flag_fb = False

        elif not ophis_fnb:
            flag_fb = True
    else:
        flag_fb = False

    if mat_close_date == last_journ_transgl:

        ophis_mat = db_session.query(Ophis_mat).filter(
                (Ophis_mat.op_art == 3) &  (get_month(Ophis_mat.datum) == get_month(mat_close_date)) &  (get_year(Ophis_mat.datum) == get_year(mat_close_date))).first()

        if ophis_mat:
            flag_mat = False

        elif not ophis_mat:
            flag_mat = True
    else:
        flag_mat = False

    return generate_output()