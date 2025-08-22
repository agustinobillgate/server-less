#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 2/8/2025
# GL by voucher kosong
# " " -> "        "  , str -> output_list.str
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Gl_jhdrhis, Gl_acct, Gl_jourhis, Gl_journal, Htparam

def gl_jourefbl(sorttype:int, from_date:date, to_date:date, from_refno:string):

    prepare_cache ([Gl_jouhdr, Gl_jhdrhis, Gl_acct, Gl_jourhis, Gl_journal, Htparam])

    output_list_data = []
    gl_jouhdr = gl_jhdrhis = gl_acct = gl_jourhis = gl_journal = htparam = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string, "refno":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, gl_jouhdr, gl_jhdrhis, gl_acct, gl_jourhis, gl_journal, htparam
        nonlocal sorttype, from_date, to_date, from_refno


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def get_bemerk(bemerk:string):

        nonlocal output_list_data, gl_jouhdr, gl_jhdrhis, gl_acct, gl_jourhis, gl_journal, htparam
        nonlocal sorttype, from_date, to_date, from_refno


        nonlocal output_list
        nonlocal output_list_data

        n:int = 0
        s1:string = ""
        n = get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk


    def create_list():

        nonlocal output_list_data, gl_jouhdr, gl_jhdrhis, gl_acct, gl_jourhis, gl_journal, htparam
        nonlocal sorttype, from_date, to_date, from_refno


        nonlocal output_list
        nonlocal output_list_data

        debit:Decimal = to_decimal("0.0")
        credit:Decimal = to_decimal("0.0")
        balance:Decimal = to_decimal("0.0")
        konto:string = ""
        i:int = 0
        c:string = ""
        bezeich:string = ""
        datum:date = None
        refno:string = ""
        h_bezeich:string = ""
        id:string = ""
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        chgdate:string = ""
        output_list_data.clear()

        if sorttype == 2:

            gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(ge, from_date),(le, to_date)]})

            if not gl_jouhdr:

                for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter(
                             (Gl_jhdrhis.datum >= from_date) & (Gl_jhdrhis.datum <= to_date)).order_by(Gl_jhdrhis.datum, Gl_jhdrhis.refno).all():
                    balance =  to_decimal("0")
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.refno = gl_jhdrhis.refno
                    output_list.str = "        " + to_string(gl_jhdrhis.refno, "x(30)") + to_string(gl_jhdrhis.bezeich, "x(30)")

                    gl_jourhis_obj_list = {}
                    gl_jourhis = Gl_jourhis()
                    gl_acct = Gl_acct()
                    for gl_jourhis.chgdate, gl_jourhis.debit, gl_jourhis.credit, gl_jourhis.userinit, gl_jourhis.sysdate, gl_jourhis.chginit, gl_jourhis.bemerk, gl_jourhis.jnr, gl_jourhis._recid, gl_acct.fibukonto, gl_acct.bezeich, gl_acct._recid in db_session.query(Gl_jourhis.chgdate, Gl_jourhis.debit, Gl_jourhis.credit, Gl_jourhis.userinit, Gl_jourhis.sysdate, Gl_jourhis.chginit, Gl_jourhis.bemerk, Gl_jourhis.jnr, Gl_jourhis._recid, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct._recid).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto)).filter(
                                 (Gl_jourhis.jnr == gl_jhdrhis.jnr)).order_by(Gl_jourhis.fibukonto).all():
                        if gl_jourhis_obj_list.get(gl_jourhis._recid):
                            continue
                        else:
                            gl_jourhis_obj_list[gl_jourhis._recid] = True

                        if gl_jourhis.chgdate == None:
                            chgdate = ""
                        else:
                            chgdate = to_string(gl_jourhis.chgdate)
                        c = convert_fibu(gl_acct.fibukonto)
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.str = to_string(gl_jhdrhis.datum) + to_string(c, "x(30)") + to_string(gl_acct.bezeich, "x(30)") + to_string(gl_jourhis.debit, "->>>,>>>,>>>,>>>,>>9.99") + \
                                to_string(gl_jourhis.credit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_jourhis.userinit, "x(2)") + to_string(gl_jourhis.sysdate) + \
                                to_string(gl_jourhis.chginit, "x(2)") + to_string(chgdate, "x(8)") + to_string(get_bemerk (gl_jourhis.bemerk) , "x(100)") + \
                                to_string(gl_jourhis.jnr, ">>>,>>>,>>9")
                        
                        t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                        t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1,54 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + "T O T A L     " + to_string(t_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_data.append(output_list)

            else:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                             (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno).all():

                    if gl_jouhdr:
                        balance =  to_decimal("0")
                        t_debit =  to_decimal("0")
                        t_credit =  to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.refno = gl_jouhdr.refno
                        output_list.str = "        " + to_string(gl_jouhdr.refno, "x(30)") + to_string(gl_jouhdr.bezeich, "x(30)")

                        gl_journal_obj_list = {}
                        gl_journal = Gl_journal()
                        gl_acct = Gl_acct()
                        for gl_journal.chgdate, gl_journal.debit, gl_journal.credit, gl_journal.userinit, gl_journal.sysdate, gl_journal.chginit, gl_journal.bemerk, gl_journal.jnr, gl_journal._recid, gl_acct.fibukonto, gl_acct.bezeich, gl_acct._recid in db_session.query(Gl_journal.chgdate, Gl_journal.debit, Gl_journal.credit, Gl_journal.userinit, Gl_journal.sysdate, Gl_journal.chginit, Gl_journal.bemerk, Gl_journal.jnr, Gl_journal._recid, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct._recid).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal.fibukonto).all():
                            if gl_journal_obj_list.get(gl_journal._recid):
                                continue
                            else:
                                gl_journal_obj_list[gl_journal._recid] = True

                            if gl_journal.chgdate == None:
                                chgdate = ""
                            else:
                                chgdate = to_string(gl_journal.chgdate)
                            c = convert_fibu(gl_acct.fibukonto)
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.str = to_string(gl_jouhdr.datum) + to_string(c, "x(30)") + to_string(gl_acct.bezeich, "x(30)") + to_string(gl_journal.debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.credit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.userinit, "x(2)") + to_string(gl_journal.sysdate) + to_string(gl_journal.chginit, "x(2)") + to_string(chgdate, "x(8)") + to_string(get_bemerk (gl_journal.bemerk) , "x(100)") + to_string(gl_journal.jnr, ">>>,>>>,>>9")
                            t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                            t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                            tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                            tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1,54 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L     " + to_string(t_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,48 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND T O T A L     " + to_string(tot_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>>,>>>,>>>,>>>,>>9.99")
        else:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.refno == (from_refno).lower())).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno).all():
                balance =  to_decimal("0")
                t_debit =  to_decimal("0")
                t_credit =  to_decimal("0")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.refno = gl_jouhdr.refno
                output_list.str = "        " + to_string(gl_jouhdr.refno, "x(30)") + to_string(gl_jouhdr.bezeich, "x(30)")

                gl_journal_obj_list = {}
                gl_journal = Gl_journal()
                gl_acct = Gl_acct()
                for gl_journal.chgdate, gl_journal.debit, gl_journal.credit, gl_journal.userinit, gl_journal.sysdate, gl_journal.chginit, gl_journal.bemerk, gl_journal.jnr, gl_journal._recid, gl_acct.fibukonto, gl_acct.bezeich, gl_acct._recid in db_session.query(Gl_journal.chgdate, Gl_journal.debit, Gl_journal.credit, Gl_journal.userinit, Gl_journal.sysdate, Gl_journal.chginit, Gl_journal.bemerk, Gl_journal.jnr, Gl_journal._recid, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct._recid).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal.fibukonto).all():
                    if gl_journal_obj_list.get(gl_journal._recid):
                        continue
                    else:
                        gl_journal_obj_list[gl_journal._recid] = True

                    if gl_journal.chgdate == None:
                        chgdate = ""
                    else:
                        chgdate = to_string(gl_journal.chgdate)
                    c = convert_fibu(gl_acct.fibukonto)
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = to_string(gl_jouhdr.datum) + to_string(c, "x(30)") + to_string(gl_acct.bezeich, "x(30)") + to_string(gl_journal.debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.credit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(gl_journal.userinit, "x(2)") + to_string(gl_journal.sysdate) + to_string(gl_journal.chginit, "x(2)") + to_string(chgdate, "x(8)") + to_string(get_bemerk (gl_journal.bemerk) , "x(100)") + to_string(gl_journal.jnr, ">>>,>>>,>>9")
                    t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                    t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                    tot_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                    tot_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                output_list = Output_list()
                output_list_data.append(output_list)

                for i in range(1,54 + 1) :
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + "T O T A L " + to_string(t_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,54 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L " + to_string(tot_debit, "->>>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>>,>>>,>>>,>>>,>>9.99")


    def convert_fibu(konto:string):

        nonlocal output_list_data, gl_jouhdr, gl_jhdrhis, gl_acct, gl_jourhis, gl_journal, htparam
        nonlocal sorttype, from_date, to_date, from_refno


        nonlocal output_list
        nonlocal output_list_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()

    create_list()

    return generate_output()