#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 2/8/2025
# GL by voucher kosong
# Rd, 25/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_jourefbl import gl_jourefbl
from models import Queasy
from sqlalchemy import func

def gl_jouref_webbl(idflag:string, sorttype:int, from_date:date, to_date:date, from_refno:string):

    prepare_cache ([Queasy])

    counter:int = 0
    queasy = None

    output_list = bqueasy = tqueasy = None

    output_list_data, Output_list = create_model("Output_list", {"str":string, "refno":string})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, queasy
        nonlocal idflag, sorttype, from_date, to_date, from_refno
        nonlocal bqueasy, tqueasy


        nonlocal output_list, bqueasy, tqueasy
        nonlocal output_list_data

        return {}


    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Journalist by voucher"
    queasy.number1 = 1
    queasy.char2 = idflag
    pass
    output_list_data = get_output(gl_jourefbl(sorttype, from_date, to_date, from_refno))
    # print(output_list_data)
    # output_list = query(output_list_data, first=True)
    # while None != output_list:
    #     counter = counter + 1


    #     queasy = Queasy()
    #     db_session.add(queasy)

    #     queasy.key = 280
    #     queasy.char1 = "Journalist by voucher"
    #     queasy.char3 = idflag
    #     queasy.char2 = output_list.str + "|" +\
    #             output_list.refno
    #     queasy.number1 = counter

    #     output_list = query(output_list_data, next=True)
    
    counter = 0
    queasy_list = []
    # print("nRec:", len(output_list_data))
    if output_list_data: 
        for output in output_list_data:
            counter += 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Journalist by voucher"
            queasy.char3 = idflag
            queasy.char2 = output.str + "|" + output.refno
            queasy.number1 = counter
            # print("Counter:", counter)
            db_session.commit()


    # Rd, 25/11/2025, with_for_update
    # bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "journalist by voucher")],"char2": [(eq, idflag)]})
    bqueasy = db_session.query(Queasy).filter(Queasy.key == 285, func.lower(Queasy.char1) == "journalist by voucher", Queasy.char2 == idflag).with_for_update().first()

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()