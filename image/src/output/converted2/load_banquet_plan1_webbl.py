#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_ba_planbl import prepare_ba_planbl
from functions.get_banquet_plan_infobl import get_banquet_plan_infobl
from functions.ba_plan_btn_notebl import ba_plan_btn_notebl
from functions.edit_baresnotebl import edit_baresnotebl
from functions.ba_plan_create_dlist_prevbl import ba_plan_create_dlist_prevbl
from functions.ba_plan_create_dlistbl import ba_plan_create_dlistbl
from functions.ba_plan_create_wlist_prevbl import ba_plan_create_wlist_prevbl
from functions.ba_plan_create_wlistbl import ba_plan_create_wlistbl
from models import Bk_raum

def load_banquet_plan1_webbl(curr_view:string, from_date:date):
    run_beowarning = False
    ba_dept = 0
    p_900 = 0
    ci_date = None
    mess_str = ""
    info1 = ""
    info2 = ""
    info3 = ""
    t_veran_nr = 0
    avail_mainres = False
    efield = ""
    rsl_list = []
    ba_plan_list = []
    zugriff:bool = False
    main_exist:bool = False
    curr_resnr:int = 0
    count_j:int = 0
    counter:int = 0
    str:string = ""
    gstat_found:bool = False
    end_gstat:bool = False
    bk_raum = None

    t_bk_raum = ba_plan = rsl = rsv_line = None

    t_bk_raum_list, T_bk_raum = create_model_like(Bk_raum)
    ba_plan_list, Ba_plan = create_model("Ba_plan", {"nr":int, "raum":string, "bezeich":string, "departement":int, "resnr":[int,48], "reslinnr":[int,48], "gstatus":[int,48], "room":[string,48], "blocked":[int,48]})
    rsl_list, Rsl = create_model("Rsl", {"resnr":int, "reslinnr":int, "resstatus":int, "sdate":date, "ndate":date, "stime":string, "ntime":string, "created_date":date, "venue":string, "userinit":string, "mess_str":string, "info1":string, "info2":string, "info3":string, "t_veran_nr":int, "efield":string})
    rsv_line_list, Rsv_line = create_model("Rsv_line", {"resnr":int, "reslinnr":int, "resstatus":int, "sdate":date, "ndate":date, "stime":string, "ntime":string, "created_date":date, "venue":string, "userinit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal run_beowarning, ba_dept, p_900, ci_date, mess_str, info1, info2, info3, t_veran_nr, avail_mainres, efield, rsl_list, ba_plan_list, zugriff, main_exist, curr_resnr, count_j, counter, str, gstat_found, end_gstat, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan, rsl, rsv_line
        nonlocal t_bk_raum_list, ba_plan_list, rsl_list, rsv_line_list

        return {"run_beowarning": run_beowarning, "ba_dept": ba_dept, "p_900": p_900, "ci_date": ci_date, "mess_str": mess_str, "info1": info1, "info2": info2, "info3": info3, "t_veran_nr": t_veran_nr, "avail_mainres": avail_mainres, "efield": efield, "rsl": rsl_list, "ba-plan": ba_plan_list}

    def create_rlist():

        nonlocal run_beowarning, ba_dept, p_900, ci_date, mess_str, info1, info2, info3, t_veran_nr, avail_mainres, efield, rsl_list, ba_plan_list, zugriff, main_exist, curr_resnr, count_j, counter, str, gstat_found, end_gstat, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan, rsl, rsv_line
        nonlocal t_bk_raum_list, ba_plan_list, rsl_list, rsv_line_list

        for t_bk_raum in query(t_bk_raum_list, sort_by=[("bezeich",False)]):
            ba_plan = Ba_plan()
            ba_plan_list.append(ba_plan)

            ba_plan.nr = 1
            ba_plan.raum = t_bk_raum.raum
            ba_plan.bezeich = t_bk_raum.bezeich
            ba_plan.departement = t_bk_raum.departement
            ba_plan = Ba_plan()
            ba_plan_list.append(ba_plan)

            ba_plan.nr = 2
            ba_plan.raum = t_bk_raum.raum
            ba_plan.bezeich = t_bk_raum.bezeich
            ba_plan.departement = t_bk_raum.departement
            ba_plan = Ba_plan()
            ba_plan_list.append(ba_plan)

            ba_plan.nr = 3
            ba_plan.raum = t_bk_raum.raum
            ba_plan.bezeich = t_bk_raum.bezeich
            ba_plan.departement = t_bk_raum.departement


    def create_dlist_prev():

        nonlocal run_beowarning, ba_dept, p_900, ci_date, mess_str, info1, info2, info3, t_veran_nr, avail_mainres, efield, rsl_list, ba_plan_list, zugriff, main_exist, curr_resnr, count_j, counter, str, gstat_found, end_gstat, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan, rsl, rsv_line
        nonlocal t_bk_raum_list, ba_plan_list, rsl_list, rsv_line_list

        i:int = 0

        if not main_exist:
            curr_resnr = 0

        for ba_plan in query(ba_plan_list):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


            i = 1
        ba_plan_list = get_output(ba_plan_create_dlist_prevbl(ba_plan_list, from_date))


    def create_dlist():

        nonlocal run_beowarning, ba_dept, p_900, ci_date, mess_str, info1, info2, info3, t_veran_nr, avail_mainres, efield, rsl_list, ba_plan_list, zugriff, main_exist, curr_resnr, count_j, counter, str, gstat_found, end_gstat, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan, rsl, rsv_line
        nonlocal t_bk_raum_list, ba_plan_list, rsl_list, rsv_line_list

        i:int = 0

        if not main_exist:
            curr_resnr = 0

        for ba_plan in query(ba_plan_list):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


        ba_plan_list = get_output(ba_plan_create_dlistbl(ba_plan_list, from_date))


    def create_wlist_prev():

        nonlocal run_beowarning, ba_dept, p_900, ci_date, mess_str, info1, info2, info3, t_veran_nr, avail_mainres, efield, rsl_list, ba_plan_list, zugriff, main_exist, curr_resnr, count_j, counter, str, gstat_found, end_gstat, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan, rsl, rsv_line
        nonlocal t_bk_raum_list, ba_plan_list, rsl_list, rsv_line_list

        i:int = 0
        rmbuff = None
        childrm = None
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)
        curr_resnr = 0

        for ba_plan in query(ba_plan_list):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


        ba_plan_list = get_output(ba_plan_create_wlist_prevbl(ba_plan_list, from_date))


    def create_wlist():

        nonlocal run_beowarning, ba_dept, p_900, ci_date, mess_str, info1, info2, info3, t_veran_nr, avail_mainres, efield, rsl_list, ba_plan_list, zugriff, main_exist, curr_resnr, count_j, counter, str, gstat_found, end_gstat, bk_raum
        nonlocal curr_view, from_date


        nonlocal t_bk_raum, ba_plan, rsl, rsv_line
        nonlocal t_bk_raum_list, ba_plan_list, rsl_list, rsv_line_list

        i:int = 0
        rmbuff = None
        childrm = None
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)
        curr_resnr = 0

        for ba_plan in query(ba_plan_list):
            for i in range(1,48 + 1) :
                ba_plan.gstatus[i - 1] = 0
                ba_plan.room[i - 1] = ""
                ba_plan.resnr[i - 1] = 0
                ba_plan.reslinnr[i - 1] = 0
                ba_plan.blocked[i - 1] = 0


        ba_plan_list = get_output(ba_plan_create_wlistbl(ba_plan_list, from_date))


    ci_date, ba_dept, run_beowarning, p_900, t_bk_raum_list = get_output(prepare_ba_planbl())
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

    for ba_plan in query(ba_plan_list):
        counter = 0
        gstat_found = False
        for count_j in range(1,48 + 1) :
            counter = counter + 1

            if ba_plan.gstatus[count_j - 1] != 0:

                if count_j <= 47:

                    if ba_plan.gstatus[count_j + 1 - 1] == 0:
                        gstat_found = True
                        break

                elif count_j == 48 and ba_plan.gstatus[count_j - 1] != 0:
                    gstat_found = True
                    break

        if gstat_found:
            for count_j in range(1,48 + 1) :

                if ba_plan.resnr[count_j - 1] == 0:
                    continue
                else:
                    mess_str, info1, info2, info3, rsv_line_list = get_output(get_banquet_plan_infobl(curr_view, ba_plan.bezeich, ba_plan.raum, ba_plan.nr, ba_plan.blocked[count_j - 1], ba_plan.resnr[count_j - 1], ba_plan.reslinnr[count_j - 1], counter, from_date))
                    t_veran_nr, avail_mainres = get_output(ba_plan_btn_notebl(ba_plan.resnr[count_j - 1]))

                    if avail_mainres:
                        efield = get_output(edit_baresnotebl(ba_plan.resnr[count_j - 1]))

                    for rsv_line in query(rsv_line_list):
                        rsl = Rsl()
                        rsl_list.append(rsl)

                        buffer_copy(rsv_line, rsl)
                        rsl.mess_str = mess_str
                        rsl.info1 = info1
                        rsl.info2 = info2
                        rsl.info3 = info3
                        rsl.t_veran_nr = t_veran_nr
                        rsl.efield = efield

    return generate_output()