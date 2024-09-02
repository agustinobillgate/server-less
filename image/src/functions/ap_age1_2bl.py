from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from models import L_kredit, Htparam, L_lieferant, Queasy

def ap_age1_2bl(pvilanguage:int, to_date:date, from_name:str, to_name:str, detailed:bool, mi_bill:bool, segm:int, curr_disp:int, round_zero:bool):
    apage_list_list = []
    billdate:date = None
    curr_lief_nr:int = 0
    curr_art:int = 0
    counter:int = 0
    i:int = 0
    curr_name:str = ""
    firma:str = ""
    curr_po:str = ""
    curr_lschein:str = ""
    p_bal:decimal = 0
    debit:decimal = 0
    credit:decimal = 0
    debt0:decimal = 0
    debt1:decimal = 0
    debt2:decimal = 0
    debt3:decimal = 0
    tot_debt:decimal = 0
    t_comm:decimal = 0
    t_adjust:decimal = 0
    t_saldo:decimal = 0
    t_prev:decimal = 0
    t_debit:decimal = 0
    t_credit:decimal = 0
    t_debt0:decimal = 0
    t_debt1:decimal = 0
    t_debt2:decimal = 0
    t_debt3:decimal = 0
    tmp_saldo:decimal = 0
    curr_rgdatum:str = ""
    from_date:date = None
    guest_name:str = ""
    curr_bezeich:str = ""
    outlist:str = ""
    do_it:bool = False
    price_decimal:int = 0
    voucher_no:str = ""
    day1:int = 30
    day2:int = 30
    day3:int = 30
    curr_saldo:decimal = 0
    lvcarea:str = "ap_age1"
    l_kredit = htparam = l_lieferant = queasy = None

    apage_list = debtrec = debt = age_list = None

    apage_list_list, Apage_list = create_model("Apage_list", {"docu_nr":str, "lschein":str, "rgdatum":str, "rechnr":str, "str":str})
    age_list_list, Age_list = create_model("Age_list", {"artnr":int, "rechnr":str, "lschein":str, "counter":int, "lief_nr":int, "rgdatum":date, "firma":str, "voucher_no":int, "p_bal":decimal, "debit":decimal, "credit":decimal, "saldo":decimal, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal})

    Debtrec = L_kredit
    Debt = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list
        return {"apage-list": apage_list_list}

    def age_list():

        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart <= 1) &  (L_kredit.counter >= 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                if l_kredit.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt = 0
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.lschein = l_kredit.lscheinnr

                if l_kredit.zahlkonto == 0:
                    age_list.tot_debt = age_list.tot_debt + l_kredit.netto
                else:
                    age_list.tot_debt = age_list.tot_debt + l_kredit.saldo

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                    age_list.p_bal = age_list.p_bal + l_kredit.netto

                if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                    age_list.debit = age_list.debit + l_kredit.netto

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                    age_list.p_bal = age_list.p_bal + l_kredit.saldo
                else:

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                        age_list.credit = age_list.credit - l_kredit.saldo
        counter = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.lief_nr > 0) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = l_kredit.netto
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr


                age_list.lschein = l_kredit.lscheinnr

                if l_kredit.rgdatum < from_date:
                    age_list.p_bal = age_list.p_bal + l_kredit.netto

                elif l_kredit.rgdatum >= from_date:
                    age_list.debit = age_list.debit + l_kredit.netto

                for debtrec in db_session.query(Debtrec).filter(
                        (Debtrec.counter == l_kredit.counter) &  (Debtrec.opart == 2) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                    age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                    if debtrec.rgdatum < from_date:
                        age_list.p_bal = age_list.p_bal + debtrec.saldo

                    elif debtrec.rgdatum >= from_date:
                        age_list.credit = age_list.credit - debtrec.saldo
        counter = 0
        curr_lief_nr = 0
        curr_name = ""

    def age_list1():

        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart <= 1) &  (L_kredit.counter >= 0) &  (L_kredit.steuercode == 1)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                if l_kredit.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt = 0
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.lschein = l_kredit.lscheinnr

                if l_kredit.zahlkonto == 0:
                    age_list.tot_debt = age_list.tot_debt + l_kredit.netto
                else:
                    age_list.tot_debt = age_list.tot_debt + l_kredit.saldo

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                    age_list.p_bal = age_list.p_bal + l_kredit.netto

                if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                    age_list.debit = age_list.debit + l_kredit.netto

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                    age_list.p_bal = age_list.p_bal + l_kredit.saldo
                else:

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                        age_list.credit = age_list.credit - l_kredit.saldo
        counter = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.lief_nr > 0) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0) &  (L_kredit.steuercode == 1)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = l_kredit.netto
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr


                age_list.lschein = l_kredit.lscheinnr

                if l_kredit.rgdatum < from_date:
                    age_list.p_bal = age_list.p_bal + l_kredit.netto

                elif l_kredit.rgdatum >= from_date:
                    age_list.debit = age_list.debit + l_kredit.netto

                for debtrec in db_session.query(Debtrec).filter(
                        (Debtrec.counter == l_kredit.counter) &  (Debtrec.opart == 2) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                    age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                    if debtrec.rgdatum < from_date:
                        age_list.p_bal = age_list.p_bal + debtrec.saldo

                    elif debtrec.rgdatum >= from_date:
                        age_list.credit = age_list.credit - debtrec.saldo
        counter = 0
        curr_lief_nr = 0
        curr_name = ""

    def age_list2():

        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart <= 1) &  (L_kredit.counter >= 0) &  (L_kredit.steuercode == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                if l_kredit.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt = 0
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.lschein = l_kredit.lscheinnr

                if l_kredit.zahlkonto == 0:
                    age_list.tot_debt = age_list.tot_debt + l_kredit.netto
                else:
                    age_list.tot_debt = age_list.tot_debt + l_kredit.saldo

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                    age_list.p_bal = age_list.p_bal + l_kredit.netto

                if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                    age_list.debit = age_list.debit + l_kredit.netto

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                    age_list.p_bal = age_list.p_bal + l_kredit.saldo
                else:

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                        age_list.credit = age_list.credit - l_kredit.saldo
        counter = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.lief_nr > 0) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0) &  (L_kredit.steuercode == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = l_kredit.netto
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr


                age_list.lschein = l_kredit.lscheinnr

                if l_kredit.rgdatum < from_date:
                    age_list.p_bal = age_list.p_bal + l_kredit.netto

                elif l_kredit.rgdatum >= from_date:
                    age_list.debit = age_list.debit + l_kredit.netto

                for debtrec in db_session.query(Debtrec).filter(
                        (Debtrec.counter == l_kredit.counter) &  (Debtrec.opart == 2) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                    age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                    if debtrec.rgdatum < from_date:
                        age_list.p_bal = age_list.p_bal + debtrec.saldo

                    elif debtrec.rgdatum >= from_date:
                        age_list.credit = age_list.credit - debtrec.saldo
        counter = 0
        curr_lief_nr = 0
        curr_name = ""

    def age_list3():

        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart <= 1) &  (L_kredit.counter >= 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 221) &  (Queasy.number1 == l_kredit.lief_nr) &  (Queasy.char1 == l_kredit.lscheinnr)).first()

                if queasy:

                    if l_kredit.counter > 0:

                        age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == l_kredit.counter), first=True)

                    if (l_kredit.counter == 0) or (not age_list):
                        age_list = Age_list()
                        age_list_list.append(age_list)

                        age_list.rgdatum = queasy.date1
                        age_list.counter = l_kredit.counter
                        age_list.lief_nr = l_kredit.lief_nr
                        age_list.tot_debt = 0
                        age_list.firma = l_lieferant.firma
                        age_list.rechnr = l_kredit.name
                        age_list.lschein = l_kredit.lscheinnr

                    if l_kredit.zahlkonto == 0:
                        age_list.tot_debt = age_list.tot_debt + l_kredit.netto
                    else:
                        age_list.tot_debt = age_list.tot_debt + l_kredit.saldo

                    if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                        age_list.p_bal = age_list.p_bal + l_kredit.netto

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                        age_list.debit = age_list.debit + l_kredit.netto

                    if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                        age_list.p_bal = age_list.p_bal + l_kredit.saldo
                    else:

                        if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                            age_list.credit = age_list.credit - l_kredit.saldo
        counter = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.lief_nr > 0) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 221) &  (Queasy.number1 == l_kredit.lief_nr) &  (Queasy.char1 == l_kredit.lscheinnr)).first()

                if queasy:
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = queasy.date1
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt = l_kredit.netto
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    guest_name = l_lieferant.firma
                    age_list.voucher_no = l_kredit.rechnr


                    age_list.lschein = l_kredit.lscheinnr

                    if l_kredit.rgdatum < from_date:
                        age_list.p_bal = age_list.p_bal + l_kredit.netto

                    elif l_kredit.rgdatum >= from_date:
                        age_list.debit = age_list.debit + l_kredit.netto

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == l_kredit.counter) &  (Debtrec.opart == 2) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                        age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                        if debtrec.rgdatum < from_date:
                            age_list.p_bal = age_list.p_bal + debtrec.saldo

                        elif debtrec.rgdatum >= from_date:
                            age_list.credit = age_list.credit - debtrec.saldo
        counter = 0
        curr_lief_nr = 0
        curr_name = ""

    def fill_in_list(fill_billno:bool, curr_po:str, curr_lschein:str, curr_rgdatum:str, voucher_no:str):

        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list


        apage_list = Apage_list()
        apage_list_list.append(apage_list)


        if fill_billno:
            apage_list.docu_nr = curr_po
            apage_list.lschein = curr_lschein
            apage_list.rgdatum = curr_rgdatum
            apage_list.rechnr = voucher_no


        apage_list.str = outlist

        if substring(outlist, 0, 5) == "-----":
            apage_list.docu_nr = "----------------"
            apage_list.lschein = "-------------------"
            apage_list.rgdatum = "--------"
            apage_list.rechnr = "----------"

    def add_detail_date():

        nonlocal apage_list_list, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        if to_date - age_list.rgdatum > day3:
            age_list.debt3 = age_list.tot_debt

        elif to_date - age_list.rgdatum > day2:
            age_list.debt2 = age_list.tot_debt

        elif to_date - age_list.rgdatum > day1:
            age_list.debt1 = age_list.tot_debt
        else:
            age_list.debt0 = age_list.tot_debt

        if round_zero:
            t_saldo = t_saldo + age_list.tot_debt
            t_prev = t_prev + age_list.p_bal
            t_debit = t_debit + age_list.debit
            t_credit = t_credit + age_list.credit
            t_debt0 = t_debt0 + age_list.debt0
            t_debt1 = t_debt1 + age_list.debt1
            t_debt2 = t_debt2 + age_list.debt2
            t_debt3 = t_debt3 + age_list.debt3
            curr_po = age_list.rechnr
            curr_lschein = age_list.lschein
            curr_rgdatum = to_string(age_list.rgdatum, "99/99/99")
            firma = age_list.firma
            voucher_no = to_string(age_list.voucher_no)
            tot_debt = round(age_list.tot_debt, 0)
            p_bal = round(age_list.p_bal , 0)
            debit = round(age_list.debit , 0)
            credit = round(age_list.credit , 0)
            debt0 = round(age_list.debt0 , 0)
            debt1 = round(age_list.debt1 , 0)
            debt2 = round(age_list.debt2 , 0)
            debt3 = round(age_list.debt3 , 0)


            counter = counter + 1
        else:
            t_saldo = t_saldo + age_list.tot_debt
            t_prev = t_prev + age_list.p_bal
            t_debit = t_debit + age_list.debit
            t_credit = t_credit + age_list.credit
            t_debt0 = t_debt0 + age_list.debt0
            t_debt1 = t_debt1 + age_list.debt1
            t_debt2 = t_debt2 + age_list.debt2
            t_debt3 = t_debt3 + age_list.debt3
            curr_po = age_list.rechnr
            curr_lschein = age_list.lschein
            curr_rgdatum = to_string(age_list.rgdatum, "99/99/99")
            firma = age_list.firma
            voucher_no = to_string(age_list.voucher_no)
            tot_debt = age_list.tot_debt
            p_bal = age_list.p_bal
            debit = age_list.debit
            credit = age_list.credit
            debt0 = age_list.debt0
            debt1 = age_list.debt1
            debt2 = age_list.debt2
            debt3 = age_list.debt3
            counter = counter + 1

        if p_bal != 0 or debit != 0 or credit != 0:

            if price_decimal == 0:
                outlist = "  " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
            else:
                outlist = "  " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
            fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, voucher_no)
            curr_po = age_list.rechnr
            curr_lschein = age_list.lschein
            voucher_no = to_string(age_list.voucher_no)


        else:
            counter = counter - 1
        age_list_list.remove(age_list)

    billdate = None
    curr_lief_nr = 0
    curr_art = 0
    counter = 0
    i = 0
    curr_name = ""
    firma = ""
    curr_po = ""
    curr_lschein = ""
    p_bal = 0
    debit = 0
    credit = 0
    debt0 = 0
    debt1 = 0
    debt2 = 0
    debt3 = 0
    tot_debt = 0
    t_comm = 0
    t_adjust = 0
    t_saldo = 0
    t_prev = 0
    t_debit = 0
    t_credit = 0
    t_debt0 = 0
    t_debt1 = 0
    t_debt2 = 0
    t_debt3 = 0
    tmp_saldo = 0
    curr_rgdatum = None

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 330)).first()

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 331)).first()

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 332)).first()

    if htparam.finteger != 0:
        day3 = htparam.finteger
    day2 = day2 + day1
    day3 = day3 + day2
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    price_decimal = get_output(htpint(491))

    if curr_disp == 1:
        age_list()

    elif curr_disp == 2:
        age_list1()

    elif curr_disp == 3:
        age_list2()

    elif curr_disp == 4:
        age_list3()

    if not detailed:

        for age_list in query(age_list_list):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 = age_list.tot_debt
            else:
                age_list.debt0 = age_list.tot_debt

            if round_zero:
                t_saldo = t_saldo + age_list.tot_debt
                t_prev = t_prev + age_list.p_bal
                t_debit = t_debit + age_list.debit
                t_credit = t_credit + age_list.credi
                t_debt0 = t_debt0 + age_list.debt0
                t_debt1 = t_debt1 + age_list.debt1
                t_debt2 = t_debt2 + age_list.debt2
                t_debt3 = t_debt3 + age_list.debt3
            else:
                t_saldo = t_saldo + age_list.tot_debt
                t_prev = t_prev + age_list.p_bal
                t_debit = t_debit + age_list.debit
                t_credit = t_credit + age_list.credit
                t_debt0 = t_debt0 + age_list.debt0
                t_debt1 = t_debt1 + age_list.debt1
                t_debt2 = t_debt2 + age_list.debt2
                t_debt3 = t_debt3 + age_list.debt3

            if curr_lief_nr == 0:

                if round_zero:
                    curr_po = age_list.rechnr
                    curr_lschein = age_list.lschein
                    firma = age_list.firma
                    tot_debt = round(age_list.tot_debt, 0)
                    p_bal = round(age_list.p_bal , 0)
                    debit = round(age_list.debit , 0)
                    credit = round(age_list.credit , 0)
                    debt0 = round(age_list.debt0 , 0)
                    debt1 = round(age_list.debt1 , 0)
                    debt2 = round(age_list.debt2 , 0)
                    debt3 = round(age_list.debt3 , 0)


                    counter = counter + 1
                else:
                    curr_po = age_list.rechnr
                    curr_lschein = age_list.lschein
                    firma = age_list.firma
                    tot_debt = age_list.tot_debt
                    p_bal = age_list.p_bal
                    debit = age_list.debit
                    credit = age_list.credit
                    debt0 = age_list.debt0
                    debt1 = age_list.debt1
                    debt2 = age_list.debt2
                    debt3 = age_list.debt3
                    counter = counter + 1

            elif curr_name != age_list.firma:

                if p_bal != 0 or debit != 0 or credit != 0:

                    if price_decimal == 0:
                        outlist = "  " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
                    else:
                        outlist = "  " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                    fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, "")
                    curr_po = age_list.rechnr
                    curr_lschein = age_list.lschein


                else:
                    counter = counter - 1

                if round_zero:
                    firma = age_list.firma
                    tot_debt = round(age_list.tot_debt, 0)
                    p_bal = round(age_list.p_bal , 0)
                    debit = round(age_list.debit , 0)
                    credit = round(age_list.credit , 0)
                    debt0 = round(age_list.debt0 , 0)
                    debt1 = round(age_list.debt1 , 0)
                    debt2 = round(age_list.debt2 , 0)
                    debt3 = round(age_list.debt3 , 0)
                    counter = counter + 1
                else:
                    firma = age_list.firma
                    tot_debt = age_list.tot_debt
                    p_bal = age_list.p_bal
                    debit = age_list.debit
                    credit = age_list.credit
                    debt0 = age_list.debt0
                    debt1 = age_list.debt1
                    debt2 = age_list.debt2
                    debt3 = age_list.debt3
                    counter = counter + 1
            else:

                if round_zero:
                    tot_debt = tot_debt + round(age_list.tot_debt, 0)
                    p_bal = p_bal + round(age_list.p_bal , 0)
                    debit = debit + round(age_list.debit , 0)
                    credit = credit + round(age_list.credit , 0)
                    debt0 = debt0 + round(age_list.debt0 , 0)
                    debt1 = debt1 + round(age_list.debt1 , 0)
                    debt2 = debt2 + round(age_list.debt2 , 0)
                    debt3 = debt3 + round(age_list.debt3 , 0)
                else:
                    tot_debt = tot_debt + age_list.tot_debt
                    p_bal = p_bal + age_list.p_bal
                    debit = debit + age_list.debit
                    credit = credit + age_list.credit
                    debt0 = debt0 + age_list.debt0
                    debt1 = debt1 + age_list.debt1
                    debt2 = debt2 + age_list.debt2
                    debt3 = debt3 + age_list.debt3
            curr_lief_nr = age_list.lief_nr

            if not detailed:
                curr_name = age_list.firma
            age_list_list.remove(age_list)
    else:

        if not mi_bill:

            for age_list in query(age_list_list):
                add_detail_date()


        for age_list in query(age_list_list):
            add_detail_date()

    if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0) and not detailed:

        if price_decimal == 0:
            outlist = "  " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = "  " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, "")
    else:
        counter = counter - 1
    outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    fill_in_list(False, "", "", "--------", "")

    if round_zero:
        outlist = "       " + to_string(translateExtended ("T O T A L  A/P:", lvcarea, "") , "x(30)") + to_string(round(t_saldo, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_prev, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debit, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_credit, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt0, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt1, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt2, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt3, 0) , "->>,>>>,>>>,>>9.99")
    else:
        outlist = "       " + to_string(translateExtended ("T O T A L  A/P:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>9.99") + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
    fill_in_list(False, "", "", "", "")
    outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    fill_in_list(False, "", "", "--------", "")
    outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
    for i in range(1,54 + 1) :
        outlist = outlist + " "
    outlist = outlist + to_string((t_debt0 / t_saldo * 100) , "           ->>9.99") + to_string((t_debt1 / t_saldo * 100) , "           ->>9.99") + to_string((t_debt2 / t_saldo * 100) , "           ->>9.99") + to_string((t_debt3 / t_saldo * 100) , "           ->>9.99")
    fill_in_list(False, "", "", "", "")
    outlist = ""
    fill_in_list(False, "", "", "", "")

    return generate_output()