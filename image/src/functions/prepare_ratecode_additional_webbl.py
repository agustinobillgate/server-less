from functions.additional_functions import *
import decimal
import re

def prepare_ratecode_additional_webbl(inpchar3:str):
    g_list_list = []

    g_list = None

    g_list_list, G_list = create_model("G_list", {"rcode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_list


        nonlocal g_list
        nonlocal g_list_list
        return {"g-list": g_list_list}

    def fill_list():

        nonlocal g_list_list


        nonlocal g_list
        nonlocal g_list_list

        tokcounter:int = 0
        mesvalue:str = ""
        ct:str = ""

        if re.match(".*;.*",inpchar3):
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