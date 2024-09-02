from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Kontline

def global_allotment_updatebl(gastno:int, inp_kontcode:str, g_list:[G_list]):
    kontcode_str = ""
    queasy = kontline = None

    g_list = None

    g_list_list, G_list = create_model("G_list", {"gastnr":int, "gname":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kontcode_str, queasy, kontline


        nonlocal g_list
        nonlocal g_list_list
        return {"kontcode_str": kontcode_str}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 147) &  (Queasy.number1 == gastno) &  (func.lower(Queasy.char1) == (inp_kontcode).lower())).first()

    if queasy:
        db_session.delete(queasy)

    for g_list in query(g_list_list):
        kontcode_str = kontcode_str + to_string(g_list.gastnr) + ","
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 147
    queasy.number1 = gastno
    queasy.char1 = inp_kontcode
    queasy.char3 = kontcode_str

    for kontline in db_session.query(Kontline).filter(
            (Kontline.gastnr == gastno) &  (func.lower(Kontline.kontcode) == (inp_kontcode).lower())).all():
        kontline.pr_code = kontcode_str

    return generate_output()