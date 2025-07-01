#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Zinrstat

def mn_early_checkoutbl():

    prepare_cache ([Htparam, Zinrstat])

    i = 0
    ci_date:date = None
    htparam = res_line = zinrstat = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, res_line, zinrstat

        return {"i": i}

    def early_checkout():

        nonlocal ci_date, htparam, res_line, zinrstat

        i:int = 0
        ci_datum:date = None
        ci_datum = ci_date - timedelta(days=1)

        res_line = get_cache (Res_line, {"active_flag": [(eq, 2)],"resstatus": [(eq, 8)],"abreise": [(eq, ci_datum)],"zipreis": [(gt, 0)],"erwachs": [(gt, 0)],"anztage ": [(gt, ci_datum)]})
        while None != res_line:
            i = i + 1

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "early-co")],"datum": [(eq, ci_datum)]})

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = ci_datum
                zinrstat.zinr = "Early-CO"


            zinrstat.zimmeranz = zinrstat.zimmeranz + res_line.zimmeranz
            zinrstat.personen = zinrstat.personen + res_line.erwachs

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_datum) & (Res_line.zipreis > 0) & (Res_line.erwachs > 0) & ((Res_line.ankunft + Res_line.anztage) > ci_datum) & (Res_line._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    early_checkout()

    return generate_output()