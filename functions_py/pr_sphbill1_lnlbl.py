#using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/10/2025

    TicketID: D202E2 
        _issue_:    - update from FDL: 6DCD86, FDL: DECE04, MALIK: C68F4A
                    - changed import from functions to functions_py
                    - var dept not defined
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
from functions.print_hbill1_phbl import print_hbill1_phbl
from functions.prepare_pr_sphbill1bl import prepare_pr_sphbill1bl
from models import H_mjourn, Printer, Artikel, H_bill, H_bill_line, Htparam, Hoteldpt, Queasy, H_queasy, Kellner, H_artikel, Kontplan, Paramtext, Bediener, Tisch, Res_line, Mc_guest, Printcod, H_journal, Waehrung

from functions import log_program

def pr_sphbill1_lnlbl(pvilanguage:int, hbrecid:int, printnr:int, use_h_queasy:bool, session_parameter:string, user_init:string, billnr:int, print_all:bool):

    prepare_cache ([Artikel, H_bill, H_bill_line, Htparam, Hoteldpt, Queasy, H_queasy, Kellner, Kontplan, Paramtext, Bediener, Tisch, Res_line, Mc_guest, Printcod, H_journal, Waehrung])

    winprinterflag = False
    filename = ""
    msg_str = ""
    output_list_data = []
    t_printer_data = []
    lvcarea:string = "print-sphbill1"
    disc_bezeich:string = ""
    amount:Decimal = to_decimal("0.0")
    sort_i:int = 0
    order_id:string = ""
    disc_zwkum:int = 0
    print_balance:bool = True
    disc_art1:int = -1
    disc_art2:int = -1
    disc_art3:int = -1
    incl_service:bool = False
    incl_mwst:bool = False
    service_taxable:bool = False
    print_fbtotal:bool = False
    prdisc_flag:bool = False
    mwst_str:string = ""
    service_str:string = ""
    hmargin:int = 0
    bmargin:int = 1
    lpage:int = 0
    nbezeich:int = 0
    nwidth:int = 0
    npause:int = 0
    bill_date110:date = None
    bill_date:date = None
    price_decimal:int = 0
    n11:int = 11
    long_digit:bool = False
    prtwoline:bool = False
    printed_line:int = 0
    last_amount:Decimal = to_decimal("0.0")
    zeit:int = 0
    comp_flag:bool = False
    service:Decimal = to_decimal("0.0")
    mwst:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    comp_taxserv:bool = False
    tot_sales:Decimal = to_decimal("0.0")
    new_item:bool = False
    printed:bool = False
    qty:int = 0
    do_it:bool = False
    rm_transfer:bool = False
    new_fbart:bool = False
    tot_line:int = 0
    h_service:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    serv_perc:Decimal = to_decimal("0.0")
    mwst_perc:Decimal = to_decimal("0.0")
    fact:Decimal = 1
    mwst1:Decimal = to_decimal("0.0")
    subtotal:Decimal = to_decimal("0.0")
    bline_exist:bool = False
    qty1000:bool = False
    i:int = 0
    n:int = 0
    curr_j:int = 0
    npage:int = 0
    tot_ndisc_line:int = 0
    tot_disc_line:int = 0
    buttom_lines:int = 0
    prtabledesc:bool = False
    header1:string = ""
    header2:string = ""
    foot1:string = ""
    foot2:string = ""
    foot3:string = ""
    anz_foot:int = 0
    overhead1:int = 0
    overhead2:int = 0
    overhead3:int = 0
    overhead4:int = 0
    total_food:Decimal = to_decimal("0.0")
    total_bev:Decimal = to_decimal("0.0")
    total_other:Decimal = to_decimal("0.0")
    total_fdisc:Decimal = to_decimal("0.0")
    total_bdisc:Decimal = to_decimal("0.0")
    total_odisc:Decimal = to_decimal("0.0")
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    str451:string = ""
    sc_art:int = 0
    mwst_perc:Decimal = to_decimal("0.0")
    serv_perc:Decimal = to_decimal("0.0")
    serv_code:int = 0
    vat_code:int = 0
    servtax_use_foart:bool = False
    h_mjourn = printer = artikel = h_bill = h_bill_line = htparam = hoteldpt = queasy = h_queasy = kellner = h_artikel = kontplan = paramtext = bediener = tisch = res_line = mc_guest = printcod = h_journal = waehrung = None

    art_list = art_list_submenu = t_printer = vat_list = output_list = bline_vatlist = artbuff = abuff = bart_list_submenu = None

    art_list_data, Art_list = create_model(
        "Art_list", {
            "printed":bool, 
            "disc_flag":bool, 
            "dept":int, 
            "artnr":int, 
            "bezeich":string, 
            "artart":int, 
            "zwkum":int, 
            "qty":int, 
            "price":Decimal, 
            "amount":Decimal, 
            "betrag":Decimal, 
            "happyhr":string, 
            "datum":date, 
            "sysdate":date, 
            "zeit":int, 
            "condiment":int,
            "hline_recid":int # Malik : C68F4A
            }
        )
    art_list_submenu_data, Art_list_submenu = create_model_like(
        H_mjourn, {
            "hline_recid":int, 
            "is_deleted":bool
            }
        ) # Malik : C68F4A
    t_printer_data, T_printer = create_model_like(Printer)
    vat_list_data, Vat_list = create_model(
        "Vat_list", {
            "vat_amt":Decimal, 
            "betrag_amt":Decimal
            }
        )
    output_list_data, Output_list = create_model(
        "Output_list", {
            "str":string, 
            "str_pos":int, 
            "pos":int, 
            "flag_popup":bool, 
            "npause":int, 
            "sort_i":int
            }
        )
    bline_vatlist_data, Bline_vatlist = create_model(
        "Bline_vatlist", {
            "seqnr":int, 
            "vatnr":int, 
            "bezeich":string, 
            "betrag":Decimal
            }
        )

    Artbuff = create_buffer("Artbuff",Artikel)
    Abuff = Art_list
    abuff_data = art_list_data
    
    Bart_list_submenu = Art_list_submenu
    bart_list_submenu_data = art_list_submenu_data # Malik : C68F4A

    db_session = local_storage.db_session

    def generate_output():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu
        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        return {
            "print_all": print_all, 
            "winprinterflag": winprinterflag, 
            "filename": filename, 
            "msg_str": msg_str, 
            "output-list": output_list_data, 
            "t-printer": t_printer_data
        }

    def optional_params():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu
        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        lvctmp:string = ""
        lvcleft:string = ""
        lvcval:string = ""
        lvicnt:int = 0
        lvi:int = 0
        lvitmp:int = 0
        lvicnt = num_entries(session_parameter, ";")
        for lvi in range(1,lvicnt + 1) :
            lvctmp = ""
            lvcleft = ""


            lvctmp = trim(entry(lvi - 1, session_parameter, ";"))
            lvcleft = trim(entry(0, lvctmp, "="))

            if lvcleft == "WINprinter":
                winprinterflag = True
            elif lvcleft == "TableDesc":
                lvcval = entry(1, lvctmp, "=")

                if lvcval.lower()  == ("YES").lower() :
                    prtabledesc = True
            elif lvcleft == "Pr2Line":
                lvcval = entry(1, lvctmp, "=")

                if lvcval.lower()  == ("YES").lower() :
                    prtwoline = True
            elif lvcleft == "print-all":
                lvitmp = to_int(entry(1, lvctmp, "="))

                if lvitmp == 1:
                    print_all = True
            elif lvcleft == "top-margin":
                lvitmp = -1
                lvitmp = to_int(entry(1, lvctmp, "="))

                if lvitmp >= 1:
                    hmargin = lvitmp
            elif lvcleft == "num-lines":
                lvitmp = -1
                lvitmp = to_int(entry(1, lvctmp, "="))

                if lvitmp >= 1:
                    lpage = lvitmp
            elif lvcleft == "DesLen":
                lvitmp = to_int(entry(1, lvctmp, "="))

                if lvitmp >= 1:
                    nbezeich = lvitmp
            elif lvcleft == "buttom-lines":
                lvitmp = to_int(entry(1, lvctmp, "="))

                if lvitmp >= 1:
                    buttom_lines = lvitmp
            elif lvcleft == "header1":
                header1 = entry(1, lvctmp, "=")

            elif lvcleft == "header2":
                header2 = entry(1, lvctmp, "=")

            elif lvcleft == "foot1":
                foot1 = entry(1, lvctmp, "=")
                foot2 = ""
                anz_foot = 1

            elif lvcleft == "foot2":
                foot2 = entry(1, lvctmp, "=")
                anz_foot = 2

    def cal_servat(depart:int, h_artnr:int, service_code:int, mwst_code:int, inpdate:date):
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu
        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        serv_perc = to_decimal("0.0")
        mwst_perc = to_decimal("0.0")
        servat = to_decimal("0.0")
        serv_htp:Decimal = to_decimal("0.0")
        vat_htp:Decimal = to_decimal("0.0")
        hbuff = None
        abuff = None

        def generate_inner_output():
            return (serv_perc, mwst_perc, servat)

        Hbuff =  create_buffer("Hbuff",H_artikel)
        Abuff =  create_buffer("Abuff",Artikel)

        if bill_date < bill_date110 and (service_code != 0 or mwst_code != 0):

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) & (Hbuff.departement == depart)).first()

            abuff = get_cache (Artikel, {"artnr": [(eq, hbuff.artnrfront)],"departement": [(eq, depart)]})

            kontplan = get_cache (Kontplan, {"betriebsnr": [(eq, depart)],"kontignr": [(eq, abuff.artnr)],"datum": [(eq, inpdate)]})

            if kontplan:
                serv_htp =  to_decimal(kontplan.anzkont) / to_decimal("10000")
                vat_htp =  to_decimal(kontplan.anzconf) / to_decimal("10000")

                serv_perc =  to_decimal(serv_htp)
                mwst_perc =  to_decimal(vat_htp)
                servat =  to_decimal("1") + to_decimal(serv_perc) + to_decimal(mwst_perc)

                return generate_inner_output()
        serv_htp =  to_decimal("0")
        vat_htp =  to_decimal("0")

        if servtax_use_foart:

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) & (Hbuff.departement == depart)).first()

            abuff = get_cache (Artikel, {"artnr": [(eq, hbuff.artnrfront)],"departement": [(eq, depart)]})

            if abuff:
                service_code = abuff.service_code
                mwst_code = abuff.mwst_code
        else:
            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) & (Hbuff.departement == depart)).first()

            if hbuff:
                service_code = hbuff.service_code
                mwst_code = hbuff.mwst_code

        if service_code != 0:
            htparam = get_cache (Htparam, {"paramnr": [(eq, service_code)]})
            serv_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if mwst_code != 0:
            htparam = get_cache (Htparam, {"paramnr": [(eq, mwst_code)]})
            vat_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if service_taxable:
            serv_perc =  to_decimal(serv_htp)
            mwst_perc = ( to_decimal("1") + to_decimal(serv_htp)) * to_decimal(vat_htp)
            servat =  to_decimal("1") + to_decimal(serv_perc) + to_decimal(mwst_perc)

        else:
            serv_perc =  to_decimal(serv_htp)
            mwst_perc =  to_decimal(vat_htp)
            servat =  to_decimal("1") + to_decimal(serv_perc) + to_decimal(mwst_perc)

        return generate_inner_output()

    def add_unitprice_text():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu
        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        n:int = 0
        s:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 412)]})

        if not htparam.flogical:
            return

        if htparam.paramgruppe != 19:
            return

        if prtwoline:
            return

        for art_list in query(art_list_data, filters=(lambda art_list:(art_list.qty != 1) and (art_list.qty != -1) and art_list.qty != 0 and art_list.artnr != 0)):
            s = " @" + to_string(art_list.price)

            if length(art_list.bezeich + s) <= nbezeich:
                art_list.bezeich = art_list.bezeich + s
            else:
                art_list.bezeich = substring(art_list.bezeich, 0, nbezeich - length(s)) + s

    def check_pages():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu
        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        total_line:int = 0
        new_sold_item:bool = False

        if prdisc_flag:
            for art_list in query(art_list_data, filters=(lambda art_list: art_list.artart == 0)):
                if art_list.disc_flag:
                    tot_disc_line = tot_disc_line + 1
                else:
                    tot_ndisc_line = tot_ndisc_line + 1

        art_list = query(art_list_data, filters=(lambda art_list: art_list.artart == 0), first=True)
        new_sold_item = None != art_list
        overhead1 = hmargin + bmargin + 3
        overhead2 = 6
        overhead3 = 0

        for art_list in query(art_list_data, filters=(lambda art_list: art_list.artart != 0)):
            if new_sold_item or (not art_list.printed):
                overhead3 = overhead3 + 1

        if overhead3 != 0:
            overhead3 = overhead3 + 2

        if h_bill.saldo == 0 or print_all:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 713)]})

            if paramtext:

                if foot3 == "" and paramtext.ptexte != "":
                    foot3 = paramtext.ptexte
                    anz_foot = 3

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 712)]})

            if foot2 == "" and paramtext.ptexte != "":
                foot2 = paramtext.ptexte
                anz_foot = 2

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 711)]})

            if foot1 == "" and paramtext.ptexte != "":
                foot1 = paramtext.ptexte

                if anz_foot == 0:
                    anz_foot = 1

        if anz_foot == 0:
            overhead4 = 0
        else:
            overhead4 = anz_foot + 2

        npage = 1
        total_line = overhead1 + tot_line + overhead2 + overhead3 + overhead4

        if tot_ndisc_line >= 1 and tot_ndisc_line >= 1:
            total_line = total_line + 3
        while total_line > lpage:
            npage = npage + 1
            total_line = total_line - (lpage - overhead1)
        npage = 9999


    def print_overhead1():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        i:int = 0
        rechnr_str:string = ""
        kname:string = ""

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            kname = bediener.username

        elif kellner:
            kname = kellner.kellnername

        if printed_line == 0 or print_all:
            for i in range(1,hmargin + 1) :
                output_list.str = output_list.str + to_string(" ")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                curr_j = curr_j + 1
                printed_line = printed_line + 1

            if header1 != "":
                for i in range(1,length(header1)  + 1) :
                    output_list.str = output_list.str + to_string(substring(header1, i - 1, 1) , "x(1)")
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1

            if header2 != "":
                for i in range(1,length(header2)  + 1) :
                    output_list.str = output_list.str + to_string(substring(header2, i - 1, 1) , "x(1)")
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1

            if header1 != "" or header2 != "":
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1
            rechnr_str = to_string(h_bill.rechnr)

            if h_bill.mwst[89] != 0:
                rechnr_str = to_string(h_bill.mwst[89])

            if print_all:
                rechnr_str = rechnr_str + "**"

            if h_bill.bilname != "":
                if gst_logic:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        " " + to_string(bill_date) + "|" +\
                        to_string(get_current_time_in_seconds(), "HH:MM") + "|" +\
                        translateExtended ("Tax Invoice No", lvcarea, "") + "|" +\
                        rechnr_str

                else:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        " " + to_string(bill_date) + "|" +\
                        to_string(get_current_time_in_seconds(), "HH:MM") + "|" +\
                        translateExtended ("BillNo", lvcarea, "") + "|" +\
                        rechnr_str

                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 2
                output_list.str = output_list.str + to_string(" " + hoteldpt.depart, "x(32)")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 3
                output_list.str = output_list.str + " " + translateExtended ("Table", lvcarea, "") + "|" + to_string(h_bill.tischnr, ">>>>>9") + "|" + to_string(h_bill.belegung, "->>>9 ") + "|" + "(" + to_string(billnr, ">>>9") + ") " + "|" + to_string(kname) + "|" + order_id
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

                if prtabledesc:
                    tisch = get_cache (Tisch, {"tischnr": [(eq, h_bill.tischnr)],"departement": [(eq, h_bill.departement)]})

                    if tisch and tisch.bezeich != "":
                        output_list.str_pos = 4
                        output_list.str = output_list.str + to_string("     " + tisch.bezeich, "x(32)")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                        curr_j = curr_j + 1
                output_list.str_pos = 5
                output_list.str = output_list.str + to_string("     " + translateExtended ("Guest", lvcarea, "") + "|" + h_bill.bilname, "x(32)")

                queasy = get_cache (Queasy, {"key": [(eq, 286)],"number1": [(eq, h_bill.rechnr)],"number2": [(eq, h_bill.departement)],"number3": [(eq, billnr)]})

                if queasy:
                    if output_list.str != "":
                        output_list.str = output_list.str + " | " + trim(queasy.char1)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

                if gst_logic:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str_pos = 6
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str = output_list.str +\
                            to_string("            " + translateExtended ("Tax Invoice", lvcarea, ""))

                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str_pos = 7
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str = output_list.str +\
                            to_string("       " + translateExtended ("GST ID : 001865060352", lvcarea, ""))

                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                curr_j = curr_j + 4
                printed_line = printed_line + 4

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:
                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        mc_guest = db_session.query(Mc_guest).filter(
                                (Mc_guest.gastnr == res_line.gastnrmember) & (Mc_guest.activeflag)).first()

                elif h_bill.resnr > 0 and h_bill.reslinnr == 0:
                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == h_bill.resnr) & (Mc_guest.activeflag)).first()

                if mc_guest:
                    output_list.str_pos = 8
                    output_list.str = output_list.str + to_string("     " + translateExtended ("MemberCard", lvcarea, "") + " " + mc_guest.cardnum, "x(32)")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    curr_j = curr_j + 1
                    printed_line = printed_line + 1
            else:
                if gst_logic:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        "     " + to_string(bill_date) + "|" +\
                        to_string(get_current_time_in_seconds(), "HH:MM") + "|" +\
                        translateExtended ("Tax Invoice No", lvcarea, "") + "|" +\
                        rechnr_str

                else:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        "     " + to_string(bill_date) + "|" +\
                        to_string(get_current_time_in_seconds(), "HH:MM") + "|" +\
                        " " + translateExtended ("BillNo", lvcarea, "") + "|" +\
                        rechnr_str

                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 2
                output_list.str = output_list.str + to_string("     " + hoteldpt.depart, "x(32)")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 3
                output_list.str = output_list.str + "     " + translateExtended ("Table", lvcarea, "") + "|" + to_string(h_bill.tischnr, ">>>9") + "|" + to_string(h_bill.belegung, "->>>9 ") + "|" + "(" + to_string(billnr, ">>>9") + ") " + "|" + to_string(kname) + "|" + order_id
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

                if gst_logic:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str_pos = 6
                    output_list.str = output_list.str + to_string("            " + translateExtended ("Tax Invoice", lvcarea, ""))

                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str_pos = 7
                    output_list.str = output_list.str +\
                            to_string("       " + translateExtended ("GST ID : 001865060352", lvcarea, ""))

                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

                if prtabledesc:
                    tisch = get_cache (Tisch, {"tischnr": [(eq, h_bill.tischnr)],"departement": [(eq, h_bill.departement)]})

                    if tisch and tisch.bezeich != "":
                        output_list.str_pos = 4
                        output_list.str = output_list.str + to_string(" " + tisch.bezeich, "x(32)")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                        curr_j = curr_j + 1
                curr_j = curr_j + 3
                printed_line = printed_line + 3
            for i in range(1,bmargin + 1) :
                curr_j = curr_j + 1
                printed_line = printed_line + 1
                output_list.str = output_list.str + to_string(" ")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

    def print_billine():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        i:int = 0
        anz:int = 0
        leerch:string = ""
        ct:string = ""
        bezeich:string = ""
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        bezeich = art_list.happyhr + art_list.bezeich

        log_program.write_log("DEBUG bezeich", f"bezeich = {bezeich}", "Log_Rulita.txt" )

        if qty1000:
            output_list.str_pos = 10
            output_list.str = output_list.str + to_string("   ") + to_string(art_list.qty, "->>>> ") + "|"
        else:
            output_list.str_pos = 10
            output_list.str = output_list.str + to_string("   ") + to_string(art_list.qty) + "|"

        for i in range(1,nbezeich + 1) :
            if i > length(bezeich):
                output_list.str = output_list.str + to_string(" ")
            else:
                output_list.str = output_list.str + to_string(substring(bezeich, i - 1, 1) , "x(1)")
        output_list.str = output_list.str + "|"

        if prtwoline:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            curr_j = curr_j + 1
            printed_line = printed_line + 1

        else:
            if price_decimal == 0:
                if not long_digit:
                    output_list.str = output_list.str + to_string(art_list.amount, "   ->>,>>>,>>>,>>9") + "|"
                else:
                    output_list.str = output_list.str + to_string(art_list.amount, "->,>>>,>>>,>>>,>>9") + "|"
            else:
                output_list.str = output_list.str + to_string(art_list.amount, "->>,>>>,>>>,>>9.99") + "|"
            curr_j = curr_j + 1
            printed_line = printed_line + 1

        output_list.str = output_list.str + "1"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1

        if prtwoline:
            if qty1000:
                output_list.str = output_list.str + to_string("      ")
            else:
                output_list.str = output_list.str + to_string("     ")
            anz = nbezeich - 22

            if anz > 0:
                leerch = fill(" ", anz)

            if price_decimal == 0:
                ct = "@" + to_string(art_list.price, "->,>>>,>>9") + leerch + to_string(art_list.amount, "->>>,>>>,>>9") + chr_unicode(10)
            else:
                ct = "@" + to_string(art_list.price, "->>,>>9.99") + leerch + to_string(art_list.amount, "->>>,>>9.99") + chr_unicode(10)
            for i in range(1,length(ct)  + 1) :
                output_list.str = output_list.str + to_string(substring(ct, i - 1, 1) , "x(1)")
            curr_j = curr_j + 1
            printed_line = printed_line + 1

        if art_list.condiment == 0 or art_list.disc_flag:
            return

        for h_mjourn in db_session.query(H_mjourn).filter(
                (H_mjourn.departement == art_list.dept) & (H_mjourn.h_artnr == art_list.artnr) & (H_mjourn.rechnr == h_bill.rechnr) & (H_mjourn.bill_datum == art_list.datum) & (H_mjourn.sysdate == art_list.sysdate) & (H_mjourn.zeit == art_list.zeit)).order_by(H_mjourn._recid).all():

            h_art = db_session.query(H_art).filter(
                    (H_art.artnr == h_mjourn.artnr) & (H_art.departement == h_mjourn.departement)).first()
            
            log_program.write_log("DEBUG h_art", f"h_art.bezeich = {h_art.bezeich}", "Log_Rulita.txt" )

            if h_art:
                # bezeich = h_art.bezeich
                # output_list.str = output_list.str + to_string(art_list.qty) + to_string(" ")
                # for i in range(1,nbezeich + 1) :

                #     if i > length(bezeich):
                #         output_list.str = output_list.str + to_string(" ")
                #     else:
                #         output_list.str = output_list.str + to_string(substring(bezeich, i - 1, 1) , "x(1)")
                # output_list.str = output_list.str + to_string(translateExtended ("(Condiment)", lvcarea, "") , "x(11)")
                # output_list = Output_list()
                # output_list_data.append(output_list)

                # output_list.sort_i = sort_i
                # sort_i = sort_i + 1
                if num_entries(h_mjourn.request, "|") > 1:

                    if entry(0, h_mjourn.request, "|") == to_string(art_list.hline_recid):
                        bezeich = h_art.bezeich
                        output_list.str_pos = 10
                        output_list.str = output_list.str + to_string(h_mjourn.anzahl) + to_string(" ") + "|"
                        for i in range(1,nbezeich + 1) :

                            if i > length(bezeich):
                                output_list.str = output_list.str + to_string(" ")
                            else:
                                output_list.str = output_list.str + to_string(substring(bezeich, i - 1, 1) , "x(1)")
                        output_list.str = output_list.str + "|" + "|" + "2"
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1 # Malik : C68F4A
            curr_j = curr_j + 1
            printed_line = printed_line + 1


    def print_overhead2(prall_flag:int):
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu
        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        i:int = 0
        pos:int = 0
        nbez1:int = 0
        s:string = ""
        tot_str:string = ""

        if curr_j > (lpage - 6):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag_popup = True
            output_list.npause = npause
            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            curr_j = 0
            printed_line = 0
            print_overhead1()
        pos = 5

        if qty1000:
            pos = 6
        nbez1 = nbezeich

        if prtwoline:
            nbez1 = nbez1 - 11

        if prall_flag <= 1:
            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")
            for i in range(1,(nbezeich + n11)  + 1) :
                output_list.str = output_list.str + to_string("-", "x(1)")
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if service != 0 or mwst != 0:
            if comp_taxserv and comp_flag:
                s = translateExtended ("TOTAL", lvcarea, "") + "   "

                if qty1000:
                    output_list.str = output_list.str + to_string("", "x(6)")
                else:
                    output_list.str = output_list.str + to_string("", "x(5)")

                for i in range(1,(nbezeich + n11)  + 1) :
                    if i < (nbezeich + n11):
                        output_list.str = output_list.str + to_string("-", "x(1)")
                    else:
                        output_list.str = output_list.str + to_string("-", "x(1)")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1

                printed_line = printed_line + 1

            else:
                s = translateExtended ("subtotal", lvcarea, "")

            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")

            for i in range(1,nbez1 + 1) :

                if i > length(s):
                    output_list.str_pos = 11
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str_pos = 11
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")

            if price_decimal == 0:
                if not long_digit:
                    output_list.str = output_list.str + "|" + to_string(subtotal, "   ->>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(subtotal, "->,>>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
            else:
                output_list.str = output_list.str + "|" + to_string(subtotal, "->>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
            printed_line = printed_line + 1

            if prall_flag == 0:
                return
            
            cal_totalfb()
            print_totalfb()

            if comp_taxserv and comp_flag:
                if qty1000:
                    output_list.str = output_list.str + to_string("", "x(6)")
                else:
                    output_list.str = output_list.str + to_string("", "x(5)")

                for i in range(1,(nbezeich + n11)  + 1) :
                    if i < (nbezeich + n11):
                        output_list.str = output_list.str + to_string("-", "x(1)")
                    else:
                        output_list.str = output_list.str + to_string("-", "x(1)")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1

                printed_line = printed_line + 1
                tot_amount =  to_decimal(subtotal)

                return

            if service != 0:
                for i in range(1,pos + 1) :
                    output_list.str = output_list.str + to_string(" ")

                for i in range(1,nbez1 + 1) :
                    if i > length(service_str):
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(substring(service_str, i - 1, 1) , "x(1)")

                if price_decimal == 0:
                    if not long_digit:
                        output_list.str = output_list.str + "|" + to_string(service, "   ->>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(service, "->,>>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(service, "->>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                printed_line = printed_line + 1


            if mwst != 0:
                for i in range(1,pos + 1) :
                    output_list.str = output_list.str + to_string(" ")

                for i in range(1,nbez1 + 1) :
                    if i > length(mwst_str):
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(substring(mwst_str, i - 1, 1) , "x(1)")

                if price_decimal == 0:
                    if not long_digit:
                        output_list.str = output_list.str + "|" + to_string(mwst, "   ->>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(mwst, "->,>>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(mwst, "->>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                printed_line = printed_line + 1

        if qty1000:
            output_list.str = output_list.str + to_string("", "x(6)")
        else:
            output_list.str = output_list.str + to_string("", "x(5)")

        for i in range(1,(nbezeich + n11 + 4)  + 1) :
            if i < (nbezeich + n11 + 4):
                output_list.str = output_list.str + to_string("-", "x(1)")
            else:
                output_list.str = output_list.str + to_string("-", "x(1)")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

        printed_line = printed_line + 1
        for i in range(1,pos + 1) :
            output_list.str = output_list.str + to_string(" ")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 846)]})

        if htparam.fchar == "":
            tot_str = translateExtended ("TOTAL", lvcarea, "")
        else:
            tot_str = htparam.fchar

        for i in range(1,nbez1 + 1) :
            if i > length(tot_str):
                output_list.str_pos = 13
                output_list.str = output_list.str + to_string(" ")
            else:
                output_list.str_pos = 13
                output_list.str = output_list.str + to_string(substring(tot_str, i - 1, 1) , "x(1)")

        tot_amount =  to_decimal("0")

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.waehrungsnr == billnr)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True

            tot_amount =  to_decimal(tot_amount) + to_decimal(h_bill_line.betrag)

        if price_decimal == 0:
            if not long_digit:
                output_list.str = output_list.str + "|" + to_string(tot_amount, "   ->>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
            else:
                output_list.str = output_list.str + "|" + to_string(tot_amount, "->,>>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + "|" + to_string(tot_amount, "->>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

        if h_bill.bilname != "":
            output_list.str_pos = 18
            output_list.str = output_list.str + to_string(" ") + to_string(h_bill.bilname, "x(30)")
        printed_line = printed_line + 1
        curr_j = curr_j + 6
        multi_currency()

    def print_overhead3():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        nbez1:int = 0
        i:int = 0
        pos:int = 0
        lpage1:int = 0
        balance:Decimal = to_decimal("0.0")
        amt:Decimal = to_decimal("0.0")
        bal_str:string = ""
        chg_str:string = ""
        new_sold_item:bool = False
        compli_notax:bool = False

        art_list = query(art_list_data, filters=(lambda art_list: art_list.artart == 0), first=True)
        new_sold_item = None != art_list
        nbez1 = nbezeich

        if prtwoline:
            nbez1 = nbez1 - 11

        if anz_foot == 0:
            lpage1 = lpage - 4
        else:
            lpage1 = lpage - 8

        if curr_j > lpage1:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag_popup = True
            output_list.npause = npause
            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            curr_j = 0
            printed_line = 0
            print_overhead1()
        balance =  to_decimal(tot_amount)

        for art_list in query(art_list_data, filters=(lambda art_list: art_list.artart != 0)):
            if new_sold_item or not art_list.printed:
                if qty1000:
                    output_list.str = output_list.str + to_string("", "x(6)")
                else:
                    output_list.str = output_list.str + to_string("", "x(5)")

                for i in range(1,nbez1 + 1) :
                    if i > length(art_list.bezeich):
                        output_list.str_pos = 14
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str_pos = 14
                        output_list.str = output_list.str + to_string(substring(art_list.bezeich, i - 1, 1) , "x(1)")

            if (art_list.artart == 11 or art_list.artart == 12) and comp_taxserv and comp_flag:
                if art_list.amount * subtotal > 0:
                    amt =  to_decimal(subtotal)
                else:
                    amt =  - to_decimal(subtotal)

                balance =  to_decimal(balance) + to_decimal(amt)
                last_amount =  to_decimal(last_amount) + to_decimal(amt)
                compli_notax = True

                if new_sold_item or not art_list.printed:
                    if price_decimal == 0:
                        if not long_digit:
                            output_list.str = output_list.str + "|" + to_string(amt, "   ->>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                        else:
                            output_list.str = output_list.str + "|" + to_string(amt, "->,>>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1

                    else:
                        output_list.str = output_list.str + "|" + to_string(amt, "->>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1

                    printed_line = printed_line + 1

            else:

                if not art_list.printed or print_all:
                    balance =  to_decimal(balance) + to_decimal(art_list.amount)

                last_amount =  to_decimal(last_amount) + to_decimal(art_list.amount)

                if new_sold_item or not art_list.printed:
                    if price_decimal == 0:
                        if not long_digit:
                            output_list.str = output_list.str + "|" + to_string(art_list.amount, "   ->>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                        else:
                            output_list.str = output_list.str + "|" + to_string(art_list.amount, "->,>>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(art_list.amount, "->>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    printed_line = printed_line + 1

        if qty1000:
            output_list.str = output_list.str + to_string("", "x(6)")
        else:
            output_list.str = output_list.str + to_string("", "x(5)")

        for i in range(1,(nbezeich + n11 + 4)  + 1) :
            if i < (nbezeich + n11 + 4):
                output_list.str = output_list.str + to_string("-", "x(1)")
            else:
                output_list.str = output_list.str + to_string("-", "x(1)")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

        printed_line = printed_line + 1
        pos = 5

        if qty1000:
            pos = 6
        for i in range(1,pos + 1) :
            output_list.str = output_list.str + to_string(" ")

        if not compli_notax:
            balance =  to_decimal("0")

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.waehrungsnr == billnr)).order_by(H_bill_line._recid).all():
                balance =  to_decimal(balance) + to_decimal(h_bill_line.betrag)

        if (balance >= 0):
            if not rm_transfer or print_balance or balance != 0:
                bal_str = translateExtended ("balance", lvcarea, "")
                for i in range(1,nbez1 + 1) :
                    if i > length(bal_str):
                        output_list.str_pos = 15
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str_pos = 15
                        output_list.str = output_list.str + to_string(substring(bal_str, i - 1, 1) , "x(1)")

                if price_decimal == 0:
                    if not long_digit:
                        output_list.str = output_list.str + "|" + to_string(balance, "   ->>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(balance, "->,>>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(balance, "->>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                printed_line = printed_line + 1
        else:
            chg_str = translateExtended ("CHANGE", lvcarea, "")
            for i in range(1,nbez1 + 1) :
                if i > length(chg_str):
                    output_list.str_pos = 16
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str_pos = 16
                    output_list.str = output_list.str + to_string(substring(chg_str, i - 1, 1) , "x(1)")

            if price_decimal == 0:
                if not long_digit:
                    output_list.str = output_list.str + "|" + to_string(- balance, "   ->>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(- balance, "->,>>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
            else:
                output_list.str = output_list.str + "|" + to_string(- balance, "->>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
            printed_line = printed_line + 1
        print_net_vat()
        print_in_word()

        if h_bill.bilname != "":
            if h_bill.resnr > 0 and h_bill.reslinnr > 0:
                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

                    if qty1000:
                        output_list.str = output_list.str + to_string("", "x(5)")
                    else:
                        output_list.str = output_list.str + to_string("", "x(5)")

                    output_list.str_pos = 17
                    output_list.str = output_list.str + to_string(translateExtended ("Room :", lvcarea, "") + " " + res_line.zinr)
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

            else:
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")

            output_list.str_pos = 18
            output_list.str = output_list.str + to_string(" ") + to_string(h_bill.bilname, "x(30)")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")

            output_list.str = output_list.str + to_string(translateExtended ("Time :", lvcarea, "") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS") , "x(20)")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")
            output_list.str = output_list.str + to_string(translateExtended ("Time :", lvcarea, "") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS") , "x(20)")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

        multi_currency()

        if gst_logic:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(translateExtended ("     Tax Code      Amount     GST", lvcarea, ""))

            if comp_taxserv:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str = output_list.str + to_string(translateExtended ("     " + to_string(mwst_str, "x(13)") +\
                        to_string(subtotal, "->>9.99 ") +\
                        to_string(0, "->>9.99") , lvcarea, ""))

            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str = output_list.str + to_string(translateExtended ("     " + to_string(mwst_str, "x(13)") +\
                        to_string(subtotal, "->>9.99 ") +\
                        to_string(mwst, "->>9.99") , lvcarea, ""))

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

    def print_overhead4():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        i:int = 0

        if anz_foot > 0:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str_pos = 19
            output_list.str = output_list.str + to_string(foot1)
            output_list.pos = 6
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 3

        if foot2 != "":
            output_list.str_pos = 19
            output_list.str = output_list.str + to_string(foot2)
            output_list.pos = 6
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if foot3 != "":
            output_list.str_pos = 19
            output_list.str = output_list.str + to_string(foot3)
            output_list.pos = 6
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if buttom_lines >= 1:
            for i in range(1,buttom_lines + 1) :
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1

    def cut_it():

        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        printcod = get_cache (Printcod, {"emu": [(eq, printer.emu)],"code": [(eq, "cut")]})

        if printcod:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(printcod.contcod)
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1


    def cal_totalfb():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        billdate:date = None
        fact:int = 0

        if not print_fbtotal:
            return

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

        if not h_bill_line:
            return
        
        billdate = h_bill_line.bill_datum

        h_journal_obj_list = {}
        for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).filter(
                 (H_journal.bill_datum == billdate) & (H_journal.departement == h_bill.departement) & (H_journal.rechnr == h_bill.rechnr)).order_by(H_journal._recid).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True

            fact = 1

            if h_artikel.artnr == disc_art1:
                total_fdisc =  to_decimal(total_fdisc) + to_decimal(fact) * to_decimal(h_journal.epreis)

            elif h_artikel.artnr == disc_art2:
                total_bdisc =  to_decimal(total_bdisc) + to_decimal(fact) * to_decimal(h_journal.epreis)

            elif h_artikel.artnr == disc_art3:
                total_odisc =  to_decimal(total_odisc) + to_decimal(fact) * to_decimal(h_journal.epreis)
            else:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    total_food =  to_decimal(total_food) + to_decimal(fact) * to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis)

                elif artikel.umsatzart == 6:
                    total_bev =  to_decimal(total_bev) + to_decimal(fact) * to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis)

                elif artikel.umsatzart == 4:
                    total_other =  to_decimal(total_other) + to_decimal(fact) * to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis)


    def print_totalfb():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        pos:int = 0
        s:string = ""
        i:int = 0
        nbez1:int = 0

        h_bill_line = db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.artnr == f_discart) & (substring(H_bill_line.bezeich, length(H_bill_line.bezeich) - 1) == ("*").lower())).first()

        if h_bill_line:
            return
        pos = 5

        if qty1000:
            pos = 6

        nbez1 = nbezeich

        if prtwoline:
            nbez1 = nbez1 - 11

        if total_food != 0 or total_bev != 0 or total_other != 0:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_food != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")

            s = translateExtended ("FOOD", lvcarea, "")
            for i in range(1,nbez1 + 1) :
                if i > length(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")

            output_list.str = output_list.str + to_string(total_food, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_bev != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("BEVERAGE", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > length(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_bev, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_other != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("OTHER", lvcarea, "")
            for i in range(1,nbez1 + 1) :
                if i > length(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")

            output_list.str = output_list.str + to_string(total_other, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_fdisc != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")

            s = translateExtended ("DISC FOOD", lvcarea, "")
            for i in range(1,nbez1 + 1) :
                if i > length(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")

            output_list.str = output_list.str + to_string(total_fdisc, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_bdisc != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("DISC BEVERAGE", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > length(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_bdisc, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_odisc != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")

            s = translateExtended ("DISC OTHER", lvcarea, "")
            for i in range(1,nbez1 + 1) :
                if i > length(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")

            output_list.str = output_list.str + to_string(total_odisc, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1
        printed_line = printed_line + 1

    def multi_currency():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        i:int = 0
        n:int = 0
        mesval:string = ""
        s:string = ""
        exchg_rate:Decimal = to_decimal("0.0")
        foreign_amt:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 830)]})

        if htparam.feldtyp != 5 or htparam.fchar == "":

            return
        for i in range(1,num_entries(htparam.fchar, ";")  + 1) :
            mesval = trim(entry(i - 1, htparam.fchar, ";"))

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, mesval)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                foreign_amt = to_decimal(round(tot_amount / exchg_rate , 2))
                s = waehrung.wabkurz + " " + translateExtended ("TOTAL", lvcarea, "")

                if qty1000:
                    output_list.str = output_list.str + to_string("", "x(6)")
                else:
                    output_list.str = output_list.str + to_string("", "x(5)")

                for n in range(1,(nbezeich - 2)  + 1) :
                    if n > length(s):
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str = output_list.str + to_string(substring(s, n - 1, 1) , "x(1)")

                output_list.str = output_list.str + to_string(foreign_amt, "->>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                curr_j = curr_j + 1
                printed_line = printed_line + 1

    def print_net_vat():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        lpage1:int = 0
        net_amt:Decimal = to_decimal("0.0")
        vat_str:string = ""
        vat_proz:Decimal = to_decimal("0.0")
        vat_num:int = 0

        if comp_taxserv or rm_transfer:
            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 376)]})

        if not htparam.flogical:
            return
        
        vat_list_data.clear()

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0) & (H_artikel.mwst_code != 0)).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True

            htparam = get_cache (Htparam, {"paramnr": [(eq, h_artikel.mwst_code)]})

            if htparam.fdecimal != 0:
                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vat_amt == htparam.fdecimal), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                    vat_list.vat_amt =  to_decimal(htparam.fdecimal)

                vat_list.betrag_amt =  to_decimal(vat_list.betrag_amt) + to_decimal(h_bill_line.betrag)

        vat_list = query(vat_list_data, first=True)

        if vat_list:
            net_amt =  to_decimal("0")

            for vat_list in query(vat_list_data):
                vat_num = vat_num + 1
                vat_proz =  to_decimal(vat_list.vat_amt)
                net_amt =  to_decimal(net_amt) + to_decimal(vat_list.betrag_amt) / to_decimal((1) + to_decimal(vat_list.vat_amt) / to_decimal(100))
                vat_list_data.remove(vat_list)
            net_amt = to_decimal(round(net_amt , price_decimal))
            mwst1 =  to_decimal(tot_sales) - to_decimal(net_amt)

        else:
            net_amt =  to_decimal(tot_amount) - to_decimal(mwst1)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 872)]})

        if htparam.fchar != "":
            vat_str = htparam.fchar
        else:
            vat_str = translateExtended ("VAT", lvcarea, "")

        if vat_num == 1:
            vat_str = vat_str + " " + to_string(vat_proz) + "%"

        if anz_foot == 0:
            lpage1 = lpage - 3
        else:
            lpage1 = lpage - 7

        if curr_j > lpage1:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag_popup = True
            output_list.npause = npause
            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            curr_j = 0
            printed_line = 0
            print_overhead1()

        if qty1000:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(translateExtended ("NET", lvcarea, ""))
            output_list.pos = 7
            output_list.str = output_list.str + to_string(" ")
        else:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(translateExtended ("NET", lvcarea, ""))
            output_list.pos = 6
            output_list.str = output_list.str + to_string(" ")

        if not long_digit:
            output_list.str = output_list.str + to_string(net_amt, "->>,>>>,>>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + to_string(net_amt, "->,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

        printed_line = printed_line + 2

        if qty1000:
            output_list.str = output_list.str + to_string(vat_str)
            output_list.pos = 7
            output_list.str = output_list.str + to_string(" ")
        else:
            output_list.str = output_list.str + to_string(vat_str)
            output_list.pos = 6
            output_list.str = output_list.str + to_string(" ")

        if not long_digit:
            output_list.str = output_list.str + to_string(mwst1, "->>,>>>,>>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + to_string(mwst1, "->,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        printed_line = printed_line + 2

    def print_in_word():
        nonlocal winprinterflag, filename, msg_str, output_list_data, t_printer_data, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, foot3, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, str451, sc_art, mwst_perc, serv_perc, serv_code, vat_code, servtax_use_foart, h_mjourn, printer, artikel, h_bill, h_bill_line, htparam, hoteldpt, queasy, h_queasy, kellner, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, printcod, h_journal, waehrung
        nonlocal pvilanguage, hbrecid, printnr, use_h_queasy, session_parameter, user_init, billnr, print_all
        nonlocal artbuff, abuff, bart_list_submenu

        nonlocal art_list, art_list_submenu, t_printer, vat_list, output_list, bline_vatlist, artbuff, abuff, bart_list_submenu
        nonlocal art_list_data, art_list_submenu_data, t_printer_data, vat_list_data, output_list_data, bline_vatlist_data

        lpage1:int = 0
        progname:string = ""
        str1:string = ""
        str2:string = ""
        w_length:int = 0
        i:int = 0

        if comp_taxserv:
            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 825)]})

        if htparam.flogical == False:
            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 829)]})

        if htparam.fchar == "":
            return

        if anz_foot == 0:
            lpage1 = lpage - 3
        else:
            lpage1 = lpage - 7

        if curr_j > lpage1:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag_popup = True
            output_list.npause = npause
            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            curr_j = 0
            printed_line = 0
            print_overhead1()
        progname = htparam.fchar
        w_length = nbezeich

        if not prtwoline:
            w_length = w_length + 15
        str1, str2 = get_output(run_program(progname,(tot_amount, w_length)))
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1

        if qty1000:
            output_list.str = output_list.str + to_string("", "x(6)")
        else:
            output_list.str = output_list.str + to_string("", "x(5)")

        for i in range(1,length(str1)  + 1) :
            output_list.str = output_list.str + to_string(substring(str1, i - 1, 1) , "x(1)")

        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1
        printed_line = printed_line + 2

        if trim(str2) != "":
            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")

            for i in range(1,length(str2)  + 1) :
                output_list.str = output_list.str + to_string(substring(str2, i - 1, 1) , "x(1)")

            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

    mwst_str = translateExtended ("Government Tax", lvcarea, "")
    service_str = translateExtended ("service Charge", lvcarea, "")
    str451 = get_output(htpchar(451))
    str451 = replace_str(str451, "," , ";")
    str451 = replace_str(str451, "-" , ";")
    sc_art = to_int(entry(0, str451, ";"))

    if sc_art != 0:
        h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)],"artnr": [(eq, sc_art)]})

        if h_bill_line:
            print_all = True
            print_all, filename, msg_str, winprinterflag, output_list_data, t_printer_data = get_output(print_hbill1_phbl(pvilanguage, session_parameter, user_init, hbrecid, printnr, use_h_queasy, print_all))

            return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})

    if htparam:
        serv_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})

    if htparam:
        vat_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam.finteger != 0:
        f_discart = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 376)]})

    if htparam:
        if not htparam.flogical and entry(0, htparam.fchar, ";") == ("GST(MA)").lower() :
            gst_logic = True

    if printnr > 0:
        printer = get_cache (Printer, {"nr": [(eq, printnr)]})

        if not printer:
            msg_str = translateExtended ("No such Printer Number:", lvcarea, "") + " " + to_string(printnr)

            return generate_output()
        t_printer = T_printer()
        t_printer_data.append(t_printer)

        buffer_copy(printer, t_printer)
    order_id, prdisc_flag, disc_art1, disc_art2, disc_art3, disc_zwkum, print_balance, incl_service, incl_mwst, service_taxable, print_fbtotal = get_output(prepare_pr_sphbill1bl(hbrecid))

    if printnr != 0:
        h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})

        if not h_bill:
            return generate_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if artikel:
            artbuff = get_cache (Artikel, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, h_bill.departement)]})

            if artbuff and artbuff.endkum == artikel.endkum:
                mwst_str = artbuff.bezeich
            else:
                mwst_str = artikel.bezeich

        htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if artikel:
            service_str = artikel.bezeich

        htparam = get_cache (Htparam, {"paramnr": [(eq, 850)]})
        hmargin = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 858)]})

        if htparam.finteger != 0:
            bmargin = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 851)]})
        lpage = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 871)]})
        nbezeich = 50

        htparam = get_cache (Htparam, {"paramnr": [(eq, 831)]})
        nwidth = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 890)]})
        npause = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date110 = htparam.fdate
        bill_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + timedelta(days=1)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        if price_decimal == 0:
            n11 = 12

        htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
        long_digit = htparam.flogical

        if long_digit:
            n11 = 14

        htparam = get_cache (Htparam, {"paramnr": [(eq, 874)]})

        if htparam.feldtyp == 4 and htparam.flogical:
            print_all = True

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_bill.departement)]})

        if hoteldpt:
            servtax_use_foart = hoteldpt.defult
        optional_params()

        if prtwoline:
            n11 = 1

        if not use_h_queasy:
            queasy = get_cache (Queasy, {"key": [(eq, 4)],"number1": [(eq, (h_bill.departement + h_bill.rechnr * 100))],"number2": [(eq, 0)],"deci2": [(eq, billnr)]})

            if queasy and not print_all:
                printed_line = queasy.number3
                last_amount =  to_decimal(queasy.deci1)

                if printed_line == lpage:
                    printed_line = 0

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 4
                queasy.number1 = (h_bill.departement + h_bill.rechnr * 100)
                queasy.number2 = 0
                queasy.deci2 =  to_decimal(billnr)

        else:

            h_queasy = get_cache (H_queasy, {"number1": [(eq, (h_bill.departement + h_bill.rechnr * 100))],"number2": [(eq, 0)],"billno": [(eq, billnr)]})

            if h_queasy and not print_all:
                printed_line = h_queasy.number3
                last_amount =  to_decimal(h_queasy.deci1)

                if printed_line == lpage:
                    printed_line = 0

            if not h_queasy:
                h_queasy = H_queasy()
                db_session.add(h_queasy)

                h_queasy.number1 = (h_bill.departement + h_bill.rechnr * 100)
                h_queasy.number2 = 0
                h_queasy.billno = billnr

        kellner = get_cache (Kellner, {"departement": [(eq, h_bill.departement)],"kellner_nr": [(eq, h_bill.kellner_nr)]})

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_bill.departement)]})
        zeit = get_current_time_in_seconds()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 824)]})
        comp_flag = htparam.flogical
        service =  to_decimal("0")
        mwst =  to_decimal("0")
        tot_amount =  to_decimal(last_amount)

        if h_bill.flag == 1:
            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

            if h_bill_line:
                bill_date = h_bill_line.bill_datum

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.waehrungsnr == billnr)).order_by(H_bill_line._recid).all():

            if h_bill_line.artnr != 0:
                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                if (h_artikel.artart == 11 or h_artikel.artart == 12):
                    comp_taxserv = not comp_taxserv

                elif h_artikel.artart == 0:
                    tot_sales =  to_decimal(tot_sales) + to_decimal(h_bill_line.betrag)
            new_item = False
            printed = True

            if not use_h_queasy:
                queasy = get_cache (Queasy, {"key": [(eq, 4)],"number1": [(eq, (h_bill.departement + h_bill.rechnr * 100))],"number2": [(eq, to_int(h_bill_line._recid))],"deci2": [(eq, billnr)]})

                if not queasy:
                    new_item = True

                    if printnr >= 0:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 4
                        queasy.number1 = (h_bill.departement + h_bill.rechnr * 100)
                        queasy.number2 = to_int(h_bill_line._recid)
                        queasy.deci2 =  to_decimal(billnr)

            else:
                h_queasy = get_cache (H_queasy, {"number1": [(eq, (h_bill.departement + h_bill.rechnr * 100))],"number2": [(eq, to_int(h_bill_line._recid))],"billno": [(eq, billnr)]})

                if not h_queasy:
                    new_item = True

                    if printnr >= 0:
                        h_queasy = H_queasy()
                        db_session.add(h_queasy)

                        h_queasy.number1 = (h_bill.departement +\
                                h_bill.rechnr * 100)
                        h_queasy.number2 = to_int(h_bill_line._recid)
                        h_queasy.billno = billnr

            if new_item or print_all:
                printed = False

            if (h_bill_line.artnr == 0 or h_artikel.artart != 0) and not new_item:
                new_item = True
                printed = True

            qty = h_bill_line.anzahl

            if qty == 0:
                qty = 1
            pass
            do_it = None != h_artikel and h_artikel.artart == 0 and h_artikel.zwkum != disc_zwkum

            if do_it:
                art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == h_bill_line.artnr and art_list.dept == h_bill_line.departement and art_list.bezeich == h_bill_line.bezeich and art_list.price == h_bill_line.epreis and art_list.condiment == 0 and not art_list.printed), first=True)

            if h_bill_line.artnr == 0:
                rm_transfer = not rm_transfer

            if h_bill_line.artnr != 0:
                if h_artikel.artart == 0 and (new_item or print_all):
                    new_fbart = True

            if not art_list: # Malik : C68F4A
                art_list = Art_list()
                art_list_data.append(art_list)

                art_list.printed = printed
                art_list.artnr = h_bill_line.artnr
                art_list.dept = h_bill_line.departement
                art_list.bezeich = h_bill_line.bezeich
                art_list.price =  to_decimal(h_bill_line.epreis)
                art_list.datum = h_bill_line.bill_datum
                art_list.sysdate = h_bill_line.sysdate
                art_list.zeit = h_bill_line.zeit
                art_list.hline_recid = h_bill_line._recid

                if h_bill_line.artnr != 0:
                    art_list.artart = h_artikel.artart
                    art_list.zwkum = h_artikel.zwkum
                else:
                    art_list.artart = 2

                if h_artikel and h_artikel.artart == 0 and h_artikel.epreis2 != 0 and art_list.price == h_artikel.epreis2:
                    art_list.happyhr = "*"

                if h_artikel and h_artikel.artart == 0:
                    # art_list.condiment = h_bill_line.betriebsnr
                    art_list.condiment = h_artikel.betriebsnr
                art_list.disc_flag = prdisc_flag and (art_list.zwkum == disc_zwkum)
                tot_line = tot_line + 1
            art_list.betrag =  to_decimal(art_list.betrag) + to_decimal(h_bill_line.betrag)
            h_service =  to_decimal("0")
            h_mwst =  to_decimal("0")

            # log_program.write_log("DEBUG1", f"art_list = {art_list_data}", "Log_Rulita.txt")

            amount =  to_decimal(h_bill_line.betrag)

            if art_list.artart == 0:
                serv_perc, mwst_perc, fact = cal_servat(h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_bill_line.bill_datum)
                # Rulita 03/02/2026
                # Fixing issue service tax pecent
                # mwst_perc =  to_decimal(mwst_perc) * to_decimal("100")
                # serv_perc =  to_decimal(serv_perc) * to_decimal("100")

                if h_bill_line.artnr == f_discart:
                    if h_bill_line.epreis != h_bill_line.betrag:
                        if not serv_disc and h_bill_line.artnr == f_discart:
                            pass
                        else:
                            h_service =  to_decimal(h_bill_line.betrag) / to_decimal(fact) * to_decimal(serv_perc)
                            h_service = to_decimal(round(h_service , 2))

                        if not vat_disc and h_bill_line.artnr == f_discart:
                            pass
                        else:
                            h_mwst =  to_decimal(h_bill_line.betrag) / to_decimal(fact) * to_decimal(mwst_perc)
                            h_mwst = to_decimal(round(h_mwst , 2))

                        if not incl_service:
                            amount =  to_decimal(amount) - to_decimal(h_service)
                            service =  to_decimal(service) + to_decimal(h_service)

                        if not incl_mwst:
                            amount =  to_decimal(amount) - to_decimal(h_mwst)
                            mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                            mwst1 =  to_decimal(mwst1) + to_decimal(h_mwst)

                else:
                    if not serv_disc and h_bill_line.artnr == f_discart:
                        pass
                    else:
                        h_service =  to_decimal(h_bill_line.betrag) / to_decimal(fact) * to_decimal(serv_perc)
                        h_service = to_decimal(round(h_service , 2))

                    if not vat_disc and h_bill_line.artnr == f_discart:
                        pass
                    else:
                        h_mwst =  to_decimal(h_bill_line.betrag) / to_decimal(fact) * to_decimal(mwst_perc)
                        h_mwst = to_decimal(round(h_mwst , 2))

                    if not incl_service:
                        amount =  to_decimal(amount) - to_decimal(h_service)
                        service =  to_decimal(service) + to_decimal(h_service)

                    if not incl_mwst:
                        amount =  to_decimal(amount) - to_decimal(h_mwst)
                        mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                        mwst1 =  to_decimal(mwst1) + to_decimal(h_mwst)

                if not art_list.disc_flag:
                    subtotal =  to_decimal(subtotal) + to_decimal(amount)

            art_list.amount =  to_decimal(art_list.amount) + to_decimal(amount)

            if h_bill_line.artnr != 0:
                # art_list.qty = art_list.qty + qty
                if h_bill_line.betriebsnr != 1:
                    art_list.qty = art_list.qty + qty
                else:
                    art_list.qty = qty # Malik : C68F4A

        for art_list in query(art_list_data):
            if art_list.qty == 0 and round(art_list.amount, 0) == 0:
                art_list_data.remove(art_list)
                tot_line = tot_line - 1
                bline_exist = True

            elif art_list.qty > 999 or art_list.qty < -999:
                qty1000 = True

        h_mjourn = db_session.query(H_mjourn).filter(
            (H_mjourn.rechnr == h_bill.rechnr) & (H_mjourn.departement == h_bill.departement) & (H_mjourn.anzahl < 0)).first()

        if h_mjourn:
            for h_mjourn in db_session.query(H_mjourn).filter(
                (H_mjourn.rechnr == h_bill.rechnr) & (H_mjourn.departement == h_bill.departement)).order_by(H_mjourn.h_artnr, H_mjourn.artnr).all():
                art_list_submenu = Art_list_submenu()
                art_list_submenu_data.append(art_list_submenu)

                buffer_copy(h_mjourn, art_list_submenu)

                if num_entries(h_mjourn.request, "|") > 1:
                    art_list_submenu.hline_recid = to_int(entry(0, h_mjourn.request, "|"))

            for art_list_submenu in query(art_list_submenu_data, filters=(lambda art_list_submenu: art_list_submenu.anzahl > 0), sort_by=[("h_artnr",False),("artnr",False)]):
                bart_list_submenu = query(bart_list_submenu_data, filters=(lambda bart_list_submenu: bart_list_submenu.h_artnr == art_list_submenu.h_artnr and bart_list_submenu.artnr == art_list_submenu.artnr and bart_list_submenu.anzahl < 0 and bart_list_submenu.anzahl == (- art_list_submenu.anzahl)), first=True)

                if bart_list_submenu:
                    art_list_submenu_data.remove(art_list_submenu)
                    bart_list_submenu_data.remove(bart_list_submenu)

            for art_list in query(art_list_data, filters=(lambda art_list: art_list.condiment != 0)):
                art_list_submenu = query(art_list_submenu_data, filters=(lambda art_list_submenu: art_list_submenu.hline_recid == art_list.hline_recid), first=True)

                if art_list_submenu:
                    pass
                else:
                    art_list_data.remove(art_list)
                    tot_line = tot_line - 1  # Malik : C68F4A
                    
        for abuff in query(abuff_data, filters=(lambda abuff:(abuff.zwkum == disc_zwkum) and matches(abuff.bezeich,r"*-*"))):
            disc_bezeich = replace_str(abuff.bezeich, "-", "")

            art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == abuff.artnr and art_list.bezeich.lower()  == (disc_bezeich).lower()  and art_list.amount == - abuff.amount), first=True)

            if art_list:
                art_list_data.remove(art_list)
                abuff_data.remove(abuff)
                tot_line = tot_line - 2

        for abuff in query(abuff_data, filters=(lambda abuff: abuff.disc_flag)):
            disc_bezeich = abuff.bezeich

            art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == abuff.artnr and art_list.bezeich.lower()  == (disc_bezeich).lower()  and art_list.amount == - abuff.amount), first=True)

            if art_list:
                art_list_data.remove(art_list)
                abuff_data.remove(abuff)
                tot_line = tot_line - 2
        add_unitprice_text()

        art_list = query(art_list_data, filters=(lambda art_list: art_list.printed == False), first=True)

        if not art_list and printnr >= 0 and not bline_exist:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("No new bill-lines was found.", lvcarea, "")

            return generate_output()
        check_pages()

        if printnr > 0:
            pass

        elif printnr < 0:
            filename = "billdir\\" + to_string(h_bill.tischnr) + "_" + to_string(h_bill.departement, "99")

        for i in range(1,printed_line + 1) :
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.str = output_list.str + to_string("")
            output_list.sort_i = sort_i
            sort_i = sort_i + 1

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1

        if prdisc_flag and tot_ndisc_line >= 1 and tot_disc_line >= 1:
            # art_list = query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and not art_list.disc_flag and not art_list.printed), first=True)
            n = 0
            curr_j = printed_line

            # while i < npage :
            for i in range(1,npage + 1) :
                if not art_list:
                    i = npage

                print_overhead1()

                for art_list in query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and art_list.disc_flag and not art_list.printed)):
                    if curr_j <= lpage :
                        print_billine()

                        if not art_list:
                            i = npage 

                # while None != art_list and (curr_j <= lpage) :
                #     print_billine()

                #     art_list = query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and not art_list.disc_flag and not art_list.printed), next=True)

                #     if not art_list:
                #         i = npage

                if i == npage:
                    print_overhead2(0)

                    for art_list in query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and art_list.disc_flag)):
                        subtotal =  to_decimal(subtotal) + to_decimal(art_list.amount)
                        print_billine()

                    if new_fbart:
                        print_overhead2(1)

                    if overhead3 > 0:
                        print_overhead3()

                    if overhead4 > 0 or buttom_lines >= 1:
                        print_overhead4()
                    cut_it()

                elif curr_j > lpage:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag_popup = True
                    output_list.npause = npause
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

                    curr_j = 0
                    printed_line = 0
        else:
            # art_list = query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and not art_list.printed), first=True)
            n = 0
            curr_j = printed_line

            # while i < npage :
            for i in range(1,npage + 1) :
                if not art_list:
                    i = npage 

                print_overhead1()

                for art_list in query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and art_list.disc_flag and not art_list.printed)):
                    if curr_j <= lpage :

                    # while None != art_list and (curr_j <= lpage) :
                        print_billine()

                        # art_list = query(art_list_data, filters=(lambda art_list: art_list.artart == 0 and not art_list.printed), next=True)

                        if not art_list:
                            i = npage + 1

                if i == npage:
                    if new_fbart:
                        print_overhead2(2)

                    if overhead3 > 0:
                        print_overhead3()

                    if overhead4 > 0 or buttom_lines >= 1:
                        print_overhead4()
                    cut_it()

                elif curr_j > lpage:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag_popup = True
                    output_list.npause = npause
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

                    curr_j = 0
                    printed_line = 0
        tot_amount =  to_decimal("0")

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
            tot_amount =  to_decimal(tot_amount) + to_decimal(h_bill_line.betrag)

        if printnr >= 0:
            if not use_h_queasy:
                queasy = get_cache (Queasy, {"key": [(eq, 4)],"number1": [(eq, (h_bill.departement + h_bill.rechnr * 100))],"number2": [(eq, 0)],"deci2": [(eq, billnr)]})
                queasy.number3 = printed_line
                queasy.deci1 =  to_decimal(tot_amount)

            else:
                h_queasy = get_cache (H_queasy, {"number1": [(eq, (h_bill.departement + h_bill.rechnr * 100))],"number2": [(eq, 0)],"billno": [(eq, billnr)]})
                
                if h_queasy:
                    h_queasy.number3 = printed_line
                    h_queasy.deci1 =  to_decimal(tot_amount)

    return generate_output()