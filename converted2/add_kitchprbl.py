#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 13/8/2025
# num-entries
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Queasy, H_bill_line, H_artikel, Htparam, Hoteldpt, H_bill, Wgrpdep, Printer, Bediener, Kellner, H_journal, H_mjourn, Printcod

def add_kitchprbl(pvilanguage:int, session_parameter:string, dept:int, rechnr:int, billdate:date, user_init:string):

    prepare_cache ([Queasy, H_bill_line, H_artikel, Htparam, Hoteldpt, H_bill, Wgrpdep, Printer, Bediener, Kellner, H_journal, H_mjourn, Printcod])

    error_str = ""
    lvcarea:string = "add-kitchpr"
    kitchen_pr:List[int] = create_empty_list(10,0)
    numcat1:int = 0
    numcat2:int = 0
    k:int = 0
    prev_zknr:int = 0
    add_zeit:int = 0
    always_do:bool = True
    bline_created:bool = False
    print_subgrp:bool = True
    print_single:bool = False
    desclength:int = 0
    sort_subgrp:bool = False
    recid_h_bill_line:int = 0
    sort_subgrp_prior:bool = False
    room:string = ""
    gname:string = ""
    room_str:string = ""
    printer_loc:string = ""
    create_queasy:bool = False
    count_k:int = 0
    queasy = h_bill_line = h_artikel = htparam = hoteldpt = h_bill = wgrpdep = printer = bediener = kellner = h_journal = h_mjourn = printcod = None

    t_queasy = submenu_list = hbline = buf_h_artikel = qsy = qbuff = None

    t_queasy_data, T_queasy = create_model_like(Queasy)
    submenu_list_data, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})

    Hbline = create_buffer("Hbline",H_bill_line)
    Buf_h_artikel = create_buffer("Buf_h_artikel",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        return {"error_str": error_str}

    def create_bon_output():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        tableno:int = 0
        Qsy = T_queasy
        qsy_data = t_queasy_data

        printer = get_cache (Printer, {"nr": [(eq, buf_h_artikel.bondruckernr[0])]})

        if not printer:
            error_str = error_str + translateExtended ("The kitchen vhp.printer number", lvcarea, "") + " " + to_string(buf_h_artikel.bondrucker[0]) + chr_unicode(10) + translateExtended ("in Article", lvcarea, "") + " " + to_string(buf_h_artikel.artnr) + " - " + buf_h_artikel.bezeich + chr_unicode(10) + translateExtended ("not defined in the vhp.printer Administration!", lvcarea, "") + chr_unicode(10)
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            t_queasy.key = 3


        else:
            get_printer_number()

            queasy = get_cache (Queasy, {"key": [(eq, 208)],"number1": [(eq, buf_h_artikel.endkum)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 208
                queasy.number1 = buf_h_artikel.endkum
                queasy.number2 = 1


            else:
                pass
                queasy.number2 = queasy.number2 + 1


                pass
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            t_queasy.key = 3
            t_queasy.number1 = printer.nr
            t_queasy.number3 = printer.nr
            t_queasy.deci1 =  to_decimal(queasy.number2)


        tableno = h_bill_line.tischnr
        t_queasy.number2 = get_current_time_in_seconds() + add_zeit
        t_queasy.logi1 = False
        t_queasy.date1 = billdate
        t_queasy.date2 = get_current_date()
        t_queasy.char2 = printer_loc
        t_queasy.logi2 = True


        t_queasy.char3 = hoteldpt.depart + chr_unicode(10) + translateExtended ("BillNo", lvcarea, "") + " " + to_string(h_bill.rechnr) + chr_unicode(10) + translateExtended (room_str, lvcarea, "") + " " + to_string(room) + " " + to_string(gname) + chr_unicode(10) + translateExtended ("Table", lvcarea, "") + " " + to_string(tableno) + " " + translateExtended ("Pax", lvcarea, "") + " " + to_string(h_bill.belegung) + chr_unicode(10) + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM") + chr_unicode(10)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            t_queasy.char3 = t_queasy.char3 + translateExtended ("Posted by:", lvcarea, "") + " " + bediener.username + chr_unicode(10)
        else:

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

            if kellner:
                t_queasy.char3 = t_queasy.char3 + translateExtended ("Waiter:", lvcarea, "") + " " + kellner.kellnername + chr_unicode(10)

        qsy = query(qsy_data, filters=(lambda qsy: qsy.key == 10 and qsy.number1 == h_bill.betriebsnr), first=True)

        if qsy:
            t_queasy.char3 = t_queasy.char3 + translateExtended ("Order Taker:", lvcarea, "") + " " + qsy.char1 + chr_unicode(10)
        t_queasy.char3 = t_queasy.char3 + chr_unicode(10)


    def write_article():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        curr_recid:int = 0
        created:bool = False
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        Qbuff = T_queasy
        qbuff_data = t_queasy_data

        h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_bill_line.bill_datum)],"sysdate": [(eq, h_bill_line.sysdate)],"zeit": [(eq, h_bill_line.zeit)],"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)],"schankbuch": [(eq, recid_h_bill_line)]})

        if print_subgrp and print_single:
            prev_zknr = wgrpdep.zknr
            t_queasy.char3 = t_queasy.char3 + "[" + to_string(wgrpdep.bezeich) + "]" + chr_unicode(10)

        elif (print_subgrp or sort_subgrp_prior) and not print_single and (prev_zknr != wgrpdep.zknr):
            prev_zknr = wgrpdep.zknr
            t_queasy.char3 = t_queasy.char3 + "[" + to_string(wgrpdep.bezeich) + "]" + chr_unicode(10)

        if desclength == 0 or length(h_bill_line.bezeich) <= desclength:
            t_queasy.char3 = t_queasy.char3 + to_string(h_bill_line.anzahl, "->>9 ") + to_string(h_bill_line.bezeich) + chr_unicode(10)
        else:
            write_descript(to_string(h_bill_line.anzahl, "->>9 "), to_string(h_bill_line.bezeich))

        qbuff = query(qbuff_data, filters=(lambda qbuff: qbuff.key == 38 and qbuff.number1 == h_bill_line.departement and qbuff.number2 == h_bill_line.artnr), first=True)

        if qbuff:

            if desclength == 0 or length(t_queasy.char3) <= desclength:
                t_queasy.char3 = t_queasy.char3 + to_string("", "x(5)") + to_string(qbuff.char3) + chr_unicode(10)
            else:
                write_descript(to_string("", "x(5)"), to_string(qbuff.char3))

        if h_bill_line.anzahl != 0:

            if h_journal and h_journal.aendertext != "":
                t_queasy.char3 = t_queasy.char3 + " ::: " + h_journal.aendertext + chr_unicode(10)

            if h_journal and h_journal.stornogrund != "":
                t_queasy.char3 = t_queasy.char3 + " >>> " + to_string(h_journal.stornogrund, "x(20)") + chr_unicode(10)

        if buf_h_artikel.betriebsnr > 0:

            for submenu_list in query(submenu_list_data, filters=(lambda submenu_list: submenu_list.nr == buf_h_artikel.betriebsnr and submenu_list.zeit == h_bill_line.zeit)):
                created = True
                t_queasy.char3 = t_queasy.char3 + " -> " + to_string(submenu_list.bezeich) + chr_unicode(10)

                if submenu_list.request != "":
                    t_queasy.char3 = t_queasy.char3 + ":::" + submenu_list.request + chr_unicode(10)
                submenu_list_data.remove(submenu_list)

            if not created:

                h_journal = get_cache (H_journal, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, dept)],"rechnr": [(eq, rechnr)],"bill_datum": [(eq, h_bill_line.bill_datum)],"zeit": [(eq, h_bill_line.zeit)],"sysdate": [(eq, h_bill_line.sysdate)],"schankbuch": [(eq, recid_h_bill_line)]})

                if h_journal:
                    # Rd 13/8/2025
                    # for h_mjourn in db_session.query(H_mjourn).filter(
                    #          (H_mjourn.departement == dept) & (H_mjourn.h_artnr == h_journal.artnr) & (H_mjourn.rechnr == h_journal.rechnr) & (H_mjourn.bill_datum == h_journal.bill_datum) & (H_mjourn.sysdate == h_journal.sysdate) & (H_mjourn.zeit == h_journal.zeit) & (num_entries(H_mjourn.request, "|") > 1) & (to_int(entry(0, H_mjourn.request, "|")) == recid_h_bill_line)).order_by(H_mjourn._recid).all():
                    for h_mjourn in db_session.query(H_mjourn).filter(
                             (H_mjourn.departement == dept) & (H_mjourn.h_artnr == h_journal.artnr) & 
                             (H_mjourn.rechnr == h_journal.rechnr) & (H_mjourn.bill_datum == h_journal.bill_datum) & 
                             (H_mjourn.sysdate == h_journal.sysdate) & (H_mjourn.zeit == h_journal.zeit) & 
                             (to_int(entry(0, H_mjourn.request, "|")) == recid_h_bill_line)).order_by(H_mjourn._recid).all():
                        if  (num_entries(H_mjourn.request, "|") > 1):
                            h_art = get_cache (H_artikel, {"artnr": [(eq, h_mjourn.artnr)],"departement": [(eq, dept)]})

                            if h_art:
                                created = True
                                t_queasy.char3 = t_queasy.char3 + " -> " + to_string(h_art.bezeich) + chr_unicode(10)

                                if h_mjourn.request != "":
                                    t_queasy.char3 = t_queasy.char3 + ":::" + h_mjourn.request + chr_unicode(10)


        if created:
            t_queasy.char3 = t_queasy.char3 + " " + chr_unicode(10)


    def write_descript(str1:string, str2:string):

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        s1:string = ""
        s2:string = ""
        word:string = ""
        next_line:bool = False
        i:int = 0
        length1:int = 0
        t_queasy.char3 = t_queasy.char3 + str1

        if num_entries(str2, " ") == 1:

            if round(desclength / 2, 0) * 2 != desclength:
                length1 = desclength - 1
            else:
                length1 = desclength
            t_queasy.char3 = t_queasy.char3 + substring(str2, 0, length1) + chr_unicode(10)
            for i in range(1,length(str1)  + 1) :
                t_queasy.char3 = t_queasy.char3 + " "
            t_queasy.char3 = t_queasy.char3 + substring(str2, length1 + 1 - 1) + chr_unicode(10)

            return
        next_line = False
        for i in range(1,num_entries(str2, " ")  + 1) :
            word = entry(i - 1, str2, " ")

            if next_line:
                s2 = s2 + word + " "
            else:

                if length(s1 + word) <= desclength:
                    s1 = s1 + word + " "
                else:
                    next_line = True
                    s2 = s2 + word + " "
        t_queasy.char3 = t_queasy.char3 + s1 + chr_unicode(10)
        for i in range(1,length(str1)  + 1) :
            t_queasy.char3 = t_queasy.char3 + " "
        t_queasy.char3 = t_queasy.char3 + s2 + chr_unicode(10)


    def cut_it():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        i:int = 0

        if numcat1 == 0:
            t_queasy.char3 = t_queasy.char3 + " " + chr_unicode(10) + chr_unicode(10) + " " + chr_unicode(10) + " " + chr_unicode(10)
        else:
            for i in range(1,numcat1 + 1) :
                t_queasy.char3 = t_queasy.char3 + " " + chr_unicode(10)

        printcod = get_cache (Printcod, {"emu": [(eq, printer.emu)],"code": [(eq, "cut")]})

        if printcod:
            t_queasy.char3 = t_queasy.char3 + printcod.contcode + chr_unicode(10)
        else:

            if numcat2 == 0:
                t_queasy.char3 = t_queasy.char3 + " " + chr_unicode(10) + " " + chr_unicode(10) + " " + chr_unicode(10) + " " + chr_unicode(10) + " " + chr_unicode(10)
            else:
                for i in range(1,numcat2 + 1) :
                    t_queasy.char3 = t_queasy.char3 + " " + chr_unicode(10)


    def readsession():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        lvctmp:string = ""
        lvcleft:string = ""
        lvcval:string = ""
        lvicnt:int = 0
        lvi:int = 0
        lvitmp:int = 0
        i:int = 0
        lvicnt = num_entries(session_parameter, ";")
        for lvi in range(1,lvicnt + 1) :
            lvctmp = ""
            lvcleft = ""


            lvctmp = trim(entry(lvi - 1, session_parameter, ";"))
            lvcleft = trim(entry(0, lvctmp, "="))

            if lvcleft == "kpr1":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[0] = to_int(lvcval)
            elif lvcleft == "kpr2":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[1] = to_int(lvcval)
            elif lvcleft == "kpr3":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[2] = to_int(lvcval)
            elif lvcleft == "kpr4":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[3] = to_int(lvcval)
            elif lvcleft == "kpr5":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[4] = to_int(lvcval)
            elif lvcleft == "kpr6":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[5] = to_int(lvcval)
            elif lvcleft == "kpr7":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[6] = to_int(lvcval)
            elif lvcleft == "kpr8":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[7] = to_int(lvcval)
            elif lvcleft == "kpr9":
                lvcval = trim(entry(1, lvctmp, "="))
                kitchen_pr[8] = to_int(lvcval)
            elif lvcleft == "DesLen":
                lvcval = trim(entry(1, lvctmp, "="))
                desclength = to_int(lvcval)
            elif lvcleft == "PrSubgrp":

                if trim(entry(1, lvctmp, "=")) == ("NO").lower() :
                    print_subgrp = False
            elif lvcleft == "PrSingle":

                if trim(entry(1, lvctmp, "=")) == ("YEs").lower() :
                    print_single = True
            elif lvcleft == "printer-loc":
                lvcval = trim(entry(1, lvctmp, "="))
                printer_loc = lvcval
        for i in range(1,9 + 1) :

            if kitchen_pr[i - 1] != 0:

                printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[i - 1])]})

                if not printer:
                    error_str = error_str + translateExtended ("Kitchen Printer Number", lvcarea, "") + " " + to_string(kitchen_pr[i - 1]) + " " + translateExtended ("not found (wrong parameter startup).", lvcarea, "") + chr_unicode(10)

                    return
        kitchen_pr[9] = 1


    def get_printer_number():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, h_artikel, htparam, hoteldpt, h_bill, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline, buf_h_artikel


        nonlocal t_queasy, submenu_list, hbline, buf_h_artikel, qsy, qbuff
        nonlocal t_queasy_data, submenu_list_data

        if printer.path == "KPR1":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[0])]})

            return
        elif printer.path == "KPR2":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[1])]})

            return
        elif printer.path == "KPR3":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[2])]})

            return
        elif printer.path == "KPR4":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[3])]})

            return
        elif printer.path == "KPR5":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[4])]})

            return
        elif printer.path == "KPR6":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[5])]})

            return
        elif printer.path == "KPR7":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[6])]})

            return
        elif printer.path == "KPR8":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[7])]})

            return
        elif printer.path == "KPR9":

            printer = get_cache (Printer, {"nr": [(eq, kitchen_pr[8])]})

            return

    htparam = get_cache (Htparam, {"paramnr": [(eq, 252)]})
    numcat1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 562)]})
    numcat2 = htparam.finteger
    billdate = get_output(htpdate(110))

    if get_current_date() > billdate:
        billdate = get_current_date()
    readsession()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 450)]})

    if htparam:
        print_subgrp = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 147)]})

    if htparam:
        sort_subgrp = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 838)]})

    if htparam:
        sort_subgrp_prior = htparam.flogical

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"rechnr": [(eq, rechnr)]})

    if sort_subgrp :

        h_bill_line_obj_list = {}
        h_bill_line = H_bill_line()
        buf_h_artikel = H_artikel()
        wgrpdep = Wgrpdep()
        for h_bill_line.tischnr, h_bill_line.bill_datum, h_bill_line.sysdate, h_bill_line.zeit, h_bill_line.artnr, h_bill_line.departement, h_bill_line.bezeich, h_bill_line.anzahl, h_bill_line._recid, h_bill_line.steuercode, buf_h_artikel.bondruckernr, buf_h_artikel.artnr, buf_h_artikel.bezeich, buf_h_artikel.endkum, buf_h_artikel.betriebsnr, buf_h_artikel._recid, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep._recid in db_session.query(H_bill_line.tischnr, H_bill_line.bill_datum, H_bill_line.sysdate, H_bill_line.zeit, H_bill_line.artnr, H_bill_line.departement, H_bill_line.bezeich, H_bill_line.anzahl, H_bill_line._recid, H_bill_line.steuercode, Buf_h_artikel.bondruckernr, Buf_h_artikel.artnr, Buf_h_artikel.bezeich, Buf_h_artikel.endkum, Buf_h_artikel.betriebsnr, Buf_h_artikel._recid, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep._recid).join(Buf_h_artikel,(Buf_h_artikel.artnr == H_bill_line.artnr) & (Buf_h_artikel.departement == dept) & (Buf_h_artikel.artart == 0)).join(Wgrpdep,(Wgrpdep.departement == dept) & (Wgrpdep.zknr == Buf_h_artikel.zwkum)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept) & (H_bill_line.steuercode <= 0)).order_by(Buf_h_artikel.bondruckernr[inc_value(0)], Buf_h_artikel.zwkum, H_bill_line.sysdate, H_bill_line.zeit, H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            add_zeit = add_zeit + 1
            recid_h_bill_line = h_bill_line._recid

            htparam = get_cache (Htparam, {"paramnr": [(eq, 865)]})

            if htparam.flogical and buf_h_artikel.bondruckernr[0] > 0:

                if not print_single:

                    if (k != buf_h_artikel.bondruckernr[0]):

                        if k > 0:
                            cut_it()
                        create_bon_output()
                        k = buf_h_artikel.bondruckernr[0]
                    write_article()
                else:
                    create_bon_output()
                    k = buf_h_artikel.bondruckernr[0]
                    write_article()
                    cut_it()

            hbline = get_cache (H_bill_line, {"_recid": [(eq, h_bill_line._recid)]})

            if buf_h_artikel.bondruckernr[0] != 0:

                if hbline.steuercode == 0:
                    hbline.steuercode = buf_h_artikel.bondruckernr[0]
                else:
                    hbline.steuercode = 9999
            else:

                if hbline.steuercode == 0:
                    h_bill_line.steuercode = 1
                else:
                    hbline.steuercode = 9999
            pass
            pass
            bline_created = True

    elif sort_subgrp_prior :

        h_bill_line_obj_list = {}
        h_bill_line = H_bill_line()
        buf_h_artikel = H_artikel()
        wgrpdep = Wgrpdep()
        for h_bill_line.tischnr, h_bill_line.bill_datum, h_bill_line.sysdate, h_bill_line.zeit, h_bill_line.artnr, h_bill_line.departement, h_bill_line.bezeich, h_bill_line.anzahl, h_bill_line._recid, h_bill_line.steuercode, buf_h_artikel.bondruckernr, buf_h_artikel.artnr, buf_h_artikel.bezeich, buf_h_artikel.endkum, buf_h_artikel.betriebsnr, buf_h_artikel._recid, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep._recid in db_session.query(H_bill_line.tischnr, H_bill_line.bill_datum, H_bill_line.sysdate, H_bill_line.zeit, H_bill_line.artnr, H_bill_line.departement, H_bill_line.bezeich, H_bill_line.anzahl, H_bill_line._recid, H_bill_line.steuercode, Buf_h_artikel.bondruckernr, Buf_h_artikel.artnr, Buf_h_artikel.bezeich, Buf_h_artikel.endkum, Buf_h_artikel.betriebsnr, Buf_h_artikel._recid, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep._recid).join(Buf_h_artikel,(Buf_h_artikel.artnr == H_bill_line.artnr) & (Buf_h_artikel.departement == dept) & (Buf_h_artikel.artart == 0)).join(Wgrpdep,(Wgrpdep.departement == dept) & (Wgrpdep.zknr == Buf_h_artikel.zwkum)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept) & (H_bill_line.steuercode <= 0)).order_by(Buf_h_artikel.bondruckernr[inc_value(0)], Wgrpdep.betriebsnr.desc(), H_bill_line.sysdate, H_bill_line.zeit, H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            add_zeit = add_zeit + 1
            recid_h_bill_line = h_bill_line._recid

            htparam = get_cache (Htparam, {"paramnr": [(eq, 865)]})

            if htparam.flogical and buf_h_artikel.bondruckernr[0] > 0:

                if not print_single:

                    if (k != buf_h_artikel.bondruckernr[0]):

                        if k > 0:
                            cut_it()
                        create_bon_output()
                        k = buf_h_artikel.bondruckernr[0]
                    write_article()
                else:
                    create_bon_output()
                    k = buf_h_artikel.bondruckernr[0]
                    write_article()
                    cut_it()

            hbline = get_cache (H_bill_line, {"_recid": [(eq, h_bill_line._recid)]})

            if buf_h_artikel.bondruckernr[0] != 0:

                if hbline.steuercode == 0:
                    hbline.steuercode = buf_h_artikel.bondruckernr[0]
                else:
                    hbline.steuercode = 9999
            else:

                if hbline.steuercode == 0:
                    h_bill_line.steuercode = 1
                else:
                    hbline.steuercode = 9999
            pass
            pass
            bline_created = True
    else:

        h_bill_line_obj_list = {}
        h_bill_line = H_bill_line()
        buf_h_artikel = H_artikel()
        wgrpdep = Wgrpdep()
        for h_bill_line.tischnr, h_bill_line.bill_datum, h_bill_line.sysdate, h_bill_line.zeit, h_bill_line.artnr, h_bill_line.departement, h_bill_line.bezeich, h_bill_line.anzahl, h_bill_line._recid, h_bill_line.steuercode, buf_h_artikel.bondruckernr, buf_h_artikel.artnr, buf_h_artikel.bezeich, buf_h_artikel.endkum, buf_h_artikel.betriebsnr, buf_h_artikel._recid, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep._recid in db_session.query(H_bill_line.tischnr, H_bill_line.bill_datum, H_bill_line.sysdate, H_bill_line.zeit, H_bill_line.artnr, H_bill_line.departement, H_bill_line.bezeich, H_bill_line.anzahl, H_bill_line._recid, H_bill_line.steuercode, Buf_h_artikel.bondruckernr, Buf_h_artikel.artnr, Buf_h_artikel.bezeich, Buf_h_artikel.endkum, Buf_h_artikel.betriebsnr, Buf_h_artikel._recid, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep._recid).join(Buf_h_artikel,(Buf_h_artikel.artnr == H_bill_line.artnr) & (Buf_h_artikel.departement == dept) & (Buf_h_artikel.artart == 0)).join(Wgrpdep,(Wgrpdep.departement == dept) & (Wgrpdep.zknr == Buf_h_artikel.zwkum)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept) & (H_bill_line.steuercode <= 0)).order_by(Buf_h_artikel.bondruckernr[inc_value(0)], H_bill_line.sysdate, H_bill_line.zeit, H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            count_k = count_k + 1
            add_zeit = add_zeit + 1
            recid_h_bill_line = h_bill_line._recid

            htparam = get_cache (Htparam, {"paramnr": [(eq, 865)]})

            if htparam.flogical and buf_h_artikel.bondruckernr[0] > 0:

                if not print_single:

                    if (k != buf_h_artikel.bondruckernr[0]):

                        if k > 0:
                            cut_it()
                        create_bon_output()
                        k = buf_h_artikel.bondruckernr[0]
                    write_article()
                else:
                    create_bon_output()
                    k = buf_h_artikel.bondruckernr[0]
                    write_article()
                    cut_it()

            hbline = get_cache (H_bill_line, {"_recid": [(eq, h_bill_line._recid)]})

            if buf_h_artikel.bondruckernr[0] != 0:

                if hbline.steuercode == 0:
                    hbline.steuercode = buf_h_artikel.bondruckernr[0]
                else:
                    hbline.steuercode = 9999
            else:

                if hbline.steuercode == 0:
                    h_bill_line.steuercode = 1
                else:
                    hbline.steuercode = 9999
            pass
            pass
            bline_created = True

    if k > 0 and not print_single:
        cut_it()

    for t_queasy in query(t_queasy_data):
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        pass
        pass

    return generate_output()