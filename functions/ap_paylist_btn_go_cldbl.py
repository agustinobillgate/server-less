#using conversion tools version: 1.0.0.61

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, L_kredit, Artikel, Bediener

def ap_paylist_btn_go_cldbl(all_supp:bool, remark_flag:bool, from_supp:str, from_date:date, to_date:date, from_remark:str, price_decimal:int):
    lief_nr1 = 0
    ap_exist = False
    err_code = 0
    output_list_list = []
    t_list_list = []
    l_lieferant = l_kredit = artikel = bediener = None

    t_list = output_list = obuff = None

    t_list_list, T_list = create_model("T_list", {"artnr":int, "bezeich":str, "betrag":decimal})
    output_list_list, Output_list = create_model("Output_list", {"srecid":int, "remark":str, "str":str})

    Obuff = Output_list
    obuff_list = output_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr1, ap_exist, err_code, output_list_list, t_list_list, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal
        nonlocal obuff


        nonlocal t_list, output_list, obuff
        nonlocal t_list_list, output_list_list

        return {"lief_nr1": lief_nr1, "ap_exist": ap_exist, "err_code": err_code, "output-list": output_list_list, "t-list": t_list_list}

    def create_list1():

        nonlocal lief_nr1, ap_exist, err_code, output_list_list, t_list_list, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal
        nonlocal obuff


        nonlocal t_list, output_list, obuff
        nonlocal t_list_list, output_list_list

        artnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        i:int = 0
        receiver:str = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        output_list_list.clear()
        t_list_list.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = []
        for l_kredit, debt, art, l_lieferant in db_session.query(L_kredit, Debt, Art, L_lieferant).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum, L_kredit.bemerk).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_list, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,49 + 1) :
                            output_list.str = output_list.str + " "

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string("TOTAL", "x(8)") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>>,>>9")
                        else:
                            output_list.str = output_list.str + to_string("TOTAL", "x(8)") + to_string(t_credit, "->,>>>,>>>,>>>,>>>,>>9.99")
                        t_credit =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("", "x(8)") + to_string(receiver, "x(30)")
                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                output_list = Output_list()
                output_list_list.append(output_list)


                if price_decimal == 0:
                    output_list.srecid = l_kredit._recid
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(l_kredit.name, "x(30)") +\
                        to_string(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") +\
                        to_string(l_kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") +\
                        to_string(l_kredit.rgdatum)


                else:
                    output_list.srecid = l_kredit._recid
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(l_kredit.name, "x(30)") +\
                        to_string(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") +\
                        to_string(l_kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99") +\
                        to_string(l_kredit.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str +\
                        to_string(art.bezeich, "x(20)") +\
                        to_string(l_kredit.bemerk, "x(32)") +\
                        to_string(receiver, "x(24)") +\
                        to_string(l_kredit.lscheinnr, "x(30)") +\
                        to_string(l_kredit.zahlkonto, "99999") +\
                        to_string(l_kredit.rechnr, ">>,>>9") +\
                        to_string(art.bezeich, "x(35)") +\
                        to_string(entry(0, l_lieferant.bank, "a/n") , "x(35)") +\
                        to_string(substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3) , "x(35)") +\
                        to_string(l_lieferant.kontonr, "x(35)")
                output_list.remark = l_kredit.bemerk
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)


        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,49 + 1) :
            output_list.str = output_list.str + " "

        if price_decimal == 0:
            output_list.str = output_list.str + to_string("TOTAL", "x(8)") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string("TOTAL", "x(8)") + to_string(t_credit, "->,>>>,>>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,43 + 1) :
            output_list.str = output_list.str + " "

        if price_decimal == 0:
            output_list.str = output_list.str + to_string("Grand TOTAL", "x(14)") + to_string(tot_credit, "->>>,>>>,>>>,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string("Grand TOTAL", "x(14)") + to_string(tot_credit, "->,>>>,>>>,>>>,>>>,>>9.99")


    def create_list1a():

        nonlocal lief_nr1, ap_exist, err_code, output_list_list, t_list_list, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal
        nonlocal obuff


        nonlocal t_list, output_list, obuff
        nonlocal t_list_list, output_list_list

        artnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        i:int = 0
        receiver:str = ""
        lief_nr:int = 0
        do_it:bool = False
        curr_remark:str = ""
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        output_list_list.clear()
        t_list_list.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")

        l_kredit_obj_list = []
        for l_kredit, debt, art, l_lieferant in db_session.query(L_kredit, Debt, Art, L_lieferant).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0)).order_by(L_kredit.rgdatum, L_kredit.bemerk).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_list, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)
                ap_exist = True

                if curr_remark == "":
                    curr_remark = l_kredit.bemerk

                if curr_remark != l_kredit.bemerk:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,49 + 1) :
                        output_list.str = output_list.str + " "

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    t_credit =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_remark = l_kredit.bemerk
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                output_list = Output_list()
                output_list_list.append(output_list)


                if price_decimal == 0:
                    output_list.srecid = l_kredit._recid
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(l_kredit.name, "x(30)") +\
                        to_string(debt.netto, "->>>,>>>,>>>,>>>,>>9") +\
                        to_string(l_kredit.saldo, " ->>>,>>>,>>>,>>>,>>9") +\
                        to_string(l_kredit.rgdatum)


                else:
                    output_list.srecid = l_kredit._recid
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(l_kredit.name, "x(30)") +\
                        to_string(debt.netto, "->,>>>,>>>,>>>,>>9.99") +\
                        to_string(l_kredit.saldo, "->,>>>,>>>,>>>,>>9.99") +\
                        to_string(l_kredit.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str +\
                        to_string(art.bezeich, "x(20)") +\
                        to_string(l_kredit.bemerk, "x(32)") +\
                        to_string(receiver, "x(24)") +\
                        to_string(l_kredit.lscheinnr, "x(30)") +\
                        to_string(l_kredit.zahlkonto, "99999") +\
                        to_string(l_kredit.rechnr, ">>,>>9") +\
                        to_string(art.bezeich, "x(35)") +\
                        to_string(entry(0, l_lieferant.bank, "a/n") , "x(35)") +\
                        to_string(substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3) , "x(35)") +\
                        to_string(l_lieferant.kontonr, "x(35)")
                output_list.remark = l_kredit.bemerk
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)


        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,49 + 1) :
            output_list.str = output_list.str + " "

        if price_decimal == 0:
            output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,43 + 1) :
            output_list.str = output_list.str + " "

        if price_decimal == 0:
            output_list.str = output_list.str + to_string("Grand TOTAL", "x(12)") + to_string(tot_credit, "->>>,>>>,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string("Grand TOTAL", "x(12)") + to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")


    def create_list2():

        nonlocal lief_nr1, ap_exist, err_code, output_list_list, t_list_list, l_lieferant, l_kredit, artikel, bediener
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal
        nonlocal obuff


        nonlocal t_list, output_list, obuff
        nonlocal t_list_list, output_list_list

        artnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        sub_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        i:int = 0
        receiver:str = ""
        curr_remark:str = ""
        lief_nr:int = 0
        do_it:bool = False
        debt = None
        art = None
        Debt =  create_buffer("Debt",L_kredit)
        Art =  create_buffer("Art",Artikel)
        ap_exist = False
        output_list_list.clear()
        t_list_list.clear()
        lief_nr = 0
        t_credit =  to_decimal("0")
        curr_remark = ""

        l_kredit_obj_list = []
        for l_kredit, debt, art in db_session.query(L_kredit, Debt, Art).join(Debt,(Debt.counter == L_kredit.counter) & (Debt.zahlkonto == 0)).join(Art,(Art.artnr == L_kredit.zahlkonto) & (Art.departement == 0)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto != 0) & (L_kredit.lief_nr == lief_nr1)).order_by(L_kredit.rgdatum, L_kredit.bemerk).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if from_remark != "" and not matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = False

            elif from_remark != "" and matches(l_kredit.bemerk,r"*" + from_remark + r"*"):
                do_it = True

            if do_it:
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                t_list = query(t_list_list, filters=(lambda t_list: t_list.artnr == l_kredit.zahlkonto), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = art.artnr
                    t_list.bezeich = art.bezeich


                sub_credit =  to_decimal(sub_credit) + to_decimal(l_kredit.saldo)
                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(l_kredit.saldo)


                ap_exist = True
                receiver = l_lieferant.firma + ", " + l_lieferant.anredefirma

                if lief_nr != l_lieferant.lief_nr:

                    if lief_nr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,49 + 1) :
                            output_list.str = output_list.str + " "

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>>,>>9")
                        else:
                            output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->,>>>,>>>,>>>,>>>,>>9.99")
                        t_credit =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + " " + to_string(receiver, "x(30)")
                    lief_nr = l_lieferant.lief_nr
                t_credit =  to_decimal(t_credit) + to_decimal(l_kredit.saldo)
                output_list = Output_list()
                output_list_list.append(output_list)


                if price_decimal == 0:
                    output_list.srecid = l_kredit._recid
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(l_kredit.name, "x(30)") +\
                        to_string(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") +\
                        to_string(l_kredit.saldo, "->>>,>>>,>>>,>>>,>>9") +\
                        to_string(l_kredit.rgdatum)


                else:
                    output_list.srecid = l_kredit._recid
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(l_kredit.name, "x(30)") +\
                        to_string(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") +\
                        to_string(l_kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99") +\
                        to_string(l_kredit.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str +\
                        to_string(art.bezeich, "x(20)") +\
                        to_string(l_kredit.bemerk, "x(32)") +\
                        to_string(receiver, "x(24)") +\
                        to_string(l_kredit.lscheinnr, "x(30)") +\
                        to_string(l_kredit.zahlkonto, "99999") +\
                        to_string(l_kredit.rechnr, ">>,>>9") +\
                        to_string(art.bezeich, "x(35)") +\
                        to_string(entry(0, l_lieferant.bank, "a/n") , "x(35)") +\
                        to_string(substring(l_lieferant.bank, length(entry(0, l_lieferant.bank, "a/n")) + 5 - 1, length(l_lieferant.bank) - length(entry(0, l_lieferant.bank, "a/n")) - 3) , "x(35)") +\
                        to_string(l_lieferant.kontonr, "x(35)")
                output_list.remark = l_kredit.bemerk
                tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)


        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,49 + 1) :
            output_list.str = output_list.str + " "

        if price_decimal == 0:
            output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->>>,>>>,>>>,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string("TOTAL", "x(6)") + to_string(t_credit, "->,>>>,>>>,>>>,>>>,>>9.99")

    if all_supp and not remark_flag:
        create_list1()

    elif all_supp and remark_flag:
        create_list1a()
    else:

        l_lieferant = db_session.query(L_lieferant).filter(
                 (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

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