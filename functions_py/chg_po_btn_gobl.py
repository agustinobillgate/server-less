#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_order, L_orderhdr, Bediener, Res_history
from sqlalchemy.orm.attributes import flag_modified

t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
s_order_data, S_order = create_model_like(L_order, {"rec_id":int, "lief_einheit":Decimal})
disc_list_data, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "disc_val":Decimal, "disc2_val":Decimal, "vat_val":Decimal})

def chg_po_btn_gobl(t_l_orderhdr_data:[T_l_orderhdr], s_order_data:[S_order], disc_list_data:[Disc_list], lief_nr:int, pr:string, tp_bediener_username:string):

    prepare_cache ([L_order, L_orderhdr, Bediener, Res_history])

    remark:string = ""
    globaldisc:Decimal = to_decimal("0.0")
    logstring:string = ""
    l_order = l_orderhdr = bediener = res_history = None

    s_order = disc_list = t_l_orderhdr = None

    db_session = local_storage.db_session
    pr = pr.strip()
    tp_bediener_username = tp_bediener_username.strip()

    def generate_output():
        nonlocal remark, globaldisc, logstring, l_order, l_orderhdr, bediener, res_history
        nonlocal lief_nr, pr, tp_bediener_username


        nonlocal s_order, disc_list, t_l_orderhdr

        return {}

    def create_log(aend_str:string):

        nonlocal remark, globaldisc, logstring, l_order, l_orderhdr, bediener, res_history
        nonlocal lief_nr, pr, tp_bediener_username


        nonlocal s_order, disc_list, t_l_orderhdr

        bediener = get_cache (Bediener, {"username": [(eq, tp_bediener_username)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Purchase Order"
        res_history.aenderung = aend_str



    t_l_orderhdr = query(t_l_orderhdr_data, first=True)

    # l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, t_l_orderhdr.rec_id)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr._recid == t_l_orderhdr.rec_id)).with_for_update().first()
    remark = entry(0, t_l_orderhdr.lief_fax[2], chr_unicode(2))

    if num_entries(t_l_orderhdr.lief_fax[2], chr_unicode(2)) > 1:
        globaldisc =  to_decimal(to_decimal(entry(1 , t_l_orderhdr.lief_fax[2] , chr_unicode(2)))) / to_decimal("100")

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
    pass
    l_orderhdr.lief_nr = t_l_orderhdr.lief_nr
    l_orderhdr.lieferdatum = t_l_orderhdr.lieferdatum
    l_orderhdr.bestellart = t_l_orderhdr.bestellart
    l_orderhdr.angebot_lief[0] = t_l_orderhdr.angebot_lief[0]
    l_orderhdr.angebot_lief[1] = t_l_orderhdr.angebot_lief[1]
    l_orderhdr.lief_fax[1] = t_l_orderhdr.lief_fax[1]
    l_orderhdr.lief_fax[2] = remark
    l_orderhdr.gedruckt = t_l_orderhdr.gedruckt
    flag_modified(l_orderhdr, "angebot_lief")
    flag_modified(l_orderhdr, "lief_fax")


    pass

    # l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)]})
    l_order = db_session.query(L_order).filter(
             (L_order.docu_nr == l_orderhdr.docu_nr) &
             (L_order.pos == 0)).with_for_update().first()  

    if l_order.lief_nr != lief_nr:
        logstring = "[CHG LORDER]DOC NO: " + t_l_orderhdr.docu_nr + " Supplier Number Changed From: " + to_string(l_order.lief_nr) + " To: " + to_string(lief_nr)
        create_log(logstring)

    if l_orderhdr.lief_fax[0] != (pr).lower() :
        logstring = "[CHG LORDER]DOC NO: " + t_l_orderhdr.docu_nr + " pr Number Changed From: " + to_string(l_orderhdr.lief_fax[0]) + " To: " + to_string(pr)
        create_log(logstring)
    pass

    if l_order.warenwert != globaldisc:
        logstring = "[CHG LORDER]DOC NO: " + t_l_orderhdr.docu_nr + " GLobal Discount Changed From: " + to_string(l_order.warenwert) + " To: " + to_string(globaldisc)
        create_log(logstring)
    l_order.lief_nr = lief_nr
    l_order.lief_fax[0] = pr
    l_order.warenwert =  to_decimal(globaldisc)
    flag_modified(l_order, "lief_fax")


    pass

    for s_order in query(s_order_data):

        disc_list = query(disc_list_data, filters=(lambda disc_list: disc_list.l_recid == s_order.rec_id), first=True)

        # l_order = get_cache (L_order, {"_recid": [(eq, s_order.rec_id)]})
        l_order = db_session.query(L_order).filter(
                 (L_order._recid == s_order.rec_id)).with_for_update().first()

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
        l_order.anzahl =  to_decimal(s_order.anzahl)
        l_order.einzelpreis =  to_decimal(s_order.einzelpreis)
        l_order.besteller = s_order.besteller
        l_order.quality = s_order.quality
        l_order.warenwert =  to_decimal(s_order.warenwert)
        l_order.stornogrund = s_order.stornogrund
        flag_modified(l_order, "lief_fax")


    return generate_output()