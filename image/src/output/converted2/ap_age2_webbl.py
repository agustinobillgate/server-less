#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import L_kredit, Htparam, L_lieferant, Queasy, L_orderhdr

def ap_age2_webbl(pvilanguage:int, to_date:date, from_name:string, to_name:string, mi_bill:bool, segm:int, curr_disp:int, round_zero:bool):

    prepare_cache ([L_kredit, Htparam, L_lieferant, Queasy, L_orderhdr])

    apage_list_list = []
    tt_no:string = ""
    tt_supp:string = ""
    tt_saldo:string = ""
    tt_prev:string = ""
    tt_debit:string = ""
    tt_credit:string = ""
    tt_debt0:string = ""
    tt_debt1:string = ""
    tt_debt2:string = ""
    tt_debt3:string = ""
    billdate:date = None
    curr_lief_nr:int = 0
    curr_art:int = 0
    counter:int = 0
    i:int = 0
    curr_name:string = ""
    firma:string = ""
    curr_po:string = ""
    curr_lschein:string = ""
    p_bal:Decimal = to_decimal("0.0")
    debit:Decimal = to_decimal("0.0")
    credit:Decimal = to_decimal("0.0")
    debt0:Decimal = to_decimal("0.0")
    debt1:Decimal = to_decimal("0.0")
    debt2:Decimal = to_decimal("0.0")
    debt3:Decimal = to_decimal("0.0")
    agdatum:int = 0
    overdatum:date = None
    termof_pay:int = 0
    tot_debt:Decimal = to_decimal("0.0")
    t_comm:Decimal = to_decimal("0.0")
    t_adjust:Decimal = to_decimal("0.0")
    t_saldo:Decimal = to_decimal("0.0")
    t_prev:Decimal = to_decimal("0.0")
    t_debit:Decimal = to_decimal("0.0")
    t_credit:Decimal = to_decimal("0.0")
    t_debt0:Decimal = to_decimal("0.0")
    t_debt1:Decimal = to_decimal("0.0")
    t_debt2:Decimal = to_decimal("0.0")
    t_debt3:Decimal = to_decimal("0.0")
    tmp_saldo:Decimal = to_decimal("0.0")
    curr_rgdatum:string = ""
    from_date:date = None
    guest_name:string = ""
    curr_bezeich:string = ""
    outlist:string = ""
    do_it:bool = False
    price_decimal:int = 0
    voucher_no:string = ""
    day1:int = 30
    day2:int = 30
    day3:int = 30
    curr_saldo:Decimal = to_decimal("0.0")
    lvcarea:string = "ap-age1"
    l_kredit = htparam = l_lieferant = queasy = l_orderhdr = None

    apage_list = debtrec = debt = age_list = None

    apage_list_list, Apage_list = create_model("Apage_list", {"docu_nr":string, "lschein":string, "rgdatum":string, "rechnr":string, "ag_datum":string, "overdue":string, "term_pay":string, "t_no":string, "t_supp":string, "t_saldo":string, "t_prev":string, "t_debit":string, "t_credit":string, "t_debt0":string, "t_debt1":string, "t_debt2":string, "t_debt3":string})
    age_list_list, Age_list = create_model("Age_list", {"artnr":int, "rechnr":string, "lschein":string, "counter":int, "lief_nr":int, "rgdatum":date, "firma":string, "voucher_no":int, "p_bal":Decimal, "debit":Decimal, "credit":Decimal, "saldo":Decimal, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal, "ap_term":int})

    Debtrec = create_buffer("Debtrec",L_kredit)
    Debt = create_buffer("Debt",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, agdatum, overdatum, termof_pay, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        return {"apage-list": apage_list_list}

    def age_list():

        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, agdatum, overdatum, termof_pay, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart <= 1) & (L_kredit.counter >= 0)).order_by(L_lieferant.firma, L_kredit.zahlkonto).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                if l_kredit.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal("0")
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.lschein = l_kredit.lscheinnr

                if l_kredit.zahlkonto == 0:
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.netto)
                else:
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.saldo)

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.saldo)
                else:

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(l_kredit.saldo)
                age_list.ap_term = l_kredit.ziel
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.lief_nr > 0) & (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(l_kredit.netto)
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr


                age_list.lschein = l_kredit.lscheinnr

                if l_kredit.rgdatum < from_date:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                elif l_kredit.rgdatum >= from_date:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                for debtrec in db_session.query(Debtrec).filter(
                         (Debtrec.counter == l_kredit.counter) & (Debtrec.opart == 2) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debtrec.saldo)

                    if debtrec.rgdatum < from_date:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debtrec.saldo)

                    elif debtrec.rgdatum >= from_date:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(debtrec.saldo)
                age_list.ap_term = l_kredit.ziel
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def age_list1():

        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, agdatum, overdatum, termof_pay, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart <= 1) & (L_kredit.counter >= 0) & (L_kredit.steuercode == 1)).order_by(L_lieferant.firma, L_kredit.zahlkonto).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                if l_kredit.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal("0")
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.lschein = l_kredit.lscheinnr

                if l_kredit.zahlkonto == 0:
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.netto)
                else:
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.saldo)

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.saldo)
                else:

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(l_kredit.saldo)
                age_list.ap_term = l_kredit.ziel
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.lief_nr > 0) & (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0) & (L_kredit.steuercode == 1)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(l_kredit.netto)
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr


                age_list.lschein = l_kredit.lscheinnr

                if l_kredit.rgdatum < from_date:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                elif l_kredit.rgdatum >= from_date:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                for debtrec in db_session.query(Debtrec).filter(
                         (Debtrec.counter == l_kredit.counter) & (Debtrec.opart == 2) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debtrec.saldo)

                    if debtrec.rgdatum < from_date:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debtrec.saldo)

                    elif debtrec.rgdatum >= from_date:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(debtrec.saldo)
            age_list.ap_term = l_kredit.ziel
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def age_list2():

        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, agdatum, overdatum, termof_pay, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart <= 1) & (L_kredit.counter >= 0) & (L_kredit.steuercode == 0)).order_by(L_lieferant.firma, L_kredit.zahlkonto).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                if l_kredit.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal("0")
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.lschein = l_kredit.lscheinnr

                if l_kredit.zahlkonto == 0:
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.netto)
                else:
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.saldo)

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.saldo)
                else:

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(l_kredit.saldo)
                age_list.ap_term = l_kredit.ziel
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.lief_nr > 0) & (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0) & (L_kredit.steuercode == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(l_kredit.netto)
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr


                age_list.lschein = l_kredit.lscheinnr

                if l_kredit.rgdatum < from_date:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                elif l_kredit.rgdatum >= from_date:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                for debtrec in db_session.query(Debtrec).filter(
                         (Debtrec.counter == l_kredit.counter) & (Debtrec.opart == 2) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                    age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debtrec.saldo)

                    if debtrec.rgdatum < from_date:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debtrec.saldo)

                    elif debtrec.rgdatum >= from_date:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(debtrec.saldo)
                age_list.ap_term = l_kredit.ziel
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def age_list3():

        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, agdatum, overdatum, termof_pay, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart <= 1) & (L_kredit.counter >= 0)).order_by(L_lieferant.firma, L_kredit.zahlkonto).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                if queasy:

                    if l_kredit.counter > 0:

                        age_list = query(age_list_list, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                    if (l_kredit.counter == 0) or (not age_list):
                        age_list = Age_list()
                        age_list_list.append(age_list)

                        age_list.rgdatum = queasy.date1
                        age_list.counter = l_kredit.counter
                        age_list.lief_nr = l_kredit.lief_nr
                        age_list.tot_debt =  to_decimal("0")
                        age_list.firma = l_lieferant.firma
                        age_list.rechnr = l_kredit.name
                        age_list.lschein = l_kredit.lscheinnr

                    if l_kredit.zahlkonto == 0:
                        age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.netto)
                    else:
                        age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(l_kredit.saldo)

                    if l_kredit.rgdatum < from_date and l_kredit.zahlkonto == 0:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                    if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto == 0:
                        age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                    if l_kredit.rgdatum < from_date and l_kredit.zahlkonto != 0:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.saldo)
                    else:

                        if l_kredit.rgdatum >= from_date and l_kredit.zahlkonto != 0:
                            age_list.credit =  to_decimal(age_list.credit) - to_decimal(l_kredit.saldo)

                    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, l_kredit.name)]})

                    if l_orderhdr:
                        age_list.ap_term = l_orderhdr.angebot_lief[1]
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit.ziel, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit.ziel, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.lief_nr > 0) & (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if segm != 0 and l_lieferant.segment1 != segm:
                do_it = False

            if do_it:

                queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                if queasy:
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.rgdatum = queasy.date1
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal(l_kredit.netto)
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    guest_name = l_lieferant.firma
                    age_list.voucher_no = l_kredit.rechnr


                    age_list.lschein = l_kredit.lscheinnr

                    if l_kredit.rgdatum < from_date:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(l_kredit.netto)

                    elif l_kredit.rgdatum >= from_date:
                        age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.netto)

                    for debtrec in db_session.query(Debtrec).filter(
                             (Debtrec.counter == l_kredit.counter) & (Debtrec.opart == 2) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                        age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debtrec.saldo)

                        if debtrec.rgdatum < from_date:
                            age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debtrec.saldo)

                        elif debtrec.rgdatum >= from_date:
                            age_list.credit =  to_decimal(age_list.credit) - to_decimal(debtrec.saldo)

                    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, l_kredit.name)]})

                    if l_orderhdr:
                        age_list.ap_term = l_orderhdr.angebot_lief[1]
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def fill_in_list(fill_billno:bool, curr_po:string, curr_lschein:string, curr_rgdatum:string, voucher_no:string, agdatum:string, overdatum:string, termof_pay:string):

        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
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
            apage_list.ag_datum = agdatum
            apage_list.overdue = overdatum
            apage_list.term_pay = termof_pay

        if tt_no.lower()  == ("-------").lower() :
            apage_list.docu_nr = "----------------"
            apage_list.lschein = "-------------------"
            apage_list.rgdatum = "--------"
            apage_list.rechnr = "----------"
            apage_list.rechnr = "----------"
            apage_list.rechnr = "----------"
            apage_list.ag_datum = "------"
            apage_list.overdue = "--------"
        apage_list.t_no = tt_no
        apage_list.t_supp = tt_supp
        apage_list.t_saldo = tt_saldo
        apage_list.t_prev = tt_prev
        apage_list.t_debit = tt_debit
        apage_list.t_credit = tt_credit
        apage_list.t_debt0 = tt_debt0
        apage_list.t_debt1 = tt_debt1
        apage_list.t_debt2 = tt_debt2
        apage_list.t_debt3 = tt_debt3


    def add_detail_date():

        nonlocal apage_list_list, tt_no, tt_supp, tt_saldo, tt_prev, tt_debit, tt_credit, tt_debt0, tt_debt1, tt_debt2, tt_debt3, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, agdatum, overdatum, termof_pay, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy, l_orderhdr
        nonlocal pvilanguage, to_date, from_name, to_name, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, debtrec, debt, age_list
        nonlocal apage_list_list, age_list_list

        if to_date - age_list.rgdatum <= 30:
            age_list.debt0 =  to_decimal(age_list.tot_debt)

        elif to_date - age_list.rgdatum >= 30 and to_date - age_list.rgdatum < 60:
            age_list.debt1 =  to_decimal(age_list.tot_debt)

        elif to_date - age_list.rgdatum >= 60 and to_date - age_list.rgdatum < 90:
            age_list.debt2 =  to_decimal(age_list.tot_debt)

        elif to_date - age_list.rgdatum >= 90:
            age_list.debt3 =  to_decimal(age_list.tot_debt)

        if round_zero:
            t_saldo = to_decimal(t_saldo + round(age_list.tot_debt , 0))
            t_prev = to_decimal(t_prev + round(age_list.p_bal , 0))
            t_debit = to_decimal(t_debit + round(age_list.debit , 0))
            t_credit = to_decimal(t_credit + round(age_list.credit , 0))
            t_debt0 = to_decimal(t_debt0 + round(age_list.debt0 , 0))
            t_debt1 = to_decimal(t_debt1 + round(age_list.debt1 , 0))
            t_debt2 = to_decimal(t_debt2 + round(age_list.debt2 , 0))
            t_debt3 = to_decimal(t_debt3 + round(age_list.debt3 , 0))
            curr_po = age_list.rechnr
            curr_lschein = age_list.lschein
            curr_rgdatum = to_string(age_list.rgdatum, "99/99/99")
            firma = age_list.firma
            voucher_no = to_string(age_list.voucher_no)
            tot_debt = to_decimal(round(age_list.tot_debt , 0))
            p_bal = to_decimal(round(age_list.p_bal , 0))
            debit = to_decimal(round(age_list.debit , 0))
            credit = to_decimal(round(age_list.credit , 0))
            debt0 = to_decimal(round(age_list.debt0 , 0))
            debt1 = to_decimal(round(age_list.debt1 , 0))
            debt2 = to_decimal(round(age_list.debt2 , 0))
            debt3 = to_decimal(round(age_list.debt3 , 0))
            agdatum = to_date - age_list.rgdatum
            overdatum = age_list.rgdatum + ap_term
            termof_pay = age_list.ap_term


            counter = counter + 1
        else:
            t_saldo =  to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
            t_prev =  to_decimal(t_prev) + to_decimal(age_list.p_bal)
            t_debit =  to_decimal(t_debit) + to_decimal(age_list.debit)
            t_credit =  to_decimal(t_credit) + to_decimal(age_list.credit)
            t_debt0 =  to_decimal(t_debt0) + to_decimal(age_list.debt0)
            t_debt1 =  to_decimal(t_debt1) + to_decimal(age_list.debt1)
            t_debt2 =  to_decimal(t_debt2) + to_decimal(age_list.debt2)
            t_debt3 =  to_decimal(t_debt3) + to_decimal(age_list.debt3)
            curr_po = age_list.rechnr
            curr_lschein = age_list.lschein
            curr_rgdatum = to_string(age_list.rgdatum, "99/99/99")
            firma = age_list.firma
            voucher_no = to_string(age_list.voucher_no)
            tot_debt =  to_decimal(age_list.tot_debt)
            p_bal =  to_decimal(age_list.p_bal)
            debit =  to_decimal(age_list.debit)
            credit =  to_decimal(age_list.credit)
            debt0 =  to_decimal(age_list.debt0)
            debt1 =  to_decimal(age_list.debt1)
            debt2 =  to_decimal(age_list.debt2)
            debt3 =  to_decimal(age_list.debt3)
            counter = counter + 1
            agdatum = to_date - age_list.rgdatum
            overdatum = age_list.rgdatum + ap_term
            termof_pay = age_list.ap_term

        if p_bal != 0 or debit != 0 or credit != 0:

            if price_decimal == 0:
                tt_no = " " + to_string(counter, ">>>9 ")
                tt_supp = to_string(firma, "x(30)")
                tt_saldo = to_string(tot_debt, "->,>>>,>>>,>>>,>>9")
                tt_prev = to_string(p_bal, "->,>>>,>>>,>>>,>>9")
                tt_debit = to_string(debit, "->,>>>,>>>,>>>,>>9")
                tt_credit = to_string(credit, "->,>>>,>>>,>>>,>>9")
                tt_debt0 = to_string(debt0, "->,>>>,>>>,>>>,>>9")
                tt_debt1 = to_string(debt1, "->,>>>,>>>,>>>,>>9")
                tt_debt2 = to_string(debt2, "->,>>>,>>>,>>>,>>9")
                tt_debt3 = to_string(debt3, "->,>>>,>>>,>>>,>>9")


            else:
                tt_no = " " + to_string(counter, ">>>9 ")
                tt_supp = to_string(firma, "x(30)")
                tt_saldo = to_string(tot_debt, "->>,>>>,>>>,>>9.99")
                tt_prev = to_string(p_bal, "->>,>>>,>>>,>>9.99")
                tt_debit = to_string(debit, "->>,>>>,>>>,>>9.99")
                tt_credit = to_string(credit, "->>,>>>,>>>,>>9.99")
                tt_debt0 = to_string(debt0, "->>,>>>,>>>,>>9.99")
                tt_debt1 = to_string(debt1, "->>,>>>,>>>,>>9.99")
                tt_debt2 = to_string(debt2, "->>,>>>,>>>,>>9.99")
                tt_debt3 = to_string(debt3, "->>,>>>,>>>,>>9.99")


            fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, voucher_no, agdatum, overdatum, termof_pay)
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
    p_bal =  to_decimal("0")
    debit =  to_decimal("0")
    credit =  to_decimal("0")
    debt0 =  to_decimal("0")
    debt1 =  to_decimal("0")
    debt2 =  to_decimal("0")
    debt3 =  to_decimal("0")
    tot_debt =  to_decimal("0")
    t_comm =  to_decimal("0")
    t_adjust =  to_decimal("0")
    t_saldo =  to_decimal("0")
    t_prev =  to_decimal("0")
    t_debit =  to_decimal("0")
    t_credit =  to_decimal("0")
    t_debt0 =  to_decimal("0")
    t_debt1 =  to_decimal("0")
    t_debt2 =  to_decimal("0")
    t_debt3 =  to_decimal("0")
    tmp_saldo =  to_decimal("0")
    curr_rgdatum = None

    htparam = get_cache (Htparam, {"paramnr": [(eq, 330)]})

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 331)]})

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 332)]})

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

    if not mi_bill:

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.tot_debt != 0), sort_by=[("firma",False)]):
            add_detail_date()

    else:

        for age_list in query(age_list_list, sort_by=[("rgdatum",False)]):
            add_detail_date()
    counter = counter - 1
    tt_no = "-------"
    tt_supp = "------------------------------"
    tt_saldo = "------------------"
    tt_prev = "------------------"
    tt_debit = "------------------"
    tt_credit = "------------------"
    tt_debt0 = "------------------"
    tt_debt1 = "------------------"
    tt_debt2 = "------------------"
    tt_debt3 = "------------------"
    fill_in_list(False, "", "", "--------", "", "", "", "")

    if price_decimal == 0:
        tt_no = " "
        tt_supp = to_string(translateExtended ("T O T A L A/P:", lvcarea, "") , "x(30)")
        tt_saldo = to_string(t_saldo, "->,>>>,>>>,>>>,>>9")
        tt_prev = to_string(t_prev, "->,>>>,>>>,>>>,>>9")
        tt_debit = to_string(t_debit, "->,>>>,>>>,>>>,>>9")
        tt_credit = to_string(t_credit, "->,>>>,>>>,>>>,>>9")
        tt_debt0 = to_string(t_debt0, "->,>>>,>>>,>>>,>>9")
        tt_debt1 = to_string(t_debt1, "->,>>>,>>>,>>>,>>9")
        tt_debt2 = to_string(t_debt2, "->,>>>,>>>,>>>,>>9")
        tt_debt3 = to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
    else:
        tt_no = " "
        tt_supp = to_string(translateExtended ("T O T A L A/P:", lvcarea, "") , "x(30)")
        tt_saldo = to_string(t_saldo, "->>,>>>,>>>,>>9.99")
        tt_prev = to_string(t_prev, "->>,>>>,>>>,>>9.99")
        tt_debit = to_string(t_debit, "->>,>>>,>>>,>>9.99")
        tt_credit = to_string(t_credit, "->>,>>>,>>>,>>9.99")
        tt_debt0 = to_string(t_debt0, "->>,>>>,>>>,>>9.99")
        tt_debt1 = to_string(t_debt1, "->>,>>>,>>>,>>9.99")
        tt_debt2 = to_string(t_debt2, "->>,>>>,>>>,>>9.99")
        tt_debt3 = to_string(t_debt3, "->>,>>>,>>>,>>9.99")
    fill_in_list(False, "", "", "", "", "", "", "")
    tt_no = "-------"
    tt_supp = "------------------------------"
    tt_saldo = "------------------"
    tt_prev = "------------------"
    tt_debit = "------------------"
    tt_credit = "------------------"
    tt_debt0 = "------------------"
    tt_debt1 = "------------------"
    tt_debt2 = "------------------"
    tt_debt3 = "------------------"
    fill_in_list(False, "", "", "--------", "", "", "", "")
    tt_no = " "
    tt_supp = to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)")
    tt_saldo = " 100.00"
    tt_prev = ""
    tt_debit = ""
    tt_credit = ""
    tt_debt0 = to_string((t_debt0 / t_saldo * 100) , " ->>9.99")
    tt_debt1 = to_string((t_debt1 / t_saldo * 100) , " ->>9.99")
    tt_debt2 = to_string((t_debt2 / t_saldo * 100) , " ->>9.99")
    tt_debt3 = to_string((t_debt3 / t_saldo * 100) , " ->>9.99")
    fill_in_list(False, "", "", "", "", "", "", "")
    tt_no = ""
    tt_supp = ""
    tt_saldo = ""
    tt_prev = ""
    tt_debit = ""
    tt_credit = ""
    tt_debt0 = ""
    tt_debt1 = ""
    tt_debt2 = ""
    tt_debt3 = ""
    fill_in_list(False, "", "", "", "", "", "", "")

    return generate_output()