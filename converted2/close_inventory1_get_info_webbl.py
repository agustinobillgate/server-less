#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def close_inventory1_get_info_webbl(pvilanguage:int):
    close_done = False
    msg_str = ""
    plist_data = []
    inpfile:string = ""
    lic_nr:string = ""
    search_txt:string = ""
    temp_char:string = ""
    counter:int = 0
    lvcarea:string = "close-inventory"
    queasy = None

    plist = bqueasy = pqueasy = mqueasy = None

    plist_data, Plist = create_model("Plist", {"bezeich":string, "progres":string, "counter":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Mqueasy = create_buffer("Mqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_done, msg_str, plist_data, inpfile, lic_nr, search_txt, temp_char, counter, lvcarea, queasy
        nonlocal pvilanguage
        nonlocal bqueasy, pqueasy, mqueasy


        nonlocal plist, bqueasy, pqueasy, mqueasy
        nonlocal plist_data

        return {"close_done": close_done, "msg_str": msg_str, "plist": plist_data}


    plist_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 279) & (Queasy.date1 == get_current_date())).order_by(Queasy.number1).all():
        plist = Plist()
        plist_data.append(plist)

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
            db_session.delete(pqueasy)

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
                pass
                db_session.delete(pqueasy)
                pass
    else:

        mqueasy = db_session.query(Mqueasy).filter(
                 (Mqueasy.key == 296) & (Mqueasy.number2 == 0)).first()

        if mqueasy:
            close_done = True

            pqueasy = db_session.query(Pqueasy).filter(
                     (Pqueasy.key == 296) & (Pqueasy.number2 == 0)).first()

            if pqueasy:
                pass
                db_session.delete(pqueasy)
                pass

            for bqueasy in db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 279) & (Bqueasy.date1 == TODAY)).order_by(Bqueasy._recid).all():
                db_session.delete(bqueasy)

    return generate_output()