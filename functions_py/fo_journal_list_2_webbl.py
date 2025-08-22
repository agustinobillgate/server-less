#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 13/8/2025
# date
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fo_journal_cld_3bl import fo_journal_cld_3bl
from models import Queasy, Artikel, Htparam

def fo_journal_list_2_webbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, onlyjournal:bool, excljournal:bool, mi_post:bool, mi_showrelease:bool, mi_break:bool, id_flag:string):

    prepare_cache ([Queasy, Artikel, Htparam])

    fo_journal_list_data = []
    done_flag = False
    gtot:Decimal = to_decimal("0.0")
    queasy = artikel = htparam = None

    output_list = fo_journal_list = bqueasy = None

    output_list_data, Output_list = create_model("Output_list", {"bezeich":string, "c":string, "ns":string, "mb":string, "shift":string, "dept":string, "str":string, "remark":string, "gname":string, "descr":string, "voucher":string, "checkin":date, "checkout":date, "guestname":string, "segcode":string, "amt_nett":Decimal, "service":Decimal, "vat":Decimal, "zinr":string, "deptno":int, "nationality":string, "resnr":int, "book_source":string, "resname":string})
    fo_journal_list_data, Fo_journal_list = create_model("Fo_journal_list", {"datum":date, "c":string, "roomnumber":string, "nsflag":string, "mbflag":string, "shift":string, "billno":int, "artno":int, "bezeich":string, "voucher":string, "depart":string, "outlet":string, "qty":int, "amount":Decimal, "guestname":string, "billrcvr":string, "zeit":string, "id":string, "sysdate":date, "remark":string, "checkin":date, "checkout":date, "segcode":string, "amt_nett":Decimal, "service":Decimal, "vat":Decimal, "vat_percentage":Decimal, "serv_percentage":Decimal, "deptno":int, "nationality":string, "resnr":int, "book_source":string, "resname":string})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fo_journal_list_data, done_flag, gtot, queasy, artikel, htparam
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, onlyjournal, excljournal, mi_post, mi_showrelease, mi_break, id_flag
        nonlocal bqueasy


        nonlocal output_list, fo_journal_list, bqueasy
        nonlocal output_list_data, fo_journal_list_data

        return {"fo-journal-list": fo_journal_list_data, "done_flag": done_flag}

    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "FO Transaction"
    queasy.number1 = 1
    queasy.char2 = id_flag


    pass
    gtot, output_list_data = get_output(fo_journal_cld_3bl(from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, onlyjournal, excljournal, mi_post, mi_showrelease, mi_break, id_flag))
    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "fo transaction")],"char2": [(eq, id_flag)]})

    if bqueasy:
        output_list_data
        done_flag = True
        pass
        bqueasy.number1 = 0


        pass
        pass
    fo_journal_list_data.clear()

    for output_list in query(output_list_data):
        fo_journal_list = Fo_journal_list()
        fo_journal_list_data.append(fo_journal_list)
        
        fo_journal_list.datum = date_mdy(substring(output_list.str, 0, 8))  # Rd 13/8/2025, error disini, output_list None
        fo_journal_list.c = output_list.c
        fo_journal_list.roomnumber = output_list.zinr
        fo_journal_list.nsflag = output_list.ns
        fo_journal_list.mbflag = output_list.mb
        fo_journal_list.shift = output_list.shift
        fo_journal_list.billno = to_int(substring(output_list.str, 14, 9))
        fo_journal_list.artno = to_int(substring(output_list.str, 23, 4))
        fo_journal_list.bezeich = output_list.descr
        fo_journal_list.voucher = output_list.voucher
        fo_journal_list.depart = substring(output_list.str, 77, 12)
        fo_journal_list.outlet = substring(output_list.str, 89, 6)
        fo_journal_list.qty = to_int(substring(output_list.str, 95, 5))
        fo_journal_list.amount = to_decimal(substring(output_list.str, 100, 22))
        fo_journal_list.guestname = output_list.guestname
        fo_journal_list.billrcvr = output_list.gname
        fo_journal_list.zeit = substring(output_list.str, 122, 8)
        fo_journal_list.id = substring(output_list.str, 130, 4)
        fo_journal_list.sysdate = date_mdy(substring(output_list.str, 134, 8))
        fo_journal_list.remark = output_list.remark
        fo_journal_list.checkin = output_list.checkin
        fo_journal_list.checkout = output_list.checkout
        fo_journal_list.segcode = output_list.segcode
        fo_journal_list.deptno = output_list.deptno
        fo_journal_list.nationality = output_list.nationality
        fo_journal_list.resnr = output_list.resnr
        fo_journal_list.book_source = output_list.book_source
        fo_journal_list.resname = output_list.resname

        if mi_break:
            fo_journal_list.amt_nett =  to_decimal(output_list.amt_nett)
            fo_journal_list.service =  to_decimal(output_list.service)
            fo_journal_list.vat =  to_decimal(output_list.vat)

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

    return generate_output()