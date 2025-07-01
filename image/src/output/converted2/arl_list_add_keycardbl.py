#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Htparam

def arl_list_add_keycardbl(pvilanguage:int, recid_resline:int, keyint:int):

    prepare_cache ([Htparam])

    msg_str = ""
    anz0 = 0
    do_it = False
    card_type = ""
    case1 = 0
    resline_reslinnr = 0
    resline_resnr = 0
    err_flag = 0
    resline_betrieb_gast = 0
    resline_resstatus = 0
    resline_recid = 0
    t_keycard_list = []
    lvcarea:string = "arl-list"
    resno:int = 0
    i:int = 0
    maxkey:int = 2
    replaced:bool = False
    res_line = htparam = None

    resline = rline = t_keycard = None

    t_keycard_list, T_keycard = create_model("T_keycard", {"msg_str":string, "rline_betrieb_gast":int, "rline_resstatus":int, "resline_resnr":int, "resline_reslinnr":int, "rline_recid":int})

    Resline = create_buffer("Resline",Res_line)
    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, anz0, do_it, card_type, case1, resline_reslinnr, resline_resnr, err_flag, resline_betrieb_gast, resline_resstatus, resline_recid, t_keycard_list, lvcarea, resno, i, maxkey, replaced, res_line, htparam
        nonlocal pvilanguage, recid_resline, keyint
        nonlocal resline, rline


        nonlocal resline, rline, t_keycard
        nonlocal t_keycard_list

        return {"msg_str": msg_str, "anz0": anz0, "do_it": do_it, "card_type": card_type, "case1": case1, "resline_reslinnr": resline_reslinnr, "resline_resnr": resline_resnr, "err_flag": err_flag, "resline_betrieb_gast": resline_betrieb_gast, "resline_resstatus": resline_resstatus, "resline_recid": resline_recid, "t-keycard": t_keycard_list}

    res_line = get_cache (Res_line, {"_recid": [(eq, recid_resline)]})

    if not res_line:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 926)]})
    anz0 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 927)]})

    if htparam.finteger != 0:
        maxkey = htparam.finteger

    if res_line.resstatus == 11 or res_line.resstatus == 13:
        maxkey = 1

    elif keyint == 1:

        resline = db_session.query(Resline).filter(
                 (Resline.active_flag <= 1) & (((Resline.ankunft == res_line.ankunft)) | ((Resline.abreise == res_line.ankunft))) & (Resline.zinr == res_line.zinr) & (Resline.betrieb_gast > 0) & (Resline.resnr != res_line.resnr)).first()

        if resline:
            err_flag = 1
            msg_str = msg_str + chr_unicode(2) + "Keycard is being used for other guest: " + resline.name

            return generate_output()

        resline = db_session.query(Resline).filter(
                 (Resline._recid == res_line._recid)).first()

        if resline.betrieb_gast >= maxkey:
            err_flag = 2
            msg_str = msg_str + chr_unicode(2) + "Number of given KeyCard = " + to_string(resline.betrieb_gast) + chr_unicode(10) + "No more KeyCard can be generated for room " + resline.zinr

            return generate_output()
        card_type = "cardtype=1"

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == res_line.resnr) & (Rline.reslinnr != res_line.resnr) & (Rline.zinr == res_line.zinr) & (Rline.active_flag <= 1) & (Rline.betrieb_gast > 0)).first()

        if rline:
            card_type = "cardtype=2"

        if resline.betrieb_gast == 0 and resline.resstatus != 11 and resline.resstatus != 13:
            case1 = 1
        else:
            case1 = 2
        resline_reslinnr = resline.reslinnr
        resline_resnr = resline.resnr
        resline_recid = resline._recid

    elif keyint == 2:

        resline = db_session.query(Resline).filter(
                 (Resline._recid == res_line._recid)).first()

        if resline.betrieb_gast == 0:
            err_flag = 1

            return generate_output()

        if (resline.resstatus == 11 or resline.resstatus == 13):
            err_flag = 2
        card_type = "cardtype=1"
        resline_betrieb_gast = resline.betrieb_gast
        resline_reslinnr = resline.reslinnr
        resline_resnr = resline.resnr
        resline_resstatus = resline.resstatus

        if (resline.resstatus == 1 or resline.resstatus == 6) and replaced:

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == resline.resnr) & ((Rline.resstatus == 11) | (Rline.resstatus == 13)) & (Rline.zinr == resline.zinr) & (Rline.betrieb_gast > 0)).first()

            if rline:
                msg_str = msg_str + chr_unicode(2) + "&W" + "Room Shrer found. Replace the KeyCard too."

    elif keyint == 3:

        resline = db_session.query(Resline).filter(
                 (Resline._recid == res_line._recid)).first()
        resno = resline.resnr

        if anz0 == 0:
            anz0 = resline.erwachs

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resno) & (Resline.active_flag == 0) & (Resline.zinr != "")).order_by(Resline.zinr, Resline.resstatus).all():

            rline = db_session.query(Rline).filter(
                     (Rline.active_flag <= 1) & (((Rline.ankunft == resline.ankunft)) | ((Rline.abreise == resline.ankunft))) & (Rline.zinr == resline.zinr) & (Rline.betrieb_gast > 0) & (Rline.resnr != resline.resnr)).first()
            t_keycard = T_keycard()
            t_keycard_list.append(t_keycard)

            do_it = not None != rline

            if not do_it:
                t_keycard.msg_str = msg_str + chr_unicode(2) + "RmNo " + rline.zinr + " Keycard is being used for other guest: " + rline.name
            else:

                rline = db_session.query(Rline).filter(
                         (Rline._recid == resline._recid)).first()
            t_keycard.rline_betrieb_gast = rline.betrieb_gast
            t_keycard.rline_resstatus = rline.resstatus
            t_keycard.resline_resnr = resline.resnr
            t_keycard.resline_reslinnr = resline.reslinnr
            t_keycard.rline_recid = rline._recid

            if resline.betrieb_gast >= maxkey:
                t_keycard.msg_str = "Number of given KeyCard = " + to_string(resline.betrieb_gast) + chr_unicode(10) + "No more KeyCard can be generated for room " + resline.zinr

    return generate_output()