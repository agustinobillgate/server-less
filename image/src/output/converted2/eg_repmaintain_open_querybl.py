#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_maintain

def eg_repmaintain_open_querybl(fdate:date, tdate:date):
    t_eg_maintain_list = []
    eg_maintain = None

    t_eg_maintain = None

    t_eg_maintain_list, T_eg_maintain = create_model_like(Eg_maintain)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_maintain_list, eg_maintain
        nonlocal fdate, tdate


        nonlocal t_eg_maintain
        nonlocal t_eg_maintain_list

        return {"t-eg-maintain": t_eg_maintain_list}

    for eg_maintain in db_session.query(Eg_maintain).filter(
             (Eg_maintain.estworkdate >= fdate) & (Eg_maintain.estworkdate <= tdate) & not_ (Eg_maintain.delete_flag)).order_by(Eg_maintain._recid).all():
        t_eg_maintain = T_eg_maintain()
        t_eg_maintain_list.append(t_eg_maintain)

        buffer_copy(eg_maintain, t_eg_maintain)

    return generate_output()