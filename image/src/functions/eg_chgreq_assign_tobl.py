from functions.additional_functions import *
import decimal
from models import Eg_staff

def eg_chgreq_assign_tobl(request1_deptnum:int, request1_assign_to:int):
    avail_usr = False
    usr_name = ""
    eg_staff = None

    usr1 = None

    Usr1 = Eg_staff

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_usr, usr_name, eg_staff
        nonlocal usr1


        nonlocal usr1
        return {"avail_usr": avail_usr, "usr_name": usr_name}


    usr1 = db_session.query(Usr1).filter(
            (Usr1.usergroup == request1_deptnum) &  (Usr1.activeflag) &  (Usr1.nr == request1_assign_to)).first()

    if usr1:
        avail_usr = True
        usr_name = usr1.name

    return generate_output()