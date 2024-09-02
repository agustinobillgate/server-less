from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Zimkateg, Res_line

def res_tacancelbl(pvilanguage:int, stattype:int, sorttype:int, fdate:date, fname:str, tname:str):
    t_mnite = 0
    t_ynite = 0
    t_mtu = 0
    t_ytu = 0
    res_tacancel_list = []
    lvcarea:str = "res_tacancel"
    guest = zimkateg = res_line = None

    res_tacancel = None

    res_tacancel_list, Res_tacancel = create_model("Res_tacancel", {"resnr":int, "name":str, "mnite":int, "pmnite":int, "ynite":int, "pynite":int, "mtu":decimal, "pmtu":int, "ytu":decimal, "pytu":int, "wohnort":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mnite, t_ynite, t_mtu, t_ytu, res_tacancel_list, lvcarea, guest, zimkateg, res_line


        nonlocal res_tacancel
        nonlocal res_tacancel_list
        return {"t_mnite": t_mnite, "t_ynite": t_ynite, "t_mtu": t_mtu, "t_ytu": t_ytu, "res-tacancel": res_tacancel_list}

    def disp_noshow():

        nonlocal t_mnite, t_ynite, t_mtu, t_ytu, res_tacancel_list, lvcarea, guest, zimkateg, res_line


        nonlocal res_tacancel
        nonlocal res_tacancel_list

        gastnr:int = 0
        rmnite:int = 0
        bdate:date = None
        res_tacancel_list.clear()
        bdate = date_mdy(1, 1, get_year(fdate))
        t_mnite = 0
        t_mtu = 0
        t_ynite = 0
        t_ytu = 0

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == 2)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 2) &  (Res_line.resstatus == 9) &  (Res_line.ankunft >= bdate) &  (Res_line.ankunft <= fdate) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel :res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                rmnite = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz

                if get_month(res_line.ankunft) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu = res_tacancel.mtu + rmnite * res_line.zipreis
                    t_mnite = t_mnite + rmnite
                    t_mtu = t_mtu + rmnite * res_line.zipreis
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu = res_tacancel.ytu + rmnite * res_line.zipreis
                t_ynite = t_ynite + rmnite
                t_ytu = t_ytu + rmnite * res_line.zipreis

        else:

            res_line_obj_list = []
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 2) &  (Res_line.resstatus == 9) &  (Res_line.ankunft >= bdate) &  (Res_line.ankunft <= fdate) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) <= (tname).lower())).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel :res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                rmnite = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz

                if get_month(res_line.ankunft) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu = res_tacancel.mtu + rmnite * res_line.zipreis
                    t_mnite = t_mnite + rmnite
                    t_mtu = t_mtu + rmnite * res_line.zipreis
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu = res_tacancel.ytu + rmnite * res_line.zipreis
                t_ynite = t_ynite + rmnite
                t_ytu = t_ytu + rmnite * res_line.zipreis


        for res_tacancel in query(res_tacancel_list):

            if t_mnite != 0:
                res_tacancel.pmnite = res_tacancel.mnite / t_mnite * 100
                res_tacancel.pmtu = res_tacancel.mtu / t_mtu * 100

            if t_ynite != 0:
                res_tacancel.pynite = res_tacancel.ynite / t_ynite * 100
                res_tacancel.pytu = res_tacancel.ytu / t_ytu * 100

    def disp_noshow1():

        nonlocal t_mnite, t_ynite, t_mtu, t_ytu, res_tacancel_list, lvcarea, guest, zimkateg, res_line


        nonlocal res_tacancel
        nonlocal res_tacancel_list

        gastnr:int = 0
        rmnite:int = 0
        bdate:date = None
        res_tacancel_list.clear()
        bdate = date_mdy(1, 1, get_year(fdate))
        t_mnite = 0
        t_mtu = 0
        t_ynite = 0
        t_ytu = 0

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == 2)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 2) &  (Res_line.resstatus == 9) &  (Res_line.cancelled >= bdate) &  (Res_line.cancelled <= fdate) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel :res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                rmnite = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz

                if get_month(res_line.cancelled) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu = res_tacancel.mtu + rmnite * res_line.zipreis
                    t_mnite = t_mnite + rmnite
                    t_mtu = t_mtu + rmnite * res_line.zipreis
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu = res_tacancel.ytu + rmnite * res_line.zipreis
                t_ynite = t_ynite + rmnite
                t_ytu = t_ytu + rmnite * res_line.zipreis

        else:

            res_line_obj_list = []
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 2) &  (Res_line.resstatus == 9) &  (Res_line.cancelled >= bdate) &  (Res_line.cancelled <= fdate) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel :res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                rmnite = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz

                if get_month(res_line.cancelled) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu = res_tacancel.mtu + rmnite * res_line.zipreis
                    t_mnite = t_mnite + rmnite
                    t_mtu = t_mtu + rmnite * res_line.zipreis
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu = res_tacancel.ytu + rmnite * res_line.zipreis
                t_ynite = t_ynite + rmnite
                t_ytu = t_ytu + rmnite * res_line.zipreis


        for res_tacancel in query(res_tacancel_list):

            if t_mnite != 0:
                res_tacancel.pmnite = res_tacancel.mnite / t_mnite * 100
                res_tacancel.pmtu = res_tacancel.mtu / t_mtu * 100

            if t_ynite != 0:
                res_tacancel.pynite = res_tacancel.ynite / t_ynite * 100
                res_tacancel.pytu = res_tacancel.ytu / t_ytu * 100

    if stattype == 1:
        disp_noshow()
    else:
        disp_noshow1()

    return generate_output()