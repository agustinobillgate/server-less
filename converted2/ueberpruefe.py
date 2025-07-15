from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def ueberpruefe(uname:str, id:str):
    usrnr = -1
    nr:int = 0
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal usrnr, nr, bediener
        nonlocal uname, id

        return {"usrnr": usrnr}

    def decode_usercode():

        nonlocal usrnr, nr, bediener
        nonlocal uname, id

        nr = -1
        found:bool = False
        passwd:str = ""
        usr = None

        def generate_inner_output():
            return (nr)

        Usr =  create_buffer("Usr",Bediener)

        usr = db_session.query(Usr).filter(
                 (func.lower(Usr.username) == (uname).lower()) & (Usr.flag == 0) & (Usr.betriebsnr == 1)).first()
        while None != usr and not found:
            passwd = decode_string1(usr.usercode)

            if passwd.lower()  == (id).lower() :
                nr = usr.nr
                found = True
            else:

                curr_recid = usr._recid
                usr = db_session.query(Usr).filter(
                         (func.lower(Usr.username) == (uname).lower()) & (Usr.flag == 0) & (Usr.betriebsnr == 1) & (Usr._recid > curr_recid)).first()

        return generate_inner_output()


    def decode_string1(in_str:str):

        nonlocal usrnr, nr, bediener
        nonlocal uname, id

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (len(out_str) - 4))

        return generate_inner_output()


    nr = decode_usercode()
    usrnr = nr

    return generate_output()