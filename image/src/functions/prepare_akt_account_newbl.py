from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Guest, Htparam, Zimkateg, Bediener, Reservation

def prepare_akt_account_newbl(userinit:str):
    ci_date = None
    other_time = 0
    mainres_list_list = []
    resline_list = []
    usr_list = []
    res_line = guest = htparam = zimkateg = bediener = reservation = None

    mainres_list = resline = usr = gmember = None

    mainres_list_list, Mainres_list = create_model("Mainres_list", {"resname":str, "gastnr":int, "resnr":int, "actflag":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":decimal, "until":date, "paid":decimal, "vesrcode":str, "id1":str, "id2":str, "id2_date":date, "groupname":str, "grpflag":bool, "bemerk":str, "arrival":bool, "resident":bool, "arr_today":bool, "gname":str, "address":str, "city":str}, {"ankunft": 01/01/2099, "abreise": 01/01/1998})
    resline_list, Resline = create_model_like(Res_line, {"kurzbez":str})
    usr_list, Usr = create_model("Usr", {"userinit":str, "username":str})

    Gmember = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, other_time, mainres_list_list, resline_list, usr_list, res_line, guest, htparam, zimkateg, bediener, reservation
        nonlocal gmember


        nonlocal mainres_list, resline, usr, gmember
        nonlocal mainres_list_list, resline_list, usr_list
        return {"ci_date": ci_date, "other_time": other_time, "mainres-list": mainres_list_list, "resline": resline_list, "usr": usr_list}

    def fill_mainres(fill_code:int):

        nonlocal ci_date, other_time, mainres_list_list, resline_list, usr_list, res_line, guest, htparam, zimkateg, bediener, reservation
        nonlocal gmember


        nonlocal mainres_list, resline, usr, gmember
        nonlocal mainres_list_list, resline_list, usr_list


        mainres_list_list.clear()

        for guest in db_session.query(Guest).filter(
                (Guest.gastnr > 0) &  (func.lower(Guest.phonetik3) == (userinit).lower())).all():

            for reservation in db_session.query(Reservation).filter(
                    (Reservation.gastnr == guest.gastnr) &  (Reservation.activeflag == 0)).all():
                mainres_list = Mainres_list()
                mainres_list_list.append(mainres_list)

                mainres_list.resname = guest.name
                mainres_list.gastnr = guest.gastnr
                mainres_list.resnr = reservation.resnr
                mainres_list.deposit = reservation.depositgef
                mainres_list.until = reservation.limitdate
                mainres_list.paid = reservation.depositbez + reservation.depositbez2
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

        nonlocal ci_date, other_time, mainres_list_list, resline_list, usr_list, res_line, guest, htparam, zimkateg, bediener, reservation
        nonlocal gmember


        nonlocal mainres_list, resline, usr, gmember
        nonlocal mainres_list_list, resline_list, usr_list

        resline_exist:bool = False
        mainres_list.ankunft = 01/01/2099
        mainres_list.abreise = 01/01/1998
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == mainres_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():
            resline_exist = True

            if res_line.resstatus != 11 and res_line.resstatus != 13:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if (res_line.resstatus <= 5 or res_line.resstatus == 11):
                mainres_list.arrival = True

            if mainres_list.arrival  and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

        if not resline_exist:
            mainres_list_list.remove(mainres_list)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 297)).first()
    other_time = htparam.finteger
    fill_mainres(1)

    for mainres_list in query(mainres_list_list):

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.resnr == mainres_list.resnr)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            resline = Resline()
            resline_list.append(resline)

            buffer_copy(res_line, resline)
            resline.kurzbez = zimkateg.kurzbez

    for bediener in db_session.query(Bediener).all():
        usr = Usr()
        usr_list.append(usr)

        usr.userinit = bediener.userinit
        usr.username = bediener.username

    return generate_output()