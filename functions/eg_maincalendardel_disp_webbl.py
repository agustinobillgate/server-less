#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.eg_maincalendardel_gobl import eg_maincalendardel_gobl
from models import Zimmer, Eg_maintain

def eg_maincalendardel_disp_webbl(from_date:date, to_date:date, user_init:string, all_room:bool):
    groupid = 0
    engid = 0
    p_992 = False
    smaintain_data = []
    selected_date:date = None
    zimmer = eg_maintain = None

    t_zimmer = maintain = smaintain = tproperty = troom = tmaintask = tpic = tstatus = dept_link = tlocation = tcategory = t_eg_maintain = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    maintain_data, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int, "cancel_date":date, "cancel_time":int, "cancel_str":string, "cancel_by":string, "categnr":int})
    smaintain_data, Smaintain = create_model("Smaintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "stat_nr":int, "stat_nm":string, "categ_nr":int, "categ_nm":string, "main_nr":int, "main_nm":string, "loc_nr":int, "loc_nm":string, "prop_nr":int, "prop_nm":string, "pzinr":string, "pic_nr":int, "pic_nm":string, "str":string, "rec":string, "cancel_date":date, "cancel_time":int, "cancel_str":string, "cancel_by":string})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    dept_link_data, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    t_eg_maintain_data, T_eg_maintain = create_model_like(Eg_maintain)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, p_992, smaintain_data, selected_date, zimmer, eg_maintain
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, smaintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain
        nonlocal t_zimmer_data, maintain_data, smaintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        return {"groupid": groupid, "engid": engid, "p_992": p_992, "smaintain": smaintain_data}

    def fill_maintain():

        nonlocal groupid, engid, p_992, smaintain_data, selected_date, zimmer, eg_maintain
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, smaintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain
        nonlocal t_zimmer_data, maintain_data, smaintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        for maintain in query(maintain_data):
            tStatus = query(tstatus_data, (lambda tStatus: tStatus.stat_nr == maintain.type), first=True)
            if not tStatus:
                continue

            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == maintain.maintask), first=True)
            if not tmaintask:
                continue

            tlocation = query(tlocation_data, (lambda tlocation: tlocation.loc_nr == maintain.location), first=True)
            if not tlocation:
                continue

            tproperty = query(tproperty_data, (lambda tproperty: tproperty.prop_nr == maintain.propertynr), first=True)
            if not tproperty:
                continue

            tpic = query(tpic_data, (lambda tpic: tpic.pic_nr == maintain.pic), first=True)
            if not tpic:
                continue

            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == maintain.categnr), first=True)
            if not tcategory:
                continue

            create_temp()


    def create_temp():

        nonlocal groupid, engid, p_992, smaintain_data, selected_date, zimmer, eg_maintain
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, smaintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain
        nonlocal t_zimmer_data, maintain_data, smaintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data


        smaintain = Smaintain()
        smaintain_data.append(smaintain)

        smaintain.maintainnr = maintain.maintainnr
        smaintain.workdate = maintain.workdate
        smaintain.estworkdate = maintain.estworkdate
        smaintain.stat_nr = maintain.type
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


    groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data = get_output(eg_maincalendardel_gobl(from_date, to_date, user_init, all_room))
    fill_maintain()

    return generate_output()