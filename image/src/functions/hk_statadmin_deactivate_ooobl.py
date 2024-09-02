from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimkateg, Queasy, Zimmer, Outorder, Zinrstat, Res_history, Res_line

bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})
om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})

def hk_statadmin_deactivate_ooobl(bline_list_list:[Bline_list], om_list_list:[Om_list], ci_date:date, user_nr:int, chgsort:int):
    z_list_list = []
    datum:date = None
    cat_flag:bool = False
    roomnr:int = 0
    zimkateg = queasy = zimmer = outorder = zinrstat = res_history = res_line = None

    z_list = om_list = bline_list = zbuff = qsy = None

    z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})

    Zbuff = create_buffer("Zbuff",Zimkateg)
    Qsy = create_buffer("Qsy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal z_list_list, datum, cat_flag, roomnr, zimkateg, queasy, zimmer, outorder, zinrstat, res_history, res_line
        nonlocal ci_date, user_nr, chgsort
        nonlocal zbuff, qsy


        nonlocal z_list, om_list, bline_list, zbuff, qsy
        nonlocal z_list_list, om_list_list, bline_list_list
        return {"bline-list": bline_list_list, "om-list": om_list_list, "z-list": z_list_list}

    def deactivate_ooo():

        nonlocal z_list_list, datum, cat_flag, roomnr, zimkateg, queasy, zimmer, outorder, zinrstat, res_history, res_line
        nonlocal ci_date, user_nr, chgsort
        nonlocal zbuff, qsy


        nonlocal z_list, om_list, bline_list, zbuff, qsy
        nonlocal z_list_list, om_list_list, bline_list_list

        answer:bool = False
        result:bool = False
        oos_flag:bool = False
        ooo_flag:bool = False

        for bline_list in query(bline_list_list, filters=(lambda bline_list: bline_list.selected)):

            if not zimmer or not(zimmer.zinr == bline_list.zinr):
                zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == bline_list.zinr)).first()

            for outorder in db_session.query(Outorder).filter(
                    (Outorder.zinr == bline_list.zinr)).order_by(Outorder._recid).all():
                oos_flag = (outorder.betriebsnr == 3 or outorder.betriebsnr == 4)
                ooo_flag = (outorder.betriebsnr <= 1 and ci_date >= outorder.gespstart and ci_date <= outorder.gespende)

                if oos_flag and (outorder.gespstart == outorder.gespende):

                    if not zinrstat or not(zinrstat.zinr.lower()  == ("oos").lower()  and zinrstat.datum == ci_date):
                        zinrstat = db_session.query(Zinrstat).filter(
                            (func.lower(Zinrstat.zinr) == ("oos").lower()) &  (Zinrstat.datum == ci_date)).first()

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = ci_date
                        zinrstat.zinr = "oos"


                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                    db_session.delete(outorder)
                    pass

                elif ooo_flag:

                    if not queasy or not(queasy.key == 152):
                        queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 152)).first()

                    if queasy:
                        cat_flag = True

                    if not zbuff or not(zbuff.zikatnr == zimmer.zikatnr):
                        zbuff = db_session.query(Zbuff).filter(
                            (Zbuff.zikatnr == zimmer.zikatnr)).first()

                    if zbuff:

                        if cat_flag:
                            roomnr = zbuff.typ
                        else:
                            roomnr = zbuff.zikatnr
                    for datum in date_range(outorder.gespstart,outorder.gespende) :

                        if not queasy or not(queasy.key == 171 and queasy.date1 == datum and queasy.number1 == roomnr and queasy.char1 == ""):
                            queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (Queasy.char1 == "")).first()

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:

                            if not qsy or not(qsy._recid == queasy._recid):
                                qsy = db_session.query(Qsy).filter(
                                    (Qsy._recid == queasy._recid)).first()

                            if qsy:
                                qsy.logi2 = True
                                pass
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = user_nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Remove O-O-O Record of Room " + outorder.zinr +\
                            " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende)
                    res_history.action = "HouseKeeping"


                    pass
                    db_session.delete(outorder)
                    pass
            zimmer.bediener_nr_stat = user_nr

            if zimmer.zistatus >= 6:
                zimmer.zistatus = chgsort - 1

                if not om_list or not(om_list.zinr == zimmer.zinr):
                    om_list = query(om_list_list, filters=(lambda om_list: om_list.zinr == zimmer.zinr), first=True)
                om_list.ind = zimmer.zistatus + 1
            bline_list.selected = False
        z_list_list.clear()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            z_list = Z_list()
            z_list_list.append(z_list)

            buffer_copy(zimmer, z_list)

            if zimmer.zistatus == 2:

                if not res_line or not(res_line.resstatus == 8 and res_line.zinr == zimmer.zinr and res_line.abreise == ci_date):
                    res_line = db_session.query(Res_line).filter(
                        (Res_line.resstatus == 8) &  (Res_line.zinr == zimmer.zinr) &  (Res_line.abreise == ci_date)).first()

                if res_line:
                    z_list.checkout = True

            if not outorder or not(outorder.zinr == zimmer.zinr and outorder.betriebsnr <= 2 and outorder.gespstart <= ci_date and outorder.gespende >= ci_date):
                outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr <= 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()

            if outorder:
                z_list.str_reason = entry(0, outorder.gespgrund, "$")


            else:
                z_list.str_reason = " "

    deactivate_ooo()

    return generate_output()