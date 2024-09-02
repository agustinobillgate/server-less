from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Guest, Akt_kont, Guestseg, Segment, Guest_pr, Htparam

def gcf_atlist_create_listbl():
    s_list_list = []
    bediener = guest = akt_kont = guestseg = segment = guest_pr = htparam = None

    s_list = bediener1 = None

    s_list_list, S_list = create_model("S_list", {"ktype":int, "gastnr":int, "segm":int, "code":str, "name":str, "kname":str, "phone":str, "fax":str, "adresse":str, "city":str, "land":str, "zip":str, "sales":str, "email":str, "guest_pr_code":str, "avail_guest_pr":bool, "flag":int})

    Bediener1 = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, bediener, guest, akt_kont, guestseg, segment, guest_pr, htparam
        nonlocal bediener1


        nonlocal s_list, bediener1
        nonlocal s_list_list
        return {"s-list": s_list_list}

    def create_list():

        nonlocal s_list_list, bediener, guest, akt_kont, guestseg, segment, guest_pr, htparam
        nonlocal bediener1


        nonlocal s_list, bediener1
        nonlocal s_list_list


        Bediener1 = Bediener

        for guest in db_session.query(Guest).filter(
                (Guest.karteityp >= 1) &  (Guest.gastnr > 0)).all():

            akt_kont = db_session.query(Akt_kont).filter(
                    (Akt_kont.gastnr == guest.gastnr) &  (substring(Akt_kont.abteilung, 0, 3) != "Acc") &  (Akt_kont.hauptkontakt)).first()

            if not akt_kont:

                akt_kont = db_session.query(Akt_kont).filter(
                        (Akt_kont.gastnr == guest.gastnr) &  (substring(Akt_kont.abteilung, 0, 3) != "Acc")).first()

            if not akt_kont:

                akt_kont = db_session.query(Akt_kont).filter(
                        (Akt_kont.gastnr == guest.gastnr)).first()

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

            if not guestseg:

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr)).first()
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.ktype = guest.karteityp
            s_list.gastnr = guest.gastnr
            s_list.name = guest.name
            s_list.phone = guest.telefon
            s_list.fax = guest.fax
            s_list.adresse = guest.adresse1
            s_list.city = guest.wohnort
            s_list.land = guest.land
            s_list.zip = guest.plz

            if akt_kont:
                s_list.kname = akt_kont.name

                if akt_kont.vorname != "":

                    if s_list.kname == "":
                        s_list.kname = akt_kont.vorname
                    else:
                        s_list.kname = s_list.kname + ", " + akt_kont.vorname

            if guestseg:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == guestseg.segmentcode)).first()
                s_list.segm = segmentgrup
                s_list.code = entry(0, segment.bezeich, "$$0")

            if guest.adresse2 != "":
                s_list.adresse = s_list.adresse + " " + guest.adresse2

            if guest.phonetik3 != "":

                bediener1 = db_session.query(Bediener1).filter(
                        (Bediener1.userinit == guest.phonetik3)).first()

                if bediener1:
                    s_list.sales = bediener1.username
            s_list.email = guest.email

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == s_list.gastnr)).first()

            if guest_pr:
                s_list.guest_pr_code = guest_pr.code
                s_list.avail_guest_pr = True

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 550)).first()

                if htparam.feldtyp == 4 and htparam.flogical:
                    s_list.flag = 1
                else:
                    s_list.flag = 2


    create_list()

    return generate_output()