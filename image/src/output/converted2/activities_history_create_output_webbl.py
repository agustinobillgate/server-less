#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

b1_list_list, B1_list = create_model("B1_list", {"datum":string, "action":string, "aenderung":string, "username":string, "zeit":string})

def activities_history_create_output_webbl(idflag:string, b1_list_list:[B1_list]):
    doneflag = False
    counter:int = 0
    queasy = None

    b1_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, queasy
        nonlocal idflag, b1_list_list
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal b1_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "b1-list": b1_list_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("System Logfiles").lower()) & (Queasy.char2 == idflag)).order_by(Queasy.number1).yield_per(100):
        counter = counter + 1

        if counter > 1000:
            break
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = entry(0, queasy.char3, "$")
        b1_list.action = entry(1, queasy.char3, "$")
        b1_list.aenderung = entry(2, queasy.char3, "$")
        b1_list.username = entry(3, queasy.char3, "$")
        b1_list.zeit = to_string(entry(4, queasy.char3, "$"))

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("System Logfiles").lower()) & (Pqueasy.char2 == idflag)).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("System Logfiles").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("System Logfiles").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()