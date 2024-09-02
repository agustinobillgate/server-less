from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from functions.htpchar import htpchar

def prepare_floorplanbl():
    p_87 = None
    p_48 = 0
    p_141 = ""
    p_109 = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_87, p_48, p_141, p_109


        return {"p_87": p_87, "p_48": p_48, "p_141": p_141, "p_109": p_109}

    p_87 = get_output(htpdate(87))
    p_48 = get_output(htpint(48))
    p_141 = get_output(htpchar(141))
    p_109 = get_output(htpint(109))

    return generate_output()