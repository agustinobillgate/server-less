#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Eg_staff, Queasy

def prepare_eg_kpibl():

    prepare_cache ([Queasy])

    tpic_data = []
    tmaintask_data = []
    bediener = eg_staff = queasy = None

    kpi_list = tpic = tlocation = troom = tmaintask = t_bediener = None

    kpi_list_data, Kpi_list = create_model("Kpi_list", {"name1":string, "new1":int, "processed1":int, "done1":int, "postponed1":int, "closed1":int})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    t_bediener_data, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tpic_data, tmaintask_data, bediener, eg_staff, queasy


        nonlocal kpi_list, tpic, tlocation, troom, tmaintask, t_bediener
        nonlocal kpi_list_data, tpic_data, tlocation_data, troom_data, tmaintask_data, t_bediener_data

        return {"tpic": tpic_data, "tMaintask": tmaintask_data}

    def define_group():

        nonlocal tpic_data, tmaintask_data, bediener, eg_staff, queasy


        nonlocal kpi_list, tpic, tlocation, troom, tmaintask, t_bediener
        nonlocal kpi_list_data, tpic_data, tlocation_data, troom_data, tmaintask_data, t_bediener_data

        for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    def create_pic():

        nonlocal tpic_data, tmaintask_data, bediener, eg_staff, queasy


        nonlocal kpi_list, tpic, tlocation, troom, tmaintask, t_bediener
        nonlocal kpi_list_data, tpic_data, tlocation_data, troom_data, tmaintask_data, t_bediener_data

        qbuff = None
        qbuff1 = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        Qbuff1 =  create_buffer("Qbuff1",Bediener)
        tpic_data.clear()
        tpic = Tpic()
        tpic_data.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_data.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False


    def create_maintask():

        nonlocal tpic_data, tmaintask_data, bediener, eg_staff, queasy


        nonlocal kpi_list, tpic, tlocation, troom, tmaintask, t_bediener
        nonlocal kpi_list_data, tpic_data, tlocation_data, troom_data, tmaintask_data, t_bediener_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tmaintask_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            tmaintask = Tmaintask()
            tmaintask_data.append(tmaintask)

            tmaintask.main_nr = qbuff.number1
            tmaintask.main_nm = qbuff.char1
            tmaintask.main_selected = False


    define_group()
    create_pic()
    create_maintask()

    return generate_output()