#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_zimmerbl import read_zimmerbl
from functions.read_res_linebl import read_res_linebl
from models import Zimmer, Res_line

def fo_inv_transfer_roomok(pvilanguage:int, currroom:string):
    gname = ""
    msgstr = ""
    lvcarea:string = "fo-inv-transfer-roomok"
    zimmer = res_line = None

    t_zimmer = t_res_line = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    t_res_line_data, T_res_line = create_model_like(Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, msgstr, lvcarea, zimmer, res_line
        nonlocal pvilanguage, currroom


        nonlocal t_zimmer, t_res_line
        nonlocal t_zimmer_data, t_res_line_data

        return {"gname": gname, "msgstr": msgstr}


    if currroom != "":
        t_zimmer_data = get_output(read_zimmerbl(1, currroom, None, None))

        t_zimmer = query(t_zimmer_data, first=True)

        if not t_zimmer:
            msgstr = translateExtended ("No such room number.", lvcarea, "")
        t_res_line_data = get_output(read_res_linebl(35, None, None, None, None, currroom, None, None, None, None, ""))

        t_res_line = query(t_res_line_data, first=True)

        if not t_res_line:
            msgstr = translateExtended ("Room not occupied.", lvcarea, "")
        else:
            gname = t_res_line.name

    return generate_output()