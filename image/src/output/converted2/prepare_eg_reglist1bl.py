#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from models import Queasy, Htparam, L_lager, Bediener, Eg_staff, Zimmer, Eg_location, Eg_property

def prepare_eg_reglist1bl(user_init:string):

    prepare_cache ([Queasy, Htparam, L_lager, Bediener, Eg_staff, Zimmer, Eg_location, Eg_property])

    ci_date = None
    store_number = 0
    groupid = 0
    engid = 0
    p_992 = False
    q_133_list = []
    tpic_list = []
    dept_link_list = []
    queasy = htparam = l_lager = bediener = eg_staff = zimmer = eg_location = eg_property = None

    q_133 = tproperty = tmaintask = tcategory = tsource = troom = tlocation = tstatus = tpic = dept_link = qbuff = comlocat = commain = comroom = None

    q_133_list, Q_133 = create_model("Q_133", {"number1":int, "char1":string})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})

    Qbuff = create_buffer("Qbuff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        return {"ci_date": ci_date, "store_number": store_number, "groupid": groupid, "engid": engid, "p_992": p_992, "q-133": q_133_list, "tpic": tpic_list, "dept-link": dept_link_list}

    def define_group():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_related_dept():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        i:int = 0
        c:int = 0
        dept_link_list.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, engid)]})

        if queasy:
            dept_link = Dept_link()
            dept_link_list.append(dept_link)

            dept_link.dept_nr = engid
            dept_link.dept_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, to_int(entry(i - 1, queasy.char2, ";")))]})

                if qbuff:
                    dept_link = Dept_link()
                    dept_link_list.append(dept_link)

                    dept_link.dept_nr = c
                    dept_link.dept_nm = qbuff.char3


    def create_pic():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for eg_staff in db_session.query(Eg_staff).filter(
                 (Eg_staff.usergroup == engid) & (Eg_staff.activeflag)).order_by(Eg_staff.nr).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = eg_staff.nr
            tpic.pic_nm = eg_staff.name
            tpic.pic_dept = eg_staff.usergroup
            tpic.pic_selected = False


    def create_status():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tstatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "New"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 2
        tstatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 3
        tstatus.stat_nm = "Done"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 4
        tstatus.stat_nm = "Postponed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 5
        tstatus.stat_nm = "Closed"
        tstatus.stat_selected = False


    def create_room():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        i:int = 0
        troom_list.clear()

        tlocation = query(tlocation_list, filters=(lambda tlocation: tlocation.loc_selected  and tlocation.loc_guest), first=True)

        if tlocation:

            for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = zimmer.zinr
                troom.room_selected = False


    def create_source():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tsource = Tsource()
        tsource_list.append(tsource)

        tsource.source_nr = qbuff.number1
        tsource.source_nm = qbuff.char1
        tsource.source_selected = False


    def create_category():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tcategory = Tcategory()
        tcategory_list.append(tcategory)

        tcategory.categ_nr = qbuff.number1
        tcategory.categ_nm = qbuff.char1
        tcategory.categ_selected = False


    def create_maintask():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tmaintask = Tmaintask()
        tmaintask_list.append(tmaintask)

        tmaintask.main_nr = qbuff.number1
        tmaintask.main_nm = qbuff.char1
        tmaintask.main_selected = False


        q_133 = Q_133()
        q_133_list.append(q_133)

        q_133.number1 = qbuff.number1
        q_133.char1 = qbuff.char1


    def create_location():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tlocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():

            if eg_location.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = eg_location.nr
                tlocation.loc_nm = eg_location.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = eg_location.nr
                tlocation.loc_nm = eg_location.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_main():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        do_it:bool = False

        eg_property = get_cache (Eg_property, {"nr": [(eq, 0)],"bezeich": [(eq, "")]})

        if not eg_property:
            eg_property = Eg_property()
            db_session.add(eg_property)

            eg_property.nr = 0
            eg_property.bezeich = ""


        else:
            do_it = True

        eg_location = get_cache (Eg_location, {"nr": [(eq, 0)],"bezeich": [(eq, "")]})

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
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list

        ques = None
        Comlocat = Tlocation
        comlocat_list = tlocation_list
        Commain = Tmaintask
        commain_list = tmaintask_list
        Comroom = Troom
        comroom_list = troom_list
        Ques =  create_buffer("Ques",Queasy)
        tproperty_list.clear()
        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        eg_property_obj_list = {}
        for eg_property in db_session.query(Eg_property).filter(
                 ((Eg_property.location.in_(list(set([comlocat.loc_nr for comlocat in comlocat_list if comlocat.loc_selected])))))).order_by(Eg_property.location).all():
            if eg_property_obj_list.get(eg_property._recid):
                continue
            else:
                eg_property_obj_list[eg_property._recid] = True

            comlocat = query(comlocat_list, (lambda comlocat: (eg_property.location == comlocat.loc_nr)), first=True)

            if comlocat.loc_guest :

                commain = query(commain_list, filters=(lambda commain: commain.main_nr == eg_property.maintask and commain.main_selected), first=True)

                if commain:

                    comroom = query(comroom_list, filters=(lambda comroom: comroom.room_nm == eg_property.zinr and comroom.room_selected), first=True)

                    if comroom:
                        tproperty = Tproperty()
                        tproperty_list.append(tproperty)

                        tproperty.prop_nr = eg_property.nr
                        tproperty.prop_nm = eg_property.bezeich + "(" + trim (to_string(eg_property.nr , ">>>>>>9")) + ")"
                        tproperty.pzinr = eg_property.zinr
                        tproperty.pmain_nr = eg_property.maintask
                        tproperty.ploc_nr = eg_property.location

                        queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, eg_property.maintask)]})

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

                        eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

                        if eg_location:
                            tproperty.ploc = eg_location.bezeich


                        else:
                            tproperty.ploc = ""


            else:

                commain = query(commain_list, filters=(lambda commain: commain.main_nr == eg_property.maintask and commain.main_selected), first=True)

                if commain:
                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = eg_property.nr
                    tproperty.prop_nm = eg_property.bezeich + "(" + trim (to_string(eg_property.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = eg_property.zinr
                    tproperty.pmain_nr = eg_property.maintask
                    tproperty.ploc_nr = eg_property.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == eg_property.maintask)).first()

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

                    eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


    def create_queasy():

        nonlocal ci_date, store_number, groupid, engid, p_992, q_133_list, tpic_list, dept_link_list, queasy, htparam, l_lager, bediener, eg_staff, zimmer, eg_location, eg_property
        nonlocal user_init
        nonlocal qbuff


        nonlocal q_133, tproperty, tmaintask, tcategory, tsource, troom, tlocation, tstatus, tpic, dept_link, qbuff, comlocat, commain, comroom
        nonlocal q_133_list, tproperty_list, tmaintask_list, tcategory_list, tsource_list, troom_list, tlocation_list, tstatus_list, tpic_list, dept_link_list


        tsource_list.clear()
        tcategory_list.clear()
        tmaintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 130) | (Qbuff.key == 132) | (Qbuff.key == 133)).order_by(Qbuff._recid).all():

            if qbuff.key == 130:
                create_source()

            if qbuff.key == 132:
                create_category()

            if qbuff.key == 133:
                create_maintask()


    p_992 = get_output(htplogic(992))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1061)]})

    if htparam and htparam.finteger != 0:

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, htparam.finteger)]})

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