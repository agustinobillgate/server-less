from functions.additional_functions import *
import decimal
from models import Paramtext

def prepare_if_dataexchangebl():
    htlno = ""
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htlno, paramtext

        return {"htlno": htlno}

    def decode_string(in_str:str):

        nonlocal htlno, paramtext

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        htlno = decode_string(paramtext.ptexte)

    return generate_output()