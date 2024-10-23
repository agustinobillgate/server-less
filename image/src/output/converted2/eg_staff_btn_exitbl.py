from functions.additional_functions import *
import decimal
from models import Eg_staff

staff_list, Staff = create_model_like(Eg_staff)

def eg_staff_btn_exitbl(staff_list:[Staff], case_type:int, rec_id:int):
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
        nonlocal staff_list
        return {"fl_code": fl_code}

    staff = query(staff_list, first=True)

    if case_type == 1:
        eg_staff = Eg_staff()
        db_session.add(eg_staff)

        buffer_copy(staff, eg_staff)

    elif case_type == 2:

        eg_staff = db_session.query(Eg_staff).filter(
                 (Eg_staff._recid == rec_id)).first()

        queri = db_session.query(Queri).filter(
                 (Queri.Nr == staff.Nr) & (Queri._recid != eg_staff._recid)).first()

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = db_session.query(Queri).filter(
                     (Queri.name == staff.name) & (Queri._recid != eg_staff._recid)).first()

            if queri:
                fl_code = 2

                return generate_output()
            else:
                buffer_copy(staff, eg_staff)
                fl_code = 3

    return generate_output()