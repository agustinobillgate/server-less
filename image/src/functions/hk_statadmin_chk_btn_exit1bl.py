from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Zimmer, Outorder, Queasy, Zimkateg

def hk_statadmin_chk_btn_exit1bl(bline_list:[Bline_list], om_list:[Om_list], pvilanguage:int, resflag:bool, dept:int, zinr:str, user_nr:int, from_date:date, to_date:date, ci_date:date, reason:str):
    msg_str = ""
    z_list_list = []
    return_flag:bool = False
    lvcarea:str = "hk_statadmin"
    res_line = zimmer = outorder = queasy = zimkateg = None

    z_list = om_list = bline_list = resline = qsy = None

    z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})
    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
    bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})

    Resline = Res_line
    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, z_list_list, return_flag, lvcarea, res_line, zimmer, outorder, queasy, zimkateg
        nonlocal resline, qsy


        nonlocal z_list, om_list, bline_list, resline, qsy
        nonlocal z_list_list, om_list_list, bline_list_list
        return {"msg_str": msg_str, "z-list": z_list_list}

    def update_queasy(zikatnr:int):

        nonlocal msg_str, z_list_list, return_flag, lvcarea, res_line, zimmer, outorder, queasy, zimkateg
        nonlocal resline, qsy


        nonlocal z_list, om_list, bline_list, resline, qsy
        nonlocal z_list_list, om_list_list, bline_list_list

        cat_flag:bool = False
        z_nr:int = 0
        Qsy = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152)).first()

        if queasy:
            cat_flag = True

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zikatnr)).first()

        if zimkateg:

            if cat_flag:
                z_nr = zimkateg.typ
            else:
                z_nr = zimkateg.zikatnr

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 171) &  (Queasy.date1 >= ci_date) &  (Queasy.number1 == z_nr)).first()
        while None != queasy and queasy.logi1 == False and queasy.logi2 == False :

            qsy = db_session.query(Qsy).filter(
                    (Qsy._recid == queasy._recid)).first()

            if qsy:
                qsy.logi2 = True

                qsy = db_session.query(Qsy).first()


            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 >= ci_date) &  (Queasy.number1 == z_nr)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == dept) &  (func.lower(Res_line.(zinr).lower()) == (zinr).lower())).first()

    for bline_list in query(bline_list_list, filters=(lambda bline_list :bline_list.selected)):

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == bline_list.zinr)).first()

        if not resflag:

            resline = db_session.query(Resline).filter(
                    (Resline.active_flag <= 1) &  (Resline.resnr != res_line.resnr) &  (Resline.resstatus != 12) &  (not Resline.abreise <= from_date) &  (not Resline.ankunft > to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower())).first()
        else:

            resline = db_session.query(Resline).filter(
                    (Resline.active_flag <= 1) &  (Resline.resstatus != 12) &  (not Resline.abreise <= from_date) &  (not Resline.ankunft > to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower())).first()

        if resline:
            msg_str = msg_str + translateExtended ("Reservation exists under ResNo", lvcarea, "") + "  ==  " + to_string(resline.resnr) + chr(10) + translateExtended ("Guest Name", lvcarea, "") + "  ==  " + resline.name + chr(10) + translateExtended ("Arrival :", lvcarea, "") + " " + to_string(resline.ankunft) + "   " + translateExtended ("Departure :", lvcarea, "") + " " + to_string(resline.abreise)
            return_flag = True

            return generate_output()

    for bline_list in query(bline_list_list, filters=(lambda bline_list :bline_list.selected)):

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == bline_list.zinr)).first()
        outorder = Outorder()
        db_session.add(outorder)

        outorder.zinr = bline_list.zinr
        outorder.gespstart = from_date
        outorder.gespende = to_date

        if resflag:
            outorder.betriebsnr = 2
        else:
            outorder.betriebsnr = dept
        outorder.gespgrund = reason + "$" + to_string(user_nr)

        outorder = db_session.query(Outorder).first()

        if outorder.gespstart == ci_date:

            om_list = query(om_list_list, filters=(lambda om_list :om_list.zinr == outorder.zinr), first=True)
            om_list.ind = 8
        update_queasy(zimmer.zikatnr)

        zimmer = db_session.query(Zimmer).first()
        zimmer.bediener_nr_stat = user_nr

        zimmer = db_session.query(Zimmer).first()
        bline_list.selected = False


    if return_flag:

        return generate_output()
    z_list_list.clear()

    for zimmer in db_session.query(Zimmer).all():
        z_list = Z_list()
        z_list_list.append(z_list)

        buffer_copy(zimmer, z_list)

        if zimmer.zistatus == 2:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resstatus == 8) &  (Res_line.zinr == zimmer.zinr) &  (Res_line.abreise == ci_date)).first()

            if res_line:
                z_list.checkout = True

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr <= 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()

        if outorder:
            z_list.str_reason = entry(0, outorder.gespgrund, "$")


        else:
            z_list.str_reason = " "

    return generate_output()