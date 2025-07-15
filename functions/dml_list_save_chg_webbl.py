#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.dml_list_save_it_1bl import dml_list_save_it_1bl
from functions.dml_list_create_it_11bl import dml_list_create_it_11bl

c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal})

def dml_list_save_chg_webbl(c_list_data:[C_list], user_init:string, curr_dept:int, selected_date:date):


    supply_list = c_list = None

    supply_list_data, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":string, "telefon":string, "fax":string, "namekontakt":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, curr_dept, selected_date


        nonlocal supply_list, c_list
        nonlocal supply_list_data

        return {"c-list": c_list_data}


    for c_list in query(c_list_data):
        c_list.qty =  to_decimal(c_list.qty) + to_decimal(c_list.a_qty)

        if c_list.qty < 0:
            c_list.qty =  to_decimal("0")
        c_list.a_qty =  to_decimal("0")
        c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
        c_list.cid = user_init
        get_output(dml_list_save_it_1bl(curr_dept, c_list.artnr, c_list.qty, selected_date, user_init, c_list.price, c_list.lief_nr, c_list.approved, c_list.remark))
    c_list_data.clear()
    supply_list_data, c_list_data = get_output(dml_list_create_it_11bl(curr_dept, selected_date))

    return generate_output()