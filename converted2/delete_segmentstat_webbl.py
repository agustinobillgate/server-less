#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Segmentstat

del_list_data, Del_list = create_model("Del_list", {"int1":int, "int2":int, "date1":date})

def delete_segmentstat_webbl(case_type:int, del_list_data:[Del_list]):
    success_flag = False
    segmentstat = None

    del_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, segmentstat
        nonlocal case_type


        nonlocal del_list

        return {"success_flag": success_flag}

    if case_type == 1:

        for del_list in query(del_list_data, sort_by=[("int1",False)]):

            segmentstat = get_cache (Segmentstat, {"segmentcode": [(eq, del_list.int1)],"datum": [(eq, del_list.date1)]})

            if segmentstat:
                db_session.delete(segmentstat)
                success_flag = True
                pass

    return generate_output()