#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def prepare_ratecode_additional_webbl(inpchar3:string):
    g_list_list = []

    g_list = None

    g_list_list, G_list = create_model("G_list", {"rcode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_list
        nonlocal inpchar3


        nonlocal g_list
        nonlocal g_list_list

        return {"g-list": g_list_list}

    def fill_list():

        nonlocal g_list_list
        nonlocal inpchar3


        nonlocal g_list
        nonlocal g_list_list

        tokcounter:int = 0
        mesvalue:string = ""
        ct:string = ""

        if matches(inpchar3,r"*;*"):
            ct = entry(1, inpchar3, ";")
        else:
            ct = inpchar3
        for tokcounter in range(1,num_entries(ct, ",")  + 1) :
            mesvalue = entry(tokcounter - 1, ct, ",")

            if mesvalue != "":
                g_list = G_list()
                g_list_list.append(g_list)

                g_list.rcode = mesvalue

    fill_list()

    return generate_output()