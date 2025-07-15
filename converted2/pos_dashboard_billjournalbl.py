#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Queasy, Hoteldpt, H_journal, H_artikel, H_bill, Res_line, Guest

def pos_dashboard_billjournalbl(from_date:date, to_date:date, from_dept:int, to_dept:int):

    prepare_cache ([Htparam, Queasy, Hoteldpt, H_journal, H_artikel, H_bill, Res_line, Guest])

    journal_list_data = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    htparam = queasy = hoteldpt = h_journal = h_artikel = h_bill = res_line = guest = None

    journal_list = t_list = None

    journal_list_data, Journal_list = create_model("Journal_list", {"bill_date":date, "table_no":int, "bill_no":int, "order_no":int, "article_no":int, "article_name":string, "qty":int, "amount":Decimal, "payment":Decimal, "dept_name":string, "id":string, "bill_time":string, "guest_name":string, "room_no":string})
    t_list_data, T_list = create_model("T_list", {"bill_date":date, "dept_no":int, "rechnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal journal_list_data, disc_art1, disc_art2, disc_art3, htparam, queasy, hoteldpt, h_journal, h_artikel, h_bill, res_line, guest
        nonlocal from_date, to_date, from_dept, to_dept


        nonlocal journal_list, t_list
        nonlocal journal_list_data, t_list_data

        return {"journal-list": journal_list_data}

    def journal_list():

        nonlocal journal_list_data, disc_art1, disc_art2, disc_art3, htparam, queasy, hoteldpt, h_journal, h_artikel, h_bill, res_line, guest
        nonlocal from_date, to_date, from_dept, to_dept


        nonlocal journal_list, t_list
        nonlocal journal_list_data, t_list_data

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        sub_tot1:Decimal = to_decimal("0.0")
        tot1:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        curr_guest:string = ""
        curr_room:string = ""
        validate_rechnr:int = 0
        mess_str:string = ""
        i_str:int = 0
        mess_token:string = ""
        mess_keyword:string = ""
        mess_value:string = ""
        dept_i:int = 0
        journal_list_data.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 225) & (Queasy.char1 == ("orderbill").lower()) & (num_entries(Queasy.char2, "|") > 7) & (matches(entry(7, Queasy.char2, "|"),"*BL=*"))).order_by(Queasy._recid).all():
            mess_str = queasy.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, "=")
                mess_value = entry(1, mess_token, "=")

                if mess_keyword.lower()  == ("BL").lower() :
                    validate_rechnr = to_int(mess_value)

                if validate_rechnr != 0:
                    break

            if validate_rechnr != 0:

                t_list = query(t_list_data, filters=(lambda t_list: t_list.rechnr == validate_rechnr and t_list.bill_date == queasy.date1 and t_list.dept_no == queasy.number1), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.bill_date = queasy.date1
                    t_list.dept_no = queasy.number1
                    t_list.rechnr = validate_rechnr


                validate_rechnr = 0

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            sub_tot =  to_decimal("0")
            sub_tot1 =  to_decimal("0")
            it_exist = False
            qty = 0

            h_journal_obj_list = {}
            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
                t_list = query(t_list_data, (lambda t_list: t_list.rechnr == h_journal.rechnr and t_list.dept_no == h_journal.departement), first=True)
                if not t_list:
                    continue

                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)]})
                it_exist = True
                curr_guest = ""
                curr_room = ""

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                if h_bill:

                    if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                        res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                        if res_line:
                            curr_guest = res_line.name
                            curr_room = res_line.zinr

                    elif h_bill.resnr > 0:

                        guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                        if guest:
                            curr_guest = guest.name + "," + guest.vorname1
                            curr_room = ""

                    elif h_bill.resnr == 0:
                        curr_guest = h_bill.bilname
                        curr_room = ""

                if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art3) and h_journal.betrag == 0:
                    pass
                else:
                    journal_list = Journal_list()
                    journal_list_data.append(journal_list)

                    journal_list.guest_name = curr_guest
                    journal_list.bill_date = h_journal.bill_datum
                    journal_list.table_no = h_journal.tischnr
                    journal_list.bill_no = h_journal.rechnr
                    journal_list.article_no = h_journal.artnr
                    journal_list.article_name = h_journal.bezeich
                    journal_list.dept_name = hoteldpt.depart
                    journal_list.qty = h_journal.anzahl

                    if h_artikel and h_artikel.artart == 0:
                        journal_list.amount =  to_decimal(h_journal.betrag)
                        journal_list.payment =  to_decimal("0")
                        sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                        tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                    elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 9) == ("To Table ").lower() :
                        journal_list.amount =  to_decimal(h_journal.betrag)
                        journal_list.payment =  to_decimal("0")
                        sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                        tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                    elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 11) == ("From Table ").lower() :
                        journal_list.amount =  to_decimal(h_journal.betrag)
                        journal_list.payment =  to_decimal("0")
                        sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                        tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                    else:
                        journal_list.amount =  to_decimal("0")
                        journal_list.payment =  to_decimal(h_journal.betrag)
                        sub_tot1 =  to_decimal(sub_tot1) + to_decimal(h_journal.betrag)
                        tot1 =  to_decimal(tot1) + to_decimal(h_journal.betrag)
                    journal_list.id = to_string(h_journal.kellner_nr, "9999")
                    journal_list.bill_time = to_string(h_journal.zeit, "HH:MM:SS")
                    journal_list.room_no = curr_room
                    qty = qty + h_journal.anzahl

            if it_exist:
                journal_list = Journal_list()
                journal_list_data.append(journal_list)

                journal_list.article_name = "T O T A L"
                journal_list.qty = qty
                journal_list.amount =  to_decimal(sub_tot)
                journal_list.payment =  to_decimal(sub_tot1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger
    journal_list()

    return generate_output()