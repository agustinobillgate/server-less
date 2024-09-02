from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpchar import htpchar

def prepare_foreign_listbl():
    fdate = None
    def_nat = ""


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, def_nat


        return {"fdate": fdate, "def_nat": def_nat}

    fdate = get_output(htpdate(87))
    def_nat = get_output(htpchar(153))

    return generate_output()