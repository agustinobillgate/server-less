#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Bediener, Guest, Akt_kont, Guestseg, Segment, Queasy, Guest_pr

def gcf_atlist_create_listbl_fitria():

    prepare_cache ([Htparam, Bediener, Guest, Akt_kont, Guestseg, Segment, Queasy, Guest_pr])

    sflag:int = 0
    s_list_data = []
    htparam = bediener = guest = akt_kont = guestseg = segment = queasy = guest_pr = None

    s_list = None

    s_list_data, S_list = create_model("S_list", {"ktype":int, "gastnr":int, "segm":int, "code":string, "name":string, "kname":string, "phone":string, "fax":string, "adresse":string, "city":string, "land":string, "zip":string, "sales":string, "email":string, "guest_pr_code":string, "avail_guest_pr":bool, "flag":int, "segmbez":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sflag, s_list_data, htparam, bediener, guest, akt_kont, guestseg, segment, queasy, guest_pr


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    def create_list():

        nonlocal sflag, s_list_data, htparam, bediener, guest, akt_kont, guestseg, segment, queasy, guest_pr


        nonlocal s_list
        nonlocal s_list_data

        bediener1 = None
        Bediener1 =  create_buffer("Bediener1",Bediener)

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp >= 1) & (Guest.gastnr > 0)).order_by(Guest.name).all():
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.ktype = guest.karteityp
            s_list.gastnr = guest.gastnr
            s_list.name = guest.name
            s_list.phone = guest.telefon
            s_list.fax = guest.fax
            s_list.adresse = guest.adresse1
            s_list.city = guest.wohnort
            s_list.land = guest.land
            s_list.zip = guest.plz

            for akt_kont in db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == guest.gastnr) & (substring(Akt_kont.abteilung, 0, 3) != ("Acc").lower())).order_by(Akt_kont.hauptkontakt.desc()).all():
                s_list.kname = akt_kont.name

                if akt_kont.vorname != "":

                    if s_list.kname == "":
                        s_list.kname = akt_kont.vorname
                    else:
                        s_list.kname = s_list.kname + ", " + akt_kont.vorname
                break

            if s_list.kname == "":

                akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

                if akt_kont:
                    s_list.kname = akt_kont.name

                    if akt_kont.vorname != "":

                        if s_list.kname == "":
                            s_list.kname = akt_kont.vorname
                        else:
                            s_list.kname = s_list.kname + ", " + akt_kont.vorname

            for guestseg in db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == guest.gastnr)).order_by(Guestseg.reihenfolge.desc()).all():

                segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                s_list.segm = segment.segmentgrup
                s_list.code = entry(0, segment.bezeich, "$$0")

                queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, s_list.segm)]})
                s_list.segmbez = queasy.char3
                break

            if guest.adresse2 != "":
                s_list.adresse = s_list.adresse + " " + guest.adresse2

            if guest.phonetik3 != "":

                bediener1 = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                if bediener1:
                    s_list.sales = bediener1.username
            s_list.email = guest.email_adr

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, s_list.gastnr)]})

            if guest_pr:
                s_list.guest_pr_code = guest_pr.code
                s_list.avail_guest_pr = True
                s_list.flag = sflag


    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4 and htparam.flogical:
        sflag = 1
    else:
        sflag = 2
    create_list()

    return generate_output()