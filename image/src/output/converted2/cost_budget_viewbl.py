from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def cost_budget_viewbl():
    from_date = None
    bill_date:date = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, bill_date, htparam


        return {"from_date": from_date}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    from_date = bill_date - timedelta(days=80)
    from_date = date_mdy(get_month(from_date) , 1, get_year(from_date))

    return generate_output()