#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_kredit, L_artikel, L_untergrup, Gl_acct, Gl_jouhdr, Gl_journal, L_op, Htparam, L_bestand

def supply_inlist_btn_delete_all_by_lscheinnr_webbl(pvilanguage:int, str_list_billdate:date, str_list_lief_nr:int, str_list_docu_nr:string, str_list_lscheinnr:string, str_list_l_recid:int, str_list_artnr:int):

    prepare_cache ([L_artikel, L_untergrup, Gl_acct, Gl_jouhdr, L_op, Htparam, L_bestand])

    may_delete = False
    msg_str = ""
    msg_str1 = ""
    msg_str2 = ""
    l_op_not_eligible_data = []
    art_fibu:string = ""
    lvcarea:string = "supply-inlist"
    l_kredit = l_artikel = l_untergrup = gl_acct = gl_jouhdr = gl_journal = l_op = htparam = l_bestand = None

    l_op_not_eligible = None

    l_op_not_eligible_data, L_op_not_eligible = create_model("L_op_not_eligible", {"lscheinnr":string, "artnr":int, "bezeich":string, "reason":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal may_delete, msg_str, msg_str1, msg_str2, l_op_not_eligible_data, art_fibu, lvcarea, l_kredit, l_artikel, l_untergrup, gl_acct, gl_jouhdr, gl_journal, l_op, htparam, l_bestand
        nonlocal pvilanguage, str_list_billdate, str_list_lief_nr, str_list_docu_nr, str_list_lscheinnr, str_list_l_recid, str_list_artnr


        nonlocal l_op_not_eligible
        nonlocal l_op_not_eligible_data

        return {"may_delete": may_delete, "msg_str": msg_str, "msg_str1": msg_str1, "msg_str2": msg_str2, "l-op-not-eligible": l_op_not_eligible_data}

    def check_onhand_after_cancel_receiving():

        nonlocal may_delete, msg_str, msg_str1, msg_str2, l_op_not_eligible_data, art_fibu, lvcarea, l_kredit, l_artikel, l_untergrup, gl_acct, gl_jouhdr, gl_journal, l_op, htparam, l_bestand
        nonlocal pvilanguage, str_list_billdate, str_list_lief_nr, str_list_docu_nr, str_list_lscheinnr, str_list_l_recid, str_list_artnr


        nonlocal l_op_not_eligible
        nonlocal l_op_not_eligible_data

        f_endkum:int = 0
        b_endkum:int = 0
        m_endkum:int = 0
        billdate:date = None
        fb_closedate:date = None
        m_closedate:date = None
        qty:Decimal = to_decimal("0.0")
        trf_gl:date = None

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.lscheinnr, l_op.artnr, l_op.lager_nr, l_op.anzahl, l_op._recid, l_artikel.bezeich, l_artikel.endkum, l_artikel.zwkum, l_artikel.fibukonto, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.artnr, L_op.lager_nr, L_op.anzahl, L_op._recid, L_artikel.bezeich, L_artikel.endkum, L_artikel.zwkum, L_artikel.fibukonto, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.lief_nr > 0) & (L_op.lscheinnr == (str_list_lscheinnr).lower()) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op._recid == 0:
                msg_str1 = msg_str1 + chr_unicode(2) + translateExtended ("Old record(s) can not be deleted,", lvcarea, "") + translateExtended ("Cancel Receiving not possible.", lvcarea, "")
                l_op_not_eligible = L_op_not_eligible()
                l_op_not_eligible_data.append(l_op_not_eligible)

                l_op_not_eligible.lscheinnr = l_op.lscheinnr
                l_op_not_eligible.artnr = l_op.artnr
                l_op_not_eligible.bezeich = l_artikel.bezeich
                l_op_not_eligible.reason = msg_str1


                continue

            if l_op.flag:
                continue

            htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

            if htparam:
                trf_gl = htparam.fdate

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

            if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and str_list_billdate > fb_closedate) or (l_artikel.endkum >= m_endkum and str_list_billdate > m_closedate):
                continue

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, l_op.lager_nr)]})
            qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)

            if qty < 0:
                msg_str1 = msg_str1 + chr_unicode(2) + translateExtended ("Onhand qty in Store ", lvcarea, "") + to_string(l_op.lager_nr, "99") + " " + translateExtended ("would become (-) =", lvcarea, "") + " " + trim(to_string(qty, "->,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("Cancel Receiving not possible.", lvcarea, "")
                l_op_not_eligible = L_op_not_eligible()
                l_op_not_eligible_data.append(l_op_not_eligible)

                l_op_not_eligible.lscheinnr = l_op.lscheinnr
                l_op_not_eligible.artnr = l_op.artnr
                l_op_not_eligible.bezeich = l_artikel.bezeich
                l_op_not_eligible.reason = msg_str1


                continue

            if str_list_billdate <= trf_gl:
                msg_str1 = msg_str1 + chr_unicode(2) + translateExtended ("Receiving have been transfered to the G/L, ", lvcarea, "") + translateExtended ("cancel Receiving not possible.", lvcarea, "")
                l_op_not_eligible = L_op_not_eligible()
                l_op_not_eligible_data.append(l_op_not_eligible)

                l_op_not_eligible.lscheinnr = l_op.lscheinnr
                l_op_not_eligible.artnr = l_op.artnr
                l_op_not_eligible.bezeich = l_artikel.bezeich
                l_op_not_eligible.reason = msg_str1

        l_op_not_eligible = query(l_op_not_eligible_data, first=True)

        if not l_op_not_eligible:
            may_delete = True


    l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, str_list_lief_nr)],"name": [(eq, str_list_docu_nr)],"lscheinnr": [(eq, str_list_lscheinnr)],"opart": [(ge, 1)],"zahlkonto": [(gt, 0)]})

    if l_kredit:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The A/P Payment record found.", lvcarea, "") + chr_unicode(10) + translateExtended ("Cancel Receiving is no longer possible.", lvcarea, "")

        return generate_output()

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, str_list_artnr)]})

    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

    if not gl_acct:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

    if gl_acct:
        art_fibu = gl_acct.fibukonto

    if art_fibu != "":

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum == str_list_billdate) & (Gl_jouhdr.jtype == 6) & (matches(Gl_jouhdr.refno,"RCV*"))).order_by(Gl_jouhdr._recid).all():

            gl_journal = get_cache (Gl_journal, {"jnr": [(eq, gl_jouhdr.jnr)],"fibukonto": [(eq, art_fibu)]})

            if gl_journal:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Stock receiving records have been transfered to the G/L.", lvcarea, "") + chr_unicode(10) + translateExtended ("Cancel Receiving is no longer possible.", lvcarea, "")
                break

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum == str_list_billdate) & (Gl_jouhdr.jtype == 3) & (matches(Gl_jouhdr.refno,"OUT*"))).order_by(Gl_jouhdr._recid).all():

            gl_journal = get_cache (Gl_journal, {"jnr": [(eq, gl_jouhdr.jnr)],"fibukonto": [(eq, art_fibu)]})

            if gl_journal:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Stock outgoing records have been transfered to the G/L.", lvcarea, "") + chr_unicode(10) + translateExtended ("Cancel outgoing is no longer possible.", lvcarea, "")
                break

    if msg_str != "":

        return generate_output()
    check_onhand_after_cancel_receiving()

    if not may_delete:

        return generate_output()

    return generate_output()