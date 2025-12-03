#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr, L_op, Queasy

c_list_data, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":Decimal, "zwkum":int, "endkum":int, "qty":Decimal, "qty1":Decimal, "amount":Decimal, "avrg_amount":Decimal, "fibukonto":string, "cost_center":string, "variance":Decimal, "lscheinnr":string, "id":string, "change_id":string, "chage_date":string}, {"fibukonto": "0000000000"})

def inv_adjustlist_btn_save_webbl(user_init:string, c_list_data:[C_list]):

    prepare_cache ([L_ophdr, L_op, Queasy])

    err_code = 0
    gl_notfound:bool = False
    l_ophdr = l_op = queasy = None

    c_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_notfound, l_ophdr, l_op, queasy
        nonlocal user_init


        nonlocal c_list

        return {"c-list": c_list_data, "err_code": err_code}

    for c_list in query(c_list_data):

        l_ophdr = db_session.query(L_ophdr).filter(
                 (L_ophdr.lscheinnr == c_list.lscheinnr) & (L_ophdr.docu_nr == c_list.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & ((trim(L_ophdr.fibukonto) == ("0").lower()) | (trim(L_ophdr.fibukonto) == ("00").lower()) | (trim(L_ophdr.fibukonto) == ("000").lower()) | (trim(L_ophdr.fibukonto) == ("0000").lower()) | (trim(L_ophdr.fibukonto) == ("00000").lower()) | (trim(L_ophdr.fibukonto) == ("000000").lower()) | (trim(L_ophdr.fibukonto) == ("0000000").lower()) | (trim(L_ophdr.fibukonto) == ("00000000").lower()) | (trim(L_ophdr.fibukonto) == ("000000000").lower()) | (trim(L_ophdr.fibukonto) == ("0000000000").lower()) | (trim(L_ophdr.fibukonto) == ("00000000000").lower()) | (trim(L_ophdr.fibukonto) == ("000000000000").lower()) | (trim(L_ophdr.fibukonto) == ("0000000000000").lower()))).with_for_update().first()

        if l_ophdr:
            l_ophdr.fibukonto = c_list.fibukonto

        l_op = db_session.query(L_op).filter(
                 (L_op.lscheinnr == c_list.lscheinnr) & (L_op.artnr == c_list.artnr) & (to_int(L_op.stornogrund) == 0)).with_for_update().first()

        if l_op:

            queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char2": [(eq, user_init)],"number1": [(eq, l_op.artnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 334
                queasy.char1 = l_op.lscheinnr
                queasy.char2 = user_init
                queasy.char3 = "Adjusment Result"
                queasy.number1 = l_op.artnr
                queasy.date2 = get_current_date()


            l_op.stornogrund = c_list.fibukonto


            pass
            pass

    return generate_output()