from functions.additional_functions import *
import decimal
from models import Akt_kont, Guest

def gcf_contact_btn_exitbl(aktkont_list:[Aktkont_list], case_type:int, gastnr:int):
    kont_nr = 0
    akt_kont = guest = None

    aktkont_list = gbuff = abuff = None

    aktkont_list_list, Aktkont_list = create_model_like(Akt_kont)

    Gbuff = Guest
    Abuff = Akt_kont

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kont_nr, akt_kont, guest
        nonlocal gbuff, abuff


        nonlocal aktkont_list, gbuff, abuff
        nonlocal aktkont_list_list
        return {"kont_nr": kont_nr}

    if case_type == 1:

        aktkont_list = query(aktkont_list_list, first=True)
        kont_nr = 1

        for abuff in db_session.query(Abuff).filter(
                (Abuff.gastnr == gastnr)).all():
            kont_nr = abuff.kontakt_nr + 1
            break
        akt_kont = Akt_kont()
        db_session.add(akt_kont)

        buffer_copy(aktkont_list, akt_kont,except_fields=["kontakt_nr","gastnr","kategorie"])
        akt_kont.kategorie = 1
        akt_kont.kontakt_nr = kont_nr
        akt_kont.gastnr = gastnr

    elif case_type == 2:

        aktkont_list = query(aktkont_list_list, first=True)

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.kontakt_nr == aktkont_list.kontakt_nr)).first()
        buffer_copy(aktkont_list, akt_kont,except_fields=["kontakt_nr","gastnr","kategorie"])

    return generate_output()