#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def gst_init_update_foartikelbl(t_artnr:int, dept:int, bez:string):

    prepare_cache ([Artikel])

    artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel
        nonlocal t_artnr, dept, bez

        return {}


    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, dept)]})

    if artikel:
        artikel.bezeich2 = bez

    return generate_output()