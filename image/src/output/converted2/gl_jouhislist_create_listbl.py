from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Gl_jourhis, Gl_jhdrhis, Gl_accthis, Htparam

def gl_jouhislist_create_listbl(sorttype:int, from_fibu:str, to_fibu:str, from_dept:int, from_date:date, to_date:date, close_year:date):
    output_list_list = []
    gl_acct = gl_jourhis = gl_jhdrhis = gl_accthis = htparam = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"marked":str, "fibukonto":str, "jnr":int, "bemerk":str, "str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, gl_acct, gl_jourhis, gl_jhdrhis, gl_accthis, htparam
        nonlocal sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year


        nonlocal output_list
        nonlocal output_list_list

        return {"output-list": output_list_list}

    def get_bemerk(bemerk:str):

        nonlocal output_list_list, gl_acct, gl_jourhis, gl_jhdrhis, gl_accthis, htparam
        nonlocal sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year


        nonlocal output_list
        nonlocal output_list_list

        n:int = 0
        s1:str = ""
        bemerk = replace_str(bemerk, chr(10) , " ")
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1


    def create_list():

        nonlocal output_list_list, gl_acct, gl_jourhis, gl_jhdrhis, gl_accthis, htparam
        nonlocal sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year


        nonlocal output_list
        nonlocal output_list_list

        debit:decimal = to_decimal("0.0")
        credit:decimal = to_decimal("0.0")
        balance:decimal = to_decimal("0.0")
        konto:str = ""
        i:int = 0
        c:str = ""
        bezeich:str = ""
        datum:date = None
        refno:str = ""
        h_bezeich:str = ""
        id:str = ""
        chgdate:str = ""
        beg_date:date = None
        beg_day:int = 0
        t_debit:decimal = to_decimal("0.0")
        t_credit:decimal = to_decimal("0.0")
        tot_debit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        e_bal:decimal = to_decimal("0.0")
        delta:decimal = to_decimal("0.0")
        fdate:date = None
        tdate:date = None
        gl_account = None
        gl_jour1 = None
        gl_jouh1 = None
        prev_mm:int = 0
        prev_yr:int = 0
        prev_bal:decimal = to_decimal("0.0")
        end_bal:decimal = to_decimal("0.0")
        blankchar:str = ""
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        Gl_jour1 =  create_buffer("Gl_jour1",Gl_jourhis)
        Gl_jouh1 =  create_buffer("Gl_jouh1",Gl_jhdrhis)
        for i in range(1,72 + 1) :
            blankchar = blankchar + " "
        prev_mm = get_month(from_date) - 1
        prev_yr = get_year(from_date)

        if prev_mm == 0:
            prev_mm = 12
            prev_yr = prev_yr - 1


        beg_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        output_list_list.clear()

        if sorttype == 2:

            gl_jourhis_obj_list = []
            for gl_jourhis, gl_jhdrhis, gl_acct in db_session.query(Gl_jourhis, Gl_jhdrhis, Gl_acct).join(Gl_jhdrhis,(Gl_jhdrhis.jnr == Gl_jourhis.jnr) & (Gl_jhdrhis.datum >= from_date) & (Gl_jhdrhis.datum <= to_date)).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto)).filter(
                         (func.lower(Gl_jourhis.fibukonto) >= (from_fibu).lower()) & (func.lower(Gl_jourhis.fibukonto) <= (to_fibu).lower())).order_by(Gl_jourhis.fibukonto, Gl_jhdrhis.datum, Gl_jhdrhis.refno, func.substring(Gl_jourhis.bemerk, 0, 24)).all():
                if gl_jourhis._recid in gl_jourhis_obj_list:
                    continue
                else:
                    gl_jourhis_obj_list.append(gl_jourhis._recid)

                if gl_jourhis.chgdate == None:
                    chgdate = ""
                else:
                    chgdate = to_string(gl_jourhis.chgdate)

                if konto == "":
                    prev_bal =  to_decimal("0")

                    gl_account = db_session.query(Gl_account).filter(
                                 (Gl_account.fibukonto == gl_acct.fibukonto)).first()

                    if prev_yr < get_year(close_year):

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                     (Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

                        if gl_accthis:
                            prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

                    elif prev_yr == get_year(close_year):
                        prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        prev_bal =  - to_decimal(prev_bal)

                    if gl_account.acc_type == 3 or gl_account.acc_type == 4:
                        balance =  to_decimal(prev_bal)
                    else:
                        balance =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    str = " " + to_string(c, "x(15)") + to_string(gl_acct.bezeich, "x(40)")
                    konto = gl_acct.fibukonto

                if konto != gl_acct.fibukonto:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,30 + 1) :
                        str = str + " "
                    str = str + "T O T A L " + to_string(prev_bal, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99") + blankchar + to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    balance =  to_decimal("0")
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    prev_bal =  to_decimal("0")

                    gl_account = db_session.query(Gl_account).filter(
                                 (Gl_account.fibukonto == gl_acct.fibukonto)).first()

                    if prev_yr < get_year(close_year):

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                     (Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

                        if gl_accthis:
                            prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

                    elif prev_yr == get_year(close_year):
                        prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        prev_bal =  - to_decimal(prev_bal)

                    if gl_account.acc_type == 3 or gl_account.acc_type == 4:
                        balance =  to_decimal(prev_bal)
                    else:
                        balance =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    str = " " + to_string(c, "x(15)") + to_string(gl_acct.bezeich, "x(40)")
                    konto = gl_acct.fibukonto

                gl_account = db_session.query(Gl_account).filter(
                             (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance =  to_decimal(balance) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                else:
                    balance =  to_decimal(balance) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.fibukonto = gl_jourhis.fibukonto
                output_list.jnr = gl_jhdrhis.jnr
                str = to_string(gl_jhdrhis.datum) +\
                        to_string(gl_jhdrhis.refno, "x(15)") +\
                        to_string(gl_jhdrhis.bezeich, "x(40)") +\
                        to_string(gl_jourhis.debit, "->>,>>>,>>>,>>>,>>9.99") +\
                        to_string(gl_jourhis.credit, "->>,>>>,>>>,>>>,>>9.99") +\
                        to_string(gl_jourhis.userinit, "x(3)") +\
                        to_string(gl_jourhis.sysdate) +\
                        to_string(gl_jourhis.chginit, "x(3)") +\
                        to_string(chgdate, "x(8)") +\
                        to_string(get_bemerk (gl_jourhis.bemerk) , "x(50)") +\
                        to_string(balance, "->>,>>>,>>>,>>>,>>9.99")


                output_list.bemerk = get_bemerk (gl_jourhis.bemerk)
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,30 + 1) :
                str = str + " "
            str = str + "T O T A L " + to_string(prev_bal, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99") + blankchar + to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,30 + 1) :
                str = str + " "
            str = str + "GRAND T O T A L " + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")

        elif sorttype == 1:

            gl_jourhis_obj_list = []
            for gl_jourhis, gl_jhdrhis, gl_acct in db_session.query(Gl_jourhis, Gl_jhdrhis, Gl_acct).join(Gl_jhdrhis,(Gl_jhdrhis.jnr == Gl_jourhis.jnr) & (Gl_jhdrhis.datum >= from_date) & (Gl_jhdrhis.datum <= to_date)).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto) & (Gl_acct.main_nr == gl_main.nr)).filter(
                         (func.lower(Gl_jourhis.fibukonto) >= (from_fibu).lower()) & (func.lower(Gl_jourhis.fibukonto) <= (to_fibu).lower())).order_by(Gl_jourhis.fibukonto, Gl_jhdrhis.datum, Gl_jhdrhis.refno, func.substring(Gl_jourhis.bemerk, 0, 24)).all():
                if gl_jourhis._recid in gl_jourhis_obj_list:
                    continue
                else:
                    gl_jourhis_obj_list.append(gl_jourhis._recid)

                if gl_jourhis.chgdate == None:
                    chgdate = ""
                else:
                    chgdate = to_string(gl_jourhis.chgdate)

                if konto == "":
                    prev_bal =  to_decimal("0")

                    gl_account = db_session.query(Gl_account).filter(
                                 (Gl_account.fibukonto == gl_acct.fibukonto)).first()

                    if prev_yr < get_year(close_year):

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                     (Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

                        if gl_accthis:
                            prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

                    elif prev_yr == get_year(close_year):
                        prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        prev_bal =  - to_decimal(prev_bal)

                    if gl_account.acc_type == 3 or gl_account.acc_type == 4:
                        balance =  to_decimal(prev_bal)
                    else:
                        balance =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    str = " " + to_string(c, "x(15)") + to_string(gl_acct.bezeich, "x(40)")
                    konto = gl_acct.fibukonto

                if konto != gl_acct.fibukonto:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,30 + 1) :
                        str = str + " "
                    str = str + "T O T A L " + to_string(prev_bal, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99") + blankchar + to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    balance =  to_decimal("0")
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    prev_bal =  to_decimal("0")

                    gl_account = db_session.query(Gl_account).filter(
                                 (Gl_account.fibukonto == gl_acct.fibukonto)).first()

                    if prev_yr < get_year(close_year):

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                     (Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

                        if gl_accthis:
                            prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

                    elif prev_yr == get_year(close_year):
                        prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        prev_bal =  - to_decimal(prev_bal)

                    if gl_account.acc_type == 3 or gl_account.acc_type == 4:
                        balance =  to_decimal(prev_bal)
                    else:
                        balance =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    str = " " + to_string(c, "x(15)") + to_string(gl_acct.bezeich, "x(40)")
                    konto = gl_acct.fibukonto

                gl_account = db_session.query(Gl_account).filter(
                             (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance =  to_decimal(balance) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                else:
                    balance =  to_decimal(balance) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.fibukonto = gl_jourhis.fibukonto
                output_list.jnr = gl_jhdrhis.jnr
                str = to_string(gl_jhdrhis.datum) +\
                        to_string(gl_jhdrhis.refno, "x(15)") +\
                        to_string(gl_jhdrhis.bezeich, "x(40)") +\
                        to_string(gl_jourhis.debit, "->>,>>>,>>>,>>>,>>9.99") +\
                        to_string(gl_jourhis.credit, "->>,>>>,>>>,>>>,>>9.99") +\
                        to_string(gl_jourhis.userinit, "x(3)") +\
                        to_string(gl_jourhis.sysdate) +\
                        to_string(gl_jourhis.chginit, "x(3)") +\
                        to_string(chgdate, "x(8)") +\
                        to_string(get_bemerk (gl_jourhis.bemerk) , "x(50)") +\
                        to_string(balance, "->>,>>>,>>>,>>>,>>9.99")


                output_list.bemerk = get_bemerk (gl_jourhis.bemerk)
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,30 + 1) :
                str = str + " "
            str = str + "T O T A L " + to_string(prev_bal, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99") + blankchar + to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,30 + 1) :
                str = str + " "
            str = str + "GRAND T O T A L " + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")

        elif sorttype == 3:

            gl_jourhis_obj_list = []
            for gl_jourhis, gl_jhdrhis, gl_acct in db_session.query(Gl_jourhis, Gl_jhdrhis, Gl_acct).join(Gl_jhdrhis,(Gl_jhdrhis.jnr == Gl_jourhis.jnr) & (Gl_jhdrhis.datum >= from_date) & (Gl_jhdrhis.datum <= to_date)).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto) & (Gl_acct.deptnr == from_dept)).filter(
                         (func.lower(Gl_jourhis.fibukonto) >= (from_fibu).lower()) & (func.lower(Gl_jourhis.fibukonto) <= (to_fibu).lower())).order_by(Gl_jourhis.fibukonto, Gl_jhdrhis.datum, Gl_jhdrhis.refno, func.substring(Gl_jourhis.bemerk, 0, 24)).all():
                if gl_jourhis._recid in gl_jourhis_obj_list:
                    continue
                else:
                    gl_jourhis_obj_list.append(gl_jourhis._recid)

                if gl_jourhis.chgdate == None:
                    chgdate = ""
                else:
                    chgdate = to_string(gl_jourhis.chgdate)

                if konto == "":
                    prev_bal =  to_decimal("0")

                    gl_account = db_session.query(Gl_account).filter(
                                 (Gl_account.fibukonto == gl_acct.fibukonto)).first()

                    if prev_yr < get_year(close_year):

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                     (Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

                        if gl_accthis:
                            prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

                    elif prev_yr == get_year(close_year):
                        prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        prev_bal =  - to_decimal(prev_bal)

                    if gl_account.acc_type == 3 or gl_account.acc_type == 4:
                        balance =  to_decimal(prev_bal)
                    else:
                        balance =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    str = " " + to_string(c, "x(15)") + to_string(gl_acct.bezeich, "x(40)")
                    konto = gl_acct.fibukonto

                if konto != gl_acct.fibukonto:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,30 + 1) :
                        str = str + " "
                    str = str + "T O T A L " + to_string(prev_bal, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99") + blankchar + to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    balance =  to_decimal("0")
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    prev_bal =  to_decimal("0")

                    gl_account = db_session.query(Gl_account).filter(
                                 (Gl_account.fibukonto == gl_acct.fibukonto)).first()

                    if prev_yr < get_year(close_year):

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                     (Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

                        if gl_accthis:
                            prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

                    elif prev_yr == get_year(close_year):
                        prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        prev_bal =  - to_decimal(e_bal)

                    if gl_account.acc_type == 3 or gl_account.acc_type == 4:
                        balance =  to_decimal(prev_bal)
                    else:
                        balance =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    str = " " + to_string(c, "x(15)") + to_string(gl_acct.bezeich, "x(40)")
                    konto = gl_acct.fibukonto

                gl_account = db_session.query(Gl_account).filter(
                             (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance =  to_decimal(balance) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                else:
                    balance =  to_decimal(balance) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.fibukonto = gl_jourhis.fibukonto
                output_list.jnr = gl_jhdrhis.jnr
                str = to_string(gl_jhdrhis.datum) +\
                        to_string(gl_jhdrhis.refno, "x(15)") +\
                        to_string(gl_jhdrhis.bezeich, "x(40)") +\
                        to_string(gl_jourhis.debit, "->>,>>>,>>>,>>>,>>9.99") +\
                        to_string(gl_jourhis.credit, "->>,>>>,>>>,>>>,>>9.99") +\
                        to_string(gl_jourhis.userinit, "x(3)") +\
                        to_string(gl_jourhis.sysdate) +\
                        to_string(gl_jourhis.chginit, "x(3)") +\
                        to_string(chgdate, "x(8)") +\
                        to_string(get_bemerk (gl_jourhis.bemerk) , "x(50)") +\
                        to_string(balance, "->>,>>>,>>>,>>>,>>9.99")


                output_list.bemerk = get_bemerk (gl_jourhis.bemerk)
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,30 + 1) :
                str = str + " "
            str = str + "T O T A L " + to_string(prev_bal, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99") + blankchar + to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,30 + 1) :
                str = str + " "
            str = str + "GRAND T O T A L " + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99") + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")


    def convert_fibu(konto:str):

        nonlocal output_list_list, gl_acct, gl_jourhis, gl_jhdrhis, gl_accthis, htparam
        nonlocal sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year


        nonlocal output_list
        nonlocal output_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 977)).first()

        if htparam:
            ch = htparam.fchar
        j = 0
        for i in range(1,len(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()

    create_list()

    return generate_output()