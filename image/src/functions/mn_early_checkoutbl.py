from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Res_line, Zinrstat

def mn_early_checkoutbl():
    i = 0
    ci_date:date = None
    htparam = res_line = zinrstat = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, res_line, zinrstat


        return {"i": i}

    def early_checkout():

        nonlocal i, ci_date, htparam, res_line, zinrstat

        i:int = 0
        ci_datum:date = None
        ci_datum = ci_date - 1

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_datum) &  (Res_line.zipreis > 0) &  (Res_line.erwachs > 0) &  ((Res_line.ankunft + Res_line.anztage) > ci_datum)).first()
        while None != res_line:
            i = i + 1

            zinrstat = db_session.query(Zinrstat).filter(
                        (func.lower(Zinrstat.zinr) == "Early_CO") &  (Zinrstat.datum == ci_datum)).first()

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = ci_datum
                zinrstat.zinr = "Early_CO"


            zinrstat.zimmeranz = zinrstat.zimmeranz + res_line.zimmeranz
            zinrstat.personen = zinrstat.personen + res_line.erwachs


            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_datum) &  (Res_line.zipreis > 0) &  (Res_line.erwachs > 0) &  ((Res_line.ankunft + Res_line.anztage) > ci_datum)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    early_checkout()

    return generate_output()