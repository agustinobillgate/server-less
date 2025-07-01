#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Interface

def mn_crm_checkoutbl():

    prepare_cache ([Htparam, Res_line, Interface])

    htparam = res_line = interface = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, res_line, interface

        return {}

    def crm_checkout():

        nonlocal htparam, res_line, interface

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.erwachs > 0)).order_by(Res_line._recid).all():
            interface = Interface()
            db_session.add(interface)

            interface.key = 5
            interface.zinr = res_line.zinr
            interface.nebenstelle = res_line.zinr
            interface.resnr = res_line.resnr
            interface.reslinnr = res_line.reslinnr
            interface.intfield = 0
            interface.int_time = get_current_time_in_seconds()
            interface.intdate = get_current_date()
            interface.parameters = "CRM check-out"


            pass
            pass


    crm_checkout()

    return generate_output()