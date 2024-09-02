from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Gl_jouhdr

def prepare_gl_linkcomplibl():
    f_int = 0
    double_currency = False
    foreign_nr = 0
    exchg_rate = 0
    last_acctdate = None
    acct_date = None
    close_year = None
    gl_jouhdr_list_list = []
    htparam = waehrung = gl_jouhdr = None

    gl_jouhdr_list = None

    gl_jouhdr_list_list, Gl_jouhdr_list = create_model("Gl_jouhdr_list", {"refno":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, double_currency, foreign_nr, exchg_rate, last_acctdate, acct_date, close_year, gl_jouhdr_list_list, htparam, waehrung, gl_jouhdr


        nonlocal gl_jouhdr_list
        nonlocal gl_jouhdr_list_list
        return {"f_int": f_int, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "gl-jouhdr-list": gl_jouhdr_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1123)).first()
    last_acctdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    acct_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jtype == 3)).all():
        gl_jouhdr_list = Gl_jouhdr_list()
        gl_jouhdr_list_list.append(gl_jouhdr_list)

        gl_jouhdr_list.refno = gl_jouhdr.refno

    return generate_output()