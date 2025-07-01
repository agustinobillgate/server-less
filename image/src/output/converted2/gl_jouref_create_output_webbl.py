#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

output_list_list, Output_list = create_model("Output_list", {"str":string, "refno":string})

def gl_jouref_create_output_webbl(idflag:string, output_list_list:[Output_list]):
    doneflag = False
    counter:int = 0
    queasy = None

    output_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, queasy
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal output_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "output-list": output_list_list}

    queasy = get_cache (Queasy, {"key": [(eq, 280)],"char1": [(eq, "journalist by voucher")],"char3": [(eq, idflag)]})
    while None != queasy:
        counter = counter + 1

        if counter > 7000:
            break
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = entry(0, queasy.char2, "|")
        output_list.refno = entry(1, queasy.char2, "|")

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        db_session.delete(bqueasy)
        pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == ("Journalist by voucher").lower()) & (Queasy.char3 == idflag) & (Queasy._recid > curr_recid)).first()

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Journalist by voucher").lower()) & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Journalist by voucher").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Journalist by voucher").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()