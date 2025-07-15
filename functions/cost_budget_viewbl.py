#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def cost_budget_viewbl():

    prepare_cache ([Htparam])

    from_date = None
    bill_date:date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, bill_date, htparam

        return {"from_date": from_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    from_date = bill_date - timedelta(days=80)
    from_date = date_mdy(get_month(from_date) , 1, get_year(from_date))

    return generate_output()