from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import L_lieferant, L_kredit, Bediener

def ap_debtlistbl(duedate_flag:bool, from_lief:int, to_lief:int, paid_flag:bool, excl_apmanual:bool, from_date:date, to_date:date, from_supp:str, to_supp:str, only_apmanual:bool, taxcode_list:[Taxcode_list]):
    output_list_list = []
    l_lieferant = l_kredit = bediener = None

    output_list = taxcode_list = None

    output_list_list, Output_list = create_model("Output_list", {"paid":str, "ap_recid":int, "str":str, "lscheinnr":str, "gstid":str, "tax_code":str, "tax_amount":str, "tot_amt":str})
    taxcode_list_list, Taxcode_list = create_model("Taxcode_list", {"taxcode":str, "taxamount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list
        return {"output-list": output_list_list}

    def create_list0a():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == from_lief) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_dlist0a():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                ((L_kredit.rgdatum + L_kredit.ziel) >= from_date) &  ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == from_lief) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_list0b():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == from_lief) &  (L_kredit.opart == 0) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_dlist0b():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                ((L_kredit.rgdatum + L_kredit.ziel) >= from_date) &  ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == from_lief) &  (L_kredit.opart == 0) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_lista():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        for l_lieferant, l_kredit in db_session.query(L_lieferant, L_kredit).join(L_kredit,(L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == L_lieferant.lief_nr) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).filter(
                (func.lower(L_lieferant.firma) >= (from_supp).lower()) &  (func.lower(L_lieferant.firma) <= (to_supp).lower())).all():
            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_dlista():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        for l_lieferant, l_kredit in db_session.query(L_lieferant, L_kredit).join(L_kredit,((L_kredit.rgdatum + L_kredit.ziel) >= from_date) &  ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == L_lieferant.lief_nr) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).filter(
                (func.lower(L_lieferant.firma) >= (from_supp).lower()) &  (func.lower(L_lieferant.firma) <= (to_supp).lower())).all():
            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_listb():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        for l_lieferant, l_kredit in db_session.query(L_lieferant, L_kredit).join(L_kredit,(L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == L_lieferant.lief_nr) &  (L_kredit.opart == 0) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).filter(
                (func.lower(L_lieferant.firma) >= (from_supp).lower()) &  (func.lower(L_lieferant.firma) <= (to_supp).lower())).all():
            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")

    def create_dlistb():

        nonlocal output_list_list, l_lieferant, l_kredit, bediener


        nonlocal output_list, taxcode_list
        nonlocal output_list_list, taxcode_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        due_date:date = None
        receiver:str = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        tot_tax:decimal = 0
        tot_amt:decimal = 0
        t_amt:decimal = 0
        tamt:decimal = 0
        output_list_list.clear()
        t_debit = 0
        tot_debit = 0
        amt = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0
        t_amt = 0
        tamt = 0

        if excl_apmanual:
            code2 = 0

        for l_lieferant, l_kredit in db_session.query(L_lieferant, L_kredit).join(L_kredit,((L_kredit.rgdatum + L_kredit.ziel) >= from_date) &  ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) &  (L_kredit.zahlkonto == 0) &  (L_kredit.lief_nr == L_lieferant.lief_nr) &  (L_kredit.opart == 0) &  (L_kredit.steuercode >= code1) &  (L_kredit.steuercode <= code2)).filter(
                (func.lower(L_lieferant.firma) >= (from_supp).lower()) &  (func.lower(L_lieferant.firma) <= (to_supp).lower())).all():
            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if only_apmanual and l_kredit.steuercode == 1:
                do_it = True

            elif only_apmanual and l_kredit.steuercode == 0:
                do_it = False

            if do_it:

                if receiver != l_lieferant.firma:

                    if receiver != "":
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,66 + 1) :
                            output_list.str = output_list.str + " "
                        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_debit = 0
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + l_kredit.ziel
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.str = to_string(l_kredit.rgdatum) + to_string(receiver, "x(32)") + to_string(l_kredit.name, "x(11)") + to_string(l_kredit.lscheinnr, "x(24)") + to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == l_kredit.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(2)")
                else:
                    output_list.str = output_list.str + "  "
                output_list.str = output_list.str + to_string(due_date)

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if re.match(".*#.*",l_lieferant.plz):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt = decimal.Decimal(entry(2, l_kredit.bemerk, ";"))
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax = t_tax + t_amt
                    tot_tax = tot_tax + t_amt
                    tamt = l_kredit.netto - t_amt
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv = t_inv + tamt
                    tot_amt = tot_amt + tamt


                else:

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_kredit.netto * taxcode_list.taxamount
                        t_amt = l_kredit.netto * taxcode_list.taxamount
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax = t_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_kredit.netto * taxcode_list.taxamount)
                        tamt = l_kredit.netto - t_amt
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv = t_inv + (l_kredit.netto - t_amt)
                        tot_amt = tot_amt + (l_kredit.netto - t_amt)

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit = t_debit + l_kredit.netto
                tot_debit = tot_debit + l_kredit.netto
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,66 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "T O T A L" + to_string(t_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,64 + 1) :
            output_list.str = output_list.str + " "
        output_list.str = output_list.str + "Grand TOTAL" + to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    if not duedate_flag:

        if from_lief != 0 and to_lief == from_lief:

            if paid_flag:
                create_list0a()
            else:
                create_list0b()
        else:

            if paid_flag:
                create_lista()
            else:
                create_listb()

    elif duedate_flag:

        if from_lief != 0 and to_lief == from_lief:

            if paid_flag:
                create_dlist0a()
            else:
                create_dlist0b()
        else:

            if paid_flag:
                create_dlista()
            else:
                create_dlistb()

    return generate_output()