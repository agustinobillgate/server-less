#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 3/8/2025
# 
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Eg_property, Queasy, Eg_location

tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

def eg_repmaintain_all_locationbl(all_room:bool, tlocation_data:[Tlocation], tmaintask_data:[Tmaintask]):

    prepare_cache ([Eg_property, Queasy, Eg_location])

    troom_data = []
    tproperty_data = []
    zimmer = eg_property = queasy = eg_location = None

    tproperty = tmaintask = troom = tlocation = qbuff1 = comlocat = commain = comroom = None

    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_data, tproperty_data, zimmer, eg_property, queasy, eg_location
        nonlocal all_room


        nonlocal tproperty, tmaintask, troom, tlocation, qbuff1, comlocat, commain, comroom
        nonlocal tproperty_data, troom_data

        return {"troom": troom_data, "tproperty": tproperty_data}

    def create_room():

        nonlocal troom_data, tproperty_data, zimmer, eg_property, queasy, eg_location
        nonlocal all_room


        nonlocal tproperty, tmaintask, troom, tlocation, qbuff1, comlocat, commain, comroom
        nonlocal tproperty_data, troom_data

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_data = tlocation_data
        troom_data.clear()

        qbuff1 = query(qbuff1_data, filters=(lambda qbuff1_data: qbuff1_data.loc_selected  and qbuff1_data.loc_guest), first=True)
        if qbuff1:
            #-------------------------
            # for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
            for qbuff in db_session.query(Zimmer).order_by(Zimmer._recid).all():
                troom = Troom()
                troom.room_nm = qbuff.zinr
                troom.room_selected = False
                troom_data.append(troom)


    def create_property():

        nonlocal troom_data, tproperty_data, zimmer, eg_property, queasy, eg_location
        nonlocal all_room

        nonlocal tproperty, tmaintask, troom, tlocation, qbuff1, comlocat, commain, comroom
        nonlocal tproperty_data, troom_data

        qbuff = None
        ques = None
        Qbuff =  create_buffer("Qbuff",Eg_property)
        Comlocat = Tlocation
        comlocat_data = tlocation_data
        Commain = Tmaintask
        commain_data = tmaintask_data
        Comroom = Troom
        comroom_data = troom_data
        Ques =  create_buffer("Ques",Queasy)
        tproperty_data.clear()

        if all_room:

            for troom in query(troom_data):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_data.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_data, filters=(lambda comlocat: comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_data, (lambda comroom: comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = get_cache (Eg_location, {"nr": [(eq, qbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = get_cache (Eg_location, {"nr": [(eq, qbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


    create_room()
    create_property()

    return generate_output()