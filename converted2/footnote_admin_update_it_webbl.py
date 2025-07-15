#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def footnote_admin_update_it_webbl(foot1:string, foot2:string, foot3:string):

    prepare_cache ([Paramtext])

    paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal paramtext
        nonlocal foot1, foot2, foot3

        return {}

    def update_it():

        nonlocal paramtext
        nonlocal foot1, foot2, foot3

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 711)]})

        if paramtext:
            paramtext.ptexte = foot1
            pass

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 712)]})

        if paramtext:
            paramtext.ptexte = foot2
            pass

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 713)]})

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 713
            paramtext.ptexte = foot3
        else:
            pass
            paramtext.ptexte = foot3
            pass
            pass


    update_it()

    return generate_output()