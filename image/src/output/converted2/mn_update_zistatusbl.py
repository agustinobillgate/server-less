#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.genoooroombl import genoooroombl
from models import Zimmer, Htparam, Queasy, Res_line, Guest, Outorder, Zinrstat

def mn_update_zistatusbl(pvilanguage:int):

    prepare_cache ([Zimmer, Htparam, Res_line, Guest, Zinrstat])

    i = 0
    msg_str = ""
    lvcarea:string = "mn-start"
    ci_date:date = None
    bill_date:date = None
    zimmer = htparam = queasy = res_line = guest = outorder = zinrstat = None

    t_zimmer = None

    T_zimmer = create_buffer("T_zimmer",Zimmer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, msg_str, lvcarea, ci_date, bill_date, zimmer, htparam, queasy, res_line, guest, outorder, zinrstat
        nonlocal pvilanguage
        nonlocal t_zimmer


        nonlocal t_zimmer

        return {"i": i, "msg_str": msg_str}

    def update_zistatus():

        nonlocal msg_str, lvcarea, ci_date, bill_date, zimmer, htparam, queasy, res_line, guest, outorder, zinrstat
        nonlocal pvilanguage
        nonlocal t_zimmer


        nonlocal t_zimmer

        i:int = 0
        zbuff = None
        qbuff = None
        Zbuff =  create_buffer("Zbuff",Zimmer)
        Qbuff =  create_buffer("Qbuff",Queasy)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus == 6)).order_by(Res_line._recid).all():
            i = i + 1

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if not zimmer:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("ALARM: RmNo incorrect -> Updating Room Status not possible :", lvcarea, "") + chr_unicode(10) + translateExtended ("ResNo :", lvcarea, "") + to_string(res_line.resnr) + " - " + guest.name
            else:
                pass

                if res_line.abreise == ci_date:
                    zimmer.zistatus = 3

                elif res_line.abreise > ci_date:
                    zimmer.zistatus = 4
                zimmer.bediener_nr_stat = 0
                pass
        i = 0

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zistatus == 6) & (Zimmer.sleeping)).first()
        while None != zimmer:

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespende": [(lt, ci_date)]})

            if outorder:
                get_output(genoooroombl(outorder.zinr))
                i = i + 1
                pass
                zimmer.zistatus = 2

                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "ooo")],"datum": [(eq, outorder.gespende)]})

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = outorder.gespende
                    zinrstat.zinr = "ooo"


                zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                pass
                db_session.delete(outorder)
                pass
                zimmer.bediener_nr_stat = 0
                pass

            curr_recid = zimmer._recid
            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zistatus == 6) & (Zimmer._recid > curr_recid)).first()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"betriebsnr": [(gt, 1)]})
            while None != outorder :

                if outorder.gespende < ci_date:
                    i = i + 1
                    pass
                    db_session.delete(outorder)
                    pass

                curr_recid = outorder._recid
                outorder = db_session.query(Outorder).filter(
                         (Outorder.zinr == zimmer.zinr) & (Outorder.betriebsnr > 1) & (Outorder._recid > curr_recid)).first()

        for outorder in db_session.query(Outorder).filter(
                 (Outorder.gespstart <= ci_date) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():

            zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

            if zimmer and zimmer.zistatus <= 2:
                pass
                zimmer.zistatus = 6
                pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 250)]})

        if htparam.flogical:

            zimmer = get_cache (Zimmer, {"zistatus": [(eq, 0)]})
            while None != zimmer:
                pass
                zimmer.zistatus = 1
                zimmer.bediener_nr_stat = 0
                pass

                curr_recid = zimmer._recid
                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zistatus == 0) & (Zimmer._recid > curr_recid)).first()

        zimmer = get_cache (Zimmer, {"features": [(ne, "")]})
        while None != zimmer:

            zbuff = get_cache (Zimmer, {"_recid": [(eq, zimmer._recid)]})
            zbuff.features = ""
            zbuff.house_status = 0


            pass

            curr_recid = zimmer._recid
            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.features != "") & (Zimmer._recid > curr_recid)).first()

        queasy = get_cache (Queasy, {"key": [(eq, 162)]})
        while None != queasy:

            qbuff = db_session.query(Qbuff).filter(
                         (Qbuff._recid == queasy._recid)).first()
            db_session.delete(qbuff)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 162) & (Queasy._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    update_zistatus()

    return generate_output()