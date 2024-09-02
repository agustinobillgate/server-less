from functions.additional_functions import *
import decimal
from models import Akt_kont

def gcf0_contact_btn_delnamebl(gastnr:int, kontnr:int):
    main_kont = ""
    maincontact = ""
    akt_kont = None

    akt_kont1 = None

    Akt_kont1 = Akt_kont

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_kont, maincontact, akt_kont
        nonlocal akt_kont1


        nonlocal akt_kont1
        return {"main_kont": main_kont, "maincontact": maincontact}


    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.kontakt_nr == kontnr)).first()

    if akt_kont.hauptkontakt :

        akt_kont1 = db_session.query(Akt_kont1).filter(
                (Akt_kont1.gastnr == gastnr) &  (Akt_kont1.hauptkontakt == False)).first()

        if akt_kont1:
            main_kont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede

            akt_kont = db_session.query(Akt_kont).first()
            akt_kont.hauptkontakt = False

            akt_kont = db_session.query(Akt_kont).first()
            akt_kont1.hauptkontakt = True

            akt_kont1 = db_session.query(Akt_kont1).first()
        else:
            main_kont = ""
        maincontact = main_kont

    akt_kont = db_session.query(Akt_kont).first()
    db_session.delete(akt_kont)

    return generate_output()