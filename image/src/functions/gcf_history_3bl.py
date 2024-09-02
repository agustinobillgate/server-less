from functions.additional_functions import *
import decimal
from datetime import date
from models import History, Paramtext, Res_line, Guest

def gcf_history_3bl(gastnr:int, fdate:date, tdate:date):
    ghistory_list = []
    summ_list_list = []
    htl_name:str = ""
    str:str = ""
    i:int = 0
    history = paramtext = res_line = guest = None

    ghistory = summ_list = hist1 = None

    ghistory_list, Ghistory = create_model_like(History, {"hname":str, "gname":str, "address":str, "s_recid":int, "vcrnr":str, "mblnr":str, "email":str})
    summ_list_list, Summ_list = create_model_like(History)

    Hist1 = History

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ghistory_list, summ_list_list, htl_name, str, i, history, paramtext, res_line, guest
        nonlocal hist1


        nonlocal ghistory, summ_list, hist1
        nonlocal ghistory_list, summ_list_list
        return {"ghistory": ghistory_list, "summ-list": summ_list_list}

    def create_ghistory():

        nonlocal ghistory_list, summ_list_list, htl_name, str, i, history, paramtext, res_line, guest
        nonlocal hist1


        nonlocal ghistory, summ_list, hist1
        nonlocal ghistory_list, summ_list_list

        for history in db_session.query(History).filter(
                (History.gastnr == gastnr) &  (History.abreise >= fdate) &  (History.abreise <= tdate)).all():
            ghistory = Ghistory()
            ghistory_list.append(ghistory)

            buffer_copy(history, ghistory,except_fields=["gastinfo"])

            hist1 = db_session.query(Hist1).filter(
                    (Hist1.resnr == history.resnr) &  (Hist1.ankunft == history.ankunft) &  (Hist1.abreise == history.abreise) &  (Hist1.segmentcode == history.segmentcode) &  (Hist1.arrangement == history.arrangement)).first()

            if hist1:
                ghistory.gastinfo = hist1.gastinfo
                ghistory.gname = entry(0, ghistory.gastinfo, "-")

                if num_entries(ghistory.gastinfo, "-") == 2:
                    ghistory.address = entry(1, ghistory.gastinfo, "-")

            res_line = db_session.query(Res_line).filter(
                    (Res_line.zimmer_wunsch.op("~")(".*voucher.*")) &  (Res_line.resnr == history.resnr)).first()

            if res_line:
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == "voucher":
                        ghistory.vcrnr = substring(str, 7)

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == history.gastnr)).first()

            if guest:
                ghistory.mblnr = guest.mobil_telefon
                ghistory.email = guest.email_adr
            ghistory.hname = htl_name
            ghistory.s_recid = to_int(history._recid)

        for ghistory in query(ghistory_list):

            summ_list = query(summ_list_list, filters=(lambda summ_list :summ_list.gastnr == ghistory.gastnr and summ_list.arrangement == ghistory.arrangement), first=True)

            if not summ_list:
                summ_list = Summ_list()
                summ_list_list.append(summ_list)

                summ_list.gastnr = ghistory.gastnr
                summ_list.zikateg = "T O T A L"
                summ_list.arrangement = ghistory.arrangement
                summ_list.zimmeranz = 1
                summ_list.zipreis = ghistory.zipreis
                summ_list.gesamtumsatz = ghistory.gesamtumsatz
                summ_list.argtumsatz = ghistory.argtumsatz
                summ_list.f_b_umsatz = ghistory.f_b_umsatz
                summ_list.sonst_umsatz = ghistory.sonst_umsatz


            else:
                summ_list.zimmeranz = summ_list.zimmeranz + 1
                summ_list.zipreis = summ_list.zipreis + ghistory.zipreis
                summ_list.gesamtumsatz = summ_list.gesamtumsatz + ghistory.gesamtumsatz
                summ_list.argtumsatz = summ_list.argtumsatz + ghistory.argtumsatz
                summ_list.f_b_umsatz = summ_list.f_b_umsatz + ghistory.f_b_umsatz
                summ_list.sonst_umsatz = summ_list.sonst_umsatz + ghistory.sonst_umsatz

            guest = db_session.query(Guest).filter(
                    (Guest.name == entry(0, ghistory.gname, ","))).first()

            if guest:
                ghistory.mblnr = guest.mobil_telefon
                ghistory.email = guest.email_adr


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 200)).first()

    if paramtext:
        htl_name = paramtext.ptext
    create_ghistory()

    return generate_output()