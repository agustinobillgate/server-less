from functions.additional_functions import *
import decimal
from models import Zimmer, Eg_property, Queasy, Eg_location

def eg_maincalendar_all_locationbl(all_room:bool, tlocation:[Tlocation], tmaintask:[Tmaintask]):
    troom_list = []
    tproperty_list = []
    zimmer = eg_property = queasy = eg_location = None

    tproperty = tmaintask = troom = tlocation = qbuff = qbuff1 = comlocat = commain = comroom = ques = None

    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})

    Qbuff = Eg_property
    Qbuff1 = Tlocation
    qbuff1_list = tlocation_list

    Comlocat = Tlocation
    comlocat_list = tlocation_list

    Commain = Tmaintask
    commain_list = tmaintask_list

    Comroom = Troom
    comroom_list = troom_list

    Ques = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_list, tproperty_list, zimmer, eg_property, queasy, eg_location
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal tproperty, tmaintask, troom, tlocation, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal tproperty_list, tmaintask_list, troom_list, tlocation_list
        return {"troom": troom_list, "tproperty": tproperty_list}

    def create_room():

        nonlocal troom_list, tproperty_list, zimmer, eg_property, queasy, eg_location
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal tproperty, tmaintask, troom, tlocation, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal tproperty_list, tmaintask_list, troom_list, tlocation_list

        i:int = 0
        Qbuff = Zimmer
        Qbuff1 = Tlocation
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1 :qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_SELECTED = False


        else:
            pass

    def create_property():

        nonlocal troom_list, tproperty_list, zimmer, eg_property, queasy, eg_location
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal tproperty, tmaintask, troom, tlocation, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal tproperty_list, tmaintask_list, troom_list, tlocation_list


        Qbuff = Eg_property
        Comlocat = Tlocation
        Commain = Tmaintask
        Comroom = Troom
        Ques = Queasy
        tproperty_list.clear()

        if all_room:

            for troom in query(troom_list):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_list, filters=(lambda comlocat :comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = []
                for qbuff, commain, comroom in db_session.query(Qbuff, Commain, Comroom).join(Commain,(Commain.main_nr == Qbuff.maintask) &  (Commain.main_selected)).join(Comroom,(Comroom.room_nm == Qbuff.zinr) &  (Comroom.room_selected)).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    if qbuff._recid in qbuff_obj_list:
                        continue
                    else:
                        qbuff_obj_list.append(qbuff._recid)


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.nr == qbuff.location)).first()

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                qbuff_obj_list = []
                for qbuff, commain in db_session.query(Qbuff, Commain).join(Commain,(Commain.main_nr == Qbuff.maintask) &  (Commain.main_selected)).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    if qbuff._recid in qbuff_obj_list:
                        continue
                    else:
                        qbuff_obj_list.append(qbuff._recid)


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.nr == qbuff.location)).first()

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""

    create_room()
    create_property()

    return generate_output()