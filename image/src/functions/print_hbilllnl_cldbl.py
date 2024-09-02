from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_print_hbill1bl import prepare_print_hbill1bl
import re
from sqlalchemy import func
from models import Printer, Artikel, Htparam, H_bill, Hoteldpt, Queasy, H_queasy, Kellner, H_bill_line, H_artikel, Kontplan, Paramtext, Bediener, Tisch, Res_line, Mc_guest, H_mjourn, Guest, Printcod, H_journal, Waehrung

def print_hbilllnl_cldbl(pvilanguage:int, session_parameter:str, user_init:str, hbrecid:int, printnr:int, use_h_queasy:bool, print_all:bool):
    filename = ""
    msg_str = ""
    winprinterflag = False
    output_list_list = []
    t_printer_list = []
    lvcarea:str = "print_hbill1"
    disc_bezeich:str = ""
    amount:decimal = 0
    sort_i:int = 0
    order_id:str = ""
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
    mwst_str:str = ""
    service_str:str = ""
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
    last_amount:decimal = 0
    zeit:int = 0
    comp_flag:bool = False
    service:decimal = 0
    mwst:decimal = 0
    tot_amount:decimal = 0
    comp_taxserv:bool = False
    tot_sales:decimal = 0
    new_item:bool = False
    printed:bool = False
    qty:int = 0
    do_it:bool = False
    rm_transfer:bool = False
    new_fbart:bool = False
    tot_line:int = 0
    h_service:decimal = 0
    h_mwst:decimal = 0
    serv_perc:decimal = 0
    mwst_perc:decimal = 0
    fact:decimal = 1
    mwst1:decimal = 0
    subtotal:decimal = 0
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
    header1:str = ""
    header2:str = ""
    foot1:str = ""
    foot2:str = ""
    anz_foot:int = 0
    overhead1:int = 0
    overhead2:int = 0
    overhead3:int = 0
    overhead4:int = 0
    total_food:decimal = 0
    total_bev:decimal = 0
    total_other:decimal = 0
    total_fdisc:decimal = 0
    total_bdisc:decimal = 0
    total_odisc:decimal = 0
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    guest_addr:str = ""
    serv_code:int = 0
    vat_code:int = 0
    servtax_use_foart:bool = False
    printer = artikel = htparam = h_bill = hoteldpt = queasy = h_queasy = kellner = h_bill_line = h_artikel = kontplan = paramtext = bediener = tisch = res_line = mc_guest = h_mjourn = guest = printcod = h_journal = waehrung = None

    art_list = t_printer = vat_list = output_list = artbuff = abuff = hbuff = h_art = None

    art_list_list, Art_list = create_model("Art_list", {"printed":bool, "disc_flag":bool, "dept":int, "artnr":int, "bezeich":str, "artart":int, "zwkum":int, "qty":int, "price":decimal, "amount":decimal, "betrag":decimal, "happyhr":str, "datum":date, "sysdate":date, "zeit":int, "condiment":int})
    t_printer_list, T_printer = create_model_like(Printer)
    vat_list_list, Vat_list = create_model("Vat_list", {"vat_amt":decimal, "betrag_amt":decimal})
    output_list_list, Output_list = create_model("Output_list", {"str":str, "str_pos":int, "pos":int, "flag_popup":bool, "npause":int, "sort_i":int})

    Artbuff = Artikel
    Abuff = Artikel
    Hbuff = H_artikel
    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list
        return {"filename": filename, "msg_str": msg_str, "winprinterflag": winprinterflag, "output-list": output_list_list, "t-printer": t_printer_list}

    def optional_params():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        lvctmp:str = ""
        lvcleft:str = ""
        lvcval:str = ""
        lvicnt:int = 0
        lvi:int = 0
        lvitmp:int = 0
        lvicnt = num_entries(session_parameter, ";")
        for lvi in range(1,lvicnt + 1) :
            lvctmp = ""
            lvcleft = ""


            lvctmp = trim(entry(lvi - 1, session_parameter, ";"))
            lvcleft = trim(entry(0, lvctmp, " == "))

            if lvcleft == "WINprinter":
                winprinterflag = True
            elif lvcleft == "TableDesc":
                lvcval = entry(1, lvctmp, " == ")

                if lvcval.lower()  == ("YES").lower():
                    prtabledesc = True
            elif lvcleft == "Pr2Line":
                lvcval = entry(1, lvctmp, " == ")

                if lvcval.lower()  == ("YES").lower():
                    prtwoline = True
            elif lvcleft == "print_all":
                lvitmp = to_int(entry(1, lvctmp, " == "))

                if lvitmp == 1:
                    print_all = True
            elif lvcleft == "top_margin":
                lvitmp = -1
                lvitmp = to_int(entry(1, lvctmp, " == "))

                if lvitmp >= 1:
                    hmargin = lvitmp
            elif lvcleft == "num_lines":
                lvitmp = -1
                lvitmp = to_int(entry(1, lvctmp, " == "))

                if lvitmp >= 1:
                    lpage = lvitmp
            elif lvcleft == "DesLen":
                lvitmp = to_int(entry(1, lvctmp, " == "))

                if lvitmp >= 1:
                    nbezeich = lvitmp
            elif lvcleft == "buttom_lines":
                lvitmp = to_int(entry(1, lvctmp, " == "))

                if lvitmp >= 1:
                    buttom_lines = lvitmp
            elif lvcleft == "header1":
                header1 = entry(1, lvctmp, " == ")


            elif lvcleft == "header2":
                header2 = entry(1, lvctmp, " == ")


            elif lvcleft == "foot1":
                foot1 = entry(1, lvctmp, " == ")
                foot2 = ""
                anz_foot = 1


            elif lvcleft == "foot2":
                foot2 = entry(1, lvctmp, " == ")
                anz_foot = 2

    def cal_servat(depart:int, h_artnr:int, service_code:int, mwst_code:int, inpdate:date):

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        serv% = 0
        mwst% = 0
        servat = 0
        serv_htp:decimal = 0
        vat_htp:decimal = 0

        def generate_inner_output():
            return serv%, mwst%, servat
        Hbuff = H_artikel
        Abuff = Artikel

        if bill_date < bill_date110 and (service_code != 0 or mwst_code != 0):

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) &  (Hbuff.departement == depart)).first()

            abuff = db_session.query(Abuff).filter(
                    (Abuff.artnr == hbuff.artnrfront) &  (Abuff.departement == depart)).first()

            kontplan = db_session.query(Kontplan).filter(
                    (Kontplan.betriebsnr == depart) &  (Kontplan.kontignr == abuff.artnr) &  (Kontplan.datum == inpdate)).first()

            if kontplan:
                serv_htp = kontplan.anzkont / 10000
                vat_htp = kontplan.anzconf / 10000


                serv% = serv_htp
                mwst% = vat_htp
                servat = 1 + serv% + mwst%

                return generate_inner_output()
        serv_htp = 0
        vat_htp = 0

        if servtax_use_foart:

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) &  (Hbuff.departement == depart)).first()

            abuff = db_session.query(Abuff).filter(
                    (Abuff.artnr == hbuff.artnrfront) &  (Abuff.departement == depart)).first()

            if abuff:
                service_code = abuff.service_code
                mwst_code = abuff.mwst_code
        else:

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.artnr == h_artnr) &  (Hbuff.departement == depart)).first()

            if hbuff:
                service_code = hbuff.service_code
                mwst_code = hbuff.mwst_code

        if service_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == service_code)).first()
            serv_htp = htparam.fdecimal / 100

        if mwst_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == mwst_code)).first()
            vat_htp = htparam.fdecimal / 100

        if service_taxable:
            serv% = serv_htp
            mwst% = (1 + serv_htp) * vat_htp
            servat = 1 + serv% + mwst%


        else:
            serv% = serv_htp
            mwst% = vat_htp
            servat = 1 + serv% + mwst%


        return generate_inner_output()

    def add_unitprice_text():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        n:int = 0
        s:str = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 412)).first()

        if not htparam.flogical:

            return

        if htparam.paramgruppe != 19:

            return

        if prtwoline:

            return

        for art_list in query(art_list_list, filters=(lambda art_list :(art_list.qty != 1) and (art_list.qty != -1) and art_list.qty != 0 and art_list.artnr != 0)):
            s = " @" + to_string(art_list.price)

            if len(art_list.bezeich + s) <= nbezeich:
                art_list.bezeich = art_list.bezeich + s
            else:
                art_list.bezeich = substring(art_list.bezeich, 0, nbezeich - len(s)) + s

    def check_pages():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        total_line:int = 0
        new_sold_item:bool = False

        if prdisc_flag:

            for art_list in query(art_list_list, filters=(lambda art_list :art_list.artart == 0)):

                if art_list.disc_flag:
                    tot_disc_line = tot_disc_line + 1
                else:
                    tot_ndisc_line = tot_ndisc_line + 1

        art_list = query(art_list_list, filters=(lambda art_list :art_list.artart == 0), first=True)
        new_sold_item = None != art_list
        overhead1 = hmargin + bmargin + 3
        overhead2 = 6
        overhead3 = 0

        for art_list in query(art_list_list, filters=(lambda art_list :art_list.artart != 0)):

            if new_sold_item or (not art_list.printed):
                overhead3 = overhead3 + 1

        if overhead3 != 0:
            overhead3 = overhead3 + 2

        if h_bill.saldo == 0 or print_all:

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 712)).first()

            if foot2 == "" and paramtext.ptexte != "":
                foot2 = paramtext.ptexte
                anz_foot = 2

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 711)).first()

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

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        i:int = 0
        rechnr_str:str = ""
        kname:str = ""

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            kname = bediener.username

        elif kellner:
            kname = kellnername

        if printed_line == 0 or print_all:
            for i in range(1,hmargin + 1) :
                output_list.str = output_list.str + to_string(" ")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                curr_j = curr_j + 1
                printed_line = printed_line + 1

            if header1 != "":
                for i in range(1,len(header1)  + 1) :
                    output_list.str = output_list.str + to_string(substring(header1, i - 1, 1) , "x(1)")
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1

            if header2 != "":
                for i in range(1,len(header2)  + 1) :
                    output_list.str = output_list.str + to_string(substring(header2, i - 1, 1) , "x(1)")
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1

            if header1 != "" or header2 != "":
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_list.append(output_list)

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
                        "     " + to_string(bill_date) + "|" +\
                        to_string(time, "HH:MM") + "|" +\
                        translateExtended ("Tax Invoice No", lvcarea, "") + "|" +\
                        rechnr_str


                else:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        "     " + to_string(bill_date) + "|" +\
                        to_string(time, "HH:MM") + "|" +\
                        translateExtended ("BillNo", lvcarea, "") + "|" +\
                        rechnr_str


                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 2
                output_list.str = output_list.str + to_string("     " + hoteldpt.depart, "x(32)")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 3
                output_list.str = output_list.str + "     " + translateExtended ("Table", lvcarea, "") + "|" + to_string(h_bill.tischnr, ">>>>9") + "|" + to_string(h_bill.belegung, "->>>9 ") + "|" + to_string(kname, "x(32)") + "|" + order_id
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

                if prtabledesc:

                    tisch = db_session.query(Tisch).filter(
                            (Tischnr == h_bill.tischnr) &  (Tisch.departement == h_bill.departement)).first()

                    if tisch and tisch.bezeich != "":
                        output_list.str_pos = 4
                        output_list.str = output_list.str + to_string("     " + tisch.bezeich, "x(32)")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                        curr_j = curr_j + 1
                output_list.str_pos = 5
                output_list.str = output_list.str + to_string("     " + translateExtended ("Guest", lvcarea, "") + "|" + h_bill.bilname, "x(32)")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

                if gst_logic:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str_pos = 6
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str = output_list.str +\
                            to_string("            " + translateExtended ("Tax Invoice", lvcarea, ""))


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str_pos = 7
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str = output_list.str +\
                            to_string("       " + translateExtended ("GST ID : 00185060352", lvcarea, ""))


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                curr_j = curr_j + 4
                printed_line = printed_line + 4

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                    if res_line:

                        mc_guest = db_session.query(Mc_guest).filter(
                                (Mc_guest.gastnr == res_line.gastnrmember) &  (Mc_guest.activeflag)).first()

                elif h_bill.resnr > 0 and h_bill.reslinnr == 0:

                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == h_bill.resnr) &  (Mc_guest.activeflag)).first()

                if mc_guest:
                    output_list.str_pos = 8
                    output_list.str = output_list.str + to_string("     " + translateExtended ("MemberCard", lvcarea, "") + " " + mc_guest.cardnum, "x(32)")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    curr_j = curr_j + 1
                    printed_line = printed_line + 1
            else:

                if gst_logic:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        "     " + to_string(bill_date) + "|" +\
                        to_string(time, "HH:MM") + "|" +\
                        translateExtended ("Tax Invoice No", lvcarea, "") + "|" +\
                        rechnr_str


                else:
                    output_list.str_pos = 1
                    output_list.str = output_list.str +\
                        "     " + to_string(bill_date) + "|" +\
                        to_string(get_current_time_in_seconds(), "HH:MM") + "|" +\
                        translateExtended ("BillNo", lvcarea, "") + "|" +\
                        rechnr_str


                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 2
                output_list.str = output_list.str + to_string("     " + hoteldpt.depart, "x(32)")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str_pos = 3
                output_list.str = output_list.str + "     " + translateExtended ("Table", lvcarea, "") + "|" + to_string(h_bill.tischnr, ">>>9") + "|" + to_string(h_bill.belegung, "->>>9 ") + "|" + to_string(kname, "x(32)") + "|" + order_id
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

                if gst_logic:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str_pos = 4
                    output_list.str = output_list.str +\
                            to_string("            " + translateExtended ("Tax Invoice", lvcarea, ""))


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                    output_list.str_pos = 5
                    output_list.str = output_list.str +\
                            to_string("       " + translateExtended ("GST ID : 00185060352", lvcarea, ""))


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

                if prtabledesc:

                    tisch = db_session.query(Tisch).filter(
                            (Tischnr == h_bill.tischnr) &  (Tisch.departement == h_bill.departement)).first()

                    if tisch and tisch.bezeich != "":
                        output_list.str_pos = 6
                        output_list.str = output_list.str + to_string("     " + tisch.bezeich, "x(32)")
                        output_list = Output_list()
                        output_list_list.append(output_list)

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
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1

    def print_billine():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        i:int = 0
        anz:int = 0
        leerch:str = ""
        ct:str = ""
        bezeich:str = ""
        H_art = H_artikel
        bezeich = art_list.happyhr + art_list.bezeich

        if qty1000:
            output_list.str_pos = 10
            output_list.str = output_list.str + to_string("   ") + to_string(art_list.qty, "->>>> ") + "|"


        else:
            output_list.str_pos = 10
            output_list.str = output_list.str + to_string("   ") + to_string(art_list.qty) + "|"


        for i in range(1,30 + 1) :

            if i > len(bezeich):
                output_list.str = output_list.str + to_string(" ")
            else:
                output_list.str = output_list.str + to_string(substring(bezeich, i - 1, 1) , "x(1)")
        output_list.str = output_list.str + "|"

        if prtwoline:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_list.append(output_list)

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


        output_list = Output_list()
        output_list_list.append(output_list)

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
                ct = "@" + to_string(art_list.price, "->,>>>,>>9") + leerch + to_string(art_list.amount, "->>>,>>>,>>9") + chr(10)
            else:
                ct = "@" + to_string(art_list.price, "->>,>>9.99") + leerch + to_string(art_list.amount, "->>,>>>,>>9.99") + chr(10)
            for i in range(1,len(ct)  + 1) :
                output_list.str = output_list.str + to_string(substring(ct, i - 1, 1) , "x(1)")
            curr_j = curr_j + 1
            printed_line = printed_line + 1

        if art_list.condiment == 0 or art_list.disc_flag:

            return

        for h_mjourn in db_session.query(H_mjourn).filter(
                (H_mjourn.departement == art_list.dept) &  (H_mjourn.h_artnr == art_list.artnr) &  (H_mjourn.rechnr == h_bill.rechnr) &  (H_mjourn.bill_datum == art_list.datum) &  (H_mjourn.sysdate == art_list.sysdate) &  (H_mjourn.zeit == art_list.zeit)).all():

            h_art = db_session.query(H_art).filter(
                    (H_art.artnr == h_mjourn.artnr) &  (H_art.departement == dept)).first()

            if h_art:
                bezeich = h_art.bezeich
                output_list.str = output_list.str + to_string(art_list.qty) + to_string(" ")
                for i in range(1,nbezeich + 1) :

                    if i > len(bezeich):
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str = output_list.str + to_string(substring(bezeich, i - 1, 1) , "x(1)")
                output_list.str = output_list.str + to_string(translateExtended ("(Condiment)", lvcarea, "") , "x(11)")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
            curr_j = curr_j + 1
            printed_line = printed_line + 1

    def print_overhead2(prall_flag:int):

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        i:int = 0
        pos:int = 0
        nbez1:int = 0
        s:str = ""
        tot_str:str = ""

        if curr_j > (lpage - 6):
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list_list.append(output_list)

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
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                printed_line = printed_line + 1
            else:
                s = translateExtended ("subtotal", lvcarea, "")
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str_pos = 11
                    output_list.str = output_list.str + to_string(" ")


                else:
                    output_list.str_pos = 11
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")

            if price_decimal == 0:

                if not long_digit:
                    output_list.str = output_list.str + "|" + to_string(subtotal, "   ->>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(subtotal, "->,>>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
            else:
                output_list.str = output_list.str + "|" + to_string(subtotal, "->>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_list.append(output_list)

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
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                printed_line = printed_line + 1
                tot_amount = subtotal

                return

            if service != 0:
                for i in range(1,pos + 1) :
                    output_list.str = output_list.str + to_string(" ")
                for i in range(1,nbez1 + 1) :

                    if i > len(service_str):
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(" ")


                    else:
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(substring(service_str, i - 1, 1) , "x(1)")

                if price_decimal == 0:

                    if not long_digit:
                        output_list.str = output_list.str + "|" + to_string(service, "   ->>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(service, "->,>>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(service, "->>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                printed_line = printed_line + 1

            if mwst != 0:
                for i in range(1,pos + 1) :
                    output_list.str = output_list.str + to_string(" ")
                for i in range(1,nbez1 + 1) :

                    if i > len(mwst_str):
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(" ")


                    else:
                        output_list.str_pos = 12
                        output_list.str = output_list.str + to_string(substring(mwst_str, i - 1, 1) , "x(1)")

                if price_decimal == 0:

                    if not long_digit:
                        output_list.str = output_list.str + "|" + to_string(mwst, "   ->>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(mwst, "->,>>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(mwst, "->>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                printed_line = printed_line + 1

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
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
        printed_line = printed_line + 1
        for i in range(1,pos + 1) :
            output_list.str = output_list.str + to_string(" ")

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 846)).first()

        if htparam.fchar == "":
            tot_str = translateExtended ("TOTAL", lvcarea, "")
        else:
            tot_str = htparam.fchar
        for i in range(1,nbez1 + 1) :

            if i > len(tot_str):
                output_list.str_pos = 13
                output_list.str = output_list.str + to_string(" ")


            else:
                output_list.str_pos = 13
                output_list.str = output_list.str + to_string(substring(tot_str, i - 1, 1) , "x(1)")


        tot_amount = 0

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart == 0)).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            tot_amount = tot_amount + h_bill_line.betrag

        if price_decimal == 0:

            if not long_digit:
                output_list.str = output_list.str + "|" + to_string(tot_amount, "   ->>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
            else:
                output_list.str = output_list.str + "|" + to_string(tot_amount, "->,>>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + "|" + to_string(tot_amount, "->>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

        if res_line:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:
                guest_addr = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3

        if h_bill.bilname != "":
            output_list.str_pos = 18
            output_list.str = output_list.str + to_string(" ") + to_string(h_bill.bilname, "x(64)")
        printed_line = printed_line + 1
        curr_j = curr_j + 6
        multi_currency()

    def print_overhead3():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        nbez1:int = 0
        i:int = 0
        pos:int = 0
        lpage1:int = 0
        balance:decimal = 0
        amt:decimal = 0
        bal_str:str = ""
        chg_str:str = ""
        new_sold_item:bool = False
        compli_notax:bool = False

        art_list = query(art_list_list, filters=(lambda art_list :art_list.artart == 0), first=True)
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
            output_list_list.append(output_list)

            output_list.flag_popup = True
            output_list.npause = npause
            output_list.sort_i = sort_i
            sort_i = sort_i + 1


            curr_j = 0
            printed_line = 0
            print_overhead1()
        balance = tot_amount

        for art_list in query(art_list_list, filters=(lambda art_list :art_list.artart != 0)):

            if new_sold_item or not art_list.printed:

                if qty1000:
                    output_list.str = output_list.str + to_string("", "x(6)")
                else:
                    output_list.str = output_list.str + to_string("", "x(5)")
                for i in range(1,nbez1 + 1) :

                    if i > len(art_list.bezeich):
                        output_list.str_pos = 14
                        output_list.str = output_list.str + to_string(" ")


                    else:
                        output_list.str_pos = 14
                        output_list.str = output_list.str + to_string(substring(art_list.bezeich, i - 1, 1) , "x(1)")

            if (art_list.artart == 11 or art_list.artart == 12) and comp_taxserv and comp_flag:

                if art_list.amount * subtotal > 0:
                    amt = subtotal
                else:
                    amt = - subtotal
                balance = balance + amt
                last_amount = last_amount + amt
                compli_notax = True

                if new_sold_item or not art_list.printed:

                    if price_decimal == 0:

                        if not long_digit:
                            output_list.str = output_list.str + "|" + to_string(amt, "   ->>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                        else:
                            output_list.str = output_list.str + "|" + to_string(amt, "->,>>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(amt, "->>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    printed_line = printed_line + 1
            else:

                if not art_list.printed or print_all:
                    balance = balance + art_list.amount
                last_amount = last_amount + art_list.amount

                if new_sold_item or not art_list.printed:

                    if price_decimal == 0:

                        if not long_digit:
                            output_list.str = output_list.str + "|" + to_string(art_list.amount, "   ->>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                        else:
                            output_list.str = output_list.str + "|" + to_string(art_list.amount, "->,>>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.sort_i = sort_i
                            sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(art_list.amount, "->>,>>>,>>>,>>9.99")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    printed_line = printed_line + 1

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
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
        printed_line = printed_line + 1
        pos = 5

        if qty1000:
            pos = 6
        for i in range(1,pos + 1) :
            output_list.str = output_list.str + to_string(" ")

        if not compli_notax:
            balance = 0

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).all():
                balance = balance + h_bill_line.betrag

        if (balance >= 0):

            if not rm_transfer or print_balance or balance != 0:
                bal_str = translateExtended ("balance", lvcarea, "")
                for i in range(1,nbez1 + 1) :

                    if i > len(bal_str):
                        output_list.str_pos = 15
                        output_list.str = output_list.str + to_string(" ")


                    else:
                        output_list.str_pos = 15
                        output_list.str = output_list.str + to_string(substring(bal_str, i - 1, 1) , "x(1)")

                if price_decimal == 0:

                    if not long_digit:
                        output_list.str = output_list.str + "|" + to_string(balance, "   ->>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                    else:
                        output_list.str = output_list.str + "|" + to_string(balance, "->,>>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.sort_i = sort_i
                        sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(balance, "->>,>>>,>>>,>>9.99")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                printed_line = printed_line + 1
        else:
            chg_str = translateExtended ("CHANGE", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(chg_str):
                    output_list.str_pos = 16
                    output_list.str = output_list.str + to_string(" ")


                else:
                    output_list.str_pos = 16
                    output_list.str = output_list.str + to_string(substring(chg_str, i - 1, 1) , "x(1)")

            if price_decimal == 0:

                if not long_digit:
                    output_list.str = output_list.str + "|" + to_string(- balance, "   ->>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + "|" + to_string(- balance, "->,>>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
            else:
                output_list.str = output_list.str + "|" + to_string(- balance, "->>,>>>,>>>,>>9.99")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
            printed_line = printed_line + 1
        print_net_vat()
        print_in_word()

        if h_bill.bilname != "":

            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                if res_line:
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

                    if qty1000:
                        output_list.str = output_list.str + to_string("", "x(5)")
                    else:
                        output_list.str = output_list.str + to_string("", "x(5)")
                    output_list.str_pos = 17
                    output_list.str = output_list.str + to_string(translateExtended ("Room  :", lvcarea, "") + " " + res_line.zinr)
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1
                else:
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

            if res_line:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                if guest:
                    guest_addr = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
            output_list.str_pos = 18
            output_list.str = output_list.str + to_string(" ") + to_string(h_bill.bilname, "x(64)")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")
            output_list.str = output_list.str + to_string(translateExtended ("   :", lvcarea, "") + " " + to_string(time, "HH:MM:SS") , "x(20)")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")
            output_list.str = output_list.str + to_string(translateExtended ("Time  :", lvcarea, "") + " " + to_string(time, "HH:MM:SS") , "x(20)")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        multi_currency()

        if gst_logic:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(translateExtended ("     Tax Code      amount     GST", lvcarea, ""))

            if comp_taxserv:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str = output_list.str + to_string(translateExtended ("     " + to_string(mwst_str, "x(13)") +\
                        to_string(subtotal, "->>9.99 ") +\
                        to_string(0, "->>9.99") , lvcarea, ""))


            else:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                output_list.str = output_list.str + to_string(translateExtended ("     " + to_string(mwst_str, "x(13)") +\
                        to_string(subtotal, "->>9.99 ") +\
                        to_string(mwst, "->>9.99") , lvcarea, ""))


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

    def print_overhead4():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        i:int = 0

        if anz_foot > 0:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str_pos = 19
            output_list.str = output_list.str + to_string(foot1)
            output_list.pos = 6
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 3

        if foot2 != "":
            output_list.str_pos = 19
            output_list.str = output_list.str + to_string(foot2)
            output_list.pos = 6
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if buttom_lines >= 1:
            for i in range(1,buttom_lines + 1) :
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                printed_line = printed_line + 1

    def cut_it():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        printcod = db_session.query(Printcod).filter(
                (Printcod.emu == printer.emu) &  (func.lower(Printcod.code) == "cut")).first()

        if printcod:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(printcod.contcod)
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1

    def cal_totalfb():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        billdate:date = None
        fact:int = 0

        if not print_fbtotal:

            return

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).first()

        if not h_bill_line:

            return
        billdate = h_bill_line.bill_datum

        h_journal_obj_list = []
        for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) &  (H_artikel.departement == H_journal.departement) &  (H_artikel.artart == 0)).filter(
                (H_journal.bill_datum == billdate) &  (H_journal.departement == h_bill.departement) &  (H_journal.rechnr == h_bill.rechnr)).all():
            if h_journal._recid in h_journal_obj_list:
                continue
            else:
                h_journal_obj_list.append(h_journal._recid)


            fact = 1

            if h_artikel.artnr == disc_art1:
                total_fdisc = total_fdisc + fact * h_journal.epreis

            elif h_artikel.artnr == disc_art2:
                total_bdisc = total_bdisc + fact * h_journal.epreis

            elif h_artikel.artnr == disc_art3:
                total_odisc = total_odisc + fact * h_journal.epreis
            else:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    total_food = total_food + fact * h_journal.anzahl * h_journal.epreis

                elif artikel.umsatzart == 6:
                    total_bev = total_bev + fact * h_journal.anzahl * h_journal.epreis

                elif artikel.umsatzart == 4:
                    total_other = total_other + fact * h_journal.anzahl * h_journal.epreis

    def print_totalfb():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        pos:int = 0
        s:str = ""
        i:int = 0
        nbez1:int = 0

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.artnr == f_discart) &  (substring(H_bill_line.bezeich, len(H_bill_line.bezeich) - 1) == "*")).first()

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
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_food != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("FOOD", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_food, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_bev != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("BEVERAGE", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_bev, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_other != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("OTHER", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_other, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_fdisc != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("DISC FOOD", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_fdisc, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_bdisc != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("DISC BEVERAGE", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_bdisc, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

        if total_odisc != 0:
            for i in range(1,pos + 1) :
                output_list.str = output_list.str + to_string(" ")
            s = translateExtended ("DISC OTHER", lvcarea, "")
            for i in range(1,nbez1 + 1) :

                if i > len(s):
                    output_list.str = output_list.str + to_string(" ")
                else:
                    output_list.str = output_list.str + to_string(substring(s, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string(total_odisc, "->>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1
        printed_line = printed_line + 1

    def multi_currency():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        i:int = 0
        n:int = 0
        mesval:str = ""
        s:str = ""
        exchg_rate:decimal = 0
        foreign_amt:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 830)).first()

        if htparam.feldtyp != 5 or htparam.fchar == "":

            return
        for i in range(1,num_entries(htparam.fchar, ";")  + 1) :
            mesval = trim(entry(i - 1, htparam.fchar, ";"))

            waehrung = db_session.query(Waehrung).filter(
                    (func.lower(Waehrung.wabkurz) == (mesval).lower())).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit
                foreign_amt = round(tot_amount / exchg_rate, 2)
                s = waehrung.wabkurz + " " + translateExtended ("TOTAL", lvcarea, "")

                if qty1000:
                    output_list.str = output_list.str + to_string("", "x(6)")
                else:
                    output_list.str = output_list.str + to_string("", "x(5)")
                for n in range(1,(nbezeich - 2)  + 1) :

                    if n > len(s):
                        output_list.str = output_list.str + to_string(" ")
                    else:
                        output_list.str = output_list.str + to_string(substring(s, n - 1, 1) , "x(1)")
                output_list.str = output_list.str + to_string(foreign_amt, "->,>>>,>>9.99")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.sort_i = sort_i
                sort_i = sort_i + 1
                curr_j = curr_j + 1
                printed_line = printed_line + 1

    def print_net_vat():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        lpage1:int = 0
        net_amt:decimal = 0
        vat_str:str = ""
        vat_proz:decimal = 0
        vat_num:int = 0

        if comp_taxserv or rm_transfer:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 376)).first()

        if not htparam.flogical:

            return
        vat_list_list.clear()

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart == 0) &  (H_artikel.mwst_code != 0)).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == h_artikel.mwst_code)).first()

            if htparam.fdecimal != 0:

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vat_amt == htparam.fdecimal), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_list.append(vat_list)

                    vat_list.vat_amt = htparam.fdecimal


                vat_list.betrag_amt = vat_list.betrag_amt + h_bill_line.betrag

        vat_list = query(vat_list_list, first=True)

        if vat_list:
            net_amt = 0

            for vat_list in query(vat_list_list):
                vat_num = vat_num + 1
                vat_proz = vat_list.vat_amt
                net_amt = net_amt + vat_list.betrag_amt / (1 + vat_list.vat_amt / 100)
                vat_list_list.remove(vat_list)
            net_amt = round(net_amt, price_decimal)
            mwst1 = tot_sales - net_amt


        else:
            net_amt = tot_amount - mwst1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 872)).first()

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
            output_list_list.append(output_list)

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
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(translateExtended ("NET", lvcarea, ""))
            output_list.pos = 7
            output_list.str = output_list.str + to_string(" ")
        else:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            output_list.str = output_list.str + to_string(translateExtended ("NET", lvcarea, ""))
            output_list.pos = 6
            output_list.str = output_list.str + to_string(" ")

        if not long_digit:
            output_list.str = output_list.str + to_string(net_amt, "->>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + to_string(net_amt, "->,>>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.str = output_list.str + to_string(mwst1, "->>,>>>,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        else:
            output_list.str = output_list.str + to_string(mwst1, "->,>>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        printed_line = printed_line + 2

    def print_in_word():

        nonlocal filename, msg_str, winprinterflag, output_list_list, t_printer_list, lvcarea, disc_bezeich, amount, sort_i, order_id, disc_zwkum, print_balance, disc_art1, disc_art2, disc_art3, incl_service, incl_mwst, service_taxable, print_fbtotal, prdisc_flag, mwst_str, service_str, hmargin, bmargin, lpage, nbezeich, nwidth, npause, bill_date110, bill_date, price_decimal, n11, long_digit, prtwoline, printed_line, last_amount, zeit, comp_flag, service, mwst, tot_amount, comp_taxserv, tot_sales, new_item, printed, qty, do_it, rm_transfer, new_fbart, tot_line, h_service, h_mwst, serv_perc, mwst_perc, fact, mwst1, subtotal, bline_exist, qty1000, i, n, curr_j, npage, tot_ndisc_line, tot_disc_line, buttom_lines, prtabledesc, header1, header2, foot1, foot2, anz_foot, overhead1, overhead2, overhead3, overhead4, total_food, total_bev, total_other, total_fdisc, total_bdisc, total_odisc, gst_logic, serv_disc, vat_disc, f_discart, guest_addr, serv_code, vat_code, servtax_use_foart, printer, artikel, htparam, h_bill, hoteldpt, queasy, h_queasy, kellner, h_bill_line, h_artikel, kontplan, paramtext, bediener, tisch, res_line, mc_guest, h_mjourn, guest, printcod, h_journal, waehrung
        nonlocal artbuff, abuff, hbuff, h_art


        nonlocal art_list, t_printer, vat_list, output_list, artbuff, abuff, hbuff, h_art
        nonlocal art_list_list, t_printer_list, vat_list_list, output_list_list

        lpage1:int = 0
        progname:str = ""
        str1:str = ""
        str2:str = ""
        w_length:int = 0
        i:int = 0

        if comp_taxserv:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 825)).first()

        if htparam.flogical == False:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 829)).first()

        if htparam.fchar == "":

            return

        if anz_foot == 0:
            lpage1 = lpage - 3
        else:
            lpage1 = lpage - 7

        if curr_j > lpage1:
            output_list = Output_list()
            output_list_list.append(output_list)

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
        str1, str2 = value(progname) (tot_amount, w_length)
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1

        if qty1000:
            output_list.str = output_list.str + to_string("", "x(6)")
        else:
            output_list.str = output_list.str + to_string("", "x(5)")
        for i in range(1,len(str1)  + 1) :
            output_list.str = output_list.str + to_string(substring(str1, i - 1, 1) , "x(1)")
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1
        printed_line = printed_line + 2

        if trim(str2) != "":

            if qty1000:
                output_list.str = output_list.str + to_string("", "x(6)")
            else:
                output_list.str = output_list.str + to_string("", "x(5)")
            for i in range(1,len(str2)  + 1) :
                output_list.str = output_list.str + to_string(substring(str2, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.sort_i = sort_i
            sort_i = sort_i + 1
            printed_line = printed_line + 1

    mwst_str = translateExtended ("Government Tax", lvcarea, "")
    service_str = translateExtended ("service Charge", lvcarea, "")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 468)).first()

    if htparam:
        serv_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 469)).first()

    if htparam:
        vat_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()

    if htparam.finteger != 0:
        f_discart = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 376)).first()

    if htparam:

        if not htparam.flogic and entry(0, htparam.fchar, ";") == "GST(MA)":
            gst_logic = True

    if printnr > 0:

        printer = db_session.query(Printer).filter(
                (Printer.nr == printnr)).first()

        if not printer:
            msg_str = translateExtended ("No such Printer Number:", lvcarea, "") + " " + to_string(printnr)

            return generate_output()
        t_printer = T_printer()
        t_printer_list.append(t_printer)

        buffer_copy(printer, t_printer)
    order_id, prdisc_flag, disc_art1, disc_art2, disc_art3, disc_zwkum, print_balance, incl_service, incl_mwst, service_taxable, print_fbtotal = get_output(prepare_print_hbill1bl(hbrecid))

    if printnr != 0:

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == hbrecid)).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 132)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if artikel:

            artbuff = db_session.query(Artbuff).filter(
                    (artBuff.artnr == artikel.artnr) &  (artBuff.departement == h_bill.departement)).first()

            if artBuff and artBuff.endkum == artikel.endkum:
                mwst_str = artBuff.bezeich
            else:
                mwst_str = artikel.bezeich

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 133)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if artikel:
            service_str = artikel.bezeich

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 850)).first()
        hmargin = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 858)).first()

        if htparam.finteger != 0:
            bmargin = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 851)).first()
        lpage = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 871)).first()
        nbezeich = 25

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 831)).first()
        nwidth = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 890)).first()
        npause = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date110 = htparam.fdate
        bill_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 253)).first()

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger

        if price_decimal == 0:
            n11 = 12

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 246)).first()
        long_digit = htparam.flogical

        if long_digit:
            n11 = 14

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 874)).first()

        if htparam.feldtyp == 4 and htparam.flogical:
            print_all = True

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == h_bill.departement)).first()

        if hoteldpt:
            servtax_use_foart = hoteldpt.defult
        optional_params()

        if prtwoline:
            n11 = 1

        if not use_h_queasy:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 == 0) &  (Queasy.deci2 == billnr)).first()

            if queasy and not print_all:
                printed_line = queasy.number3
                last_amount = queasy.deci1

                if printed_line == lpage:
                    printed_line = 0

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 4
                queasy.number1 = (h_bill.departement + h_bill.rechnr * 100)
                queasy.number2 = 0
                queasy.deci2 = billnr


        else:

            h_queasy = db_session.query(H_queasy).filter(
                    (H_queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (H_queasy.number2 == 0) &  (H_queasy.billno == billnr)).first()

            if h_queasy and not print_all:
                printed_line = h_queasy.number3
                last_amount = h_queasy.deci1

                if printed_line == lpage:
                    printed_line = 0

            if not h_queasy:
                h_queasy = H_queasy()
                db_session.add(h_queasy)

                h_queasy.number1 = (h_bill.departement + h_bill.rechnr * 100)
                h_queasy.number2 = 0
                h_queasy.billno = billnr

        kellner = db_session.query(Kellner).filter(
                (Kellner.departement == h_bill.departement) &  (Kellner_nr == h_bill.kellner_nr)).first()

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == h_bill.departement)).first()
        zeit = get_current_time_in_seconds()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 824)).first()
        comp_flag = htparam.flogical
        service = 0
        mwst = 0
        tot_amount = last_amount

        if h_bill.flag == 1:

            h_bill_line = db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).first()

            if h_bill_line:
                bill_date = h_bill_line.bill_datum

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).all():

            if h_bill_line.artnr != 0:

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

                if (h_artikel.artart == 11 or h_artikel.artart == 12):
                    comp_taxserv = not comp_taxserv

                elif h_artikel.artart == 0:
                    tot_sales = tot_sales + h_bill_line.betrag
            new_item = False
            printed = True

            if not use_h_queasy:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 == to_int(h_bill_line._recid)) &  (Queasy.deci2 == billnr)).first()

                if not queasy:
                    new_item = True

                    if printnr >= 0:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 4
                        queasy.number1 = (h_bill.departement + h_bill.rechnr * 100)
                        queasy.number2 = to_int(h_bill_line._recid)
                        queasy.deci2 = billnr


            else:

                h_queasy = db_session.query(H_queasy).filter(
                        (H_queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (H_queasy.number2 == to_int(h_bill_line._recid)) &  (H_queasy.billno == billnr)).first()

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

            do_it = None != h_artikel and h_artikel.artart == 0 and h_artikel.zwkum != disc_zwkum

            if do_it:

                art_list = query(art_list_list, filters=(lambda art_list :art_list.artnr == h_bill_line.artnr and art_list.dept == h_bill_line.departement and art_list.bezeich == h_bill_line.bezeich and art_list.price == h_bill_line.epreis and art_list.condiment == 0 and not art_list.printed), first=True)

            if h_bill_line.artnr == 0:
                rm_transfer = not rm_transfer

            if h_bill_line.artnr != 0:

                if h_artikel.artart == 0 and (new_item or print_all):
                    new_fbart = True

            if not art_list or h_bill_line.betriebsnr == 1:
                art_list = Art_list()
                art_list_list.append(art_list)

                art_list.printed = printed
                art_list.artnr = h_bill_line.artnr
                art_list.dept = h_bill_line.departemen
                art_list.bezeich = h_bill_line.bezeich
                art_list.price = h_bill_line.epreis
                art_list.datum = h_bill_line.bill_datum
                art_list.sysdate = h_bill_line.sysdate
                art_list.zeit = h_bill_line.zeit

                if h_bill_line.artnr != 0:
                    art_list.artart = h_artikel.artart
                    art_list.zwkum = h_artikel.zwkum


                else:
                    art_list.artart = 2

                if h_artikel and h_artikel.artart == 0 and h_artikel.epreis2 != 0 and art_list.price == h_artikel.epreis2:
                    art_list.happyhr = "*"

                if h_artikel and h_artikel.artart == 0:
                    art_list.condiment = h_bill_line.betriebsnr
                art_list.disc_flag = prdisc_flag and (art_list.zwkum == disc_zwkum)
                tot_line = tot_line + 1
            art_list.betrag = art_list.betrag + h_bill_line.betrag
            h_service = 0
            h_mwst = 0


            amount = h_bill_line.betrag

            if art_list.artart == 0:
                serv%, mwst%, fact = cal_servat(h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_bill_line.bill_datum)

                if h_bill_line.artnr == f_discart:

                    if h_bill_line.epreis != h_bill_line.betrag:

                        if not serv_disc and h_bill_line.artnr == f_discart:
                            pass
                        else:
                            h_service = h_bill_line.betrag / fact * serv%
                            h_service = round(h_service, 2)

                        if not vat_disc and h_bill_line.artnr == f_discart:
                            pass
                        else:
                            h_mwst = h_bill_line.betrag / fact * mwst%
                            h_mwst = round(h_mwst, 2)

                        if not incl_service:
                            amount = amount - h_service
                            service = service + h_service

                        if not incl_mwst:
                            amount = amount - h_mwst
                            mwst = mwst + h_mwst
                            mwst1 = mwst1 + h_mwst


                else:

                    if not serv_disc and h_bill_line.artnr == f_discart:
                        pass
                    else:
                        h_service = h_bill_line.betrag / fact * serv%
                        h_service = round(h_service, 2)

                    if not vat_disc and h_bill_line.artnr == f_discart:
                        pass
                    else:
                        h_mwst = h_bill_line.betrag / fact * mwst%
                        h_mwst = round(h_mwst, 2)

                    if not incl_service:
                        amount = amount - h_service
                        service = service + h_service

                    if not incl_mwst:
                        amount = amount - h_mwst
                        mwst = mwst + h_mwst
                        mwst1 = mwst1 + h_mwst

                if not art_list.disc_Flag:
                    subtotal = subtotal + amount
            art_list.amount = art_list.amount + amount

            if h_bill_line.artnr != 0:
                art_list.qty = art_list.qty + qty

        for art_list in query(art_list_list):

            if art_list.qty == 0 and round(art_list.amount, 0) == 0:
                art_list_list.remove(art_list)
                tot_line = tot_line - 1
                bline_exist = True

            elif art_list.qty > 999 or art_list.qty < -999:
                qty1000 = True

        for abuff in query(abuff_list, filters=(lambda abuff :(abuff.zwkum == disc_zwkum) and re.match(".*-.*",abuff.bezeich))):
            disc_bezeich = replace_str(abuff.bezeich, "-", "")

            art_list = query(art_list_list, filters=(lambda art_list :art_list.artnr == abuff.artnr and art_list.bezeich.lower()  == (disc_bezeich).lower()  and art_list.amount == - abuff.amount), first=True)

            if art_list:
                art_list_list.remove(art_list)
                abuff_list.remove(abuff)
                tot_line = tot_line - 2

        for abuff in query(abuff_list, filters=(lambda abuff :abuff.disc_flag)):
            disc_bezeich = abuff.bezeich

            art_list = query(art_list_list, filters=(lambda art_list :art_list.artnr == abuff.artnr and art_list.bezeich.lower()  == (disc_bezeich).lower()  and art_list.amount == - abuff.amount), first=True)

            if art_list:
                art_list_list.remove(art_list)
                abuff_list.remove(abuff)
                tot_line = tot_line - 2
        add_unitprice_text()

        art_list = query(art_list_list, filters=(lambda art_list :art_list.printed == False), first=True)

        if not art_list and printnr >= 0 and not bline_exist:
            msg_str = msg_str + chr(2) + translateExtended ("No new bill_lines was found.", lvcarea, "")

            return generate_output()
        check_pages()

        if printnr > 0:
            pass

        elif printnr < 0:
            filename = "billdir\\" + to_string(h_bill.tischnr) + "__" + to_string(h_bill.departement, "99")
        for i in range(1,printed_line + 1) :
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = output_list.str + to_string("")
            output_list.sort_i = sort_i
            sort_i = sort_i + 1
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.sort_i = sort_i
        sort_i = sort_i + 1

        if prdisc_flag and tot_ndisc_line >= 1 and tot_disc_line >= 1:

            art_list = query(art_list_list, filters=(lambda art_list :art_list.artart == 0 and not art_list.disc_flag and not art_list.printed), first=True)
            n = 0
            curr_j = printed_line
            for i in range(1,npage + 1) :

                if not art_list:
                    i = npage
                print_overhead1()
                while None != art_list and (curr_j <= lpage) :
                    print_billine()

                    art_list = query(art_list_list, filters=(lambda art_list :art_list.artart == 0 and not art_list.disc_flag and not art_list.printed), next=True)

                    if not art_list:
                        i = npage

                if i == npage:
                    print_overhead2(0)

                    for art_list in query(art_list_list, filters=(lambda art_list :art_list.artart == 0 and art_list.disc_flag)):
                        subtotal = subtotal + art_list.amount
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
                    output_list_list.append(output_list)

                    output_list.flag_popup = True
                    output_list.npause = npause
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1


                    curr_j = 0
                    printed_line = 0
        else:

            art_list = query(art_list_list, filters=(lambda art_list :art_list.artart == 0 and not art_list.printed), first=True)
            n = 0
            curr_j = printed_line
            for i in range(1,npage + 1) :

                if not art_list:
                    i = npage
                print_overhead1()
                while None != art_list and (curr_j <= lpage) :
                    print_billine()

                    art_list = query(art_list_list, filters=(lambda art_list :art_list.artart == 0 and not art_list.printed), next=True)

                    if not art_list:
                        i = npage

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
                    output_list_list.append(output_list)

                    output_list.flag_popup = True
                    output_list.npause = npause
                    output_list.sort_i = sort_i
                    sort_i = sort_i + 1


                    curr_j = 0
                    printed_line = 0
        tot_amount = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).all():
            tot_amount = tot_amount + h_bill_line.betrag

        if printnr >= 0:

            if not use_h_queasy:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 == 0) &  (Queasy.deci2 == billnr)).first()
                queasy.number3 = printed_line
                queasy.deci1 = tot_amount

                queasy = db_session.query(Queasy).first()
            else:

                h_queasy = db_session.query(H_queasy).filter(
                        (H_queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (H_queasy.number2 == 0) &  (H_queasy.billno == billnr)).first()

                if h_queasy:
                    h_queasy.number3 = printed_line
                    h_queasy.deci1 = tot_amount

                    h_queasy = db_session.query(H_queasy).first()

    return generate_output()