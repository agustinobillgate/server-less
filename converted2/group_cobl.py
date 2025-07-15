#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Reservation

def group_cobl(case_type:int, ci_date:date):

    prepare_cache ([Res_line, Guest, Reservation])

    mainres_list_data = []
    res_line = guest = reservation = None

    mainres_list = None

    mainres_list_data, Mainres_list = create_model("Mainres_list", {"resnr":int, "gastnr":int, "name":string, "zimanz":int, "arr":int, "co":int, "res":int, "dep":int, "groupname":string, "res_address":string, "res_city":string, "res_bemerk":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_list_data, res_line, guest, reservation
        nonlocal case_type, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_data

        return {"mainres-list": mainres_list_data}

    def update_mainres():

        nonlocal mainres_list_data, res_line, guest, reservation
        nonlocal case_type, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_data


        mainres_list.zimanz = 0
        mainres_list.co = 0
        mainres_list.res = 0
        mainres_list.dep = 0
        mainres_list.arr = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == mainres_list.resnr) & ((Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12))).order_by(Res_line._recid).all():
            mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if res_line.active_flag == 0:
                mainres_list.arr = mainres_list.arr + 1

            if res_line.active_flag == 1:

                if res_line.abreise > ci_date:
                    mainres_list.res = mainres_list.res + 1
                else:
                    mainres_list.dep = mainres_list.dep + 1

            if res_line.active_flag == 2:
                mainres_list.co = mainres_list.co + 1


    if case_type == 1:

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        guest = Guest()
        for reservation.gastnr, reservation.name, reservation.resnr, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zimmeranz, res_line.active_flag, res_line.abreise, res_line._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Reservation.gastnr, Reservation.name, Reservation.resnr, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zimmeranz, Res_line.active_flag, Res_line.abreise, Res_line._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.abreise == ci_date)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                 (Reservation.grpflag)).order_by(Reservation.resnr).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            mainres_list = Mainres_list()
            mainres_list_data.append(mainres_list)

            mainres_list.gastnr = reservation.gastnr
            mainres_list.name = reservation.name
            mainres_list.resnr = reservation.resnr
            mainres_list.groupname = reservation.groupname
            mainres_list.res_address = guest.adresse1
            mainres_list.res_city = guest.wohnort + " " + guest.plz
            mainres_list.res_bemerk = reservation.bemerk


            update_mainres()

    return generate_output()