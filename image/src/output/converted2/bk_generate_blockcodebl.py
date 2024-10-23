from functions.additional_functions import *
import decimal
from datetime import date

def bk_generate_blockcodebl(gname:str, startdate:date):
    blockcode = ""
    icounter:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal blockcode, icounter
        nonlocal gname, startdate


        return {"blockcode": blockcode}

    icounter = 0
    gname = replace_str(gname, " ", "")
    gname = substring(gname, 0, 4)

    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.name == gname) & (Bk_master.startdate == startdate)).order_by(Bk_master._recid.desc()).first()

    if bk_master:
        icounter = to_int(entry(1, bk_master.block_code, "/")) + 1
    else:
        icounter = 1
    blockcode = gname + to_string(get_year(startdate) , "9999") + to_string(get_month(startdate) , "99") + to_string(get_day(startdate) , "99") + "/" + to_string(icounter, "99")

    return generate_output()