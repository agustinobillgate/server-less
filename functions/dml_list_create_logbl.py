#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_history

c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})

def dml_list_create_logbl(curr_flag:string, bediener_nr:int, curr_dept:int, curr_date:date, prev_qty:int, prev_amt:int, c_list_data:[C_list]):

    prepare_cache ([Res_history])

    curr_qty:int = 0
    curr_amt:int = 0
    t_qty:int = 0
    t_amt:int = 0
    res_history = None

    c_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_qty, curr_amt, t_qty, t_amt, res_history
        nonlocal curr_flag, bediener_nr, curr_dept, curr_date, prev_qty, prev_amt


        nonlocal c_list

        return {}

    if curr_flag.lower()  == ("new").lower() :
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Add DML[" + to_string(curr_date) + "] Department[" + to_string(curr_dept) + "]"


        res_history.action = "DML"
        pass
        pass

    elif curr_flag.lower()  == ("chg").lower() :

        for c_list in query(c_list_data, filters=(lambda c_list: c_list.qty != 0 or c_list.a_qty != 0)):
            t_qty = c_list.qty + c_list.a_qty
            t_amt = t_qty * c_list.price
            curr_qty = curr_qty + t_qty
            curr_amt = curr_amt + t_amt


        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Modify DML[" + to_string(curr_date) + "] Dept[" + to_string(curr_dept) + "] | Total Price From: " + to_string(prev_amt) +\
                " To Total Price: " + to_string(curr_amt) + " | Total Qty From: " + to_string(prev_qty) + " To Total Qty: " + to_string(curr_qty)


        res_history.action = "DML"
        pass
        pass

    return generate_output()