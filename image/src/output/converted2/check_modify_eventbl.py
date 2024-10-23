from functions.additional_functions import *
import decimal
from models import Bk_veran, Bk_reser, Bk_func

def check_modify_eventbl(rml_resnr:int, rml_reslinnr:int, rml_raum:str, rml_nr:int, curr_i:int):
    err = 0
    recid_rl = 0
    rl_veran_nr = 0
    mess_str = ""
    curr_room:str = ""
    curr_status:int = 0
    bk_veran = bk_reser = bk_func = None

    mainres = rl = bf = bk_resline = None

    Mainres = create_buffer("Mainres",Bk_veran)
    Rl = create_buffer("Rl",Bk_reser)
    Bf = create_buffer("Bf",Bk_func)
    Bk_resline = create_buffer("Bk_resline",Bk_reser)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, recid_rl, rl_veran_nr, mess_str, curr_room, curr_status, bk_veran, bk_reser, bk_func
        nonlocal rml_resnr, rml_reslinnr, rml_raum, rml_nr, curr_i
        nonlocal mainres, rl, bf, bk_resline


        nonlocal mainres, rl, bf, bk_resline
        return {"err": err, "recid_rl": recid_rl, "rl_veran_nr": rl_veran_nr, "mess_str": mess_str}

    curr_room = rml_raum
    curr_status = rml_nr

    rl = db_session.query(Rl).filter(
             (Rl.veran_nr == rml_resnr) & (Rl.veran_seite == rml_reslinnr)).first()

    if rl:
        recid_rl = rl._recid
        rl_veran_nr = rl.veran_nr

    if rl and rl.resstatus == 1:

        mainres = db_session.query(Mainres).filter(
                 (Mainres.veran_nr == rl.veran_nr)).first()

        if (mainres.deposit_payment[0] + mainres.deposit_payment[1] + mainres.deposit_payment[2] + mainres.deposit_payment[3] + mainres.deposit_payment[4] + mainres.deposit_payment[5] + mainres.deposit_payment[6] + mainres.deposit_payment[7] + mainres.deposit_payment[8]) != 0:

            bk_resline = db_session.query(Bk_resline).filter(
                     (Bk_resline.veran_nr == mainres.veran_nr) & (Bk_resline.veran_resnr != rml_reslinnr) & (Bk_resline.resstatus == 1)).first()

            if not bk_resline:
                err = 1
                mess_str = "Deposit exists, status change not possible!"

                return generate_output()