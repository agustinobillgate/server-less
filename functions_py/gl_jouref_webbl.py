#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_jourefbl import gl_jourefbl
from models import Queasy

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

    if output_list:  # this will skip the loop if output_list is None or empty
        for output in output_list:
            counter += 1

            queasy = {
                "KEY": 280,
                "char1": "Journalist by voucher",
                "char3": idflag,
                "char2": f"{output.str}|{output.refno}",
                "number1": counter
            }

            queasy_list.append(queasy)


    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "journalist by voucher")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()