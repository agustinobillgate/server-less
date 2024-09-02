from functions.additional_functions import *
import decimal
from models import Hoteldpt, Kellner

def ldry1_report_select_userbl(ldry_dept:int):
    q2_list_list = []
    hoteldpt = kellner = None

    q2_list = None

    q2_list_list, Q2_list = create_model("Q2_list", {"departement":int, "depart":str, "kellner_nr":int, "kellnername":str, "recid_kellner":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_list, hoteldpt, kellner


        nonlocal q2_list
        nonlocal q2_list_list
        return {"q2-list": q2_list_list}

    kellner_obj_list = []
    for kellner, hoteldpt in db_session.query(Kellner, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == Kellner.departement)).filter(
            (Kellner.departement == ldry_dept)).all():
        if kellner._recid in kellner_obj_list:
            continue
        else:
            kellner_obj_list.append(kellner._recid)


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.departement = kellner.departement
        q2_list.depart = hoteldpt.depart
        q2_list.kellner_nr = kellner_nr
        q2_list.kellnername = kellnername
        q2_list.recid_kellner = kellner._recid

    return generate_output()