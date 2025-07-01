#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, H_journal

def odx_trans_logbl(art_dept:int, from_date:date, to_date:date):

    prepare_cache ([Queasy, H_journal])

    revenue_list_list = []
    article_list:string = ""
    loop_i:int = 0
    messtoken:string = ""
    getartname:string = ""
    getartno:int = 0
    bill_date:date = None
    queasy = h_journal = None

    revenue_list = art_list = buffqueasy = None

    revenue_list_list, Revenue_list = create_model("Revenue_list", {"payment_type":string, "amount":Decimal, "accounttype":string, "accountname":string, "comment":string, "bill_datum":date, "revenue_recid":int, "bill_number":int, "send_flag":bool})
    art_list_list, Art_list = create_model("Art_list", {"vhp_artdept":int, "vhp_artnr":int, "vhp_arttype":string, "vhp_artname":string, "rms_artname":string, "rms_arttype":string})

    Buffqueasy = create_buffer("Buffqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal revenue_list_list, article_list, loop_i, messtoken, getartname, getartno, bill_date, queasy, h_journal
        nonlocal art_dept, from_date, to_date
        nonlocal buffqueasy


        nonlocal revenue_list, art_list, buffqueasy
        nonlocal revenue_list_list, art_list_list

        return {"revenue-list": revenue_list_list}


    queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 97)],"date1": [(ge, from_date),(le, to_date)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 242
        queasy.number1 = 97
        queasy.number2 = art_dept
        queasy.date1 = bill_date
        queasy.char1 = "Revenue NonStay Periode : " + to_string(bill_date, "99-99-9999")
        queasy.logi1 = False
        queasy.betriebsnr = queasy._recid


    pass
    pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 242) & (Queasy.number1 == 98) & (Queasy.number2 == art_dept)).order_by(Queasy.number2, Queasy.number3).all():

        if queasy.char3 != "":
            art_list = Art_list()
            art_list_list.append(art_list)

            art_list.vhp_artdept = queasy.number2
            art_list.vhp_artnr = queasy.number3
            art_list.vhp_artname = queasy.char1
            art_list.rms_arttype = queasy.char2
            art_list.rms_artname = queasy.char3


    pass

    for buffqueasy in db_session.query(Buffqueasy).filter(
             (Buffqueasy.key == 242) & (Buffqueasy.number1 == 97) & (Buffqueasy.logi1 == False)).order_by(Buffqueasy._recid).all():

        for art_list in query(art_list_list):
            revenue_list = Revenue_list()
            revenue_list_list.append(revenue_list)

            revenue_list.accountname = art_list.rms_artname
            revenue_list.payment_type = art_list.rms_arttype
            revenue_list.accounttype = "extras"
            revenue_list.bill_datum = buffqueasy.date1
            revenue_list.revenue_recid = buffqueasy.betriebsnr
            revenue_list.send_flag = buffqueasy.logi1

            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.departement == art_dept) & (H_journal.artnr == art_list.vhp_artnr) & (H_journal.bill_datum == buffqueasy.date1)).order_by(H_journal._recid).all():
                revenue_list.amount =  to_decimal(revenue_list.amount) + to_decimal(h_journal.betrag)
                revenue_list.bill_number = h_journal.rechnr
            revenue_list.amount =  - to_decimal((revenue_list.amount))

    return generate_output()