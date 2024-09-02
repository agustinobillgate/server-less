from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Res_line, Outorder, Zinrstat, Zimmer

def arl_list_mi_releasermbl(rec_id:int, user_init:str):
    fl_error = 0
    user_nr:int = 0
    oos_flag:bool = False
    bediener = res_line = outorder = zinrstat = zimmer = None

    ubuff = None

    Ubuff = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_error, user_nr, oos_flag, bediener, res_line, outorder, zinrstat, zimmer
        nonlocal ubuff


        nonlocal ubuff
        return {"fl_error": fl_error}


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == rec_id)).first()

    outorder = db_session.query(Outorder).filter(
            (Outorder.zinr == res_line.zinr) &  (Outorder.gespstart >= res_line.ankunft) &  (Outorder.gespende <= res_line.ankunft)).first()

    if not outorder:
        fl_error = 1

        return generate_output()
    oos_flag = (outorder.betriebsnr == 3 or outorder.betriebsnr == 4)

    if oos_flag and (outorder.gespstart == outorder.gespende):

        zinrstat = db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "oos") &  (Zinrstat.datum == outorder.gespende)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = outorder.gespende
            zinrstat.zinr = "oos"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    outorder = db_session.query(Outorder).first()
    db_session.delete(outorder)


    ubuff = db_session.query(Ubuff).filter(
                (func.lower(Ubuff.userinit) == (user_init).lower())).first()

    if ubuff:
        user_nr = ubuff.nr

    zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == res_line.zinr)).first()

    if zimmer.zistatus == 6:
        zimmer.zistatus = 2
        zimmer.bediener_nr_stat = user_nr

    zimmer = db_session.query(Zimmer).first()
    fl_error = 2


    return generate_output()