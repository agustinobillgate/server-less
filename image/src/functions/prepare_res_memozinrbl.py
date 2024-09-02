from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from functions.htpchar import htpchar

def prepare_res_memozinrbl():
    htpint = 0
    ext_char = ""


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpint, ext_char


        return {"htpint": htpint, "ext_char": ext_char}

    htpint = get_output(htpint(297))
    ext_char = get_output(htpchar(148))

    return generate_output()