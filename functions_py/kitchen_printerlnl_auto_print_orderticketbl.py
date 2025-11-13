# using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_23/10/2025

    Ticket ID: C8AAF9
        _remark_:   - fix definition variabel
                    - fix python indentation
            
    _yusufwijasena_12/11/2025
    Ticket ID: F6D79E
        _remark_:   - last update from FDL: 6C4097
"""

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_bill_line, Queasy, Htparam, H_bill, Wgrpdep, Hoteldpt, Kellner, Printcod, H_journal, H_mjourn, Printer


def kitchen_printerlnl_auto_print_orderticketbl(pvilanguage: int, close_it: bool, reprint_it: bool, h_bill_rechnr: int, curr_dept: int, prorder: int, desclength: int):

    prepare_cache([H_artikel, H_bill_line, Queasy, Htparam, H_bill, Wgrpdep, Hoteldpt, Kellner, Printcod, H_journal, H_mjourn, Printer])

    k = 0
    output_list_data = []
    prev_zknr: int = 0
    do_it: bool = False
    recid_h_bill_line: int = 0
    disc_art1: int = 0
    disc_art2: int = 0
    disc_art3: int = 0
    numcat1: int = 0  # FDL: 6C4097
    numcat2: int = 0  # FDL: 6C4097
    lvcarea: str = "kitchen-printerlnl"
    h_artikel = h_bill_line = queasy = htparam = h_bill = wgrpdep = hoteldpt = kellner = printcod = h_journal = h_mjourn = printer = None

    submenu_list = output_list = abuff = hbuff = hbline = qsy = None

    submenu_list_data, Submenu_list = create_model(
        "Submenu_list",
        {
            "menurecid": int,
            "zeit": int,
            "nr": int,
            "artnr": int,
            "bezeich": str,
            "anzahl": int,
            "zknr": int,
            "request": str
        })
    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "str": str,
            "pos": int
        })

    Abuff = create_buffer("Abuff", H_artikel)
    Hbuff = create_buffer("Hbuff", H_bill_line)
    Hbline = create_buffer("Hbline", H_bill_line)
    Qsy = create_buffer("Qsy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal k, output_list_data, prev_zknr, do_it, recid_h_bill_line, disc_art1, disc_art2, disc_art3, numcat1, numcat2, lvcarea, h_artikel, h_bill_line, queasy, htparam, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn, printer
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy
        nonlocal submenu_list, output_list, abuff, hbuff, hbline, qsy
        nonlocal submenu_list_data, output_list_data

        return {
            "k": k,
            "output-list": output_list_data
        }

    def create_bon_header():
        nonlocal k, output_list_data, prev_zknr, do_it, recid_h_bill_line, disc_art1, disc_art2, disc_art3, numcat1, numcat2, lvcarea, h_artikel, h_bill_line, queasy, htparam, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn, printer
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy
        nonlocal submenu_list, output_list, abuff, hbuff, hbline, qsy
        nonlocal submenu_list_data, output_list_data

        tableno: int = 0  # FDL: 3E80DC
        ct: str = ""
        i: int = 0
        qsy = None
        Qsy = create_buffer("Qsy", Queasy)
        tableno = h_bill.tischnr

        hoteldpt = get_cache(Hoteldpt, {"num": [(eq, curr_dept)]})
        ct = hoteldpt.depart
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, len(ct) + 1):
            output_list.str = output_list.str + to_string(substring(ct, i - 1, 1), "x(1)")
            
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.str = output_list.str + to_string("")
        output_list.str = output_list.str + \
            translateExtended("Bill No:", lvcarea, "") + " " + to_string(h_bill_rechnr)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.str = output_list.str + to_string("")
        ct = translateExtended("Table", lvcarea, "") + " " + to_string(tableno) + " " + \
            translateExtended("Pax", lvcarea, "") + " " + to_string(h_bill.belegung) + \
            " - " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
        for i in range(1, length(ct) + 1):
            output_list.str = output_list.str + to_string(substring(ct, i - 1, 1), "x(1)")
            
        output_list.str = output_list.str + chr_unicode(10)

        qsy = get_cache(
            Queasy, {"key": [(eq, 10)], "number1": [(eq, h_bill.betriebsnr)]})

        if qsy:
            ct = translateExtended("Order Taker:", lvcarea, "") + " " + qsy.char1
            
            for i in range(1, len(ct) + 1):
                output_list.str = output_list.str + \
                    to_string(substring(ct, i - 1, 1), "x(1)")
            output_list.str = output_list.str + chr_unicode(10)
            
        else:
            kellner = get_cache(
                Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

            if kellner:
                ct = translateExtended(
                    "Waiter:", lvcarea, "") + " " + kellner.kellnername
                for i in range(1, len(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")
                output_list.str = output_list.str + chr_unicode(10)

        if h_bill.bilname != "" or h_bill.bilname != None:
            ct = translateExtended(
                "Guest Name:", lvcarea, "") + " " + h_bill.bilname
            for i in range(1, length(ct) + 1):
                output_list.str = output_list.str + \
                    to_string(substring(ct, i - 1, 1), "x(1)")
        output_list.str = output_list.str
        output_list = Output_list()
        output_list_data.append(output_list)

    def write_article(s_recid: int, prev_zknr: int):
        nonlocal k, output_list_data, do_it, recid_h_bill_line, disc_art1, disc_art2, disc_art3, numcat1, numcat2, lvcarea, h_artikel, h_bill_line, queasy, htparam, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn, printer
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy
        nonlocal submenu_list, output_list, abuff, hbuff, hbline, qsy
        nonlocal submenu_list_data, output_list_data

        curr_recid: int = 0
        created: bool = False
        ct: str = ""
        i: int = 0
        h_art = None
        qbuff = None
        hbuff = None

        def generate_inner_output():
            return (prev_zknr)

        H_art = create_buffer("H_art", H_artikel)
        Qbuff = create_buffer("Qbuff", Queasy)
        Hbuff = create_buffer("Hbuff", H_bill_line)

        hbuff = get_cache(H_bill_line, {"_recid": [(eq, s_recid)]})
        output_list = Output_list()
        output_list_data.append(output_list)

        if hbuff.anzahl < 0:
            # FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu
            # AND vhp.printcod.code = "redpr-" NO-LOCK NO-ERROR.
            printcod = get_cache(
                Printcod, {"emu": [(eq, printer.emu)], "code": [(eq, "redpr")]})

            if printcod:
                ct = printcod.contcod
                for i in range(1, len(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")

        h_journal = get_cache(
            H_journal, {"bill_datum": [(eq, hbuff.bill_datum)], "sysdate": [(eq, hbuff.sysdate)], "zeit": [(eq, hbuff.zeit)], "artnr": [(eq, hbuff.artnr)], "departement": [(eq, hbuff.departement)], "schankbuch": [(eq, recid_h_bill_line)]})

        if prev_zknr != wgrpdep.zknr:
            prev_zknr = wgrpdep.zknr
            # ct = "[" + to_string(wgrpdep.bezeich) + "]"
            ct = f"[{to_string(wgrpdep.bezeich)}]"
            
            for i in range(1, len(ct) + 1):
                output_list.str = output_list.str + \
                    to_string(substring(ct, i - 1, 1), "x(1)")
            output_list.str = output_list.str + chr_unicode(10)

        if desclength == 0 or length(hbuff.bezeich) <= desclength:
            ct = to_string(hbuff.anzahl, "->>9") + " " + to_string(hbuff.bezeich)
            for i in range(1, length(ct) + 1):
                output_list.str = output_list.str + \
                    to_string(substring(ct, i - 1, 1), "x(1)")
            else:
                write_descript(to_string(hbuff.anzahl), to_string(hbuff.bezeich))

        qbuff = get_cache(
            Queasy, {"key": [(eq, 38)], "number1": [(eq, hbuff.departement)], "number2": [(eq, hbuff.artnr)]})

        if qbuff:
            if desclength == 0 or length(qbuff.char3) <= desclength:
                ct = to_string("", "x(5)") + to_string(qbuff.char3)
                for i in range(1, length(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")
                output_list.str = output_list.str + chr_unicode(10)
            else:
                write_descript(to_string("", "x(5)"), to_string(qbuff.char3))
            output_list.str = output_list.str + chr_unicode(10)

        if hbuff.anzahl != 0:
            if h_journal and h_journal.aendertext != "":
                ct = ":::" + h_journal.aendertext
                for i in range(1, len(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")

            if h_journal and h_journal.stornogrund != "":
                ct = ">>>" + to_string(h_journal.stornogrund, "x(20)")
                for i in range(1, length(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")

        if h_artikel.betriebsnr > 0:
            for submenu_list in query(submenu_list_data, filters=(lambda submenu_list: submenu_list.nr == h_artikel.betriebsnr and submenu_list.zeit == hbuff.zeit)):
                created = True
                ct = "  -> " + to_string(submenu_list.bezeich)
                for i in range(1, length(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")
                output_list.str = output_list.str + chr_unicode(10)

                if submenu_list.request != "":
                    ct = ":::" + submenu_list.request
                    for i in range(1, len(ct) + 1):
                        output_list.str = output_list.str + \
                            to_string(substring(ct, i - 1, 1), "x(1)")
                    output_list.str = output_list.str + chr_unicode(10)
                submenu_list_data.remove(submenu_list)

            if not created:
                h_journal = get_cache(
                    H_journal, {"artnr": [(eq, hbuff.artnr)], "departement": [(eq, curr_dept)], "rechnr": [(eq, h_bill.rechnr)], "bill_datum": [(eq, hbuff.bill_datum)], "zeit": [(eq, hbuff.zeit)], "sysdate": [(eq, hbuff.sysdate)], "schankbuch": [(eq, recid_h_bill_line)]})

                if h_journal:
                    for h_mjourn in db_session.query(H_mjourn).filter(
                            (H_mjourn.departement == curr_dept) & 
                            (H_mjourn.h_artnr == h_journal.artnr) & 
                            (H_mjourn.rechnr == h_journal.rechnr) & 
                            (H_mjourn.bill_datum == h_journal.bill_datum) & 
                            (H_mjourn.sysdate == h_journal.sysdate) & 
                            (H_mjourn.zeit == h_journal.zeit)).order_by(H_mjourn._recid).all():

                        h_art = get_cache(
                            H_artikel, {"artnr": [(eq, h_mjourn.artnr)], "departement": [(eq, curr_dept)]})

                        if h_art:
                            if num_entries(h_mjourn.request, "|") > 1:
                                if entry(0, h_mjourn.request, "|") == to_string(recid_h_bill_line):
                                    created = True
                                    ct = " -> " + to_string(h_art.bezeich)
                                    for i in range(1, length(ct) + 1):
                                        output_list.str = output_list.str + \
                                            to_string(
                                                substring(ct, i - 1, 1), "x(1)")
                                    output_list.str = output_list.str + \
                                        chr_unicode(10)

                                    if entry(1, h_mjourn.request, "|") != "":
                                        ct = ":::" + \
                                            entry(1, h_mjourn.request, "|")
                                        for i in range(1, length(ct) + 1):
                                            output_list.str = output_list.str + \
                                                to_string(
                                                    substring(ct, i - 1, 1), "x(1)")
                                        output_list.str = output_list.str + \
                                            chr_unicode(10)

        if hbuff.anzahl < 0:
            printcod = get_cache(
                Printcod, {"emu": [(eq, printer.emu)], "code": [(eq, "redpr-")]})

            if printcod:
                ct = printcod.contcod
                for i in range(1, len(ct) + 1):
                    output_list.str = output_list.str + \
                        to_string(substring(ct, i - 1, 1), "x(1)")

        return generate_inner_output()

    def write_descript(str1: str, str2: str):
        nonlocal k, output_list_data, prev_zknr, do_it, recid_h_bill_line, disc_art1, disc_art2, disc_art3, numcat1, numcat2, lvcarea, h_artikel, h_bill_line, queasy, htparam, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn, printer
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy
        nonlocal submenu_list, output_list, abuff, hbuff, hbline, qsy
        nonlocal submenu_list_data, output_list_data

        ct = ""
        s1 = ""
        s2 = ""
        word = ""
        next_line: bool = False
        i: int = 0
        length1: int = 0
        for i in range(1, len(str1) + 1):
            output_list.str = output_list.str + \
                to_string(substring(ct, i - 1, 1), "x(1)")  

        if num_entries(str2, " ") == 1:
            if round(desclength / 2, 0) * 2 != desclength:
                length1 = desclength - 1
            else:
                length1 = desclength
            ct = substring(str2, 0, length1)
            for i in range(1, length(ct) + 1):
                output_list.str = output_list.str + \
                    to_string(substring(ct, i - 1, 1), "x(1)")
            output_list.str = output_list.str + chr_unicode(10)
            ct = ""
            for i in range(1, length(str1) + 1):
                ct = ct + " "
            ct = ct + substring(str2, length1 + 1 - 1)
            for i in range(1, length(ct) + 1):
                output_list.str = output_list.str + \
                    to_string(substring(ct, i - 1, 1), "x(1)")
            output_list.str = output_list.str + chr_unicode(10)

            return
        next_line = False
        for i in range(1, num_entries(str2, " ") + 1):
            word = entry(i - 1, str2, " ")

            if next_line:
                s2 = s2 + word + " "
            else:
                if len(s1 + word) <= desclength:
                    s1 = s1 + word + " "
                else:
                    next_line = True
                    s2 = s2 + word + " "
        ct = s1
        for i in range(1, length(ct) + 1):
            output_list.str = output_list.str + \
                to_string(substring(ct, i - 1, 1), "x(1)")
        output_list.str = output_list.str + chr_unicode(10)
        ct = ""
        for i in range(1, len(str1) + 1):
            ct = ct + " "
        ct = ct + s2
        for i in range(1, length(ct) + 1):
            output_list.str = output_list.str + \
                to_string(substring(ct, i - 1, 1), "x(1)")
        output_list.str = output_list.str + chr_unicode(10)

    # start - FDL: 6C4097
    def cut_it():
        nonlocal k, output_list_data, prev_zknr, do_it, recid_h_bill_line, disc_art1, disc_art2, disc_art3, numcat1, numcat2, lvcarea, h_artikel, h_bill_line, queasy, htparam, h_bill, wgrpdep, hoteldpt, kellner, printcod, h_journal, h_mjourn, printer
        nonlocal pvilanguage, close_it, reprint_it, h_bill_rechnr, curr_dept, prorder, desclength
        nonlocal abuff, hbuff, hbline, qsy
        nonlocal submenu_list, output_list, abuff, hbuff, hbline, qsy
        nonlocal submenu_list_data, output_list_data

        i: int = 0
        printer = get_cache(Printer, {"nr": [(eq, prorder)]})

        if printer:
            printcod = get_cache(
                Printcod, {"emu": [(eq, printer.emu)], "code": [(eq, "cut")]})

            if printcod:
                output_list.str = output_list.str + printcod.contcode
            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.str = output_list.str + chr_unicode(27) + "m"

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 252)]})
    numcat1 = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 562)]})
    numcat2 = htparam.finteger
    # end - FDL: 6C4097

    h_bill = get_cache(
        H_bill, {"rechnr": [(eq, h_bill_rechnr)], "departement": [(eq, curr_dept)]})

    if not h_bill:
        return generate_output()

    hbuff_obj_list = {}
    hbuff = H_bill_line()
    abuff = H_artikel()
    wgrpdep = Wgrpdep()
    for hbuff.bill_datum, hbuff.sysdate, hbuff.zeit, hbuff.artnr, hbuff.departement, hbuff.bezeich, hbuff.anzahl, hbuff._recid, hbuff.steuercode, abuff.betriebsnr, abuff._recid, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep._recid in db_session.query(Hbuff.bill_datum, Hbuff.sysdate, Hbuff.zeit, Hbuff.artnr, Hbuff.departement, Hbuff.bezeich, Hbuff.anzahl, Hbuff._recid, Hbuff.steuercode, Abuff.betriebsnr, Abuff._recid, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep._recid).join(Abuff, (Abuff.artnr == Hbuff.artnr) & (Abuff.departement == curr_dept) & (Abuff.artart == 0) & (Abuff.artnr != disc_art1) & (Abuff.artnr != disc_art2) & (Abuff.artnr != disc_art3)).join(Wgrpdep, (Wgrpdep.departement == curr_dept) & (Wgrpdep.zknr == Abuff.zwkum)).filter(
            (Hbuff.rechnr == h_bill_rechnr) & (Hbuff.departement == curr_dept)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr, Hbuff.artnr, Hbuff.sysdate, Hbuff.zeit).all():
        if hbuff_obj_list.get(hbuff._recid):
            continue
        else:
            hbuff_obj_list[hbuff._recid] = True

        h_artikel = get_cache(H_artikel, {"artnr": [(eq, hbuff.artnr)]})
        recid_h_bill_line = hbuff._recid
        do_it = reprint_it or (
            hbuff.steuercode >= 0 and hbuff.steuercode < 9999)

        if do_it:
            k = k + 1
            if k == 1:
                create_bon_header()
            prev_zknr = write_article(hbuff._recid, prev_zknr)

            if close_it:
                hbline = get_cache(
                    H_bill_line, {"_recid": [(eq, hbuff._recid)]})

                if hbline.steuercode == 0:
                    hbuff.steuercode = - prorder
                else:
                    hbline.steuercode = 9999

    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.str = to_string(chr_unicode(10) + chr_unicode(10))

    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.str = chr_unicode(10) + " " + chr_unicode(10)  # FDL: 6C4097
    cut_it()  # FDL: 6C4097

    return generate_output()
