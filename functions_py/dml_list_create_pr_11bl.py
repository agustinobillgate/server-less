#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Andika 04/08/2025
# gitlab: -
# remarks: -
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, Bediener, L_order, L_artikel, Dml_art, Reslin_queasy, Dml_artdep

c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})
s_list_data, S_list = create_model("S_list", {"s_flag":string, "selected":bool, "artnr":int, "bezeich":string, "qty":Decimal, "qty0":Decimal, "price":Decimal, "qty2":Decimal})

def dml_list_create_pr_11bl(c_list_data:[C_list], s_list_data:[S_list], curr_dept:int, rec_id:int, dunit_price:bool, selected_date:date, user_init:string):

    prepare_cache ([Bediener, L_order, L_artikel, Dml_art, Reslin_queasy, Dml_artdep])

    t_l_orderhdr_data = []
    docu_nr:string = ""
    t_qty:Decimal = to_decimal("0.0")
    counter:int = 0
    l_orderhdr = bediener = l_order = l_artikel = dml_art = reslin_queasy = dml_artdep = None

    c_list = s_list = t_l_orderhdr = s1_list = c1_list = None

    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_orderhdr_data, docu_nr, t_qty, counter, l_orderhdr, bediener, l_order, l_artikel, dml_art, reslin_queasy, dml_artdep
        nonlocal curr_dept, rec_id, dunit_price, selected_date, user_init


        nonlocal c_list, s_list, t_l_orderhdr, s1_list, c1_list
        nonlocal t_l_orderhdr_data

        return {"t-l-orderhdr": t_l_orderhdr_data}

    def create_pr():

        nonlocal t_l_orderhdr_data, docu_nr, t_qty, counter, l_orderhdr, bediener, l_order, l_artikel, dml_art, reslin_queasy, dml_artdep
        nonlocal curr_dept, rec_id, dunit_price, selected_date, user_init


        nonlocal c_list, s_list, t_l_orderhdr, s1_list, c1_list
        nonlocal t_l_orderhdr_data

        pos:int = 0
        S1_list = S_list
        s1_list_data = s_list_data
        C1_list = C_list
        c1_list_data = c_list_data
        pass
        l_orderhdr.betriebsnr = 10
        l_orderhdr.gedruckt = None
        l_orderhdr.lief_fax[1] = " ; ; ; "
        l_orderhdr.lief_fax[0] = bediener.username
        l_orderhdr.txtnr = curr_dept


        pass
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = l_orderhdr.docu_nr
        l_order.pos = 0
        l_order.bestelldatum = l_orderhdr.bestelldatum
        l_order.op_art = 1

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.selected)):

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, s1_list.artnr)]})
            pos = pos + 1
            l_order = L_order()
            db_session.add(l_order)

            l_order.docu_nr = l_orderhdr.docu_nr
            l_order.artnr = l_artikel.artnr
            l_order.pos = pos
            l_order.bestelldatum = l_orderhdr.bestelldatum
            l_order.op_art = 1
            l_order.lief_fax[0] = bediener.username
            l_order.lief_fax[2] = l_artikel.traubensorte
            l_order.anzahl =  to_decimal(s1_list.qty)
            l_order.einzelpreis =  to_decimal(s1_list.price)
            l_order.txtnr = 1
            l_order.flag = dunit_price
            l_order.warenwert =  to_decimal(s1_list.qty) * to_decimal(s1_list.price)
            l_order.quality = to_string(0, "99.99 ") + to_string(0, "99.99") +\
                    to_string(0, " 99.99")

            if l_artikel.lief_einheit != 0:
                l_order.warenwert =  to_decimal(l_order.warenwert) * to_decimal(l_artikel.lief_einheit)

                if dunit_price:
                    l_order.einzelpreis =  to_decimal(l_order.einzelpreis) * to_decimal(l_artikel.lief_einheit)
                l_order.txtnr = l_artikel.lief_einheit

            c1_list = query(c1_list_data, filters=(lambda c1_list: c1_list.artnr == s1_list.artnr), first=True)
            l_order.besteller = c1_list.remark

            if s1_list.qty == s1_list.qty0:
                c1_list_data.remove(c1_list)
            else:
                c1_list.qty =  to_decimal(s1_list.qty0) - to_decimal(s1_list.qty)

            if curr_dept == 0:

                dml_art = get_cache (Dml_art, {"artnr": [(eq, s1_list.artnr)],"datum": [(eq, selected_date)]})

                if dml_art:

                    if (s1_list.qty + s1_list.qty2) == s1_list.qty0:

                        if num_entries(dml_art.chginit, ";") > 2:

                            if s1_list.qty != s1_list.qty0:
                                s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                            else:
                                s1_list.qty2 =  to_decimal(s1_list.qty)
                            dml_art.chginit = entry(2, dml_art.chginit, ";", to_string(s1_list.qty2))
                        else:

                            if s1_list.qty != s1_list.qty0:
                                s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                            else:
                                s1_list.qty2 =  to_decimal(s1_list.qty)
                            dml_art.chginit = dml_art.chginit + ";" + docu_nr + ";" + to_string(s1_list.qty2)
                    else:

                        if num_entries(dml_art.chginit, ";") > 2:
                            s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                            dml_art.chginit = entry(2, dml_art.chginit, ";", to_string(s1_list.qty2))
                        else:
                            s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                            dml_art.chginit = dml_art.chginit + ";" + docu_nr + ";" + to_string(s1_list.qty)
                        pass
            else:

                if counter > 1:

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == s1_list.artnr) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy.number2 == counter)).first()

                    if reslin_queasy:

                        if (s1_list.qty + s1_list.qty2) == s1_list.qty0:

                            if num_entries(reslin_queasy.char3, ";") > 2:

                                if s1_list.qty != s1_list.qty0:
                                    s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                else:
                                    s1_list.qty2 =  to_decimal(s1_list.qty)
                                reslin_queasy.char3 = entry(2, reslin_queasy.char3, ";", to_string(s1_list.qty2))
                            else:

                                if s1_list.qty != s1_list.qty0:
                                    s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                else:
                                    s1_list.qty2 =  to_decimal(s1_list.qty)
                                reslin_queasy.char3 = reslin_queasy.char3 + ";" + to_string(s1_list.qty2)
                        else:

                            if num_entries(reslin_queasy.char3, ";") > 2:
                                s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                reslin_queasy.char3 = entry(2, reslin_queasy.char3, ";", to_string(s1_list.qty2))
                            else:
                                s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                reslin_queasy.char3 = reslin_queasy.char3 + ";" + to_string(s1_list.qty)
                            pass
                else:

                    dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, s1_list.artnr)],"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})

                    if dml_artdep:

                        if (s1_list.qty + s1_list.qty2) == s1_list.qty0:

                            if num_entries(dml_artdep.chginit, ";") > 2:

                                if s1_list.qty != s1_list.qty0:
                                    s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                else:
                                    s1_list.qty2 =  to_decimal(s1_list.qty)
                                dml_artdep.chginit = entry(2, dml_artdep.chginit, ";", to_string(s1_list.qty2))
                            else:

                                if s1_list.qty != s1_list.qty0:
                                    s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                else:
                                    s1_list.qty2 =  to_decimal(s1_list.qty)

                                if num_entries(dml_artdep.chginit, ";") > 1:
                                    dml_artdep.chginit = dml_artdep.chginit + ";" + to_string(s1_list.qty2)
                                else:
                                    dml_artdep.chginit = dml_artdep.chginit + ";" + docu_nr + ";" + to_string(s1_list.qty2)
                        else:

                            if num_entries(dml_artdep.chginit, ";") > 2:
                                s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)
                                dml_artdep.chginit = entry(2, dml_artdep.chginit, ";", to_string(s1_list.qty2))
                            else:
                                s1_list.qty2 =  to_decimal(s1_list.qty2) + to_decimal(s1_list.qty)

                                if num_entries(dml_artdep.chginit, ";") > 1:
                                    dml_artdep.chginit = dml_artdep.chginit + ";" + to_string(s1_list.qty2)
                                else:
                                    dml_artdep.chginit = dml_artdep.chginit + ";" + docu_nr + ";" + to_string(s1_list.qty2)
                            pass


    s_list = query(s_list_data, filters=(lambda s_list: s_list.selected), first=True)

    c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == s_list.artnr), first=True)

    if c_list.dml_nr != "":
        docu_nr = c_list.dml_nr
        counter = to_int(substring(c_list.dml_nr, 10, 2))
    else:
        docu_nr = "D" + to_string(c_list.dept, "99") + substring(to_string(get_year(selected_date)) , 2, 2) + to_string(get_month(selected_date) , "99") + to_string(get_day(selected_date) , "99") + "001"
        counter = 1

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    
    if l_orderhdr:

        create_pr()
        pass
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_data.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
        t_l_orderhdr.rec_id = l_orderhdr._recid

        return generate_output()