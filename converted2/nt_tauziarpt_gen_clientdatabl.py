#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Akt_kont

def nt_tauziarpt_gen_clientdatabl(casetype:int, curr_date:date, fdate:date, tdate:date):
    t_list_list = []
    cp1:str = ""
    cp2:str = ""
    cp3:str = ""
    guest_name:str = ""
    guest_adr:str = ""
    guest_comp:str = ""
    guest = akt_kont = None

    t_list = gbuff = None

    t_list_list, T_list = create_model_like(Guest, {"cp1":str, "cp2":str, "cp3":str, "guest_name":str, "guest_adr":str})

    Gbuff = create_buffer("Gbuff",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, cp1, cp2, cp3, guest_name, guest_adr, guest_comp, guest, akt_kont
        nonlocal casetype, curr_date, fdate, tdate
        nonlocal gbuff


        nonlocal t_list, gbuff
        nonlocal t_list_list

        return {"t-list": t_list_list}


    t_list_list.clear()

    if casetype == 1:

        for guest in db_session.query(Guest).filter(
                 (Guest.gastnr > 0) & (Guest.karteityp > 0) & (((Guest.anlage_datum == curr_date) | (Guest.modif_datum == curr_date)) | ((Guest.modif_datum >= curr_date) & (Guest.modif_datum <= curr_date)))).order_by(Guest._recid).all():

            akt_kont = db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == guest.gastnr)).first()

            if akt_kont:
                cp1 = to_string(akt_kont.name + akt_kont.vorname)
                cp2 = to_string(akt_kont.anrede)
                cp3 = to_string(akt_kont.abteilung)


            else:
                cp1 = "" cp2 == "" cp3 == ""

            if trim(guest.name) != "" or trim(guest.anrede1) != "":
                guest_name = trim(to_string(guest.name + " " + guest.anrede1))
            else:
                guest_name = ""

            if trim(guest.adresse1) != "" or trim(guest.adresse2) != "":
                guest_adr = trim(to_string(guest.adresse1 + " " + guest.adresse2))
            else:
                guest_adr = ""

            gbuff = db_session.query(Gbuff).filter(
                     (Gbuff.gastnr == guest.master_gastnr)).first()

            if gbuff:
                guest_comp = trim(gbuff.name + ", " + gbuff.anredefirma)
            t_list = T_list()
            t_list_list.append(t_list)

            buffer_copy(guest, t_list)
            t_list.cp1 = cp1
            t_list.cp2 = cp2
            t_list.cp3 = cp3
            t_list.guest_name = guest_name + "$#" + guest_comp
            t_list.guest_adr = guest_adr

    else:

        for guest in db_session.query(Guest).filter(
                 (Guest.gastnr > 0) & (Guest.karteityp > 0) & (((Guest.anlage_datum >= fdate) & (Guest.anlage_datum <= tdate)) | ((Guest.modif_datum >= fdate) & (Guest.modif_datum <= tdate)))).order_by(Guest._recid).all():

            akt_kont = db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == guest.gastnr)).first()

            if akt_kont:
                cp1 = to_string(akt_kont.name + akt_kont.vorname)
                cp2 = to_string(akt_kont.anrede)
                cp3 = to_string(akt_kont.abteilung)


            else:
                cp1 = "" cp2 == "" cp3 == ""

            if trim(guest.name) != "" or trim(guest.anrede1) != "":
                guest_name = trim(to_string(guest.name + " " + guest.anrede1))
            else:
                guest_name = ""

            if trim(guest.adresse1) != "" or trim(guest.adresse2) != "":
                guest_adr = trim(to_string(guest.adresse1 + " " + guest.adresse2))
            else:
                guest_adr = ""

            gbuff = db_session.query(Gbuff).filter(
                     (Gbuff.gastnr == guest.master_gastnr)).first()

            if gbuff:
                guest_comp = trim(gbuff.name + ", " + gbuff.anredefirma)
            t_list = T_list()
            t_list_list.append(t_list)

            buffer_copy(guest, t_list)
            t_list.cp1 = cp1
            t_list.cp2 = cp2
            t_list.cp3 = cp3
            t_list.guest_name = guest_name + "$#" + guest_comp
            t_list.guest_adr = guest_adr


    return generate_output()