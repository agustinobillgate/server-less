#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement, Waehrung, Htparam

def prepare_argt_adminbl(pvilanguage:int):

    prepare_cache ([Arrangement, Waehrung, Htparam])

    double_currency = False
    msg_str = ""
    w_list_list = []
    t_arrangement_list = []
    foreign_rate:bool = False
    local_nr:int = 0
    foreign_nr:int = 0
    lvcarea:string = "prepare-argt-admin"
    arrangement = waehrung = htparam = None

    t_arrangement = w_list = waehrung1 = None

    t_arrangement_list, T_arrangement = create_model_like(Arrangement, {"waehrungsnr":string})
    w_list_list, W_list = create_model("W_list", {"bez":string, "first_bez":string})

    Waehrung1 = create_buffer("Waehrung1",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, msg_str, w_list_list, t_arrangement_list, foreign_rate, local_nr, foreign_nr, lvcarea, arrangement, waehrung, htparam
        nonlocal pvilanguage
        nonlocal waehrung1


        nonlocal t_arrangement, w_list, waehrung1
        nonlocal t_arrangement_list, w_list_list

        return {"double_currency": double_currency, "msg_str": msg_str, "w-list": w_list_list, "t-arrangement": t_arrangement_list}

    def update_argt():

        nonlocal double_currency, msg_str, w_list_list, t_arrangement_list, foreign_rate, local_nr, foreign_nr, lvcarea, arrangement, waehrung, htparam
        nonlocal pvilanguage
        nonlocal waehrung1


        nonlocal t_arrangement, w_list, waehrung1
        nonlocal t_arrangement_list, w_list_list

        argt = None
        Argt =  create_buffer("Argt",Arrangement)

        if foreign_rate:

            for waehrung1 in db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr != foreign_nr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.bez = waehrung1.bezeich

            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, foreign_nr)]})

            if waehrung1:
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.first_bez = waehrung1.bezeich


        else:

            for waehrung1 in db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr != local_nr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.bez = waehrung1.bezeich

            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, local_nr)]})

            if waehrung1:
                w_list = W_list()
                w_list_list.append(w_list)

                w_list.first_bez = waehrung1.bezeich

        argt = get_cache (Arrangement, {"betriebsnr": [(eq, 0)]})

        if not argt:

            return

        for argt in db_session.query(Argt).filter(
                 (Argt.betriebsnr == 0)).order_by(Argt._recid).all():

            if not foreign_rate:
                argt.betriebsnr = local_nr
            else:
                argt.betriebsnr = foreign_nr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    local_nr = waehrung.waehrungsnr

    if foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if not waehrung:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "")

            return generate_output()
        foreign_nr = waehrung.waehrungsnr
    update_argt()

    for arrangement in db_session.query(Arrangement).filter(
             (Arrangement.segmentcode == 0)).order_by(Arrangement.argtnr).all():
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})
        t_arrangement.waehrungsnr = waehrung1.bezeich

    return generate_output()