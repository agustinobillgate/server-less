#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_op, Htparam, L_bestand

def po_invoice_check_qtybl(pvilanguage:int, qty:Decimal, s_list_s_recid:int, s_list_artnr:int):

    prepare_cache ([L_artikel, L_op, Htparam, L_bestand])

    msg_str = ""
    may_chg = True
    lvcarea:string = "po-invoice"
    l_artikel = l_op = htparam = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, may_chg, lvcarea, l_artikel, l_op, htparam, l_bestand
        nonlocal pvilanguage, qty, s_list_s_recid, s_list_artnr

        return {"msg_str": msg_str, "may_chg": may_chg}

    def check_qty():

        nonlocal msg_str, may_chg, lvcarea, l_artikel, l_op, htparam, l_bestand
        nonlocal pvilanguage, qty, s_list_s_recid, s_list_artnr

        f_endkum:int = 0
        b_endkum:int = 0
        m_endkum:int = 0
        billdate:date = None
        fb_closedate:date = None
        m_closedate:date = None
        qty1:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        l_op = get_cache (L_op, {"_recid": [(eq, s_list_s_recid)]})

        if l_op.flag:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        b_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
        m_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        fb_closedate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        m_closedate = htparam.fdate

        l_art = get_cache (L_artikel, {"artnr": [(eq, s_list_artnr)]})

        if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and l_op.datum > fb_closedate) or (l_art.endkum >= m_endkum and l_op.datum > m_closedate):

            return

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, l_op.lager_nr)]})
        qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang) + to_decimal(qty) - to_decimal(l_op.anzahl)

        if qty1 < 0:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Onhand qty in Store ", lvcarea, "") + to_string(l_op.lager_nr, "99") + " " + translateExtended ("would become negative", lvcarea, "") + " = " + trim(to_string(qty1, "->>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("The entered qty is therefore not possible.", lvcarea, "")
            may_chg = False


    check_qty()

    return generate_output()