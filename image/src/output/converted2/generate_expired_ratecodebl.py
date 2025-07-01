#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Queasy

def generate_expired_ratecodebl(fdate:date):

    prepare_cache ([Queasy])

    output_list_list = []
    ratecode = queasy = None

    output_list = bratecode = None

    output_list_list, Output_list = create_model("Output_list", {"ratecode":string, "bezeich":string, "remarks":string})

    Bratecode = create_buffer("Bratecode",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, ratecode, queasy
        nonlocal fdate
        nonlocal bratecode


        nonlocal output_list, bratecode
        nonlocal output_list_list

        return {"output-list": output_list_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(char1).all():

        ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)]})

        if ratecode:

            bratecode = db_session.query(Bratecode).filter(
                     (Bratecode.code == queasy.char1) & (Bratecode.endperiode >= fdate)).first()

            if not bratecode:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ratecode = queasy.char1
                output_list.bezeich = queasy.char2
                output_list.remarks = "Expired Rate"

        if not ratecode:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.ratecode = queasy.char1
            output_list.bezeich = queasy.char2
            output_list.remarks = "Empty Rate"

    return generate_output()