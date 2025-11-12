#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# =========================================

from functions.additional_functions import *
from decimal import Decimal

def entschl_str70(keystr:string, in_str:string):
    out_str = ""
    s:string = ""
    j:int = 0
    len_:int = 0
    ch:string = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_str, s, j, len_, ch
        nonlocal keystr, in_str

        return {"out_str": out_str}


    if keystr.lower()  != (("d" + "o" + "-" + "i" + "t").lower()):

        return generate_output()

    if length(in_str) == 0:

        return generate_output()
    s = in_str
    j = asc(substring(s, 0, 1)) - 70
    len_ = length(in_str) - 1
    s = substring(in_str, 1, len_)
    for len_ in range(1,length(s)  + 1) :
        out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

    return generate_output()