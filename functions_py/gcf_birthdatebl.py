#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 21/8/20225
# beda sorting
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line

def gcf_birthdatebl(from_date:int, to_date:int, from_age:int, to_age:int, sorttype:int):

    prepare_cache ([Guest, Res_line])

    birth_list_data = []
    guest = res_line = None

    birth_list = None

    birth_list_data, Birth_list = create_model("Birth_list", {"name2":string, "geburtdatum":date, "ankunft1":date, "abreise1":date, "zinr":string, "adresse":string, "wohnort":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal birth_list_data, guest, res_line
        nonlocal from_date, to_date, from_age, to_age, sorttype


        nonlocal birth_list
        nonlocal birth_list_data

        return {"birth-list": birth_list_data}

    def age_list():

        nonlocal birth_list_data, guest, res_line
        nonlocal from_date, to_date, from_age, to_age, sorttype


        nonlocal birth_list
        nonlocal birth_list_data

        if sorttype == 1:
                # Rd 21/8/2025, sor by name
                #     for guest in db_session.query(Guest).filter(
                #              (Guest.karteityp == 0) & (Guest.gastnr > 0) & (Guest.name > "") & (Guest.vorname1 >= "") & (Guest.geburtdatum1 != None)).order_by(Guest._recid).all():
            for guest in db_session.query(Guest).filter(
                     (Guest.karteityp == 0) & (Guest.gastnr > 0) & 
                     (Guest.name > "") & 
                     (Guest.vorname1 >= "") & 
                     (Guest.geburtdatum1 != None)).order_by(Guest.name.asc()).all():

                if (get_month(guest.geburtdatum1) * 100 + get_day(guest.geburtdatum1)) >= from_date and (get_month(guest.geburtdatum1) * 100 + get_day(guest.geburtdatum1)) <= to_date and (- get_year(guest.geburtdatum1) + get_year(get_current_date())) >= from_age and (- get_year(guest.geburtdatum1) + get_year(get_current_date())) <= to_age:
                    birth_list = Birth_list()
                    birth_list_data.append(birth_list)

                    birth_list.name = guest.name + ", " + guest.vorname1 +\
                            " " + guest.anrede1
                    birth_list.geburtdatum = guest.geburtdatum1
                    birth_list.adresse = guest.adresse1 + " " + guest.adresse2 +\
                            " " + guest.adresse3 + chr_unicode(3) + guest.email_adr + chr_unicode(3) + guest.telefon + chr_unicode(3) + guest.mobil_telefon
                    birth_list.wohnort = guest.land + " - " + guest.plz +\
                            " " + guest.wohnort

                    if guest.resflag == 2:

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.gastnrmember == guest.gastnr) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()

                        if res_line:
                            birth_list.ankunft = res_line.ankunft
                            birth_list.abreise = res_line.abreise
                            birth_list.zinr = res_line.zinr


        else:
        
            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1)).order_by(Res_line._recid).all():

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)],"geburtdatum1": [(ne, None)]})

                if guest:

                    if (get_month(guest.geburtdatum1) * 100 + get_day(guest.geburtdatum1)) >= from_date and (get_month(guest.geburtdatum1) * 100 + get_day(guest.geburtdatum1)) <= to_date and (- get_year(guest.geburtdatum1) + get_year(get_current_date())) >= from_age and (- get_year(guest.geburtdatum1) + get_year(get_current_date())) <= to_age:
                        birth_list = Birth_list()
                        birth_list_data.append(birth_list)

                        birth_list.name = guest.name + ", " + guest.vorname1 +\
                                " " + guest.anrede1
                        birth_list.geburtdatum = guest.geburtdatum1
                        birth_list.adresse = guest.adresse1 + " " + guest.adresse2 +\
                                " " + guest.adresse3 + chr_unicode(3) + guest.email_adr + chr_unicode(3) + guest.telefon + chr_unicode(3) + guest.mobil_telefon
                        birth_list.wohnort = guest.land + " - " + guest.plz +\
                                " " + guest.wohnort
                        birth_list.ankunft = res_line.ankunft
                        birth_list.abreise = res_line.abreise
                        birth_list.zinr = res_line.zinr


    age_list()

    return generate_output()