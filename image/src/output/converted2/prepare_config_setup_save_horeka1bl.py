#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def prepare_config_setup_save_horeka1bl():

    prepare_cache ([Queasy])

    custid = ""
    username = ""
    password = ""
    url_push = ""
    url_notif = ""
    storage = 0
    push_dml = False
    art_deposit = 0
    api_key = ""
    supplier = ""
    coa_apdeposit = ""
    coa_apclearence = ""
    artikel_apclearence = 0
    usr_id = 0
    url_pr = ""
    tlist_list = []
    loopi:int = 0
    str:string = ""
    queasy = None

    tlist = None

    tlist_list, Tlist = create_model("Tlist", {"datum":date, "depart":int, "approved":bool, "send_horeka":bool, "user_name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal custid, username, password, url_push, url_notif, storage, push_dml, art_deposit, api_key, supplier, coa_apdeposit, coa_apclearence, artikel_apclearence, usr_id, url_pr, tlist_list, loopi, str, queasy


        nonlocal tlist
        nonlocal tlist_list

        return {"custid": custid, "username": username, "password": password, "url_push": url_push, "url_notif": url_notif, "storage": storage, "push_dml": push_dml, "art_deposit": art_deposit, "api_key": api_key, "supplier": supplier, "coa_apdeposit": coa_apdeposit, "coa_apclearence": coa_apclearence, "artikel_apclearence": artikel_apclearence, "usr_id": usr_id, "url_pr": url_pr, "tlist": tlist_list}

    queasy = get_cache (Queasy, {"key": [(eq, 253)]})

    if queasy:
        for loopi in range(1,num_entries(queasy.char1, ";")  + 1) :
            str = entry(loopi - 1, queasy.char1, ";")

            if substring(str, 0, 8) == ("$custid$").lower() :
                custid = substring(str, 8)

            elif substring(str, 0, 10) == ("$username$").lower() :
                username = substring(str, 10)

            elif substring(str, 0, 10) == ("$password$").lower() :
                password = substring(str, 10)

            elif substring(str, 0, 9) == ("$urlpush$").lower() :
                url_push = substring(str, 9)

            elif substring(str, 0, 10) == ("$urlnotif$").lower() :
                url_notif = substring(str, 10)

            elif substring(str, 0, 9) == ("$storage$").lower() :
                storage = to_int(substring(str, 9))

            elif substring(str, 0, 9) == ("$pushdml$").lower() :
                push_dml = logical(substring(str, 9))

            elif substring(str, 0, 12) == ("$artdeposit$").lower() :
                art_deposit = to_int(substring(str, 12))

            elif substring(str, 0, 8) == ("$apikey$").lower() :
                api_key = substring(str, 8)

            elif substring(str, 0, 10) == ("$supplier$").lower() :
                supplier = substring(str, 10)

            elif substring(str, 0, 11) == ("$apdeposit$").lower() :
                coa_apdeposit = substring(str, 11)

            elif substring(str, 0, 13) == ("$apclearence$").lower() :
                coa_apclearence = substring(str, 13)

            elif substring(str, 0, 11) == ("$artikelap$").lower() :
                artikel_apclearence = to_int(substring(str, 11))

            elif substring(str, 0, 8) == ("$userID$").lower() :
                usr_id = to_int(substring(str, 8))

            elif substring(str, 0, 7) == ("$urlpr$").lower() :
                url_pr = substring(str, 7)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 254) & (Queasy.logi2) & (Queasy.logi3)).order_by(Queasy._recid).all():
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.datum = queasy.date1
        tlist.depart = queasy.number1
        tlist.approved = queasy.logi1
        tlist.send_horeka = queasy.logi2
        tlist.user_name = queasy.char1

    return generate_output()