#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, L_kredit, Artikel, Bediener

def ap_paymentlistbl(all_supp:bool, remark_flag:bool, from_supp:string, from_date:date, to_date:date, from_remark:string, price_decimal:int):

    prepare_cache ([L_lieferant, L_kredit, Artikel, Bediener])

    lief_nr1 = 0
    ap_exist = False
    err_code = 0
    ap_paymentlist_data = []
    t_list_data = []
    amount:string = ""
    l_lieferant = l_kredit = artikel = bediener = None

    t_list = output_list = ap_paymentlist = None

    t_list_data, T_list = create_model("T_list", {"artnr":int, "bezeich":string, "betrag":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"srecid":int, "remark":string, "str":string})
    ap_paymentlist_data, Ap_paymentlist = create_model("Ap_paymentlist", {"srecid":int, "remark":string, "billdate":date, "docu_nr":string, "ap_amount":Decimal, "pay_amount":Decimal, "pay_date":date, "id":string, "pay_art":string, "supplier":string, "deliv_note":string, "bank_name":string, "bank_an":string, "bank_acc":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, amount, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal


        nonlocal t_list, output_list, ap_paymentlist
        nonlocal t_list_data, output_list_data, ap_paymentlist_data

        return {"lief_nr1": lief_nr1, "ap_exist": ap_exist, "err_code": err_code, "ap-paymentlist": ap_paymentlist_data, "t-list": t_list_data}

    def create_list1():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, amount, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal


        nonlocal t_list, output_list, ap_paymentlist
        nonlocal t_list_data, output_list_data, ap_paymentlist_data

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
        output_list_data.clear()
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.bediener_nr, l_kredit.lscheinnr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.bediener_nr, debt.lscheinnr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.bediener_nr, L_kredit.lscheinnr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.bediener_nr, Debt.lscheinnr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
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

                        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
                        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

                        if price_decimal == 0:
                            ap_paymentlist.ap_amount =  to_decimal("0")
                            ap_paymentlist.pay_amount =  to_decimal(to_decimal(to_string(t_credit , "->>>,>>>,>>>,>>>,>>>,>>9")))
                        else:
                            ap_paymentlist.ap_amount =  to_decimal("0")
                            ap_paymentlist.pay_amount =  to_decimal(to_decimal(to_string(t_credit , "->,>>>,>>>,>>>,>>>,>>9.99")))
                        t_credit =  to_decimal("0")
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.billdate = date_mdy(to_string(" ", "x(8)"))
                    ap_paymentlist.docu_nr = trim(to_string(receiver, "x(30)"))
                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)


                if price_decimal == 0:
                    ap_paymentlist.srecid = l_kredit._recid
                    ap_paymentlist.billdate = date_mdy(trim(to_string(debt.rgdatum)))
                    ap_paymentlist.docu_nr = trim(to_string(l_kredit.name, "x(30)"))
                    ap_paymentlist.ap_amount =  to_decimal(to_decimal(trim(to_string(debt.netto , "->>>,>>>,>>>,>>>,>>>,>>9"))) )
                    ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(l_kredit.saldo , "->>>,>>>,>>>,>>>,>>>,>>9"))) )
                    ap_paymentlist.pay_date = date_mdy(trim(to_string(l_kredit.rgdatum)))


                else:
                    ap_paymentlist.srecid = l_kredit._recid
                    ap_paymentlist.billdate = date_mdy(trim(to_string(debt.rgdatum)))
                    ap_paymentlist.docu_nr = trim(to_string(l_kredit.name, "x(30)"))
                    ap_paymentlist.ap_amount =  to_decimal(to_decimal(trim(to_string(debt.netto , "->,>>>,>>>,>>>,>>>,>>9.99"))) )
                    ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(l_kredit.saldo , "->,>>>,>>>,>>>,>>>,>>9.99"))) )
                    ap_paymentlist.pay_date = date_mdy(trim(to_string(l_kredit.rgdatum)))

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = trim(to_string(bediener.userinit, "x(3)"))
                else:
                    ap_paymentlist.id = trim(to_string(" ", "x(3)"))
                ap_paymentlist.pay_art = to_string(art.bezeich, "x(20)")
                ap_paymentlist.supplier = to_string(receiver, "x(24)")
                ap_paymentlist.deliv_note = to_string(l_kredit.lscheinnr, "x(30)")
                ap_paymentlist.bank_name = to_string(entry(0, l_lieferant.bank, "a/n") , "x(35)")
                ap_paymentlist.bank_an = to_string(substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3) , "x(35)")
                ap_paymentlist.bank_acc = to_string(l_lieferant.kontonr, "x(35)")
                ap_paymentlist.remark = l_kredit.bemerk
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

        if price_decimal == 0:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->>>,>>>,>>>,>>>,>>>,>>9"))))
        else:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->,>>>,>>>,>>>,>>>,>>9.99"))))
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

        if price_decimal == 0:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(tot_credit , "->>>,>>>,>>>,>>>,>>>,>>9"))))
        else:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(tot_credit , "->,>>>,>>>,>>>,>>>,>>9.99"))))


    def create_list1a():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, amount, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal


        nonlocal t_list, output_list, ap_paymentlist
        nonlocal t_list_data, output_list_data, ap_paymentlist_data

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
        output_list_data.clear()
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        l_lieferant = L_lieferant()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.bediener_nr, l_kredit.lscheinnr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.bediener_nr, debt.lscheinnr, debt.netto, art.artnr, art.bezeich, art._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.lief_nr, l_lieferant.bank, l_lieferant.kontonr, l_lieferant._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.bediener_nr, L_kredit.lscheinnr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.bediener_nr, Debt.lscheinnr, Debt.netto, Art.artnr, Art.bezeich, Art._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.lief_nr, L_lieferant.bank, L_lieferant.kontonr, L_lieferant._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
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

                    ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
                    ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

                    if price_decimal == 0:
                        ap_paymentlist.ap_amount =  to_decimal("0")
                        ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->,>>>,>>>,>>>,>>9.99"))))
                    else:
                        ap_paymentlist.ap_amount =  to_decimal("0")
                        ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->,>>>,>>>,>>>,>>9.99"))))
                    t_credit =  to_decimal("0")
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    curr_remark = l_kredit.bemerk
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)


                if price_decimal == 0:
                    ap_paymentlist.srecid = l_kredit._recid
                    ap_paymentlist.billdate = date_mdy(trim(to_string(debt.rgdatum)))
                    ap_paymentlist.docu_nr = trim(to_string(l_kredit.name, "x(30)"))
                    ap_paymentlist.ap_amount =  to_decimal(to_decimal(trim(to_string(debt.netto , "->>>,>>>,>>>,>>>,>>9"))) )
                    ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(l_kredit.saldo , " ->>>,>>>,>>>,>>>,>>9"))) )
                    ap_paymentlist.pay_date = date_mdy(trim(to_string(l_kredit.rgdatum)))


                else:
                    ap_paymentlist.srecid = l_kredit._recid
                    ap_paymentlist.billdate = date_mdy(trim(to_string(debt.rgdatum)))
                    ap_paymentlist.docu_nr = trim(to_string(l_kredit.name, "x(30)"))
                    ap_paymentlist.ap_amount =  to_decimal(to_decimal(trim(to_string(debt.netto , "->,>>>,>>>,>>>,>>9.99"))) )
                    ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(l_kredit.saldo , "->,>>>,>>>,>>>,>>9.99"))) )
                    ap_paymentlist.pay_date = date_mdy(trim(to_string(l_kredit.rgdatum)))

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = trim(to_string(bediener.userinit, "x(3)"))
                else:
                    ap_paymentlist.id = trim(to_string(" ", "x(3)"))
                ap_paymentlist.pay_art = to_string(art.bezeich, "x(20)")
                ap_paymentlist.supplier = to_string(receiver, "x(24)")
                ap_paymentlist.deliv_note = to_string(l_kredit.lscheinnr, "x(30)")
                ap_paymentlist.bank_name = to_string(entry(0, l_lieferant.bank, "a/n") , "x(35)")
                ap_paymentlist.bank_an = to_string(substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3) , "x(35)")
                ap_paymentlist.bank_acc = to_string(l_lieferant.kontonr, "x(35)")
                ap_paymentlist.remark = l_kredit.bemerk
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

        if price_decimal == 0:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(tot_credit , "->>>,>>>,>>>,>>>,>>9"))))
        else:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(tot_credit , "->,>>>,>>>,>>>,>>9.99"))))
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

        if price_decimal == 0:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(tot_credit , "->>>,>>>,>>>,>>>,>>>,>>9"))))
        else:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(tot_credit , "->,>>>,>>>,>>>,>>>,>>9.99"))))


    def create_list2():

        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_data, t_list_data, amount, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal


        nonlocal t_list, output_list, ap_paymentlist
        nonlocal t_list_data, output_list_data, ap_paymentlist_data

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
        output_list_data.clear()
        t_list_data.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")
        curr_remark = ""

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        debt = L_kredit()
        art = Artikel()
        for l_kredit.bemerk, l_kredit.zahlkonto, l_kredit.saldo, l_kredit._recid, l_kredit.name, l_kredit.rgdatum, l_kredit.bediener_nr, l_kredit.lscheinnr, l_kredit.netto, debt.bemerk, debt.zahlkonto, debt.saldo, debt._recid, debt.name, debt.rgdatum, debt.bediener_nr, debt.lscheinnr, debt.netto, art.artnr, art.bezeich, art._recid in db_session.query(L_kredit.bemerk, L_kredit.zahlkonto, L_kredit.saldo, L_kredit._recid, L_kredit.name, L_kredit.rgdatum, L_kredit.bediener_nr, L_kredit.lscheinnr, L_kredit.netto, Debt.bemerk, Debt.zahlkonto, Debt.saldo, Debt._recid, Debt.name, Debt.rgdatum, Debt.bediener_nr, Debt.lscheinnr, Debt.netto, Art.artnr, Art.bezeich, Art._recid).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).filter(
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

                        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
                        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

                        if price_decimal == 0:
                            ap_paymentlist.ap_amount =  to_decimal("0")
                            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->>>,>>>,>>>,>>>,>>>,>>9"))))
                        else:
                            ap_paymentlist.ap_amount =  to_decimal("0")
                            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->,>>>,>>>,>>>,>>>,>>9.99"))))
                        t_credit =  to_decimal("0")
                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist = Ap_paymentlist()
                    ap_paymentlist_data.append(ap_paymentlist)

                    ap_paymentlist.billdate = date_mdy(to_string(" ", "x(8)"))
                    ap_paymentlist.docu_nr = trim(to_string(receiver, "x(30)"))
                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                ap_paymentlist = Ap_paymentlist()
                ap_paymentlist_data.append(ap_paymentlist)


                if price_decimal == 0:
                    ap_paymentlist.srecid = l_kredit._recid
                    ap_paymentlist.billdate = date_mdy(trim(to_string(debt.rgdatum)))
                    ap_paymentlist.docu_nr = trim(to_string(l_kredit.name, "x(30)"))
                    ap_paymentlist.ap_amount =  to_decimal(to_decimal(trim(to_string(debt.netto , "->>>,>>>,>>>,>>>,>>>,>>9"))) )
                    ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(l_kredit.saldo , "->>>,>>>,>>>,>>>,>>9"))) )
                    ap_paymentlist.pay_date = date_mdy(trim(to_string(l_kredit.rgdatum)))


                else:
                    ap_paymentlist.srecid = l_kredit._recid
                    ap_paymentlist.billdate = date_mdy(trim(to_string(debt.rgdatum)))
                    ap_paymentlist.docu_nr = trim(to_string(l_kredit.name, "x(30)"))
                    ap_paymentlist.ap_amount =  to_decimal(to_decimal(trim(to_string(debt.netto , "->,>>>,>>>,>>>,>>>,>>9.99"))) )
                    ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(l_kredit.saldo , "->,>>>,>>>,>>>,>>>,>>9.99"))) )
                    ap_paymentlist.pay_date = date_mdy(trim(to_string(l_kredit.rgdatum)))

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    ap_paymentlist.id = trim(to_string(bediener.userinit, "x(3)"))
                else:
                    ap_paymentlist.id = trim(to_string(" ", "x(3)"))
                ap_paymentlist.pay_art = to_string(art.bezeich, "x(20)")
                ap_paymentlist.supplier = to_string(receiver, "x(24)")
                ap_paymentlist.deliv_note = to_string(l_kredit.lscheinnr, "x(30)")
                ap_paymentlist.bank_name = to_string(entry(0, l_lieferant.bank, "a/n") , "x(35)")
                ap_paymentlist.bank_an = to_string(substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3) , "x(35)")
                ap_paymentlist.bank_acc = to_string(l_lieferant.kontonr, "x(35)")
                ap_paymentlist.remark = l_kredit.bemerk
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)


        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_data.append(ap_paymentlist)

        ap_paymentlist.billdate = date_mdy(trim(to_string(" ", "x(8)")))
        ap_paymentlist.docu_nr = trim(to_string(" ", "x(30)"))

        if price_decimal == 0:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->>>,>>>,>>>,>>>,>>>,>>9"))))
        else:
            ap_paymentlist.ap_amount =  to_decimal("0")
            ap_paymentlist.pay_amount =  to_decimal(to_decimal(trim(to_string(t_credit , "->,>>>,>>>,>>>,>>>,>>9.99"))))


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
            create_list2()

    return generate_output()