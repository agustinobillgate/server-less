from functions.additional_functions import *
import decimal
from datetime import date
from functions.storereq_list_create_list_1bl import storereq_list_create_list_1bl
from models import L_op

def storereq_list_btn_del_1bl(t_list_s_recid:int, bediener_nr:int, from_date:date, to_date:date, from_dept:int, to_dept:int, curr_lschein:str, show_price:bool):
    it_exist = False
    t_list_list = []
    l_op = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"s_recid":int, "t_status":int, "datum":date, "deptno":int, "lager_nr":int, "to_stock":int, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal, "deptname":str, "lscheinnr":str, "f_bezeich":str, "t_bezeich":str, "artnr":str, "bezeich":str, "einheit":str, "content":decimal, "price":str, "qty":decimal, "qty1":decimal, "val":decimal, "fibukonto":str, "id":str, "appstr":str, "appflag":bool, "stornogrund":str, "gl_bezeich":str, "art_bezeich":str, "art_lief_einheit":int, "art_traubensort":str, "zwkum":int, "endkum":int, "centername":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_list, l_op


        nonlocal t_list
        nonlocal t_list_list
        return {"it_exist": it_exist, "t-list": t_list_list}

    l_op = db_session.query(L_op).filter(
            (L_op._recid == t_list_s_recid)).first()
    l_op.loeschflag = 2
    l_op.fuellflag = bediener_nr


    it_exist, t_list_list = get_output(storereq_list_create_list_1bl(from_date, to_date, from_dept, to_dept, curr_lschein, show_price))

    return generate_output()