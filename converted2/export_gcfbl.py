#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_bedienerbl import read_bedienerbl
from models import Bediener, Guest, Queasy, Guestseg, Segment, Akt_kont

def export_gcfbl(cardtype:int, crm_flag:bool):

    prepare_cache ([Guest, Queasy, Guestseg, Segment, Akt_kont])

    guest_list_data = []
    nr:int = 0
    mastername:string = ""
    sales_name:string = ""
    mainsegm:string = ""
    bediener = guest = queasy = guestseg = segment = akt_kont = None

    guest_list = usr = masterguest = t_queasy = b_queasy = None

    guest_list_data, Guest_list = create_model("Guest_list", {"nr":int, "guest_nr":int, "guest_name":string, "guest_title":string, "address1":string, "address2":string, "address3":string, "city":string, "zip":string, "country":string, "mastercomp":string, "salesid":string, "salesid_name":string, "refno2":string, "refno3":string, "phone":string, "telefax":string, "email":string, "maincontact":string, "main_fname":string, "main_tittle":string, "main_bday":date, "main_bplace":string, "main_telp":string, "main_ext":string, "main_dept":string, "main_function":string, "main_email":string, "segmentcode":string, "tot_room":int, "tot_revenue":Decimal, "tot_room_revenue":Decimal, "tot_fb_revenue":Decimal, "tot_otherrevenue":Decimal, "refno4":string, "keyaccount":string})
    usr_data, Usr = create_model_like(Bediener)

    Masterguest = create_buffer("Masterguest",Guest)
    T_queasy = create_buffer("T_queasy",Queasy)
    B_queasy = create_buffer("B_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_list_data, nr, mastername, sales_name, mainsegm, bediener, guest, queasy, guestseg, segment, akt_kont
        nonlocal cardtype, crm_flag
        nonlocal masterguest, t_queasy, b_queasy


        nonlocal guest_list, usr, masterguest, t_queasy, b_queasy
        nonlocal guest_list_data, usr_data

        return {"guest-list": guest_list_data}


    guest = get_cache (Guest, {"karteityp": [(eq, cardtype)],"gastnr": [(gt, 0)]})
    while None != guest:
        nr = nr + 1
        guest_list = Guest_list()
        guest_list_data.append(guest_list)

        guest_list.nr = nr
        guest_list.guest_nr = guest.gastnr
        guest_list.salesid = guest.phonetik3

        masterguest = get_cache (Guest, {"gastnr": [(eq, guest.master_gastnr)]})

        if masterguest:
            mastername = masterguest.name + " " + masterguest.vorname1
        usr_data.clear()
        usr_data = get_output(read_bedienerbl(0, guest.phonetik3))

        usr = query(usr_data, first=True)

        if usr:
            sales_name = usr.username

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

        if guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

            if segment:
                mainsegm = entry(0, segment.bezeich, "$$0")

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"hauptkontakt": [(eq, True)]})

        if akt_kont:
            guest_list.maincontact = akt_kont.name
            guest_list.main_fname = akt_kont.vorname
            guest_list.main_tittle = akt_kont.anrede
            guest_list.main_bday = akt_kont.geburtdatum1
            guest_list.main_bplace = akt_kont.geburt_ort1
            guest_list.main_telp = akt_kont.telefon
            guest_list.main_ext = akt_kont.durchwahl
            guest_list.main_dept = akt_kont.abteilung
            guest_list.main_function = akt_kont.funktion
            guest_list.main_email = akt_kont.email_adr


        guest_list.guest_name = guest.name + " " + guest.vorname1
        guest_list.guest_title = guest.anredefirma
        guest_list.address1 = guest.adresse1
        guest_list.address2 = guest.adresse2
        guest_list.address3 = guest.adresse3
        guest_list.city = guest.wohnort
        guest_list.zip = guest.plz
        guest_list.country = guest.land
        guest_list.mastercomp = mastername
        guest_list.salesid = guest.phonetik3
        guest_list.salesid_name = sales_name
        guest_list.refno2 = to_string(guest.point_gastnr)
        guest_list.refno3 = to_string(guest.steuernr)
        guest_list.phone = guest.telefon
        guest_list.telefax = guest.fax
        guest_list.email = guest.email_adr
        guest_list.segmentcode = mainsegm


        mastername = ""
        sales_name = ""
        mainsegm = ""

        queasy = get_cache (Queasy, {"key": [(eq, 231)],"number1": [(eq, guest_list.guest_nr)]})

        if queasy:
            guest_list.refno4 = queasy.char1

        t_queasy = get_cache (Queasy, {"key": [(eq, 212)],"number3": [(eq, guest_list.guest_nr)]})

        if t_queasy:

            b_queasy = get_cache (Queasy, {"key": [(eq, 211)],"number1": [(eq, t_queasy.number1)]})

            if b_queasy:
                guest_list.keyaccount = b_queasy.char1

        curr_recid = guest._recid
        guest = db_session.query(Guest).filter(
                 (Guest.karteityp == cardtype) & (Guest.gastnr > 0) & (Guest._recid > curr_recid)).first()

    if crm_flag:

        for guest_list in query(guest_list_data, filters=(lambda guest_list: guest_list.refno4 == "")):
            guest_list_data.remove(guest_list)
        nr = 0

        for guest_list in query(guest_list_data):
            nr = nr + 1
            guest_list.nr = nr

    return generate_output()