from functions.additional_functions import *
import decimal
from models import Queasy

def config_setup_save_horekabl(userinit:str, custid:str, username:str, password:str, url_push:str, url_notif:str, storage:int, push_dml:bool, art_deposit:int, api_key:str, supplier:str, coa_apdeposit:str, coa_apclearence:str, artikel_apclearence:int, usr_id:int):
    ct:str = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ct, queasy


        return {}

    ct = "$custid$" + custid + ";" + "$username$" + username + ";" + "$password$" + password + ";" + "$urlpush$" + url_push + ";" + "$urlnotif$" + url_notif + ";" + "$storage$" + to_string(storage) + ";" + "$pushdml$" + to_string(push_dml) + ";" + "$artdeposit$" + to_string(art_deposit) + ";" + "$apikey$" + api_key + ";" + "$supplier$" + supplier + ";" + "$apdeposit$" + coa_apdeposit + ";" + "$apclearence$" + coa_apclearence + ";" + "$artikelap$" + to_string(artikel_apclearence) + ";" + "$userID$" + to_string(usr_id)

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 253)).first()

    if queasy:

        queasy = db_session.query(Queasy).first()
        queasy.char1 = ct
        queasy.date1 = get_current_date()
        queasy.char2 = userinit

        queasy = db_session.query(Queasy).first()

    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 253
        queasy.char1 = ct
        queasy.date1 = get_current_date()
        queasy.char2 = userinit

    return generate_output()