from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Hoteldpt, H_artikel, H_bill_line, H_bill, Queasy

def ts_kp_statusbl(pvilanguage:int, billno:int, depart:int):
    msg_str = ""
    tlist_list = []
    lvcarea:str = "kp_status"
    lvdelimiter1:str = ""
    lvdelimiter2:str = ""
    loopi:int = 0
    loopn:int = 0
    curr_str:str = ""
    str1:str = ""
    dept_name:str = ""
    hoteldpt = h_artikel = h_bill_line = h_bill = queasy = None

    tlist = print_list = None

    tlist_list, Tlist = create_model("Tlist", {"artqty":int, "artname":str, "send_print":date, "send_tprint":bool, "printed":bool})
    print_list_list, Print_list = create_model("Print_list", {"artno":int, "dept_no":int, "art_desc":str, "art_desc2":str, "bill_no":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, tlist_list, lvcarea, lvdelimiter1, lvdelimiter2, loopi, loopn, curr_str, str1, dept_name, hoteldpt, h_artikel, h_bill_line, h_bill, queasy


        nonlocal tlist, print_list
        nonlocal tlist_list, print_list_list
        return {"msg_str": msg_str, "tlist": tlist_list}

    lvdelimiter1 = chr(10)
    lvdelimiter2 = ":::"

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == depart)).first()

    if hoteldpt:
        dept_name = hoteldpt.depart

    h_bill_line_obj_list = []
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == depart) &  (H_artikel.artart == 0)).filter(
            (H_bill_line.rechnr == billno) &  (H_bill_line.departement == depart)).all():
        if h_bill_line._recid in h_bill_line_obj_list:
            continue
        else:
            h_bill_line_obj_list.append(h_bill_line._recid)

        print_list = query(print_list_list, filters=(lambda print_list :print_list.bill_no == h_bill_line.rechnr and print_list.dept_no == h_bill_line.departement and print_list.artno == h_bill_line.artnr and print_list.art_desc == h_artikel.bezeich and print_list.art_desc2 == h_bill_line.bezeich), first=True)

        if not print_list:
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.artno = h_bill_line.artnr
            print_list.dept_no = h_bill_line.departement
            print_list.art_desc = h_artikel.bezeich
            print_list.bill_no = h_bill_line.rechnr

            if h_artikel.bezaendern:
                print_list.art_desc2 = h_bill_line.bezeich

    h_bill = db_session.query(H_bill).filter(
            (H_bill.rechnr == billno) &  (H_bill.departement == depart) &  (H_bill.flag == 0)).first()

    if h_bill:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 3) &  (Queasy.char3.op("~")(".*" + to_string(h_bill.rechnr) + "*")) &  (Queasy.char3.op("~")(".*" + dept_name + ".*"))).all():
            for loopi in range(1,num_entries(queasy.char3, lvdelimiter1)  + 1) :
                curr_str = entry(loopi - 1, queasy.char3, lvdelimiter1)

                if curr_str != "":

                    print_list = query(print_list_list, filters=(lambda print_list :(re.match(".*" + trim(substring(curr_str, 5,print_list.art_desc)) + "*") or re.match(".*" + trim(substring(curr_str, 5,print_list.art_desc2)) + "*")) and print_list.dept_no == h_bill.departement), first=True)

                    if print_list:

                        if trim(substring(curr_str, 5)) != "":
                            tlist = Tlist()
                            tlist_list.append(tlist)

                            tlist.artqty = to_int(substring(curr_str, 0, 5))
                            tlist.artname = trim(substring(curr_str, 5))
                            tlist.send_print = queasy.date1
                            tlist.send_tprint = not queasy.logi1
                            tlist.printed = not queasy.logi2

    elif not h_bill:
        msg_str = translateExtended ("No record Available", lvcarea, "")

    return generate_output()