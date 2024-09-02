from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimkateg, Queasy, Outorder, Res_history, Zimmer, Zinrstat

def deactivate_ooo2_1bl(user_nr:int, oos_flag:bool, ci_date:date, ooo_list2:[Ooo_list2]):
    datum:date = None
    cat_flag:bool = False
    roomnr:int = 0
    zimkateg = queasy = outorder = res_history = zimmer = zinrstat = None

    om_list = ooo_list2 = zbuff = qsy = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int})
    ooo_list2_list, Ooo_list2 = create_model("Ooo_list2", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int, "selected_om":bool})

    Zbuff = Zimkateg
    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, cat_flag, roomnr, zimkateg, queasy, outorder, res_history, zimmer, zinrstat
        nonlocal zbuff, qsy


        nonlocal om_list, ooo_list2, zbuff, qsy
        nonlocal om_list_list, ooo_list2_list
        return {}


    ooo_list2 = query(ooo_list2_list, first=True)

    outorder = db_session.query(Outorder).filter(
            (Outorder.zinr == ooo_list2.zinr) &  (Outorder.betriebsnr == ooo_list2.betriebsnr) &  (Outorder.gespstart == ooo_list2.gespstart) &  (Outorder.gespende == ooo_list2.gespende)).first()

    if outorder.betriebsnr <= 1:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = user_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Remove O_O_O Record of Room " + outorder.zinr +\
                " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende)
        res_history.action = "HouseKeeping"

        res_history = db_session.query(Res_history).first()


        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == ooo_list2.zinr)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152)).first()

        if queasy:
            cat_flag = True

        zbuff = db_session.query(Zbuff).filter(
                (Zbuff.zikatnr == zimmer.zikatnr)).first()

        if zbuff:

            if cat_flag:
                roomnr = zbuff.typ
            else:
                roomnr = zbuff.zikatnr
        for datum in range(outorder.gespstart,outorder.gespende + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (Queasy.char1 == "")).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True

                    qsy = db_session.query(Qsy).first()


    if oos_flag and (outorder.gespstart == outorder.gespende):

        zinrstat = db_session.query(Zinrstat).filter(
                (func.lower(Zinrstat.zinr) == "oos") &  (Zinrstat.datum == ci_date)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = ci_date
            zinrstat.zinr = "oos"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    outorder = db_session.query(Outorder).first()
    db_session.delete(outorder)

    zimmer = db_session.query(Zimmer).filter(
            (Zimmer.zinr == ooo_list2.zinr)).first()

    if zimmer.zistatus == 6:
        zimmer.zistatus = 2
    zimmer.bediener_nr_stat = user_nr

    zimmer = db_session.query(Zimmer).first()

    return generate_output()