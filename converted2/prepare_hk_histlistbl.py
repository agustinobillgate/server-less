#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, History

def prepare_hk_histlistbl(sorttype:int, f_date:date, t_date:date, disptype:int):

    prepare_cache ([History])

    hk_histlist_data = []
    guest = history = None

    hk_histlist = None

    hk_histlist_data, Hk_histlist = create_model("Hk_histlist", {"gastinfo":string, "zinr":string, "zikateg":string, "ankunft":date, "abreise":date, "abreisezeit":string, "arrangement":string, "zi_wechsel":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hk_histlist_data, guest, history
        nonlocal sorttype, f_date, t_date, disptype


        nonlocal hk_histlist
        nonlocal hk_histlist_data

        return {"hk-histlist": hk_histlist_data}

    if sorttype == 0:

        history_obj_list = {}
        for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr) & (Guest.karteityp == disptype)).filter(
                 (History.betriebsnr == 0) & (History.ankunft >= f_date) & (History.ankunft <= t_date) & (History.gastnr > 0)).order_by(History.gastinfo).all():
            if history_obj_list.get(history._recid):
                continue
            else:
                history_obj_list[history._recid] = True


            hk_histlist = Hk_histlist()
            hk_histlist_data.append(hk_histlist)

            hk_histlist.gastinfo = history.gastinfo
            hk_histlist.zinr = history.zinr
            hk_histlist.zikateg = history.zikateg
            hk_histlist.ankunft = history.ankunft
            hk_histlist.abreise = history.abreise
            hk_histlist.abreisezeit = history.abreisezeit
            hk_histlist.arrangement = history.arrangement
            hk_histlist.zi_wechsel = history.zi_wechsel

    elif sorttype == 1:

        history_obj_list = {}
        for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr) & (Guest.karteityp == disptype)).filter(
                 (History.betriebsnr == 0) & (History.abreise >= f_date) & (History.abreise <= t_date) & (History.gastnr > 0)).order_by(History.gastinfo).all():
            if history_obj_list.get(history._recid):
                continue
            else:
                history_obj_list[history._recid] = True


            hk_histlist = Hk_histlist()
            hk_histlist_data.append(hk_histlist)

            hk_histlist.gastinfo = history.gastinfo
            hk_histlist.zinr = history.zinr
            hk_histlist.zikateg = history.zikateg
            hk_histlist.ankunft = history.ankunft
            hk_histlist.abreise = history.abreise
            hk_histlist.abreisezeit = history.abreisezeit
            hk_histlist.arrangement = history.arrangement
            hk_histlist.zi_wechsel = history.zi_wechsel

    return generate_output()