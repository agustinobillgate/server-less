#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ar_subledger_create_age_list1bl import ar_subledger_create_age_list1bl
from functions.ar_subledger_create_age_list1abl import ar_subledger_create_age_list1abl

def ar_subledger_create_age_listbl(detail:bool, incl:bool, t_artnr:int, t_artart:int, t_dept:int, from_name:string, to_name:string, fr_date:date, to_date:date, bdate:date):
    tot_debt = to_decimal("0.0")
    tot_paid = to_decimal("0.0")
    tot_bal = to_decimal("0.0")
    age_list_list = []
    curr_art:int = 0
    debt_selected:bool = False

    age_list = abuff = abuff = None

    age_list_list, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":string, "billname":string, "gastnrmember":int, "zinr":string, "datum":date, "rgdatum":date, "paydatum":date, "user_init":string, "bezeich":string, "wabkurz":string, "debt":Decimal, "credit":Decimal, "fdebt":Decimal, "t_debt":Decimal, "tot_debt":Decimal, "rid":int, "dept":int, "gname":string, "voucher":string, "ankunft":date, "abreise":date, "stay":int, "remarks":string, "ttl":Decimal, "resname":string, "comp_name":string, "comp_add":string, "comp_fax":string, "comp_phone":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debt, tot_paid, tot_bal, age_list_list, curr_art, debt_selected
        nonlocal detail, incl, t_artnr, t_artart, t_dept, from_name, to_name, fr_date, to_date, bdate


        nonlocal age_list, abuff, abuff
        nonlocal age_list_list

        return {"tot_debt": tot_debt, "tot_paid": tot_paid, "tot_bal": tot_bal, "age-list": age_list_list}

    def create_age_list1():

        nonlocal tot_debt, tot_paid, tot_bal, age_list_list, curr_art, debt_selected
        nonlocal detail, incl, t_artnr, t_artart, t_dept, from_name, to_name, fr_date, to_date, bdate


        nonlocal age_list, abuff, abuff
        nonlocal age_list_list

        pay_amt:Decimal = to_decimal("0.0")
        pay_date:date = None
        Abuff = Age_list
        abuff_list = age_list_list
        curr_art = t_artnr
        tot_debt, tot_paid, age_list_list = get_output(ar_subledger_create_age_list1bl(incl, t_artnr, t_dept, from_name, to_name, fr_date, to_date, bdate))
        tot_bal =  to_decimal(tot_debt) - to_decimal(tot_paid)
        pass
        debt_selected = True
        pay_amt =  to_decimal("0")

        if not detail:

            for age_list in query(age_list_list, sort_by=[("nr",True)]):

                if age_list.billname != "" and pay_amt != 0:
                    age_list.paydatum = pay_date
                    age_list.credit =  to_decimal(age_list.credit) + to_decimal(pay_amt)
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) - to_decimal(pay_amt)
                    pay_amt =  to_decimal("0")

                elif age_list.billname == "":
                    pay_amt =  to_decimal(pay_amt) + to_decimal(age_list.credit)
                    pay_date = age_list.paydatum
                    age_list_list.remove(age_list)


        if not detail and t_artart == 2:

            for age_list in query(age_list_list, filters=(lambda age_list: age_list.billname != "")):

                for abuff in query(abuff_list, filters=(lambda abuff: abuff.rechnr == age_list.rechnr and abuff.dept == age_list.dept and abuff.gastnr == age_list.gastnr and abuff._recid != age_list._recid)):
                    age_list.credit =  to_decimal(age_list.credit) + to_decimal(abuff.credit)
                    age_list.debt =  to_decimal(age_list.debt) + to_decimal(abuff.debt)
                    age_list.fdebt =  to_decimal(age_list.fdebt) + to_decimal(abuff.fdebt)
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(abuff.tot_debt)


                    abuff_list.remove(abuff)

    def create_age_list1a():

        nonlocal tot_debt, tot_paid, tot_bal, age_list_list, curr_art, debt_selected
        nonlocal detail, incl, t_artnr, t_artart, t_dept, from_name, to_name, fr_date, to_date, bdate


        nonlocal age_list, abuff, abuff
        nonlocal age_list_list

        pay_amt:Decimal = to_decimal("0.0")
        pay_date:date = None
        Abuff = Age_list
        abuff_list = age_list_list
        curr_art = t_artnr
        tot_debt, tot_paid, age_list_list = get_output(ar_subledger_create_age_list1abl(incl, t_artnr, t_dept, from_name, to_name, fr_date, to_date, bdate))
        tot_bal =  to_decimal(tot_debt) - to_decimal(tot_paid)
        debt_selected = True
        pay_amt =  to_decimal("0")

        if not detail:

            for age_list in query(age_list_list, sort_by=[("nr",True)]):

                if age_list.billname != "" and pay_amt != 0:
                    age_list.paydatum = pay_date
                    age_list.credit =  to_decimal(age_list.credit) + to_decimal(pay_amt)
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) - to_decimal(pay_amt)
                    pay_amt =  to_decimal("0")

                elif age_list.billname == "":
                    pay_amt =  to_decimal(pay_amt) + to_decimal(age_list.credit)
                    pay_date = age_list.paydatum
                    age_list_list.remove(age_list)


        if not detail and t_artart == 2:

            for age_list in query(age_list_list, filters=(lambda age_list: age_list.billname != "")):

                for abuff in query(abuff_list, filters=(lambda abuff: abuff.rechnr == age_list.rechnr and abuff.dept == age_list.dept and abuff.gastnr == age_list.gastnr and abuff._recid != age_list._recid)):
                    age_list.credit =  to_decimal(age_list.credit) + to_decimal(abuff.credit)
                    age_list.debt =  to_decimal(age_list.debt) + to_decimal(abuff.debt)
                    age_list.fdebt =  to_decimal(age_list.fdebt) + to_decimal(abuff.fdebt)
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(abuff.tot_debt)


                    abuff_list.remove(abuff)

    if substring(to_name, 0, 2) == ("zz").lower() :
        create_age_list1a()
    else:
        create_age_list1()

    return generate_output()