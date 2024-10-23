from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Reslin_queasy

def arl_list_incognitobl(t_resnr:int, t_reslinnr:int, user_init:str):
    cid:str = " "
    cdate:str = " "
    s:str = ""
    res_line = reslin_queasy = None

    resline = None

    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cid, cdate, s, res_line, reslin_queasy
        nonlocal t_resnr, t_reslinnr, user_init
        nonlocal resline


        nonlocal resline
        return {}


    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == t_resnr) & (Res_line.reslinnr == t_reslinnr)).first()

    resline = db_session.query(Resline).filter(
             (Resline._recid == res_line._recid)).first()
    resline.pseudofix = not resline.pseudofix

    if trim(resline.changed_id) != "":
        cid = resline.changed_id
        cdate = to_string(resline.changed)
    resline.changed_id = user_init
    resline.changed = get_current_date()

    if resline.pseudofix:
        s = "INCOGNITO ON"

        if resline.active_flag == 1:
            get_output(intevent_1(7, res_line.zinr, "Do Not Disturb ON!", res_line.resnr, res_line.reslinnr))
    else:
        s = "INCOGNITO OFF"

        if resline.active_flag == 1:
            get_output(intevent_1(8, res_line.zinr, "Do Not Disturb OFF!", res_line.resnr, res_line.reslinnr))
    reslin_queasy = Reslin_queasy()
    db_session.add(reslin_queasy)

    reslin_queasy.key = "ResChanges"
    reslin_queasy.resnr = res_line.resnr
    reslin_queasy.reslinnr = res_line.reslinnr
    reslin_queasy.date2 = get_current_date()
    reslin_queasy.number2 = get_current_time_in_seconds()


    reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr, "x(6)") + ";" + to_string(res_line.zinr, "x(6)") + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(" ") + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string(s, "x(16)") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
    pass

    return generate_output()