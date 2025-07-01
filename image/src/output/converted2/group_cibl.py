#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Res_line, Guest

def group_cibl(pvilanguage:int, ci_date:date):

    prepare_cache ([Reservation, Res_line, Guest])

    mainres_list_list = []
    lvcarea:string = "group-ci"
    reservation = res_line = guest = None

    mainres_list = None

    mainres_list_list, Mainres_list = create_model("Mainres_list", {"resnr":int, "gastnr":int, "name":string, "zimanz":int, "ci":int, "co":int, "arr":int, "abreise":date, "segm":int, "deposit":Decimal, "until":date, "paid":Decimal, "groupname":string, "res_address":string, "res_city":string, "res_bemerk":string}, {"abreise": date_mdy(1, 1, 1998), "res_address": "", "res_city": "", "res_bemerk": ""})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_list_list, lvcarea, reservation, res_line, guest
        nonlocal pvilanguage, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_list

        return {"mainres-list": mainres_list_list}

    def fill_mainres():

        nonlocal mainres_list_list, lvcarea, reservation, res_line, guest
        nonlocal pvilanguage, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_list

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.activeflag == 0) & (Reservation.grpflag) & (Reservation.name > "") & (Reservation.gastnr > 0)).order_by(Reservation.name, Reservation.resnr).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == ci_date)).first()

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                mainres_list = Mainres_list()
                mainres_list_list.append(mainres_list)

                mainres_list.gastnr = reservation.gastnr
                mainres_list.name = reservation.name
                mainres_list.resnr = reservation.resnr
                mainres_list.deposit =  to_decimal(reservation.depositgef)
                mainres_list.until = reservation.limitdate
                mainres_list.paid =  to_decimal(reservation.depositbez) + to_decimal(reservation.depositbez2)
                mainres_list.segm = reservation.segmentcode
                mainres_list.groupname = reservation.groupname
                mainres_list.res_address = guest.adresse1
                mainres_list.res_city = guest.wohnort + " " + guest.plz


                update_mainres()


    def update_mainres():

        nonlocal mainres_list_list, lvcarea, reservation, res_line, guest
        nonlocal pvilanguage, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_list


        mainres_list.abreise = date_mdy(1, 1, 1998)
        mainres_list.zimanz = 0
        mainres_list.ci = 0
        mainres_list.co = 0
        mainres_list.arr = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & (Res_line.grpflag) & (Res_line.ankunft == ci_date)).order_by(Res_line._recid).all():

            if res_line.resstatus != 9 and res_line.resstatus != 10 and res_line.resstatus != 12:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

                if res_line.active_flag == 1:
                    mainres_list.ci = mainres_list.ci + 1

                if res_line.active_flag == 2:
                    mainres_list.co = mainres_list.co + 1

                if res_line.active_flag == 0 and res_line.ankunft == ci_date:
                    mainres_list.arr = mainres_list.arr + res_line.zimmeranz

                if mainres_list.abreise < res_line.abreise:
                    mainres_list.abreise = res_line.abreise

    fill_mainres()

    return generate_output()