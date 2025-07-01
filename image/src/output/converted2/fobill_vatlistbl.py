#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from models import Htparam, Bill_line, Artikel, Bill, Res_line, Arrangement, Argt_line, Billjournal, Waehrung, Exrate

def fobill_vatlistbl(pvilanguage:int, billno:int):

    prepare_cache ([Htparam, Bill_line, Artikel, Res_line, Arrangement, Argt_line, Billjournal, Waehrung, Exrate])

    bline_vatlist_list = []
    exchg_rate:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    curr_billdate:date = None
    lvcarea:string = "fo-invoice"
    htparam = bill_line = artikel = bill = res_line = arrangement = argt_line = billjournal = waehrung = exrate = None

    bline_vatlist = None

    bline_vatlist_list, Bline_vatlist = create_model("Bline_vatlist", {"seqnr":int, "vatnr":int, "bezeich":string, "betrag":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bline_vatlist_list, exchg_rate, price_decimal, curr_billdate, lvcarea, htparam, bill_line, artikel, bill, res_line, arrangement, argt_line, billjournal, waehrung, exrate
        nonlocal pvilanguage, billno


        nonlocal bline_vatlist
        nonlocal bline_vatlist_list

        return {"bline-vatlist": bline_vatlist_list}

    def calc_servtaxes(artno:int, deptno:int, betrag:Decimal, billdate:date):

        nonlocal bline_vatlist_list, exchg_rate, price_decimal, curr_billdate, lvcarea, htparam, bill_line, artikel, bill, res_line, arrangement, argt_line, billjournal, waehrung, exrate
        nonlocal pvilanguage, billno


        nonlocal bline_vatlist
        nonlocal bline_vatlist_list

        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        tax:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        vat_bez:string = ""
        tax_bez:string = ""
        sc_bez:string = ""
        netto:Decimal = to_decimal("0.0")
        vat_amt:Decimal = to_decimal("0.0")
        tax_amt:Decimal = to_decimal("0.0")
        sc_amt:Decimal = to_decimal("0.0")
        artbuff = None
        Artbuff =  create_buffer("Artbuff",Artikel)

        artbuff = get_cache (Artikel, {"artnr": [(eq, artno)],"departement": [(eq, deptno)]})

        if artbuff.mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artbuff.mwst_code)]})

            if htparam and htparam.paramnr != 0:
                vat_bez = htparam.bezeichnung

        if artbuff.service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artbuff.service_code)]})

            if htparam and htparam.paramnr != 0:
                sc_bez = htparam.bezeichnung

        if artbuff.prov_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artbuff.prov_code)]})

            if htparam and htparam.paramnr != 0:
                tax_bez = htparam.bezeichnung


        serv, vat, tax, fact = get_output(calc_servtaxesbl(1, artno, deptno, billdate))
        netto = to_decimal(round(betrag / fact , price_decimal))
        vat_amt = to_decimal(round(netto * vat , price_decimal))
        tax_amt = to_decimal(round(netto * tax , price_decimal))
        sc_amt =  to_decimal(betrag) - to_decimal(netto) - to_decimal(vat_amt) - to_decimal(tax_amt)

        if vat != 0:

            bline_vatlist = query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr == artbuff.mwst_code), first=True)

            if not bline_vatlist:
                bline_vatlist = Bline_vatlist()
                bline_vatlist_list.append(bline_vatlist)

                bline_vatlist.seqnr = 9
                bline_vatlist.vatnr = artbuff.mwst_code
                bline_vatlist.bezeich = vat_bez


            bline_vatlist.betrag =  to_decimal(bline_vatlist.betrag) + to_decimal(vat_amt)

        if tax != 0:

            bline_vatlist = query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr == artbuff.prov_code), first=True)

            if not bline_vatlist:
                bline_vatlist = Bline_vatlist()
                bline_vatlist_list.append(bline_vatlist)

                bline_vatlist.seqnr = 4
                bline_vatlist.vatnr = artbuff.prov_code
                bline_vatlist.bezeich = tax_bez


            bline_vatlist.betrag =  to_decimal(bline_vatlist.betrag) + to_decimal(tax_amt)

        if serv != 0:

            bline_vatlist = query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr == artbuff.service_code), first=True)

            if not bline_vatlist:
                bline_vatlist = Bline_vatlist()
                bline_vatlist_list.append(bline_vatlist)

                bline_vatlist.seqnr = 3
                bline_vatlist.vatnr = artbuff.service_code
                bline_vatlist.bezeich = sc_bez


            bline_vatlist.betrag =  to_decimal(bline_vatlist.betrag) + to_decimal(sc_amt)

        bline_vatlist = query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.seqnr == 1), first=True)

        if not bline_vatlist:
            bline_vatlist = Bline_vatlist()
            bline_vatlist_list.append(bline_vatlist)

            bline_vatlist.seqnr = 1
            bline_vatlist.vatnr = -1
            bline_vatlist.bezeich = \
                    translateExtended ("Total Incl. vat", lvcarea, "")


        bline_vatlist.betrag =  to_decimal(bline_vatlist.betrag) + to_decimal(betrag)

        bline_vatlist = query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.seqnr == 2), first=True)

        if not bline_vatlist:
            bline_vatlist = Bline_vatlist()
            bline_vatlist_list.append(bline_vatlist)

            bline_vatlist.seqnr = 2
            bline_vatlist.vatnr = -2
            bline_vatlist.bezeich = \
                    translateExtended ("Net Amount", lvcarea, "")


        bline_vatlist.betrag =  to_decimal(bline_vatlist.betrag) + to_decimal(netto)


    def rev_bdown1():

        nonlocal bline_vatlist_list, exchg_rate, price_decimal, curr_billdate, lvcarea, htparam, bill_line, artikel, bill, res_line, arrangement, argt_line, billjournal, waehrung, exrate
        nonlocal pvilanguage, billno


        nonlocal bline_vatlist
        nonlocal bline_vatlist_list


        pass
        pass
        calc_servtaxes(artikel.artnr, artikel.departement, bill_line.betrag, bill_line.bill_datum)


    def rev_bdown2():

        nonlocal bline_vatlist_list, exchg_rate, price_decimal, curr_billdate, lvcarea, htparam, bill_line, artikel, bill, res_line, arrangement, argt_line, billjournal, waehrung, exrate
        nonlocal pvilanguage, billno


        nonlocal bline_vatlist
        nonlocal bline_vatlist_list

        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        ex_rate:Decimal = to_decimal("0.0")
        p_sign:int = 1
        artikel1 = None
        billbuff = None
        mbill = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        Billbuff =  create_buffer("Billbuff",Bill)
        Mbill =  create_buffer("Mbill",Bill)
        pass
        pass

        if bill_line.betrag < 0:
            p_sign = -1

        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)]})

        if not res_line:

            return

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        billbuff = db_session.query(Billbuff).filter(
                 (Billbuff.resnr == res_line.resnr) & (Billbuff.reslinnr == res_line.reslinnr)).first()

        mbill = db_session.query(Mbill).filter(
                 (Mbill.resnr == res_line.resnr) & (Mbill.reslinnr == 0)).first()
        rest_betrag =  to_decimal(bill_line.betrag)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

            billjournal = get_cache (Billjournal, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)],"bill_datum": [(eq, bill_line.bill_datum)],"zeit": [(eq, bill_line.zeit)],"userinit": [(eq, bill_line.userinit)],"rechnr": [(eq, billbuff.rechnr)],"anzahl": [(ne, 0)]})

            if not billjournal and mbill:

                billjournal = get_cache (Billjournal, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)],"bill_datum": [(eq, bill_line.bill_datum)],"zeit": [(eq, bill_line.zeit)],"userinit": [(eq, bill_line.userinit)],"rechnr": [(eq, mbill.rechnr)],"anzahl": [(ne, 0)]})

            if billjournal:
                argt_betrag =  to_decimal(billjournal.betrag)
            else:
                argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                argt_betrag = to_decimal(round(argt_betrag * ex_rate , price_decimal))
                argt_betrag =  to_decimal(argt_betrag) * to_decimal(p_sign)


            rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

            if argt_betrag != 0:
                calc_servtaxes(argt_line.argt_artnr, argt_line.departement, argt_betrag, bill_line.bill_datum)

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})
        calc_servtaxes(artikel1.artnr, artikel1.departement, rest_betrag, bill_line.bill_datum)


    def rev_bdown3():

        nonlocal bline_vatlist_list, exchg_rate, price_decimal, curr_billdate, lvcarea, htparam, bill_line, artikel, bill, res_line, arrangement, argt_line, billjournal, waehrung, exrate
        nonlocal pvilanguage, billno


        nonlocal bline_vatlist
        nonlocal bline_vatlist_list

        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        ex_rate:Decimal = to_decimal("0.0")
        p_sign:int = 1
        artikel1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        pass
        pass

        if bill_line.betrag < 0:
            p_sign = -1

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, artikel.artgrp)]})
        rest_betrag =  to_decimal(bill_line.betrag)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

            billjournal = get_cache (Billjournal, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)],"bill_datum": [(eq, bill_line.bill_datum)],"zeit": [(eq, bill_line.zeit)],"userinit": [(eq, bill_line.userinit)],"anzahl": [(ne, 0)]})

            if billjournal:
                argt_betrag =  to_decimal(billjournal.betrag)
            else:

                if argt_line.betrag != 0:
                    argt_betrag =  to_decimal(argt_line.betrag) * to_decimal(bill_line.anzahl)

                    if artikel.pricetab:
                        exchg_rate =  to_decimal("1")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if bill_line.bill_datum == curr_billdate and waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                        else:

                            exrate = get_cache (Exrate, {"datum": [(eq, bill_line.bill_datum)],"artnr": [(eq, artikel.betriebsnr)]})

                            if exrate:
                                exchg_rate =  to_decimal(exrate.betrag)

                            elif waehrung:
                                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                        argt_betrag = to_decimal(round(argt_betrag * exchg_rate , price_decimal))
                else:
                    argt_betrag =  to_decimal(bill_line.betrag) * to_decimal(argt_line.vt_percnt) / to_decimal("100")
                    argt_betrag = to_decimal(round(argt_betrag , price_decimal))


                rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

                if argt_betrag != 0:
                    calc_servtaxes(argt_line.argt_artnr, argt_line.departement, argt_betrag, bill_line.bill_datum)

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})
        calc_servtaxes(artikel1.artnr, artikel1.departement, rest_betrag, bill_line.bill_datum)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    curr_billdate = get_output(htpdate(110))

    for bill_line in db_session.query(Bill_line).filter(
             (Bill_line.rechnr == billno) & (Bill_line.betrag != 0)).order_by(Bill_line._recid).all():

        artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

        if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8:
            rev_bdown1()

        elif artikel.artart == 9:

            if artikel.artgrp == 0:
                rev_bdown2()
            else:
                rev_bdown3()

    return generate_output()