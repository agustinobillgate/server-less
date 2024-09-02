from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Guestseg, Guest_pr, Mc_guest, Mc_types, Segment

def gcf_print_1bl(pvilanguage:int, fl_list:bool, city:str, sorttype:int, from_name:str, to_name:str, segm_all:bool, paytype:int, prtype:int, fl_email:bool, segmentcode:int, fdate:date, tdate:date, fl_mcid:bool, prov:bool):
    output_list_list = []
    gcf_print2_list = []
    anzahl = 0
    lvcarea:str = "gcf_print"
    guest = guestseg = guest_pr = mc_guest = mc_types = segment = None

    output_list = gcf_print2 = guest1 = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    gcf_print2_list, Gcf_print2 = create_model_like(Guest, {"ratecode":str, "memberno":str, "membertype":str, "count_num":int, "segment":str})

    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, gcf_print2_list, anzahl, lvcarea, guest, guestseg, guest_pr, mc_guest, mc_types, segment
        nonlocal guest1


        nonlocal output_list, gcf_print2, guest1
        nonlocal output_list_list, gcf_print2_list
        return {"output-list": output_list_list, "gcf-print2": gcf_print2_list, "anzahl": anzahl}

    def create_gcflist():

        nonlocal output_list_list, gcf_print2_list, anzahl, lvcarea, guest, guestseg, guest_pr, mc_guest, mc_types, segment
        nonlocal guest1


        nonlocal output_list, gcf_print2, guest1
        nonlocal output_list_list, gcf_print2_list

        str1:str = ""
        do_it:bool = False
        to_city:str = "zzz"
        Guest1 = Guest
        output_list_list.clear()

        if city != "":
            to_city = city

        for guest in db_session.query(Guest).filter(
                (Guest.gastnr > 0) &  (Guest.karteityp == sorttype) &  (func.lower(Guest.name) >= (from_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower()) &  (func.lower(Guest.wohnort) >= (city).lower()) &  (func.lower(Guest.wohnort) <= (to_city).lower()) &  (Guest.anlage_datum >= fdate) &  (Guest.anlage_datum <= tdate)).all():
            do_it = True

            if not segm_all:

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr) &  (Guestseg.segmentcode == segmentcode)).first()
                do_it = None != guestseg

            if do_it and paytype > 0:

                if paytype == 1:
                    do_it = (guest.zahlungsart != 0)
                else:
                    do_it = (guest.zahlungsart == 0)

            if do_it and prtype > 0:

                guest_pr = db_session.query(Guest_pr).filter(
                        (Guest_pr.gastnr == guest.gastnr)).first()

                if prtype == 1:
                    do_it = None != guest_pr
                else:
                    do_it = not None != guest_pr

            if do_it and fl_email:

                if guest.email_adr == "":
                    do_it = False

            if do_it and fl_mcid:

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == guest.gastnr)).first()

                if not mc_guest:
                    do_it = False

            if do_it:
                anzahl = anzahl + 1

                if sorttype == 0:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = to_string((translateExtended ("Name :", lvcarea, "") + " " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1) , "x(64)") + translateExtended ("CardNo :", lvcarea, "") + " " + to_string(guest.gastnr)
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + "  " + guest.adresse2

                    if guest.adresse3 != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = "         " + guest.adresse3
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("city :", lvcarea, "") + " " + guest.land + " - " + to_string(guest.plz) + " " + guest.wohnort

                    if prov:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Province :", lvcarea, "") + " " + guest.geburt_ort2
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Telephone :", lvcarea, "") + " " + to_string(guest.telefon) + "   " + translateExtended ("Telefax :", lvcarea, "") + " " + to_string(guest.fax)

                    if guest.email_adr != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("E_mail :", lvcarea, "") + " " + guest.email_adr
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if guest.geburtdatum1 != None:
                        output_list.str = translateExtended ("Birthdate :", lvcarea, "") + " " + to_string(guest.geburtdatum1) + "   " + translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)
                    else:
                        output_list.str = translateExtended ("Birthdate :", lvcarea, "") + " " + "          " + "   " + translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)

                    if guest.zahlungsart != 0:
                        output_list.str = output_list.str + "   " + translateExtended ("Payment :", lvcarea, "") + " " + to_string(guest.zahlungsart)

                    if guest.master_gastnr != 0:

                        guest1 = db_session.query(Guest1).filter(
                                (Guest1.gastnr == guest.master_gastnr)).first()
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Master Company :", lvcarea, "") + " " + guest1.name + " " + guest.anredefirma

                    if fl_mcid:

                        mc_guest = db_session.query(Mc_guest).filter(
                                (Mc_guest.gastnr == guest.gastnr)).first()

                        if mc_guest:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.str = translateExtended ("Membership No :", lvcarea, "") + " " + mc_guest.cardnum

                            mc_types = db_session.query(Mc_types).filter(
                                    (Mc_types.nr == mc_guest.nr)).first()

                            if mc_types:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.str = translateExtended ("Membership Type :", lvcarea, "") + " " + mc_types.bezeich

                    if prtype == 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Rate Codes :", lvcarea, "")

                        for guest_pr in db_session.query(Guest_pr).filter(
                                (Guest_pr.gastnr == guest.gastnr)).all():
                            output_list.str = output_list.str + " " + guest_pr.CODE + ";"

                    if guest.bemerk != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Comments :", lvcarea, "") + " " + to_string(guest.bemerk, "x(80)")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = chr (10)

                elif sorttype == 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = to_string((translateExtended ("Name :", lvcarea, "") + " " + guest.name + " " + guest.anredefirma) , "x(64)") + translateExtended ("CardNo :", lvcarea, "") + " " + to_string(guest.gastnr)
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + "  " + guest.adresse2

                    if guest.adresse3 != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = "         " + guest.adresse3
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("city :", lvcarea, "") + " " + guest.land + " - " + to_string(guest.plz) + " " + guest.wohnort

                    if prov:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Province :", lvcarea, "") + " " + guest.geburt_ort2
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Telephone :", lvcarea, "") + " " + to_string(guest.telefon) + "   " + translateExtended ("Telefax :", lvcarea, "") + " " + to_string(guest.fax)

                    if guest.email_adr != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("E_mail :", lvcarea, "") + " " + guest.email_adr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)

                    if guest.zahlungsart != 0:
                        output_list.str = output_list.str + "   " + translateExtended ("Payment :", lvcarea, "") + " " + to_string(guest.zahlungsart)

                    if guest.namekontakt != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Contact Name :", lvcarea, "") + " " + guest.namekontakt

                    if guest.master_gastnr != 0:

                        guest1 = db_session.query(Guest1).filter(
                                (Guest1.gastnr == guest.master_gastnr)).first()
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Master Company :", lvcarea, "") + " " + guest1.name + " " + guest.anredefirma

                    if fl_mcid:

                        mc_guest = db_session.query(Mc_guest).filter(
                                (Mc_guest.gastnr == guest.gastnr)).first()

                        if mc_guest:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.str = translateExtended ("Membership No :", lvcarea, "") + " " + mc_guest.cardnum

                            mc_types = db_session.query(Mc_types).filter(
                                    (Mc_types.nr == mc_guest.nr)).first()

                            if mc_types:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.str = translateExtended ("Membership Type :", lvcarea, "") + " " + mc_types.bezeich

                    if prtype == 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Rate Codes :", lvcarea, "")

                        for guest_pr in db_session.query(Guest_pr).filter(
                                (Guest_pr.gastnr == guest.gastnr)).all():
                            output_list.str = output_list.str + " " + guest_pr.CODE + ";"

                    if guest.bemerk != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Comments :", lvcarea, "") + " " + to_string(guest.bemerk, "x(80)")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = chr (10)

                elif sorttype == 2:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = to_string((translateExtended ("Name :", lvcarea, "") + " " + guest.name + " " + guest.anredefirma) , "x(64)") + translateExtended ("CardNo :", lvcarea, "") + " " + to_string(guest.gastnr)
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + "  " + guest.adresse2

                    if guest.adresse3 != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = "         " + guest.adresse3
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("city :", lvcarea, "") + " " + guest.land + " - " + to_string(guest.plz) + " " + guest.wohnort

                    if prov:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Province :", lvcarea, "") + " " + guest.geburt_ort2
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Telephone :", lvcarea, "") + " " + to_string(guest.telefon) + "   " + translateExtended ("Telefax :", lvcarea, "") + " " + to_string(guest.fax)

                    if guest.email_adr != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("E_mail :", lvcarea, "") + " " + guest.email_adr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = translateExtended ("Credit Limit :", lvcarea, "") + " " + to_string(guest.kreditlimit)

                    if guest.zahlungsart != 0:
                        output_list.str = output_list.str + "   " + translateExtended ("Payment :", lvcarea, "") + " " + to_string(guest.zahlungsart)

                    if guest.namekontakt != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Contact Name :", lvcarea, "") + " " + guest.namekontakt

                    if guest.master_gastnr != 0:

                        guest1 = db_session.query(Guest1).filter(
                                (Guest1.gastnr == guest.master_gastnr)).first()
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Master Company :", lvcarea, "") + " " + guest1.name + " " + guest.anredefirma

                    if fl_mcid:

                        mc_guest = db_session.query(Mc_guest).filter(
                                (Mc_guest.gastnr == guest.gastnr)).first()

                        if mc_guest:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.str = translateExtended ("Membership No :", lvcarea, "") + " " + mc_guest.cardnum

                            mc_types = db_session.query(Mc_types).filter(
                                    (Mc_types.nr == mc_guest.nr)).first()

                            if mc_types:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.str = translateExtended ("Membership Type :", lvcarea, "") + " " + mc_types.bezeich

                    if prtype == 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Rate Codes :", lvcarea, "")

                        for guest_pr in db_session.query(Guest_pr).filter(
                                (Guest_pr.gastnr == guest.gastnr)).all():
                            output_list.str = output_list.str + " " + guest_pr.CODE + ";"

                    if guest.bemerk != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = translateExtended ("Comments :", lvcarea, "") + " " + to_string(guest.bemerk, "x(80)")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = chr (10)

    def create_gcflist1():

        nonlocal output_list_list, gcf_print2_list, anzahl, lvcarea, guest, guestseg, guest_pr, mc_guest, mc_types, segment
        nonlocal guest1


        nonlocal output_list, gcf_print2, guest1
        nonlocal output_list_list, gcf_print2_list

        str1:str = ""
        do_it:bool = False
        to_city:str = "zzz"
        Guest1 = Guest
        gcf_print2_list.clear()

        if city != "":
            to_city = city

        for guest in db_session.query(Guest).filter(
                (Guest.gastnr > 0) &  (Guest.karteityp == sorttype) &  (func.lower(Guest.name) >= (from_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower()) &  (func.lower(Guest.wohnort) >= (city).lower()) &  (func.lower(Guest.wohnort) <= (to_city).lower()) &  (Guest.anlage_datum >= fdate) &  (Guest.anlage_datum <= tdate)).all():
            do_it = True

            if not segm_all :

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr) &  (Guestseg.segmentcode == segmentcode)).first()
                do_it = None != guestseg

            if do_it and paytype > 0:

                if paytype == 1:
                    do_it = (guest.zahlungsart != 0)
                else:
                    do_it = (guest.zahlungsart == 0)

            if do_it and prtype > 0:

                guest_pr = db_session.query(Guest_pr).filter(
                        (Guest_pr.gastnr == guest.gastnr)).first()

                if prtype == 1:
                    do_it = None != guest_pr
                else:
                    do_it = not None != guest_pr

            if do_it and fl_email:

                if guest.email_adr == "":
                    do_it = False

            if do_it and fl_mcid:

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == guest.gastnr)).first()

                if not mc_guest:
                    do_it = False

            if do_it:
                anzahl = anzahl + 1
                gcf_print2 = Gcf_print2()
                gcf_print2_list.append(gcf_print2)

                gcf_print2.count_num = anzahl
                buffer_copy(guest, gcf_print2)

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == guest.gastnr)).first()

                if mc_guest:
                    gcf_print2.memberno = mc_guest.cardnum

                    mc_types = db_session.query(Mc_types).filter(
                            (Mc_types.nr == mc_guest.nr)).first()

                    if mc_types:
                        gcf_print2.membertype = mc_types.bezeich

                if prtype == 1:

                    for guest_pr in db_session.query(Guest_pr).filter(
                            (Guest_pr.gastnr == guest.gastnr)).all():
                        gcf_print2.ratecode = gcf_print2.ratecode + guest_pr.CODE + ";"


                if segm_all:

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == guestseg.segmentcode)).first()

                if segment:
                    gcf_print2.segment = segment.bezeich
                else:
                    gcf_print2.segment = ""


    if fl_list:
        create_gcflist1()
    else:
        create_gcflist()

    return generate_output()