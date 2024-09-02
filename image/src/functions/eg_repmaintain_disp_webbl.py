from functions.additional_functions import *
import decimal
from datetime import date
from functions.eg_repmaintain_all_locationbl import eg_repmaintain_all_locationbl
from functions.eg_repmaintain_open_querybl import eg_repmaintain_open_querybl
from models import Eg_maintain

def eg_repmaintain_disp_webbl(all_room:bool, all_status:bool, all_location:bool, all_property:bool, all_pic:bool, fdate:date, tdate:date, main_date:int, tmaintask:[Tmaintask], tfrequency:[Tfrequency], tstatus:[Tstatus], tlocation:[Tlocation], troom:[Troom], tproperty:[Tproperty], tpic:[Tpic]):
    smaintain_list = []
    int_str:[str] = ["", "", "", "", "", "", ""]
    eg_maintain = None

    t_eg_maintain = smaintain = tstatus = tlocation = tmaintask = troom = tproperty = tpic = tfrequency = None

    t_eg_maintain_list, T_eg_maintain = create_model_like(Eg_maintain)
    smaintain_list, Smaintain = create_model("Smaintain", {"maintainnr":int, "estworkdate":date, "workdate":date, "donedate":date, "stat_nr":int, "stat_nm":str, "freq":str, "category_str":str, "maintask":str, "location":str, "zinr":str, "property":str, "comments":str, "pic":str, "str":str})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool})
    tfrequency_list, Tfrequency = create_model("Tfrequency", {"freq_nr":int, "freq_nm":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal smaintain_list, int_str, eg_maintain


        nonlocal t_eg_maintain, smaintain, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tfrequency
        nonlocal t_eg_maintain_list, smaintain_list, tstatus_list, tlocation_list, tmaintask_list, troom_list, tproperty_list, tpic_list, tfrequency_list
        return {"smaintain": smaintain_list}

    def create_temp():

        nonlocal smaintain_list, int_str, eg_maintain


        nonlocal t_eg_maintain, smaintain, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tfrequency
        nonlocal t_eg_maintain_list, smaintain_list, tstatus_list, tlocation_list, tmaintask_list, troom_list, tproperty_list, tpic_list, tfrequency_list


        smaintain = Smaintain()
        smaintain_list.append(smaintain)

        smaintain.maintainnr = t_eg_maintain.maintainnr
        smaintain.estWorkDate = t_eg_maintain.estWorkDate
        smaintain.workdate = t_eg_maintain.workdate
        smaintain.donedate = t_eg_maintain.donedate
        smaintain.stat_nr = t_eg_maintain.TYPE
        smaintain.stat_nm = tstatus.stat_nm
        smaintain.freq = int_str[t_eg_maintain.typework - 1]
        smaintain.category = tproperty.pcateg
        smaintain.maintask = tproperty.pmain
        smaintain.location = tLocation.loc_nm
        smaintain.zinr = t_eg_maintain.zinr
        smaintain.property = tproperty.prop_nm
        smaintain.comments = t_eg_maintain.comments
        smaintain.pic = tpic.pic_nm


    smaintain_list.clear()
    troom_list, tproperty_list = get_output(eg_repmaintain_all_locationbl(all_room, tLocation, tMaintask))

    if all_status:

        for tstatus in query(tstatus_list):
            tstatus.stat_selected = True


    if all_location:

        for tlocation in query(tlocation_list):
            tlocation.loc_selected = True


    if all_property:

        for tproperty in query(tproperty_list):
            tproperty.prop_selected = True


    if all_pic:

        for tpic in query(tpic_list):
            tpic.pic_selected = True

    t_eg_maintain_list = get_output(eg_repmaintain_open_querybl(fdate, tdate))

    if main_date == 1:

        for t_eg_maintain in query(t_eg_maintain_list):
            tLocation = db_session.query(TLocation).filter((TLocation.loc_nr == t_eg_maintain.location) &  (TLocation.loc_selected)).first()
            if not tLocation:
                continue

            tproperty = db_session.query(Tproperty).filter((Tproperty.prop_nr == t_eg_maintain.propertynr) &  (Tproperty.prop_selected)).first()
            if not tproperty:
                continue

            tstatus = db_session.query(Tstatus).filter((Tstatus.stat_nr == t_eg_maintain.TYPE) &  (Tstatus.stat_selected)).first()
            if not tstatus:
                continue

            tpic = db_session.query(Tpic).filter((Tpic.pic_nr == t_eg_maintain.pic) &  (Tpic.pic_selected)).first()
            if not tpic:
                continue

            tFrequency = db_session.query(TFrequency).filter((TFrequency.freq_nr == t_eg_maintain.TYPE)).first()
            if not tFrequency:
                continue

            create_temp()

    elif main_date == 2:

        for t_eg_maintain in query(t_eg_maintain_list):
            tLocation = db_session.query(TLocation).filter((TLocation.loc_nr == t_eg_maintain.location) &  (TLocation.loc_selected)).first()
            if not tLocation:
                continue

            tproperty = db_session.query(Tproperty).filter((Tproperty.prop_nr == t_eg_maintain.propertynr) &  (Tproperty.prop_selected)).first()
            if not tproperty:
                continue

            tstatus = db_session.query(Tstatus).filter((Tstatus.stat_nr == t_eg_maintain.TYPE) &  (Tstatus.stat_selected)).first()
            if not tstatus:
                continue

            tpic = db_session.query(Tpic).filter((Tpic.pic_nr == t_eg_maintain.pic) &  (Tpic.pic_selected)).first()
            if not tpic:
                continue

            tFrequency = db_session.query(TFrequency).filter((TFrequency.freq_nr == t_eg_maintain.TYPE)).first()
            if not tFrequency:
                continue

            create_temp()

    elif main_date == 3:

        for t_eg_maintain in query(t_eg_maintain_list):
            tLocation = db_session.query(TLocation).filter((TLocation.loc_nr == t_eg_maintain.location) &  (TLocation.loc_selected)).first()
            if not tLocation:
                continue

            tproperty = db_session.query(Tproperty).filter((Tproperty.prop_nr == t_eg_maintain.propertynr) &  (Tproperty.prop_selected)).first()
            if not tproperty:
                continue

            tstatus = db_session.query(Tstatus).filter((Tstatus.stat_nr == t_eg_maintain.TYPE) &  (Tstatus.stat_selected)).first()
            if not tstatus:
                continue

            tpic = db_session.query(Tpic).filter((Tpic.pic_nr == t_eg_maintain.pic) &  (Tpic.pic_selected)).first()
            if not tpic:
                continue

            tFrequency = db_session.query(TFrequency).filter((TFrequency.freq_nr == t_eg_maintain.TYPE)).first()
            if not tFrequency:
                continue

            create_temp()

    return generate_output()