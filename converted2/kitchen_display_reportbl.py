#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, H_bill_line, H_artikel, H_journal, Hoteldpt, Printer

def kitchen_display_reportbl(from_date:date, to_date:date, dept:int, kds_number:int):

    prepare_cache ([Queasy, H_bill_line, H_artikel, H_journal, Hoteldpt, Printer])

    kds_data = []
    count_i:int = 0
    nr:int = 0
    spreq:string = ""
    starttime:int = 0
    endtime:int = 0
    inttime:int = 0
    deptname:string = ""
    currdate:date = None
    orig_char:string = ""
    queasy = h_bill_line = h_artikel = h_journal = hoteldpt = printer = None

    kds = q_kds_line = qtime = void_line = None

    kds_data, Kds = create_model("Kds", {"nr":int, "kdsno":string, "datum":date, "tableno":int, "deptno":string, "billno":int, "artno":int, "artqty":int, "artname":string, "sp_req":string, "postby":string, "postdate":date, "post_time":string, "cooking_time":string, "done_time":string, "cooking_interval":string, "served_time":string, "serving_interval":string, "inttime":string})

    Q_kds_line = create_buffer("Q_kds_line",Queasy)
    Qtime = create_buffer("Qtime",Queasy)
    Void_line = create_buffer("Void_line",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kds_data, count_i, nr, spreq, starttime, endtime, inttime, deptname, currdate, orig_char, queasy, h_bill_line, h_artikel, h_journal, hoteldpt, printer
        nonlocal from_date, to_date, dept, kds_number
        nonlocal q_kds_line, qtime, void_line


        nonlocal kds, q_kds_line, qtime, void_line
        nonlocal kds_data

        return {"kds": kds_data}


    for currdate in date_range(from_date,to_date) :

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 257) & (Queasy.char1 == ("kds-header").lower()) & (Queasy.date1 == currdate) & (Queasy.number1 == dept)).order_by(Queasy.date1, Queasy.deci1).all():

            q_kds_line_obj_list = {}
            q_kds_line = Queasy()
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            for q_kds_line._recid, q_kds_line.date1, q_kds_line.number3, q_kds_line.char2, q_kds_line.deci1, q_kds_line.deci3, q_kds_line.number2, q_kds_line.char3, q_kds_line.char1, h_bill_line.anzahl, h_bill_line._recid, h_artikel.departement, h_artikel.bondruckernr, h_artikel.artnr, h_artikel.bezeich, h_artikel._recid in db_session.query(Q_kds_line._recid, Q_kds_line.date1, Q_kds_line.number3, Q_kds_line.char2, Q_kds_line.deci1, Q_kds_line.deci3, Q_kds_line.number2, Q_kds_line.char3, Q_kds_line.char1, H_bill_line.anzahl, H_bill_line._recid, H_artikel.departement, H_artikel.bondruckernr, H_artikel.artnr, H_artikel.bezeich, H_artikel._recid).join(H_bill_line,(H_bill_line._recid == Q_kds_line.number3)).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.bondruckernr[inc_value(0)] == kds_number)).filter(
                     (Q_kds_line.key == 255) & (Q_kds_line.char1 == ("kds-line").lower()) & (Q_kds_line.deci2 == to_decimal(queasy._recid))).order_by(Q_kds_line.date1, Q_kds_line.deci1).all():
                if q_kds_line_obj_list.get(q_kds_line._recid):
                    continue
                else:
                    q_kds_line_obj_list[q_kds_line._recid] = True

                h_journal = get_cache (H_journal, {"schankbuch": [(eq, q_kds_line.number3)]})

                if h_journal:
                    spreq = h_journal.aendertext
                else:
                    spreq = ""

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_artikel.departement)]})

                if hoteldpt:
                    deptname = hoteldpt.depart
                else:
                    deptname = ""
                starttime = to_int(q_kds_line.deci1)
                endtime = to_int(q_kds_line.deci3)

                if q_kds_line.char3.lower()  == ("2").lower() :
                    inttime = endtime - starttime
                else:
                    inttime = 0

                printer = get_cache (Printer, {"nr": [(eq, h_artikel.bondruckernr[0])]})

                qtime = get_cache (Queasy, {"key": [(eq, 302)],"betriebsnr": [(eq, to_int(q_kds_line._recid))]})

                if qtime:
                    orig_char = qtime.char1
                else:
                    orig_char = "-|-|-"
                nr = nr + 1
                kds = Kds()
                kds_data.append(kds)

                kds.nr = nr
                kds.kdsno = to_string(printer.nr) + " - " + printer.make
                kds.datum = queasy.date1
                kds.tableno = queasy.number3
                kds.deptno = deptname
                kds.billno = q_kds_line.number2
                kds.artno = h_artikel.artnr
                kds.artqty = h_bill_line.anzahl
                kds.artname = h_artikel.bezeich
                kds.sp_req = spreq
                kds.postby = queasy.char2
                kds.postdate = queasy.date1
                kds.post_time = to_string(starttime, "HH:MM:SS")
                kds.done_time = to_string(endtime, "HH:MM:SS")
                kds.inttime = to_string(inttime, "HH:MM:SS")
                kds.cooking_time = entry(0, orig_char, "|")
                kds.done_time = entry(1, orig_char, "|")
                kds.cooking_interval = to_string(to_datetime(kds.done_time) - to_datetime(kds.cooking_time) , "HH:MM:SS")
                kds.served_time = entry(2, orig_char, "|")
                kds.serving_interval = to_string(to_datetime(kds.served_time) - to_datetime(kds.done_time) , "HH:MM:SS")

    return generate_output()