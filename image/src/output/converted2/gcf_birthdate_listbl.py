#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gcf_birthdatebl import gcf_birthdatebl

def gcf_birthdate_listbl(from_mm:int, from_dd:int, to_mm:int, to_dd:int, from_age:int, to_age:int, sorttype:int):
    birth_list2_list = []
    from_date:int = 0
    to_date:int = 0

    birth_list = birth_list2 = None

    birth_list_list, Birth_list = create_model("Birth_list", {"name":string, "geburtdatum":date, "ankunft1":date, "abreise1":date, "zinr":string, "adresse":string, "wohnort":string})
    birth_list2_list, Birth_list2 = create_model("Birth_list2", {"name":string, "geburtdatum":date, "ankunft1":date, "abreise1":date, "zinr":string, "adresse":string, "wohnort":string, "telefon":string, "mobil_telefon":string, "email_addr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal birth_list2_list, from_date, to_date
        nonlocal from_mm, from_dd, to_mm, to_dd, from_age, to_age, sorttype


        nonlocal birth_list, birth_list2
        nonlocal birth_list_list, birth_list2_list

        return {"birth-list2": birth_list2_list}

    from_date = from_mm * 100 + from_dd

    if from_mm <= to_mm:
        to_date = to_mm * 100 + to_dd
    else:
        to_date = (to_mm + 12) * 100 + to_dd
    birth_list_list = get_output(gcf_birthdatebl(from_date, to_date, from_age, to_age, sorttype))

    for birth_list2 in query(birth_list2_list):
        birth_list2_list.remove(birth_list2)

    for birth_list in query(birth_list_list):
        birth_list2 = Birth_list2()
        birth_list2_list.append(birth_list2)

        birth_list2.name = birth_list.name
        birth_list2.geburtdatum = birth_list.geburtdatum
        birth_list2.ankunft1 = birth_list.ankunft1
        birth_list2.abreise1 = birth_list.abreise1
        birth_list2.zinr = birth_list.zinr
        birth_list2.adresse = entry(0, birth_list.adresse, chr_unicode(3))
        birth_list2.wohnort = birth_list.wohnort

        if num_entries(birth_list.adresse, chr_unicode(3)) > 1:
            birth_list2.email_addr = entry(1, birth_list.adresse, chr_unicode(3))

            if num_entries(birth_list.adresse, chr_unicode(3)) > 2:
                birth_list2.telefon = entry(2, birth_list.adresse, chr_unicode(3))
                birth_list2.mobil_telefon = entry(3, birth_list.adresse, chr_unicode(3))

    return generate_output()