#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Htparam, Guest, Akt_kont, Bk_reser, Bk_func

def main_fs_create_main_page1bl(b1_resnr:int, b1_resline:int, to_date:date, recid_bk_veran:int):

    prepare_cache ([Bk_veran, Guest, Akt_kont, Bk_reser])

    resnr = 0
    resline = 0
    search_str = ""
    guestsort = 0
    curr_gastnr = 0
    readequipment = False
    name_contact:string = ""
    i:int = 0
    ind:int = 0
    bk_veran = htparam = guest = akt_kont = bk_reser = bk_func = None

    glist = veranb = htparam_date = None

    glist_data, Glist = create_model("Glist", {"gastnr":int, "karteityp":int, "name":string, "telefon":string, "land":string, "plz":string, "wohnort":string, "adresse1":string, "adresse2":string, "adresse3":string, "namekontakt":string, "von_datum":date, "bis_datum":date, "von_zeit":string, "bis_zeit":string, "rstatus":int, "fax":string, "firmen_nr":int})

    Veranb = create_buffer("Veranb",Bk_veran)
    Htparam_date = create_buffer("Htparam_date",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr, resline, search_str, guestsort, curr_gastnr, readequipment, name_contact, i, ind, bk_veran, htparam, guest, akt_kont, bk_reser, bk_func
        nonlocal b1_resnr, b1_resline, to_date, recid_bk_veran
        nonlocal veranb, htparam_date


        nonlocal glist, veranb, htparam_date
        nonlocal glist_data

        return {"resnr": resnr, "resline": resline, "search_str": search_str, "guestsort": guestsort, "curr_gastnr": curr_gastnr, "readequipment": readequipment}


    glist_data.clear()

    bk_veran = get_cache (Bk_veran, {"_recid": [(eq, recid_bk_veran)]})

    if b1_resnr != 0:
        resnr = b1_resnr
        resline = b1_resline

        veranb = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, veranb.gastnr)]})
        search_str = guest.name
        guestsort = guest.karteityp
        curr_gastnr = guest.gastnr

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

        if akt_kont:
            name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        else:
            name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        glist = query(glist_data, filters=(lambda glist: glist.gastnr == veranb.gastnr), first=True)

        if not glist:
            glist = Glist()
            glist_data.append(glist)

            glist.gastnr = guest.gastnr
            glist.karteityp = guest.karteityp
            glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
            glist.adresse1 = guest.adresse1
            glist.adresse2 = guest.adresse2
            glist.adresse3 = guest.adresse3
            glist.telefon = guest.telefon
            glist.land = guest.land
            glist.plz = guest.plz
            glist.wohnort = guest.wohnort
            glist.namekontakt = name_contact
            glist.rstatus = veranb.resstatus
            glist.fax = guest.fax
            glist.firmen_nr = guest.firmen_nr
        readequipment = True

        return generate_output()

    veranb_obj_list = {}
    veranb = Bk_veran()
    guest = Guest()
    bk_reser = Bk_reser()
    for veranb.resstatus, veranb._recid, veranb.gastnr, veranb.veran_nr, guest.name, guest.karteityp, guest.gastnr, guest.vorname1, guest.anrede1, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.land, guest.plz, guest.wohnort, guest.fax, guest.firmen_nr, guest._recid, bk_reser.veran_seite, bk_reser._recid in db_session.query(Veranb.resstatus, Veranb._recid, Veranb.gastnr, Veranb.veran_nr, Guest.name, Guest.karteityp, Guest.gastnr, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.land, Guest.plz, Guest.wohnort, Guest.fax, Guest.firmen_nr, Guest._recid, Bk_reser.veran_seite, Bk_reser._recid).join(Guest,(Guest.gastnr == Veranb.gastnr)).join(Bk_reser,(Bk_reser.veran_nr == Veranb.veran_nr) & (Bk_reser.resstatus <= 3)).filter(
             (Veranb.limit_date <= to_date) & (Veranb.activeflag == 0)).order_by(Guest.karteityp, Guest.name).all():
        if veranb_obj_list.get(veranb._recid):
            continue
        else:
            veranb_obj_list[veranb._recid] = True


        ind = ind + 1

        if ind == 1:
            resnr = veranb.veran_nr
            resline = bk_reser.veran_seite

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

        if akt_kont:
            name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        else:
            name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        glist = query(glist_data, filters=(lambda glist: glist.gastnr == veranb.gastnr), first=True)

        if not glist:
            guestsort = guest.karteityp
            glist = Glist()
            glist_data.append(glist)

            glist.gastnr = guest.gastnr
            glist.karteityp = guest.karteityp
            glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
            glist.adresse1 = guest.adresse1
            glist.adresse2 = guest.adresse2
            glist.adresse3 = guest.adresse3
            glist.telefon = guest.telefon
            glist.land = guest.land
            glist.plz = guest.plz
            glist.wohnort = guest.wohnort
            glist.namekontakt = name_contact
            glist.rstatus = bk_veran.resstatus
            glist.fax = guest.fax
            glist.firmen_nr = guest.firmen_nr
    readequipment = True

    veranb = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

    if not veranb:

        return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, veranb.gastnr)]})

    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, veranb.veran_nr)],"veran_seite": [(eq, resline)]})

    return generate_output()