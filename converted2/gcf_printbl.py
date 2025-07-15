#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guestseg, Guest_pr, Mc_guest

def gcf_printbl(pvilanguage:int, fl_list:bool, city:string, sorttype:int, from_name:string, to_name:string, segm_all:bool, paytype:int, prtype:int, fl_email:bool, segmentcode:int):

    prepare_cache ([Guest, Mc_guest])

    output_list_data = []
    gcf_print2_data = []
    anzahl = 0
    lvcarea:string = "gcf-print"
    guest = guestseg = guest_pr = mc_guest = None

    output_list = gcf_print2 = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    gcf_print2_data, Gcf_print2 = create_model_like(Guest, {"ratecode":string, "memberno":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, gcf_print2_data, anzahl, lvcarea, guest, guestseg, guest_pr, mc_guest
        nonlocal pvilanguage, fl_list, city, sorttype, from_name, to_name, segm_all, paytype, prtype, fl_email, segmentcode


        nonlocal output_list, gcf_print2
        nonlocal output_list_data, gcf_print2_data

        return {"output-list": output_list_data, "gcf-print2": gcf_print2_data, "anzahl": anzahl}

    def create_gcflist():

        nonlocal output_list_data, gcf_print2_data, anzahl, lvcarea, guest, guestseg, guest_pr, mc_guest
        nonlocal pvilanguage, fl_list, city, sorttype, from_name, to_name, segm_all, paytype, prtype, fl_email, segmentcode


        nonlocal output_list, gcf_print2
        nonlocal output_list_data, gcf_print2_data

        str1:string = ""
        do_it:bool = False
        guest1 = None
        to_city:string = "zzz"
        Guest1 =  create_buffer("Guest1",Guest)
        output_list_data.clear()

        if city != "":
            to_city = city

        for guest in db_session.query(Guest).filter(
                 (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower()) & (Guest.wohnort >= (city).lower()) & (Guest.wohnort <= (to_city).lower())).order_by(Guest.name).all():
            do_it = True

            if not segm_all:

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"segmentcode": [(eq, segmentcode)]})
                do_it = None != guestseg

            if do_it and paytype > 0:

                if paytype == 1:
                    do_it = (guest.zahlungsart != 0)
                else:
                    do_it = (guest.zahlungsart == 0)

            if do_it and prtype > 0:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                if prtype == 1:
                    do_it = None != guest_pr
                else:
                    do_it = not None != guest_pr

            if do_it and fl_email:

                if guest.email_adr == "":
                    do_it = False

            if do_it:
                anzahl = anzahl + 1

                if sorttype == 0:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = to_string((translateExtended ("Name :", lvcarea, "") + " " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1) , "x(64)") + translateExtended ("CardNo :", lvcarea, "") + " " + to_string(guest.gastnr)
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + " " + guest.adresse2

                    if guest.adresse3 != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = " " + guest.adresse3
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("city :", lvcarea, "") + " " + guest.land + " - " + to_string(guest.plz) + " " + guest.wohnort
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Telephone :", lvcarea, "") + " " + to_string(guest.telefon) + " " + translateExtended ("Telefax :", lvcarea, "") + " " + to_string(guest.fax)

                    if guest.email_adr != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("E-mail :", lvcarea, "") + " " + guest.email_adr
                    output_list = Output_list()
                    output_list_data.append(output_list)


                    if guest.geburtdatum1 != None:
                        output_list.str = translateExtended ("Birthdate :", lvcarea, "") + " " + to_string(guest.geburtdatum1) + " " + translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)
                    else:
                        output_list.str = translateExtended ("Birthdate :", lvcarea, "") + " " + " " + " " + translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)

                    if guest.zahlungsart != 0:
                        output_list.str = output_list.str + " " + translateExtended ("Payment :", lvcarea, "") + " " + to_string(guest.zahlungsart)

                    if guest.master_gastnr != 0:

                        guest1 = get_cache (Guest, {"gastnr": [(eq, guest.master_gastnr)]})
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Master Company :", lvcarea, "") + " " + guest1.name + " " + guest.anredefirma

                    if prtype == 1:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Rate Codes :", lvcarea, "")

                        for guest_pr in db_session.query(Guest_pr).filter(
                                 (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr.code).all():
                            output_list.str = output_list.str + " " + guest_pr.code + ";"

                    if guest.bemerkung != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Comments :", lvcarea, "") + " " + to_string(guest.bemerkung, "x(80)")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = chr_unicode(10)

                elif sorttype == 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = to_string((translateExtended ("Name :", lvcarea, "") + " " + guest.name + " " + guest.anredefirma) , "x(64)") + translateExtended ("CardNo :", lvcarea, "") + " " + to_string(guest.gastnr)
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + " " + guest.adresse2

                    if guest.adresse3 != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = " " + guest.adresse3
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("city :", lvcarea, "") + " " + guest.land + " - " + to_string(guest.plz) + " " + guest.wohnort
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Telephone :", lvcarea, "") + " " + to_string(guest.telefon) + " " + translateExtended ("Telefax :", lvcarea, "") + " " + to_string(guest.fax)

                    if guest.email_adr != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("E-mail :", lvcarea, "") + " " + guest.email_adr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)

                    if guest.zahlungsart != 0:
                        output_list.str = output_list.str + " " + translateExtended ("Payment :", lvcarea, "") + " " + to_string(guest.zahlungsart)

                    if guest.namekontakt != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Contact Name :", lvcarea, "") + " " + guest.namekontakt

                    if guest.master_gastnr != 0:

                        guest1 = get_cache (Guest, {"gastnr": [(eq, guest.master_gastnr)]})
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Master Company :", lvcarea, "") + " " + guest1.name + " " + guest.anredefirma

                    if prtype == 1:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Rate Codes :", lvcarea, "")

                        for guest_pr in db_session.query(Guest_pr).filter(
                                 (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr.code).all():
                            output_list.str = output_list.str + " " + guest_pr.code + ";"

                    if guest.bemerkung != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Comments :", lvcarea, "") + " " + to_string(guest.bemerkung, "x(80)")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = chr_unicode(10)

                elif sorttype == 2:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = to_string((translateExtended ("Name :", lvcarea, "") + " " + guest.name + " " + guest.anredefirma) , "x(64)") + translateExtended ("CardNo :", lvcarea, "") + " " + to_string(guest.gastnr)
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + " " + guest.adresse2

                    if guest.adresse3 != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = " " + guest.adresse3
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("city :", lvcarea, "") + " " + guest.land + " - " + to_string(guest.plz) + " " + guest.wohnort
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Telephone :", lvcarea, "") + " " + to_string(guest.telefon) + " " + translateExtended ("Telefax :", lvcarea, "") + " " + to_string(guest.fax)

                    if guest.email_adr != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("E-mail :", lvcarea, "") + " " + guest.email_adr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)

                    if guest.zahlungsart != 0:
                        output_list.str = output_list.str + " " + translateExtended ("Payment :", lvcarea, "") + " " + to_string(guest.zahlungsart)

                    if guest.namekontakt != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Contact Name :", lvcarea, "") + " " + guest.namekontakt

                    if guest.master_gastnr != 0:

                        guest1 = get_cache (Guest, {"gastnr": [(eq, guest.master_gastnr)]})
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Master Company :", lvcarea, "") + " " + guest1.name + " " + guest.anredefirma

                    if prtype == 1:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Rate Codes :", lvcarea, "")

                        for guest_pr in db_session.query(Guest_pr).filter(
                                 (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr.code).all():
                            output_list.str = output_list.str + " " + guest_pr.code + ";"

                    if guest.bemerkung != "":
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = translateExtended ("Comments :", lvcarea, "") + " " + to_string(guest.bemerkung, "x(80)")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = chr_unicode(10)


    def create_gcflist1():

        nonlocal output_list_data, gcf_print2_data, anzahl, lvcarea, guest, guestseg, guest_pr, mc_guest
        nonlocal pvilanguage, fl_list, city, sorttype, from_name, to_name, segm_all, paytype, prtype, fl_email, segmentcode


        nonlocal output_list, gcf_print2
        nonlocal output_list_data, gcf_print2_data

        str1:string = ""
        do_it:bool = False
        guest1 = None
        to_city:string = "zzz"
        Guest1 =  create_buffer("Guest1",Guest)
        gcf_print2_data.clear()

        if city != "":
            to_city = city

        for guest in db_session.query(Guest).filter(
                 (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.name >= (from_name).lower()) & (Guest.name <= (to_name).lower()) & (Guest.wohnort >= (city).lower()) & (Guest.wohnort <= (to_city).lower())).order_by(Guest.name).all():
            do_it = True

            if not segm_all :

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"segmentcode": [(eq, segmentcode)]})
                do_it = None != guestseg

            if do_it and paytype > 0:

                if paytype == 1:
                    do_it = (guest.zahlungsart != 0)
                else:
                    do_it = (guest.zahlungsart == 0)

            if do_it and prtype > 0:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                if prtype == 1:
                    do_it = None != guest_pr
                else:
                    do_it = not None != guest_pr

            if do_it and fl_email:

                if guest.email_adr == "":
                    do_it = False

            if do_it:
                anzahl = anzahl + 1
                gcf_print2 = Gcf_print2()
                gcf_print2_data.append(gcf_print2)

                buffer_copy(guest, gcf_print2)

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                if mc_guest:
                    gcf_print2.memberno = mc_guest.cardnum

                if prtype == 1:

                    for guest_pr in db_session.query(Guest_pr).filter(
                             (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr.code).all():
                        gcf_print2.ratecode = gcf_print2.ratecode + guest_pr.code + ";"


    if fl_list:
        create_gcflist1()
    else:
        create_gcflist()

    return generate_output()