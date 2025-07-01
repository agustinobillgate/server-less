#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Ratecode, Queasy, Zimkateg, Guest_pr, Arrangement

def prepare_bookengine_ratecodepushbl(bookengid:int):

    prepare_cache ([Ratecode, Queasy, Zimkateg, Guest_pr, Arrangement])

    bookeng_name = ""
    t_push_list_list = []
    cat_flag:bool = False
    gastnrbe:int = 0
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    scode:string = ""
    ratecode = queasy = zimkateg = guest_pr = arrangement = None

    t_push_list = q_list = rmcat_list = dynarate_list = bratecode = None

    t_push_list_list, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    q_list_list, Q_list = create_model("Q_list", {"rcode":string, "rcodebe":string, "zikatnr":int, "rmtype":string, "rmtypebe":string, "arrangement":string})
    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "typ":int, "sleeping":bool, "bezeich":string}, {"sleeping": True})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"scode":string})

    Bratecode = create_buffer("Bratecode",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bookeng_name, t_push_list_list, cat_flag, gastnrbe, tokcounter, iftask, mestoken, mesvalue, scode, ratecode, queasy, zimkateg, guest_pr, arrangement
        nonlocal bookengid
        nonlocal bratecode


        nonlocal t_push_list, q_list, rmcat_list, dynarate_list, bratecode
        nonlocal t_push_list_list, q_list_list, rmcat_list_list, dynarate_list_list

        return {"bookeng_name": bookeng_name, "t-push-list": t_push_list_list}


    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if queasy:
        bookeng_name = queasy.char1
        gastnrbe = queasy.number2
    else:

        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    for zimkateg in db_session.query(Zimkateg).filter(
             (Zimkateg.verfuegbarkeit) & (not_(matches(Zimkateg.bezeichnung,"*NOT USED*")))).order_by(Zimkateg._recid).all():

        if cat_flag and zimkateg.typ != 0:

            rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list: rmcat_list.typ == zimkateg.typ), first=True)
        else:

            rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list: rmcat_list.zikatnr == zimkateg.zikatnr), first=True)

        if not rmcat_list:
            rmcat_list = Rmcat_list()
            rmcat_list_list.append(rmcat_list)


            if cat_flag and zimkateg.typ != 0:

                queasy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, zimkateg.typ)]})

                if queasy:
                    rmcat_list.bezeich = queasy.char1
                rmcat_list.typ = zimkateg.typ
            else:
                rmcat_list.typ = zimkateg.zikatnr
                rmcat_list.bezeich = zimkateg.kurzbez

    for guest_pr in db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == gastnrbe)).order_by(Guest_pr._recid).all():

        for rmcat_list in query(rmcat_list_list):
            q_list = Q_list()
            q_list_list.append(q_list)

            q_list.rcode = guest_pr.code
            q_list.zikatnr = rmcat_list.typ
            q_list.rmtype = rmcat_list.bezeich

    for q_list in query(q_list_list):

        if cat_flag:

            zimkateg = get_cache (Zimkateg, {"typ": [(eq, q_list.zikatnr)]})
        else:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, q_list.zikatnr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, q_list.rcode)]})

        if queasy and queasy.logi2:

            ratecode = get_cache (Ratecode, {"code": [(eq, q_list.rcode)]})

            if ratecode:
                dynarate_list_list.clear()
                for tokcounter in range(1,num_entries(ratecode.char1[4], ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, ratecode.char1[4], ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, ratecode.char1[4], ";") , 2)

                    if mestoken == "RC":

                        if mesvalue != "":
                            dynarate_list = Dynarate_list()
                            dynarate_list_list.append(dynarate_list)

                            dynarate_list.scode = mesvalue

                for dynarate_list in query(dynarate_list_list):

                    bratecode = get_cache (Ratecode, {"code": [(eq, dynarate_list.scode)],"zikatnr": [(eq, zimkateg.zikatnr)]})

                    if bratecode:

                        arrangement = get_cache (Arrangement, {"argtnr": [(eq, bratecode.argtnr)]})

                        if arrangement:
                            q_list.arrangement = arrangement.arrangement
                        break

        elif queasy and not queasy.logi2:

            bratecode = get_cache (Ratecode, {"code": [(eq, q_list.rcode)],"zikatnr": [(eq, zimkateg.zikatnr)]})

            if bratecode:

                arrangement = get_cache (Arrangement, {"argtnr": [(eq, bratecode.argtnr)]})

                if arrangement:
                    q_list.arrangement = arrangement.arrangement

        elif not queasy:
            q_list_list.remove(q_list)
            pass

    for q_list in query(q_list_list):

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 161) & (Queasy.number1 == bookengid) & (entry(0, Queasy.char1, ";") == q_list.rcode) & (entry(2, Queasy.char1, ";") == q_list.rmtype)).first()

        if queasy:
            q_list.rcodebe = entry(1, queasy.char1, ";")
            q_list.rmytpebe = entry(3, queasy.char1, ";")


        t_push_list = T_push_list()
        t_push_list_list.append(t_push_list)

        t_push_list.rcodevhp = q_list.rcode
        t_push_list.rcodebe = q_list.rcodebe
        t_push_list.rmtypevhp = q_list.rmtype
        t_push_list.rmytpebe = q_list.rmytpebe
        t_push_list.argtvhp = q_list.arrangement

    return generate_output()