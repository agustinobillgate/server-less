#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.export_topgcf_getturnoverbl import export_topgcf_getturnoverbl
from functions.read_bedienerbl import read_bedienerbl
from models import Bediener, Guest, Guestseg, Segment, Akt_kont, Queasy

def export_topgcfbl(cardtype:int, from_date:date, to_date:date, recordcount:int, crm_flag:bool, his_flag:bool):

    prepare_cache ([Guest, Guestseg, Segment, Akt_kont, Queasy])

    guest_list_data = []
    sort_type:int = 1
    check_ftd:bool = True
    currency:string = "Rp"
    excl_other:bool = False
    curr_sort:List[int] = create_empty_list(2,0)
    nr:int = 0
    mastername:string = ""
    sales_name:string = ""
    mainsegm:string = ""
    bediener = guest = guestseg = segment = akt_kont = queasy = None

    guest_list = cust_list = usr = masterguest = None

    guest_list_data, Guest_list = create_model("Guest_list", {"nr":int, "guest_nr":int, "guest_name":string, "guest_title":string, "address1":string, "address2":string, "address3":string, "city":string, "zip":string, "country":string, "mastercomp":string, "salesid":string, "salesid_name":string, "refno2":string, "refno3":string, "phone":string, "telefax":string, "email":string, "maincontact":string, "main_fname":string, "main_tittle":string, "main_bday":date, "main_bplace":string, "main_telp":string, "main_ext":string, "main_dept":string, "main_function":string, "main_email":string, "segmentcode":string, "tot_room":int, "tot_revenue":Decimal, "tot_room_revenue":Decimal, "tot_fb_revenue":Decimal, "tot_otherrevenue":Decimal, "refno4":string})
    cust_list_data, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})
    usr_data, Usr = create_model_like(Bediener)

    Masterguest = create_buffer("Masterguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_list_data, sort_type, check_ftd, currency, excl_other, curr_sort, nr, mastername, sales_name, mainsegm, bediener, guest, guestseg, segment, akt_kont, queasy
        nonlocal cardtype, from_date, to_date, recordcount, crm_flag, his_flag
        nonlocal masterguest


        nonlocal guest_list, cust_list, usr, masterguest
        nonlocal guest_list_data, cust_list_data, usr_data

        return {"guest-list": guest_list_data}


    curr_sort[0] = 1
    curr_sort[1] = 0
    check_ftd = True


    currency = ""
    excl_other = False
    sort_type = 1
    curr_sort[1], cust_list_data = get_output(export_topgcf_getturnoverbl(cardtype, sort_type, curr_sort[0], from_date, to_date, check_ftd, currency, excl_other, curr_sort[1]))

    if his_flag:

        for cust_list in query(cust_list_data, filters=(lambda cust_list: cust_list.gesamtumsatz != 0), sort_by=[("gesamtumsatz",True)]):
            nr = nr + 1
            guest_list = Guest_list()
            guest_list_data.append(guest_list)

            guest_list.nr = nr
            guest_list.guest_nr = cust_list.gastnr
            guest_list.salesid = cust_list.sales_id
            guest_list.tot_room = cust_list.logiernachte
            guest_list.tot_revenue =  to_decimal(cust_list.gesamtumsatz)
            guest_list.tot_room_revenue =  to_decimal(cust_list.argtumsatz)
            guest_list.tot_fb_revenue =  to_decimal(cust_list.f_b_umsatz) + to_decimal(cust_list.ba_umsatz)
            guest_list.tot_otherrevenue =  to_decimal(cust_list.sonst_umsatz)

            if recordcount != 0:

                if nr == recordcount:
                    break
    else:

        for cust_list in query(cust_list_data, sort_by=[("gesamtumsatz",True)]):
            nr = nr + 1
            guest_list = Guest_list()
            guest_list_data.append(guest_list)

            guest_list.nr = nr
            guest_list.guest_nr = cust_list.gastnr
            guest_list.salesid = cust_list.sales_id
            guest_list.tot_room = cust_list.logiernachte
            guest_list.tot_revenue =  to_decimal(cust_list.gesamtumsatz)
            guest_list.tot_room_revenue =  to_decimal(cust_list.argtumsatz)
            guest_list.tot_fb_revenue =  to_decimal(cust_list.f_b_umsatz) + to_decimal(cust_list.ba_umsatz)
            guest_list.tot_otherrevenue =  to_decimal(cust_list.sonst_umsatz)

            if recordcount != 0:

                if nr == recordcount:
                    break

        guest = get_cache (Guest, {"karteityp": [(eq, cardtype)]})
        while None != guest:

            guest_list = query(guest_list_data, filters=(lambda guest_list: guest_list.guest_nr == guest.gastnr), first=True)

            if not guest_list:
                nr = nr + 1
                guest_list = Guest_list()
                guest_list_data.append(guest_list)

                guest_list.nr = nr
                guest_list.guest_nr = guest.gastnr
                guest_list.salesid = guest.phonetik3

                if recordcount != 0:

                    if nr == recordcount:
                        break

            curr_recid = guest._recid
            guest = db_session.query(Guest).filter(
                     (Guest.karteityp == cardtype) & (Guest._recid > curr_recid)).first()

    for guest_list in query(guest_list_data):

        guest = get_cache (Guest, {"karteityp": [(eq, cardtype)],"gastnr": [(eq, guest_list.guest_nr)]})

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

    if crm_flag:

        for guest_list in query(guest_list_data, filters=(lambda guest_list: guest_list.refno4 == "")):
            guest_list_data.remove(guest_list)
        nr = 0

        for guest_list in query(guest_list_data):
            nr = nr + 1
            guest_list.nr = nr

    return generate_output()