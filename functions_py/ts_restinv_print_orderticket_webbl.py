#using conversion tools version: 1.0.0.119

# ======================================
# Rulita, 10-11-2025 | C553A2
# Issue :
# - New Compile Program
# - Fixing inden
# - Fixing printter.emu -> printcod.emu
# ======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line, H_artikel, Queasy, H_bill, Wgrpdep, Hoteldpt, Kellner, Printcod, H_journal, H_mjourn

submenu_list_data, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})

def ts_restinv_print_orderticket_webbl(submenu_list_data:[Submenu_list], pvilanguage:int, close_it:bool, reprint_it:bool, h_bill_rechnr:int, curr_dept:int, disc_art1:int, disc_art2:int, disc_art3:int, prorder:int, desclength:int):

    prepare_cache ([H_bill_line, H_artikel, Queasy, H_bill, Wgrpdep, Hoteldpt, Kellner, Printcod, H_journal, H_mjourn])

    k = 0
    header_list_data = []
    output_list_data = []
    prev_zknr:int = 0
    do_it:bool = False
    recid_h_bill_line:int = 0
    lvcarea:string = "TS-restinv"
    h_bill_line = h_artikel = queasy = h_bill = wgrpdep = hoteldpt = kellner = printcod = h_journal = h_mjourn = None

    submenu_list = header_list = output_list = art_list = abuff = hbuff = hbline = qsy = None

    header_list_data, Header_list = create_model("Header_list", {"k":int, "depart":string, "tableno":string, "datum":date, "pax":string, "zeit":string, "ordertaker":string, "waiter":string, "bill_no":string, "guest_name":string})
    output_list_data, Output_list = create_model("Output_list", {"bill_no":int, "bezeich":string, "pos":int, "subgrp":string, "submenu_request":string, "printcod_concod":string, "aendertext":string, "pax":string, "stornogrund":string, "submenu_bezeich":string, "bezeich2":string, "rec_id":int, "menu_flag":int, "sub_menu_betriebsnr":int})
    art_list_data, Art_list = create_model_like(H_bill_line)

    Abuff = create_buffer("Abuff",H_artikel)
    Hbuff = create_buffer("Hbuff",H_bill_line)
    Hbline = create_buffer("Hbline",H_bill_line)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal k, header_list_data, output_list_data, prev_zknr, do_it, recid_h_bill_line, lvcarea, h_bill_line, h_artikel, queasy, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, disc_art1, disc_art2, disc_art3, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy


        nonlocal submenu_list, header_list, output_list, art_list, abuff, hbuff, hbline, qsy
        nonlocal header_list_data, output_list_data, art_list_data

        return {"k": k, "header-list": header_list_data, "output-list": output_list_data}

    def create_bon_header():

        nonlocal k, header_list_data, output_list_data, prev_zknr, do_it, recid_h_bill_line, lvcarea, h_bill_line, h_artikel, queasy, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, disc_art1, disc_art2, disc_art3, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy


        nonlocal submenu_list, header_list, output_list, art_list, abuff, hbuff, hbline, qsy
        nonlocal header_list_data, output_list_data, art_list_data

        tableno:int = 0
        ct:string = ""
        i:int = 0
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
        ct = hoteldpt.depart
        header_list = Header_list()
        header_list_data.append(header_list)

        header_list.tableno = to_string(h_bill.tischnr)
        header_list.pax = to_string(h_bill.belegung)
        header_list.datum = get_current_date()
        header_list.zeit = to_string(get_current_time_in_seconds(), "HH:MM")
        header_list.depart = ct
        header_list.bill_no = "Bill No: " + to_string(h_bill.rechnr)

        if reprint_it or (hbuff.steuercode == 9999):
            header_list.bill_no = header_list.bill_no + " (RE-PRINT)"

        qsy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

        # Rulita, 10-11-2025
        # Fixing inden
        if qsy:
            header_list.ordertaker = qsy.char1 + "-" + qsy.char2
        else:

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

            if kellner:
                header_list.waiter = kellner.kellnername

        if h_bill.bilname != "" or h_bill.bilname != None:
            header_list.guest_name = "Guest Name: " + h_bill.bilname


    def write_article(s_recid:int, prev_zknr:int):

        nonlocal k, header_list_data, output_list_data, do_it, recid_h_bill_line, lvcarea, h_bill_line, h_artikel, queasy, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, disc_art1, disc_art2, disc_art3, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy


        nonlocal submenu_list, header_list, output_list, art_list, abuff, hbuff, hbline, qsy
        nonlocal header_list_data, output_list_data, art_list_data

        curr_recid:int = 0
        created:bool = False
        i:int = 0
        ct:string = ""
        h_art = None
        qbuff = None
        hbuff = None

        def generate_inner_output():
            return (prev_zknr)

        H_art =  create_buffer("H_art",H_artikel)
        Qbuff =  create_buffer("Qbuff",Queasy)
        Hbuff =  create_buffer("Hbuff",H_bill_line)

        hbuff = get_cache (H_bill_line, {"_recid": [(eq, s_recid)]})
        output_list = Output_list()
        output_list_data.append(output_list)


        if hbuff.anzahl < 0:

            # Rulita, 10-11-2025
            # Fixing printter.emu -> printcod.emu
            printcod = get_cache (Printcod, {"emu": [(eq, printcod.emu)],"code": [(eq, "redpr")]})

            if printcod:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.printcod_concod = printcod.contcod

        h_journal = get_cache (H_journal, {"bill_datum": [(eq, hbuff.bill_datum)],"sysdate": [(eq, hbuff.sysdate)],"zeit": [(eq, hbuff.zeit)],"artnr": [(eq, hbuff.artnr)],"departement": [(eq, hbuff.departement)],"schankbuch": [(eq, recid_h_bill_line)]})

        if prev_zknr != wgrpdep.zknr:
            prev_zknr = wgrpdep.zknr
            output_list.subgrp = "[" + wgrpdep.bezeich + "]"
        
        # Rulita, 10-11-2025
        # Fixing inden
        if desclength == 0 or length(hbuff.bezeich) <= desclength:
            output_list.pax = to_string(hbuff.anzahl)
            output_list.bezeich = hbuff.bezeich
        else:
            write_descript(to_string(hbuff.anzahl), to_string(hbuff.bezeich))

        qbuff = get_cache (Queasy, {"key": [(eq, 38)],"number1": [(eq, hbuff.departement)],"number2": [(eq, hbuff.artnr)]})

        if qbuff:

            if desclength == 0 or length(qbuff.char3) <= desclength:
                output_list.bezeich2 = qbuff.char3
            else:
                write_descript(to_string("", "x(5)"), to_string(qbuff.char3))

        if hbuff.anzahl != 0:

            if h_journal and h_journal.aendertext != "":
                output_list.aendertext = ":::" + h_journal.aendertext

            if h_journal and h_journal.stornogrund != "":
                output_list.stornogrund = ">>>" + to_string(h_journal.stornogrund, "x(20)")
        output_list.rec_id = s_recid
        output_list.rec_id = hbuff._recid

        if hbuff.anzahl < 0:

            # Rulita, 10-11-2025
            # Fixing printter.emu -> printcod.emu
            printcod = get_cache (Printcod, {"emu": [(eq, printcod.emu)],"code": [(eq, "redpr-")]})

            if printcod:
                output_list.printcod_concod = printcod.contcod

        if h_artikel.betriebsnr > 0:

            for submenu_list in query(submenu_list_data, filters=(lambda submenu_list: submenu_list.nr == h_artikel.betriebsnr and submenu_list.zeit == hbuff.zeit)):
                created = True
                submenu_bezeich = "-> " + to_string(submenu_list.bezeich)

                if submenu_list.request != "":
                    output_list.submenu_request = ":::" + submenu_list.request
                submenu_list_data.remove(submenu_list)

            if not created:

                h_journal = get_cache (H_journal, {"artnr": [(eq, hbuff.artnr)],"departement": [(eq, curr_dept)],"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(eq, hbuff.bill_datum)],"zeit": [(eq, hbuff.zeit)],"sysdate": [(eq, hbuff.sysdate)]})

                if h_journal:

                    for h_mjourn in db_session.query(H_mjourn).filter(
                             (H_mjourn.departement == curr_dept) & (H_mjourn.h_artnr == h_journal.artnr) & (H_mjourn.rechnr == h_journal.rechnr) & (H_mjourn.bill_datum == h_journal.bill_datum) & (H_mjourn.sysdate == h_journal.sysdate) & (H_mjourn.zeit == h_journal.zeit)).order_by(H_mjourn._recid).all():

                        h_art = get_cache (H_artikel, {"artnr": [(eq, h_mjourn.artnr)],"departement": [(eq, curr_dept)]})

                        if h_art:

                            if num_entries(h_mjourn.request, "|") > 1:

                                if entry(0, h_mjourn.request, "|") == to_string(s_recid):
                                    created = True
                                    output_list = Output_list()
                                    output_list_data.append(output_list)

                                    output_list.menu_flag = 2
                                    output_list.sub_menu_betriebsnr = h_mjourn.nr
                                    output_list.submenu_bezeich = h_art.bezeich
                                    output_list.rec_id = s_recid
                                    output_list.aendertext = ":::" + entry(1, h_mjourn.request, "|")
                                    output_list.pax = to_string(h_mjourn.anzahl)
                                    output_list.subgrp = "[" + wgrpdep.bezeich + "]"


        return generate_inner_output()


    def write_descript(str1:string, str2:string):

        nonlocal k, header_list_data, output_list_data, prev_zknr, do_it, recid_h_bill_line, lvcarea, h_bill_line, h_artikel, queasy, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, disc_art1, disc_art2, disc_art3, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy


        nonlocal submenu_list, header_list, output_list, art_list, abuff, hbuff, hbline, qsy
        nonlocal header_list_data, output_list_data, art_list_data

        ct:string = ""
        s1:string = ""
        s2:string = ""
        word:string = ""
        next_line:bool = False
        i:int = 0
        length1:int = 0

        if num_entries(str2, " ") == 1:

            if round(desclength / 2, 0) * 2 != desclength:
                length1 = desclength - 1
            else:
                length1 = desclength
            ct = substring(str2, 0, length1)
            for i in range(1,length(ct)  + 1) :
                output_list.bezeich = to_string(substring(ct, i - 1, 1) , "x(1)")
            output_list.bezeich = " "
            ct = ""
            for i in range(1,length(str1)  + 1) :
                ct = ct + " "
            ct = ct + substring(str2, length1 + 1 - 1)
            for i in range(1,length(ct)  + 1) :
                output_list.bezeich = to_string(substring(ct, i - 1, 1) , "x(1)")
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
        ct = s1
        for i in range(1,length(ct)  + 1) :
            output_list.bezeich = to_string(substring(ct, i - 1, 1) , "x(1)")
        output_list.bezeich = " "
        ct = ""
        for i in range(1,length(str1)  + 1) :
            ct = ct + " "
        ct = ct + s2
        for i in range(1,length(ct)  + 1) :
            output_list.pax = to_string(substring(ct, i - 1, 1) , "x(1)")
        output_list.pax = " "

    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_rechnr)],"departement": [(eq, curr_dept)]})

    if not h_bill:

        return generate_output()

    if not reprint_it:

        hbuff_obj_list = {}
        hbuff = H_bill_line()
        abuff = H_artikel()
        wgrpdep = Wgrpdep()
        for hbuff.bill_datum, hbuff.sysdate, hbuff.zeit, hbuff.artnr, hbuff.departement, hbuff.bezeich, hbuff.anzahl, hbuff._recid, hbuff.steuercode, abuff.betriebsnr, abuff._recid, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep._recid in db_session.query(Hbuff.bill_datum, Hbuff.sysdate, Hbuff.zeit, Hbuff.artnr, Hbuff.departement, Hbuff.bezeich, Hbuff.anzahl, Hbuff._recid, Hbuff.steuercode, Abuff.betriebsnr, Abuff._recid, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep._recid).join(Abuff,(Abuff.artnr == Hbuff.artnr) & (Abuff.departement == curr_dept) & (Abuff.artart == 0) & (Abuff.artnr != disc_art1) & (Abuff.artnr != disc_art2) & (Abuff.artnr != disc_art3)).join(Wgrpdep,(Wgrpdep.departement == curr_dept) & (Wgrpdep.zknr == Abuff.zwkum)).filter(
                 (Hbuff.rechnr == h_bill_rechnr) & (Hbuff.departement == curr_dept)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr, Hbuff.artnr, Hbuff.sysdate, Hbuff.zeit).all():
            if hbuff_obj_list.get(hbuff._recid):
                continue
            else:
                hbuff_obj_list[hbuff._recid] = True

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, hbuff.artnr)]})
            recid_h_bill_line = hbuff._recid
            do_it = reprint_it or (hbuff.steuercode >= 0 and hbuff.steuercode < 9999)

            if do_it:
                k = k + 1

                if k == 1:
                    create_bon_header()
                prev_zknr = write_article(hbuff._recid, prev_zknr)

                if close_it:

                    hbline = get_cache (H_bill_line, {"_recid": [(eq, hbuff._recid)]})

                    if hbline.steuercode == 0:
                        hbuff.steuercode = - prorder
                    else:
                        hbline.steuercode = 9999
                    pass
                    pass
    else:

        hbuff_obj_list = {}
        hbuff = H_bill_line()
        abuff = H_artikel()
        wgrpdep = Wgrpdep()
        for hbuff.bill_datum, hbuff.sysdate, hbuff.zeit, hbuff.artnr, hbuff.departement, hbuff.bezeich, hbuff.anzahl, hbuff._recid, hbuff.steuercode, abuff.betriebsnr, abuff._recid, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep._recid in db_session.query(Hbuff.bill_datum, Hbuff.sysdate, Hbuff.zeit, Hbuff.artnr, Hbuff.departement, Hbuff.bezeich, Hbuff.anzahl, Hbuff._recid, Hbuff.steuercode, Abuff.betriebsnr, Abuff._recid, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep._recid).join(Abuff,(Abuff.artnr == Hbuff.artnr) & (Abuff.departement == curr_dept) & (Abuff.artart == 0) & (Abuff.artnr != disc_art1) & (Abuff.artnr != disc_art2) & (Abuff.artnr != disc_art3)).join(Wgrpdep,(Wgrpdep.departement == curr_dept) & (Wgrpdep.zknr == Abuff.zwkum)).filter(
                 (Hbuff.rechnr == h_bill_rechnr) & (Hbuff.departement == curr_dept) & (Hbuff.steuercode == 9999)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr, Hbuff.artnr, Hbuff.sysdate, Hbuff.zeit).all():
            if hbuff_obj_list.get(hbuff._recid):
                continue
            else:
                hbuff_obj_list[hbuff._recid] = True

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, hbuff.artnr)]})
            recid_h_bill_line = hbuff._recid
            do_it = reprint_it or (hbuff.steuercode == 9999)

            if do_it:
                k = k + 1

                if k == 1:
                    create_bon_header()
                prev_zknr = write_article(hbuff._recid, prev_zknr)

    return generate_output()