from functions.additional_functions import *
import decimal

def ccard_verification(strcc:str):
    cardok = False
    nchecksum:int = 0
    fdbl:bool = False
    ncharpos:int = 0
    nchar:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cardok, nchecksum, fdbl, ncharpos, nchar
        nonlocal strcc


        return {"cardok": cardok}


    if len(strcc) != 16:
        cardok = False

        return generate_output()
    fdbl = False
    nchecksum = 0


    strcc = replace_str(strcc, " ", "")
    for ncharpos in range(len(strcc),1  - 1, -1) :
        nchar = asc(substring(strcc, ncharpos - 1, 1)) - asc("0")

        if 0 <= nchar and nchar <= 9:

            if (fdbl):
                nchar = nchar * 2

            if 10 <= nchar:
                nchar = nchar - 9
        nchecksum = nchecksum + nchar
        fdbl = not fdbl
    cardok = (nchecksum % 10) == 0

    return generate_output()