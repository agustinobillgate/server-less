#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Gl_jouhdr, Gl_journal, Gl_acct

def odoo_list_journalbl(inp_fdate:date, inp_tdate:date):

    prepare_cache ([Queasy, Gl_jouhdr, Gl_journal, Gl_acct])

    counter = 0
    date_char:string = ""
    mapping:string = ""
    jour_desc:string = ""
    queasy = gl_jouhdr = gl_journal = gl_acct = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, date_char, mapping, jour_desc, queasy, gl_jouhdr, gl_journal, gl_acct
        nonlocal inp_fdate, inp_tdate
        nonlocal bqueasy


        nonlocal bqueasy

        return {"counter": counter}

    counter = 0

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= inp_fdate) & (Gl_jouhdr.datum <= inp_tdate)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)],"userinit": [(ne, None),(ne, "")]})

            if gl_acct:

                if num_entries(gl_acct.userinit, ";") >= 2:
                    mapping = trim(entry(1, gl_acct.userinit, ";"))


                else:
                    mapping = trim(entry(0, gl_acct.userinit, ";"))

                if mapping != "":

                    bqueasy = get_cache (Queasy, {"key": [(eq, 345)],"number1": [(eq, gl_jouhdr.jnr)],"date1": [(eq, gl_jouhdr.datum)]})

                    if bqueasy:
                        pass
                        bqueasy.logi1 = True
                        bqueasy.logi2 = False
                        bqueasy.logi3 = False


                        pass
                        pass
                        counter = counter + 1


                    else:
                        bqueasy = Queasy()
                        db_session.add(bqueasy)

                        bqueasy.key = 345
                        bqueasy.number1 = gl_jouhdr.jnr
                        bqueasy.number2 = get_current_time_in_seconds()
                        bqueasy.char1 = gl_jouhdr.bezeich
                        bqueasy.date1 = gl_jouhdr.datum
                        bqueasy.logi1 = True
                        bqueasy.logi2 = False
                        bqueasy.logi3 = False


                        pass
                        counter = counter + 1

    return generate_output()