#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Bediener, L_kredit, L_lieferant, L_op, L_artikel, L_ophis, Queasy

def prepare_supply_inlist_webbl(user_init:string, ap_recid:int):

    prepare_cache ([Htparam, Bediener, L_kredit, L_lieferant, L_artikel])

    from_date = None
    to_date = None
    lieferant_recid = 0
    l_kredit_recid = 0
    from_supp = ""
    char1 = ""
    all_supp = True
    long_digit = False
    show_price = False
    log1 = False
    gst_flag = False
    avail_addvat = False
    start_endkum:int = 0
    htparam = bediener = l_kredit = l_lieferant = l_op = l_artikel = l_ophis = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, lieferant_recid, l_kredit_recid, from_supp, char1, all_supp, long_digit, show_price, log1, gst_flag, avail_addvat, start_endkum, htparam, bediener, l_kredit, l_lieferant, l_op, l_artikel, l_ophis, queasy
        nonlocal user_init, ap_recid

        return {"from_date": from_date, "to_date": to_date, "lieferant_recid": lieferant_recid, "l_kredit_recid": l_kredit_recid, "from_supp": from_supp, "char1": char1, "all_supp": all_supp, "long_digit": long_digit, "show_price": show_price, "log1": log1, "gst_flag": gst_flag, "avail_addvat": avail_addvat}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam.fchar != "":
        char1 = htparam.fchar
        log1 = True

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    if ap_recid != 0:

        l_kredit = get_cache (L_kredit, {"_recid": [(eq, ap_recid)]})

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_kredit.lief_nr)]})
        from_date = l_kredit.rgdatum
        to_date = l_kredit.rgdatum
        from_supp = l_lieferant.firma
        from_supp = from_supp + ";" + l_kredit.name
        all_supp = False
        lieferant_recid = l_lieferant._recid
        l_kredit_recid = l_kredit._recid


        start_endkum = 0

        l_op = get_cache (L_op, {"datum": [(eq, l_kredit.rgdatum)],"lief_nr": [(eq, l_kredit.lief_nr)]})

        if l_op:

            l_op_obj_list = {}
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum == l_kredit.rgdatum) & (L_op.lief_nr == l_kredit.lief_nr)).order_by(L_artikel.endkum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if start_endkum == 0:
                    from_supp = from_supp + ";" + to_string(l_artikel.endkum)

                if l_artikel.endkum >= start_endkum:
                    start_endkum = l_artikel.endkum


        else:

            l_ophis_obj_list = {}
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.datum == l_kredit.rgdatum) & (L_ophis.lief_nr == l_kredit.lief_nr)).order_by(L_artikel.endkum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if start_endkum == 0:
                    from_supp = from_supp + ";" + to_string(l_artikel.endkum)

                if l_artikel.endkum >= start_endkum:
                    start_endkum = l_artikel.endkum


        from_supp = from_supp + ";" + to_string(start_endkum) + ";"


    else:
        from_date = get_output(htpdate(110))
        to_date = from_date

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    queasy = get_cache (Queasy, {"key": [(eq, 303)]})

    if queasy:
        avail_addvat = True

    return generate_output()