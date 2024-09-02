from functions.additional_functions import *
import decimal
from models import Ratecode, Queasy, Zimkateg, Guest_pr, Arrangement

def prepare_bookengine_ratecodepushbl(bookengid:int):
    bookeng_name = ""
    t_push_list_list = []
    cat_flag:bool = False
    gastnrbe:int = 0
    tokcounter:int = 0
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    scode:str = ""
    ratecode = queasy = zimkateg = guest_pr = arrangement = None

    t_push_list = q_list = rmcat_list = dynarate_list = bratecode = None

    t_push_list_list, T_push_list = create_model("T_push_list", {"rcodevhp":str, "rcodebe":str, "rmtypevhp":str, "rmtypebe":str, "argtvhp":str, "flag":int})
    q_list_list, Q_list = create_model("Q_list", {"rcode":str, "rcodebe":str, "zikatnr":int, "rmtype":str, "rmtypebe":str, "arrangement":str})
    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "typ":int, "sleeping":bool, "bezeich":str}, {"sleeping": True})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"scode":str})

    Bratecode = Ratecode

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bookeng_name, t_push_list_list, cat_flag, gastnrbe, tokcounter, iftask, mestoken, mesvalue, scode, ratecode, queasy, zimkateg, guest_pr, arrangement
        nonlocal bratecode


        nonlocal t_push_list, q_list, rmcat_list, dynarate_list, bratecode
        nonlocal t_push_list_list, q_list_list, rmcat_list_list, dynarate_list_list
        return {"bookeng_name": bookeng_name, "t-push-list": t_push_list_list}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 159) &  (Queasy.number1 == bookengid)).first()

    if queasy:
        bookeng_name = queasy.char1
        gastnrbe = queasy.number2
    else:

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    for zimkateg in db_session.query(Zimkateg).filter(
            (Zimkateg.verfuegbarkeit) &  (not Zimkateg.bezeich.op("~")(".*NOT USED.*"))).all():

        if cat_flag and zimkateg.typ != 0:

            rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.typ == zimkateg.typ), first=True)
        else:

            rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.zikatnr == zimkateg.zikatnr), first=True)

        if not rmcat_list:
            rmcat_list = Rmcat_list()
            rmcat_list_list.append(rmcat_list)


            if cat_flag and zimkateg.typ != 0:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 152) &  (Queasy.number1 == zimkateg.typ)).first()

                if queasy:
                    rmcat_list.bezeich = queasy.char1
                rmcat_list.typ = zimkateg.typ
            else:
                rmcat_list.typ = zimkateg.zikatnr
                rmcat_list.bezeich = zimkateg.kurzbez

    for guest_pr in db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == gastnrbe)).all():

        for rmcat_list in query(rmcat_list_list):
            q_list = Q_list()
            q_list_list.append(q_list)

            q_list.rcode = guest_pr.CODE
            q_list.zikatnr = rmcat_list.typ
            q_list.rmtype = rmcat_list.bezeich

    for q_list in query(q_list_list):

        if cat_flag:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.typ == q_list.zikatnr)).first()
        else:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == q_list.zikatnr)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == q_list.rcode)).first()

        if queasy and queasy.logi2:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == q_list.rcode)).first()

            if ratecode:
                dynarate_list._list.clear()
                for tokcounter in range(1,num_entries(ratecode.char1[4], ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, ratecode.char1[4], ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, ratecode.char1[4], ";") , 2)

                    if mestoken == "RC":

                        if mesvalue != "":
                            dynarate_list = Dynarate_list()
                            dynarate_list_list.append(dynarate_list)

                            dynarate_list.scode = mesvalue

            for dynarate_list in query(dynarate_list_list):

                bratecode = db_session.query(Bratecode).filter(
                        (Bratecode.CODE == dynarate_list.scode) &  (Bratecode.zikatnr == zimkateg.zikatnr)).first()

                if bratecode:

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement.argtnr == bratecode.argtnr)).first()

                    if arrangement:
                        q_list.arrangement = arrangement
                    break

    elif queasy and not queasy.logi2:

        bratecode = db_session.query(Bratecode).filter(
                (Bratecode.CODE == q_list.rcode) &  (Bratecode.zikatnr == zimkateg.zikatnr)).first()

        if bratecode:

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == bratecode.argtnr)).first()

            if arrangement:
                q_list.arrangement = arrangement

    elif not queasy:
        q_list_list.remove(q_list)


    for q_list in query(q_list_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 161) &  (Queasy.number1 == bookengid) &  (entry(0, Queasy.char1, ";") == q_list.rcode) &  (entry(2, Queasy.char1, ";") == q_list.rmtype)).first()

        if queasy:
            q_list.rcodeBE = entry(1, queasy.char1, ";")
            q_list.rmtypeBE = entry(3, queasy.char1, ";")


        t_push_list = T_push_list()
        t_push_list_list.append(t_push_list)

        t_push_list.rcodeVHP = q_list.rcode
        t_push_list.rcodeBE = q_list.rcodeBE
        t_push_list.rmtypeVHP = q_list.rmtype
        t_push_list.rmtypeBE = q_list.rmtypeBE
        t_push_list.argtVHP = q_list.arrangement

    return generate_output()