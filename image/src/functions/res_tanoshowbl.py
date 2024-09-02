from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Zimkateg, Res_line

def res_tanoshowbl(fdate:date, sorttype:int, fname:str, tname:str):
    outlist_list = []
    t_mnite:int = 0
    t_ynite:int = 0
    t_mtu:decimal = 0
    t_ytu:decimal = 0
    gastnr:int = 0
    rmnite:int = 0
    bdate:date = None
    guest = zimkateg = res_line = None

    outlist = None

    outlist_list, Outlist = create_model("Outlist", {"resnr":int, "name":str, "mnite":int, "pmnite":int, "ynite":int, "pynite":int, "mtu":decimal, "pmtu":int, "ytu":decimal, "pytu":int, "wohnort":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal outlist_list, t_mnite, t_ynite, t_mtu, t_ytu, gastnr, rmnite, bdate, guest, zimkateg, res_line


        nonlocal outlist
        nonlocal outlist_list
        return {"outlist": outlist_list}


    bdate = date_mdy(1, 1, get_year(fdate))
    t_mnite = 0
    t_mtu = 0
    t_ynite = 0
    t_ytu = 0

    if sorttype == 1:

        res_line_obj_list = []
        for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == 2)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 2) &  (Res_line.resstatus == 10) &  (Res_line.ankunft >= bdate) &  (Res_line.ankunft <= fdate) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            outlist = query(outlist_list, filters=(lambda outlist :outlist.resnr == res_line.resnr), first=True)

            if not outlist:
                outlist = Outlist()
                outlist_list.append(outlist)

                outlist.resnr = res_line.resnr
                outlist.name = guest.name + ", " + guest.anredefirma
                outlist.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                gastnr = res_line.gastnr
            rmnite = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz

            if get_month(res_line.ankunft) == get_month(fdate):
                outlist.mnite = outlist.mnite + rmnite
                outlist.mtu = outlist.mtu + rmnite * res_line.zipreis
                t_mnite = t_mnite + rmnite
                t_mtu = t_mtu + rmnite * res_line.zipreis
            outlist.ynite = outlist.ynite + rmnite
            outlist.ytu = outlist.ytu + rmnite * res_line.zipreis
            t_ynite = t_ynite + rmnite
            t_ytu = t_ytu + rmnite * res_line.zipreis

    else:

        res_line_obj_list = []
        for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 2) &  (Res_line.resstatus == 10) &  (Res_line.ankunft >= bdate) &  (Res_line.ankunft <= fdate) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            outlist = query(outlist_list, filters=(lambda outlist :outlist.resnr == res_line.resnr), first=True)

            if not outlist:
                outlist = Outlist()
                outlist_list.append(outlist)

                outlist.resnr = res_line.resnr
                outlist.name = guest.name + ", " + guest.anredefirma
                outlist.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                gastnr = res_line.gastnr
            rmnite = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz

            if get_month(res_line.ankunft) == get_month(fdate):
                outlist.mnite = outlist.mnite + rmnite
                outlist.mtu = outlist.mtu + rmnite * res_line.zipreis
                t_mnite = t_mnite + rmnite
                t_mtu = t_mtu + rmnite * res_line.zipreis
            outlist.ynite = outlist.ynite + rmnite
            outlist.ytu = outlist.ytu + rmnite * res_line.zipreis
            t_ynite = t_ynite + rmnite
            t_ytu = t_ytu + rmnite * res_line.zipreis


    for outlist in query(outlist_list):

        if t_mnite != 0:
            outlist.pmnite = outlist.mnite / t_mnite * 100
            outlist.pmtu = outlist.mtu / t_mtu * 100

        if t_ynite != 0:
            outlist.pynite = outlist.ynite / t_ynite * 100
            outlist.pytu = outlist.ytu / t_ytu * 100

    return generate_output()