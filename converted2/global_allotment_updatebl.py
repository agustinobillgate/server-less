#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Kontline

g_list_data, G_list = create_model("G_list", {"gastnr":int, "gname":string})

def global_allotment_updatebl(gastno:int, inp_kontcode:string, g_list_data:[G_list]):

    prepare_cache ([Kontline])

    kontcode_str = ""
    queasy = kontline = None

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kontcode_str, queasy, kontline
        nonlocal gastno, inp_kontcode


        nonlocal g_list

        return {"kontcode_str": kontcode_str}

    queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, gastno)],"char1": [(eq, inp_kontcode)]})

    if queasy:
        db_session.delete(queasy)

    for g_list in query(g_list_data):
        kontcode_str = kontcode_str + to_string(g_list.gastnr) + ","
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 147
    queasy.number1 = gastno
    queasy.char1 = inp_kontcode
    queasy.char3 = kontcode_str

    for kontline in db_session.query(Kontline).filter(
             (Kontline.gastnr == gastno) & (Kontline.kontcode == (inp_kontcode).lower())).order_by(Kontline._recid).all():
        kontline.pr_code = kontcode_str

    return generate_output()