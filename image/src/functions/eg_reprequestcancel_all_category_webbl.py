from functions.additional_functions import *
import decimal
from models import Queasy, Eg_property, Eg_location, Eg_subtask

def eg_reprequestcancel_all_category_webbl(all_room:bool, all_maintask:bool, tcategory:[Tcategory], tlocation:[Tlocation], troom:[Troom]):
    tmaintask_list = []
    tproperty_list = []
    tsubtask_list = []
    queasy = eg_property = eg_location = eg_subtask = None

    tsubtask = tproperty = troom = tlocation = tmaintask = tcategory = qbuff = comcategory = comlocat = commain = comroom = ques = None

    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":str, "sub_nm":str, "sub_selected":bool})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pmain_nr":int, "pmain":str, "pcateg_nr":int, "pcateg":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool, "categ_nr":int, "categ_nm":str})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})

    Qbuff = Eg_subtask
    Comcategory = Tcategory
    comcategory_list = tcategory_list

    Comlocat = Tlocation
    comlocat_list = tlocation_list

    Commain = Tmaintask
    commain_list = tmaintask_list

    Comroom = Troom
    comroom_list = troom_list

    Ques = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmaintask_list, tproperty_list, tsubtask_list, queasy, eg_property, eg_location, eg_subtask
        nonlocal qbuff, comcategory, comlocat, commain, comroom, ques


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, qbuff, comcategory, comlocat, commain, comroom, ques
        nonlocal tsubtask_list, tproperty_list, troom_list, tlocation_list, tmaintask_list, tcategory_list
        return {"tMaintask": tmaintask_list, "tproperty": tproperty_list, "tsubtask": tsubtask_list}

    def create_maintask():

        nonlocal tmaintask_list, tproperty_list, tsubtask_list, queasy, eg_property, eg_location, eg_subtask
        nonlocal qbuff, comcategory, comlocat, commain, comroom, ques


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, qbuff, comcategory, comlocat, commain, comroom, ques
        nonlocal tsubtask_list, tproperty_list, troom_list, tlocation_list, tmaintask_list, tcategory_list


        Qbuff = Queasy
        Comcategory = Tcategory
        tMaintask_list.clear()

        for comcategory in query(comcategory_list, filters=(lambda comcategory :comCategory.categ_SELECTED)):

            for qbuff in db_session.query(Qbuff).filter(
                    (Qbuff.key == 133) &  (Qbuff.number2 == comcategory.categ_nr)).all():
                tmaintask = Tmaintask()
                tmaintask_list.append(tmaintask)

                tMaintask.Main_nr = qbuff.number1
                tMaintask.Main_nm = qbuff.char1
                tmaintask.main_selected = True


                tMaintask.categ_nr = comcategory.categ_nr
                tMaintask.categ_nm = comcategory.categ_nm

    def create_property():

        nonlocal tmaintask_list, tproperty_list, tsubtask_list, queasy, eg_property, eg_location, eg_subtask
        nonlocal qbuff, comcategory, comlocat, commain, comroom, ques


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, qbuff, comcategory, comlocat, commain, comroom, ques
        nonlocal tsubtask_list, tproperty_list, troom_list, tlocation_list, tmaintask_list, tcategory_list


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
                    tproperty.prop_nm = qbuff.bezeich + "(" + to_string(qbuff.nr) + ")"
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
                    tproperty.prop_nm = qbuff.bezeich + "(" + to_string(qbuff.nr) + ")"
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

    def create_subtask():

        nonlocal tmaintask_list, tproperty_list, tsubtask_list, queasy, eg_property, eg_location, eg_subtask
        nonlocal qbuff, comcategory, comlocat, commain, comroom, ques


        nonlocal tsubtask, tproperty, troom, tlocation, tmaintask, tcategory, qbuff, comcategory, comlocat, commain, comroom, ques
        nonlocal tsubtask_list, tproperty_list, troom_list, tlocation_list, tmaintask_list, tcategory_list


        Qbuff = Eg_subtask
        tsubtask_list.clear()
        tsubtask = Tsubtask()
        tsubtask_list.append(tsubtask)

        tsubtask.sub_nr = "0"
        tsubtask.sub_nm = ""
        tsubtask.sub_selected = False

        if all_maintask:

            for qbuff in db_session.query(Qbuff).all():
                tsubtask = Tsubtask()
                tsubtask_list.append(tsubtask)

                tsubtask.sub_nr = qbuff.sub_code
                tsubtask.sub_nm = qbuff.bezeich
                tsubtask.sub_selected = False


        else:

            for tmaintask in query(tmaintask_list, filters=(lambda tmaintask :tmaintask.main_selected)):

                for qbuff in db_session.query(Qbuff).filter(
                        (Qbuff.main_nr == tmaintask.main_nr)).all():
                    tsubtask = Tsubtask()
                    tsubtask_list.append(tsubtask)

                    tsubtask.sub_nr = qbuff.sub_code
                    tsubtask.sub_nm = qbuff.bezeich
                    tsubtask.sub_selected = False

    create_maintask()
    create_property()
    create_subtask()

    return generate_output()