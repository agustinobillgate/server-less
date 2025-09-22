#using conversion tools version: 1.0.0.117

# ======================================================================
# Rulita, 22-09-2025
# Issue : Fixing format id, fixing format datum, fixing format due date
# ======================================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, L_kredit, Bediener

taxcode_list_data, Taxcode_list = create_model("Taxcode_list", {"taxcode":string, "taxamount":Decimal})

def ap_debtlist_webbl(duedate_flag:bool, from_lief:int, to_lief:int, paid_flag:bool, excl_apmanual:bool, from_date:date, to_date:date, from_supp:string, to_supp:string, only_apmanual:bool, taxcode_list_data:[Taxcode_list]):

    prepare_cache ([L_lieferant, L_kredit, Bediener])

    output_list_data = []
    l_lieferant = l_kredit = bediener = None

    output_list = taxcode_list = None

    output_list_data, Output_list = create_model("Output_list", {"paid":string, "ap_recid":int, "str":string, "lscheinnr":string, "gstid":string, "tax_code":string, "tax_amount":string, "tot_amt":string, "lief":string, "datum":string, "docu_nr":string, "name":string, "amount":string, "id":string, "due_date":string, "remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        return {"output-list": output_list_data}
    
    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def create_list0a():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart, l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart, L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == from_lief) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).order_by(L_lieferant.firma, L_kredit.rgdatum, L_kredit.name).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_dlist0a():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart, l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart, L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 ((L_kredit.rgdatum + L_kredit.ziel) >= from_date) & ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == from_lief) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).order_by(L_lieferant.firma, (L_kredit.rgdatum + L_kredit.ziel), L_kredit.name).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_list0b():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart, l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart, L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == from_lief) & (L_kredit.opart == 0) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).order_by(L_lieferant.firma, L_kredit.rgdatum, L_kredit.name).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_dlist0b():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart, l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart, L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                 ((L_kredit.rgdatum + L_kredit.ziel) >= from_date) & ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == from_lief) & (L_kredit.opart == 0) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).order_by(L_lieferant.firma, (L_kredit.rgdatum + L_kredit.ziel), L_kredit.name).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_lista():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_lieferant = L_lieferant()
        l_kredit = L_kredit()
        for l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart in db_session.query(L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart).join(L_kredit,(L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == L_lieferant.lief_nr) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).filter(
                 (L_lieferant.firma >= (from_supp).lower()) & (L_lieferant.firma <= (to_supp).lower())).order_by(L_lieferant.firma).all():
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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.str = output_list.str + to_string(entry(0, l_kredit.bemerk, ";") , "x(30)")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.str = output_list.str + to_string(l_kredit.bemerk, "x(30)")

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_dlista():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_lieferant = L_lieferant()
        l_kredit = L_kredit()
        for l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart in db_session.query(L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart).join(L_kredit,((L_kredit.rgdatum + L_kredit.ziel) >= from_date) & ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == L_lieferant.lief_nr) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).filter(
                 (L_lieferant.firma >= (from_supp).lower()) & (L_lieferant.firma <= (to_supp).lower())).order_by(L_lieferant.firma, (L_kredit.rgdatum + L_kredit.ziel)).all():
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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_listb():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_lieferant = L_lieferant()
        l_kredit = L_kredit()
        for l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart in db_session.query(L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart).join(L_kredit,(L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == L_lieferant.lief_nr) & (L_kredit.opart == 0) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).filter(
                 (L_lieferant.firma >= (from_supp).lower()) & (L_lieferant.firma <= (to_supp).lower())).order_by(L_lieferant.firma).all():
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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
        output_list.tax_amount = to_string(tot_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(tot_amt, "->>>,>>>,>>>,>>9.99")


    def create_dlistb():

        nonlocal output_list_data, l_lieferant, l_kredit, bediener
        nonlocal duedate_flag, from_lief, to_lief, paid_flag, excl_apmanual, from_date, to_date, from_supp, to_supp, only_apmanual


        nonlocal output_list, taxcode_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        due_date:date = None
        receiver:string = ""
        code1:int = 0
        code2:int = 1
        do_it:bool = False
        loopi:int = 0
        amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        tot_tax:Decimal = to_decimal("0.0")
        tot_amt:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        tamt:Decimal = to_decimal("0.0")
        output_list_data.clear()
        t_debit =  to_decimal("0")
        tot_debit =  to_decimal("0")
        amt =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")
        t_amt =  to_decimal("0")
        tamt =  to_decimal("0")

        if excl_apmanual:
            code2 = 0

        l_lieferant = L_lieferant()
        l_kredit = L_kredit()
        for l_lieferant.segment1, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_kredit.rgdatum, l_kredit.ziel, l_kredit._recid, l_kredit.name, l_kredit.netto, l_kredit.lscheinnr, l_kredit.bediener_nr, l_kredit.bemerk, l_kredit.steuercode, l_kredit.opart in db_session.query(L_lieferant.segment1, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_kredit.rgdatum, L_kredit.ziel, L_kredit._recid, L_kredit.name, L_kredit.netto, L_kredit.lscheinnr, L_kredit.bediener_nr, L_kredit.bemerk, L_kredit.steuercode, L_kredit.opart).join(L_kredit,((L_kredit.rgdatum + L_kredit.ziel) >= from_date) & ((L_kredit.rgdatum + L_kredit.ziel) <= to_date) & (L_kredit.zahlkonto == 0) & (L_kredit.lief_nr == L_lieferant.lief_nr) & (L_kredit.opart == 0) & (L_kredit.steuercode >= code1) & (L_kredit.steuercode <= code2)).filter(
                 (L_lieferant.firma >= (from_supp).lower()) & (L_lieferant.firma <= (to_supp).lower())).order_by(L_lieferant.firma, (L_kredit.rgdatum + L_kredit.ziel)).all():
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
                        output_list_data.append(output_list)

                        output_list.lscheinnr = "T O T A L"
                        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_debit =  to_decimal("0")
                receiver = l_lieferant.firma
                due_date = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ap_recid = l_kredit._recid
                output_list.datum = to_string(l_kredit.rgdatum, "%d/%m/%y") # Rulita
                output_list.lief = receiver
                output_list.name = l_kredit.name
                output_list.amount = to_string(l_kredit.netto, "->>>,>>>,>>>,>>9.99")
                output_list.docu_nr = l_kredit.lscheinnr
                output_list.lscheinnr = l_kredit.lscheinnr

                bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

                if bediener:
                    # output_list.id = to_string(bediener.userinit, "x(2)")
                    output_list.id = format_fixed_length(bediener.userinit, 2) # Rulita
                else:
                    output_list.id = " "
                output_list.due_date = to_string(due_date, "%d/%m/%y") # Rulita

                if num_entries(l_kredit.bemerk, ";") > 1:
                    output_list.remark = entry(0, l_kredit.bemerk, ";")
                    output_list.tax_code = to_string(entry(1, l_kredit.bemerk, ";") , "x(10)")


                else:
                    output_list.remark = l_kredit.bemerk

                if l_lieferant.plz != " ":

                    if matches(l_lieferant.plz,r"*#*"):
                        for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                            if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                output_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                break

                if num_entries(l_kredit.bemerk, ";") == 3:
                    t_amt =  to_decimal(to_decimal(entry(2 , l_kredit.bemerk , ";")) )
                    output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                    t_tax =  to_decimal(t_tax) + to_decimal(t_amt)
                    tot_tax =  to_decimal(tot_tax) + to_decimal(t_amt)
                    tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                    output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                    t_inv =  to_decimal(t_inv) + to_decimal(tamt)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(tamt)


                else:

                    taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == output_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        t_amt =  to_decimal(l_kredit.netto) * to_decimal(taxcode_list.taxamount)
                        output_list.tax_amount = to_string(t_amt, "->>>,>>>,>>>,>>9.99")
                        t_tax =  to_decimal(t_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_kredit.netto) * to_decimal(taxcode_list.taxamount) )
                        tamt =  to_decimal(l_kredit.netto) - to_decimal(t_amt)
                        output_list.tot_amt = to_string(tamt, "->>>,>>>,>>>,>>9.99")
                        t_inv =  to_decimal(t_inv) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_kredit.netto) - to_decimal(t_amt) )

                if l_kredit.opart == 2:
                    output_list.paid = "Yes"
                else:
                    output_list.paid = "No"
                t_debit =  to_decimal(t_debit) + to_decimal(l_kredit.netto)
                tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.netto)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = "T O T A L"
        output_list.amount = to_string(t_debit, "->>>,>>>,>>>,>>9.99")


        output_list.tax_amount = to_string(t_tax, "->>>,>>>,>>>,>>9.99")
        output_list.tot_amt = to_string(t_inv, "->>>,>>>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.lscheinnr = output_list.str + "Grand TOTAL"
        output_list.amount = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
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