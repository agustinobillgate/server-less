from functions.additional_functions import *
import decimal

def entschl_str70(keystr:str, in_str:str):
    out_str = ""
    s:str = ""
    j:int = 0
    len_:int = 0
    ch:str = ""


    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_str, s, j, len_, ch
        nonlocal keystr, in_str

        return {"out_str": out_str}


    if keystr.lower()  != (("d" + "o" + "-" + "i" + "t").lower()):

        return generate_output()

    if len(in_str) == 0:

        return generate_output()
    s = in_str
    j = asc(substring(s, 0, 1)) - 70
    len_ = len(in_str) - 1
    s = substring(in_str, 1, len_)
    for len_ in range(1,len(s)  + 1) :
        out_str = out_str + chr(asc(substring(s, len_ - 1, 1)) - j)

    return generate_output()