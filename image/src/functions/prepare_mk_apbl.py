from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_acct, L_lieferant

def prepare_mk_apbl():
    closed_date = None
    rgdatum = None
    p_2000 = False
    av_gl_acct = False
    ap_acct = ""
    ap_other = ""
    gst_flag = False
    htparam = gl_acct = l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal closed_date, rgdatum, p_2000, av_gl_acct, ap_acct, ap_other, gst_flag, htparam, gl_acct, l_lieferant


        return {"closed_date": closed_date, "rgdatum": rgdatum, "p_2000": p_2000, "av_gl_acct": av_gl_acct, "ap_acct": ap_acct, "ap_other": ap_other, "gst_flag": gst_flag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    closed_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    rgdatum = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2000)).first()
    p_2000 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 986)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == htparam.fchar)).first()

    if not gl_acct:
        av_gl_acct = False
    else:
        av_gl_acct = True
        ap_acct = gl_acct.fibukonto

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 395)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == htparam.fchar)).first()

    if gl_acct:
        ap_other = gl_acct.fibukonto
    else:
        ap_other = ap_acct

    l_lieferant = db_session.query(L_lieferant).filter(
            (func.lower(L_lieferant.firma) == "GST")).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()