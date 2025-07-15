from functions.additional_functions import *
import decimal
from models import Res_line, Reslin_queasy

def mk_resline_res_fixartbl(reslin_list_resnr:int, reslin_list_reslinnr:int, reslin_list_changed_id:str, reslin_list_changed:int, reslin_list_reserve_char:str, user_init:str, fixed_rate:bool):
    cid:str = " "
    cdate:str = " "
    res_line = reslin_queasy = None

    resline = None

    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cid, cdate, res_line, reslin_queasy
        nonlocal reslin_list_resnr, reslin_list_reslinnr, reslin_list_changed_id, reslin_list_changed, reslin_list_reserve_char, user_init, fixed_rate
        nonlocal resline


        nonlocal resline
        return {}


    resline = db_session.query(Resline).filter(
             (Resline.resnr == reslin_list_resnr) & (Resline.reslinnr == reslin_list_reslinnr)).first()

    if trim(reslin_list_changed_id) != "":
        cid = reslin_list_changed_id
        cdate = to_string(reslin_list_changed)

    elif len(reslin_list_reserve_char) >= 14:
        cid = substring(reslin_list_reserve_char, 13)
    reslin_queasy = Reslin_queasy()
    db_session.add(reslin_queasy)

    reslin_queasy.key = "ResChanges"
    reslin_queasy.resnr = reslin_list_resnr
    reslin_queasy.reslinnr = reslin_list_reslinnr
    reslin_queasy.date2 = get_current_date()
    reslin_queasy.number2 = get_current_time_in_seconds()


    reslin_queasy.char3 = to_string(resline.ankunft) + ";" + to_string(resline.ankunft) + ";" + to_string(resline.abreise) + ";" + to_string(resline.abreise) + ";" + to_string(resline.zimmeranz) + ";" + to_string(resline.zimmeranz) + ";" + to_string(resline.erwachs) + ";" + to_string(resline.erwachs) + ";" + to_string(resline.kind1) + ";" + to_string(resline.kind1) + ";" + to_string(resline.gratis) + ";" + to_string(resline.gratis) + ";" + to_string(resline.zikatnr) + ";" + to_string(resline.zikatnr) + ";" + to_string(resline.zinr) + ";" + to_string(resline.zinr) + ";" + to_string(resline.arrangement) + ";" + to_string(resline.arrangement) + ";" + to_string(resline.zipreis) + ";" + to_string(resline.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate) + ";" + to_string(get_current_date()) + ";" + to_string(" ") + ";" + to_string("Called FixArt") + ";"

    if resline.was_status == 0:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";"
    else:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"

    if not fixed_rate:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";"
    else:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"
    pass

    return generate_output()