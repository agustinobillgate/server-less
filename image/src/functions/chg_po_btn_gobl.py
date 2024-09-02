from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order, L_orderhdr, Bediener, Res_history

def chg_po_btn_gobl(t_l_orderhdr:[T_l_orderhdr], s_order:[S_order], disc_list:[Disc_list], lief_nr:int, pr:str, tp_bediener_username:str):
    remark:str = ""
    globaldisc:decimal = 0
    logstring:str = ""
    l_order = l_orderhdr = bediener = res_history = None

    s_order = disc_list = t_l_orderhdr = None

    s_order_list, S_order = create_model_like(L_order, {"rec_id":int, "lief_einheit":decimal})
    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_val":decimal, "disc2_val":decimal, "vat_val":decimal})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal remark, globaldisc, logstring, l_order, l_orderhdr, bediener, res_history


        nonlocal s_order, disc_list, t_l_orderhdr
        nonlocal s_order_list, disc_list_list, t_l_orderhdr_list
        return {}

    def create_log(aend_str:str):

        nonlocal remark, globaldisc, logstring, l_order, l_orderhdr, bediener, res_history


        nonlocal s_order, disc_list, t_l_orderhdr
        nonlocal s_order_list, disc_list_list, t_l_orderhdr_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (tp_bediener_username).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Purchase Order"
        res_history.aenderung = aend_str

        res_history = db_session.query(Res_history).first()


    t_l_orderhdr = query(t_l_orderhdr_list, first=True)

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == t_L_orderhdr.rec_id)).first()
    remark = entry(0, t_l_orderhdr.lief_fax[2], chr(2))

    if num_entries(t_l_orderhdr.lief_fax[2], chr(2)) > 1:
        globaldisc = decimal.Decimal(entry(1, t_l_orderhdr.lief_fax[2], chr(2))) / 100

    if l_orderhdr.lief_nr != t_l_orderhdr.lief_nr:
        logstring = "[CHG ORDERHDR]DOC NO: " + t_l_orderhdr.docu_nr + " Supplier Number Changed From: " + to_string(l_orderhdr.lief_nr) + " To: " + to_string(t_l_orderhdr.lief_nr)
        create_log(logstring)

    if l_orderhdr.lieferdatum != t_l_orderhdr.lieferdatum:
        logstring = "[CHG ORDERHDR]DOC NO: " + t_l_orderhdr.docu_nr + " Delivery Date Changed From: " + to_string(l_orderhdr.lieferdatum) + " To: " + to_string(t_l_orderhdr.lieferdatum)
        create_log(logstring)

    if l_orderhdr.bestellart != t_l_orderhdr.bestellart:
        logstring = "[CHG ORDERHDR]DOC NO: " + t_l_orderhdr.docu_nr + " Order Type Changed From: " + to_string(l_orderhdr.bestellart) + " To: " + to_string(t_l_orderhdr.bestellart)
        create_log(logstring)

    if l_orderhdr.angebot_lief[0] != t_l_orderhdr.angebot_lief[0]:
        logstring = "[CHG ORDERHDR]DOC NO: " + t_l_orderhdr.docu_nr + " Department Changed From: " + to_string(l_orderhdr.angebot_lief[0]) + " To: " + to_string(t_l_orderhdr.angebot_lief[0])
        create_log(logstring)

    if l_orderhdr.lief_fax[1] != t_l_orderhdr.lief_fax[1]:
        logstring = "[CHG ORDERHDR]DOC NO: " + t_l_orderhdr.docu_nr + " Credit Term Changed From: " + to_string(l_orderhdr.lief_fax[1]) + " To: " + to_string(t_l_orderhdr.lief_fax[1])
        create_log(logstring)

    if l_orderhdr.lief_fax[2] != (remark).lower() :
        logstring = "[CHG ORDERHDR]DOC NO: " + t_l_orderhdr.docu_nr + " Remarks Changed From: " + to_string(l_orderhdr.lief_fax[2]) + " To: " + to_string(remark)
        create_log(logstring)

    l_orderhdr = db_session.query(L_orderhdr).first()
    l_orderhdr.lief_nr = t_l_orderhdr.lief_nr
    l_orderhdr.lieferdatum = t_l_orderhdr.lieferdatum
    l_orderhdr.bestellart = t_l_orderhdr.bestellart
    l_orderhdr.angebot_lief[0] = t_l_orderhdr.angebot_lief[0]
    l_orderhdr.angebot_lief[1] = t_l_orderhdr.angebot_lief[1]
    l_orderhdr.lief_fax[1] = t_l_orderhdr.lief_fax[1]
    l_orderhdr.lief_fax[2] = remark

    l_orderhdr = db_session.query(L_orderhdr).first()

    l_order = db_session.query(L_order).filter(
            (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.pos == 0)).first()

    if l_order.lief_nr != lief_nr:
        logstring = "[CHG LORDER]DOC NO: " + t_l_orderhdr.docu_nr + " Supplier Number Changed From: " + to_string(l_order.lief_nr) + " To: " + to_string(lief_nr)
        create_log(logstring)

    if l_orderhdr.lief_fax[0] != (pr).lower() :
        logstring = "[CHG LORDER]DOC NO: " + t_l_orderhdr.docu_nr + " pr Number Changed From: " + to_string(l_orderhdr.lief_fax[0]) + " To: " + to_string(pr)
        create_log(logstring)

    if l_order.warenwert != globaldisc:
        logstring = "[CHG LORDER]DOC NO: " + t_l_orderhdr.docu_nr + " GLobal Discount Changed From: " + to_string(l_order.warenwert) + " To: " + to_string(globaldisc)
        create_log(logstring)
    l_order.lief_nr = lief_nr
    l_order.lief_fax[0] = pr
    l_order.warenwert = globaldisc

    l_order = db_session.query(L_order).first()

    for s_order in query(s_order_list):

        disc_list = query(disc_list_list, filters=(lambda disc_list :disc_list.l_recid == s_order.rec_id), first=True)

        l_order = db_session.query(L_order).filter(
                (L_order._recid == s_order.rec_id)).first()

        if l_order.lief_nr != lief_nr:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " Supplier Number Changed From: " + to_string(l_order.lief_nr) + " To: " + to_string(lief_nr)
            create_log(logstring)

        if l_order.lief_fax[0] != (pr).lower() :
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " pr Number Changed From: " + to_string(l_order.lief_fax[0]) + " To: " + to_string(pr)
            create_log(logstring)

        if l_order.lief_fax[1] != (tp_bediener_username).lower() :
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " Username Changed From: " + to_string(l_order.lief_fax[1]) + " To: " + to_string(tp_bediener_username)
            create_log(logstring)

        if l_order.anzahl != s_order.anzahl:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " QTY Changed From: " + to_string(l_order.anzahl) + " To: " + to_string(s_order.anzahl)
            create_log(logstring)

        if l_order.einzelpreis != s_order.einzelpreis:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " Nett Price Changed From: " + to_string(l_order.einzelpreis) + " To: " + to_string(s_order.einzelpreis)
            create_log(logstring)

        if l_order.besteller != s_order.besteller:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " remark Changed From: " + to_string(l_order.besteller) + " To: " + to_string(s_order.besteller)
            create_log(logstring)

        if l_order.quality != s_order.quality:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " Disc Changed From: " + to_string(l_order.quality) + " To: " + to_string(s_order.quality)
            create_log(logstring)

        if l_order.warenwert != s_order.warenwert:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " Net Amount Changed From: " + to_string(l_order.warenwert) + " To: " + to_string(s_order.warenwert)
            create_log(logstring)

        if l_order.stornogrund != s_order.stornogrund:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " Article No: " + to_string(s_order.artnr) + " AcctNo Changed From: " + to_string(l_order.stornogrund) + " To: " + to_string(s_order.stornogrund)
            create_log(logstring)
        l_order.lief_nr = lief_nr
        l_order.lieferdatum = get_current_date()
        l_order.lief_fax[0] = pr
        l_order.lief_fax[1] = tp_bediener_username
        l_order.anzahl = s_order.anzahl
        l_order.einzelpreis = s_order.einzelpreis
        l_order.besteller = s_order.besteller
        l_order.quality = s_order.quality
        l_order.warenwert = s_order.warenwert
        l_order.stornogrund = s_order.stornogrund

        l_order = db_session.query(L_order).first()

    return generate_output()