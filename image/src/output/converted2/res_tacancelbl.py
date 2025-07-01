#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Zimkateg, Res_line

def res_tacancelbl(pvilanguage:int, stattype:int, sorttype:int, fdate:date, fname:string, tname:string):

    prepare_cache ([Guest, Res_line])

    t_mnite = 0
    t_ynite = 0
    t_mtu = to_decimal("0.0")
    t_ytu = to_decimal("0.0")
    res_tacancel_list = []
    lvcarea:string = "res-tacancel"
    tmpint:int = 0
    guest = zimkateg = res_line = None

    res_tacancel = None

    res_tacancel_list, Res_tacancel = create_model("Res_tacancel", {"resnr":int, "name":string, "mnite":int, "pmnite":int, "ynite":int, "pynite":int, "mtu":Decimal, "pmtu":int, "ytu":Decimal, "pytu":int, "wohnort":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mnite, t_ynite, t_mtu, t_ytu, res_tacancel_list, lvcarea, tmpint, guest, zimkateg, res_line
        nonlocal pvilanguage, stattype, sorttype, fdate, fname, tname


        nonlocal res_tacancel
        nonlocal res_tacancel_list

        return {"t_mnite": t_mnite, "t_ynite": t_ynite, "t_mtu": t_mtu, "t_ytu": t_ytu, "res-tacancel": res_tacancel_list}

    def disp_noshow():

        nonlocal t_mnite, t_ynite, t_mtu, t_ytu, res_tacancel_list, lvcarea, tmpint, guest, zimkateg, res_line
        nonlocal pvilanguage, stattype, sorttype, fdate, fname, tname


        nonlocal res_tacancel
        nonlocal res_tacancel_list

        gastnr:int = 0
        rmnite:int = 0
        bdate:date = None
        res_tacancel_list.clear()
        bdate = date_mdy(1, 1, get_year(fdate))
        t_mnite = 0
        t_mtu =  to_decimal("0")
        t_ynite = 0
        t_ytu =  to_decimal("0")

        if sorttype == 1:

            res_line_obj_list = {}
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 2)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 2) & (Res_line.resstatus == 9) & (Res_line.ankunft >= bdate) & (Res_line.ankunft <= fdate) & (Res_line.resname >= (fname).lower()) & (Res_line.resname <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resname, Res_line.ankunft, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel: res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                tmpint = (res_line.abreise - res_line.ankunft).days
                rmnite = tmpint * res_line.zimmeranz

                if get_month(res_line.ankunft) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu =  to_decimal(res_tacancel.mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                    t_mnite = t_mnite + rmnite
                    t_mtu =  to_decimal(t_mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu =  to_decimal(res_tacancel.ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                t_ynite = t_ynite + rmnite
                t_ytu =  to_decimal(t_ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)

        else:

            res_line_obj_list = {}
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 2) & (Res_line.resstatus == 9) & (Res_line.ankunft >= bdate) & (Res_line.ankunft <= fdate) & (Res_line.resname >= (fname).lower()) & (Res_line.resname <= (tname).lower())).order_by(Res_line.resname, Res_line.ankunft, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel: res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                tmpint = (res_line.abreise - res_line.ankunft).days
                rmnite = tmpint * res_line.zimmeranz

                if get_month(res_line.ankunft) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu =  to_decimal(res_tacancel.mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                    t_mnite = t_mnite + rmnite
                    t_mtu =  to_decimal(t_mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu =  to_decimal(res_tacancel.ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                t_ynite = t_ynite + rmnite
                t_ytu =  to_decimal(t_ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)


        for res_tacancel in query(res_tacancel_list):

            if t_mnite != 0:
                res_tacancel.pmnite = res_tacancel.mnite / t_mnite * 100
                res_tacancel.pmtu = res_tacancel.mtu / t_mtu * 100

            if t_ynite != 0:
                res_tacancel.pynite = res_tacancel.ynite / t_ynite * 100
                res_tacancel.pytu = res_tacancel.ytu / t_ytu * 100


    def disp_noshow1():

        nonlocal t_mnite, t_ynite, t_mtu, t_ytu, res_tacancel_list, lvcarea, tmpint, guest, zimkateg, res_line
        nonlocal pvilanguage, stattype, sorttype, fdate, fname, tname


        nonlocal res_tacancel
        nonlocal res_tacancel_list

        gastnr:int = 0
        rmnite:int = 0
        bdate:date = None
        res_tacancel_list.clear()
        bdate = date_mdy(1, 1, get_year(fdate))
        t_mnite = 0
        t_mtu =  to_decimal("0")
        t_ynite = 0
        t_ytu =  to_decimal("0")

        if sorttype == 1:

            res_line_obj_list = {}
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 2)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 2) & (Res_line.resstatus == 9) & (Res_line.cancelled >= bdate) & (Res_line.cancelled <= fdate) & (Res_line.resname >= (fname).lower()) & (Res_line.resname <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resname, Res_line.cancelled, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel: res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                tmpint = (res_line.abreise - res_line.ankunft).days
                rmnite = tmpint * res_line.zimmeranz

                if get_month(res_line.cancelled) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu =  to_decimal(res_tacancel.mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                    t_mnite = t_mnite + rmnite
                    t_mtu =  to_decimal(t_mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu =  to_decimal(res_tacancel.ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                t_ynite = t_ynite + rmnite
                t_ytu =  to_decimal(t_ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)

        else:

            res_line_obj_list = {}
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 2) & (Res_line.resstatus == 9) & (Res_line.cancelled >= bdate) & (Res_line.cancelled <= fdate) & (Res_line.resname >= (fname).lower()) & (Res_line.resname <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resname, Res_line.cancelled, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                res_tacancel = query(res_tacancel_list, filters=(lambda res_tacancel: res_tacancel.resnr == res_line.resnr), first=True)

                if not res_tacancel:
                    res_tacancel = Res_tacancel()
                    res_tacancel_list.append(res_tacancel)

                    res_tacancel.resnr = res_line.resnr
                    res_tacancel.name = guest.name + ", " + guest.anredefirma
                    res_tacancel.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                    gastnr = res_line.gastnr
                tmpint = (res_line.abreise - res_line.ankunft).days
                rmnite = tmpint * res_line.zimmeranz

                if get_month(res_line.cancelled) == get_month(fdate):
                    res_tacancel.mnite = res_tacancel.mnite + rmnite
                    res_tacancel.mtu =  to_decimal(res_tacancel.mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                    t_mnite = t_mnite + rmnite
                    t_mtu =  to_decimal(t_mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                res_tacancel.ynite = res_tacancel.ynite + rmnite
                res_tacancel.ytu =  to_decimal(res_tacancel.ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                t_ynite = t_ynite + rmnite
                t_ytu =  to_decimal(t_ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)


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