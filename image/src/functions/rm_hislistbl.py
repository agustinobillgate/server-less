from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, History

def rm_hislistbl(t_date:date, f_date:date, zinr:str):
    t_hislist_list = []
    guest = history = None

    t_hislist = None

    t_hislist_list, T_hislist = create_model("T_hislist", {"gastinfo":str, "ankunft":date, "abreise":date, "abreisezeit":str, "zikateg":str, "zinr":str, "zipreis":decimal, "zimmeranz":int, "arrangement":str, "resnr":int, "gesamtumsatz":decimal, "zahlungsart":int, "segmentcode":int, "bemerk":str, "betriebsnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hislist_list, guest, history


        nonlocal t_hislist
        nonlocal t_hislist_list
        return {"t-hislist": t_hislist_list}

    history_obj_list = []
    for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
            (History.betriebsnr <= 1) &  (not (History.ankunft > t_date)) &  (not (History.abreise <= f_date)) &  (func.lower(History.(zinr).lower()) == (zinr).lower()) &  (History.gastnr > 0)).all():
        if history._recid in history_obj_list:
            continue
        else:
            history_obj_list.append(history._recid)


        t_hislist = T_hislist()
        t_hislist_list.append(t_hislist)

        t_hislist.gastinfo = history.gastinfo
        t_hislist.ankunft = history.ankunft
        t_hislist.abreise = history.abreise
        t_hislist.abreisezeit = history.abreisezeit
        t_hislist.zikateg = history.zikateg
        t_hislist.zinr = history.zinr
        t_hislist.zipreis = history.zipreis
        t_hislist.zimmeranz = history.zimmeranz
        t_hislist.arrangement = history.arrangement
        t_hislist.resnr = history.resnr
        t_hislist.gesamtumsatz = history.gesamtumsatz
        t_hislist.zahlungsart = history.zahlungsart
        t_hislist.segmentcode = history.segmentcode
        t_hislist.bemerk = history.bemerk

    return generate_output()