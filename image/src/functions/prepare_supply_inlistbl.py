from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from models import Htparam, Bediener, L_kredit, L_lieferant, L_op, L_artikel, L_ophis

def prepare_supply_inlistbl(user_init:str, ap_recid:int):
    from_date = None
    to_date = None
    lieferant_recid = 0
    l_kredit_recid = 0
    from_supp = ""
    char1 = ""
    all_supp = False
    long_digit = False
    show_price = False
    log1 = False
    gst_flag = False
    start_endkum:int = 0
    htparam = bediener = l_kredit = l_lieferant = l_op = l_artikel = l_ophis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, lieferant_recid, l_kredit_recid, from_supp, char1, all_supp, long_digit, show_price, log1, gst_flag, start_endkum, htparam, bediener, l_kredit, l_lieferant, l_op, l_artikel, l_ophis


        return {"from_date": from_date, "to_date": to_date, "lieferant_recid": lieferant_recid, "l_kredit_recid": l_kredit_recid, "from_supp": from_supp, "char1": char1, "all_supp": all_supp, "long_digit": long_digit, "show_price": show_price, "log1": log1, "gst_flag": gst_flag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()

    if htparam.fchar != "":
        char1 = htparam.fchar
        log1 = True

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    if ap_recid != 0:

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit._recid == ap_recid)).first()

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == l_kredit.lief_nr)).first()
        from_date = l_kredit.rgdatum
        to_date = l_kredit.rgdatum
        from_supp = l_lieferant.firma
        from_supp = from_supp + ";" + l_kredit.name
        all_supp = False
        lieferant_recid = l_lieferant._recid
        l_kredit_recid = l_kredit._recid


        start_endkum = 0

        l_op = db_session.query(L_op).filter(
                (L_op.datum == l_kredit.rgdatum) &  (L_op.lief_nr == l_kredit.lief_nr)).first()

        if l_op:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.datum == l_kredit.rgdatum) &  (L_op.lief_nr == l_kredit.lief_nr)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if start_endkum == 0:
                    from_supp = from_supp + ";" + to_string(l_artikel.endkum)

                if l_artikel.endkum >= start_endkum:
                    start_endkum = l_artikel.endkum


        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                    (L_ophis.datum == l_kredit.rgdatum) &  (L_ophis.lief_nr == l_kredit.lief_nr)).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if start_endkum == 0:
                    from_supp = from_supp + ";" + to_string(l_artikel.endkum)

                if l_artikel.endkum >= start_endkum:
                    start_endkum = l_artikel.endkum


        from_supp = from_supp + ";" + to_string(start_endkum) + ";"


    else:
        from_date = get_output(htpdate(110))
        to_date = from_date

    l_lieferant = db_session.query(L_lieferant).filter(
            (func.lower(L_lieferant.firma) == "GST")).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()