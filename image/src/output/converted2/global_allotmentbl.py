from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Guest

def global_allotmentbl(gastno:int, inp_kontcode:str):
    g_list_list = []
    queasy = guest = None

    g_list = None

    g_list_list, G_list = create_model("G_list", {"gastnr":int, "gname":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_list, queasy, guest
        nonlocal gastno, inp_kontcode


        nonlocal g_list
        nonlocal g_list_list
        return {"g-list": g_list_list}

    def fill_list():

        nonlocal g_list_list, queasy, guest
        nonlocal gastno, inp_kontcode


        nonlocal g_list
        nonlocal g_list_list

        tokcounter:int = 0
        mesvalue:str = ""

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 147) & (Queasy.number1 == gastno) & (func.lower(Queasy.char1) == (inp_kontcode).lower())).first()

        if queasy:
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if mesvalue != "":

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == to_int(mesvalue))).first()

                    if guest:
                        g_list = G_list()
                        g_list_list.append(g_list)

                        g_list.gastnr = guest.gastnr
                        g_list.gname = guest.name + ", " + guest.anredefirma +\
                                guest.vorname1

    fill_list()

    return generate_output()