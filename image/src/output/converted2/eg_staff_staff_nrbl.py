from functions.additional_functions import *
import decimal
from models import Eg_staff

def eg_staff_staff_nrbl(rec_id:int, staff_nr:int, curr_select:str):
    avail_sub = False
    eg_staff = None

    sub = None

    Sub = create_buffer("Sub",Eg_staff)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_staff
        nonlocal rec_id, staff_nr, curr_select
        nonlocal sub


        nonlocal sub
        return {"avail_sub": avail_sub}


    eg_staff = db_session.query(Eg_staff).filter(
             (Eg_staff._recid == rec_id)).first()

    if curr_select.lower()  == ("chg").lower() :

        sub = db_session.query(Sub).filter(
                 (Sub.nr == staff_nr) & (Sub._recid != eg_staff._recid)).first()

    elif curr_select.lower()  == ("add").lower() :

        sub = db_session.query(Sub).filter(
                 (Sub.nr == staff_nr)).first()

    if sub:
        avail_sub = True

    return generate_output()