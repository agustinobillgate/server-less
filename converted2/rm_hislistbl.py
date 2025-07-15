#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, History

def rm_hislistbl(t_date:date, f_date:date, zinr:string):

    prepare_cache ([History])

    t_hislist_data = []
    guest = history = None

    t_hislist = None

    t_hislist_data, T_hislist = create_model("T_hislist", {"gastinfo":string, "ankunft":date, "abreise":date, "abreisezeit":string, "zikateg":string, "zinr":string, "zipreis":Decimal, "zimmeranz":int, "arrangement":string, "resnr":int, "gesamtumsatz":Decimal, "zahlungsart":int, "segmentcode":int, "bemerk":string, "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hislist_data, guest, history
        nonlocal t_date, f_date, zinr


        nonlocal t_hislist
        nonlocal t_hislist_data

        return {"t-hislist": t_hislist_data}

    history_obj_list = {}
    for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr)).filter(
             (History.betriebsnr <= 1) & (not_ (History.ankunft > t_date)) & (not_ (History.abreise <= f_date)) & (History.zinr == (zinr).lower()) & (History.gastnr > 0)).order_by(History.gastinfo).all():
        if history_obj_list.get(history._recid):
            continue
        else:
            history_obj_list[history._recid] = True


        t_hislist = T_hislist()
        t_hislist_data.append(t_hislist)

        t_hislist.gastinfo = history.gastinfo
        t_hislist.ankunft = history.ankunft
        t_hislist.abreise = history.abreise
        t_hislist.abreisezeit = history.abreisezeit
        t_hislist.zikateg = history.zikateg
        t_hislist.zinr = history.zinr
        t_hislist.zipreis =  to_decimal(history.zipreis)
        t_hislist.zimmeranz = history.zimmeranz
        t_hislist.arrangement = history.arrangement
        t_hislist.resnr = history.resnr
        t_hislist.gesamtumsatz =  to_decimal(history.gesamtumsatz)
        t_hislist.zahlungsart = history.zahlungsart
        t_hislist.segmentcode = history.segmentcode
        t_hislist.bemerk = history.bemerk

    return generate_output()