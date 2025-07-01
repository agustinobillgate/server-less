#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Waehrung, Zimkateg, Guest, Reservation, Res_line

def gcheck_inbl(input_resnr:int, ci_date:date):

    prepare_cache ([Waehrung, Zimkateg, Reservation, Res_line])

    gcheck_in_list = []
    waehrung = zimkateg = guest = reservation = res_line = None

    gcheck_in = None

    gcheck_in_list, Gcheck_in = create_model("Gcheck_in", {"resnr":int, "zinr":string, "name":string, "abreise":date, "anztage":int, "zimmeranz":int, "kurzbez":string, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":string, "zipreis":Decimal, "wabkurz":string, "l_zuordnung":int, "ankzeit":int, "gastnr":int, "reslinnr":int, "gastnrmember":int, "grpflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gcheck_in_list, waehrung, zimkateg, guest, reservation, res_line
        nonlocal input_resnr, ci_date


        nonlocal gcheck_in
        nonlocal gcheck_in_list

        return {"gcheck-in": gcheck_in_list}

    def disp_arlist():

        nonlocal gcheck_in_list, waehrung, zimkateg, guest, reservation, res_line
        nonlocal input_resnr, ci_date


        nonlocal gcheck_in
        nonlocal gcheck_in_list

        res_line_obj_list = {}
        for res_line, waehrung, zimkateg, guest, reservation in db_session.query(Res_line, Waehrung, Zimkateg, Guest, Reservation).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                 ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.resnr == input_resnr) & (Res_line.ankunft == ci_date)).order_by(Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            gcheck_in = Gcheck_in()
            gcheck_in_list.append(gcheck_in)

            gcheck_in.resnr = res_line.resnr
            gcheck_in.zinr = res_line.zinr
            gcheck_in.name = res_line.name
            gcheck_in.abreise = res_line.abreise
            gcheck_in.anztage = res_line.anztage
            gcheck_in.zimmeranz = res_line.zimmeranz
            gcheck_in.kurzbez = zimkateg.kurzbez
            gcheck_in.erwachs = res_line.erwachs
            gcheck_in.gratis = res_line.gratis
            gcheck_in.resstatus = res_line.resstatus
            gcheck_in.arrangement = res_line.arrangement
            gcheck_in.zipreis =  to_decimal(res_line.zipreis)
            gcheck_in.wabkurz = waehrung.wabkurz
            gcheck_in.l_zuordnung = res_line.l_zuordnung[2]
            gcheck_in.ankzeit = res_line.ankzeit
            gcheck_in.gastnr = res_line.gastnr
            gcheck_in.reslinnr = res_line.reslinnr
            gcheck_in.gastnrmember = res_line.gastnrmember
            gcheck_in.grpflag = reservation.grpflag

    disp_arlist()

    return generate_output()