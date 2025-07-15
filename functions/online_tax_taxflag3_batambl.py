#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_onlinetax import read_onlinetax
from functions.delete_onlinetaxbl import delete_onlinetaxbl
from functions.nt_onlinetax_batam_billdate_manual import nt_onlinetax_batam_billdate_manual
from functions.if_read_onlinetax_mbl import if_read_onlinetax_mbl

def online_tax_taxflag3_batambl(curr_date:date):
    already_read = False
    online_tax_data = []
    avail_flag = False

    online_tax = None

    online_tax_data, Online_tax = create_model("Online_tax", {"line_nr":int, "ct":string, "departement":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal already_read, online_tax_data, avail_flag
        nonlocal curr_date


        nonlocal online_tax
        nonlocal online_tax_data

        return {"already_read": already_read, "online-tax": online_tax_data, "avail_flag": avail_flag}


    already_read, online_tax_data = get_output(read_onlinetax(curr_date))

    online_tax = query(online_tax_data, first=True)

    if not online_tax:
        get_output(delete_onlinetaxbl(curr_date, curr_date))
        avail_flag = get_output(nt_onlinetax_batam_billdate_manual(curr_date, curr_date))
        get_output(if_read_onlinetax_mbl(curr_date))
        already_read, online_tax_data = get_output(read_onlinetax(curr_date))

        online_tax = query(online_tax_data, first=True)

        if not online_tax:

            return generate_output()

    return generate_output()