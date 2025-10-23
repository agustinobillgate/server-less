#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false
"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning
            - changed to_int() to int()
            - convert data type to return entry()
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions_py.htpdate import htpdate
from functions_py.htpchar import htpchar
from models import Printer, Queasy, Tisch, Hoteldpt, H_bill, Res_line

def kitchen_printerlnl_2bl(print_str:string, kplnl_number:string):

    prepare_cache ([Tisch, Hoteldpt, H_bill, Res_line])

    queasy_list_data = []
    reprint_qlist_data = []
    t_printer_data = []
    printer_path:str
    temp_billno:str
    billno = 0
    roomno = ""
    gname = ""
    room_str = ""
    pos_name:str
    param_lnl = ""
    bill_date:date
    k:int = 0
    i:int = 0
    n:int = 0
    lvdelimiter1:string = ""
    lvdelimiter2:string = ""
    curr_str:string = ""
    printer_loc:string = ""
    printer_char:string = ""
    outlet_name:string = ""
    tableno:int = 0
    pax:int = 0
    dept_no:int = 0
    count_j:int = 0
    count_kp:int = 0
    found_kp:bool = False
    printer = queasy = tisch = hoteldpt = h_bill = res_line = None

    queasy_list = reprint_qlist = t_printer = kp_list = qbuff = buffqueasy = qsybuff = qsy = None

    queasy_list_data, Queasy_list = create_model(
        "Queasy_list", {
            "char1":string, 
            "printer_path":string, 
            "char2":string, 
            "number2":int, 
            "rec_id":int, 
            "queue_nr":Decimal, 
            "billno":int, 
            "roomno":string, 
            "gname":string, 
            "pos_name":string, 
            "table_desc":string, 
            "od_taker":string, 
            "printer_num":int, 
            "bill_number":int, 
            "dept_number":int
            }
        )
    reprint_qlist_data, Reprint_qlist = create_model(
        "Reprint_qlist", {
            "char1":string, 
            "printer_path":string, 
            "char2":string, 
            "number2":int, 
            "rec_id":int, 
            "queue_nr":Decimal, 
            "billno":int, 
            "roomno":string, 
            "gname":string, 
            "pos_name":string, 
            "table_desc":string, 
            "od_taker":string, 
            "printer_num":int, 
            "bill_number":int, 
            "dept_number":int
            }
        )
    t_printer_data, T_printer = create_model_like(Printer)
    kp_list_data, Kp_list = create_model(
        "Kp_list", {
            "kp_number":int})

    Qbuff = create_buffer(
        "Qbuff",Queasy)
    Buffqueasy = create_buffer(
        "Buffqueasy",Queasy)
    Qsybuff = create_buffer(
        "Qsybuff",Queasy)
    Qsy = create_buffer(
        "Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, printer_path, temp_billno, billno, roomno, gname, room_str, pos_name, param_lnl, bill_date, k, i, n, lvdelimiter1, lvdelimiter2, curr_str, printer_loc, printer_char, outlet_name, tableno, pax, dept_no, count_j, count_kp, found_kp, printer, queasy, tisch, hoteldpt, h_bill, res_line
        nonlocal print_str, kplnl_number
        nonlocal qbuff, buffqueasy, qsybuff, qsy


        nonlocal queasy_list, reprint_qlist, t_printer, kp_list, qbuff, buffqueasy, qsybuff, qsy
        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, kp_list_data

        return {
            "queasy-list": queasy_list_data, 
            "reprint-qlist": reprint_qlist_data, 
            "t-printer": t_printer_data, 
            "printer_path": printer_path, 
            "temp_billno": temp_billno, 
            "billno": billno, 
            "roomno": roomno, 
            "gname": gname, 
            "room_str": room_str, 
            "pos_name": pos_name, 
            "param_lnl": param_lnl
        }

    def print_request(ch1:string, req_str:string):

        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, printer_path, temp_billno, billno, roomno, gname, room_str, pos_name, param_lnl, bill_date, k, lvdelimiter1, lvdelimiter2, curr_str, printer_loc, printer_char, outlet_name, tableno, pax, dept_no, count_j, count_kp, found_kp, printer, queasy, tisch, hoteldpt, h_bill, res_line
        nonlocal print_str, kplnl_number
        nonlocal qbuff, buffqueasy, qsybuff, qsy


        nonlocal queasy_list, reprint_qlist, t_printer, kp_list, qbuff, buffqueasy, qsybuff, qsy
        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, kp_list_data

        ch:string
        i:int = 0
        j:int = 0
        n:int = 1
        n = num_entries(req_str, ";")  # type: ignore return int dari num entries
        for i in range(1,n + 1) :
            ch = ch1 + str(entry(i - 1, req_str, ";")) 
            for j in range(1,length(ch)  + 1) :  # type: ignore value ch unknown
                if asc(substring(ch, j - 1, 1)) <= 127:
                    queasy_list.char1 = queasy_list.char1 + substring(ch, j - 1, 1) # type: ignore queasy_list belum tercreate
                else:
                    queasy_list.char1 = queasy_list.char1 + substring(ch, j - 1, 2) # type: ignore queasy_list belum tercreate
                    j = j + 1
            queasy_list.char1 = queasy_list.char1 + "�" # type: ignore queasy_list belum tercreate


    def re_print_request(ch1:string, req_str:string):

        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, printer_path, temp_billno, billno, roomno, gname, room_str, pos_name, param_lnl, bill_date, k, lvdelimiter1, lvdelimiter2, curr_str, printer_loc, printer_char, outlet_name, tableno, pax, dept_no, count_j, count_kp, found_kp, printer, queasy, tisch, hoteldpt, h_bill, res_line
        nonlocal print_str, kplnl_number
        nonlocal qbuff, buffqueasy, qsybuff, qsy

        nonlocal queasy_list, reprint_qlist, t_printer, kp_list, qbuff, buffqueasy, qsybuff, qsy
        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, kp_list_data

        ch:string = ""
        i:int = 0
        j:int = 0
        n:int = 1
        n = num_entries(req_str, ";") # type: ignore return int dari num entries
        for i in range(1,n + 1) :
            ch = ch1 + (entry(i - 1, req_str, ";"))  # type: ignore return string value dari entry + ch1
            for j in range(1,length(ch)  + 1) : # type: ignore value ch unknown
                if asc(substring(ch, j - 1, 1)) <= 127:
                    reprint_qlist.char1 = reprint_qlist.char1 + substring(ch, j - 1, 1) # type: ignore queasy_list belum tercreate
                else:
                    reprint_qlist.char1 = reprint_qlist.char1 + substring(ch, j - 1, 2) # type: ignore queasy_list belum tercreate
                    j = j + 1
            reprint_qlist.char1 = reprint_qlist.char1 + "�" # type: ignore queasy_list belum tercreate


    def assign_more_info():

        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, printer_path, temp_billno, billno, roomno, gname, room_str, pos_name, param_lnl, bill_date, k, i, n, lvdelimiter1, lvdelimiter2, curr_str, printer_loc, printer_char, outlet_name, tableno, dept_no, count_j, count_kp, found_kp, printer, queasy, tisch, hoteldpt, h_bill, res_line
        nonlocal print_str, kplnl_number
        nonlocal qbuff, buffqueasy, qsybuff, qsy


        nonlocal queasy_list, reprint_qlist, t_printer, kp_list, qbuff, buffqueasy, qsybuff, qsy
        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, kp_list_data

        counter:int = 0
        pax:int = 0
        counter2:int = 0
        temp_char:string 
        queuing:string = ""
        outlet_name = entry(0, queasy_list.char1, "�")  # type: ignore model queasy list belum tercreate
        outlet_name = replace_str(outlet_name, "�", " ")
        pos_name = entry(0, queasy_list.char1, "�")  # type: ignore model queasy list belum tercreate
        queasy_list.char1 = entry(0, queasy_list.char1, "�", "") # type: ignore model queasy list belum tercreate
        queasy_list.pos_name = pos_name # type: ignore model queasy list belum tercreate

        hoteldpt = db_session.query(Hoteldpt).filter(
            (trim(Hoteldpt.depart) == trim(outlet_name))).first()

        if hoteldpt:
            dept_no = hoteldpt.num
        for counter in range(1,num_entries(queasy_list.char1, "�")  + 1): # type: ignore model queasy list belum tercreate
            temp_char = entry(counter - 1, queasy_list.char1, "�") # type: ignore model queasy list belum tercreate

            if matches(temp_char,r"*billno*"):
                temp_billno = entry(counter - 1, queasy_list.char1, "�") # type: ignore model queasy list belum tercreate
                billno = to_int(entry(1, temp_billno, " "))
                queasy_list.char1 = entry(counter - 1, queasy_list.char1, "�", "") # type: ignore model queasy list belum tercreate
                queasy_list.billno = billno # type: ignore model queasy list belum tercreate

            if matches(temp_char,r"*Table*"):
                for counter2 in range(1,num_entries(temp_char, " ")  + 1):   # type: ignore return model sqlalchemy
                    if matches(entry(counter2 - 1, temp_char, " "),r"*Table*"):
                        tableno = int(entry(counter2 + 1 - 1, temp_char, " "))  # type: ignore return model sqlalchemy

                    if matches(entry(counter2 - 1, temp_char, " "),r"*pax*"):
                        pax = int(entry(counter2 + 1 - 1, temp_char, " "))  # type: ignore return model sqlalchemy

        h_bill = get_cache (H_bill, {
            "rechnr": [(eq, billno)],
            "departement": [(eq, dept_no)]}
        )

        if h_bill:
            tableno = int(h_bill.tischnr)
            pax = int(h_bill.belegung)

        h_bill = get_cache (H_bill, {
            "rechnr": [(eq, billno)],
            "tischnr": [(eq, tableno)],
            "belegung": [(eq, pax)]}
        )

        if h_bill:

            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    room_str = "Room"
                    roomno = res_line.zinr + " - "
                    queasy_list.roomno = roomno  # type: ignore model queasy list belum tercreate


                else:
                    # roomno = " "
                    # room_str = " "
                    roomno = None
                    room_str = None
                    queasy_list.roomno = roomno  # type: ignore model queasy list belum tercreate

            # if h_bill.bilname == None:
            if not h_bill.bilname:
                gname = None

            else:
                gname = h_bill.bilname
                
            queasy_list.gname = gname  # type: ignore model queasy list belum tercreate

            qsy = db_session.query(Qsy).filter((Qsy.key == 10) & (Qsy.number1 == h_bill.betriebsnr)).first()

            if qsy:
                queasy_list.od_taker = qsy.char1  # type: ignore model queasy list belum tercreate

        buffqueasy = db_session.query(Buffqueasy).filter((Buffqueasy.key == 191) & (Buffqueasy.number1 == billno)).first()

        if buffqueasy:
            pos_name = pos_name + "$" + str(to_string(buffqueasy.number2, ">>>,>>>9"))


    def re_assign_more_info():

        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, printer_path, temp_billno, billno, roomno, gname, room_str, pos_name, param_lnl, bill_date, k, i, n, lvdelimiter1, lvdelimiter2, curr_str, printer_loc, printer_char, outlet_name, tableno, dept_no, count_j, count_kp, found_kp, printer, queasy, tisch, hoteldpt, h_bill, res_line
        nonlocal print_str, kplnl_number
        nonlocal qbuff, buffqueasy, qsybuff, qsy


        nonlocal queasy_list, reprint_qlist, t_printer, kp_list, qbuff, buffqueasy, qsybuff, qsy
        nonlocal queasy_list_data, reprint_qlist_data, t_printer_data, kp_list_data

        counter:int = 0
        pax:int = 0
        counter2:int = 0
        temp_char:string 
        queuing:string = ""
        outlet_name = entry(0, reprint_qlist.char1, "�")  # type: ignore model reprint_qlist belum tercreate
        outlet_name = replace_str(outlet_name, "�", " ") 
        pos_name = entry(0, reprint_qlist.char1, "�")  # type: ignore model reprint qlist belum tercreate
        reprint_qlist.char1 = entry(0, reprint_qlist.char1, "�", "")  # type: ignore model reprint qlist belum tercreate
        reprint_qlist.pos_name = pos_name  # type: ignore model reprint qlist belum tercreate

        hoteldpt = db_session.query(Hoteldpt).filter(
        (trim(Hoteldpt.depart) == trim(outlet_name))).first()

        if hoteldpt:
            dept_no = hoteldpt.num
        for counter in range(1,num_entries(reprint_qlist.char1, "�")  + 1):  # type: ignore return model sqlalchemy
            temp_char = str(entry(counter - 1, reprint_qlist.char1, "�") )   # type: ignore model reprint qlist belum tercreate

            if matches(temp_char,r"*billno*"):
                temp_billno = entry(counter - 1, reprint_qlist.char1, "�")  # type: ignore model reprint qlist belum tercreate
                billno = to_int(entry(1, temp_billno, " "))
                reprint_qlist.char1 = entry(counter - 1, reprint_qlist.char1, "�", "")  # type: ignore model reprint qlist belum tercreate
                reprint_qlist.billno = billno  # type: ignore model reprint qlist belum tercreate

            if matches(temp_char,r"*Table*"):
                for counter2 in range(1,num_entries(temp_char, " ")  + 1):  # type: ignore return model sqlalchemy
                    if matches(entry(counter2 - 1, temp_char, " "),r"*Table*"):
                        tableno = int(entry(counter2 + 1 - 1, temp_char, " "))   # type: ignore return model sqlalchemy

                    if matches(entry(counter2 - 1, temp_char, " "),r"*pax*"):
                        pax = int(entry(counter2 + 1 - 1, temp_char, " "))  # type: ignore return model sqlalchemy

        h_bill = get_cache (H_bill, {
            "rechnr": [(eq, billno)],
            "departement": [(eq, dept_no)]}
        )

        if h_bill:
            tableno = int(h_bill.tischnr)
            pax = int(h_bill.belegung)

        h_bill = get_cache (H_bill, {
            "rechnr": [(eq, billno)],
            "tischnr": [(eq, tableno)],
            "belegung": [(eq, pax)]})

        if h_bill:

            if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    room_str = "Room"
                    roomno = res_line.zinr + " - "
                    reprint_qlist.roomno = roomno  # type: ignore model reprint qlist belum tercreate

                else:
                    roomno = None
                    room_str = None
                    reprint_qlist.roomno = roomno  # type: ignore model reprint qlist belum tercreate

            if not h_bill.bilname :
                gname = None

            else:
                gname = h_bill.bilname
                
            reprint_qlist.gname = gname  # type: ignore model reprint_qlist belum tercreate

            qsy = db_session.query(Qsy).filter(
                (Qsy.key == 10) & (Qsy.number1 == h_bill.betriebsnr)).first()

            if qsy:
                reprint_qlist.od_taker = qsy.char1  # type: ignore model reprint qlist belum tercreate

        buffqueasy = db_session.query(Buffqueasy).filter(
            (Buffqueasy.key == 191) & (Buffqueasy.number1 == billno)).first()

        if buffqueasy:
            pos_name = pos_name + "$" + str(to_string(buffqueasy.number2, ">>>,>>>9"))


    lvdelimiter1 = chr_unicode(10)
    lvdelimiter2 = ":::"

    if num_entries(print_str, ";") > 1:  # type: ignore return model sqlalchemy
        printer_loc = str(entry(0, print_str, ";"))
        printer_char = str(entry(1, print_str, ";"))


    else:
        printer_loc = str(entry(0, print_str, ";"))
    bill_date = get_output(htpdate(110))  # type: ignore return unknown dict/ tuple
    param_lnl = get_output(htpchar(417))
    t_printer_data.clear()

    for printer in db_session.query(Printer).filter(
        (Printer.bondrucker)).order_by(Printer._recid).all():
        t_printer = T_printer()
        t_printer_data.append(t_printer)

        buffer_copy(printer, t_printer)

    if kplnl_number and num_entries(kplnl_number, "|") > 1:  # type: ignore return num_entries model sqlalchemy
        kp_list_data.clear()
        for count_kp in range(1,num_entries(kplnl_number, "|")  + 1) :  # type: ignore return model sqlalchemy
            kp_list = Kp_list()
            kp_list_data.append(kp_list)

            kp_list.kp_number = int(entry(count_kp - 1, kplnl_number, "|"))   # type: ignore return model sqlalchemy, model kp list belum tercreate

    elif kplnl_number and num_entries(kplnl_number, "|") <= 1:  # type: ignore return model sqlalchemy
        kp_list_data.clear()
        kp_list = Kp_list()
        kp_list_data.append(kp_list)

        kp_list.kp_number = int(kplnl_number)  # type: ignore model kp list belum tercreate

    qbuff = db_session.query(Qbuff).filter(
        (Qbuff.key == 3) & (Qbuff.number1 != 0) & (Qbuff.logi2) & ((Qbuff.char1 != "") | (Qbuff.char3 != "")) & ((Qbuff.date1 >= bill_date)) & (Qbuff.char2 == (printer_loc).lower())).first()
    while qbuff:

        if kplnl_number:
            found_kp = False

            kp_list = query(kp_list_data, filters=(lambda kp_list: kp_list.kp_number == qbuff.number1), first=True)  # type: ignore model qbuff belum tercreate

            if kp_list:
                found_kp = True
        else:
            found_kp = True

        if found_kp:
            count_j = count_j + 1

            if count_j > 10:
                break

            queasy = get_cache (Queasy, {
                "_recid": [(eq, qbuff._recid)]})

            if queasy:
                queasy_list = Queasy_list()
                queasy_list_data.append(queasy_list)

                queasy_list.rec_id = queasy._recid  # type: ignore model queasy list belum tercreate
                queasy_list.bill_number = queasy.deci2 # type: ignore model queasy list belum tercreate
                queasy_list.dept_number = queasy.deci3 # type: ignore model queasy list belum tercreate

                printer = get_cache (Printer, {
                    "nr": [(eq, queasy.number1)]})
                queasy_list.printer_num = printer.nr # type: ignore model queasy list belum tercreate
                printer_path = printer.path
                queasy_list.printer_path = printer_path # type: ignore model queasy list belum tercreate
                k = queasy.number1
                for i in range(1,length(queasy.char1) + 1) :  # type: ignore return column element[Any]

                    if asc(substring(queasy.char1, i - 1, 1)) <= 127:
                        queasy_list.char1 = queasy_list.char1 + substring(queasy.char1, i - 1, 1)  # type: ignore model queasy list belum tercreate
                    else:
                        queasy_list.char1 = queasy_list.char1 + substring(queasy.char1, i - 1, 2) # type: ignore model queasy list belum tercreate
                        i = i + 1
                for i in range(1,num_entries(queasy.char3, lvdelimiter1) + 1) : # type: ignore model queasy list belum tercreate
                    curr_str = str(entry(i - 1, queasy.char3, lvdelimiter1)) 

                    if not matches(curr_str,r"*:::*"):
                        for n in range(1,length(curr_str) + 1) : # type: ignore return column element[Any]

                            if asc(substring(curr_str, n - 1, 1)) <= 127:
                                queasy_list.char1 = queasy_list.char1 + substring(curr_str, n - 1, 1)  # type: ignore model queasy list belum tercreate
                            else:
                                queasy_list.char1 = queasy_list.char1 + substring(curr_str, n - 1, 2)  # type: ignore model queasy list belum tercreate
                                n = n + 1
                        queasy_list.char1 = queasy_list.char1 + "�"  # type: ignore model queasy list belum tercreate
                    else:
                        print_request(lvdelimiter2, str(substring(curr_str, 3)))
                queasy_list.char2 = queasy.char2 # type: ignore model queasy list belum tercreate
                queasy_list.number2 = queasy.number2 # type: ignore model queasy list belum tercreate
                queasy_list.queue_nr =  to_decimal(queasy.deci1) # type: ignore model queasy list belum tercreate

                assign_more_info()

                tisch = get_cache (Tisch, {
                    "tischnr": [(eq, tableno)],
                    "departement": [(eq, dept_no)]})

                if tisch:
                    queasy_list.table_desc = tisch.bezeich  # type: ignore model queasy list belum tercreate

                # if printer_char.lower() != "" and printer_char.lower()  == ("Design").lower():
                if printer_char.lower() and printer_char.lower()  == "design":
                    pass
                else:
                    queasy.logi1 = True

        curr_recid = qbuff._recid
        qbuff = db_session.query(Qbuff).filter(
            (Qbuff.key == 3) & (Qbuff.number1 != 0) & (Qbuff.logi2) & ((Qbuff.char1 != "") | (Qbuff.char3 != "")) & ((Qbuff.date1 >= bill_date)) & (Qbuff.char2 == (printer_loc).lower()) & (Qbuff._recid > curr_recid)).first()

    qsybuff = db_session.query(Qsybuff).filter(
        (Qsybuff.key == 233) & (Qsybuff.number1 != 0) & (Qsybuff.logi2) & ((Qsybuff.char1 != "") | (Qsybuff.char3 != "")) & ((Qsybuff.date1 >= bill_date)) & (Qsybuff.char2 == (printer_loc).lower())).first()
    while qsybuff:

        if kplnl_number:
            found_kp = False

            kp_list = query(kp_list_data, filters=(lambda kp_list: kp_list.kp_number == qsybuff.number1), first=True)  # type: ignore model qsybuff belum tercreate

            if kp_list:
                found_kp = True
        else:
            found_kp = True

        if found_kp:

            queasy = get_cache (Queasy, {"_recid": [(eq, qsybuff._recid)]})

            if queasy:
                reprint_qlist = Reprint_qlist()
                reprint_qlist_data.append(reprint_qlist)

                reprint_qlist.rec_id = queasy._recid  # type: ignore model reprint qlist belum tercreate
                reprint_qlist.bill_number = queasy.deci2  # type: ignore model reprint qlist belum tercreate
                reprint_qlist.dept_number = queasy.deci3 # type: ignore model reprint qlist belum tercreate

                printer = get_cache (Printer, {
                    "nr": [(eq, queasy.number1)]})
                reprint_qlist.printer_num = printer.nr # type: ignore model reprint qlist belum tercreate
                printer_path = printer.path
                reprint_qlist.printer_path = printer_path # type: ignore model reprint qlist belum tercreate
                k = queasy.number1
                for i in range(1,length(queasy.char1)  + 1) :    # type: ignore return ColumnElement[Any]

                    if asc(substring(queasy.char1, i - 1, 1)) <= 127:
                        reprint_qlist.char1 = reprint_qlist.char1 + substring(queasy.char1, i - 1, 1) # type: ignore model reprint qlist belum tercreate
                    else:
                        reprint_qlist.char1 = reprint_qlist.char1 + substring(queasy.char1, i - 1, 2) # type: ignore model reprint qlist belum tercreate
                        i = i + 1
                for i in range(1,num_entries(queasy.char3, lvdelimiter1)  + 1) : # type: ignore return ColumnElement[Any]
                    curr_str = str(entry(i - 1, queasy.char3, lvdelimiter1))

                    if not matches(curr_str,r"*:::*"):
                        for n in range(1,length(curr_str)  + 1) : # type: ignore return ColumnElement[Any]

                            if asc(substring(curr_str, n - 1, 1)) <= 127:
                                reprint_qlist.char1 = reprint_qlist.char1 + substring(curr_str, n - 1, 1) # type: ignore model reprint qlist belum tercreate
                            else:
                                reprint_qlist.char1 = reprint_qlist.char1 + substring(curr_str, n - 1, 2) # type: ignore model reprint qlist belum tercreate
                                n = n + 1
                        reprint_qlist.char1 = reprint_qlist.char1 + "�" # type: ignore model reprint qlist belum tercreate
                    else:
                        re_print_request(lvdelimiter2, str(substring(curr_str, 3)))
                reprint_qlist.char2 = queasy.char2 # type: ignore model reprint qlist belum tercreate
                reprint_qlist.number2 = queasy.number2 # type: ignore model reprint qlist belum tercreate
                reprint_qlist.queue_nr =  to_decimal(queasy.deci1) # type: ignore model reprint qlist belum tercreate


                re_assign_more_info()

                tisch = get_cache (Tisch, {
                    "tischnr": [(eq, tableno)],
                    "departement": [(eq, dept_no)]})

                if tisch:
                    reprint_qlist.table_desc = tisch.bezeich # type: ignore model reprint qlist belum tercreate

                if printer_char.lower() and printer_char.lower()  == "design":
                    pass
                else:
                    queasy.logi1 = True

        curr_recid = qsybuff._recid
        qsybuff = db_session.query(Qsybuff).filter(
            (Qsybuff.key == 233) & (Qsybuff.number1 != 0) & (Qsybuff.logi2) & ((Qsybuff.char1 != "") | (Qsybuff.char3 != "")) & ((Qsybuff.date1 >= bill_date)) & (Qsybuff.char2 == (printer_loc).lower()) & (Qsybuff._recid > curr_recid)).first()

    return generate_output()