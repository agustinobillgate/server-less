from functions.additional_functions import *
import decimal
from models import Mast_art

def write_mast_artbl(case_type:int, resno:int, artikel_list:[Artikel_list]):
    mast_art = None

    artikel_list = None

    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mast_art


        nonlocal artikel_list
        nonlocal artikel_list_list
        return {}

    if case_type == 1:

        for mast_art in db_session.query(Mast_art).filter(
                (Mast_art.resnr == resno)).all():
            db_session.delete(mast_art)

        artikel_list = query(artikel_list_list, first=True)
        while None != artikel_list:
            mast_art = Mast_art()
            db_session.add(mast_art)

            mast_art.resnr = resno
            mast_art.artnr = artikel_list.artnr
            mast_art.departement = artikel_list.departement
            mast_art.reslinnr = 1

            artikel_list = query(artikel_list_list, next=True)
    elif case_type == 2:
        1

    return generate_output()