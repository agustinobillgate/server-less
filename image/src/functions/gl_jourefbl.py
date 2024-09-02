from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Gl_acct, Gl_journal, Htparam

def gl_jourefbl(sorttype:int, from_date:date, to_date:date, from_refno:str):
    output_list_list = []
    gl_jouhdr = gl_acct = gl_journal = htparam = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str, "refno":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, gl_jouhdr, gl_acct, gl_journal, htparam


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def get_bemerk(bemerk:str):

        nonlocal output_list_list, gl_jouhdr, gl_acct, gl_journal, htparam


        nonlocal output_list
        nonlocal output_list_list

        n:int = 0
        s1:str = ""
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk

    def create_list():

        nonlocal output_list_list, gl_jouhdr, gl_acct, gl_journal, htparam


        nonlocal output_list
        nonlocal output_list_list

        debit:decimal = 0
        credit:decimal = 0
        balance:decimal = 0
        konto:str = ""
        i:int = 0
        c:str = ""
        bezeich:str = ""
        datum:date = None
        refno:str = ""
        h_bezeich:str = ""
        id:str = ""
        t_debit:decimal = 0
        t_credit:decimal = 0
        tot_debit:decimal = 0
        tot_credit:decimal = 0
        chgdate:str = ""
        output_list_list.clear()

        if sorttype == 2:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).all():
                balance = 0
                t_debit = 0
                t_credit = 0
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.refno = gl_jouhdr.refno
                STR = "        " + to_string(gl_jouhdr.refno, "x(16)") + to_string(gl_jouhdr.bezeich, "x(30)")

                gl_journal_obj_list = []
                for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                            (Gl_journal.jnr == gl_jouhdr.jnr)).all():
                    if gl_journal._recid in gl_journal_obj_list:
                        continue
                    else:
                        gl_journal_obj_list.append(gl_journal._recid)

                    if gl_journal.chgdate == None:
                        chgdate = ""
                    else:
                        chgdate = to_string(gl_journal.chgdate)
                    c = convert_fibu(gl_acct.fibukonto)
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    STR = to_string(gl_jouhdr.datum) + to_string(c, "x(16)") + to_string(gl_acct.bezeich, "x(30)") + to_string(gl_journal.debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.credit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.userinit, "x(2)") + to_string(gl_journal.sysdate) + to_string(gl_journal.chginit, "x(2)") + to_string(chgdate, "x(8)") + to_string(get_bemerk (gl_journal.bemerk) , "x(100)") + to_string(gl_journal.jnr, ">>>,>>>,>>9")
                    t_debit = t_debit + gl_journal.debit
                    t_credit = t_credit + gl_journal.credit
                    tot_debit = tot_debit + gl_journal.debit
                    tot_credit = tot_credit + gl_journal.credit
                output_list = Output_list()
                output_list_list.append(output_list)

                for i in range(1,40 + 1) :
                    STR = STR + " "
                STR = STR + "T O T A L     " + to_string(t_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,34 + 1) :
                STR = STR + " "
            STR = STR + "GRAND T O T A L     " + to_string(tot_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>>,>>>,>>>,>>>,>>9.99")
        else:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date) &  (func.lower(Gl_jouhdr.refno) == (from_refno).lower())).all():
                balance = 0
                t_debit = 0
                t_credit = 0
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.refno = gl_jouhdr.refno
                STR = "        " + to_string(gl_jouhdr.refno, "x(16)") + to_string(gl_jouhdr.bezeich, "x(30)")

                gl_journal_obj_list = []
                for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                            (Gl_journal.jnr == gl_jouhdr.jnr)).all():
                    if gl_journal._recid in gl_journal_obj_list:
                        continue
                    else:
                        gl_journal_obj_list.append(gl_journal._recid)

                    if gl_journal.chgdate == None:
                        chgdate = ""
                    else:
                        chgdate = to_string(gl_journal.chgdate)
                    c = convert_fibu(gl_acct.fibukonto)
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    STR = to_string(gl_jouhdr.datum) + to_string(c, "x(16)") + to_string(gl_acct.bezeich, "x(30)") + to_string(gl_journal.debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.credit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.userinit, "x(2)") + to_string(gl_journal.sysdate) + to_string(gl_journal.chginit, "x(2)") + to_string(chgdate, "x(8)") + to_string(get_bemerk (gl_journal.bemerk) , "x(100)") + to_string(gl_journal.jnr, ">>>,>>>,>>9")
                    t_debit = t_debit + gl_journal.debit
                    t_credit = t_credit + gl_journal.credit
                    tot_debit = t_debit + gl_journal.debit
                    tot_credit = t_credit + gl_journal.credit
                output_list = Output_list()
                output_list_list.append(output_list)

                for i in range(1,40 + 1) :
                    STR = STR + " "
                STR = STR + "T O T A L     " + to_string(t_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,40 + 1) :
                STR = STR + " "
            STR = STR + "T O T A L     " + to_string(tot_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>>,>>>,>>>,>>>,>>9.99")

    def convert_fibu(konto:str):

        nonlocal output_list_list, gl_jouhdr, gl_acct, gl_journal, htparam


        nonlocal output_list
        nonlocal output_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return s

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 977)).first()
        ch = htparam.fchar
        j = 0
        for i in range(1,len(ch)  + 1) :

            if substring(ch, i - 1, 1) >= "0" and substring(ch, i - 1, 1) <= "9":
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)


        return generate_inner_output()


    create_list()

    return generate_output()