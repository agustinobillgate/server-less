from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from functions.htpchar import htpchar
from functions.htpint import htpint
from functions.htpdec import htpdec

def gethtpbl(casetype:int, inp_param:int):
    flogical = False
    fdate = None
    fchar = ""
    fint = 0
    fdec = to_decimal("0.0")


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flogical, fdate, fchar, fint, fdec
        nonlocal casetype, inp_param


        return {"flogical": flogical, "fdate": fdate, "fchar": fchar, "fint": fint, "fdec": fdec}


    if casetype == 1:
        flogical = get_output(htplogic(inp_param))
    elif casetype == 2:
        fdate = get_output(htpdate(inp_param))
    elif casetype == 3:
        fchar = get_output(htpchar(inp_param))
    elif casetype == 4:
        fint = get_output(htpint(inp_param))
    elif casetype == 5:
        fdec = get_output(htpdec(inp_param))

    return generate_output()