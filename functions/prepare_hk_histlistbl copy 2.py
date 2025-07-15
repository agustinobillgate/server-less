from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, History

def prepare_hk_histlistbl(sorttype:int, f_date:date, t_date:date, disptype:int):
    hk_histlist_list = []
    guest = history = None

    hk_histlist = None

    hk_histlist_list, Hk_histlist = create_model("Hk_histlist", {"gastinfo":str, "zinr":str, "zikateg":str, "ankunft":date, "abreise":date, "abreisezeit":str, "arrangement":str, "zi_wechsel":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hk_histlist_list, guest, history
        nonlocal sorttype, f_date, t_date, disptype


        nonlocal hk_histlist
        nonlocal hk_histlist_list
        return {"hk-histlist": hk_histlist_list}

    if sorttype == 0:

        history_obj_list = []
        for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr) &  (Guest.karteityp == disptype)).filter(
                (History.betriebsnr == 0) &  (History.ankunft >= f_date) &  (History.ankunft <= t_date) &  (History.gastnr > 0)).order_by(History.gastinfo).all():
            if history._recid in history_obj_list:
                continue
            else:
                history_obj_list.append(history._recid)


            hk_histlist = Hk_histlist()
            hk_histlist_list.append(hk_histlist)

            hk_histlist.gastinfo = history.gastinfo
            hk_histlist.zinr = history.zinr
            hk_histlist.zikateg = history.zikateg
            hk_histlist.ankunft = history.ankunft
            hk_histlist.abreise = history.abreise
            hk_histlist.abreisezeit = history.abreisezeit
            hk_histlist.arrangement = history.arrangement
            hk_histlist.zi_wechsel = history.zi_wechsel

    elif sorttype == 1:

        history_obj_list = []
        for history, guest in db_session.query(History, Guest).join(Guest,(Guest.gastnr == History.gastnr) &  (Guest.karteityp == disptype)).filter(
                (History.betriebsnr == 0) &  (History.abreise >= f_date) &  (History.abreise <= t_date) &  (History.gastnr > 0)).order_by(History.gastinfo).all():
            if history._recid in history_obj_list:
                continue
            else:
                history_obj_list.append(history._recid)


            hk_histlist = Hk_histlist()
            hk_histlist_list.append(hk_histlist)

            hk_histlist.gastinfo = history.gastinfo
            hk_histlist.zinr = history.zinr
            hk_histlist.zikateg = history.zikateg
            hk_histlist.ankunft = history.ankunft
            hk_histlist.abreise = history.abreise
            hk_histlist.abreisezeit = history.abreisezeit
            hk_histlist.arrangement = history.arrangement
            hk_histlist.zi_wechsel = history.zi_wechsel

    return generate_output()