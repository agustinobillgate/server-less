from functions.additional_functions import *
import decimal
from functions.prepare_rwaiter_adminbl import prepare_rwaiter_adminbl
from models import Kellner, Kellne1

def rwaiter_admin_btn_exitbl(t_list:[T_list], case_type:int, dept:int, curr_mode:str, kzahl_nr1:int, kumsatz_nr1:int, r_kellner:int, r_kellne1:int):
    q1_list_list = []
    t_kellner_list = []
    kellner = kellne1 = None

    t_kellner = q1_list = t_list = waiter1 = None

    t_kellner_list, T_kellner = create_model_like(Kellner)
    q1_list_list, Q1_list = create_model("Q1_list", {"kellner_nr":int, "kellnername":str, "kumsatz_nr":int, "kumsatz_nr1":int, "kcredit_nr":int, "kzahl_nr":int, "kzahl_nr1":int, "masterkey":bool, "sprachcode":int, "r_kellner":int, "r_kellne1":int})
    t_list_list, T_list = create_model_like(Kellner)

    Waiter1 = Kellne1

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, t_kellner_list, kellner, kellne1
        nonlocal waiter1


        nonlocal t_kellner, q1_list, t_list, waiter1
        nonlocal t_kellner_list, q1_list_list, t_list_list
        return {"q1-list": q1_list_list, "t-kellner": t_kellner_list}

    def fill_new_kellner():

        nonlocal q1_list_list, t_kellner_list, kellner, kellne1
        nonlocal waiter1


        nonlocal t_kellner, q1_list, t_list, waiter1
        nonlocal t_kellner_list, q1_list_list, t_list_list


        Waiter1 = Kellne1
        kellner.departement = dept
        kellner_nr = t_list.kellner_nr
        kellnername = t_list.kellnername
        kellner.kumsatz_nr = t_list.kumsatz_nr
        kellner.kcredit_nr = t_list.kcredit_nr
        kellner.kzahl_nr = t_list.kzahl_nr
        kellner.masterkey = t_list.masterkey
        kellner.sprachcode = t_list.sprachcode

        if curr_mode.lower()  == "chg":
            kellne1.kzahl_nr = kzahl_nr1
            kellne1.kumsatz_nr = kumsatz_nr1

        elif curr_mode.lower()  == "add":
            waiter1 = Waiter1()
            db_session.add(waiter1)

            waiter1.departement = dept
            waiter1.kellner_nr = t_list.kellner_nr
            waiter1.kzahl_nr = kzahl_nr1
            waiter1.kumsatz_nr = kumsatz_nr1

    t_list = query(t_list_list, first=True)

    if case_type == 1:
        kellner = Kellner()
        db_session.add(kellner)

        fill_new_kellner()

    elif case_type == 2:

        kellner = db_session.query(Kellner).filter(
                (Kellner._recid == r_kellner)).first()

        kellne1 = db_session.query(Kellne1).filter(
                (Kellne1._recid == r_kellne1)).first()

        kellner = db_session.query(Kellner).first()

        kellne1 = db_session.query(Kellne1).first()
        fill_new_kellner()
    q1_list_list, t_kellner_list = get_output(prepare_rwaiter_adminbl(dept))

    return generate_output()