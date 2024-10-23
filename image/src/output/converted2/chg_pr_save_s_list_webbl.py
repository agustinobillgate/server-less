from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_lieferant, L_orderhdr, Queasy, Bediener, Res_history

s_list_list, S_list = create_model_like(L_order, {"curr":str, "exrate":decimal, "s_recid":int, "amount":decimal, "supp1":int, "supp2":int, "supp3":int, "suppn1":str, "suppn2":str, "suppn3":str, "supps":str, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "curr1":str, "curr2":str, "curr3":str, "fdate1":date, "fdate2":date, "fdate3":date, "tdate1":date, "tdate2":date, "tdate3":date, "desc_coa":str, "last_pprice":decimal, "avg_pprice":decimal, "lprice":decimal, "lief_fax2":str, "ek_letzter":decimal, "lief_einheit":int, "supplier":str, "lief_fax_2":str, "vk_preis":decimal, "soh":decimal, "last_pdate":date, "a_firma":str, "last_pbook":decimal, "avg_cons":decimal})
approved_list, Approved = create_model("Approved", {"nr":int, "flag":bool, "usrid":str, "app_date":date, "app_time":str})

def chg_pr_save_s_list_webbl(s_list_list:[S_list], approved_list:[Approved], rec_id:int, deptnr:int, comments_screen_value:str, rej_id:str, lieferdatum:date, rej_flag:bool, user_init:str):
    sfdate1:str = ""
    sfdate2:str = ""
    sfdate3:str = ""
    stdate1:str = ""
    stdate2:str = ""
    stdate3:str = ""
    app_id:List[str] = create_empty_list(4,"")
    i:int = ""
    app_str:str = ""
    str:str = ""
    count_app:int = 0
    j:int = 0
    logstring:str = ""
    l_order = l_lieferant = l_orderhdr = queasy = bediener = res_history = None

    s_list = approved = t_l_lieferant = old_l_orderhdr = old_l_order = t_lieferant = sbuff = None

    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)
    old_l_orderhdr_list, Old_l_orderhdr = create_model_like(L_orderhdr)
    old_l_order_list, Old_l_order = create_model_like(L_order)

    T_lieferant = create_buffer("T_lieferant",L_lieferant)
    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sfdate1, sfdate2, sfdate3, stdate1, stdate2, stdate3, app_id, i, app_str, str, count_app, j, logstring, l_order, l_lieferant, l_orderhdr, queasy, bediener, res_history
        nonlocal rec_id, deptnr, comments_screen_value, rej_id, lieferdatum, rej_flag, user_init
        nonlocal t_lieferant, sbuff


        nonlocal s_list, approved, t_l_lieferant, old_l_orderhdr, old_l_order, t_lieferant, sbuff
        nonlocal s_list_list, approved_list, t_l_lieferant_list, old_l_orderhdr_list, old_l_order_list
        return {}

    def create_log(aend_str:str):

        nonlocal sfdate1, sfdate2, sfdate3, stdate1, stdate2, stdate3, app_id, i, app_str, str, count_app, j, logstring, l_order, l_lieferant, l_orderhdr, queasy, bediener, res_history
        nonlocal rec_id, deptnr, comments_screen_value, rej_id, lieferdatum, rej_flag, user_init
        nonlocal t_lieferant, sbuff


        nonlocal s_list, approved, t_l_lieferant, old_l_orderhdr, old_l_order, t_lieferant, sbuff
        nonlocal s_list_list, approved_list, t_l_lieferant_list, old_l_orderhdr_list, old_l_order_list

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Purchase Request"
        res_history.aenderung = aend_str


        pass


    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr._recid == rec_id)).first()
    buffer_copy(l_orderhdr, old_l_orderhdr)
    l_orderhdr.lief_fax[2] = comments_screen_value
    l_orderhdr.lieferdatum = lieferdatum
    l_orderhdr.angebot_lief[0] = deptnr

    if l_orderhdr.lief_fax[2] != old_l_orderhdr.lief_fax[2]:

        if l_orderhdr.lief_fax[2] == None:
            l_orderhdr.lief_fax[2] = " "

        if old_l_orderhdr.lief_fax[2] == None:
            old_l_orderhdr.lief_fax[2] = " "
        logstring = "[CHG ORDERHDR]DOC NO: " + l_orderhdr.docu_nr + " Order Instruction changed From: " + to_string(old_l_orderhdr.lief_fax[2]) + " To: " + to_string(l_orderhdr.lief_fax[2])
        create_log(logstring)

    if l_orderhdr.lieferdatum != old_l_orderhdr.lieferdatum:
        logstring = "[CHG ORDERHDR]DOC NO: " + l_orderhdr.docu_nr + " Needed Date changed From: " + to_string(old_l_orderhdr.lieferdatum) + " To: " + to_string(l_orderhdr.lieferdatum)
        create_log(logstring)

    if l_orderhdr.angebot_lief[0] != old_l_orderhdr.angebot_lief[0]:
        logstring = "[CHG ORDERHDR]DOC NO: " + l_orderhdr.docu_nr + " Dept No changed From: " + to_string(old_l_orderhdr.angebot_lief[0]) + " To: " + to_string(l_orderhdr.angebot_lief[0])
        create_log(logstring)
    l_orderhdr.lief_fax[1] = ""
    for i in range(1,4 + 1) :
        app_str = ""

        approved = query(approved_list, filters=(lambda approved: approved.nr == i), first=True)

        if approved:
            app_str = approved.usrid + " " + to_string(approved.app_date) + " " + approved.app_time

            if approved.nr == 1:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 278) & (Queasy.char1 == l_orderhdr.docu_nr)).first()

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 278
                    queasy.char1 = l_orderhdr.docu_nr
                    queasy.logi1 = True
                    queasy.logi2 = False
                    queasy.date1 = get_current_date()
                    queasy.number2 = get_current_time_in_seconds()


        str = str + app_str + ";"

    if rej_id == None:
        rej_id = " "


    l_orderhdr.lief_fax[1] = substring(str, 0, len(str) - 1) + rej_id

    for sbuff in query(sbuff_list):

        l_order = db_session.query(L_order).filter(
                 (L_order._recid == sbuff.s_recid)).first()

        s_list = query(s_list_list, filters=(lambda s_list: s_list.s_recid == to_int(l_order._recid)), first=True)
        buffer_copy(l_order, old_l_order)
        l_order.einzelpreis =  to_decimal(s_list.einzelpreis)
        l_order.anzahl =  to_decimal(s_list.anzahl)
        l_order.stornogrund = s_list.stornogrund
        l_order.besteller = s_list.besteller
        l_order.angebot_lief[2] = s_list.angebot_lief[2]
        l_order.angebot_lief[1] = s_list.angebot_lief[1]
        l_order.warenwert =  to_decimal(s_list.amount)
        l_order.lief_fax[1] = s_list.lief_fax_2

        if l_order.einzelpreis != old_l_order.einzelpreis:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " DUnit Price changed From: " + to_string(old_l_order.einzelpreis) + " To: " + to_string(l_order.einzelpreis)
            create_log(logstring)

        if l_order.anzahl != old_l_order.anzahl:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Ammount changed From: " + to_string(old_l_order.anzahl) + " To: " + to_string(l_order.anzahl)
            create_log(logstring)

        if l_order.stornogrund != old_l_order.stornogrund:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " AcctNo changed From: " + to_string(old_l_order.stornogrund) + " To: " + to_string(l_order.stornogrund)
            create_log(logstring)

        if l_order.besteller != old_l_order.besteller:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Remark changed From: " + to_string(old_l_order.besteller) + " To: " + to_string(l_order.besteller)
            create_log(logstring)

        if l_order.angebot_lief[2] != old_l_order.angebot_lief[2]:
            logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Delivery Ammount changed From: " + to_string(old_l_order.angebot_lief[2]) + " To: " + to_string(l_order.angebot_lief[2])
            create_log(logstring)

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

        if num_entries(old_l_order.bestellart, "-") > 0:
            for j in range(1,num_entries(l_order.bestellart, "-")  + 1) :

                if trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")) != trim(entry(1, entry(j - 1, old_l_order.bestellart, "-") , ";") - 1) and trim(entry(1, entry(j, old_l_order.bestellart, "-") , ";") - 1 - 1) == ("0").lower() :

                    l_lieferant = db_session.query(L_lieferant).filter(
                             (L_lieferant.lief_nr == to_int(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")))).first()

                    if l_lieferant:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is added" + " Value: " + l_lieferant.firma
                    else:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is added" + " Value: " + trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";"))
                    create_log(logstring)

                elif trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")) != trim(entry(1, entry(j - 1, old_l_order.bestellart, "-") , ";") - 1) and trim(entry(1, entry(j, l_order.bestellart, "-") , ";") - 1 - 1) == ("0").lower() :

                    l_lieferant = db_session.query(L_lieferant).filter(
                             (L_lieferant.lief_nr == to_int(entry(0, entry(j - 1, old_l_order.bestellart, "-") , ";")))).first()

                    if l_lieferant:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is removed" + " Value: " + l_lieferant.firma
                    else:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is removed" + " Value: " + trim(entry(0, entry(j - 1, old_l_order.bestellart, "-") , ";"))
                    create_log(logstring)

                elif trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")) != trim(entry(1, entry(j - 1, old_l_order.bestellart, "-") , ";") - 1):

                    l_lieferant = db_session.query(L_lieferant).filter(
                             (L_lieferant.lief_nr == to_int(entry(0, entry(j - 1, old_l_order.bestellart, "-") , ";")))).first()

                    if l_lieferant:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is changed" + " From: " + l_lieferant.firma
                    else:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is changed" + " From: " + trim(entry(0, entry(j - 1, old_l_order.bestellart, "-") , ";"))

                    l_lieferant = db_session.query(L_lieferant).filter(
                             (L_lieferant.lief_nr == to_int(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")))).first()

                    if l_lieferant:
                        logstring = logstring + " To: " + l_lieferant.firma
                    else:
                        logstring = logstring + " To: " + trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";"))
                    create_log(logstring)
        else:
            for j in range(1,num_entries(l_order.bestellart, "-")  + 1) :

                if trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")) != ("0").lower() :

                    l_lieferant = db_session.query(L_lieferant).filter(
                             (L_lieferant.lief_nr == to_int(entry(0, entry(j - 1, l_order.bestellart, "-") , ";")))).first()

                    if l_lieferant:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is added" + " Value: " + l_lieferant.firma
                    else:
                        logstring = "[CHG LORDER]DOC NO: " + l_order.docu_nr + " - ITEM NO: " + to_string(l_order.artnr) + " Supplier " + to_string(j) + " is added" + " Value: " + trim(entry(0, entry(j - 1, l_order.bestellart, "-") , ";"))
                    create_log(logstring)

    if rej_flag :

        for l_order in db_session.query(L_order).filter(
                 (L_order.lief_nr == 0) & (L_order.docu_nr == l_orderhdr.docu_nr)).order_by(L_order._recid).all():
            l_order.loeschflag = 1


    return generate_output()