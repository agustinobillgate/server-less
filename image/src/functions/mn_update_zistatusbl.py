from functions.additional_functions import *
import decimal
from datetime import date
from functions.genoooroombl import genoooroombl
from sqlalchemy import func
from models import Zimmer, Htparam, Queasy, Res_line, Guest, Outorder, Zinrstat

def mn_update_zistatusbl(pvilanguage:int):
    i = 0
    msg_str = ""
    lvcarea:str = "mn_start"
    ci_date:date = None
    bill_date:date = None
    zimmer = htparam = queasy = res_line = guest = outorder = zinrstat = None

    t_zimmer = zbuff = qbuff = None

    T_zimmer = Zimmer
    Zbuff = Zimmer
    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, msg_str, lvcarea, ci_date, bill_date, zimmer, htparam, queasy, res_line, guest, outorder, zinrstat
        nonlocal t_zimmer, zbuff, qbuff


        nonlocal t_zimmer, zbuff, qbuff
        return {"i": i, "msg_str": msg_str}

    def update_zistatus():

        nonlocal i, msg_str, lvcarea, ci_date, bill_date, zimmer, htparam, queasy, res_line, guest, outorder, zinrstat
        nonlocal t_zimmer, zbuff, qbuff


        nonlocal t_zimmer, zbuff, qbuff

        i:int = 0
        Zbuff = Zimmer
        Qbuff = Queasy

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).all():
            i = i + 1

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if not zimmer:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnr)).first()
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("ALARM: RmNo incorrect -> Updating Room Status not possible :", lvcarea, "") + chr(10) + translateExtended ("ResNo :", lvcarea, "") + to_string(res_line.resnr) + " - " + guest.name
            else:

                zimmer = db_session.query(Zimmer).first()

                if res_line.abreise == ci_date:
                    zimmer.zistatus = 3

                elif res_line.abreise > ci_date:
                    zimmer.zistatus = 4
                zimmer.bediener_nr_stat = 0

                zimmer = db_session.query(Zimmer).first()
        i = 0

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zistatus == 6) &  (sleeping)).first()
        while None != zimmer:

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.gespende < ci_date)).first()

            if outorder:
                get_output(genoooroombl(outorder.zinr))
                i = i + 1

                zimmer = db_session.query(Zimmer).first()
                zimmer.zistatus = 2

                zinrstat = db_session.query(Zinrstat).filter(
                            (func.lower(Zinrstat.zinr) == "ooo") &  (Zinrstat.datum == outorder.gespende)).first()

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = outorder.gespende
                    zinrstat.zinr = "ooo"


                zinrstat.zimmeranz = zinrstat.zimmeranz + 1

                outorder = db_session.query(Outorder).first()
                db_session.delete(outorder)

                zimmer.bediener_nr_stat = 0

                zimmer = db_session.query(Zimmer).first()


            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zistatus == 6)).first()

        for zimmer in db_session.query(Zimmer).all():

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr > 1)).first()
            while None != outorder :

                if outorder.gespende < ci_date:
                    i = i + 1

                    outorder = db_session.query(Outorder).first()
                    db_session.delete(outorder)


                outorder = db_session.query(Outorder).filter(
                        (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr > 1)).first()

        for outorder in db_session.query(Outorder).filter(
                (Outorder.gespstart <= ci_date) &  (Outorder.betriebsnr <= 1)).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == outorder.zinr)).first()

            if zimmer and zimmer.zistatus <= 2:

                zimmer = db_session.query(Zimmer).first()
                zimmer.zistatus = 6

                zimmer = db_session.query(Zimmer).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 250)).first()

        if htparam.flogical:

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zistatus == 0)).first()
            while None != zimmer:

                zimmer = db_session.query(Zimmer).first()
                zimmer.zistatus = 1
                zimmer.bediener_nr_stat = 0

                zimmer = db_session.query(Zimmer).first()


                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zistatus == 0)).first()

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.features != "")).first()
        while None != zimmer:

            zbuff = db_session.query(Zbuff).filter(
                        (Zbuff._recid == zimmer._recid)).first()
            zbuff.features = ""
            zbuff.house_status = 0

            zbuff = db_session.query(Zbuff).first()


            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.features != "")).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 162)).first()
        while None != queasy:

            qbuff = db_session.query(Qbuff).filter(
                        (Qbuff._recid == queasy._recid)).first()
            db_session.delete(qbuff)


            queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 162)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    update_zistatus()

    return generate_output()