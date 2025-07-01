#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Guest, Artikel

def prepare_gl_linkar_1bl(combo_pf_file1:string, combo_pf_file2:string, combo_gastnr:int, combo_ledger:int, combo_gl_link:bool):

    prepare_cache ([Htparam, Guest])

    f_int = 0
    last_acctdate = None
    from_date = None
    acct_date = None
    close_year = None
    msg_str = ""
    last_acct_period:date = None
    htparam = guest = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, last_acctdate, from_date, acct_date, close_year, msg_str, last_acct_period, htparam, guest, artikel
        nonlocal combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger, combo_gl_link

        return {"f_int": f_int, "last_acctdate": last_acctdate, "from_date": from_date, "acct_date": acct_date, "close_year": close_year, "msg_str": msg_str, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger, "combo_gl_link": combo_gl_link}


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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 343)]})
        combo_gl_link = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1014)]})
    last_acctdate = htparam.fdate
    from_date = last_acctdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    acct_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_acct_period = htparam.fdate

    if from_date <= last_acct_period:
        msg_str = "Last AR transfer to GL (Param 1014) lower THEN last accounting closing period (Param 558)." + chr_unicode(10) + "Transfer to GL not possible."

        return generate_output()

    return generate_output()