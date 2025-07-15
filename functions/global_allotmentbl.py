#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guest

def global_allotmentbl(gastno:int, inp_kontcode:string):

    prepare_cache ([Queasy, Guest])

    g_list_data = []
    queasy = guest = None

    g_list = None

    g_list_data, G_list = create_model("G_list", {"gastnr":int, "gname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_data, queasy, guest
        nonlocal gastno, inp_kontcode


        nonlocal g_list
        nonlocal g_list_data

        return {"g-list": g_list_data}

    def fill_list():

        nonlocal g_list_data, queasy, guest
        nonlocal gastno, inp_kontcode


        nonlocal g_list
        nonlocal g_list_data

        tokcounter:int = 0
        mesvalue:string = ""

        queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, gastno)],"char1": [(eq, inp_kontcode)]})

        if queasy:
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if mesvalue != "":

                    guest = get_cache (Guest, {"gastnr": [(eq, to_int(mesvalue))]})

                    if guest:
                        g_list = G_list()
                        g_list_data.append(g_list)

                        g_list.gastnr = guest.gastnr
                        g_list.gname = guest.name + ", " + guest.anredefirma +\
                                guest.vorname1

    fill_list()

    return generate_output()