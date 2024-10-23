from functions.additional_functions import *
import decimal
from datetime import date
from models import Reservation, Res_line, Guest

def group_cobl(case_type:int, ci_date:date):
    mainres_list_list = []
    reservation = res_line = guest = None

    mainres_list = None

    mainres_list_list, Mainres_list = create_model("Mainres_list", {"resnr":int, "gastnr":int, "name":str, "zimanz":int, "arr":int, "co":int, "res":int, "dep":int, "groupname":str, "res_address":str, "res_city":str, "res_bemerk":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_list_list, reservation, res_line, guest
        nonlocal case_type, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_list
        return {"mainres-list": mainres_list_list}

    def update_mainres():

        nonlocal mainres_list_list, reservation, res_line, guest
        nonlocal case_type, ci_date


        nonlocal mainres_list
        nonlocal mainres_list_list


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

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.grpflag)).order_by(Reservation.resnr).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & (Res_line.abreise == ci_date)).first()

            if res_line:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnr)).first()
                mainres_list = Mainres_list()
                mainres_list_list.append(mainres_list)

                mainres_list.gastnr = reservation.gastnr
                mainres_list.name = reservation.name
                mainres_list.resnr = reservation.resnr
                mainres_list.groupname = reservation.groupname
                mainres_list.res_address = guest.adresse1
                mainres_list.res_city = guest.wohnort + " " + guest.plz
                mainres_list.res_bemerk = reservation.bemerk


                update_mainres()

    return generate_output()