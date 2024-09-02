from functions.additional_functions import *
import decimal
from models import B_storno

def sales_activity_list_btndelbl(resnr:int, counter_reason:int, outnr:int, output_list:[Output_list]):
    b_storno = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"outnr":int, "act_str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_storno


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def create_outlist():

        nonlocal b_storno


        nonlocal output_list
        nonlocal output_list_list

        i:int = 0
        counter_reason = 0
        output_list_list.clear()
        for i in range(1,18 + 1) :

            if b_storno.grund[i - 1] != "":
                output_list = Output_list()
                output_list_list.append(output_list)

                outnr = i
                act_str = b_storno.grund[i - 1]


                counter_reason = i

    def reorg_outlist():

        nonlocal b_storno


        nonlocal output_list
        nonlocal output_list_list

        i:int = 0

        for output_list in query(output_list_list):

            b_storno = db_session.query(B_storno).filter(
                    (B_storno.bankettnr == resnr) &  (output_list.outnr == outnr)).first()

            b_storno = db_session.query(B_storno).first()

            if output_list.outnr < 18:
                for i in range((output_list.outnr + 1),18 + 1) :
                    b_storno.grund[i - 1 - 1] = b_storno.grund[i - 1]
            b_storno.grund[counter_reason - 1] = ""
            create_outlist()


    reorg_outlist()

    return generate_output()