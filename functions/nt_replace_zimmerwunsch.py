from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line

def nt_replace_zimmerwunsch():
    wifi_pass:str = ""
    new_passkey:str = ""
    zimm:str = ""
    i:int = 1
    iftask:str = ""
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wifi_pass, new_passkey, zimm, i, iftask, res_line

        return {}


    for res_line in db_session.query(Res_line).filter(
             (func.lower(not Res_line.zimmer_wunsch).op("~")(("*;*".lower().replace("*",".*")))) & (Res_line.zimmer_wunsch != "") & (func.lower(Res_line.zimmer_wunsch).op("~")(("*WFPass*".lower().replace("*",".*"))))).order_by(Res_line._recid).all():
        zimm = res_line.zimmer_wunsch
        for i in range(1,len(zimm)  + 1) :

            if substring(zimm, i - 1, 8) == ("$WFPass$").lower() :
                wifi_pass = substring(zimm, i + 8 - 1, 4)
        zimm = replace_str(zimm, wifi_pass, ";")
        for i in range(1,num_entries(zimm, ";") - 1 + 1) :
            iftask = entry(i - 1, zimm, ";")

            if re.match(r".*\$WFPass\$.*",iftask, re.IGNORECASE) and wifi_pass != "":
                new_passkey = "$WFPass$" + wifi_pass
                zimm = replace_str(zimm, iftask, new_passkey)
                break
        res_line.zimmer_wunsch = zimm

    return generate_output()