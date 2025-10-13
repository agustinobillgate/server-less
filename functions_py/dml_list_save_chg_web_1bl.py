#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 566
# 
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Added modify program from progress
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.dml_list_save_it_3bl import dml_list_save_it_3bl
from models import Reslin_queasy, Dml_artdep, Bediener, Res_history, Queasy

c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})

def dml_list_save_chg_web_1bl(c_list_data:[C_list], user_init:string, curr_dept:int, selected_date:date, curr_select:string):

    prepare_cache ([Reslin_queasy, Bediener, Res_history, Queasy])

    dml_no:string = ""
    counter:int = 0
    temp_nr:string = ""
    reslin_queasy = dml_artdep = bediener = res_history = queasy = None

    supply_list = c_list = qlist = breslin = None

    supply_list_data, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":string, "telefon":string, "fax":string, "namekontakt":string})
    qlist_data, Qlist = create_model("Qlist", {"datum":date, "depart":int, "number1":int})

    Breslin = create_buffer("Breslin",Reslin_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_no, counter, temp_nr, reslin_queasy, dml_artdep, bediener, res_history, queasy
        nonlocal user_init, curr_dept, selected_date, curr_select
        nonlocal breslin


        nonlocal supply_list, c_list, qlist, breslin
        nonlocal supply_list_data, qlist_data

        return {"c-list": c_list_data}


    qlist_data.clear()
    temp_nr = "D" + to_string(curr_dept, "99") + substring(to_string(get_year(selected_date)) , 2, 2) + to_string(get_month(selected_date) , "99") + to_string(get_day(selected_date) , "99")
    counter = 1

    dml_artdep = get_cache (Dml_artdep, {"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})

    if dml_artdep:
        counter = counter + 1

    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept)).first()
    while None != reslin_queasy:
        counter = reslin_queasy.number2

        curr_recid = reslin_queasy._recid
        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy._recid > curr_recid)).first()

    breslin = db_session.query(Breslin).filter(
             (Breslin.key == ("DML").lower()) & (Breslin.date1 == selected_date) & (to_int(entry(1, Breslin.char1, ";")) == curr_dept) & (Breslin.number2 == counter)).first()

    if breslin:
        counter = counter + 1
    dml_no = temp_nr + to_string(counter, "999")

    for c_list in query(c_list_data):
        c_list.qty =  to_decimal(c_list.qty) + to_decimal(c_list.a_qty)

        if c_list.qty < 0:
            c_list.qty =  to_decimal("0")
        c_list.a_qty =  to_decimal("0")
        c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
        c_list.cid = user_init

        if curr_select.lower()  == ("chg").lower() :
            dml_no = c_list.dml_nr
            counter = to_int(substring(c_list.dml_nr, 10, 2))
        # Rd 31/7/2025
        # remark unix command
        get_output(dml_list_save_it_3bl(curr_dept, c_list.artnr, c_list.qty, selected_date, user_init, c_list.price, c_list.lief_nr, c_list.approved, c_list.remark, curr_select, dml_no, counter))

        if c_list.approved:

            qlist = query(qlist_data, filters=(lambda qlist: qlist.datum == selected_date and qlist.depart == curr_dept and ((qlist.number1 == counter) or (counter == 1 and qlist.number1 == 0))), first=True)

            if not qlist:
                qlist = Qlist()
                qlist_data.append(qlist)

                qlist.datum = selected_date
                qlist.depart = curr_dept

                if counter == 1:
                    qlist.number1 = 0
                else:
                    qlist.number1 = counter

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "DML"
                res_history.aenderung = "Approved DML By :" + bediener.username + " DML Number : " +\
                        dml_no + " Departement : " + to_string(curr_dept)


                pass
    c_list_data.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 253)]})

    if queasy:

        for qlist in query(qlist_data, sort_by=[("datum",False),("depart",False)]):
            pass

            queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, qlist.depart)],"date1": [(eq, qlist.datum)],"logi1": [(eq, True)],"number3": [(eq, qlist.number1)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 254
                queasy.number1 = qlist.depart
                queasy.date1 = qlist.datum
                queasy.logi1 = True
                queasy.logi2 = False
                queasy.number3 = qlist.number1


            qlist_data.remove(qlist)

    return generate_output()