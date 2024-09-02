from functions.additional_functions import *
import decimal
from datetime import date
from functions.eg_maincalendardel_gobl import eg_maincalendardel_gobl
from models import Zimmer, Eg_maintain

def eg_maincalendardel_disp_webbl(from_date:date, to_date:date, user_init:str, all_room:bool):
    groupid = 0
    engid = 0
    p_992 = False
    smaintain_list = []
    selected_date:date = None
    zimmer = eg_maintain = None

    t_zimmer = maintain = smaintain = tproperty = troom = tmaintask = tpic = tstatus = dept_link = tlocation = tcategory = t_eg_maintain = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":str, "propertynr":int, "pic":int, "cancel_date":date, "cancel_time":int, "cancel_str":str, "cancel_by":str, "categnr":int})
    smaintain_list, Smaintain = create_model("Smaintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "stat_nr":int, "stat_nm":str, "categ_nr":int, "categ_nm":str, "main_nr":int, "main_nm":str, "loc_nr":int, "loc_nm":str, "prop_nr":int, "prop_nm":str, "pzinr":str, "pic_nr":int, "pic_nm":str, "str":str, "rec":str, "cancel_date":date, "cancel_time":int, "cancel_str":str, "cancel_by":str})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":str})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    t_eg_maintain_list, T_eg_maintain = create_model_like(Eg_maintain)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, p_992, smaintain_list, selected_date, zimmer, eg_maintain


        nonlocal t_zimmer, maintain, smaintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain
        nonlocal t_zimmer_list, maintain_list, smaintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list
        return {"groupid": groupid, "engid": engid, "p_992": p_992, "smaintain": smaintain_list}

    def fill_maintain():

        nonlocal groupid, engid, p_992, smaintain_list, selected_date, zimmer, eg_maintain


        nonlocal t_zimmer, maintain, smaintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain
        nonlocal t_zimmer_list, maintain_list, smaintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list

        for maintain in query(maintain_list):
            tStatus = db_session.query(TStatus).filter((TStatus.stat_nr == maintain.TYPE)).first()
            if not tStatus:
                continue

            tmaintask = db_session.query(Tmaintask).filter((Tmaintask.main_nr == maintain.maintask)).first()
            if not tmaintask:
                continue

            tlocation = db_session.query(Tlocation).filter((Tlocation.loc_nr == maintain.location)).first()
            if not tlocation:
                continue

            tproperty = db_session.query(Tproperty).filter((Tproperty.prop_nr == maintain.propertynr)).first()
            if not tproperty:
                continue

            tpic = db_session.query(Tpic).filter((Tpic.pic_nr == maintain.pic)).first()
            if not tpic:
                continue

            tcategory = db_session.query(Tcategory).filter((Tcategory.categ_nr == maintain.categnr)).first()
            if not tcategory:
                continue

            create_temp()

    def create_temp():

        nonlocal groupid, engid, p_992, smaintain_list, selected_date, zimmer, eg_maintain


        nonlocal t_zimmer, maintain, smaintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain
        nonlocal t_zimmer_list, maintain_list, smaintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


        smaintain = Smaintain()
        smaintain_list.append(smaintain)

        smaintain.maintainnr = maintain.maintainnr
        smaintain.workdate = maintain.workdate
        smaintain.estworkdate = maintain.estworkdate
        smaintain.stat_nr = maintain.TYPE
        smaintain.stat_nm = tStatus.stat_nm
        smaintain.main_nr = maintain.maintask
        smaintain.main_nm = tmaintask.main_nm
        smaintain.loc_nr = maintain.location
        smaintain.loc_nm = tlocation.loc_nm
        smaintain.prop_nr = maintain.propertynr
        smaintain.prop_nm = tproperty.prop_nm + "(" + trim (to_string(maintain.propertynr , ">>>>>>9")) + ")"
        smaintain.pzinr = maintain.zinr
        smaintain.pic_nr = maintain.pic
        smaintain.pic_nm = tpic.pic_nm
        smaintain.cancel_date = maintain.cancel_date
        smaintain.cancel_time = maintain.cancel_time
        smaintain.cancel_str = maintain.cancel_str
        smaintain.cancel_by = maintain.cancel_by
        smaintain.categ_nr = maintain.categnr
        smaintain.categ_nm = tcategory.categ_nm

    groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tMaintask_list, tpic_list, tStatus_list, dept_link_list, tLocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list = get_output(eg_maincalendardel_gobl(from_date, to_date, user_init, all_room))
    fill_maintain()

    return generate_output()