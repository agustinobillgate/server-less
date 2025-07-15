#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def config_setup_save_horekabl(userinit:string, custid:string, username:string, password:string, url_push:string, url_notif:string, storage:int, push_dml:bool, art_deposit:int, api_key:string, supplier:string, coa_apdeposit:string, coa_apclearence:string, artikel_apclearence:int, usr_id:int):

    prepare_cache ([Queasy])

    ct:string = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ct, queasy
        nonlocal userinit, custid, username, password, url_push, url_notif, storage, push_dml, art_deposit, api_key, supplier, coa_apdeposit, coa_apclearence, artikel_apclearence, usr_id

        return {}

    ct = "$custid$" + custid + ";" + "$username$" + username + ";" + "$password$" + password + ";" + "$urlpush$" + url_push + ";" + "$urlnotif$" + url_notif + ";" + "$storage$" + to_string(storage) + ";" + "$pushdml$" + to_string(push_dml) + ";" + "$artdeposit$" + to_string(art_deposit) + ";" + "$apikey$" + api_key + ";" + "$supplier$" + supplier + ";" + "$apdeposit$" + coa_apdeposit + ";" + "$apclearence$" + coa_apclearence + ";" + "$artikelap$" + to_string(artikel_apclearence) + ";" + "$userID$" + to_string(usr_id)

    queasy = get_cache (Queasy, {"key": [(eq, 253)]})

    if queasy:
        pass
        queasy.char1 = ct
        queasy.date1 = get_current_date()
        queasy.char2 = userinit


        pass
        pass
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 253
        queasy.char1 = ct
        queasy.date1 = get_current_date()
        queasy.char2 = userinit

    return generate_output()