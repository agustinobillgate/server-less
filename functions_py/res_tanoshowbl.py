#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/8/2025
# search filter name, perlu tambahan char \ufff
#------------------------------------------
from functions.additional_functions import *
from sqlalchemy import func, and_
from decimal import Decimal
from datetime import date
from models import Guest, Zimkateg, Res_line

def res_tanoshowbl(fdate:date, sorttype:int, fname:string, tname:string):

    prepare_cache ([Guest, Res_line])

    outlist_data = []
    t_mnite:int = 0
    t_ynite:int = 0
    t_mtu:Decimal = to_decimal("0.0")
    t_ytu:Decimal = to_decimal("0.0")
    gastnr:int = 0
    rmnite:int = 0
    bdate:date = None
    tmpint:int = 0
    guest = zimkateg = res_line = None

    outlist = None

    outlist_data, Outlist = create_model("Outlist", {"resnr":int, "name":string, "mnite":int, "pmnite":int, "ynite":int, "pynite":int, "mtu":Decimal, "pmtu":int, "ytu":Decimal, "pytu":int, "wohnort":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outlist_data, t_mnite, t_ynite, t_mtu, t_ytu, gastnr, rmnite, bdate, tmpint, guest, zimkateg, res_line
        nonlocal fdate, sorttype, fname, tname


        nonlocal outlist
        nonlocal outlist_data

        return {"outlist": outlist_data}


    bdate = date_mdy(1, 1, get_year(fdate))
    t_mnite = 0
    t_mtu =  to_decimal("0")
    t_ynite = 0
    t_ytu =  to_decimal("0")

    if sorttype == 1:

        res_line_obj_list = {}
        for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 2)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.active_flag == 2) & (Res_line.resstatus == 10) & (Res_line.ankunft >= bdate) & (Res_line.ankunft <= fdate) & (Res_line.resname >= (fname).lower()) & (Res_line.resname <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resname, Res_line.ankunft, Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            outlist = query(outlist_data, filters=(lambda outlist: outlist.resnr == res_line.resnr), first=True)

            if not outlist:
                outlist = Outlist()
                outlist_data.append(outlist)

                outlist.resnr = res_line.resnr
                outlist.name = guest.name + ", " + guest.anredefirma
                outlist.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                gastnr = res_line.gastnr
            tmpint = (res_line.abreise - res_line.ankunft).days
            rmnite = tmpint * res_line.zimmeranz

            if get_month(res_line.ankunft) == get_month(fdate):
                outlist.mnite = outlist.mnite + rmnite
                outlist.mtu =  to_decimal(outlist.mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                t_mnite = t_mnite + rmnite
                t_mtu =  to_decimal(t_mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
            outlist.ynite = outlist.ynite + rmnite
            outlist.ytu =  to_decimal(outlist.ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
            t_ynite = t_ynite + rmnite
            t_ytu =  to_decimal(t_ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)

    else:
        res_line_obj_list = {}
        # for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
        #          (Res_line.active_flag == 2) & (Res_line.resstatus == 10) & (Res_line.ankunft >= bdate) & (Res_line.ankunft <= fdate) & (Res_line.resname >= (fname).lower()) & (Res_line.resname <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resname, Res_line.ankunft, Res_line.name).all():

        for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 1)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 2) & (Res_line.resstatus == 10) & 
                (Res_line.ankunft >= bdate) & (Res_line.ankunft <= fdate) & 
                # (func.lower(Res_line.resname) >= fname.lower()) & 
                # (func.lower(Res_line.resname) <  tname.lower() + "\uffff") &
                ((Res_line.resname) >= fname) & 
                ((Res_line.resname) <  tname + "\uffff") &
                (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resname, Res_line.ankunft, Res_line.name).all():
            
            # if (res_line.resname.lower() < fname.lower()) & (res_line.resname.lower() > tname.lower()):
            #     continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            outlist = query(outlist_data, filters=(lambda outlist: outlist.resnr == res_line.resnr), first=True)

            if not outlist:
                outlist = Outlist()
                outlist_data.append(outlist)

                outlist.resnr = res_line.resnr
                outlist.name = guest.name + ", " + guest.anredefirma
                outlist.wohnort = guest.wohnort + " " + to_string(guest.plz) + " - " + guest.land
                gastnr = res_line.gastnr
            tmpint = (res_line.abreise - res_line.ankunft).days
            rmnite = tmpint * res_line.zimmeranz

            if get_month(res_line.ankunft) == get_month(fdate):
                outlist.mnite = outlist.mnite + rmnite
                outlist.mtu =  to_decimal(outlist.mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
                t_mnite = t_mnite + rmnite
                t_mtu =  to_decimal(t_mtu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
            outlist.ynite = outlist.ynite + rmnite
            outlist.ytu =  to_decimal(outlist.ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)
            t_ynite = t_ynite + rmnite
            t_ytu =  to_decimal(t_ytu) + to_decimal(rmnite) * to_decimal(res_line.zipreis)


    for outlist in query(outlist_data):

        if t_mnite != 0:
            outlist.pmnite = outlist.mnite / t_mnite * 100

            if t_mtu != 0:
                outlist.pmtu = outlist.mtu / t_mtu * 100

        if t_ynite != 0:
            outlist.pynite = outlist.ynite / t_ynite * 100

            if t_ytu != 0:
                outlist.pytu = outlist.ytu / t_ytu * 100

    return generate_output()