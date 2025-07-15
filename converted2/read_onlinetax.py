#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Nitehist, Nightaudit

def read_onlinetax(curr_date:date):

    prepare_cache ([Nitehist, Nightaudit])

    already_read = False
    online_tax_data = []
    bill_date:date = None
    reihenfolge:int = 0
    nitehist = nightaudit = None

    online_tax = nbuff = None

    online_tax_data, Online_tax = create_model("Online_tax", {"line_nr":int, "ct":string, "departement":int})

    Nbuff = create_buffer("Nbuff",Nitehist)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal already_read, online_tax_data, bill_date, reihenfolge, nitehist, nightaudit
        nonlocal curr_date
        nonlocal nbuff


        nonlocal online_tax, nbuff
        nonlocal online_tax_data

        return {"already_read": already_read, "online-tax": online_tax_data}

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, "nt-onlinetax.p")]})

    if not nightaudit:

        return generate_output()
    bill_date = get_output(htpdate(110))

    if curr_date == 01/01/2000:
        curr_date = bill_date - timedelta(days=1)

    nitehist = get_cache (Nitehist, {"datum": [(eq, curr_date)],"reihenfolge": [(eq, nightaudit.reihenfolge)],"line": [(eq, "end-of-record")]})

    if not nitehist:

        return generate_output()

    elif nitehist and nitehist.line_nr == 99999999:
        already_read = True

        return generate_output()

    for nitehist in db_session.query(Nitehist).filter(
             (Nitehist.datum == curr_date) & (Nitehist.reihenfolge == nightaudit.reihenfolge)).order_by(nitehist.line_nr).yield_per(100):

        if nitehist.line.lower()  == ("END-OF-RECORD").lower() :

            nbuff = get_cache (Nitehist, {"_recid": [(eq, nitehist._recid)]})
            nbuff.line_nr = 99999999


            pass
            break
        online_tax = Online_tax()
        online_tax_data.append(online_tax)

        online_tax.line_nr = nitehist.line_nr
        online_tax.ct = entry(0, nitehist.line , chr_unicode(2))
        online_tax.departement = to_int(entry(1, nitehist.line , chr_unicode(2)))

    return generate_output()