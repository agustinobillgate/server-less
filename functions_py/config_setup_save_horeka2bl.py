#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 27/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel, Queasy

def config_setup_save_horeka2bl(userinit:string, custid:string, username:string, password:string, url_push:string, url_notif:string, storage:int, push_dml:bool, art_deposit:int, api_key:string, supplier:string, coa_apdeposit:string, coa_apclearence:string, artikel_apclearence:int, usr_id:int, url_pr:string):

    prepare_cache ([Queasy])

    msg_str = ""
    ct:string = ""
    l_artikel = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, ct, l_artikel, queasy
        nonlocal userinit, custid, username, password, url_push, url_notif, storage, push_dml, art_deposit, api_key, supplier, coa_apdeposit, coa_apclearence, artikel_apclearence, usr_id, url_pr

        return {"msg_str": msg_str}


    l_artikel = db_session.query(L_artikel).filter(
             (L_artikel.bestellt) & (not_(matches(L_artikel.bezeich,"(Don't use)*"))) & (not_(matches(L_artikel.bezeich,"(Dont use)*"))) & (not_(matches(L_artikel.bezeich,"(Don't used)*"))) & (not_(matches(L_artikel.bezeich,"(Dont used)*"))) & (not_(matches(L_artikel.bezeich,"(Don't Use )*"))) & (not_(matches(L_artikel.bezeich,"*(Don't Use)"))) & (((L_artikel.traubensorte == " ") | (L_artikel.masseinheit == " ")) | ((L_artikel.traubensorte == None) | (L_artikel.masseinheit == None)))).first()

    if l_artikel:
        msg_str = "There are delivery units/mess units still empty. Please check again."

        return generate_output()
    ct = "$custid$" + custid + ";" + "$username$" + username + ";" + "$password$" + password + ";" + "$urlpush$" + url_push + ";" + "$urlnotif$" + url_notif + ";" + "$storage$" + to_string(storage) + ";" + "$pushdml$" + to_string(push_dml) + ";" + "$artdeposit$" + to_string(art_deposit) + ";" + "$apikey$" + api_key + ";" + "$supplier$" + supplier + ";" + "$apdeposit$" + coa_apdeposit + ";" + "$apclearence$" + coa_apclearence + ";" + "$artikelap$" + to_string(artikel_apclearence) + ";" + "$userID$" + to_string(usr_id) + ";" + "$urlpr$" + url_pr

    # queasy = get_cache (Queasy, {"key": [(eq, 253)]})
    queasy = db_session.query(Queasy).filter(Queasy.key == 253).with_for_update().first()

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