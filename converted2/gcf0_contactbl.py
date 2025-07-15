#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont

aktkont_list_data, Aktkont_list = create_model_like(Akt_kont, {"nat":string, "email":string, "rec_id":int})

def gcf0_contactbl(aktkont_list_data:[Aktkont_list], case_type:int, gastnr:int):

    prepare_cache ([Akt_kont])

    main_kont = ""
    maincontact = ""
    kont_nr:int = 0
    akt_kont = None

    aktkont_list = a_buff = None

    A_buff = create_buffer("A_buff",Akt_kont)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_kont, maincontact, kont_nr, akt_kont
        nonlocal case_type, gastnr
        nonlocal a_buff


        nonlocal aktkont_list, a_buff

        return {"aktkont-list": aktkont_list_data, "main_kont": main_kont, "maincontact": maincontact}

    def fill_aktkont():

        nonlocal main_kont, maincontact, kont_nr, akt_kont
        nonlocal case_type, gastnr
        nonlocal a_buff


        nonlocal aktkont_list, a_buff


        buffer_copy(aktkont_list, akt_kont)
        akt_kont.funktion = aktkont_list.email + ";" + aktkont_list.nat

        if akt_kont.hauptkontakt :
            main_kont = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        maincontact = main_kont


    if case_type == 1:

        aktkont_list = query(aktkont_list_data, first=True)
        kont_nr = 0

        for a_buff in db_session.query(A_buff).filter(
                 (A_buff.gastnr == gastnr)).order_by(A_buff._recid).all():

            if a_buff.kontakt_nr > kont_nr:
                kont_nr = a_buff.kontakt_nr
        kont_nr = kont_nr + 1
        aktkont_list.kontakt_nr = kont_nr
        akt_kont = Akt_kont()
        db_session.add(akt_kont)

        fill_aktkont()
        akt_kont.kategorie = 1
        akt_kont.kontakt_nr = kont_nr
        akt_kont.gastnr = gastnr

    elif case_type == 2:

        aktkont_list = query(aktkont_list_data, first=True)

        akt_kont = get_cache (Akt_kont, {"_recid": [(eq, aktkont_list.rec_id)]})

        if akt_kont:
            buffer_copy(aktkont_list, akt_kont)
            pass

    return generate_output()