#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/8/2025
# Total nol, untuk flag-string = 1, menggunakan pay_amount
# Total Beda
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, L_kredit, Artikel, Bediener

def ap_paymentlist_webbl(all_supp:bool, remark_flag:bool, from_supp:string, from_date:date, to_date:date, from_remark:string, price_decimal:int, sort_type:int):

    prepare_cache ([L_lieferant, L_kredit, Artikel, Bediener])

    lief_nr1 = 0
    ap_exist = False
    err_code = 0
    ap_paymentlist_data = []
    t_list_data = []
    l_lieferant = l_kredit = artikel = bediener = None

    t_list = ap_paymentlist = None

    t_list_data, T_list = create_model("T_list", {"artnr":int, "bezeich":string, "betrag":Decimal})
    ap_paymentlist_data, Ap_paymentlist = create_model("Ap_paymentlist", {"srecid":int, "remark":string, "billdate":date, "docu_nr":string, "ap_amount":Decimal, "pay_amount":Decimal, "pay_date":date, "id":string, "pay_art":string, "supplier":string, "deliv_note":string, "bank_name":string, "bank_an":string, "bank_acc":string, "flag_string":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        return {"lief_nr1": lief_nr1, "ap_exist": ap_exist, "err_code": err_code, "ap-paymentlist": ap_paymentlist_data, "t-list": t_list_data}

    def create_list1():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1


                        t_credit =  to_decimal("0")
                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                if debt.netto == 0:
                    ap_paymentlist.ap_amount =  to_decimal(1.11)
                else:
                    ap_paymentlist.ap_amount =  to_decimal(debt.netto)

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        # ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        # ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list1a():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        curr_remark:string = ""
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_kredit.rgdatum, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True

                if curr_remark == "":
                    curr_remark = l_kredit.bemerk

                if curr_remark != l_kredit.bemerk:
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.pay_amount =  to_decimal(t_credit)
                    ap_paymentlist.flag_string = 1


                    t_credit =  to_decimal("0")
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.flag_string = 1
                    curr_remark = l_kredit.bemerk
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.flag_string = 1
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list1b():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        sub_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        curr_remark:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")
        curr_remark = ""

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0) & (L_kredit.lief_nr == lief_nr1)).order_by(L_kredit.rgdatum, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                sub_credit =  to_decimal(sub_credit) + to_decimal(l_kredit.saldo)
                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)


                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                if debt.netto == 0:
                    ap_paymentlist.ap_amount =  to_decimal("111111")

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


    def create_list2():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_lieferant.firma, Debt.rgdatum, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list2a():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        curr_remark:string = ""
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(Debt.rgdatum, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True

                if curr_remark == "":
                    curr_remark = l_kredit.bemerk

                if curr_remark != l_kredit.bemerk:
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.pay_amount =  to_decimal(t_credit)
                    ap_paymentlist.flag_string = 1
                    t_credit =  to_decimal("0")


                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.flag_string = 1


                    curr_remark = l_kredit.bemerk
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list2b():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        sub_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        curr_remark:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")
        curr_remark = ""

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0) & (L_kredit.lief_nr == lief_nr1)).order_by(Debt.rgdatum, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                sub_credit =  to_decimal(sub_credit) + to_decimal(l_kredit.saldo)
                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)


                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


    def create_list3():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_lieferant.firma, L_kredit.name, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list3a():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        curr_remark:string = ""
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_kredit.name, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True

                if curr_remark == "":
                    curr_remark = l_kredit.bemerk

                if curr_remark != l_kredit.bemerk:
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.pay_amount =  to_decimal(t_credit)
                    ap_paymentlist.flag_string = 1
                    t_credit =  to_decimal("0")


                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.flag_string = 1


                    curr_remark = l_kredit.bemerk
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list3b():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        sub_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        curr_remark:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")
        curr_remark = ""

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0) & (L_kredit.lief_nr == lief_nr1)).order_by(L_kredit.name, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                sub_credit =  to_decimal(sub_credit) + to_decimal(l_kredit.saldo)
                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)


                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


    def create_list4():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_lieferant.firma, L_kredit.lscheinnr, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list4a():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        lief_nr:int = 0
        do_it:bool = False
        curr_remark:string = ""
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_kredit.lscheinnr, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True

                if curr_remark == "":
                    curr_remark = l_kredit.bemerk

                if curr_remark != l_kredit.bemerk:
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.pay_amount =  to_decimal(t_credit)
                    ap_paymentlist.flag_string = 1
                    t_credit =  to_decimal("0")


                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.flag_string = 1


                    curr_remark = l_kredit.bemerk
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.flag_string = 1


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(tot_credit)
        ap_paymentlist.flag_string = 1


    def create_list4b():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, ap_paymentlist
        nonlocal t_list_data, ap_paymentlist_data

        artnr:int = 0
        t_credit:Decimal = to_decimal("0.0")
        sub_credit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        curr_remark:string = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")
        curr_remark = ""

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.lscheinnr, debt.bediener_nr, debt.netto, art.artnr, art.bezeich, art._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.lscheinnr, Debt.bediener_nr, Debt.netto, Art.artnr, Art.bezeich, Art._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0) & (L_kredit.lief_nr == lief_nr1)).order_by(L_kredit.lscheinnr, L_kredit.bemerk).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_data, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                sub_credit =  to_decimal(sub_credit) + to_decimal(l_kredit.saldo)
                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)


                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        ap_paymentlist = Ap_paymentlist()
                        ap_paymentlist_data.append(ap_paymentlist)

                        ap_paymentlist.pay_amount =  to_decimal(t_credit)
                        ap_paymentlist.flag_string = 1
                        t_credit =  to_decimal("0")


                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)

                ap_paymentlist.srecid = l_kredit._recid
                ap_paymentlist.billdate = debt.rgdatum
                ap_paymentlist.docu_nr = l_kredit.name
                ap_paymentlist.ap_amount =  to_decimal(debt.netto)
                ap_paymentlist.pay_amount =  to_decimal(l_kredit.saldo)
                ap_paymentlist.pay_date = l_kredit.rgdatum
                ap_paymentlist.pay_art = art.bezeich
                ap_paymentlist.supplier = receiver
                ap_paymentlist.deliv_note = l_kredit.lscheinnr
                ap_paymentlist.bank_name = entry(0, l_lieferant.bank, "a/n")
                ap_paymentlist.bank_an = substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3)
                ap_paymentlist.bank_acc = l_lieferant.kontonr
                ap_paymentlist.remark = l_kredit.bemerk

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = bediener.userinit
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.pay_amount =  to_decimal(t_credit)
        ap_paymentlist.flag_string = 1

    if sort_type == 1:

        if all_supp and not remark_flag:
            create_list2()

        elif all_supp and remark_flag:
            create_list2a()
        else:

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

            if not l_lieferant and from_supp != "":
                err_code = 1

                return generate_output()

            elif not l_lieferant and from_supp == "":
                all_supp = True
                err_code = 2
                create_list2()

            elif l_lieferant:
                lief_nr1 = l_lieferant.lief_nr
                all_supp = False
                err_code = 3
                create_list2b()

    elif sort_type == 2:

        if all_supp and not remark_flag:
            create_list3()

        elif all_supp and remark_flag:
            create_list3a()
        else:

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

            if not l_lieferant and from_supp != "":
                err_code = 1

                return generate_output()

            elif not l_lieferant and from_supp == "":
                all_supp = True
                err_code = 2
                create_list3()

            elif l_lieferant:
                lief_nr1 = l_lieferant.lief_nr
                all_supp = False
                err_code = 3
                create_list3b()

    elif sort_type == 3:

        if all_supp and not remark_flag:
            create_list4()

        elif all_supp and remark_flag:
            create_list4a()
        else:

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

            if not l_lieferant and from_supp != "":
                err_code = 1

                return generate_output()

            elif not l_lieferant and from_supp == "":
                all_supp = True
                err_code = 2
                create_list4()

            elif l_lieferant:
                lief_nr1 = l_lieferant.lief_nr
                all_supp = False
                err_code = 3
                create_list4b()
    else:

        if all_supp and not remark_flag:
            create_list1()

        elif all_supp and remark_flag:
            create_list1a()
        else:

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

            if not l_lieferant and from_supp != "":
                err_code = 1

                return generate_output()

            elif not l_lieferant and from_supp == "":
                all_supp = True
                err_code = 2
                create_list1()

            elif l_lieferant:
                lief_nr1 = l_lieferant.lief_nr
                all_supp = False
                err_code = 3
                create_list1b()

    return generate_output()