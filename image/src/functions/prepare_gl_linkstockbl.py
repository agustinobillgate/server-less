from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_hauptgrp

def prepare_gl_linkstockbl(link_in:bool):
    f_int = 0
    jtype = 0
    last_acctdate = None
    acct_date = None
    close_year = None
    l_hauptgrp_list_list = []
    htparam = l_hauptgrp = None

    l_hauptgrp_list = None

    l_hauptgrp_list_list, L_hauptgrp_list = create_model("L_hauptgrp_list", {"endkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, jtype, last_acctdate, acct_date, close_year, l_hauptgrp_list_list, htparam, l_hauptgrp


        nonlocal l_hauptgrp_list
        nonlocal l_hauptgrp_list_list
        return {"f_int": f_int, "jtype": jtype, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "l-hauptgrp-list": l_hauptgrp_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    if link_in:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 269)).first()
        jtype = 6
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1035)).first()
        jtype = 3
    last_acctdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    acct_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        l_hauptgrp_list = L_hauptgrp_list()
        l_hauptgrp_list_list.append(l_hauptgrp_list)

        l_hauptgrp_list.endkum = l_hauptgrp.endkum
        l_hauptgrp_list.bezeich = l_hauptgrp.bezeich

    return generate_output()