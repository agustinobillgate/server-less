#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.eg_repmaintain_all_locationbl import eg_repmaintain_all_locationbl
from functions.eg_repmaintain_open_querybl import eg_repmaintain_open_querybl
from models import Eg_maintain

tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
tfrequency_list, Tfrequency = create_model("Tfrequency", {"freq_nr":int, "freq_nm":string})
tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool})

def eg_repmaintain_disp_webbl(all_room:bool, all_status:bool, all_location:bool, all_property:bool, all_pic:bool, fdate:date, tdate:date, main_date:int, tmaintask_list:[Tmaintask], tfrequency_list:[Tfrequency], tstatus_list:[Tstatus], tlocation_list:[Tlocation], troom_list:[Troom], tproperty_list:[Tproperty], tpic_list:[Tpic]):
    smaintain_list = []
    int_str:List[string] = ["Weekly", "Monthly", "Quarter", "Half Yearly", "Year"]
    eg_maintain = None

    t_eg_maintain = smaintain = tstatus = tlocation = tmaintask = troom = tproperty = tpic = tfrequency = None

    t_eg_maintain_list, T_eg_maintain = create_model_like(Eg_maintain)
    smaintain_list, Smaintain = create_model("Smaintain", {"maintainnr":int, "estworkdate":date, "workdate":date, "donedate":date, "stat_nr":int, "stat_nm":string, "freq":string, "category_str":string, "maintask":string, "location":string, "zinr":string, "property":string, "comments":string, "pic":string, "str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal smaintain_list, int_str, eg_maintain
        nonlocal all_room, all_status, all_location, all_property, all_pic, fdate, tdate, main_date


        nonlocal t_eg_maintain, smaintain, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tfrequency
        nonlocal t_eg_maintain_list, smaintain_list

        return {"tStatus": tstatus_list, "tLocation": tlocation_list, "troom": troom_list, "tproperty": tproperty_list, "tpic": tpic_list, "smaintain": smaintain_list}

    def create_temp():

        nonlocal smaintain_list, int_str, eg_maintain
        nonlocal all_room, all_status, all_location, all_property, all_pic, fdate, tdate, main_date


        nonlocal t_eg_maintain, smaintain, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tfrequency
        nonlocal t_eg_maintain_list, smaintain_list


        smaintain = Smaintain()
        smaintain_list.append(smaintain)

        smaintain.maintainnr = t_eg_maintain.maintainnr
        smaintain.estworkdate = t_eg_maintain.estWorkDate
        smaintain.workdate = t_eg_maintain.workdate
        smaintain.donedate = t_eg_maintain.donedate
        smaintain.stat_nr = t_eg_maintain.type
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
    troom_list, tproperty_list = get_output(eg_repmaintain_all_locationbl(all_room, tlocation_list, tmaintask_list))

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
            tLocation = query(tlocation_list, (lambda tLocation: tLocation.loc_nr == t_eg_maintain.location and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_list, (lambda tproperty: tproperty.prop_nr == t_eg_maintain.propertynr and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == t_eg_maintain.type and tstatus.stat_selected), first=True)
            if not tstatus:
                continue

            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == t_eg_maintain.pic and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tfrequency = query(tfrequency_list, (lambda tfrequency: tfrequency.freq_nr == t_eg_maintain.type), first=True)
            if not tfrequency:
                continue

            create_temp()

    elif main_date == 2:

        for t_eg_maintain in query(t_eg_maintain_list):
            tLocation = query(tlocation_list, (lambda tLocation: tLocation.loc_nr == t_eg_maintain.location and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_list, (lambda tproperty: tproperty.prop_nr == t_eg_maintain.propertynr and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == t_eg_maintain.type and tstatus.stat_selected), first=True)
            if not tstatus:
                continue

            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == t_eg_maintain.pic and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tfrequency = query(tfrequency_list, (lambda tfrequency: tfrequency.freq_nr == t_eg_maintain.type), first=True)
            if not tfrequency:
                continue

            create_temp()

    elif main_date == 3:

        for t_eg_maintain in query(t_eg_maintain_list):
            tLocation = query(tlocation_list, (lambda tLocation: tLocation.loc_nr == t_eg_maintain.location and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_list, (lambda tproperty: tproperty.prop_nr == t_eg_maintain.propertynr and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == t_eg_maintain.type and tstatus.stat_selected), first=True)
            if not tstatus:
                continue

            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == t_eg_maintain.pic and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tfrequency = query(tfrequency_list, (lambda tfrequency: tfrequency.freq_nr == t_eg_maintain.type), first=True)
            if not tfrequency:
                continue

            create_temp()

    return generate_output()