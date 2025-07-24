#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd 24/7/2025
# gitlab: 853
# add sprachcode if "" -> None
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from functions.prepare_rwaiter_adminbl import prepare_rwaiter_adminbl
from models import Kellner, Kellne1

t_list_data, T_list = create_model_like(Kellner)

def rwaiter_admin_btn_exitbl(t_list_data:[T_list], case_type:int, dept:int, curr_mode:string, kzahl_nr1:int, kumsatz_nr1:int, r_kellner:int, r_kellne1:int):

    prepare_cache ([Kellner, Kellne1])

    q1_list_data = []
    t_kellner_data = []
    kellner = kellne1 = None

    t_kellner = q1_list = t_list = None

    t_kellner_data, T_kellner = create_model_like(Kellner)
    q1_list_data, Q1_list = create_model("Q1_list", {"kellner_nr":int, "kellnername":string, "kumsatz_nr":int, "kumsatz_nr1":int, "kcredit_nr":int, "kzahl_nr":int, "kzahl_nr1":int, "masterkey":bool, "sprachcode":int, "r_kellner":int, "r_kellne1":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, t_kellner_data, kellner, kellne1
        nonlocal case_type, dept, curr_mode, kzahl_nr1, kumsatz_nr1, r_kellner, r_kellne1


        nonlocal t_kellner, q1_list, t_list
        nonlocal t_kellner_data, q1_list_data

        return {"q1-list": q1_list_data, "t-kellner": t_kellner_data}

    def fill_new_kellner():

        nonlocal q1_list_data, t_kellner_data, kellner, kellne1
        nonlocal case_type, dept, curr_mode, kzahl_nr1, kumsatz_nr1, r_kellner, r_kellne1


        nonlocal t_kellner, q1_list, t_list
        nonlocal t_kellner_data, q1_list_data

        # Rd 24/7/2025
        if t_list.sprachcode == "":
            t_list.sprachcode = None  

        waiter1 = None
        Waiter1 =  create_buffer("Waiter1",Kellne1)
        kellner.departement = dept
        kellner.kellner_nr = t_list.kellner_nr
        kellner.kellnername = t_list.kellnername
        kellner.kumsatz_nr = t_list.kumsatz_nr
        kellner.kcredit_nr = t_list.kcredit_nr
        kellner.kzahl_nr = t_list.kzahl_nr
        kellner.masterkey = t_list.masterkey
        kellner.sprachcode = t_list.sprachcode

        if curr_mode.lower()  == ("chg").lower() :
            kellne1.kzahl_nr = kzahl_nr1
            kellne1.kumsatz_nr = kumsatz_nr1

        elif curr_mode.lower()  == ("add").lower() :
            waiter1 = Kellne1()
            db_session.add(waiter1)

            waiter1.departement = dept
            waiter1.kellner_nr = t_list.kellner_nr
            waiter1.kzahl_nr = kzahl_nr1
            waiter1.kumsatz_nr = kumsatz_nr1

    

    t_list = query(t_list_data, first=True)

    if case_type == 1:
        kellner = Kellner()
        db_session.add(kellner)

        fill_new_kellner()

    elif case_type == 2:

        kellner = get_cache (Kellner, {"_recid": [(eq, r_kellner)]})

        kellne1 = get_cache (Kellne1, {"_recid": [(eq, r_kellne1)]})

        if kellner and kellne1:
            pass
            pass
            fill_new_kellner()
            pass
            pass
            pass
            pass
    q1_list_data, t_kellner_data = get_output(prepare_rwaiter_adminbl(dept))

    return generate_output()