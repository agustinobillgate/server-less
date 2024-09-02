from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Queasy, Htparam, L_lager, Bediener, Eg_staff, Zimmer, Eg_location, Eg_property

def prepare_eg_reglist1bl(user_init:str):
    ci_date = None
    store_number = 0
    groupid = 0
    engid = 0
    p_992 = False
    q_133_list = []
    tpic_list = []
    dept_link_list = []
    queasy = htparam = l_lager = bediener = eg_staff = zimmer = eg_location = eg_property = None

    q_133 = tproperty = tmaintask = tcategory = tsource = troom = tlocation = tstatus = tpic = dept_link = qbuff = qbuff1 = comlocat = commain = comroom = ques = None

    q_133_list, Q_133 = create_model("Q_133", {"number1":int, "char1":str})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":str, "source_selected":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":str})

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
        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list
        return {"ci_date": ci_date, "store_number": store_number, "groupid": groupid, "engid": engid, "p_992": p_992, "q-133": q_133_list, "tpic": tpic_list, "dept-link": dept_link_list}

    def define_group():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def create_related_dept():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        i:int = 0
        c:int = 0
        Qbuff = Queasy
        dept_link_list.clear()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == engid)).first()

        if queasy:
            dept_link = Dept_link()
            dept_link_list.append(dept_link)

            dept_link.dept_nr = engid
            dept_link.dept_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = db_session.query(Qbuff).filter(
                        (Qbuff.key == 19) &  (Qbuff.number1 == to_int(entry(i - 1, queasy.char2, ";")))).first()

                if qbuff:
                    dept_link = Dept_link()
                    dept_link_list.append(dept_link)

                    dept_link.dept_nr = c
                    dept_link.dept_nm = qbuff.char3

    def create_pic():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        Qbuff = Eg_staff
        Qbuff1 = Bediener
        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usergroup == engid) &  (Qbuff.activeflag)).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False

    def create_status():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tStatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 1
        tStatus.stat_nm = "New"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 2
        tStatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 3
        tStatus.stat_nm = "Done"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 4
        tStatus.stat_nm = "Postponed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 5
        tStatus.stat_nm = "Closed"
        tstatus.stat_selected = False

    def create_room():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

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

    def create_source():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tsource = Tsource()
        tsource_list.append(tsource)

        tsource.source_nr = qbuff.number1
        tsource.source_nm = qbuff.char1
        tsource.source_selected = False

    def create_category():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tcategory = Tcategory()
        tcategory_list.append(tcategory)

        tcategory.categ_nr = qbuff.number1
        tcategory.categ_nm = qbuff.char1
        tcategory.categ_selected = False

    def create_maintask():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tmaintask = Tmaintask()
        tmaintask_list.append(tmaintask)

        tMaintask.Main_nr = qbuff.number1
        tMaintask.Main_nm = qbuff.char1
        tmaintask.main_selected = False


        q_133 = Q_133()
        q_133_list.append(q_133)

        q_133.number1 = qbuff.number1
        q_133.char1 = qbuff.char1

    def create_location():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        Qbuff = Eg_location
        tLocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for qbuff in db_session.query(Qbuff).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tLocation.loc_nr = qbuff.nr
                tLocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tLocation.loc_nr = qbuff.nr
                tLocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False

        for qbuff in db_session.query(Qbuff).all():
            qbuff.logi1 = False

    def create_main():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        do_it:bool = False

        eg_property = db_session.query(Eg_property).filter(
                (Eg_property.nr == 0) &  (Eg_property.bezeich == "")).first()

        if not eg_property:
            eg_property = Eg_property()
            db_session.add(eg_property)

            eg_property.nr = 0
            eg_property.bezeich = ""


        else:
            do_it = True

        eg_location = db_session.query(Eg_location).filter(
                (Eg_location.nr == 0) &  (Eg_location.bezeich == "")).first()

        if not eg_location:
            eg_location = Eg_location()
            db_session.add(eg_location)

            eg_location.nr = 0
            eg_location.bezeich = ""
            eg_location.logi1 = False


        else:
            do_it = True

        if do_it:

            return

    def create_property():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        Qbuff = Eg_property
        Comlocat = Tlocation
        Commain = Tmaintask
        Comroom = Troom
        Ques = Queasy
        tproperty_list.clear()
        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_list, filters=(lambda comlocat :comlocat.loc_selected)):
            qbuff = db_session.query(Qbuff).filter((Qbuff.location == comlocat.loc_nr)).first()
            if not qbuff:
                continue


            if comlocat.loc_guest :

                commain = query(commain_list, filters=(lambda commain :commain.main_nr == qbuff.maintask and commain.main_selected), first=True)

                if commain:

                    comroom = query(comroom_list, filters=(lambda comroom :comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)

                    if comroom:
                        tproperty = Tproperty()
                        tproperty_list.append(tproperty)

                        tproperty.prop_nr = qbuff.nr
                        tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                        tproperty.pzinr = qbuff.zinr
                        tproperty.pmain_nr = qbuff.maintask
                        tproperty.ploc_nr = qbuff.location

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 133) &  (Queasy.number1 == qbuff.maintask)).first()

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

                commain = query(commain_list, filters=(lambda commain :commain.main_nr == qbuff.maintask and commain.main_selected), first=True)

                if commain:
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

    def create_queasy():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, qbuff1, comlocat, commain, comroom, ques
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tsource_list.clear()
        tcategory_list.clear()
        tMaintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 130) |  (Qbuff.key == 132) |  (Qbuff.key == 133)).all():

            if qbuff.key == 130:
                create_source()

            if qbuff.key == 132:
                create_category()

            if qbuff.key == 133:
                create_maintask()

    p_992 = get_output(htplogic(992))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1061)).first()

    if htparam.finteger != 0:

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == htparam.finteger)).first()

        if l_lager:
            store_number = l_lager.lager_nr
    define_group()
    define_engineering()
    create_related_dept()
    create_pic()
    create_status()
    create_room()
    create_queasy()
    create_location()
    create_main()
    create_property()

    return generate_output()