#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_lieferant, Guestbook, L_orderhdr, Bediener, Res_history

s_list_list, S_list = create_model_like(L_order, {"curr":string, "exrate":Decimal, "s_recid":int, "amount":Decimal, "supp1":int, "supp2":int, "supp3":int, "suppn1":string, "suppn2":string, "suppn3":string, "supps":string, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "curr1":string, "curr2":string, "curr3":string, "fdate1":date, "fdate2":date, "fdate3":date, "tdate1":date, "tdate2":date, "tdate3":date, "desc_coa":string, "last_pprice":Decimal, "avg_pprice":Decimal})
tt_app_id_list, Tt_app_id = create_model("Tt_app_id", {"i_counter":int, "app_id":string})
t_guestbook_list, T_guestbook = create_model_like(Guestbook)

def chg_pr_save_s_list_11bl(s_list_list:[S_list], tt_app_id_list:[Tt_app_id], t_guestbook_list:[T_guestbook], rec_id:int, deptnr:int, comments_screen_value:string, rej_id:string, lieferdatum:date, rej_flag:bool, user_init:string, docu_nr:string):

    prepare_cache ([L_orderhdr, Bediener, Res_history])

    sfdate1:string = ""
    sfdate2:string = ""
    sfdate3:string = ""
    stdate1:string = ""
    stdate2:string = ""
    stdate3:string = ""
    app_id:List[string] = create_empty_list(4,"")
    l_order = l_lieferant = guestbook = l_orderhdr = bediener = res_history = None

    s_list = tt_app_id = t_l_order = t_l_lieferant = t_guestbook = sbuff = None

    t_l_order_list, T_l_order = create_model_like(L_order)
    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)

    Sbuff = S_list
    sbuff_list = s_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sfdate1, sfdate2, sfdate3, stdate1, stdate2, stdate3, app_id, l_order, l_lieferant, guestbook, l_orderhdr, bediener, res_history
        nonlocal rec_id, deptnr, comments_screen_value, rej_id, lieferdatum, rej_flag, user_init, docu_nr
        nonlocal sbuff


        nonlocal s_list, tt_app_id, t_l_order, t_l_lieferant, t_guestbook, sbuff
        nonlocal t_l_order_list, t_l_lieferant_list

        return {}

    for tt_app_id in query(tt_app_id_list):
        app_id[tt_app_id.i_counter - 1] = tt_app_id.app_id

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    l_orderhdr.lief_fax[2] = comments_screen_value
    l_orderhdr.lieferdatum = lieferdatum
    l_orderhdr.angebot_lief[0] = deptnr
    l_orderhdr.lief_fax[1] = app_id[0] + ";" + app_id[1] + ";" + app_id[2] + ";" + app_id[3] + rej_id
    pass

    for t_guestbook in query(t_guestbook_list, filters=(lambda t_guestbook: t_guestbook.reserve_char[0] == ("$pr").lower()  and t_guestbook.reserve_char[1] == (docu_nr).lower())):

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, t_guestbook.gastnr)],"reserve_char[0]": [(eq, t_guestbook.reserve_char[0])],"reserve_char[1]": [(eq, t_guestbook.reserve_char[1])]})

        if guestbook:
            buffer_copy(t_guestbook, guestbook)
            pass
        else:
            guestbook = Guestbook()
            db_session.add(guestbook)

            buffer_copy(t_guestbook, guestbook)
            pass

    for sbuff in query(sbuff_list):

        l_order = get_cache (L_order, {"_recid": [(eq, sbuff.s_recid)]})

        s_list = query(s_list_list, filters=(lambda s_list: s_list.s_recid == to_int(l_order._recid)), first=True)
        buffer_copy(l_order, t_l_order)
        l_order.einzelpreis =  to_decimal(s_list.einzelpreis)
        l_order.anzahl =  to_decimal(s_list.anzahl)
        l_order.stornogrund = s_list.stornogrund
        l_order.besteller = s_list.besteller
        l_order.angebot_lief[2] = s_list.angebot_lief[2]
        l_order.angebot_lief[1] = s_list.angebot_lief[1]
        l_order.warenwert =  to_decimal(s_list.amount)

        if s_list.fdate1 == None:
            sfdate1 = ""
            stdate1 = ""


        else:
            sfdate1 = to_string(s_list.fdate1)
            stdate1 = to_string(s_list.tdate1)

        if s_list.fdate2 == None:
            sfdate2 = ""
            stdate2 = ""


        else:
            sfdate2 = to_string(s_list.fdate2)
            stdate2 = to_string(s_list.tdate2)

        if s_list.fdate3 == None:
            sfdate3 = ""
            stdate3 = ""


        else:
            sfdate3 = to_string(s_list.fdate3)
            stdate3 = to_string(s_list.tdate3)


        l_order.bestellart = to_string(s_list.supp1) + ";" + to_string(s_list.du_price1 * 100) + ";" + s_list.curr1 + ";" + sfdate1 + ";" + stdate1 + "-" + to_string(s_list.supp2) + ";" + to_string(s_list.du_price2 * 100) + ";" + s_list.curr2 + ";" + sfdate2 + ";" + stdate2 + "-" + to_string(s_list.supp3) + ";" + to_string(s_list.du_price3 * 100) + ";" + s_list.curr3 + ";" + sfdate3 + ";" + stdate3
        pass

    if rej_flag :

        for l_order in db_session.query(L_order).filter(
                 (L_order.lief_nr == 0) & (L_order.docu_nr == l_orderhdr.docu_nr)).order_by(L_order._recid).all():
            l_order.loeschflag = 1


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.action = "Supplier"
    res_history.aenderung = "Change Supplier name from: " + chr_unicode(10) + chr_unicode(10) +\
            to_string(t_l_order.bestellart) + "*** Changed to:" + chr_unicode(10) + chr_unicode(10) +\
            to_string(l_order.bestellart)


    pass
    pass

    return generate_output()