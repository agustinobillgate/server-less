#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_staff

staff_list, Staff = create_model_like(Eg_staff)

def eg_staff_btn_exitbl(staff_list:[Staff], case_type:int, rec_id:int):

    prepare_cache ([Eg_staff])

    fl_code = 0
    eg_staff = None

    staff = queri = None

    Queri = create_buffer("Queri",Eg_staff)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_staff
        nonlocal case_type, rec_id
        nonlocal queri


        nonlocal staff, queri

        return {"fl_code": fl_code}

    staff = query(staff_list, first=True)

    if case_type == 1:
        eg_staff = Eg_staff()
        db_session.add(eg_staff)

        buffer_copy(staff, eg_staff)

    elif case_type == 2:

        eg_staff = get_cache (Eg_staff, {"_recid": [(eq, rec_id)]})

        queri = get_cache (Eg_staff, {"nr": [(eq, staff.nr)],"_recid": [(ne, eg_staff._recid)]})

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = get_cache (Eg_staff, {"name": [(eq, staff.name)],"_recid": [(ne, eg_staff._recid)]})

            if queri:
                fl_code = 2

                return generate_output()
            else:
                pass
                buffer_copy(staff, eg_staff)
                pass
                fl_code = 3

    return generate_output()