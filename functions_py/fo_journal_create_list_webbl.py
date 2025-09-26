#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Artikel, Htparam

fo_journal_list_data, Fo_journal_list = create_model("Fo_journal_list", {"datum":date, "c":string, "roomnumber":string, "nsflag":string, "mbflag":string, "shift":string, "billno":int, "artno":int, "bezeich":string, "voucher":string, "depart":string, "outlet":string, "qty":int, "amount":Decimal, "guestname":string, "billrcvr":string, "zeit":string, "id":string, "sysdate":date, "remark":string, "checkin":date, "checkout":date, "segcode":string, "amt_nett":Decimal, "service":Decimal, "vat":Decimal, "vat_percentage":Decimal, "serv_percentage":Decimal, "deptno":int, "nationality":string, "resnr":int, "book_source":string, "resname":string})

def fo_journal_create_list_webbl(id_flag:string, fo_journal_list_data:[Fo_journal_list]):

    prepare_cache ([Artikel, Htparam])

    done_flag = False
    counter:int = 0
    queasy_str1:string = ""
    queasy_str2:string = ""
    queasy = artikel = htparam = None

    fo_journal_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done_flag, counter, queasy_str1, queasy_str2, queasy, artikel, htparam
        nonlocal id_flag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal fo_journal_list, bqueasy, pqueasy, tqueasy
        return {"done_flag": done_flag, "fo-journal-list": fo_journal_list_data}


#"""
#            .                                                 1234                                    Sembodo, Yaksa           Sembodo, Yaksa                                                                                                                                      09/24/2409/25/24ECO-ONLINE 0        96252ONLINE TRAVEL AGENTTIKET.COM,                 0.00               0.00               0.00
#"""
    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("FO Transaction")) & (Queasy.char2 == (id_flag))).order_by(Queasy.number1).all():
        counter = counter + 1
        queasy_str1 = entry(0, queasy.char3, "|")
        queasy_str2 = entry(1, queasy.char3, "|")

        if counter > 1000:
            break
        fo_journal_list = Fo_journal_list()
        fo_journal_list_data.append(fo_journal_list)

        fo_journal_list.datum = substring(queasy_str1, 0, 8)
        fo_journal_list.billno = to_int(substring(queasy_str1, 14, 9))
        fo_journal_list.artno = to_int(substring(queasy_str1, 23, 4))
        fo_journal_list.depart = substring(queasy_str1, 77, 12)
        fo_journal_list.outlet = substring(queasy_str1, 89, 6)
        fo_journal_list.qty = to_int(substring(queasy_str1, 92, 5))
        fo_journal_list.amount = substring(queasy_str1, 97, 22)
        fo_journal_list.zeit = substring(queasy_str1, 122, 8)
        fo_journal_list.id = substring(queasy_str1, 130, 4)
        fo_journal_list.sysdate = substring(queasy_str1, 134, 8)
        #-------------------------------------------------------------------------
        fo_journal_list.c = trim(substring(queasy_str2, 0, 2))
        fo_journal_list.roomnumber = trim(substring(queasy_str2, 2, 6))
        fo_journal_list.nsflag = trim(substring(queasy_str2, 8, 1))
        fo_journal_list.mbflag = trim(substring(queasy_str2, 9, 1))
        fo_journal_list.shift = trim(substring(queasy_str2, 10, 2))
        fo_journal_list.bezeich = trim(substring(queasy_str2, 12, 50))
        fo_journal_list.voucher = trim(substring(queasy_str2, 62, 40))
        fo_journal_list.guestname = trim(substring(queasy_str2, 102, 25))
        fo_journal_list.billrcvr = trim(substring(queasy_str2, 127, 24))
        fo_journal_list.remark = trim(substring(queasy_str2, 151, 124))
        fo_journal_list.checkin =substring(queasy_str2, 275, 8)
        fo_journal_list.checkout = substring(queasy_str2, 283, 8)
        fo_journal_list.segcode = trim(substring(queasy_str2, 291, 20))
        fo_journal_list.deptno = to_int(trim(substring(queasy_str2, 311, 2)))
        fo_journal_list.nationality = trim(substring(queasy_str2, 313, 5))
        fo_journal_list.resnr = to_int(trim(substring(queasy_str2, 318, 10)))
        fo_journal_list.book_source = trim(substring(queasy_str2, 328, 20))
        fo_journal_list.resname = trim(substring(queasy_str2, 348, 25))

        if queasy.logi1:
            fo_journal_list.amt_nett = to_decimal(substring(queasy_str2, 373, 21))
            fo_journal_list.service = to_decimal(substring(queasy_str2, 394, 21))
            fo_journal_list.vat = to_decimal(substring(queasy_str2, 415, 21))

            artikel = get_cache (Artikel, {"departement": [(eq, fo_journal_list.deptno)],"artnr": [(eq, fo_journal_list.artno)]})

            if artikel:

                htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                if htparam:
                    fo_journal_list.vat_percentage =  to_decimal(htparam.fdecimal)
                else:
                    fo_journal_list.vat_percentage =  to_decimal("0")

                htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                if htparam:
                    fo_journal_list.serv_percentage =  to_decimal(htparam.fdecimal)
                else:
                    fo_journal_list.serv_percentage =  to_decimal("0")

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
            pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("FO Transaction")) & (Pqueasy.char2 == (id_flag))).first()

    if pqueasy:
        done_flag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("FO Transaction")) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == (id_flag))).first()

        if tqueasy:
            done_flag = False


        else:
            done_flag = True



    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("FO Transaction")) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == (id_flag))).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()


"""
Visa[Deposit #96252]                                                                                1234                                    Sembodo, Yaksa           Sembodo, Yaksa                                                                                                                                      09/24/2409/25/24ECO-ONLINE 0        96252ONLINE TRAVEL AGENTTIKET.COM,                 0.00               0.00               0.00

"""