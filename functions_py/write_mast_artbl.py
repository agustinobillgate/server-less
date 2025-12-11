#using conversion tools version: 1.0.0.117

# ===========================================
# Rulita, 11-12-2025
# - Added with_for_update before delete query
# ===========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Mast_art

artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})

def write_mast_artbl(case_type:int, resno:int, artikel_list_data:[Artikel_list]):
    mast_art = None

    artikel_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mast_art
        nonlocal case_type, resno


        nonlocal artikel_list

        return {}

    if case_type == 1:

        for mast_art in db_session.query(Mast_art).filter(
                 (Mast_art.resnr == resno)).order_by(Mast_art._recid).with_for_update().all():
            db_session.delete(mast_art)

        # change query -> for loop
        #------------------------------
        # artikel_list = query(artikel_list_data, first=True)
        # while None != artikel_list:
        #     mast_art = Mast_art()
        #     db_session.add(mast_art)

        #     mast_art.resnr = resno
        #     mast_art.artnr = artikel_list.artnr
        #     mast_art.departement = artikel_list.departement
        #     mast_art.reslinnr = 1

        #     artikel_list = query(artikel_list_data, next=True)

        for artikel_list in artikel_list_data:
            mast_art = Mast_art()
            db_session.add(mast_art)

            mast_art.resnr = resno
            mast_art.artnr = artikel_list.artnr
            mast_art.departement = artikel_list.departement
            mast_art.reslinnr = 1
        

    elif case_type == 2:
        pass

    return generate_output()