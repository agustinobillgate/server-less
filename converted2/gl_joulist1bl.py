#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_journal

out_list_data, Out_list = create_model("Out_list", {"s_recid":int, "marked":string, "fibukonto":string, "jnr":int, "jtype":int, "bemerk":string, "trans_date":date, "bezeich":string, "number1":string, "debit":Decimal, "credit":Decimal, "balance":Decimal, "debit_str":string, "credit_str":string, "balance_str":string, "refno":string, "uid":string, "created":date, "chgid":string, "chgdate":date, "tax_code":string, "tax_amount":string, "tot_amt":string, "approved":bool, "prev_bal":string})

def gl_joulist1bl(out_list_data:[Out_list]):

    prepare_cache ([Gl_journal])

    gl_journal = None

    out_list = g_jour = None

    G_jour = create_buffer("G_jour",Gl_journal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_journal
        nonlocal g_jour


        nonlocal out_list, g_jour

        return {}

    for out_list in query(out_list_data):

        gl_journal = get_cache (Gl_journal, {"_recid": [(eq, out_list.s_recid)]})

        if gl_journal:

            g_jour = get_cache (Gl_journal, {"_recid": [(eq, gl_journal._recid)]})

            if num_entries(g_jour.bemerk, chr_unicode(2)) > 1:
                g_jour.bemerk = entry(1, g_jour.bemerk, chr_unicode(2), out_list.number1)


            else:
                g_jour.bemerk = g_jour.bemerk + chr_unicode(2) + out_list.number1


            pass
            pass

    return generate_output()