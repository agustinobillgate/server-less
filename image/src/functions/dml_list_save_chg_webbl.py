from functions.additional_functions import *
import decimal
from datetime import date
from functions.dml_list_save_it_1bl import dml_list_save_it_1bl
from functions.dml_list_create_it_11bl import dml_list_create_it_11bl

def dml_list_save_chg_webbl(c_list:[C_list], user_init:str, curr_dept:int, selected_date:date):


    supply_list = c_list = None

    supply_list_list, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":str, "telefon":str, "fax":str, "namekontakt":str})
    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":str, "artnr":int, "bezeich":str, "qty":decimal, "a_qty":decimal, "price":decimal, "l_price":decimal, "unit":str, "content":decimal, "amount":decimal, "deliver":decimal, "dept":int, "supplier":str, "id":str, "cid":str, "price1":decimal, "qty1":decimal, "lief_nr":int, "approved":bool, "remark":str, "soh":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal supply_list, c_list
        nonlocal supply_list_list, c_list_list
        return {}


    for c_list in query(c_list_list):
        c_list.qty = c_list.qty + c_list.a_qty

        if c_list.qty < 0:
            c_list.qty = 0
        c_list.a_qty = 0
        c_list.amount = c_list.qty * c_list.price
        c_list.cid = user_init
        get_output(dml_list_save_it_1bl(curr_dept, c_list.artnr, c_list.qty, selected_date, user_init, c_list.price, c_list.lief_nr, c_list.approved, c_list.remark))
    c_list_list.clear()
    supply_list_list, c_list_list = get_output(dml_list_create_it_11bl(curr_dept, selected_date))

    return generate_output()