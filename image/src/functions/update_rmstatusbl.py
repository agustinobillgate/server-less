from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Zimmer, Res_line, Outorder, Zimkateg

def update_rmstatusbl(na_list:[Na_list], ci_date:date):
    i = 0
    htparam = zimmer = res_line = outorder = zimkateg = None

    na_list = None

    na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":str, "anz":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, htparam, zimmer, res_line, outorder, zimkateg


        nonlocal na_list
        nonlocal na_list_list
        return {"i": i}

    def update_rmstatus():

        nonlocal i, htparam, zimmer, res_line, outorder, zimkateg


        nonlocal na_list
        nonlocal na_list_list

        na_list = query(na_list_list, filters=(lambda na_list :na_list.reihenfolge == 3), first=True)

        zimmer = db_session.query(Zimmer).first()
        while None != zimmer:

            if zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 2:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

            elif zimmer.zistatus == 3:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line and res_line.abreise > ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

            elif zimmer.zistatus == 4 or zimmer.zistatus == 5:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line and res_line.abreise == ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 3
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

            if zimmer.zistatus == 6:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13))).first()

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

                    outorder = db_session.query(Outorder).filter(
                            (Outorder.zinr == zimmer.zinr) &  (Outorder.gespstart < res_line.abreise)).first()

                    if outorder:
                        db_session.delete(outorder)
                else:

                    outorder = db_session.query(Outorder).filter(
                            (Outorder.zinr == zimmer.zinr) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()

                    if not outorder:

                        zimmer = db_session.query(Zimmer).first()
                        zimmer.bediener_nr_stat = 0
                        zimmer.zistatus = 2

                        zimmer = db_session.query(Zimmer).first()

        zimmer = db_session.query(Zimmer).first()


    update_rmstatus()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 592)).first()
    htparam.flogical = False

    htparam = db_session.query(Htparam).first()

    for zimkateg in db_session.query(Zimkateg).all():
        i = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.zikatnr == zimkateg.zikatnr)).all():
            i = i + 1
        zimkateg.maxzimanz = i

    return generate_output()