#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions_py.storereq_list_create_list_1bl import storereq_list_create_list_1bl
from models import L_op

def storereq_list_btn_del_1bl(t_list_s_recid:int, bediener_nr:int, from_date:date, to_date:date, from_dept:int, to_dept:int, curr_lschein:string, show_price:bool):

    prepare_cache ([L_op])

    it_exist = False
    t_list_data = []
    l_op = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"s_recid":int, "t_status":int, "datum":date, "deptno":int, "lager_nr":int, "to_stock":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "deptname":string, "lscheinnr":string, "f_bezeich":string, "t_bezeich":string, "artnr":string, "bezeich":string, "einheit":string, "content":Decimal, "price":string, "qty":Decimal, "qty1":Decimal, "val":Decimal, "fibukonto":string, "id":string, "appstr":string, "appflag":bool, "stornogrund":string, "gl_bezeich":string, "art_bezeich":string, "art_lief_einheit":int, "art_traubensort":string, "zwkum":int, "endkum":int, "centername":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_data, l_op
        nonlocal t_list_s_recid, bediener_nr, from_date, to_date, from_dept, to_dept, curr_lschein, show_price


        nonlocal t_list
        nonlocal t_list_data

        return {"it_exist": it_exist, "t-list": t_list_data}

    # l_op = get_cache (L_op, {"_recid": [(eq, t_list_s_recid)]})
    l_op = db_session.query(L_op).filter(
             (L_op._recid == t_list_s_recid)).with_for_update().first()

    if l_op:
        # pass
        db_session.refresh(l_op, with_for_update=True)
        l_op.loeschflag = 2
        l_op.fuellflag = bediener_nr
        # pass
        # pass
    it_exist, t_list_data = get_output(storereq_list_create_list_1bl(from_date, to_date, from_dept, to_dept, curr_lschein, show_price))

    return generate_output()
