#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept

def chg_rezeipt_btn_gobl(rec_id:int, katnr:int, portion:int, h_bezeich:string, katbezeich:string):

    prepare_cache ([H_rezept])

    h_rezept = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept
        nonlocal rec_id, katnr, portion, h_bezeich, katbezeich

        return {}


    h_rezept = get_cache (H_rezept, {"_recid": [(eq, rec_id)]})
    pass
    h_rezept.portion = portion
    h_rezept.datummod = get_current_date()

    if katnr != h_rezept.kategorie or to_string(h_bezeich, "x(24)") != substring(h_rezept.bezeich, 0, 24):
        h_rezept.kategorie = katnr
        h_rezept.bezeich = to_string(h_bezeich, "x(24)") + katbezeich
    pass

    return generate_output()