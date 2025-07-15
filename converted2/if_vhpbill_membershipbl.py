#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Guest, Bill, Bediener

def if_vhpbill_membershipbl(inp_rechnr:int):

    prepare_cache ([Res_line, Guest, Bill, Bediener])

    username = ""
    gremark = ""
    res_line = guest = bill = bediener = None

    rline = gbuff = None

    Rline = create_buffer("Rline",Res_line)
    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal username, gremark, res_line, guest, bill, bediener
        nonlocal inp_rechnr
        nonlocal rline, gbuff


        nonlocal rline, gbuff

        return {"username": username, "gremark": gremark}


    bill = get_cache (Bill, {"rechnr": [(eq, inp_rechnr)]})

    rline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

    if rline:

        gbuff = get_cache (Guest, {"gastnr": [(eq, rline.gastnrmember)]})

        if gbuff:
            gremark = gbuff.bemerkung

        bediener = get_cache (Bediener, {"userinit": [(eq, rline.changed_id)]})

        if bediener:
            username = bediener.username

    return generate_output()