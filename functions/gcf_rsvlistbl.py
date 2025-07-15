#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, History, Guest

def gcf_rsvlistbl(gastno:int):

    prepare_cache ([Guest])

    rline_list_data = []
    res_line = history = guest = None

    rline_list = None

    rline_list_data, Rline_list = create_model("Rline_list", {"resstatus":int, "resnr":int, "name":string, "ankunft":date, "abreise":date, "zinr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rline_list_data, res_line, history, guest
        nonlocal gastno


        nonlocal rline_list
        nonlocal rline_list_data

        return {"rline-list": rline_list_data}

    for res_line in db_session.query(Res_line).filter(
             (Res_line.gastnrmember == gastno) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] != 1)).order_by(Res_line._recid).all():

        history = get_cache (History, {"gastnr": [(eq, gastno)]})

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})
        rline_list = Rline_list()
        rline_list_data.append(rline_list)

        buffer_copy(res_line, rline_list,except_fields=["res_line.name"])
        rline_list.name = guest.name

    return generate_output()