from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Htparam, Akt_line

def prepare_gcf_listbl(user_init:str):
    sorttype_fchar0 = ""
    sorttype_fchar1 = ""
    sorttype_fchar2 = ""
    ext_char = ""
    htl_city = ""
    curr_htl_city = ""
    vhp_lite = False
    vhp_multi = False
    rest_lic = False
    long_digit = False
    aktlist_flag = False
    ci_date = None
    vipnr1 = 0
    vipnr2 = 0
    vipnr3 = 0
    vipnr4 = 0
    vipnr5 = 0
    vipnr6 = 0
    vipnr7 = 0
    vipnr8 = 0
    vipnr9 = 0
    paramtext = htparam = akt_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sorttype_fchar0, sorttype_fchar1, sorttype_fchar2, ext_char, htl_city, curr_htl_city, vhp_lite, vhp_multi, rest_lic, long_digit, aktlist_flag, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, paramtext, htparam, akt_line


        return {"sorttype_fchar0": sorttype_fchar0, "sorttype_fchar1": sorttype_fchar1, "sorttype_fchar2": sorttype_fchar2, "ext_char": ext_char, "htl_city": htl_city, "curr_htl_city": curr_htl_city, "vhp_lite": vhp_lite, "vhp_multi": vhp_multi, "rest_lic": rest_lic, "long_digit": long_digit, "aktlist_flag": aktlist_flag, "ci_date": ci_date, "vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9}

    def get_vipnr():

        nonlocal sorttype_fchar0, sorttype_fchar1, sorttype_fchar2, ext_char, htl_city, curr_htl_city, vhp_lite, vhp_multi, rest_lic, long_digit, aktlist_flag, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, paramtext, htparam, akt_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 700)).first()

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 701)).first()

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 702)).first()

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 703)).first()

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 704)).first()

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 705)).first()

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 706)).first()

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 707)).first()

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 708)).first()

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 203)).first()
    curr_htl_city = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 796)).first()

    if htparam.fchar != "":
        sorttype_fchar0 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 797)).first()

    if htparam.fchar != "":
        sorttype_fchar1 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 798)).first()

    if htparam.fchar != "":
        sorttype_fchar2 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1015)).first()
    vhp_lite = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 996)).first()
    vhp_multi = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 990)).first()
    rest_lic = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 148)).first()
    ext_char = htparam.fchar
    get_vipnr()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1355)).first()

    if htparam.flogical :
        ci_date = get_current_date()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1002)).first()

    if htparam.flogical:

        akt_line = db_session.query(Akt_line).filter(
                (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= (ci_date - 1)) &  (Akt_line.datum <= ci_date)).first()
        aktlist_flag = None != akt_line

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 203)).first()
    htl_city = paramtext.ptexte

    return generate_output()