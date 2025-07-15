#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_ba_planbl import prepare_ba_planbl
from functions.ba_plan_create_dlist_prevbl import ba_plan_create_dlist_prevbl
from functions.ba_plan_create_dlistbl import ba_plan_create_dlistbl
from functions.ba_plan_create_wlist_prevbl import ba_plan_create_wlist_prevbl
from functions.ba_plan_create_wlistbl import ba_plan_create_wlistbl
from models import Bk_raum

def load_banquet_planbl(curr_view:string, from_date:date):
    zugriff:bool = False
    main_exist:bool = False
    curr_resnr:int = 0
    run_beowarning = False
    ba_dept = 0
    p_900 = 0
    ci_date = None
    ba_plan_data = []
    bk_raum = None

    t_bk_raum = ba_plan = None

    t_bk_raum_data, T_bk_raum = create_model_like(Bk_raum)
    ba_plan_data, Ba_plan = create_model("Ba_plan", {"nr":int, "raum":string, "bezeich":string, "departement":int, "resnr":[int,48], "reslinnr":[int,48], "gstatus":[int,48], "room":[string,48], "blocked":[int,48]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zugriff, main_exist, curr_resnr, run_beowarning, ba_dept, p_900, ci_date, ba_plan_data, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan
        nonlocal t_bk_raum_data, ba_plan_data

        return {"run_beowarning": run_beowarning, "ba_dept": ba_dept, "p_900": p_900, "ci_date": ci_date, "ba-plan": ba_plan_data}

    def create_rlist():

        nonlocal zugriff, main_exist, curr_resnr, run_beowarning, ba_dept, p_900, ci_date, ba_plan_data, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan
        nonlocal t_bk_raum_data, ba_plan_data

        for t_bk_raum in query(t_bk_raum_data, sort_by=[("bezeich",False)]):
            ba_plan = Ba_plan()
            ba_plan_data.append(ba_plan)

            ba_plan.nr = 1
            ba_plan.raum = t_bk_raum.raum
            ba_plan.bezeich = t_bk_raum.bezeich
            ba_plan.departement = t_bk_raum.departement
            ba_plan = Ba_plan()
            ba_plan_data.append(ba_plan)

            ba_plan.nr = 2
            ba_plan.raum = t_bk_raum.raum
            ba_plan.bezeich = t_bk_raum.bezeich
            ba_plan.departement = t_bk_raum.departement
            ba_plan = Ba_plan()
            ba_plan_data.append(ba_plan)

            ba_plan.nr = 3
            ba_plan.raum = t_bk_raum.raum
            ba_plan.bezeich = t_bk_raum.bezeich
            ba_plan.departement = t_bk_raum.departement


    def create_dlist_prev():

        nonlocal zugriff, main_exist, curr_resnr, run_beowarning, ba_dept, p_900, ci_date, ba_plan_data, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan
        nonlocal t_bk_raum_data, ba_plan_data

        i:int = 0

        if not main_exist:
            curr_resnr = 0

        for ba_plan in query(ba_plan_data):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


            i = 1
        ba_plan_data = get_output(ba_plan_create_dlist_prevbl(ba_plan_data, from_date))


    def create_dlist():

        nonlocal zugriff, main_exist, curr_resnr, run_beowarning, ba_dept, p_900, ci_date, ba_plan_data, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan
        nonlocal t_bk_raum_data, ba_plan_data

        i:int = 0

        if not main_exist:
            curr_resnr = 0

        for ba_plan in query(ba_plan_data):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


        ba_plan_data = get_output(ba_plan_create_dlistbl(ba_plan_data, from_date))


    def create_wlist_prev():

        nonlocal zugriff, main_exist, curr_resnr, run_beowarning, ba_dept, p_900, ci_date, ba_plan_data, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan
        nonlocal t_bk_raum_data, ba_plan_data

        i:int = 0
        rmbuff = None
        childrm = None
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)
        curr_resnr = 0

        for ba_plan in query(ba_plan_data):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


        ba_plan_data = get_output(ba_plan_create_wlist_prevbl(ba_plan_data, from_date))


    def create_wlist():

        nonlocal zugriff, main_exist, curr_resnr, run_beowarning, ba_dept, p_900, ci_date, ba_plan_data, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan
        nonlocal t_bk_raum_data, ba_plan_data

        i:int = 0
        rmbuff = None
        childrm = None
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)
        curr_resnr = 0

        for ba_plan in query(ba_plan_data):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


        ba_plan_data = get_output(ba_plan_create_wlistbl(ba_plan_data, from_date))


    ci_date, ba_dept, run_beowarning, p_900, t_bk_raum_data = get_output(prepare_ba_planbl())
    create_rlist()

    if from_date >= ci_date:

        if curr_view.lower()  == ("daily").lower() :
            create_dlist()
        else:
            create_wlist()
    else:

        if curr_view.lower()  == ("daily").lower() :
            create_dlist_prev()
        else:
            create_wlist_prev()

    return generate_output()