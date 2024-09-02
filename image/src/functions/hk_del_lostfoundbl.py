from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Queasy, Res_history, Guestbook

def hk_del_lostfoundbl(userinit:str, rec_id:int):
    curr_nr:int = 0
    bediener = queasy = res_history = guestbook = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_nr, bediener, queasy, res_history, guestbook
        nonlocal userinit, rec_id


        return {}


    if not bediener or not(bediener.userinit.lower()  == (userinit).lower()):
        bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (userinit).lower())).first()

    if not queasy or not(queasy._recid == rec_id):
        queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()
    curr_nr = queasy.number3
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Delete LostFound No" +\
            to_string(queasy.number3, ">>>9") +\
            " Room " + queasy.char1


    res_history.action = "HouseKeeping"
    pass
    db_session.delete(queasy)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 195) &  (func.lower(Queasy.char1) == ("LostAndFound;nr=" + to_string(curr_nr).lower()))).order_by(Queasy._recid).all():

        if not guestbook or not(guestbook.gastnr == queasy.number1):
            guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr == queasy.number1)).first()

        if guestbook:
            db_session.delete(guestbook)
        db_session.delete(queasy)

    return generate_output()