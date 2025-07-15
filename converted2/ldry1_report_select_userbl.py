#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Kellner

def ldry1_report_select_userbl(ldry_dept:int):

    prepare_cache ([Hoteldpt, Kellner])

    q2_list_data = []
    hoteldpt = kellner = None

    q2_list = None

    q2_list_data, Q2_list = create_model("Q2_list", {"departement":int, "depart":string, "kellner_nr":int, "kellnername":string, "recid_kellner":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_data, hoteldpt, kellner
        nonlocal ldry_dept


        nonlocal q2_list
        nonlocal q2_list_data

        return {"q2-list": q2_list_data}

    kellner_obj_list = {}
    kellner = Kellner()
    hoteldpt = Hoteldpt()
    for kellner.departement, kellner.kellner_nr, kellner.kellnername, kellner._recid, hoteldpt.depart, hoteldpt._recid in db_session.query(Kellner.departement, Kellner.kellner_nr, Kellner.kellnername, Kellner._recid, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num == Kellner.departement)).filter(
             (Kellner.departement == ldry_dept)).order_by(Kellner.kellner_nr).all():
        if kellner_obj_list.get(kellner._recid):
            continue
        else:
            kellner_obj_list[kellner._recid] = True


        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        q2_list.departement = kellner.departement
        q2_list.depart = hoteldpt.depart
        q2_list.kellner_nr = kellner.kellner_nr
        q2_list.kellnername = kellner.kellnername
        q2_list.recid_kellner = kellner._recid

    return generate_output()