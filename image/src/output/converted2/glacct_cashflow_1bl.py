from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Gl_acct, Gl_accthis, Gl_journal, Gl_jouhdr

coa_list_list, Coa_list = create_model("Coa_list", {"fibu":str})

def glacct_cashflow_1bl(from_date:date, to_date:date, from_lsyr:date, to_lsyr:date, pfrom_date:date, pto_date:date, from_month:date, from_year:date, coa_list_list:[Coa_list]):
    t_list_list = []
    close_month:date = None
    close_year:date = None
    last_close_yr:date = None
    prev_month:int = 0
    gl_acct = gl_accthis = gl_journal = gl_jouhdr = None

    coa_list = t_list = tbuff = None

    t_list_list, T_list = create_model("T_list", {"cf":int, "fibukonto":str, "debit":decimal, "credit":decimal, "debit_lsyear":decimal, "credit_lsyear":decimal, "debit_lsmonth":decimal, "credit_lsmonth":decimal, "balance":decimal, "ly_balance":decimal, "pm_balance":decimal, "debit_today":decimal, "credit_today":decimal, "debit_mtd":decimal, "credit_mtd":decimal, "debit_ytd":decimal, "credit_ytd":decimal, "today_balance":decimal, "mtd_balance":decimal, "ytd_balance":decimal})

    Tbuff = T_list
    tbuff_list = t_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, close_month, close_year, last_close_yr, prev_month, gl_acct, gl_accthis, gl_journal, gl_jouhdr
        nonlocal from_date, to_date, from_lsyr, to_lsyr, pfrom_date, pto_date, from_month, from_year
        nonlocal tbuff


        nonlocal coa_list, t_list, tbuff
        nonlocal t_list_list

        return {"t-list": t_list_list}

    def calc_balance(i_case:int, fibu:str, from_date:date, to_date:date):

        nonlocal t_list_list, close_month, close_year, last_close_yr, prev_month, gl_acct, gl_accthis, gl_journal, gl_jouhdr
        nonlocal from_lsyr, to_lsyr, pfrom_date, pto_date, from_month, from_year
        nonlocal tbuff


        nonlocal coa_list, t_list, tbuff
        nonlocal t_list_list

        p_bal:decimal = to_decimal("0.0")
        debit:decimal = to_decimal("0.0")
        credit:decimal = to_decimal("0.0")
        date1:date = None
        date2:date = None
        p_sign:int = 1
        i_cf:int = None
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Gl_acct)

        gbuff = db_session.query(Gbuff).filter(
                 (func.lower(Gbuff.fibukonto) == (fibu).lower())).first()

        if not gbuff:

            return

        if from_date > close_month:

            return

        if gbuff.acc_type == 1 or gbuff.acc_type == 4:
            p_sign = -1

        if gbuff.acc_type == 3 or gbuff.acc_type == 4:

            if get_year(close_year) == get_year(close_month):

                if get_year(from_date) == get_year(close_month):

                    if get_month(from_date) == 1:
                        p_bal =  to_decimal(gbuff.last_yr[11])


                    else:
                        p_bal =  to_decimal(gbuff.actual[prev_month - 1])


                else:

                    gl_accthis = db_session.query(Gl_accthis).filter(
                             (func.lower(Gl_accthis.fibukonto) == (fibu).lower()) & (Gl_accthis.year == get_year(from_date))).first()

                    if not gl_accthis:

                        return

                    if get_month(from_date) == 1:
                        p_bal =  to_decimal(gl_accthis.last_yr[11])


                    else:
                        p_bal =  to_decimal(gl_accthis.actual[prev_month - 1])

            elif get_year(close_year) < get_year(close_month):

                if get_year(from_date) == get_year(close_month):

                    if get_month(from_date) == 1:
                        p_bal =  to_decimal(gbuff.last_yr[11])


                    else:
                        p_bal =  to_decimal(gbuff.actual[prev_month - 1])

                elif get_year(from_date) == (get_year(close_month) - 1):

                    if get_month(from_date) >= 2:
                        p_bal =  to_decimal(gbuff.last_yr[prev_month - 1])


                    else:

                        gl_accthis = db_session.query(Gl_accthis).filter(
                                 (func.lower(Gl_accthis.fibukonto) == (fibu).lower()) & (Gl_accthis.year == get_year(from_date) - 1)).first()

                        if not gl_accthis:

                            return
                        p_bal =  to_decimal(gl_accthis.actual[11])


                else:

                    gl_accthis = db_session.query(Gl_accthis).filter(
                             (func.lower(Gl_accthis.fibukonto) == (fibu).lower()) & (Gl_accthis.year == get_year(from_date))).first()

                    if not gl_accthis:

                        return

                    if get_month(from_date) == 1:
                        p_bal =  to_decimal(gl_accthis.last_yr[11])


                    else:
                        p_bal =  to_decimal(gl_accthis.actual[prev_month - 1])

        if get_day(from_date) >= 2 and (gbuff.acc_type == 3 or gbuff.acc_type == 4):
            date1 = date_mdy(get_month(from_date) , 1, get_year(from_date))
            date2 = date_mdy(get_month(from_date) , get_day(from_date) - timedelta(days=1, get_year(from_date)))

            for gl_jouhdr, gl_journal in db_session.query(Gl_jouhdr, Gl_journal).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) & (func.lower(Gl_journal.fibukonto) == (fibu).lower())).filter(
                     (Gl_jouhdr.datum >= date1) & (Gl_jouhdr.datum <= date2)).order_by(Gl_jouhdr._recid).all():
                p_bal =  to_decimal(p_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

        if i_case == 1:
            tbuff.balance =  to_decimal(p_bal)
        elif i_case == 2:
            tbuff.ly_balance =  to_decimal(p_bal)
        elif i_case == 3:
            tbuff.pm_balance =  to_decimal(p_bal)
        elif i_case == 3:
            tbuff.today_balance =  to_decimal(p_bal)
        elif i_case == 5:
            tbuff.mtd_balance =  to_decimal(p_bal)
        elif i_case == 6:
            tbuff.ytd_balance =  to_decimal(p_bal)
        date1 = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date))
        date2 = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date))

        for gl_jouhdr, gl_journal in db_session.query(Gl_jouhdr, Gl_journal).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) & (func.lower(Gl_journal.fibukonto) == (fibu).lower())).filter(
                 (Gl_jouhdr.datum >= date1) & (Gl_jouhdr.datum <= date2)).order_by(Gl_jouhdr._recid).all():
            credit =  to_decimal(gl_journal.credit)
            debit =  to_decimal(gl_journal.debit)
            i_cf = None
            i_cf = to_int(entry(1, gl_journal.bemerk, chr(2)))


            pass

            if i_case > 0:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.fibukonto.lower()  == (fibu).lower()  and t_list.cf == i_cf), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.fibukonto = fibu
                    t_list.cf = i_cf

                if i_case == 1:
                    t_list.credit =  to_decimal(t_list.credit) + to_decimal(credit)
                    t_list.debit =  to_decimal(t_list.debit) + to_decimal(debit)


                elif i_case == 2:
                    t_list.credit_lsyear =  to_decimal(t_list.credit_lsyear) + to_decimal(credit)
                    t_list.debit_lsyear =  to_decimal(t_list.credit_lsyear) + to_decimal(debit)


                elif i_case == 3:
                    t_list.credit_lsmonth =  to_decimal(t_list.credit_lsmonth) + to_decimal(credit)
                    t_list.debit_lsmonth =  to_decimal(t_list.debit_lsmonth) + to_decimal(debit)


                elif i_case == 4:
                    t_list.credit_today =  to_decimal(t_list.credit_today) + to_decimal(credit)
                    t_list.debit_today =  to_decimal(t_list.debit_today) + to_decimal(debit)


                elif i_case == 5:
                    t_list.credit_mtd =  to_decimal(t_list.credit_mtd) + to_decimal(credit)
                    t_list.debit_mtd =  to_decimal(t_list.debit_mtd) + to_decimal(debit)


                elif i_case == 6:
                    t_list.credit_ytd =  to_decimal(t_list.credit_ytd) + to_decimal(credit)
                    t_list.debit_ytd =  to_decimal(t_list.debit_ytd) + to_decimal(debit)

            if i_case == 1:
                tbuff.credit =  to_decimal(tbuff.credit) + to_decimal(credit)
                tbuff.debit =  to_decimal(tbuff.debit) + to_decimal(debit)
                tbuff.balance =  to_decimal(tbuff.balance) + to_decimal(debit) - to_decimal(credit)


            elif i_case == 2:
                tbuff.credit_lsyear =  to_decimal(tbuff.credit_lsyear) + to_decimal(credit)
                tbuff.debit_lsyear =  to_decimal(tbuff.credit_lsyear) + to_decimal(debit)
                tbuff.ly_balance =  to_decimal(tbuff.ly_balance) + to_decimal(debit) - to_decimal(credit)


            elif i_case == 3:
                tbuff.credit_lsmonth =  to_decimal(tbuff.credit_lsmonth) + to_decimal(credit)
                tbuff.debit_lsmonth =  to_decimal(tbuff.debit_lsmonth) + to_decimal(debit)
                tbuff.pm_balance =  to_decimal(tbuff.pm_balance) + to_decimal(debit) - to_decimal(credit)


            elif i_case == 4:
                tbuff.credit_today =  to_decimal(tbuff.credit_today) + to_decimal(credit)
                tbuff.debit_today =  to_decimal(tbuff.debit_today) + to_decimal(debit)
                tbuff.today_balance =  to_decimal(tbuff.today_balance) + to_decimal(debit) - to_decimal(credit)


            elif i_case == 5:
                tbuff.credit_mtd =  to_decimal(tbuff.credit_mtd) + to_decimal(credit)
                tbuff.debit_mtd =  to_decimal(tbuff.debit_mtd) + to_decimal(debit)
                tbuff.mtd_balance =  to_decimal(tbuff.mtd_balance) + to_decimal(debit) - to_decimal(credit)


            elif i_case == 6:
                tbuff.credit_ytd =  to_decimal(tbuff.credit_ytd) + to_decimal(credit)
                tbuff.debit_ytd =  to_decimal(tbuff.debit_ytd) + to_decimal(debit)
                tbuff.ytd_balance =  to_decimal(tbuff.ytd_balance) + to_decimal(debit) - to_decimal(credit)

        if i_case == 1:
            tbuff.balance =  to_decimal(p_sign) * to_decimal(tbuff.balance)
        elif i_case == 2:
            tbuff.ly_balance =  to_decimal(p_sign) * to_decimal(tbuff.ly_balance)
        elif i_case == 3:
            tbuff.pm_balance =  to_decimal(p_sign) * to_decimal(tbuff.pm_balance)
        elif i_case == 4:
            tbuff.today_balance =  to_decimal(p_sign) * to_decimal(tbuff.today_balance)
        elif i_case == 5:
            tbuff.mtd_balance =  to_decimal(p_sign) * to_decimal(tbuff.mtd_balance)
        elif i_case == 6:
            tbuff.ytd_balance =  to_decimal(p_sign) * to_decimal(tbuff.ytd_balance)


    close_month = get_output(htpdate(597))
    last_close_yr = get_output(htpdate(795))
    close_year = date_mdy(12, 31, get_year(last_close_yr) + timedelta(days=1))


    prev_month = get_month(from_date) - 1

    if prev_month == 0:
        prev_month = 12

    for coa_list in query(coa_list_list):
        tbuff = Tbuff()
        tbuff_list.append(tbuff)

        tbuff.fibukonto = coa_list.fibu


        calc_balance(1, coa_list.fibu, from_date, to_date)
        calc_balance(2, coa_list.fibu, from_lsyr, to_lsyr)
        calc_balance(3, coa_list.fibu, pfrom_date, pto_date)
        calc_balance(4, coa_list.fibu, to_date, to_date)
        calc_balance(5, coa_list.fibu, from_month, to_date)
        calc_balance(6, coa_list.fibu, from_year, to_date)

    return generate_output()