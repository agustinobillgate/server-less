#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 18/8/2025
# 
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.eg_repmaintain_all_locationbl import eg_repmaintain_all_locationbl
from functions.eg_repmaintain_open_querybl import eg_repmaintain_open_querybl
from models import Eg_maintain

tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
tfrequency_data, Tfrequency = create_model("Tfrequency", {"freq_nr":int, "freq_nm":string})
tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool})

def eg_repmaintain_disp_webbl(all_room:bool, all_status:bool, all_location:bool, all_property:bool, all_pic:bool, fdate:date, tdate:date, main_date:int, 
                              tmaintask_data:[Tmaintask], 
                              tfrequency_data:[Tfrequency], 
                              tstatus_data:[Tstatus], 
                              tlocation_data:[Tlocation], 
                              troom_data:[Troom], 
                              tproperty_data:[Tproperty], 
                              tpic_data:[Tpic]):
    smaintain_data = []
    int_str:List[string] = ["Weekly", "Monthly", "Quarter", "Half Yearly", "Year"]
    eg_maintain = None
    t_eg_maintain = smaintain = tstatus = tlocation = tmaintask = troom = tproperty = tpic = tfrequency = None

    t_eg_maintain_data, T_eg_maintain = create_model_like(Eg_maintain)
    smaintain_data, Smaintain = create_model("Smaintain", {"maintainnr":int, "estworkdate":date, "workdate":date, "donedate":date, "stat_nr":int, "stat_nm":string, "freq":string, "category_str":string, "maintask":string, "location":string, "zinr":string, "property":string, "comments":string, "pic":string, "str":string})

    db_session = local_storage.db_session
    print("fdate:", fdate )
    print("tdate:", tdate )

    def generate_output():
        nonlocal smaintain_data, int_str, eg_maintain
        nonlocal all_room, all_status, all_location, all_property, all_pic, fdate, tdate, main_date


        nonlocal t_eg_maintain, smaintain, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tfrequency
        nonlocal t_eg_maintain_data, smaintain_data

        return {"tStatus": tstatus_data, "tLocation": tlocation_data, "troom": troom_data, "tproperty": tproperty_data, "tpic": tpic_data, "smaintain": smaintain_data}

    def create_temp():

        nonlocal smaintain_data, int_str, eg_maintain
        nonlocal all_room, all_status, all_location, all_property, all_pic, fdate, tdate, main_date


        nonlocal t_eg_maintain, smaintain, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tfrequency
        nonlocal t_eg_maintain_data, smaintain_data


        smaintain = Smaintain()
        smaintain_data.append(smaintain)

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


    smaintain_data.clear()
    troom_data, tproperty_data = get_output(eg_repmaintain_all_locationbl(all_room, tlocation_data, tmaintask_data))

    if all_status:

        for tstatus in query(tstatus_data):
            tstatus.stat_selected = True


    if all_location:

        for tlocation in query(tlocation_data):
            tlocation.loc_selected = True


    if all_property:

        for tproperty in query(tproperty_data):
            tproperty.prop_selected = True


    if all_pic:

        for tpic in query(tpic_data):
            tpic.pic_selected = True

    t_eg_maintain_data = get_output(eg_repmaintain_open_querybl(fdate, tdate))

    if main_date == 1:

        for t_eg_maintain in query(t_eg_maintain_data):
            tLocation = query(tlocation_data, (lambda tLocation: tLocation.loc_nr == t_eg_maintain.location and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_data, (lambda tproperty: tproperty.prop_nr == t_eg_maintain.propertynr and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == t_eg_maintain.type and tstatus.stat_selected), first=True)
            if not tstatus:
                continue

            tpic = query(tpic_data, (lambda tpic: tpic.pic_nr == t_eg_maintain.pic and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tfrequency = query(tfrequency_data, (lambda tfrequency: tfrequency.freq_nr == t_eg_maintain.type), first=True)
            if not tfrequency:
                continue

            create_temp()

    elif main_date == 2:

        for t_eg_maintain in query(t_eg_maintain_data):
            tLocation = query(tlocation_data, (lambda tLocation: tLocation.loc_nr == t_eg_maintain.location and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_data, (lambda tproperty: tproperty.prop_nr == t_eg_maintain.propertynr and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == t_eg_maintain.type and tstatus.stat_selected), first=True)
            if not tstatus:
                continue

            tpic = query(tpic_data, (lambda tpic: tpic.pic_nr == t_eg_maintain.pic and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tfrequency = query(tfrequency_data, (lambda tfrequency: tfrequency.freq_nr == t_eg_maintain.type), first=True)
            if not tfrequency:
                continue

            create_temp()

    elif main_date == 3:

        for t_eg_maintain in query(t_eg_maintain_data):
            tLocation = query(tlocation_data, (lambda tLocation: tLocation.loc_nr == t_eg_maintain.location and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_data, (lambda tproperty: tproperty.prop_nr == t_eg_maintain.propertynr and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == t_eg_maintain.type and tstatus.stat_selected), first=True)
            if not tstatus:
                continue

            tpic = query(tpic_data, (lambda tpic: tpic.pic_nr == t_eg_maintain.pic and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tfrequency = query(tfrequency_data, (lambda tfrequency: tfrequency.freq_nr == t_eg_maintain.type), first=True)
            if not tfrequency:
                continue

            create_temp()

    return generate_output()