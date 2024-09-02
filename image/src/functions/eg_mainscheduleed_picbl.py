from functions.additional_functions import *
import decimal
from models import Eg_staff

def eg_mainscheduleed_picbl(engid:int, m_pic:int):
    avail_eg_staff = False
    e_nr = 0
    e_name = ""
    staff_list = []
    eg_staff = None

    staff = qbuff = None

    staff_list, Staff = create_model_like(Eg_staff, {"staff_selected":bool})

    Qbuff = Eg_staff

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_eg_staff, e_nr, e_name, staff_list, eg_staff
        nonlocal qbuff


        nonlocal staff, qbuff
        nonlocal staff_list
        return {"avail_eg_staff": avail_eg_staff, "e_nr": e_nr, "e_name": e_name, "staff": staff_list}

    def create_staff():

        nonlocal avail_eg_staff, e_nr, e_name, staff_list, eg_staff
        nonlocal qbuff


        nonlocal staff, qbuff
        nonlocal staff_list


        Qbuff = Eg_staff
        staff_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usergroup == engid) &  (Qbuff.activeflag)).all():
            staff = Staff()
            staff_list.append(staff)

            staff.nr = qbuff.nr
            staff.name = qbuff.name
            staff.staff_SELECTED = False

    eg_staff = db_session.query(Eg_staff).filter(
            (Eg_staff.usergroup == engid) &  (Eg_staff.activeflag) &  (Eg_staff.nr == m_pic)).first()

    if eg_staff:
        avail_eg_staff = True
        e_nr = eg_staff.nr
        e_name = eg_staff.name
        create_staff()

    return generate_output()