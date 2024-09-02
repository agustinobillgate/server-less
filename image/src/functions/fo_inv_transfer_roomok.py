from functions.additional_functions import *
import decimal
from functions.read_zimmerbl import read_zimmerbl
from functions.read_res_linebl import read_res_linebl
from models import Zimmer, Res_line

def fo_inv_transfer_roomok(pvilanguage:int, currroom:str):
    gname = ""
    msgstr = ""
    lvcarea:str = "fo_inv_transfer_roomok"
    zimmer = res_line = None

    t_zimmer = t_res_line = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    t_res_line_list, T_res_line = create_model_like(Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, msgstr, lvcarea, zimmer, res_line


        nonlocal t_zimmer, t_res_line
        nonlocal t_zimmer_list, t_res_line_list
        return {"gname": gname, "msgstr": msgstr}


    if currroom != "":
        t_zimmer_list = get_output(read_zimmerbl(1, currroom, None, None))

        t_zimmer = query(t_zimmer_list, first=True)

        if not t_zimmer:
            msgstr = translateExtended ("No such room number.", lvcarea, "")
        t_res_line_list = get_output(read_res_linebl(35, None, None, None, None, currroom, None, None, None, None, ""))

        t_res_line = query(t_res_line_list, first=True)

        if not t_res_line:
            msgstr = translateExtended ("Room not occupied.", lvcarea, "")
        gname = t_res_line.name

    return generate_output()