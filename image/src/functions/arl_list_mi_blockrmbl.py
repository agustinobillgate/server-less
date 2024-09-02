from functions.additional_functions import *
import decimal
from models import Res_line, Outorder, Bediener, Zimmer

def arl_list_mi_blockrmbl(pvilanguage:int, rec_id:int, creason:str, bediener_nr:int):
    msg_str = ""
    lvcarea:str = "arl_list"
    user_nr:str = ""
    res_line = outorder = bediener = zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, user_nr, res_line, outorder, bediener, zimmer


        return {"msg_str": msg_str}


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == rec_id)).first()

    outorder = db_session.query(Outorder).filter(
            (Outorder.zinr == res_line.zinr) &  (Outorder.gespstart >= res_line.ankunft) &  (Outorder.gespende <= res_line.ankunft)).first()

    if outorder:
        msg_str = msg_str + chr(2) + translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

        return generate_output()

    bediener = db_session.query(Bediener).filter(
                (Bediener.nr == bediener_nr)).first()

    if bediener:
        user_nr = bediener.userinit


    else:
        user_nr = to_string(bediener_nr)


    outorder = Outorder()
    db_session.add(outorder)

    outorder.zinr = res_line.zinr
    outorder.gespstart = res_line.ankunft
    outorder.gespende = res_line.ankunft
    outorder.betriebsnr = res_line.resnr

    outorder = db_session.query(Outorder).first()

    zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == res_line.zinr)).first()

    if zimmer:
        zimmer.bediener_nr_stat = bediener_nr

        zimmer = db_session.query(Zimmer).first()

    return generate_output()