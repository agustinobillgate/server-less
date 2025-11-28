#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def footnote_admin_update_it_webbl(foot1:string, foot2:string, foot3:string):

    prepare_cache ([Paramtext])

    paramtext = None

    db_session = local_storage.db_session
    foot1 = foot1.strip()
    foot2 = foot2.strip()
    foot3 = foot3.strip()

    def generate_output():
        nonlocal paramtext
        nonlocal foot1, foot2, foot3

        return {}

    def update_it():

        nonlocal paramtext
        nonlocal foot1, foot2, foot3

        # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 711)]})
        paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 711).with_for_update().first()

        if paramtext:
            paramtext.ptexte = foot1
            pass

        # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 712)]})
        paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 712).with_for_update().first()  
        if paramtext:
            paramtext.ptexte = foot2
            pass

        # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 713)]})
        paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 713).with_for_update().first()

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 713
            paramtext.ptexte = foot3
        else:
            pass
            paramtext.ptexte = foot3


    update_it()

    return generate_output()