#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def footnote_admin_fill_list_webbl():

    prepare_cache ([Paramtext])

    foot1 = ""
    foot2 = ""
    foot3 = ""
    paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal foot1, foot2, foot3, paramtext

        return {"foot1": foot1, "foot2": foot2, "foot3": foot3}

    def fill_list():

        nonlocal foot1, foot2, foot3, paramtext

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 711)]})

        if paramtext:
            foot1 = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 712)]})

        if paramtext:
            foot2 = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 713)]})

        if paramtext:
            foot3 = paramtext.ptexte


    fill_list()

    return generate_output()