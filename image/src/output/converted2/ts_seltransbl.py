#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Guest, Artikel

def ts_seltransbl(combo_pf_file1:string, combo_pf_file2:string, combo_gastnr:int, combo_ledger:int):

    prepare_cache ([Htparam, Guest])

    rest_flag = False
    hogatex_flag = False
    integer_flag = 0
    htparam = guest = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest_flag, hogatex_flag, integer_flag, htparam, guest, artikel
        nonlocal combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger

        return {"rest_flag": rest_flag, "hogatex_flag": hogatex_flag, "integer_flag": integer_flag, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})
    rest_flag = (htparam.finteger == 1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 300)]})
    hogatex_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 888)]})
    integer_flag = htparam.finteger

    if combo_gastnr == None:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 155)]})
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:

            guest = get_cache (Guest, {"gastnr": [(eq, combo_gastnr)]})

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, combo_ledger)],"departement": [(eq, 0)],"artart": [(eq, 2)]})

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0


            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 339)]})
        combo_pf_file1 = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 340)]})
        combo_pf_file2 = htparam.fchar

    return generate_output()