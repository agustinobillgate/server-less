from functions.additional_functions import *
import decimal
from models import Res_line, History, Guest

def gcf_rsvlistbl(gastno:int):
    rline_list_list = []
    res_line = history = guest = None

    rline_list = None

    rline_list_list, Rline_list = create_model("Rline_list", {"resstatus":int, "resnr":int, "name":str, "ankunft":date, "abreise":date, "zinr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rline_list_list, res_line, history, guest


        nonlocal rline_list
        nonlocal rline_list_list
        return {"rline-list": rline_list_list}

    for res_line in db_session.query(Res_line).filter(
            (Res_line.gastnrmember == gastno) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99) &  (Res_line.l_zuordnung[2] != 1)).all():

        history = db_session.query(History).filter(
                (History.gastnr == gastno)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastno)).first()
        rline_list = Rline_list()
        rline_list_list.append(rline_list)

        buffer_copy(res_line, rline_list,except_fields=["res_line.name"])
        rline_list.name = guest.name

    return generate_output()