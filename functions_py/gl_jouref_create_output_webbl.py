#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
# Rd, 25/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy
from sqlalchemy import func

output_list_data, Output_list = create_model("Output_list", {"str":string, "refno":string})

def gl_jouref_create_output_webbl(idflag:string, output_list_data:[Output_list]):
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

        return {"doneflag": doneflag, "output-list": output_list_data}

    queasy = get_cache (Queasy, {"key": [(eq, 280)],"char1": [(eq, "Journalist by voucher")],"char3": [(eq, idflag)]})
    while None != queasy:
        counter = counter + 1

        if counter > 7000:
            break
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.str = entry(0, queasy.char2, "|")
        output_list.refno = entry(1, queasy.char2, "|")

        # bqueasy = db_session.query(Bqueasy).filter(
        #          (Bqueasy._recid == queasy._recid)).first()
        # Rd 14/8/2025
        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).with_for_update().first()

        if bqueasy:
            db_session.delete(bqueasy)
        pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (func.lower(Queasy.char1) == "journalist by voucher") & (Queasy.char3 == idflag) & (Queasy._recid > curr_recid)).first()

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (func.lower(Pqueasy.char1) == "journalist by voucher") & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (func.lower(Tqueasy.char1) == "journalist by voucher") & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    # tqueasy = db_session.query(Tqueasy).filter(
    #          (Tqueasy.key == 285) & (func.lower(Tqueasy.char1) == "journalist by voucher") & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()
    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (func.lower(Tqueasy.char1) == "journalist by voucher") & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).with_for_update().first()
    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()