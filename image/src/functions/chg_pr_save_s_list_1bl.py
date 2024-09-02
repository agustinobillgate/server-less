from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_lieferant, L_orderhdr, Bediener, Res_history

def chg_pr_save_s_list_1bl(s_list:[S_list], tt_app_id:[Tt_app_id], rec_id:int, deptnr:int, comments_screen_value:str, rej_id:str, lieferdatum:date, rej_flag:bool, user_init:str):
    sfdate1:str = ""
    sfdate2:str = ""
    sfdate3:str = ""
    stdate1:str = ""
    stdate2:str = ""
    stdate3:str = ""
    app_id:[str] = ["", "", "", "", ""]
    old_bestellart:str = ""
    new_bestellart:str = ""
    l_order = l_lieferant = l_orderhdr = bediener = res_history = None

    s_list = tt_app_id = t_l_order = t_l_lieferant = t_lieferant = sbuff = None

    s_list_list, S_list = create_model_like(L_order, {"curr":str, "exrate":decimal, "s_recid":int, "amount":decimal, "supp1":int, "supp2":int, "supp3":int, "suppn1":str, "suppn2":str, "suppn3":str, "supps":str, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "curr1":str, "curr2":str, "curr3":str, "fdate1":date, "fdate2":date, "fdate3":date, "tdate1":date, "tdate2":date, "tdate3":date, "desc_coa":str, "last_pprice":decimal, "avg_pprice":decimal, "lprice":decimal, "lief_fax2":str, "ek_letzter":decimal, "lief_einheit":int, "supplier":str, "lief_fax_2":str, "vk_preis":decimal, "soh":decimal, "last_pdate":date, "a_firma":str, "last_pbook":decimal})
    tt_app_id_list, Tt_app_id = create_model("Tt_app_id", {"i_counter":int, "app_id":str})
    t_l_order_list, T_l_order = create_model_like(L_order)
    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)

    T_lieferant = L_lieferant
    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sfdate1, sfdate2, sfdate3, stdate1, stdate2, stdate3, app_id, old_bestellart, new_bestellart, l_order, l_lieferant, l_orderhdr, bediener, res_history
        nonlocal t_lieferant, sbuff


        nonlocal s_list, tt_app_id, t_l_order, t_l_lieferant, t_lieferant, sbuff
        nonlocal s_list_list, tt_app_id_list, t_l_order_list, t_l_lieferant_list
        return {}


    for tt_app_id in query(tt_app_id_list):
        app_id[tt_app_id.i_counter - 1] = tt_app_id.app_id

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()
    l_orderhdr.lief_fax[2] = comments_screen_value
    l_orderhdr.lieferdatum = lieferdatum
    l_orderhdr.angebot_lief[0] = deptnr
    l_orderhdr.lief_fax[1] = app_id[0] + ";" + app_id[1] + ";" + app_id[2] + ";" + app_id[3] + rej_id

    l_orderhdr = db_session.query(L_orderhdr).first()

    for sbuff in query(sbuff_list):

        l_order = db_session.query(L_order).filter(
                (L_order._recid == sbuff.s_recid)).first()

        s_list = query(s_list_list, filters=(lambda s_list :s_list.s_recid == to_int(l_order._recid)), first=True)
        buffer_copy(l_order, t_l_order)
        old_bestellart = l_order.bestellart
        l_order.einzelpreis = s_list.einzelpreis
        l_order.anzahl = s_list.anzahl
        l_order.stornogrund = s_list.stornogrund
        l_order.besteller = s_list.besteller
        l_order.angebot_lief[2] = s_list.angebot_lief[2]
        l_order.angebot_lief[1] = s_list.angebot_lief[1]
        l_order.warenwert = s_list.amount
        l_order.lief_fax[1] = s_list.lief_fax_2

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
        new_bestellart = l_order.bestellart

        l_order = db_session.query(L_order).first()

    if rej_flag :

        for l_order in db_session.query(L_order).filter(
                (L_order.lief_nr == 0) &  (L_order.docu_nr == l_orderhdr.docu_nr)).all():
            l_order.loeschflag = 1
            new_bestellart = l_order.bestellart


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.action = "Supplier"
    res_history.aenderung = "Change Supplier name from: " + chr(10) + chr(10) +\
            to_string(old_bestellart) + "*** Changed to:" + chr(10) + chr(10) +\
            to_string(new_bestellart)

    res_history = db_session.query(Res_history).first()


    return generate_output()