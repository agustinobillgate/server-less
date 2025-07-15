#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Nitehist, Nightaudit

def delete_onlinetaxbl(fr_date:date, to_date:date):

    prepare_cache ([Nightaudit])

    curr_date:date = None
    bill_date:date = None
    nitehist = nightaudit = None

    nbuff = None

    Nbuff = create_buffer("Nbuff",Nitehist)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, bill_date, nitehist, nightaudit
        nonlocal fr_date, to_date
        nonlocal nbuff


        nonlocal nbuff

        return {}

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, "nt-onlinetax.p")]})

    if not nightaudit:

        return generate_output()
    bill_date = get_output(htpdate(110))

    if curr_date == 01/01/2000:
        curr_date = bill_date - timedelta(days=1)
    for curr_date in date_range(fr_date,to_date) :

        nitehist = get_cache (Nitehist, {"datum": [(eq, curr_date)],"reihenfolge": [(eq, nightaudit.reihenfolge)],"line": [(eq, "end-of-record")]})

        if not nitehist:

            return generate_output()

        nitehist = get_cache (Nitehist, {"datum": [(eq, curr_date)],"reihenfolge": [(eq, nightaudit.reihenfolge)]})
        while None != nitehist:

            nbuff = db_session.query(Nbuff).filter(
                     (Nbuff._recid == nitehist._recid)).first()
            db_session.delete(nbuff)
            pass

            curr_recid = nitehist._recid
            nitehist = db_session.query(Nitehist).filter(
                     (Nitehist.datum == curr_date) & (Nitehist.reihenfolge == nightaudit.reihenfolge) & (Nitehist._recid > curr_recid)).first()

    return generate_output()