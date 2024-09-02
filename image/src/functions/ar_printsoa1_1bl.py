from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Guest, Bill, Debitor, Bill_line, H_bill_line, Res_line, Artikel, Queasy, Bresline, Zimkateg, Reservation, H_bill, Hoteldpt, H_artikel

def ar_printsoa1_1bl(show_type:int, bof_month:date, eof_month:date, param_ar:[Param_ar], guestno:int, curr_day:date):
    zeit:int = 0
    zeit1:int = 0
    str:str = ""
    due_date = None
    soa_list_list = []
    rech_nr = 0
    bet_nr = 0
    msg_int = 0
    param1:str = ""
    param2:str = ""
    param3:str = ""
    param4:str = ""
    fnet_lodging:decimal = 0
    lnet_lodging:decimal = 0
    net_breakfast:decimal = 0
    net_lunch:decimal = 0
    net_dinner:decimal = 0
    net_others:decimal = 0
    tot_rmrev:decimal = 0
    nett_vat:decimal = 0
    nett_service:decimal = 0
    curr_gastnr:int = 0
    curr_refno:int = 0
    new_refno:int = 0
    cl_exist:bool = False
    saldo:decimal = 0
    s:str = ""
    i:int = 0
    arrival:date = None
    departure:date = None
    debt:decimal = 0
    crdt:decimal = 0
    fdebt:decimal = 0
    fcrdt:decimal = 0
    new_crdt:decimal = 0
    new_fcrdt:decimal = 0
    isprintedb4:bool = False
    saldo1:decimal = 0
    saldo2:decimal = 0
    saldo3:decimal = 0
    saldo4:decimal = 0
    other_flag:bool = False
    count_zimm:int = 0
    nmonth:int = 0
    mnth1:int = 0
    year2:int = 0
    val_param:int = 0
    var_param:str = ""
    guest = bill = debitor = bill_line = h_bill_line = res_line = artikel = queasy = bresline = zimkateg = reservation = h_bill = hoteldpt = h_artikel = None

    soa_list = soabuff = param_ar = gast = bill1 = debt = debt1 = billine = hbilline = bresline = bdebt = bdebt1 = debbt = None

    soa_list_list, Soa_list = create_model("Soa_list", {"counter":int, "debref":int, "done_step":int, "artno":int, "vesrdep":decimal, "to_sort":int, "outlet":bool, "datum":date, "ankunft":date, "abreise":date, "gastnr":int, "name":str, "inv_str":str, "rechnr":int, "refno":int, "voucherno":str, "voucherno1":str, "voucherno2":str, "saldo":decimal, "fsaldo":decimal, "printed":bool, "selected":bool, "printdate":date, "dptnr":int, "debt":decimal, "credit":decimal, "fdebt":decimal, "fcredit":decimal, "remarks":str, "arrecid":int, "newpayment":decimal, "newfpayment":decimal, "zinr":str, "erwachs":int, "child1":int, "child2":int, "roomrate":decimal, "tot_amount":decimal, "tot_balance":decimal, "exrate":decimal, "tot_exrate":decimal, "gst_tot_non_taxable":decimal, "gst_amount":decimal, "gst_tot_sales":decimal, "zimmeranz":int}, {"printdate": get_current_date()})
    param_ar_list, Param_ar = create_model("Param_ar", {"param_nr":int, "param_name":str, "param_val":str, "param_type":str})

    Soabuff = Soa_list
    soabuff_list = soa_list_list

    Gast = Guest
    Bill1 = Bill
    debt = Debitor
    Debt1 = Debitor
    Billine = Bill_line
    Hbilline = H_bill_line
    Bresline = Res_line
    Bdebt = Debitor
    Bdebt1 = Debitor
    Debbt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zeit, zeit1, str, due_date, soa_list_list, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, bresline, zimkateg, reservation, h_bill, hoteldpt, h_artikel
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt
        nonlocal soa_list_list, param_ar_list
        return {"due_date": due_date, "soa-list": soa_list_list, "rech_nr": rech_nr, "bet_nr": bet_nr, "msg_int": msg_int}

    def create_soalist():

        nonlocal zeit, zeit1, str, due_date, soa_list_list, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, bresline, zimkateg, reservation, h_bill, hoteldpt, h_artikel
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt
        nonlocal soa_list_list, param_ar_list

        nmonth:int = 0
        mnth1:int = 0
        year2:int = 0
        counter_saldo:decimal = 0
        val_param:int = 0
        var_param:str = ""
        Bdebt = Debitor
        Bdebt1 = Debitor
        soa_list_list.clear()

        if show_type == 0:

            debitor_obj_list = []
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                    (Debitor.gastnr == guestno) &  (Debitor.opart <= 1) &  (Debitor.saldo != 0) &  (Debitor.zahlkonto == 0)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)

                soa_list = query(soa_list_list, filters=(lambda soa_list :soa_list.gastnr == debitor.gastnr and soa_list.rechnr == debitor.rechnr and soa_list.dptnr == debitor.betriebsnr), first=True)

                if not soa_list:
                    soa_list = Soa_list()
                    soa_list_list.append(soa_list)

                    soa_list.to_sort = 1
                    soa_list.arRecid = debitor._recid
                    soa_list.rechnr = debitor.rechnr
                    soa_list.gastnr = debitor.gastnr
                    soa_list.datum = debitor.rgdatum
                    soa_list.remarks = debitor.vesrcod
                    soa_list.dptnr = debitor.betriebsnr
                    soa_list.artno = debitor.artnr
                    soa_list.counter = debitor.counter
                    soa_list.debref = debitor.debref
                    soa_list.saldo = soa_list.saldo + debitor.saldo
                    soa_list.vesrdep = debitor.vesrdep


            Debbt = Debitor

            soa_list = query(soa_list_list, filters=(lambda soa_list :soa_list.done_step == 0), first=True)
            while None != soa_list:
                crdt = 0 debt == 0 fcrdt == 0 fdebt == 0
                new_crdt = 0 new_fcrdt == 0
                isprintedb4 = (soa_list.debref > 0)

                for soabuff in query(soabuff_list, filters=(lambda soabuff :soabuff.rechnr == soa_list.rechnr and soabuff.dptnr == soa_list.dptnr and soabuff.artno == soa_list.artno and soabuff.done_step == 0)):
                    soabuff.done_step = 1
                    debt = soabuff.saldo
                    fdebt = fdebt + soabuff.vesrdep

                    if soabuff.counter > 0:

                        for debt in db_session.query(debt).filter(
                                (debt.rechnr == soabuff.rechnr) &  (debt.counter == soabuff.counter) &  (debt.gastnr == guestno) &  (debt.zahlkonto > 0)).all():
                            fcrdt = fcrdt + debt.vesrdep
                            crdt = crdt + debt.saldo

                            if isprintedb4 and debt.debref == 0:
                                new_crdt = new_crdt + crdt
                                new_fcrdt = new_fcrdt + fcrdt


                    debt_obj_list = []
                    for debt, artikel in db_session.query(debt, Artikel).join(Artikel,(Artikel.artnr == debt.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                            (debt.rechnr == soabuff.rechnr) &  (debt.gastnr == soabuff.gastnr) &  (debt.betriebsnr == soabuff.dptnr) &  (debt.opart <= 1) &  (soabuff.saldo != 0) &  (debt.zahlkonto == 0) &  (debt._recid != soa_list.arRecid)).all():
                        if debt._recid in debt_obj_list:
                            continue
                        else:
                            debt_obj_list.append(debt._recid)


                        debt = debt + debt.saldo
                        fdebt = fdebt + debt.vesrdep

                        if debt.counter > 0:

                            for debt1 in db_session.query(Debt1).filter(
                                    (Debt1.rechnr == debt.rechnr) &  (Debt1.counter == debt.counter) &  (Debt1.artnr == debt.artnr) &  (debt.gastnr == debitor.gastnr) &  (Debt1.zahlkonto > 0)).all():
                                crdt = crdt + debt.saldo
                                fcrdt = fcrdt + debt.vesrdep

                                if isprintedb4 and debt1.debref == 0:
                                    new_crdt = new_crdt + crdt
                                    new_fcrdt = new_fcrdt + fcrdt

                crdt = - crdt
                fcrdt = - fcrdt
                new_crdt = - new_crdt
                new_fcrdt = - new_fcrdt

                for soabuff in query(soabuff_list, filters=(lambda soabuff :soabuff.done_step == 1)):
                    soabuff.done_step = 2
                    soabuff.debt = debt
                    soabuff.credit = crdt
                    soabuff.saldo = debt - crdt
                    soabuff.fdebt = fdebt
                    soabuff.fcredit = fcrdt
                    soabuff.fsaldo = fdebt - fcrdt
                    soabuff.newpayment = new_crdt
                    soabuff.newfpayment = new_fcrdt

                soa_list = query(soa_list_list, filters=(lambda soa_list :soa_list.done_step == 0), next=True)

            for soa_list in query(soa_list_list):
                zeit = get_current_time_in_seconds()

                debitor = db_session.query(Debitor).filter(
                        (Debitor._recid == soa_list.arRecid)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == debitor.gastnr)).first()

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:

                        if debitor.debref != 0:

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 192) &  (Queasy.number1 == debitor.rechnr)).first()

                            if queasy:
                                soa_list.printed = True

                            elif not queasy:
                                soa_list.printed = False

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == debitor.gastnrmember)).first()

                        if gast:
                            soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        continue
                    zeit1 = get_current_time_in_seconds()
                    other_flag = False

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.artnr == debitor.artnr) &  (Bill_line.departement == 0)).first()

                    gast = db_session.query(Gast).filter(
                            (Gast.gastnr == debitor.gastnrmember)).first()
                    soa_list.refNo = billref
                    soa_list.dptnr = 0

                    if billref != 0:

                        bdebt = db_session.query(Bdebt).filter(
                                (Bdebt.rechnr == soa_list.rechnr) &  (Bdebt.debref != 0) &  (Bdebt.counter == soa_list.counter)).first()

                        if bdebt:
                            soa_list.saldo = soa_list.saldo - bdebt.saldo
                            soa_list.debt = soa_list.debt - bdebt.saldo

                            if soa_list.saldo != 0:

                                bdebt1 = db_session.query(Bdebt1).filter(
                                        (Bdebt1.debref == 0) &  (Bdebt1.rechnr == soa_list.rechnr)).first()

                                if bdebt1:
                                    soa_list.arRecid = bdebt1._recid
                                    other_flag = True

                    if billref == 0:
                        soa_list.printed = False
                    else:

                        if other_flag :

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 192) &  (Queasy.number1 == debitor.rechnr)).first()

                            if queasy:
                                soa_list.printed = True

                            elif not queasy:
                                soa_list.printed = False
                        else:
                            soa_list.printed = True

                    if bill.logidat != None:
                        soa_list.printdate = bill.logidat
                    else:
                        soa_list.printdate = get_current_date()

                    if billref != 0:
                        soa_list.inv_str = "INV" + to_string(billref, "9999999")

                    if bill_line:
                        soa_list.voucherno = entry(1, bill_line.bezeich, "/")

                    if gast:
                        soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                    else:
                        soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if bill.resnr > 0:

                        res_line = db_session.query(Res_line).filter(
                                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                        if not res_line:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr)).first()

                        if res_line:
                            soa_list.ankunft = res_line.ankunft
                            soa_list.abreise = res_line.abreise
                            soa_list.zinr = res_line.zinr
                            soa_list.erwachs = res_line.erwachs
                            soa_list.child1 = res_line.kind1
                            soa_list.child2 = res_line.kind2
                            soa_list.roomrate = res_line.zipreis
                            soa_list.remarks = soa_list.remarks + chr(3) + to_string(res_line.resnr)


                            count_zimm = 0

                            for bresline in db_session.query(Bresline).filter(
                                    (Bresline.resnr == res_line.resnr)).all():
                                count_zimm = count_zimm + res_line.zimmeranz
                                soa_list.zimmeranz = count_zimm

                            zimkateg = db_session.query(Zimkateg).filter(
                                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            if zimkateg:
                                soa_list.remarks = soa_list.remarks + chr(3) + zimkateg.kurzbez + chr(3) + zimkateg.bezeichnung
                            else:
                                soa_list.remarks = soa_list.remarks + chr(3) + chr(3)
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(get_room_breakdown(res_line._recid, res_line.ankunft, 0, date_mdy(get_current_date())))
                            soa_list.remarks = soa_list.remarks + chr(3) + to_string(nett_vat, ">>>,>>>,>>9.99") + chr(3) + to_string(nett_service, ">>>,>>>,>>9.99")
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                str = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(str, 0, 7) == "voucher":
                                    soa_list.voucherNo1 = substring(str, 7)

                            reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == res_line.resnr)).first()

                            if reservation:
                                soa_list.voucherNo2 = reservation.vesrdepot
                    else:
                        soa_list.remarks = soa_list.remarks + chr(3) + chr(3) + chr(3) + chr(3) + chr(3)

                    for billine in db_session.query(Billine).filter(
                            (Billine.rechnr == debitor.rechnr) &  (Billine.anzahl != 0)).all():

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == billine.artnr)).first()

                        if artikel:

                            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                soa_list.gst_tot_sales = soa_list.gst_tot_sales + billine.betrag

                                if artikel.artart == 1:
                                    soa_list.gst_amount = soa_list.gst_amount + (billine.betrag / 1.06)


                                else:

                                    if artikel.mwst_code != 0:
                                        soa_list.gst_amount = soa_list.gst_amount + (billine.betrag / 1.06)

                                    if artikel.mwst_code == 0:
                                        soa_list.gst_tot_non_taxable = soa_list.gst_tot_non_taxable + billine.betrag


                else:

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == debitor.rechnr) &  (H_bill.departement == debitor.betriebsnr)).first()

                    if not h_bill:
                        continue
                    else:

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == debitor.betriebsnr)).first()
                        soa_list.refNo = h_bill.service[5]
                        soa_list.dptnr = debitor.betriebsnr
                        soa_list.outlet = True

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == debitor.gastnrmember)).first()

                        if h_bill.bilname != "":
                            soa_list.name = hoteldpt.depart + " - " + h_bill.bilname
                        else:

                            if gast:
                                soa_list.name = hoteldpt.depart + " - " + Gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                            else:
                                soa_list.name = hoteldpt.depart + " - " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                        if h_bill.service[6] != 0:

                            if len(to_string(h_bill.service[6])) < 8:
                                soa_list.printdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 1)) , to_int(substring(to_string(h_bill.service[6]) , 1, 2)) , to_int(substring(to_string(h_bill.service[6]) , 3, 4)))
                            else:
                                soa_list.printdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 2)) , to_int(substring(to_string(h_bill.service[6]) , 2, 2)) , to_int(substring(to_string(h_bill.service[6]) , 4, 4)))
                        else:
                            soa_list.printdate = get_current_date()

                        if to_int(h_bill.service[5]) != 0:
                            soa_list.inv_str = "INV" + to_string(h_bill.service[5], "9999999")

                        if h_bill.service[5] == 0:
                            soa_list.printed = False
                        else:
                            soa_list.printed = True

                        for hbilline in db_session.query(Hbilline).filter(
                                (Hbilline.rechnr == h_bill.rechnr)).all():

                            h_artikel = db_session.query(H_artikel).filter(
                                    (H_artikel.artnr == hbilline.artnr)).first()

                            if h_artikel:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == h_Artikel.artnrfront)).first()

                                if artikel:

                                    if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                        soa_list.gst_tot_sales = soa_list.gst_tot_sales + hbilline.betrag

                                        if artikel.artart == 1:
                                            soa_list.gst_amount = soa_list.gst_amount + (hbilline.betrag / 1.06)


                                        else:

                                            if artikel.mwst_code != 0:
                                                soa_list.gst_amount = soa_list.gst_amount + (hbilline.betrag / 1.06)

                                            if artikel.mwst_code == 0:
                                                soa_list.gst_tot_non_taxable = soa_list.gst_tot_non_taxable + hbilline.betrag

        elif show_type == 2:

            debitor_obj_list = []
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                    (Debitor.gastnr == guestno) &  (Debitor.opart <= 1) &  (Debitor.saldo != 0) &  (Debitor.zahlkonto == 0)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)


                soa_list = Soa_list()
                soa_list_list.append(soa_list)

                soa_list.to_sort = 1
                soa_list.arRecid = debitor._recid
                soa_list.rechnr = debitor.rechnr
                soa_list.gastnr = debitor.gastnr
                soa_list.datum = debitor.rgdatum
                soa_list.remarks = debitor.vesrcod
                soa_list.dptnr = debitor.betriebsnr
                soa_list.artno = debitor.artnr
                soa_list.counter = debitor.counter
                soa_list.debref = debitor.debref
                soa_list.saldo = soa_list.saldo + debitor.saldo
                soa_list.vesrdep = debitor.vesrdep

            soa_list = query(soa_list_list, filters=(lambda soa_list :soa_list.done_step == 0), first=True)
            while None != soa_list:
                crdt = 0 debt == 0 fcrdt == 0 fdebt == 0
                new_crdt = 0 new_fcrdt == 0
                isprintedb4 = (soa_list.debref > 0)

                for soabuff in query(soabuff_list, filters=(lambda soabuff :soabuff.rechnr == soa_list.rechnr and soabuff.dptnr == soa_list.dptnr and soabuff.artno == soa_list.artno and soabuff.done_step == 0 and soabuff._recid == soa_list._recid)):
                    soabuff.done_step = 1
                    debt = soabuff.saldo
                    fdebt = fdebt + soabuff.vesrdep

                    if soabuff.counter > 0:

                        for debt in db_session.query(debt).filter(
                                (debt.rechnr == soabuff.rechnr) &  (debt.counter == soabuff.counter) &  (debt.gastnr == guestno) &  (debt.zahlkonto > 0)).all():
                            fcrdt = fcrdt + debt.vesrdep
                            crdt = crdt + debt.saldo

                            if isprintedb4 and debt.debref == 0:
                                new_crdt = new_crdt + crdt
                                new_fcrdt = new_fcrdt + fcrdt


                    debt_obj_list = []
                    for debt, artikel in db_session.query(debt, Artikel).join(Artikel,(Artikel.artnr == debt.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                            (debt.rechnr == soabuff.rechnr) &  (debt.gastnr == soabuff.gastnr) &  (debt.betriebsnr == soabuff.dptnr) &  (debt.opart <= 1) &  (soabuff.saldo != 0) &  (debt.zahlkonto == 0) &  (debt._recid != soa_list.arRecid)).all():
                        if debt._recid in debt_obj_list:
                            continue
                        else:
                            debt_obj_list.append(debt._recid)

                        if debt.counter > 0:

                            for debt1 in db_session.query(Debt1).filter(
                                    (Debt1.rechnr == debt.rechnr) &  (Debt1.counter == debt.counter) &  (Debt1.artnr == debt.artnr) &  (debt.gastnr == debitor.gastnr) &  (Debt1.zahlkonto > 0)).all():
                                crdt = crdt + debt.saldo
                                fcrdt = fcrdt + debt.vesrdep

                                if isprintedb4 and debt1.debref == 0:
                                    new_crdt = new_crdt + crdt
                                    new_fcrdt = new_fcrdt + fcrdt

                crdt = - crdt
                fcrdt = - fcrdt
                new_crdt = - new_crdt
                new_fcrdt = - new_fcrdt

                for soabuff in query(soabuff_list, filters=(lambda soabuff :soabuff.done_step == 1)):
                    soabuff.done_step = 2
                    soabuff.debt = debt
                    soabuff.credit = crdt
                    soabuff.saldo = debt - crdt
                    soabuff.fdebt = fdebt
                    soabuff.fcredit = fcrdt
                    soabuff.fsaldo = fdebt - fcrdt
                    soabuff.newpayment = new_crdt
                    soabuff.newfpayment = new_fcrdt

                soa_list = query(soa_list_list, filters=(lambda soa_list :soa_list.done_step == 0), next=True)

            for soa_list in query(soa_list_list):
                zeit = get_current_time_in_seconds()

                debitor = db_session.query(Debitor).filter(
                        (Debitor._recid == soa_list.arRecid)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == debitor.gastnr)).first()

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        continue
                    zeit1 = get_current_time_in_seconds()

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.artnr == debitor.artnr) &  (Bill_line.departement == 0)).first()

                    gast = db_session.query(Gast).filter(
                            (Gast.gastnr == debitor.gastnrmember)).first()
                    soa_list.refNo = debitor.debref
                    soa_list.dptnr = 0

                    if debitor.debref == 0:
                        soa_list.printed = False
                    else:
                        soa_list.printed = True

                    if debitor.debref != 0:
                        soa_list.inv_str = "INV" + to_string(debitor.debref, "9999999")

                    if bill.logidat != None:
                        soa_list.printdate = bill.logidat
                    else:
                        soa_list.printdate = get_current_date()

                    if bill_line:
                        soa_list.voucherno = entry(1, bill_line.bezeich, "/")

                    if gast:
                        soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                    else:
                        soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if bill.resnr > 0:

                        res_line = db_session.query(Res_line).filter(
                                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                        if not res_line:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == bill.resnr)).first()

                        if res_line:
                            soa_list.ankunft = res_line.ankunft
                            soa_list.abreise = res_line.abreise
                            soa_list.zinr = res_line.zinr
                            soa_list.erwachs = res_line.erwachs
                            soa_list.child1 = res_line.kind1
                            soa_list.child2 = res_line.kind2
                            soa_list.roomrate = res_line.zipreis
                            soa_list.remarks = soa_list.remarks + chr(3) + to_string(res_line.resnr)


                            count_zimm = 0

                            for bresline in db_session.query(Bresline).filter(
                                    (Bresline.resnr == res_line.resnr)).all():
                                count_zimm = count_zimm + res_line.zimmeranz
                                soa_list.zimmeranz = count_zimm

                            zimkateg = db_session.query(Zimkateg).filter(
                                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            if zimkateg:
                                soa_list.remarks = soa_list.remarks + chr(3) + zimkateg.kurzbez + chr(3) + zimkateg.bezeichnung
                            else:
                                soa_list.remarks = soa_list.remarks + chr(3) + chr(3)
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(get_room_breakdown(res_line._recid, res_line.ankunft, 0, date_mdy(get_current_date())))
                            soa_list.remarks = soa_list.remarks + chr(3) + to_string(nett_vat, ">>>,>>>,>>9.99") + chr(3) + to_string(nett_service, ">>>,>>>,>>9.99")
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                str = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(str, 0, 7) == "voucher":
                                    soa_list.voucherNo1 = substring(str, 7)

                            reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == res_line.resnr)).first()

                            if reservation:
                                soa_list.voucherNo2 = reservation.vesrdepot
                    else:
                        soa_list.remarks = soa_list.remarks + chr(3) + chr(3) + chr(3) + chr(3) + chr(3)

                    for billine in db_session.query(Billine).filter(
                            (Billine.rechnr == debitor.rechnr) &  (Billine.anzahl != 0)).all():

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == billine.artnr)).first()

                        if artikel:

                            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                soa_list.gst_tot_sales = soa_list.gst_tot_sales + billine.betrag

                                if artikel.artart == 1:
                                    soa_list.gst_amount = soa_list.gst_amount + (billine.betrag / 1.06)


                                else:

                                    if artikel.mwst_code != 0:
                                        soa_list.gst_amount = soa_list.gst_amount + (billine.betrag / 1.06)

                                    if artikel.mwst_code == 0:
                                        soa_list.gst_tot_non_taxable = soa_list.gst_tot_non_taxable + billine.betrag


                else:

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == debitor.rechnr) &  (H_bill.departement == debitor.betriebsnr)).first()

                    if not h_bill:
                        continue
                    else:

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == debitor.betriebsnr)).first()
                        soa_list.refNo = h_bill.service[5]
                        soa_list.dptnr = debitor.betriebsnr
                        soa_list.outlet = True

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == debitor.gastnrmember)).first()

                        if h_bill.bilname != "":
                            soa_list.name = hoteldpt.depart + " - " + h_bill.bilname
                        else:

                            if gast:
                                soa_list.name = hoteldpt.depart + " - " + Gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                            else:
                                soa_list.name = hoteldpt.depart + " - " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                        if h_bill.service[6] != 0:

                            if len(to_string(h_bill.service[6])) < 8:
                                soa_list.printdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 1)) , to_int(substring(to_string(h_bill.service[6]) , 1, 2)) , to_int(substring(to_string(h_bill.service[6]) , 3, 4)))
                            else:
                                soa_list.printdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 2)) , to_int(substring(to_string(h_bill.service[6]) , 2, 2)) , to_int(substring(to_string(h_bill.service[6]) , 4, 4)))
                        else:
                            soa_list.printdate = get_current_date()

                        if to_int(h_bill.service[5]) != 0:
                            soa_list.inv_str = "INV" + to_string(h_bill.service[5], "9999999")

                        if h_bill.service[5] == 0:
                            soa_list.printed = False
                        else:
                            soa_list.printed = True

                        for hbilline in db_session.query(Hbilline).filter(
                                (Hbilline.rechnr == h_bill.rechnr)).all():

                            h_artikel = db_session.query(H_artikel).filter(
                                    (H_artikel.artnr == hbilline.artnr)).first()

                            if h_artikel:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == h_Artikel.artnrfront)).first()

                                if artikel:

                                    if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                        soa_list.gst_tot_sales = soa_list.gst_tot_sales + hbilline.betrag

                                        if artikel.artart == 1:
                                            soa_list.gst_amount = soa_list.gst_amount + (hbilline.betrag / 1.06)


                                        else:

                                            if artikel.mwst_code != 0:
                                                soa_list.gst_amount = soa_list.gst_amount + (hbilline.betrag / 1.06)

                                            if artikel.mwst_code == 0:
                                                soa_list.gst_tot_non_taxable = soa_list.gst_tot_non_taxable + hbilline.betrag


        else:
            param4 = call_paramar(4)

            if param4 == "":
                due_date = curr_day
            else:
                var_param = substring(param4, len(param4) - 1, 1)
                val_param = to_int(substring(param4, 0, len(param4) - 1))

                if var_param.lower()  == "D" or var_param.lower()  == "d":
                    due_date = eof_month + val_param

                elif var_param.lower()  == "M" or var_param.lower()  == "m":
                    nmonth = get_month(eof_month) + val_param

                    if nmonth > 12:
                        mnth1 = 1
                        year2 = get_year(eof_month) + 1


                    else:
                        mnth1 = nmonth
                        year2 = get_year(eof_month)


                    due_date = lastdate_inmonth(mnth1, year2)

                elif var_param.lower()  == "Y" or var_param.lower()  == "y":
                    mnth1 = get_month(eof_month)
                    year2 = get_year(eof_month) + val_param


                    due_date = lastdate_inmonth(mnth1, year2)
                else:
                    mnth1 = get_month(eof_month)
                    year2 = get_year(eof_month)


                    due_date = lastdate_inmonth(mnth1, year2)

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.gastnr == guestno) &  (Debitor.zahlkonto == 0) &  (Debitor.saldo != 0) &  (Debitor.rgdatum < bof_month)).all():
                saldo1 = saldo1 + debitor.saldo

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.gastnr == guestno) &  (Debitor.zahlkonto > 0) &  (Debitor.rgdatum < bof_month) &  (Debitor.saldo != 0) &  (Debitor.opart <= 2)).all():
                saldo2 = saldo2 + debitor.saldo

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.gastnr == guestno) &  (Debitor.zahlkonto > 0) &  (Debitor.rgdatum >= bof_month) &  (Debitor.rgdatum <= eof_month) &  (Debitor.saldo != 0) &  (Debitor.opart <= 2)).all():
                saldo4 = saldo4 + debitor.saldo
            param2 = call_paramar(2)
            soa_list = Soa_list()
            soa_list_list.append(soa_list)

            soa_list.to_sort = 0
            soa_list.name = param2
            soa_list.debt = 0
            soa_list.credit = 0
            soa_list.saldo = saldo1 + saldo2
            soa_list.fsaldo = saldo1 + saldo2


            param1 = call_paramar(1)

            if param1.lower()  == ("YES").lower():
                counter_saldo = counter_saldo + saldo1 + saldo2
            else:
                counter_saldo = 0

            debitor_obj_list = []
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                    (Debitor.gastnr == guestno) &  (Debitor.saldo != 0) &  (Debitor.zahlkonto == 0) &  (Debitor.rgdatum >= bof_month) &  (Debitor.rgdatum <= eof_month)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)

                if param1.lower()  == ("YES").lower():
                    counter_saldo = counter_saldo + debitor.saldo
                else:
                    counter_saldo = debitor.saldo
                soa_list = Soa_list()
                soa_list_list.append(soa_list)

                soa_list.to_sort = 1
                soa_list.arRecid = debitor._recid
                soa_list.rechnr = debitor.rechnr
                soa_list.gastnr = debitor.gastnr
                soa_list.datum = debitor.rgdatum
                soa_list.remarks = debitor.vesrcod
                soa_list.dptnr = debitor.betriebsnr
                soa_list.debt = debitor.saldo
                soa_list.credit = 0
                soa_list.saldo = counter_saldo
                soa_list.fsaldo = counter_saldo

            for soa_list in query(soa_list_list):
                debitor = db_session.query(Debitor).filter((to_int(Debitor._recid) == soa_list.arRecid)).first()
                if not debitor:
                    continue

                guest = db_session.query(Guest).filter((Guest.gastnr == debitor.gastnr)).first()
                if not guest:
                    continue

                crdt = 0 debt == 0 fcrdt == 0 fdebt == 0
                new_crdt = 0 new_fcrdt == 0 isprintedb4 == True

                if debitor.debref != 0:
                    isprintedb4 = True
                debt = debitor.saldo
                fdebt = debitor.vesrdep

                if debitor.counter > 0:

                    for debt in db_session.query(debt).filter(
                            (debt.rechnr == debitor.rechnr) &  (debt.counter == debitor.counter) &  (debt.artnr == debitor.artnr) &  (debt.betriebsnr == debitor.betriebsnr) &  (debt.gastnr == debitor.gastnr) &  (debt.zahlkonto > 0)).all():
                        fcrdt = fcrdt + debt.vesrdep
                        crdt = crdt + debt.saldo

                        if isprintedb4 and debt.debref == 0:
                            new_crdt = new_crdt + crdt
                            new_fcrdt = new_fcrdt + fcrdt


                debt_obj_list = []
                for debt, artikel in db_session.query(debt, Artikel).join(Artikel,(Artikel.artnr == debt.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                        (debt.rechnr == debitor.rechnr) &  (debt.gastnr == debitor.gastnr) &  (debt.betriebsnr == debitor.betriebsnr) &  (debt.opart <= 1) &  (debitor.saldo != 0) &  (debt.zahlkonto == 0) &  (debt._recid != debitor._recid)).all():
                    if debt._recid in debt_obj_list:
                        continue
                    else:
                        debt_obj_list.append(debt._recid)


                    debt = debt + debt.saldo
                    fdebt = fdebt + debt.vesrdep

                    if debt.counter > 0:

                        for debt1 in db_session.query(Debt1).filter(
                                (Debt1.rechnr == debt.rechnr) &  (Debt1.counter == debt.counter) &  (Debt1.artnr == debt.artnr) &  (debt.gastnr == debitor.gastnr) &  (Debt1.zahlkonto > 0)).all():
                            crdt = crdt + debt.saldo
                            fcrdt = fcrdt + debt.vesrdep

                            if isprintedb4 and debt1.debref == 0:
                                new_crdt = new_crdt + crdt
                                new_fcrdt = new_fcrdt + fcrdt

                crdt = - crdt
                fcrdt = - fcrdt
                new_crdt = - new_crdt
                new_fcrdt = - new_fcrdt

                if debitor.betriebsnr == 0:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        rech_nr = debitor.rechnr
                        bet_nr = debitor.betriebsnr
                        msg_int = 1
                        continue

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr == artikel.artnr) &  (Bill_line.departement == 0)).first()

                    gast = db_session.query(Gast).filter(
                            (Gast.gastnr == debitor.gastnrmember)).first()
                    soa_list.refNo = billref
                    soa_list.dptnr = 0

                    if billref == 0:
                        soa_list.printed = False
                    else:
                        soa_list.printed = True

                    if bill.logidat != None:
                        soa_list.printdate = bill.logidat
                    else:
                        soa_list.printdate = get_current_date()

                    if billref != 0:
                        soa_list.inv_str = "INV" + to_string(billref, "9999999")

                    if bill_line:
                        soa_list.voucherno = entry(1, bill_line.bezeich, "/")

                    if gast:
                        soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                    else:
                        soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                    if not res_line:

                        res_line = db_session.query(Res_line).filter(
                                (Res_line.resnr == bill.resnr)).first()

                    if res_line:
                        soa_list.ankunft = res_line.ankunft
                        soa_list.abreise = res_line.abreise
                        soa_list.zinr = res_line.zinr
                        soa_list.erwachs = res_line.erwachs
                        soa_list.child1 = res_line.kind1
                        soa_list.child2 = res_line.kind2
                        soa_list.roomrate = res_line.zipreis
                        soa_list.remarks = soa_list.remarks + chr(3) + to_string(res_line.resnr)


                        count_zimm = 0

                        for bresline in db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr)).all():
                            count_zimm = count_zimm + res_line.zimmeranz
                            soa_list.zimmeranz = count_zimm

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            soa_list.remarks = soa_list.remarks + chr(3) + zimkateg.kurzbez + chr(3) + zimkateg.bezeichnung
                        else:
                            soa_list.remarks = soa_list.remarks + chr(3) + chr(3)
                        fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(get_room_breakdown(res_line._recid, res_line.ankunft, 0, date_mdy(get_current_date())))
                        soa_list.remarks = soa_list.remarks + chr(3) + to_string(nett_vat, ">>>,>>>,>>9.99") + chr(3) + to_string(nett_service, ">>>,>>>,>>9.99")
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 7) == "voucher":
                                soa_list.voucherNo1 = substring(str, 7)

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        if reservation:
                            soa_list.voucherNo2 = reservation.vesrdepot
                    else:
                        soa_list.remarks = soa_list.remarks + chr(3) + chr(3) + chr(3) + chr(3) + chr(3)

                    for billine in db_session.query(Billine).filter(
                            (Billine.rechnr == debitor.rechnr) &  (Billine.anzahl != 0)).all():

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == billine.artnr)).first()

                        if artikel:

                            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                soa_list.gst_tot_sales = soa_list.gst_tot_sales + billine.betrag

                                if artikel.artart == 1:
                                    soa_list.gst_amount = soa_list.gst_amount + (billine.betrag / 1.06)


                                else:

                                    if artikel.mwst_code != 0:
                                        soa_list.gst_amount = soa_list.gst_amount + (billine.betrag / 1.06)

                                    if artikel.mwst_code == 0:
                                        soa_list.gst_tot_non_taxable = soa_list.gst_tot_non_taxable + billine.betrag


                else:

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == debitor.rechnr) &  (H_bill.departement == debitor.betriebsnr)).first()

                    if not h_bill:
                        rech_nr = debitor.rechnr
                        bet_nr = debitor.betriebsnr
                        msg_int = 2
                        continue
                    else:

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == debitor.betriebsnr)).first()
                        soa_list.refNo = h_bill.service[5]
                        soa_list.dptnr = debitor.betriebsnr
                        soa_list.outlet = True

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == debitor.gastnrmember)).first()

                        if h_bill.bilname != "":
                            soa_list.name = hoteldpt.depart + " - " + h_bill.bilname
                        else:

                            if gast:
                                soa_list.name = hoteldpt.depart + " - " + Gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                            else:
                                soa_list.name = hoteldpt.depart + " - " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                        if h_bill.service[6] != 0:

                            if len(to_string(h_bill.service[6])) < 8:
                                soa_list.printdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 1)) , to_int(substring(to_string(h_bill.service[6]) , 1, 2)) , to_int(substring(to_string(h_bill.service[6]) , 3, 4)))
                            else:
                                soa_list.printdate = date_mdy(to_int(substring(to_string(h_bill.service[6]) , 0, 2)) , to_int(substring(to_string(h_bill.service[6]) , 2, 2)) , to_int(substring(to_string(h_bill.service[6]) , 4, 4)))
                        else:
                            soa_list.printdate = get_current_date()

                        if to_int(h_bill.service[5]) != 0:
                            soa_list.inv_str = "INV" + to_string(h_bill.service[5], "9999999")

                        if h_bill.service[5] == 0:
                            soa_list.printed = False
                        else:
                            soa_list.printed = True

                        for hbilline in db_session.query(Hbilline).filter(
                                (Hbilline.rechnr == h_bill.rechnr)).all():

                            h_artikel = db_session.query(H_artikel).filter(
                                    (H_artikel.artnr == hbilline.artnr)).first()

                            if h_artikel:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == h_Artikel.artnrfront)).first()

                                if artikel:

                                    if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                        soa_list.gst_tot_sales = soa_list.gst_tot_sales + hbilline.betrag

                                        if artikel.artart == 1:
                                            soa_list.gst_amount = soa_list.gst_amount + (hbilline.betrag / 1.06)


                                        else:

                                            if artikel.mwst_code != 0:
                                                soa_list.gst_amount = soa_list.gst_amount + (hbilline.betrag / 1.06)

                                            if artikel.mwst_code == 0:
                                                soa_list.gst_tot_non_taxable = soa_list.gst_tot_non_taxable + hbilline.betrag

        if show_type == 1:
            param3 = call_paramar(3)

            if param1.lower()  == ("YES").lower():
                counter_saldo = counter_saldo + saldo3 + saldo4
            else:
                counter_saldo = saldo3 + saldo4
            soa_list = Soa_list()
            soa_list_list.append(soa_list)

            soa_list.to_sort = 2
            soa_list.name = param3
            soa_list.debt = 0
            soa_list.credit = saldo3 + saldo4
            soa_list.saldo = counter_saldo
            soa_list.fsaldo = counter_saldo

        for soa_list in query(soa_list_list, filters=(lambda soa_list :soa_list.saldo == 0 and soa_list.to_sort == 1)):
            soa_list_list.remove(soa_list)

    def call_paramar(nr:int):

        nonlocal zeit, zeit1, str, due_date, soa_list_list, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, bresline, zimkateg, reservation, h_bill, hoteldpt, h_artikel
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt
        nonlocal soa_list_list, param_ar_list

        param_val = ""

        def generate_inner_output():
            return param_val

        param_ar = query(param_ar_list, filters=(lambda param_ar :param_ar.param_nr == nr), first=True)

        if param_ar:
            param_val = param_ar.param_val
        else:
            param_val = ""


        return generate_inner_output()

    def lastdate_inmonth(imonth:int, iyear:int):

        nonlocal zeit, zeit1, str, due_date, soa_list_list, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, bresline, zimkateg, reservation, h_bill, hoteldpt, h_artikel
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline, bdebt, bdebt1, debbt
        nonlocal soa_list_list, param_ar_list

        lastdate = None
        newmonth:int = 0
        newyear:int = 0
        newdate:date = None

        def generate_inner_output():
            return lastdate
        newmonth = imonth + 1

        if newmonth > 12:
            newmonth = newmonth - 12
            newyear = iyear + 1
            newdate = date_mdy(newmonth, 1, newyear)
            lastdate = newdate - 1
        else:
            newdate = date_mdy(newmonth , 1, iyear)
            lastdate = newdate - 1


        return generate_inner_output()

    create_soalist()

    return generate_output()