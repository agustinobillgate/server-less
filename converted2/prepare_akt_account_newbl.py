#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Htparam, Zimkateg, Bediener, Reservation

def prepare_akt_account_newbl(userinit:string):

    prepare_cache ([Guest, Htparam, Zimkateg, Bediener, Reservation])

    ci_date = None
    other_time = 0
    mainres_list_data = []
    resline_data = []
    usr_data = []
    res_line = guest = htparam = zimkateg = bediener = reservation = None

    mainres_list = resline = usr = gmember = None

    mainres_list_data, Mainres_list = create_model("Mainres_list", {"resname":string, "gastnr":int, "resnr":int, "actflag":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":Decimal, "until":date, "paid":Decimal, "vesrcode":string, "id1":string, "id2":string, "id2_date":date, "groupname":string, "grpflag":bool, "bemerk":string, "arrival":bool, "resident":bool, "arr_today":bool, "gname":string, "address":string, "city":string}, {"ankunft": date_mdy(1, 1, 2099), "abreise": date_mdy(1, 1, 1998)})
    resline_data, Resline = create_model_like(Res_line, {"kurzbez":string})
    usr_data, Usr = create_model("Usr", {"userinit":string, "username":string})

    Gmember = create_buffer("Gmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, other_time, mainres_list_data, resline_data, usr_data, res_line, guest, htparam, zimkateg, bediener, reservation
        nonlocal userinit
        nonlocal gmember


        nonlocal mainres_list, resline, usr, gmember
        nonlocal mainres_list_data, resline_data, usr_data

        return {"ci_date": ci_date, "other_time": other_time, "mainres-list": mainres_list_data, "resline": resline_data, "usr": usr_data}

    def fill_mainres(fill_code:int):

        nonlocal ci_date, other_time, mainres_list_data, resline_data, usr_data, res_line, guest, htparam, zimkateg, bediener, reservation
        nonlocal userinit
        nonlocal gmember


        nonlocal mainres_list, resline, usr, gmember
        nonlocal mainres_list_data, resline_data, usr_data


        mainres_list_data.clear()

        for guest in db_session.query(Guest).filter(
                 (Guest.gastnr > 0) & (Guest.phonetik3 == (userinit).lower())).order_by(Guest.karteityp, Guest.name).all():

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.gastnr == guest.gastnr) & (Reservation.activeflag == 0)).order_by(Reservation.resnr).all():
                mainres_list = Mainres_list()
                mainres_list_data.append(mainres_list)

                mainres_list.resname = guest.name
                mainres_list.gastnr = guest.gastnr
                mainres_list.resnr = reservation.resnr
                mainres_list.deposit =  to_decimal(reservation.depositgef)
                mainres_list.until = reservation.limitdate
                mainres_list.paid =  to_decimal(reservation.depositbez) + to_decimal(reservation.depositbez2)
                mainres_list.segm = reservation.segmentcode
                mainres_list.groupname = reservation.groupname
                mainres_list.bemerk = reservation.bemerk
                mainres_list.vesrcode = guest.phonetik3
                mainres_list.id1 = reservation.useridanlage
                mainres_list.id2 = reservation.useridmutat
                mainres_list.id2_date = reservation.mutdat
                mainres_list.grpflag = reservation.grpflag
                mainres_list.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                        " " + guest.anrede1
                mainres_list.address = guest.adresse1 + " " + guest.adresse2
                mainres_list.city = guest.land + " " + guest.wohnort + " " + guest.plz


                update_mainres()


    def update_mainres():

        nonlocal ci_date, other_time, mainres_list_data, resline_data, usr_data, res_line, guest, htparam, zimkateg, bediener, reservation
        nonlocal userinit
        nonlocal gmember


        nonlocal mainres_list, resline, usr, gmember
        nonlocal mainres_list_data, resline_data, usr_data

        resline_exist:bool = False
        mainres_list.ankunft = date_mdy(1, 1, 2099)
        mainres_list.abreise = date_mdy(1, 1, 1998)
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == mainres_list.resnr) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            resline_exist = True

            if res_line.resstatus != 11 and res_line.resstatus != 13:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if (resstatus <= 5 or resstatus == 11):
                mainres_list.arrival = True

            if mainres_list.arrival  and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

        if not resline_exist:
            mainres_list_data.remove(mainres_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 297)]})
    other_time = htparam.finteger
    fill_mainres(1)

    for mainres_list in query(mainres_list_data):

        res_line_obj_list = {}
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.resnr == mainres_list.resnr)).order_by(Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            resline = Resline()
            resline_data.append(resline)

            buffer_copy(res_line, resline)
            resline.kurzbez = zimkateg.kurzbez

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        usr = Usr()
        usr_data.append(usr)

        usr.userinit = bediener.userinit
        usr.username = bediener.username

    return generate_output()