#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zwkum, Htparam

def prepare_ba_availabilitybl():

    prepare_cache ([Htparam])

    system_date = None
    curr_date = None
    from_date = None
    ba_dept = 0
    z_list_list = []
    zwkum = htparam = None

    z_list = None

    z_list_list, Z_list = create_model_like(Zwkum)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal system_date, curr_date, from_date, ba_dept, z_list_list, zwkum, htparam


        nonlocal z_list
        nonlocal z_list_list

        return {"system_date": system_date, "curr_date": curr_date, "from_date": from_date, "ba_dept": ba_dept, "z-list": z_list_list}

    def readequipment():

        nonlocal system_date, curr_date, from_date, ba_dept, z_list_list, zwkum, htparam


        nonlocal z_list
        nonlocal z_list_list

        lvcval:string = ""
        lvi:int = 0
        lvicnt:int = 0
        dept:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
        dept = htparam.finteger

        if dept == 0:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 902)]})

        if htparam.fchar == "":

            return
        z_list_list.clear()
        lvicnt = num_entries(htparam.fchar, ";")
        for lvi in range(1,lvicnt + 1) :
            lvcval = ""


            lvcval = trim(entry(lvi - 1, htparam.fchar, ";"))

            if lvcval != "":

                zwkum = get_cache (Zwkum, {"departement": [(eq, dept)],"zknr": [(eq, to_int(lvcval))]})

                if zwkum:
                    z_list = Z_list()
                    z_list_list.append(z_list)

                    buffer_copy(zwkum, z_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    system_date = htparam.fdate
    curr_date = htparam.fdate
    from_date = curr_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
    ba_dept = htparam.finteger
    readequipment()

    return generate_output()