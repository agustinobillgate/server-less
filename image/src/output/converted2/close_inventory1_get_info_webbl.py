from functions.additional_functions import *
import decimal
from models import Queasy

def close_inventory1_get_info_webbl(pvilanguage:int):
    close_done = False
    msg_str = ""
    plist_list = []
    inpfile:str = ""
    lic_nr:str = ""
    search_txt:str = ""
    temp_char:str = ""
    counter:int = 0
    lvcarea:str = "close-inventory"
    queasy = None

    plist = bqueasy = pqueasy = mqueasy = None

    plist_list, Plist = create_model("Plist", {"bezeich":str, "progres":str, "counter":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Mqueasy = create_buffer("Mqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_done, msg_str, plist_list, inpfile, lic_nr, search_txt, temp_char, counter, lvcarea, queasy
        nonlocal pvilanguage
        nonlocal bqueasy, pqueasy, mqueasy


        nonlocal plist, bqueasy, pqueasy, mqueasy
        nonlocal plist_list
        return {"close_done": close_done, "msg_str": msg_str, "plist": plist_list}


    plist_list.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 279) & (Queasy.date1 == get_current_date())).order_by(Queasy.number1).all():
        plist = Plist()
        plist_list.append(plist)

        plist.bezeich = queasy.char2
        plist.progres = queasy.char3
        counter = counter + 1
        plist.counter = counter

    bqueasy = db_session.query(Bqueasy).filter(
             (Bqueasy.key == 283) & (Bqueasy.date1 == get_current_date())).first()

    if bqueasy:
        msg_str = bqueasy.char1
        close_done = True

        for pqueasy in db_session.query(Pqueasy).filter(
                 (Pqueasy.key == 279) & (Pqueasy.date1 == TODAY)).order_by(Pqueasy._recid).all():
            pqueasy_list.remove(pqueasy)

        return generate_output()

    bqueasy = db_session.query(Bqueasy).filter(
             (Bqueasy.key == 279) & (Bqueasy.date1 == get_current_date())).first()

    if not bqueasy:

        mqueasy = db_session.query(Mqueasy).filter(
                 (Mqueasy.key == 296) & (Mqueasy.number2 == 1)).first()

        if mqueasy:
            close_done = False


        else:
            close_done = True

            pqueasy = db_session.query(Pqueasy).filter(
                     (Pqueasy.key == 296) & (Pqueasy.number2 == 0)).first()

            if pqueasy:
                pqueasy_list.remove(pqueasy)
                pass
    else:

        mqueasy = db_session.query(Mqueasy).filter(
                 (Mqueasy.key == 296) & (Mqueasy.number2 == 0)).first()

        if mqueasy:
            close_done = True

            pqueasy = db_session.query(Pqueasy).filter(
                     (Pqueasy.key == 296) & (Pqueasy.number2 == 0)).first()

            if pqueasy:
                pqueasy_list.remove(pqueasy)
                pass

            for bqueasy in db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 279) & (Bqueasy.date1 == TODAY)).order_by(Bqueasy._recid).all():
                bqueasy_list.remove(bqueasy)

    return generate_output()