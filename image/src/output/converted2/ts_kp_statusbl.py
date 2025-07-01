#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Hoteldpt, H_artikel, H_bill_line, H_bill, Queasy

def ts_kp_statusbl(pvilanguage:int, billno:int, depart:int):

    prepare_cache ([Hoteldpt, H_artikel, H_bill_line, H_bill, Queasy])

    msg_str = ""
    tlist_list = []
    lvcarea:string = "kp-status"
    lvdelimiter1:string = ""
    lvdelimiter2:string = ""
    loopi:int = 0
    loopn:int = 0
    curr_str:string = ""
    str1:string = ""
    dept_name:string = ""
    hoteldpt = h_artikel = h_bill_line = h_bill = queasy = None

    tlist = print_list = None

    tlist_list, Tlist = create_model("Tlist", {"artqty":int, "artname":string, "send_print":date, "send_tprint":bool, "printed":bool})
    print_list_list, Print_list = create_model("Print_list", {"artno":int, "dept_no":int, "art_desc":string, "art_desc2":string, "bill_no":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, tlist_list, lvcarea, lvdelimiter1, lvdelimiter2, loopi, loopn, curr_str, str1, dept_name, hoteldpt, h_artikel, h_bill_line, h_bill, queasy
        nonlocal pvilanguage, billno, depart


        nonlocal tlist, print_list
        nonlocal tlist_list, print_list_list

        return {"msg_str": msg_str, "tlist": tlist_list}

    lvdelimiter1 = chr_unicode(10)
    lvdelimiter2 = ":::"

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, depart)]})

    if hoteldpt:
        dept_name = hoteldpt.depart

    h_bill_line_obj_list = {}
    h_bill_line = H_bill_line()
    h_artikel = H_artikel()
    for h_bill_line.rechnr, h_bill_line.departement, h_bill_line.artnr, h_bill_line.bezeich, h_bill_line._recid, h_artikel.bezeich, h_artikel._recid in db_session.query(H_bill_line.rechnr, H_bill_line.departement, H_bill_line.artnr, H_bill_line.bezeich, H_bill_line._recid, H_artikel.bezeich, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == depart) & (H_artikel.artart == 0)).filter(
             (H_bill_line.rechnr == billno) & (H_bill_line.departement == depart)).order_by(H_bill_line._recid).all():
        if h_bill_line_obj_list.get(h_bill_line._recid):
            continue
        else:
            h_bill_line_obj_list[h_bill_line._recid] = True

        print_list = query(print_list_list, filters=(lambda print_list: print_list.bill_no == h_bill_line.rechnr and print_list.dept_no == h_bill_line.departement and print_list.artno == h_bill_line.artnr and print_list.art_desc == h_artikel.bezeich and print_list.art_desc2 == h_bill_line.bezeich), first=True)

        if not print_list:
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.artno = h_bill_line.artnr
            print_list.dept_no = h_bill_line.departement
            print_list.art_desc = h_artikel.bezeich
            print_list.bill_no = h_bill_line.rechnr

            if h_artikel.bezaendern:
                print_list.art_desc2 = h_bill_line.bezeich

    h_bill = get_cache (H_bill, {"rechnr": [(eq, billno)],"departement": [(eq, depart)],"flag": [(eq, 0)]})

    if h_bill:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 3) & (matches(Queasy.char3,("*" + to_string(h_bill.rechnr) + "*"))) & (matches(Queasy.char3,("*" + dept_name + "*")))).order_by(Queasy._recid).all():
            for loopi in range(1,num_entries(queasy.char3, lvdelimiter1)  + 1) :
                curr_str = entry(loopi - 1, queasy.char3, lvdelimiter1)

                if curr_str != "":

                    print_list = query(print_list_list, filters=(lambda print_list:(matches(print_list.art_desc,r"*" + trim(substring(curr_str, 5)) + r"*)) or matches(print_list.art_desc2,r"*" + trim(substring(curr_str, 5)) + r"*")) and print_list.dept_no == h_bill.departement), first=True

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