#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import History, Paramtext, Res_line, Guest, Queasy

def gcf_history_3bl(gastnr:int, fdate:date, tdate:date):

    prepare_cache ([History, Paramtext, Res_line, Guest, Queasy])

    ghistory_list = []
    summ_list_list = []
    htl_name:string = ""
    str:string = ""
    i:int = 0
    history = paramtext = res_line = guest = queasy = None

    ghistory = summ_list = hist1 = None

    ghistory_list, Ghistory = create_model_like(History, {"hname":string, "gname":string, "address":string, "s_recid":int, "vcrnr":string, "mblnr":string, "email":string})
    summ_list_list, Summ_list = create_model_like(History)

    Hist1 = create_buffer("Hist1",History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ghistory_list, summ_list_list, htl_name, str, i, history, paramtext, res_line, guest, queasy
        nonlocal gastnr, fdate, tdate
        nonlocal hist1


        nonlocal ghistory, summ_list, hist1
        nonlocal ghistory_list, summ_list_list

        return {"ghistory": ghistory_list, "summ-list": summ_list_list}

    def create_ghistory():

        nonlocal ghistory_list, summ_list_list, htl_name, str, i, history, paramtext, res_line, guest, queasy
        nonlocal gastnr, fdate, tdate
        nonlocal hist1


        nonlocal ghistory, summ_list, hist1
        nonlocal ghistory_list, summ_list_list

        for history in db_session.query(History).filter(
                 (History.gastnr == gastnr) & (History.abreise >= fdate) & (History.abreise <= tdate)).order_by(History.abreise.desc()).all():
            ghistory = Ghistory()
            ghistory_list.append(ghistory)

            buffer_copy(history, ghistory,except_fields=["gastinfo"])

            hist1 = get_cache (History, {"resnr": [(eq, history.resnr)],"ankunft": [(eq, history.ankunft)],"abreise": [(eq, history.abreise)],"segmentcode": [(eq, history.segmentcode)],"arrangement": [(eq, history.arrangement)]})

            if hist1:
                ghistory.gastinfo = hist1.gastinfo
                ghistory.gname = entry(0, ghistory.gastinfo, "-")

                if num_entries(ghistory.gastinfo, "-") == 2:
                    ghistory.address = entry(1, ghistory.gastinfo, "-")

            res_line = db_session.query(Res_line).filter(
                     (matches(Res_line.zimmer_wunsch,"*voucher*")) & (Res_line.resnr == history.resnr)).first()

            if res_line:
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == ("voucher").lower() :
                        ghistory.vcrnr = substring(str, 7)

            guest = get_cache (Guest, {"gastnr": [(eq, history.gastnr)]})

            if guest:
                ghistory.mblnr = guest.mobil_telefon
                ghistory.email = guest.email_adr

            queasy = get_cache (Queasy, {"key": [(eq, 203)],"number1": [(eq, guest.gastnr)],"number2": [(eq, history.resnr)]})

            if queasy:
                ghistory.hname = queasy.char1


            else:
                ghistory.hname = htl_name


            ghistory.s_recid = to_int(history._recid)

        for ghistory in query(ghistory_list):

            summ_list = query(summ_list_list, filters=(lambda summ_list: summ_list.gastnr == ghistory.gastnr and summ_list.arrangement == ghistory.arrangement), first=True)

            if not summ_list:
                summ_list = Summ_list()
                summ_list_list.append(summ_list)

                summ_list.gastnr = ghistory.gastnr
                summ_list.zikateg = "T O T A L"
                summ_list.arrangement = ghistory.arrangement
                summ_list.zimmeranz = ghistory.zimmeranz
                summ_list.zipreis =  to_decimal(ghistory.zipreis)
                summ_list.gesamtumsatz =  to_decimal(ghistory.gesamtumsatz)
                summ_list.argtumsatz =  to_decimal(ghistory.argtumsatz)
                summ_list.f_b_umsatz =  to_decimal(ghistory.f_b_umsatz)
                summ_list.sonst_umsatz =  to_decimal(ghistory.sonst_umsatz)


            else:
                summ_list.zimmeranz = summ_list.zimmeranz + ghistory.zimmeranz
                summ_list.zipreis =  to_decimal(summ_list.zipreis) + to_decimal(ghistory.zipreis)
                summ_list.gesamtumsatz =  to_decimal(summ_list.gesamtumsatz) + to_decimal(ghistory.gesamtumsatz)
                summ_list.argtumsatz =  to_decimal(summ_list.argtumsatz) + to_decimal(ghistory.argtumsatz)
                summ_list.f_b_umsatz =  to_decimal(summ_list.f_b_umsatz) + to_decimal(ghistory.f_b_umsatz)
                summ_list.sonst_umsatz =  to_decimal(summ_list.sonst_umsatz) + to_decimal(ghistory.sonst_umsatz)

            guest = get_cache (Guest, {"name": [(eq, entry(0, ghistory.gname, ","))]})

            if guest:
                ghistory.mblnr = guest.mobil_telefon
                ghistory.email = guest.email_adr

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        htl_name = paramtext.ptexte
    create_ghistory()

    return generate_output()