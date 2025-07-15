#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

source_data, Source = create_model_like(Queasy)

def egsource_btn_exitbl(source_data:[Source], case_type:int, rec_id:int):

    prepare_cache ([Queasy])

    fl_code = 0
    queasy = None

    source = queri = None

    Queri = create_buffer("Queri",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queri


        nonlocal source, queri

        return {"fl_code": fl_code}

    def fill_new_queasy():

        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queri


        nonlocal source, queri


        queasy.key = 130
        queasy.number1 = source.number1
        queasy.char1 = source.char1


    source = query(source_data, first=True)

    if case_type == 1:

        queri = get_cache (Queasy, {"number1": [(eq, source.number1)],"key": [(eq, 130)]})

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = get_cache (Queasy, {"char1": [(eq, source.char1)],"key": [(eq, 130)]})

            if queri:
                fl_code = 2

                return generate_output()
            else:
                queasy = Queasy()
                db_session.add(queasy)

                fill_new_queasy()
                fl_code = 3

    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

        queri = get_cache (Queasy, {"number1": [(eq, source.number1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 130)],"_recid": [(ne, queasy._recid)]})

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = get_cache (Queasy, {"char1": [(eq, source.char1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 130)],"_recid": [(ne, queasy._recid)]})

            if queri:
                fl_code = 2

                return generate_output()
            else:
                pass
                queasy.number1 = source.number1
                queasy.char1 = source.char1
                pass
                fl_code = 3

    return generate_output()