from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, H_bill_line, H_artikel, H_journal, Hoteldpt

def kitchen_display_reportbl(from_date:date, to_date:date, dept:int, kds_number:int):
    kds_list = []
    count_i:int = 0
    nr:int = 0
    spreq:str = ""
    starttime:int = 0
    endtime:int = 0
    inttime:int = 0
    deptname:str = ""
    currdate:date = None
    queasy = h_bill_line = h_artikel = h_journal = hoteldpt = None

    kds = q_kds_line = void_line = None

    kds_list, Kds = create_model("Kds", {"nr":int, "kdsno":int, "datum":date, "tableno":int, "deptno":str, "billno":int, "artno":int, "artqty":int, "artname":str, "sp_req":str, "postby":str, "postdate":date, "posttime":str, "donetime":str, "inttime":str})

    Q_kds_line = Queasy
    Void_line = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kds_list, count_i, nr, spreq, starttime, endtime, inttime, deptname, currdate, queasy, h_bill_line, h_artikel, h_journal, hoteldpt
        nonlocal q_kds_line, void_line


        nonlocal kds, q_kds_line, void_line
        nonlocal kds_list
        return {"kds": kds_list}


    for currdate in range(from_date,to_date + 1) :

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 257) &  (func.lower(Queasy.char1) == "kds_header") &  (Queasy.date1 == currdate) &  (Queasy.number1 == dept)).all():

            q_kds_line_obj_list = []
            for q_kds_line, h_bill_line, h_artikel in db_session.query(Q_kds_line, H_bill_line, H_artikel).join(H_bill_line,(H_bill_line._recid == Q_kds_line.number3)).join(H_artikel,(H_artikel.departement == h_bill_line.departement) &  (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.bondruckernr[0] == kds_number)).filter(
                    (Q_kds_line.key == 255) &  (func.lower(Q_kds_line.char1) == "kds_line") &  (Q_kds_line.deci2 == decimal.Decimal(queasy._recid))).all():
                if q_kds_line._recid in q_kds_line_obj_list:
                    continue
                else:
                    q_kds_line_obj_list.append(q_kds_line._recid)

                h_journal = db_session.query(H_journal).filter(
                        (H_journal.schankbuch == q_kds_line.number3)).first()

                if h_journal:
                    spreq = h_journal.aendertext
                else:
                    spreq = ""

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == h_artikel.departement)).first()

                if hoteldpt:
                    deptname = hoteldpt.depart
                else:
                    deptname = ""
                starttime = to_int(q_kds_line.deci1)
                endtime = to_int(q_kds_line.deci3)

                if q_kds_line.char3.lower()  == "2":
                    inttime = endtime - starttime
                else:
                    inttime = 0
                nr = nr + 1
                kds = Kds()
                kds_list.append(kds)

                kds.nr = nr
                kds.kdsno = h_artikel.bondruckernr[0]
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
                kds.posttime = to_string(starttime, "HH:MM:SS")
                kds.donetime = to_string(endtime, "HH:MM:SS")
                kds.inttime = to_string(inttime, "HH:MM:SS")

    return generate_output()