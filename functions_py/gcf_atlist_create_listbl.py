#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 4/9/2025
# beda sorting dengan OE
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Guest, Akt_kont, Guestseg, Segment, Queasy, Guest_pr, Htparam

def gcf_atlist_create_listbl():

    prepare_cache ([Bediener, Guest, Akt_kont, Guestseg, Segment, Queasy, Guest_pr, Htparam])

    s_list_data = []
    bediener = guest = akt_kont = guestseg = segment = queasy = guest_pr = htparam = None

    s_list = None

    s_list_data, S_list = create_model("S_list", {"ktype":int, "gastnr":int, "segm":int, "code":string, "name":string, "kname":string, "phone":string, "fax":string, "adresse":string, "city":string, "land":string, "zip":string, "sales":string, "email":string, "guest_pr_code":string, "avail_guest_pr":bool, "flag":int, "segmbez":string})


    set_cache(Guest, (Guest.karteityp >= 1) & (Guest.gastnr > 0),[], True,[],["gastnr"])
    set_cache(Guestseg, (Guestseg.gastnr.in_(get_cache_value_list(Guest,"gastnr"))),[["gastnr", "reihenfolge"], ["gastnr"]], True,[],[])
    set_cache(Akt_kont, (Akt_kont.gastnr.in_(get_cache_value_list(Guest,"gastnr"))),[["gastnr"]], True,[],[])
    set_cache(Guest_pr, (Guest_pr.gastnr.in_(get_cache_value_list(Guest,"gastnr"))),[["gastnr"]], True,[],[])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, bediener, guest, akt_kont, guestseg, segment, queasy, guest_pr, htparam


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    def create_list():

        nonlocal s_list_data, bediener, guest, akt_kont, guestseg, segment, queasy, guest_pr, htparam


        nonlocal s_list
        nonlocal s_list_data

        bediener1 = None
        Bediener1 =  create_buffer("Bediener1",Bediener)

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp >= 1) & (Guest.gastnr > 0)).order_by(Guest.name).all():

            akt_kont = db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == guest.gastnr) & (substring(Akt_kont.abteilung, 0, 3) != ("Acc").lower()) & (Akt_kont.hauptkontakt)).first()

            if not akt_kont:

                akt_kont = db_session.query(Akt_kont).filter(
                         (Akt_kont.gastnr == guest.gastnr) & (substring(Akt_kont.abteilung, 0, 3) != ("Acc").lower())).first()

            if not akt_kont:

                akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

            if not guestseg:

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
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

            if akt_kont:
                s_list.kname = akt_kont.name

                if akt_kont.vorname != "":

                    if s_list.kname == "":
                        s_list.kname = akt_kont.vorname
                    else:
                        s_list.kname = s_list.kname + ", " + akt_kont.vorname

            if guestseg:

                segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                s_list.segm = segment.segmentgrup
                s_list.code = entry(0, segment.bezeich, "$$0")

                queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, s_list.segm)]})
                s_list.segmbez = queasy.char3

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

                htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

                if htparam.feldtyp == 4 and htparam.flogical:
                    s_list.flag = 1
                else:
                    s_list.flag = 2

    create_list()

    return generate_output()