from functions.additional_functions import *
import decimal
from models import Arrangement, Waehrung, Htparam

def prepare_argt_adminbl(pvilanguage:int):
    double_currency = False
    msg_str = ""
    w_list_list = []
    t_arrangement_list = []
    foreign_rate:bool = False
    local_nr:int = 0
    foreign_nr:int = 0
    lvcarea:str = "prepare_argt_admin"
    arrangement = waehrung = htparam = None

    t_arrangement = w_list = waehrung1 = argt = None

    t_arrangement_list, T_arrangement = create_model_like(Arrangement, {"waehrungsnr":str})
    w_list_list, W_list = create_model("W_list", {"bez":str, "first_bez":str})

    Waehrung1 = Waehrung
    Argt = Arrangement

    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, msg_str, w_list_list, t_arrangement_list, foreign_rate, local_nr, foreign_nr, lvcarea, arrangement, waehrung, htparam
        nonlocal waehrung1, argt


        nonlocal t_arrangement, w_list, waehrung1, argt
        nonlocal t_arrangement_list, w_list_list
        return {"double_currency": double_currency, "msg_str": msg_str, "w-list": w_list_list, "t-arrangement": t_arrangement_list}

    def update_argt():

        nonlocal double_currency, msg_str, w_list_list, t_arrangement_list, foreign_rate, local_nr, foreign_nr, lvcarea, arrangement, waehrung, htparam
        nonlocal waehrung1, argt


        nonlocal t_arrangement, w_list, waehrung1, argt
        nonlocal t_arrangement_list, w_list_list


        Argt = Arrangement

        if foreign_rate:

            for waehrung1 in db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr != foreign_nr) &  (Waehrung1.betriebsnr == 0)).all():
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.bez = waehrung1.bezeich

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == foreign_nr)).first()

            if waehrung1:
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.first_bez = waehrung1.bezeich


        else:

            for waehrung1 in db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr != local_nr) &  (Waehrung1.betriebsnr == 0)).all():
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.bez = waehrung1.bezeich

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == local_nr)).first()

            if waehrung1:
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.first_bez = waehrung1.bezeich

        argt = db_session.query(Argt).filter(
                (Argt.betriebsnr == 0)).first()

        if not argt:

            return

        for argt in db_session.query(Argt).filter(
                (Argt.betriebsnr == 0)).all():

            if not foreign_rate:
                argt.betriebsnr = local_nr
            else:
                argt.betriebsnr = foreign_nr


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        msg_str = msg_str + chr(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    local_nr = waehrungsnr

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if not waehrung:
            msg_str = msg_str + chr(2) + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "")

            return generate_output()
        foreign_nr = waehrungsnr
    update_argt()

    for arrangement in db_session.query(Arrangement).filter(
            (Arrangement.segmentcode == 0)).all():
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr == arrangement.betriebsnr)).first()
        t_arrangement.waehrungsnr = waehrung1.bezeich

    return generate_output()