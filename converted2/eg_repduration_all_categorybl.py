#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_property, Eg_location, Eg_subtask

tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})

def eg_repduration_all_categorybl(all_maintask:bool, all_room:bool, tcategory_data:[Tcategory], tlocation_data:[Tlocation], troom_data:[Troom]):

    prepare_cache ([Queasy, Eg_location, Eg_subtask])

    tmaintask_data = []
    tproperty_data = []
    tsubtask_data = []
    queasy = eg_property = eg_location = eg_subtask = None

    tsubtask = tproperty = troom = tlocation = tmaintask = tcategory = comcategory = comlocat = commain = comroom = None

    tsubtask_data, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmaintask_data, tproperty_data, tsubtask_data, queasy, eg_property, eg_location, eg_subtask
        nonlocal all_maintask, all_room


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, comcategory, comlocat, commain, comroom
        nonlocal tsubtask_data, tproperty_data, tmaintask_data

        return {"tMaintask": tmaintask_data, "tproperty": tproperty_data, "tsubtask": tsubtask_data}

    def create_maintask():

        nonlocal tmaintask_data, tproperty_data, tsubtask_data, queasy, eg_property, eg_location, eg_subtask
        nonlocal all_maintask, all_room


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, comcategory, comlocat, commain, comroom
        nonlocal tsubtask_data, tproperty_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        Comcategory = Tcategory
        comcategory_data = tcategory_data
        tmaintask_data.clear()

        for comcategory in query(comcategory_data, filters=(lambda comcategory: comcategory.categ_selected)):

            for qbuff in db_session.query(Qbuff).filter(
                     (Qbuff.key == 133) & (Qbuff.number2 == comcategory.categ_nr)).order_by(Qbuff._recid).all():
                tmaintask = Tmaintask()
                tmaintask_data.append(tmaintask)

                tmaintask.main_nr = qbuff.number1
                tmaintask.main_nm = qbuff.char1
                tmaintask.main_selected = True


    def create_property():

        nonlocal tmaintask_data, tproperty_data, tsubtask_data, queasy, eg_property, eg_location, eg_subtask
        nonlocal all_maintask, all_room


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, comcategory, comlocat, commain, comroom
        nonlocal tsubtask_data, tproperty_data, tmaintask_data

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


    def create_subtask():

        nonlocal tmaintask_data, tproperty_data, tsubtask_data, queasy, eg_property, eg_location, eg_subtask
        nonlocal all_maintask, all_room


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, comcategory, comlocat, commain, comroom
        nonlocal tsubtask_data, tproperty_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_subtask)
        tsubtask_data.clear()
        tsubtask = Tsubtask()
        tsubtask_data.append(tsubtask)

        tsubtask.sub_nr = "0"
        tsubtask.sub_nm = ""
        tsubtask.sub_selected = False

        if all_maintask:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                tsubtask = Tsubtask()
                tsubtask_data.append(tsubtask)

                tsubtask.sub_nr = qbuff.sub_code
                tsubtask.sub_nm = qbuff.bezeich
                tsubtask.sub_selected = False


        else:

            for tmaintask in query(tmaintask_data, filters=(lambda tmaintask: tmaintask.main_selected)):

                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.main_nr == tmaintask.main_nr)).order_by(Qbuff._recid).all():
                    tsubtask = Tsubtask()
                    tsubtask_data.append(tsubtask)

                    tsubtask.sub_nr = qbuff.sub_code
                    tsubtask.sub_nm = qbuff.bezeich
                    tsubtask.sub_selected = False


    create_maintask()
    create_property()
    create_subtask()

    return generate_output()