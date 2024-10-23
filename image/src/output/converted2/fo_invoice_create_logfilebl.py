from functions.additional_functions import *
import decimal
from models import Res_line, Guest, Reslin_queasy

def fo_invoice_create_logfilebl(resno:int, reslinno:int, rmno:str, user_init:str):
    res_line = guest = reslin_queasy = None

    resline = guest1 = None

    Resline = create_buffer("Resline",Res_line)
    Guest1 = create_buffer("Guest1",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, guest, reslin_queasy
        nonlocal resno, reslinno, rmno, user_init
        nonlocal resline, guest1


        nonlocal resline, guest1
        return {}


    resline = db_session.query(Resline).filter(
             (Resline.resnr == resno) & (Resline.reslinnr == reslinno)).first()
    reslin_queasy = Reslin_queasy()
    db_session.add(reslin_queasy)

    reslin_queasy.key = "ResChanges"
    reslin_queasy.resnr = resline.resnr
    reslin_queasy.reslinnr = resline.reslinnr
    reslin_queasy.date2 = get_current_date()
    reslin_queasy.number2 = get_current_time_in_seconds()


    reslin_queasy.char3 = to_string(resline.ankunft) + ";" + to_string(resline.ankunft) + ";" + to_string(resline.abreise) + ";" + to_string(resline.abreise) + ";" + to_string(resline.zimmeranz) + ";" + to_string(resline.zimmeranz) + ";" + to_string(resline.erwachs) + ";" + to_string(resline.erwachs) + ";" + to_string(resline.kind1) + ";" + to_string(resline.kind1) + ";" + to_string(resline.gratis) + ";" + to_string(resline.gratis) + ";" + to_string(resline.zikatnr) + ";" + to_string(resline.zikatnr) + ";" + to_string(resline.zinr) + ";" + to_string(resline.zinr) + ";" + to_string(resline.arrangement) + ";" + to_string(resline.arrangement) + ";" + to_string(resline.zipreis) + ";" + to_string(resline.zipreis) + ";"

    if rmno != "":
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(resline.name) + ";" + to_string("Transf to " + rmno) + ";"
    else:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(resline.name) + ";" + to_string("UNDO Transfer") + ";"

    if resline.was_status == 0:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";" + to_string(" NO") + ";"
    else:
        reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";" + to_string("YES") + ";"
    pass

    return generate_output()