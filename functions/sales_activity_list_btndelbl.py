#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import B_storno

output_list_data, Output_list = create_model("Output_list", {"outnr":int, "act_str":string})

def sales_activity_list_btndelbl(resnr:int, counter_reason:int, outnr:int, output_list_data:[Output_list]):

    prepare_cache ([B_storno])

    output_list_data = []
    b_storno = None

    output_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, b_storno
        nonlocal resnr, counter_reason, outnr


        nonlocal output_list

        return {"output-list": output_list_data}

    def create_outlist():

        nonlocal output_list_data, b_storno
        nonlocal resnr, counter_reason, outnr


        nonlocal output_list

        i:int = 0
        counter_reason = 0
        output_list_data.clear()
        for i in range(1,18 + 1) :

            if b_storno.grund[i - 1] != "":
                output_list = Output_list()
                output_list_data.append(output_list)

                outnr = i
                act_str = b_storno.grund[i - 1]


                counter_reason = i


    def reorg_outlist():

        nonlocal output_list_data, b_storno
        nonlocal resnr, counter_reason, outnr


        nonlocal output_list

        i:int = 0

        for output_list in query(output_list_data):

            b_storno = get_cache (B_storno, {"bankettnr": [(eq, resnr)],"outnr": [(eq, outnr)]})
            pass

            if output_list.outnr < 18:
                for i in range((output_list.outnr + 1),18 + 1) :
                    b_storno.grund[i - 1 - 1] = b_storno.grund[i - 1]
            b_storno.grund[counter_reason - 1] = ""
            create_outlist()

    reorg_outlist()

    return generate_output()