from functions.additional_functions import *
import decimal
from models import Htparam, Hoteldpt

def select_deptbl(from_dept:int, to_dept:int):
    depname1 = ""
    depname2 = ""
    ldry:int = 0
    dstore:int = 0
    min_dept:int = 99
    max_dept:int = 0
    htparam = hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal depname1, depname2, ldry, dstore, min_dept, max_dept, htparam, hoteldpt
        nonlocal from_dept, to_dept


        return {"from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1081)).first()
    ldry = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1082)).first()
    dstore = htparam.finteger
    min_dept = 999
    max_dept = 1

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

        if min_dept > hoteldpt.num:
            min_dept = hoteldpt.num

        if max_dept < hoteldpt.num:
            max_dept = hoteldpt.num
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = db_session.query(Hoteldpt).filter(
             (Hoteldpt.num == from_dept)).first()
    depname1 = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
             (Hoteldpt.num == to_dept)).first()
    depname2 = hoteldpt.depart

    return generate_output()