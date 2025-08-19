#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 19/8/2025
# credi-> credit
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import L_kredit, Htparam, L_lieferant, Queasy

def ap_age1_2_webbl(pvilanguage:int, to_date:date, from_name:string, to_name:string, detailed:bool, mi_bill:bool, segm:int, curr_disp:int, round_zero:bool):

    prepare_cache ([L_kredit, Htparam, L_lieferant, Queasy])

    apage_list1_data = []
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
    bemerk:string = ""
    day1:int = 30
    day2:int = 30
    day3:int = 30
    curr_saldo:Decimal = to_decimal("0.0")
    lvcarea:string = "ap-age1"
    l_kredit = htparam = l_lieferant = queasy = None

    apage_list = apage_list1 = debtrec = debt = age_list = None

    apage_list_data, Apage_list = create_model("Apage_list", {"docu_nr":string, "lschein":string, "rgdatum":string, "rechnr":string, "str":string, "bemerk":string})
    apage_list1_data, Apage_list1 = create_model("Apage_list1", {"docu_nr":string, "lschein":string, "rgdatum":string, "rechnr":string, "str":string, "nr":string, "firma":string, "prev_bal":string, "credit":string, "debit":string, "end_bal":string, "day":string, "day1":string, "day2":string, "day3":string, "bemerk":string})
    age_list_data, Age_list = create_model("Age_list", {"artnr":int, "rechnr":string, "lschein":string, "counter":int, "lief_nr":int, "rgdatum":date, "firma":string, "bemerk":string, "voucher_no":int, "p_bal":Decimal, "debit":Decimal, "credit":Decimal, "saldo":Decimal, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal})

    Debtrec = create_buffer("Debtrec",L_kredit)
    Debt = create_buffer("Debt",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        return {"apage-list1": apage_list1_data}

    def age_list():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.rgdatum = l_kredit.rgdatum
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal("0")
                    age_list.firma = l_lieferant.firma
                    age_list.rechnr = l_kredit.name
                    age_list.voucher_no = l_kredit.rechnr
                    age_list.bemerk = l_kredit.bemerk
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
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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
                age_list_data.append(age_list)

                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(l_kredit.netto)
                age_list.firma = l_lieferant.firma
                age_list.rechnr = l_kredit.name
                guest_name = l_lieferant.firma
                age_list.voucher_no = l_kredit.rechnr
                age_list.bemerk = l_kredit.bemerk


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
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def age_list1():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_data.append(age_list)

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
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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
                age_list_data.append(age_list)

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
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def age_list2():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                if (l_kredit.counter == 0) or (not age_list):
                    age_list = Age_list()
                    age_list_data.append(age_list)

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
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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
                age_list_data.append(age_list)

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
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def age_list3():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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

                        age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == l_kredit.counter), first=True)

                    if (l_kredit.counter == 0) or (not age_list):
                        age_list = Age_list()
                        age_list_data.append(age_list)

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
        counter = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.counter, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit.name, l_kredit.rechnr, l_kredit.bemerk, l_kredit.lscheinnr, l_kredit.netto, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit.name, L_kredit.rechnr, L_kredit.bemerk, L_kredit.lscheinnr, L_kredit.netto, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
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
                    age_list_data.append(age_list)

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
        counter = 0
        curr_lief_nr = 0
        curr_name = ""


    def create_total():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        if not detailed:

            for age_list in query(age_list_data, sort_by=[("firma",False)]):

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 =  to_decimal(age_list.tot_debt)

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 =  to_decimal(age_list.tot_debt)

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 =  to_decimal(age_list.tot_debt)
                else:
                    age_list.debt0 =  to_decimal(age_list.tot_debt)

                if round_zero:
                    t_saldo =  to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
                    t_prev =  to_decimal(t_prev) + to_decimal(age_list.p_bal)
                    t_debit =  to_decimal(t_debit) + to_decimal(age_list.debit)
                    # Rd 19/8/2025
                    # t_credit =  to_decimal(t_credit) + to_decimal(age_list.credi)
                    t_credit =  to_decimal(t_credit) + to_decimal(age_list.credit)
                    t_debt0 =  to_decimal(t_debt0) + to_decimal(age_list.debt0)
                    t_debt1 =  to_decimal(t_debt1) + to_decimal(age_list.debt1)
                    t_debt2 =  to_decimal(t_debt2) + to_decimal(age_list.debt2)
                    t_debt3 =  to_decimal(t_debt3) + to_decimal(age_list.debt3)
                else:
                    t_saldo =  to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
                    t_prev =  to_decimal(t_prev) + to_decimal(age_list.p_bal)
                    t_debit =  to_decimal(t_debit) + to_decimal(age_list.debit)
                    t_credit =  to_decimal(t_credit) + to_decimal(age_list.credit)
                    t_debt0 =  to_decimal(t_debt0) + to_decimal(age_list.debt0)
                    t_debt1 =  to_decimal(t_debt1) + to_decimal(age_list.debt1)
                    t_debt2 =  to_decimal(t_debt2) + to_decimal(age_list.debt2)
                    t_debt3 =  to_decimal(t_debt3) + to_decimal(age_list.debt3)

                if curr_lief_nr == 0:

                    if round_zero:
                        curr_rgdatum = to_string(age_list.rgdatum, "99/99/99")
                        curr_po = age_list.rechnr
                        curr_lschein = age_list.lschein
                        firma = age_list.firma
                        tot_debt = to_decimal(round(age_list.tot_debt , 0))
                        p_bal = to_decimal(round(age_list.p_bal , 0))
                        debit = to_decimal(round(age_list.debit , 0))
                        credit = to_decimal(round(age_list.credit , 0))
                        debt0 = to_decimal(round(age_list.debt0 , 0))
                        debt1 = to_decimal(round(age_list.debt1 , 0))
                        debt2 = to_decimal(round(age_list.debt2 , 0))
                        debt3 = to_decimal(round(age_list.debt3 , 0))
                        bemerk = age_list.bemerk


                        counter = counter + 1
                    else:
                        curr_rgdatum = to_string(age_list.rgdatum, "99/99/99")
                        curr_po = age_list.rechnr
                        curr_lschein = age_list.lschein
                        firma = age_list.firma
                        tot_debt =  to_decimal(age_list.tot_debt)
                        p_bal =  to_decimal(age_list.p_bal)
                        debit =  to_decimal(age_list.debit)
                        credit =  to_decimal(age_list.credit)
                        debt0 =  to_decimal(age_list.debt0)
                        debt1 =  to_decimal(age_list.debt1)
                        debt2 =  to_decimal(age_list.debt2)
                        debt3 =  to_decimal(age_list.debt3)
                        bemerk = age_list.bemerk
                        counter = counter + 1

                elif curr_name != age_list.firma:

                    if p_bal != 0 or debit != 0 or credit != 0:
                        outlist = " " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                        fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, "")
                        curr_po = age_list.rechnr
                        curr_lschein = age_list.lschein


                    else:
                        counter = counter - 1

                    if round_zero:
                        firma = age_list.firma
                        tot_debt = to_decimal(round(age_list.tot_debt , 0))
                        p_bal = to_decimal(round(age_list.p_bal , 0))
                        debit = to_decimal(round(age_list.debit , 0))
                        credit = to_decimal(round(age_list.credit , 0))
                        debt0 = to_decimal(round(age_list.debt0 , 0))
                        debt1 = to_decimal(round(age_list.debt1 , 0))
                        debt2 = to_decimal(round(age_list.debt2 , 0))
                        debt3 = to_decimal(round(age_list.debt3 , 0))
                        counter = counter + 1
                        bemerk = age_list.bemerk
                    else:
                        firma = age_list.firma
                        tot_debt =  to_decimal(age_list.tot_debt)
                        p_bal =  to_decimal(age_list.p_bal)
                        debit =  to_decimal(age_list.debit)
                        credit =  to_decimal(age_list.credit)
                        debt0 =  to_decimal(age_list.debt0)
                        debt1 =  to_decimal(age_list.debt1)
                        debt2 =  to_decimal(age_list.debt2)
                        debt3 =  to_decimal(age_list.debt3)
                        counter = counter + 1
                        bemerk = age_list.bemerk
                else:

                    if round_zero:
                        tot_debt = to_decimal(tot_debt + round(age_list.tot_debt , 0))
                        p_bal = to_decimal(p_bal + round(age_list.p_bal , 0))
                        debit = to_decimal(debit + round(age_list.debit , 0))
                        credit = to_decimal(credit + round(age_list.credit , 0))
                        debt0 = to_decimal(debt0 + round(age_list.debt0 , 0))
                        debt1 = to_decimal(debt1 + round(age_list.debt1 , 0))
                        debt2 = to_decimal(debt2 + round(age_list.debt2 , 0))
                        debt3 = to_decimal(debt3 + round(age_list.debt3 , 0))
                    else:
                        tot_debt =  to_decimal(tot_debt) + to_decimal(age_list.tot_debt)
                        p_bal =  to_decimal(p_bal) + to_decimal(age_list.p_bal)
                        debit =  to_decimal(debit) + to_decimal(age_list.debit)
                        credit =  to_decimal(credit) + to_decimal(age_list.credit)
                        debt0 =  to_decimal(debt0) + to_decimal(age_list.debt0)
                        debt1 =  to_decimal(debt1) + to_decimal(age_list.debt1)
                        debt2 =  to_decimal(debt2) + to_decimal(age_list.debt2)
                        debt3 =  to_decimal(debt3) + to_decimal(age_list.debt3)
                curr_lief_nr = age_list.lief_nr

                if not detailed:
                    curr_name = age_list.firma
                age_list_data.remove(age_list)
        else:

            if not mi_bill:

                for age_list in query(age_list_data, sort_by=[("firma",False)]):
                    add_detail_date()


            for age_list in query(age_list_data, sort_by=[("rgdatum",False)]):
                add_detail_date()

        if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0) and not detailed:
            outlist = " " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
            fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, "")
        else:
            counter = counter - 1
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "", "", "--------", "")

        if round_zero:
            outlist = " " + to_string(translateExtended ("T O T A L A/P:", lvcarea, "") , "x(30)") + to_string(round(t_saldo, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_prev, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debit, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_credit, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt0, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt1, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt2, 0) , "->>,>>>,>>>,>>9.99") + to_string(round(t_debt3, 0) , "->>,>>>,>>>,>>9.99")
        else:
            outlist = " " + to_string(translateExtended ("T O T A L A/P:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>9.99") + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list(False, "", "", "", "")
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "", "", "--------", "")
        outlist = " " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + " 100.00"
        for i in range(1,54 + 1) :
            outlist = outlist + " "
        outlist = outlist + to_string((t_debt0 / t_saldo * 100) , " ->>9.99") + to_string((t_debt1 / t_saldo * 100) , " ->>9.99") + to_string((t_debt2 / t_saldo * 100) , " ->>9.99") + to_string((t_debt3 / t_saldo * 100) , " ->>9.99")
        fill_in_list(False, "", "", "", "")
        outlist = ""
        fill_in_list(False, "", "", "", "")


    def fill_in_list(fill_billno:bool, curr_po:string, curr_lschein:string, curr_rgdatum:string, voucher_no:string):

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data


        apage_list = Apage_list()
        apage_list_data.append(apage_list)


        if fill_billno:
            apage_list.docu_nr = curr_po
            apage_list.lschein = curr_lschein
            apage_list.rgdatum = curr_rgdatum
            apage_list.rechnr = voucher_no
            apage_list.bemerk = bemerk


        apage_list.str = outlist

        if substring(outlist, 0, 5) == ("-----").lower() :
            apage_list.docu_nr = "----------------"
            apage_list.lschein = "-------------------"
            apage_list.rgdatum = "--------"
            apage_list.rechnr = "----------"
            apage_list.bemerk = "--------"


    def add_detail_date():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        if to_date - age_list.rgdatum > day3:
            age_list.debt3 =  to_decimal(age_list.tot_debt)

        elif to_date - age_list.rgdatum > day2:
            age_list.debt2 =  to_decimal(age_list.tot_debt)

        elif to_date - age_list.rgdatum > day1:
            age_list.debt1 =  to_decimal(age_list.tot_debt)
        else:
            age_list.debt0 =  to_decimal(age_list.tot_debt)

        if round_zero:
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
            tot_debt = to_decimal(round(age_list.tot_debt , 0))
            p_bal = to_decimal(round(age_list.p_bal , 0))
            debit = to_decimal(round(age_list.debit , 0))
            credit = to_decimal(round(age_list.credit , 0))
            debt0 = to_decimal(round(age_list.debt0 , 0))
            debt1 = to_decimal(round(age_list.debt1 , 0))
            debt2 = to_decimal(round(age_list.debt2 , 0))
            debt3 = to_decimal(round(age_list.debt3 , 0))
            bemerk = age_list.bemerk


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
            bemerk = age_list.bemerk

        if p_bal != 0 or debit != 0 or credit != 0:
            outlist = " " + to_string(counter, ">>>9 ") + to_string(firma, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
            fill_in_list(True, curr_po, curr_lschein, curr_rgdatum, voucher_no)
            curr_po = age_list.rechnr
            curr_lschein = age_list.lschein
            voucher_no = to_string(age_list.voucher_no)
            bemerk = age_list.bemerk


        else:
            counter = counter - 1
        age_list_data.remove(age_list)


    def create_apage_list1():

        nonlocal apage_list1_data, billdate, curr_lief_nr, curr_art, counter, i, curr_name, firma, curr_po, curr_lschein, p_bal, debit, credit, debt0, debt1, debt2, debt3, tot_debt, t_comm, t_adjust, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_rgdatum, from_date, guest_name, curr_bezeich, outlist, do_it, price_decimal, voucher_no, bemerk, day1, day2, day3, curr_saldo, lvcarea, l_kredit, htparam, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, detailed, mi_bill, segm, curr_disp, round_zero
        nonlocal debtrec, debt


        nonlocal apage_list, apage_list1, debtrec, debt, age_list
        nonlocal apage_list_data, apage_list1_data, age_list_data

        for apage_list in query(apage_list_data, filters=(lambda apage_list: not matches(apage_list.str,r"*---*"))):
            apage_list1 = Apage_list1()
            apage_list1_data.append(apage_list1)

            buffer_copy(apage_list, apage_list1)
            apage_list1.nr = substring(apage_list.str, 0, 7)
            apage_list1.firma = substring(apage_list.str, 7, 30)
            apage_list1.prev_bal = substring(apage_list.str, 55, 18)
            apage_list1.credit = substring(apage_list.str, 73, 18)
            apage_list1.debit = substring(apage_list.str, 91, 18)
            apage_list1.end_bal = substring(apage_list.str, 37, 18)
            apage_list1.day = substring(apage_list.str, 109, 18)
            apage_list1.day1 = substring(apage_list.str, 127, 18)
            apage_list1.day2 = substring(apage_list.str, 145, 18)
            apage_list1.day3 = substring(apage_list.str, 163, 18)
            apage_list1.bemerk = apage_list.bemerk

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
    create_total()
    create_apage_list1()

    return generate_output()