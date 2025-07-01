#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Queasy

def ts_splitbill_get_update_guestbl(v_key:int, hbill_recid:int, curr_select:int, guest_name:string):

    prepare_cache ([H_bill])

    success_flag = False
    gname = ""
    bill_no:int = 0
    dept_no:int = 0
    main_guest:string = ""
    h_bill = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gname, bill_no, dept_no, main_guest, h_bill, queasy
        nonlocal v_key, hbill_recid, curr_select, guest_name

        return {"success_flag": success_flag, "gname": gname}


    h_bill = get_cache (H_bill, {"_recid": [(eq, hbill_recid)]})

    if not h_bill:

        return generate_output()
    bill_no = h_bill.rechnr
    dept_no = h_bill.departement
    main_guest = h_bill.bilname

    if v_key == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 286)],"number1": [(eq, bill_no)],"number2": [(eq, dept_no)],"number3": [(eq, curr_select)]})

        if not queasy:

            if guest_name != "" or guest_name != None:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 286
                queasy.number1 = bill_no
                queasy.number2 = dept_no
                queasy.number3 = curr_select
                queasy.char1 = guest_name


        else:

            if guest_name != "" and guest_name != None:
                pass
                queasy.char1 = guest_name
                pass
                pass
            else:
                pass
                db_session.delete(queasy)
                pass
        success_flag = True

    elif v_key == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 286)],"number1": [(eq, bill_no)],"number2": [(eq, dept_no)],"number3": [(eq, curr_select)]})

        if queasy:
            gname = queasy.char1
        success_flag = True

    elif v_key == 3:

        queasy = get_cache (Queasy, {"key": [(eq, 286)],"number1": [(eq, bill_no)],"number2": [(eq, dept_no)],"number3": [(eq, curr_select)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass
        success_flag = True

    return generate_output()