#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import History, Paramtext, Res_line, Guest

def gcf_history_webbl(gastnr:int, fdate:date, tdate:date, vkey:int):

    prepare_cache ([History, Paramtext, Res_line, Guest])

    ghistory_data = []
    summ_list_data = []
    htl_name:string = ""
    str:string = ""
    i:int = 0
    history = paramtext = res_line = guest = None

    ghistory = summ_list = hist1 = b_history = None

    ghistory_data, Ghistory = create_model("Ghistory", {"gastnr":int, "ankunft":date, "abreise":date, "zimmeranz":int, "zikateg":string, "zinr":string, "erwachs":int, "kind":[int,2], "gratis":int, "zipreis":Decimal, "arrangement":string, "gesamtumsatz":Decimal, "bemerk":string, "logisumsatz":Decimal, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "gastinfo":string, "zahlungsart":int, "com_logis":Decimal, "com_argt":Decimal, "com_f_b":Decimal, "com_sonst":Decimal, "guestnrcom":int, "abreisezeit":string, "segmentcode":int, "zi_wechsel":bool, "resnr":int, "ums_kurz":Decimal, "ums_lang":Decimal, "reslinnr":int, "hname":string, "gname":string, "address":string, "s_recid":int, "vcrnr":string, "mblnr":string, "email":string})
    summ_list_data, Summ_list = create_model_like(History)

    Hist1 = create_buffer("Hist1",History)
    B_history = create_buffer("B_history",History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ghistory_data, summ_list_data, htl_name, str, i, history, paramtext, res_line, guest
        nonlocal gastnr, fdate, tdate, vkey
        nonlocal hist1, b_history


        nonlocal ghistory, summ_list, hist1, b_history
        nonlocal ghistory_data, summ_list_data

        return {"ghistory": ghistory_data, "summ-list": summ_list_data}

    def create_ghistory():

        nonlocal ghistory_data, summ_list_data, htl_name, str, i, history, paramtext, res_line, guest
        nonlocal gastnr, fdate, tdate, vkey
        nonlocal hist1, b_history


        nonlocal ghistory, summ_list, hist1, b_history
        nonlocal ghistory_data, summ_list_data

        if vkey == 1:

            for history in db_session.query(History).filter(
                     (History.gastnr == gastnr) & (History.abreise >= fdate) & (History.abreise <= tdate)).order_by(History.abreise.desc()).all():
                ghistory = Ghistory()
                ghistory_data.append(ghistory)

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
                    ghistory.bemerk = ghistory.bemerk + "G: " + guest.bemerkung + chr_unicode(10)

                    if guest.karteityp != 0:
                        ghistory.bemerk = ghistory.bemerk + "RL: " + chr_unicode(10)

                        for b_history in db_session.query(B_history).filter(
                                 (B_history.resnr == history.resnr) & (B_history.reslinnr != 999)).order_by(B_history.reslinnr).all():

                            res_line = get_cache (Res_line, {"resnr": [(eq, b_history.resnr)],"reslinnr": [(eq, b_history.reslinnr)]})

                            if res_line:

                                if trim(res_line.bemerk) != "":
                                    ghistory.bemerk = ghistory.bemerk + "[" + to_string(b_history.reslinnr) + "] " + res_line.bemerk + chr_unicode(10)
                ghistory.hname = htl_name
                ghistory.s_recid = to_int(history._recid)

        elif vkey == 2:

            for history in db_session.query(History).filter(
                     (History.gastnr == gastnr) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft.desc()).all():
                ghistory = Ghistory()
                ghistory_data.append(ghistory)

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
                    ghistory.bemerk = ghistory.bemerk + "G: " + guest.bemerkung + chr_unicode(10)

                    if guest.karteityp != 0:
                        ghistory.bemerk = ghistory.bemerk + "RL: " + chr_unicode(10)

                        for b_history in db_session.query(B_history).filter(
                                 (B_history.resnr == history.resnr) & (B_history.reslinnr != 999)).order_by(B_history.reslinnr).all():

                            res_line = get_cache (Res_line, {"resnr": [(eq, b_history.resnr)],"reslinnr": [(eq, b_history.reslinnr)]})

                            if res_line:

                                if trim(res_line.bemerk) != "":
                                    ghistory.bemerk = ghistory.bemerk + "[" + to_string(b_history.reslinnr) + "] " + res_line.bemerk + chr_unicode(10)
                ghistory.hname = htl_name
                ghistory.s_recid = to_int(history._recid)

        for ghistory in query(ghistory_data):

            summ_list = query(summ_list_data, filters=(lambda summ_list: summ_list.gastnr == ghistory.gastnr and summ_list.arrangement == ghistory.arrangement), first=True)

            if not summ_list:
                summ_list = Summ_list()
                summ_list_data.append(summ_list)

                summ_list.gastnr = ghistory.gastnr
                summ_list.zikateg = "T O T A L - " + ghistory.arrangement
                summ_list.arrangement = ghistory.arrangement
                summ_list.zimmeranz = 1
                summ_list.zipreis =  to_decimal(ghistory.zipreis)
                summ_list.gesamtumsatz =  to_decimal(ghistory.gesamtumsatz)
                summ_list.argtumsatz =  to_decimal(ghistory.argtumsatz)
                summ_list.f_b_umsatz =  to_decimal(ghistory.f_b_umsatz)
                summ_list.sonst_umsatz =  to_decimal(ghistory.sonst_umsatz)


            else:
                summ_list.zimmeranz = summ_list.zimmeranz + 1
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