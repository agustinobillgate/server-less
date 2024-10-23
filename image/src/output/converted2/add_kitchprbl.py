from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Queasy, H_bill_line, Htparam, Hoteldpt, H_bill, H_artikel, Wgrpdep, Printer, Bediener, Kellner, H_journal, H_mjourn, Printcod

def add_kitchprbl(pvilanguage:int, session_parameter:str, dept:int, rechnr:int, billdate:date, user_init:str):
    error_str = ""
    lvcarea:str = "add-kitchpr"
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
    room:str = ""
    gname:str = ""
    room_str:str = ""
    printer_loc:str = ""
    create_queasy:bool = False
    count_k:int = 0
    queasy = h_bill_line = htparam = hoteldpt = h_bill = h_artikel = wgrpdep = printer = bediener = kellner = h_journal = h_mjourn = printcod = None

    t_queasy = submenu_list = hbline = qsy = qbuff = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    submenu_list_list, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "zknr":int, "request":str})

    Hbline = create_buffer("Hbline",H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list
        return {"error_str": error_str}

    def create_bon_output():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list

        tableno:int = 0
        Qsy = T_queasy
        qsy_list = t_queasy_list

        printer = db_session.query(Printer).filter(
                 (Printer.nr == h_artikel.bondruckernr[0)]).first()

        if not printer:
            error_str = error_str + translateExtended ("The kitchen vhp.printer number", lvcarea, "") + " " + to_string(h_artikel.bondrucker[0]) + chr(10) + translateExtended ("in Article", lvcarea, "") + " " + to_string(h_artikel.artnr) + " - " + h_artikel.bezeich + chr(10) + translateExtended ("not defined in the vhp.printer Administration!", lvcarea, "") + chr(10)
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            t_queasy.key = 3


        else:
            get_printer_number()

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 208) & (Queasy.number1 == h_artikel.endkum)).first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 208
                queasy.number1 = h_artikel.endkum
                queasy.number2 = 1


            else:
                queasy.number2 = queasy.number2 + 1


            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

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


        t_queasy.char3 = hoteldpt.depart + chr(10) + translateExtended ("BillNo", lvcarea, "") + " " + to_string(h_bill.rechnr) + chr(10) + translateExtended (room_str, lvcarea, "") + " " + to_string(room) + " " + to_string(gname) + chr(10) + translateExtended ("Table", lvcarea, "") + " " + to_string(tableno) + " " + translateExtended ("Pax", lvcarea, "") + " " + to_string(h_bill.belegung) + chr(10) + to_string(get_current_date()) + " " + to_string(time, "HH:MM") + chr(10)

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            t_queasy.char3 = t_queasy.char3 + translateExtended ("Posted by:", lvcarea, "") + " " + bediener.username + chr(10)
        else:

            kellner = db_session.query(Kellner).filter(
                     (Kellner.kellner_nr == h_bill.kellner_nr) & (Kellner.departement == h_bill.departement)).first()

            if kellner:
                t_queasy.char3 = t_queasy.char3 + translateExtended ("Waiter:", lvcarea, "") + " " + kellner.kellnername + chr(10)

        qsy = query(qsy_list, filters=(lambda qsy: qsy.key == 10 and qsy.number1 == h_bill.betriebsnr), first=True)

        if qsy:
            t_queasy.char3 = t_queasy.char3 + translateExtended ("Order Taker:", lvcarea, "") + " " + qsy.char1 + chr(10)
        t_queasy.char3 = t_queasy.char3 + chr(10)


    def write_article():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list

        curr_recid:int = 0
        created:bool = False
        h_mjourn.h_artnr = None
        H_art =  create_buffer("H_art",H_artikel)
        Qbuff = T_queasy
        qbuff_list = t_queasy_list

        h_journal = db_session.query(H_journal).filter(
                 (H_journal.bill_datum == h_bill_line.bill_datum) & (H_journal.sysdate == h_bill_line.sysdate) & (H_journal.zeit == h_bill_line.zeit) & (H_journal.artnr == h_bill_line.artnr) & (H_journal.departement == h_bill_line.departement) & (H_journal.schankbuch == recid_h_bill_line)).first()

        if print_subgrp and print_single:
            prev_zknr = wgrpdep.zknr
            t_queasy.char3 = t_queasy.char3 + "[" + to_string(wgrpdep.bezeich) + "]" + chr(10)

        elif (print_subgrp or sort_subgrp_prior) and not print_single and (prev_zknr != wgrpdep.zknr):
            prev_zknr = wgrpdep.zknr
            t_queasy.char3 = t_queasy.char3 + "[" + to_string(wgrpdep.bezeich) + "]" + chr(10)

        if desclength == 0 or len(h_bill_line.bezeich) <= desclength:
            t_queasy.char3 = t_queasy.char3 + to_string(h_bill_line.anzahl, "->>9 ") + to_string(h_bill_line.bezeich) + chr(10)
        else:
            write_descript(to_string(h_bill_line.anzahl, "->>9 "), to_string(h_bill_line.bezeich))

        qbuff = query(qbuff_list, filters=(lambda qbuff: qbuff.key == 38 and qbuff.number1 == h_bill_line.departement and qbuff.number2 == h_bill_line.artnr), first=True)

        if qbuff:

            if desclength == 0 or len(t_queasy.char3) <= desclength:
                t_queasy.char3 = t_queasy.char3 + to_string("", "x(5)") + to_string(qbuff.char3) + chr(10)
            else:
                write_descript(to_string("", "x(5)"), to_string(qbuff.char3))

        if h_bill_line.anzahl != 0:

            if h_journal and h_journal.aendertext != "":
                t_queasy.char3 = t_queasy.char3 + " ::: " + h_journal.aendertext + chr(10)

            if h_journal and h_journal.stornogrund != "":
                t_queasy.char3 = t_queasy.char3 + " >>> " + to_string(h_journal.stornogrund, "x(20)") + chr(10)

        if h_artikel.betriebsnr > 0:

            for submenu_list in query(submenu_list_list, filters=(lambda submenu_list: submenu_list.nr == h_artikel.betriebsnr and submenu_list.zeit == h_bill_line.zeit)):
                created = True
                t_queasy.char3 = t_queasy.char3 + " -> " + to_string(submenu_list.bezeich) + chr(10)

                if submenu_list.request != "":
                    t_queasy.char3 = t_queasy.char3 + ":::" + submenu_list.request + chr(10)
                submenu_list_list.remove(submenu_list)

            if not created:

                h_journal = db_session.query(H_journal).filter(
                         (H_journal.artnr == h_bill_line.artnr) & (H_journal.departement == dept) & (H_journal.rechnr == rechnr) & (H_journal.bill_datum == h_bill_line.bill_datum) & (H_journal.zeit == h_bill_line.zeit) & (H_journal.sysdate == h_bill_line.sysdate) & (H_journal.schankbuch == recid_h_bill_line)).first()

                if h_journal:

                    for h_mjourn in db_session.query(H_mjourn).filter(
                             (H_mjourn.departement == dept) & (H_mjourn.h_artnr == h_journal.artnr) & (H_mjourn.rechnr == h_journal.rechnr) & (H_mjourn.bill_datum == h_journal.bill_datum) & (H_mjourn.sysdate == h_journal.sysdate) & (H_mjourn.zeit == h_journal.zeit)).order_by(H_mjourn._recid).all():

                        h_mjourn.h_artnr = db_session.query(H_art).filter(
                                 (H_art.artnr == h_mjourn.artnr) & (H_art.departement == dept)).first()

                        if h_mjourn.h_artnr:
                            created = True
                            t_queasy.char3 = t_queasy.char3 + " -> " + to_string(h_mjourn.h_artnr.bezeich) + chr(10)

                            if h_mjourn.request != "":
                                t_queasy.char3 = t_queasy.char3 + ":::" + h_mjourn.request + chr(10)


        if created:
            t_queasy.char3 = t_queasy.char3 + " " + chr(10)


    def write_descript(str1:str, str2:str):

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list

        s1:str = ""
        s2:str = ""
        word:str = ""
        next_line:bool = False
        i:int = 0
        length1:int = 0
        t_queasy.char3 = t_queasy.char3 + str1

        if num_entries(str2, " ") == 1:

            if round(desclength / 2, 0) * 2 != desclength:
                length1 = desclength - 1
            else:
                length1 = desclength
            t_queasy.char3 = t_queasy.char3 + substring(str2, 0, length1) + chr(10)
            for i in range(1,len(str1)  + 1) :
                t_queasy.char3 = t_queasy.char3 + " "
            t_queasy.char3 = t_queasy.char3 + substring(str2, length1 + 1 - 1) + chr(10)

            return
        next_line = False
        for i in range(1,num_entries(str2, " ")  + 1) :
            word = entry(i - 1, str2, " ")

            if next_line:
                s2 = s2 + word + " "
            else:

                if len(s1 + word) <= desclength:
                    s1 = s1 + word + " "
                else:
                    next_line = True
                    s2 = s2 + word + " "
        t_queasy.char3 = t_queasy.char3 + s1 + chr(10)
        for i in range(1,len(str1)  + 1) :
            t_queasy.char3 = t_queasy.char3 + " "
        t_queasy.char3 = t_queasy.char3 + s2 + chr(10)


    def cut_it():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list

        i:int = 0

        if numcat1 == 0:
            t_queasy.char3 = t_queasy.char3 + " " + chr(10) + chr(10) + " " + chr(10) + " " + chr(10)
        else:
            for i in range(1,numcat1 + 1) :
                t_queasy.char3 = t_queasy.char3 + " " + chr(10)

        printcod = db_session.query(Printcod).filter(
                 (Printcod.emu == printer.emu) & (func.lower(Printcod.code) == ("cut").lower())).first()

        if printcod:
            t_queasy.char3 = t_queasy.char3 + printcod.contcod + chr(10)
        else:

            if numcat2 == 0:
                t_queasy.char3 = t_queasy.char3 + " " + chr(10) + " " + chr(10) + " " + chr(10) + " " + chr(10) + " " + chr(10)
            else:
                for i in range(1,numcat2 + 1) :
                    t_queasy.char3 = t_queasy.char3 + " " + chr(10)


    def readsession():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list

        lvctmp:str = ""
        lvcleft:str = ""
        lvcval:str = ""
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

                printer = db_session.query(Printer).filter(
                         (Printer.nr == kitchen_pr[i - 1)]).first()

                if not printer:
                    error_str = error_str + translateExtended ("Kitchen Printer Number", lvcarea, "") + " " + to_string(kitchen_pr[i - 1]) + " " + translateExtended ("not found (wrong parameter startup).", lvcarea, "") + chr(10)

                    return
        kitchen_pr[9] = 1


    def get_printer_number():

        nonlocal error_str, lvcarea, kitchen_pr, numcat1, numcat2, k, prev_zknr, add_zeit, always_do, bline_created, print_subgrp, print_single, desclength, sort_subgrp, recid_h_bill_line, sort_subgrp_prior, room, gname, room_str, printer_loc, create_queasy, count_k, queasy, h_bill_line, htparam, hoteldpt, h_bill, h_artikel, wgrpdep, printer, bediener, kellner, h_journal, h_mjourn, printcod
        nonlocal pvilanguage, session_parameter, dept, rechnr, billdate, user_init
        nonlocal hbline


        nonlocal t_queasy, submenu_list, hbline, qsy, qbuff
        nonlocal t_queasy_list, submenu_list_list

        if printer.path == "KPR1":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[0)]).first()

            return
        elif printer.path == "KPR2":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[1)]).first()

            return
        elif printer.path == "KPR3":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[2)]).first()

            return
        elif printer.path == "KPR4":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[3)]).first()

            return
        elif printer.path == "KPR5":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[4)]).first()

            return
        elif printer.path == "KPR6":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[5)]).first()

            return
        elif printer.path == "KPR7":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[6)]).first()

            return
        elif printer.path == "KPR8":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[7)]).first()

            return
        elif printer.path == "KPR9":

            printer = db_session.query(Printer).filter(
                     (Printer.nr == kitchen_pr[8)]).first()

            return

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 252)).first()
    numcat1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 562)).first()
    numcat2 = htparam.finteger
    billdate = get_output(htpdate(110))

    if get_current_date() > billdate:
        billdate = get_current_date()
    readsession()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 450)).first()

    if htparam:
        print_subgrp = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 147)).first()

    if htparam:
        sort_subgrp = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 838)).first()

    if htparam:
        sort_subgrp_prior = htparam.flogical

    hoteldpt = db_session.query(Hoteldpt).filter(
             (Hoteldpt.num == dept)).first()

    h_bill = db_session.query(H_bill).filter(
             (H_bill.departement == dept) & (H_bill.rechnr == rechnr)).first()

    if sort_subgrp :

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel, wgrpdep in db_session.query(H_bill_line, H_artikel, Wgrpdep).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == dept) & (H_artikel.artart == 0)).join(Wgrpdep,(Wgrpdep.departement == dept) & (Wgrpdep.zknr == H_artikel.zwkum)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept) & (H_bill_line.steuercode <= 0)).order_by(H_artikel.bondruckernr[inc_value(0)], H_artikel.zwkum, H_bill_line.sysdate, H_bill_line.zeit, H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            add_zeit = add_zeit + 1
            recid_h_bill_line = h_bill_line._recid

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 865)).first()

            if htparam.flogical and h_artikel.bondruckernr[0] > 0:

                if not print_single:

                    if (k != h_artikel.bondruckernr[0]):

                        if k > 0:
                            cut_it()
                        create_bon_output()
                        k = h_artikel.bondruckernr[0]
                    write_article()
                else:
                    create_bon_output()
                    k = h_artikel.bondruckernr[0]
                    write_article()
                    cut_it()

            hbline = db_session.query(Hbline).filter(
                         (Hbline._recid == h_bill_line._recid)).first()

            if h_artikel.bondruckernr[0] != 0:

                if hbline.steuercode == 0:
                    hbline.steuercode = h_artikel.bondruckernr[0]
                else:
                    hbline.steuercode = 9999
            else:

                if hbline.steuercode == 0:
                    h_bill_line.steuercode = 1
                else:
                    hbline.steuercode = 9999
            pass
            bline_created = True


    elif sort_subgrp_prior :

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel, wgrpdep in db_session.query(H_bill_line, H_artikel, Wgrpdep).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == dept) & (H_artikel.artart == 0)).join(Wgrpdep,(Wgrpdep.departement == dept) & (Wgrpdep.zknr == H_artikel.zwkum)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept) & (H_bill_line.steuercode <= 0)).order_by(H_artikel.bondruckernr[inc_value(0)], Wgrpdep.betriebsnr.desc(), H_bill_line.sysdate, H_bill_line.zeit, H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            add_zeit = add_zeit + 1
            recid_h_bill_line = h_bill_line._recid

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 865)).first()

            if htparam.flogical and h_artikel.bondruckernr[0] > 0:

                if not print_single:

                    if (k != h_artikel.bondruckernr[0]):

                        if k > 0:
                            cut_it()
                        create_bon_output()
                        k = h_artikel.bondruckernr[0]
                    write_article()
                else:
                    create_bon_output()
                    k = h_artikel.bondruckernr[0]
                    write_article()
                    cut_it()

            hbline = db_session.query(Hbline).filter(
                         (Hbline._recid == h_bill_line._recid)).first()

            if h_artikel.bondruckernr[0] != 0:

                if hbline.steuercode == 0:
                    hbline.steuercode = h_artikel.bondruckernr[0]
                else:
                    hbline.steuercode = 9999
            else:

                if hbline.steuercode == 0:
                    h_bill_line.steuercode = 1
                else:
                    hbline.steuercode = 9999
            pass
            bline_created = True

    else:

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel, wgrpdep in db_session.query(H_bill_line, H_artikel, Wgrpdep).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == dept) & (H_artikel.artart == 0)).join(Wgrpdep,(Wgrpdep.departement == dept) & (Wgrpdep.zknr == H_artikel.zwkum)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept) & (H_bill_line.steuercode <= 0)).order_by(H_artikel.bondruckernr[inc_value(0)], H_bill_line.sysdate, H_bill_line.zeit, H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            count_k = count_k + 1
            add_zeit = add_zeit + 1
            recid_h_bill_line = h_bill_line._recid

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 865)).first()

            if htparam.flogical and h_artikel.bondruckernr[0] > 0:

                if not print_single:

                    if (k != h_artikel.bondruckernr[0]):

                        if k > 0:
                            cut_it()
                        create_bon_output()
                        k = h_artikel.bondruckernr[0]
                    write_article()
                else:
                    create_bon_output()
                    k = h_artikel.bondruckernr[0]
                    write_article()
                    cut_it()

            hbline = db_session.query(Hbline).filter(
                         (Hbline._recid == h_bill_line._recid)).first()

            if h_artikel.bondruckernr[0] != 0:

                if hbline.steuercode == 0:
                    hbline.steuercode = h_artikel.bondruckernr[0]
                else:
                    hbline.steuercode = 9999
            else:

                if hbline.steuercode == 0:
                    h_bill_line.steuercode = 1
                else:
                    hbline.steuercode = 9999
            pass
            bline_created = True


    if k > 0 and not print_single:
        cut_it()

    for t_queasy in query(t_queasy_list):
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        pass


    return generate_output()