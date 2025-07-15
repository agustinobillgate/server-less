#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def read_hotelnamebl(param_str:string):

    prepare_cache ([Paramtext])

    hotel_name = ""
    param_nr:int = 0
    paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hotel_name, param_nr, paramtext
        nonlocal param_str

        return {"hotel_name": hotel_name}

    def decode_string(in_str:string):

        nonlocal hotel_name, param_nr, paramtext
        nonlocal param_str

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    param_nr = to_int(substring(param_str, 1))
    param_nr = param_nr * 2

    if param_nr != 240:

        return generate_output()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

    if not paramtext:

        return generate_output()

    if paramtext and paramtext.ptexte != "":
        hotel_name = decode_string(paramtext.ptexte)

    return generate_output()