from functions.additional_functions import *
import decimal
from models import Paramtext

def read_hotelnamebl(param_str:str):
    hotel_name = ""
    param_nr:int = 0
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hotel_name, param_nr, paramtext


        return {"hotel_name": hotel_name}

    def decode_string(in_str:str):

        nonlocal hotel_name, param_nr, paramtext

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    param_nr = to_int(substring(param_str, 1))
    param_nr = param_nr * 2

    if param_nr != 240:

        return generate_output()

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 240)).first()

    if not paramtext:

        return generate_output()

    if paramtext and paramtext.ptexte != "":
        hotel_name = decode_string(paramtext.ptexte)

    return generate_output()