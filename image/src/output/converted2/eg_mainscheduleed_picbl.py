#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_staff

def eg_mainscheduleed_picbl(engid:int, m_pic:int):

    prepare_cache ([Eg_staff])

    avail_eg_staff = False
    e_nr = 0
    e_name = ""
    staff_list = []
    eg_staff = None

    staff = None

    staff_list, Staff = create_model_like(Eg_staff, {"staff_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_eg_staff, e_nr, e_name, staff_list, eg_staff
        nonlocal engid, m_pic


        nonlocal staff
        nonlocal staff_list

        return {"avail_eg_staff": avail_eg_staff, "e_nr": e_nr, "e_name": e_name, "staff": staff_list}

    def create_staff():

        nonlocal avail_eg_staff, e_nr, e_name, staff_list, eg_staff
        nonlocal engid, m_pic


        nonlocal staff
        nonlocal staff_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        staff_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff._recid).all():
            staff = Staff()
            staff_list.append(staff)

            staff.nr = qbuff.nr
            staff.name = qbuff.name
            staff.staff_selected = False


    eg_staff = get_cache (Eg_staff, {"usergroup": [(eq, engid)],"activeflag": [(eq, True)],"nr": [(eq, m_pic)]})

    if eg_staff:
        avail_eg_staff = True
        e_nr = eg_staff.nr
        e_name = eg_staff.name
        create_staff()

    return generate_output()