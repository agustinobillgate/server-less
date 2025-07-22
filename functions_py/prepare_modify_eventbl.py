#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 22/7/2025
# gitlab: 998
# bezeich-> bezichnung
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_chg_start_end_cldbl import prepare_chg_start_end_cldbl
from functions.prepare_chg_bastatus_linebl import prepare_chg_bastatus_linebl
from functions.prepare_chg_roombl import prepare_chg_roombl
from models import Bk_reser, Bk_rset, Bk_setup, Bk_raum, Bk_func

def prepare_modify_eventbl(rml_resnr:int, rml_reslinnr:int, curr_date:date):

    prepare_cache ([Bk_reser])

    begin_time = ""
    ending_time = ""
    begin_i2 = 0
    ending_i2 = 0
    sorttype = 0
    bk_reser_resstatus = 0
    chg_date = None
    begin_i = 0
    ending_i = 0
    room_list_data = []
    table_setup_data = []
    rsv_table_data = []
    t_bk_reser_data = []
    breser_data = []
    update_ok:bool = False
    msg:int = 0
    ci_date:date = None
    r_recid:int = 0
    bk_reser = bk_rset = bk_setup = bk_raum = bk_func = None

    room_list = table_setup = rsv_table = t_bk_reser = bset = bsetup = braum = bfunc = breser = broom = rl = None

    room_list_data, Room_list = create_model("Room_list", {"room_id":string, "room_name":string})
    table_setup_data, Table_setup = create_model("Table_setup", {"room_id":string, "seating":string, "max_person":int, "assign_person":int})
    rsv_table_data, Rsv_table = create_model_like(Bk_reser, {"rec_id":int, "t_vorbereit":int})
    t_bk_reser_data, T_bk_reser = create_model_like(Bk_reser, {"rec_id":int})
    bset_data, Bset = create_model_like(Bk_rset)
    bsetup_data, Bsetup = create_model_like(Bk_setup)
    braum_data, Braum = create_model_like(Bk_raum, {"rmflag":bool})
    bfunc_data, Bfunc = create_model_like(Bk_func)
    breser_data, Breser = create_model_like(Bk_reser)

    Broom = Braum
    broom_data = braum_data

    Rl = create_buffer("Rl",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal begin_time, ending_time, begin_i2, ending_i2, sorttype, bk_reser_resstatus, chg_date, begin_i, ending_i, room_list_data, table_setup_data, rsv_table_data, t_bk_reser_data, breser_data, update_ok, msg, ci_date, r_recid, bk_reser, bk_rset, bk_setup, bk_raum, bk_func
        nonlocal rml_resnr, rml_reslinnr, curr_date
        nonlocal broom, rl


        nonlocal room_list, table_setup, rsv_table, t_bk_reser, bset, bsetup, braum, bfunc, breser, broom, rl
        nonlocal room_list_data, table_setup_data, rsv_table_data, t_bk_reser_data, bset_data, bsetup_data, braum_data, bfunc_data, breser_data

        return {"curr_date": curr_date, "begin_time": begin_time, "ending_time": ending_time, "begin_i2": begin_i2, "ending_i2": ending_i2, "sorttype": sorttype, "bk_reser_resstatus": bk_reser_resstatus, "chg_date": chg_date, "begin_i": begin_i, "ending_i": ending_i, "room-list": room_list_data, "table-setup": table_setup_data, "rsv-table": rsv_table_data, "t-bk-reser": t_bk_reser_data, "breser": breser_data}

    rl = get_cache (Bk_reser, {"veran_nr": [(eq, rml_resnr)],"veran_seite": [(eq, rml_reslinnr)]})

    # Rd 22/7/2025
    if rl is None:
        return generate_output()
    if rl:
        r_recid = rl._recid
    chg_date, ci_date, update_ok, begin_i2, ending_i2, begin_time, begin_i, ending_time, ending_i, msg, rsv_table_data, t_bk_reser_data = get_output(prepare_chg_start_end_cldbl(rml_resnr, rml_reslinnr, curr_date))
    sorttype, bk_reser_resstatus = get_output(prepare_chg_bastatus_linebl(r_recid))
    braum_data, bset_data, bsetup_data, bfunc_data, breser_data = get_output(prepare_chg_roombl())

    for bset in query(bset_data):

        braum = query(braum_data, filters=(lambda braum: braum.raum == bset.raum), first=True)

        bsetup = query(bsetup_data, filters=(lambda bsetup: bsetup.setup_id == bset.setup_id), first=True)

        bfunc = query(bfunc_data, filters=(lambda bfunc: bfunc.veran_nr == rml_resnr and bfunc.veran_seite == rml_reslinnr), first=True)
        table_setup = Table_setup()
        table_setup_data.append(table_setup)

        table_setup.room_id = braum.raum

        # Rd 22/7/2025
        # table_setup.seating = bsetup.bezeich
        table_setup.seating = bsetup.bezeichnung

        table_setup.max_person = bset.personen
        table_setup.assign_person = bfunc.rpersonen[0]

    for braum in query(braum_data):
        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.room_id = braum.raum
        room_list.room_name = braum.bezeich

    return generate_output()