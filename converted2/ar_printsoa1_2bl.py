#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Guest, Bill, Debitor, Bill_line, H_bill_line, Res_line, Artikel, Queasy, Reservation, Zimkateg, H_bill, Hoteldpt, H_artikel

param_ar_data, Param_ar = create_model("Param_ar", {"param_nr":int, "param_name":string, "param_val":string, "param_type":string})

def ar_printsoa1_2bl(show_type:int, bof_month:date, eof_month:date, param_ar_data:[Param_ar], guestno:int, curr_day:date, dollar_rate:Decimal):

    prepare_cache ([Guest, Bill, Debitor, Bill_line, H_bill_line, Res_line, Artikel, Queasy, Reservation, Zimkateg, H_bill, Hoteldpt, H_artikel])

    zeit:int = 0
    zeit1:int = 0
    str:string = ""
    due_date = get_current_date()
    soa_list_data = []
    rech_nr = 0
    bet_nr = 0
    msg_int = 0
    param1:string = ""
    param2:string = ""
    param3:string = ""
    param4:string = ""
    fnet_lodging:Decimal = to_decimal("0.0")
    lnet_lodging:Decimal = to_decimal("0.0")
    net_breakfast:Decimal = to_decimal("0.0")
    net_lunch:Decimal = to_decimal("0.0")
    net_dinner:Decimal = to_decimal("0.0")
    net_others:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    nett_vat:Decimal = to_decimal("0.0")
    nett_service:Decimal = to_decimal("0.0")
    curr_gastnr:int = 0
    curr_refno:int = 0
    new_refno:int = 0
    cl_exist:bool = False
    saldo:Decimal = to_decimal("0.0")
    s:string = ""
    i:int = 0
    arrival:date = None
    departure:date = None
    debt:Decimal = to_decimal("0.0")
    crdt:Decimal = to_decimal("0.0")
    fdebt:Decimal = to_decimal("0.0")
    fcrdt:Decimal = to_decimal("0.0")
    new_crdt:Decimal = to_decimal("0.0")
    new_fcrdt:Decimal = to_decimal("0.0")
    isprintedb4:bool = False
    saldo1:Decimal = to_decimal("0.0")
    saldo2:Decimal = to_decimal("0.0")
    saldo3:Decimal = to_decimal("0.0")
    saldo4:Decimal = to_decimal("0.0")
    other_flag:bool = False
    count_zimm:int = 0
    t_voucherno:string = ""
    nmonth:int = 0
    mnth1:int = 0
    year2:int = 0
    val_param:int = 0
    var_param:string = ""
    guest = bill = debitor = bill_line = h_bill_line = res_line = artikel = queasy = reservation = zimkateg = h_bill = hoteldpt = h_artikel = None

    soa_list = soabuff = param_ar = gast = bill1 = debt = debt1 = billine = hbilline = bresline = None

    soa_list_data, Soa_list = create_model("Soa_list", {"counter":int, "debref":int, "done_step":int, "artno":int, "vesrdep":Decimal, "to_sort":int, "outlet":bool, "datum":date, "ankunft":date, "abreise":date, "gastnr":int, "name":string, "inv_str":string, "rechnr":int, "refno":int, "voucherno":string, "voucherno1":string, "voucherno2":string, "saldo":Decimal, "fsaldo":Decimal, "printed":bool, "selected":bool, "printdate":date, "dptnr":int, "debt":Decimal, "credit":Decimal, "fdebt":Decimal, "fcredit":Decimal, "remarks":string, "arrecid":int, "newpayment":Decimal, "newfpayment":Decimal, "zinr":string, "erwachs":int, "child1":int, "child2":int, "roomrate":Decimal, "tot_amount":Decimal, "tot_balance":Decimal, "exrate":Decimal, "tot_exrate":Decimal, "gst_tot_non_taxable":Decimal, "gst_amount":Decimal, "gst_tot_sales":Decimal, "zimmeranz":int, "ar_flag":int, "foreign_exchg":Decimal, "resv_name":string, "voucher_res_line":string}, {"printdate": get_current_date()})

    Soabuff = Soa_list
    soabuff_data = soa_list_data

    Gast = create_buffer("Gast",Guest)
    Bill1 = create_buffer("Bill1",Bill)
    debt = create_buffer("debt",Debitor)
    Debt1 = create_buffer("Debt1",Debitor)
    Billine = create_buffer("Billine",Bill_line)
    Hbilline = create_buffer("Hbilline",H_bill_line)
    Bresline = create_buffer("Bresline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zeit, zeit1, str, due_date, soa_list_data, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, t_voucherno, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, reservation, zimkateg, h_bill, hoteldpt, h_artikel
        nonlocal show_type, bof_month, eof_month, guestno, curr_day, dollar_rate
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline
        nonlocal soa_list_data

        return {"param-ar": param_ar_data, "due_date": due_date, "soa-list": soa_list_data, "rech_nr": rech_nr, "bet_nr": bet_nr, "msg_int": msg_int}

    def create_soalist():

        nonlocal zeit, zeit1, str, due_date, soa_list_data, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, t_voucherno, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, reservation, zimkateg, h_bill, hoteldpt, h_artikel
        nonlocal show_type, bof_month, eof_month, guestno, curr_day, dollar_rate
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline
        nonlocal soa_list_data

        bdebt = None
        bdebt1 = None
        debbt = None
        nmonth:int = 0
        mnth1:int = 0
        year2:int = 0
        counter_saldo:Decimal = to_decimal("0.0")
        val_param:int = 0
        var_param:string = ""
        Bdebt =  create_buffer("Bdebt",Debitor)
        Bdebt1 =  create_buffer("Bdebt1",Debitor)
        soa_list_data.clear()

        if show_type == 0:

            debitor_obj_list = {}
            debitor = Debitor()
            artikel = Artikel()
            for debitor.gastnr, debitor.rechnr, debitor.betriebsnr, debitor._recid, debitor.rgdatum, debitor.vesrcod, debitor.artnr, debitor.counter, debitor.debref, debitor.saldo, debitor.vesrdep, debitor.gastnrmember, debitor.zahlkonto, debitor.opart, artikel.artart, artikel.artnr, artikel.mwst_code, artikel._recid in db_session.query(Debitor.gastnr, Debitor.rechnr, Debitor.betriebsnr, Debitor._recid, Debitor.rgdatum, Debitor.vesrcod, Debitor.artnr, Debitor.counter, Debitor.debref, Debitor.saldo, Debitor.vesrdep, Debitor.gastnrmember, Debitor.zahlkonto, Debitor.opart, Artikel.artart, Artikel.artnr, Artikel.mwst_code, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                     (Debitor.gastnr == guestno) & (Debitor.opart <= 1) & (Debitor.saldo != 0) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True

                soa_list = query(soa_list_data, filters=(lambda soa_list: soa_list.gastnr == debitor.gastnr and soa_list.rechnr == debitor.rechnr and soa_list.dptnr == debitor.betriebsnr), first=True)

                if not soa_list:
                    soa_list = Soa_list()
                    soa_list_data.append(soa_list)

                    soa_list.to_sort = 1
                    soa_list.arrecid = debitor._recid
                    soa_list.rechnr = debitor.rechnr
                    soa_list.gastnr = debitor.gastnr
                    soa_list.datum = debitor.rgdatum
                    soa_list.remarks = debitor.vesrcod
                    soa_list.dptnr = debitor.betriebsnr
                    soa_list.artno = debitor.artnr
                    soa_list.counter = debitor.counter
                    soa_list.debref = debitor.debref
                    soa_list.saldo =  to_decimal(soa_list.saldo) + to_decimal(debitor.saldo)
                    soa_list.vesrdep =  to_decimal(debitor.vesrdep)
                    soa_list.foreign_exchg =  to_decimal(soa_list.saldo) / to_decimal(dollar_rate)


            Debbt =  create_buffer("Debbt",Debitor)

            soa_list = query(soa_list_data, filters=(lambda soa_list: soa_list.done_step == 0), first=True)
            while None != soa_list:
                crdt = 0 debt == 0 fcrdt == 0 fdebt == 0
                new_crdt = 0 new_fcrdt == 0
                isprintedb4 = (soa_list.debref > 0)

                for soabuff in query(soabuff_data, filters=(lambda soabuff: soabuff.rechnr == soa_list.rechnr and soabuff.dptnr == soa_list.dptnr and soabuff.artno == soa_list.artno and soabuff.done_step == 0)):
                    soabuff.done_step = 1
                    debt =  to_decimal(soabuff.saldo)
                    fdebt =  to_decimal(fdebt) + to_decimal(soabuff.vesrdep)

                    if soabuff.counter > 0:

                        for debt in db_session.query(debt).filter(
                                 (debt.rechnr == soabuff.rechnr) & (debt.counter == soabuff.counter) & (debt.gastnr == guestno) & (debt.zahlkonto > 0)).order_by(debt._recid).all():
                            fcrdt =  to_decimal(fcrdt) + to_decimal(debt.vesrdep)
                            crdt =  to_decimal(crdt) + to_decimal(debt.saldo)

                            if isprintedb4 and debt.debref == 0:
                                new_crdt =  to_decimal(new_crdt) + to_decimal(crdt)
                                new_fcrdt =  to_decimal(new_fcrdt) + to_decimal(fcrdt)


                    debt_obj_list = {}
                    debt = Debitor()
                    artikel = Artikel()
                    for debt.gastnr, debt.rechnr, debt.betriebsnr, debt._recid, debt.rgdatum, debt.vesrcod, debt.artnr, debt.counter, debt.debref, debt.saldo, debt.vesrdep, debt.gastnrmember, debt.zahlkonto, debt.opart, artikel.artart, artikel.artnr, artikel.mwst_code, artikel._recid in db_session.query(debt.gastnr, debt.rechnr, debt.betriebsnr, debt._recid, debt.rgdatum, debt.vesrcod, debt.artnr, debt.counter, debt.debref, debt.saldo, debt.vesrdep, debt.gastnrmember, debt.zahlkonto, debt.opart, Artikel.artart, Artikel.artnr, Artikel.mwst_code, Artikel._recid).join(Artikel,(Artikel.artnr == debt.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                             (debt.rechnr == soabuff.rechnr) & (debt.gastnr == soabuff.gastnr) & (debt.betriebsnr == soabuff.dptnr) & (debt.opart <= 1) & (soabuff.saldo != 0) & (debt.zahlkonto == 0) & (debt._recid != soa_list.arrecid)).order_by(debt._recid).all():
                        if debt_obj_list.get(debt._recid):
                            continue
                        else:
                            debt_obj_list[debt._recid] = True


                        debt =  to_decimal(debt) + to_decimal(debt.saldo)
                        fdebt =  to_decimal(fdebt) + to_decimal(debt.vesrdep)

                        if debt.counter > 0:

                            for debt1 in db_session.query(Debt1).filter(
                                     (Debt1.rechnr == debt.rechnr) & (Debt1.counter == debt.counter) & (Debt1.artnr == debt.artnr) & (Debt1.gastnr == debitor.gastnr) & (Debt1.zahlkonto > 0)).order_by(debt.rgdatum).all():
                                crdt =  to_decimal(crdt) + to_decimal(debt.saldo)
                                fcrdt =  to_decimal(fcrdt) + to_decimal(debt.vesrdep)

                                if isprintedb4 and debt1.debref == 0:
                                    new_crdt =  to_decimal(new_crdt) + to_decimal(crdt)
                                    new_fcrdt =  to_decimal(new_fcrdt) + to_decimal(fcrdt)

                crdt =  - to_decimal(crdt)
                fcrdt =  - to_decimal(fcrdt)
                new_crdt =  - to_decimal(new_crdt)
                new_fcrdt =  - to_decimal(new_fcrdt)

                for soabuff in query(soabuff_data, filters=(lambda soabuff: soabuff.done_step == 1)):
                    soabuff.done_step = 2
                    soabuff.debt =  to_decimal(debt)
                    soabuff.credit =  to_decimal(crdt)
                    soabuff.saldo =  to_decimal(debt) - to_decimal(crdt)
                    soabuff.fdebt =  to_decimal(fdebt)
                    soabuff.fcredit =  to_decimal(fcrdt)
                    soabuff.fsaldo =  to_decimal(fdebt) - to_decimal(fcrdt)
                    soabuff.newpayment =  to_decimal(new_crdt)
                    soabuff.newfpayment =  to_decimal(new_fcrdt)
                    soabuff.foreign_exchg =  to_decimal(soabuff.saldo) / to_decimal(dollar_rate)

                soa_list = query(soa_list_data, filters=(lambda soa_list: soa_list.done_step == 0), next=True)

            for soa_list in query(soa_list_data):
                zeit = get_current_time_in_seconds()

                debitor = get_cache (Debitor, {"_recid": [(eq, soa_list.arrecid)]})

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if not bill:

                        if debitor.debref != 0:

                            queasy = get_cache (Queasy, {"key": [(eq, 192)],"number1": [(eq, debitor.rechnr)]})

                            if queasy:
                                soa_list.printed = True
                                soa_list.refno = debitor.debref
                                soa_list.inv_str = "INV" + to_string(queasy.number2, "9999999")

                            elif not queasy:
                                soa_list.printed = False

                        gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if gast:
                            soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:

                            guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                            if guest:
                                soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        soa_list.ar_flag = 2
                        continue
                    zeit1 = get_current_time_in_seconds()
                    other_flag = False


                    soa_list.ar_flag = 1

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"artnr": [(eq, debitor.artnr)],"departement": [(eq, 0)]})
                    soa_list.refno = bill.billref
                    soa_list.dptnr = 0

                    if bill.billref != 0:

                        bdebt = get_cache (Debitor, {"rechnr": [(eq, soa_list.rechnr)],"debref": [(ne, 0)],"counter": [(eq, soa_list.counter)]})

                        if bdebt:
                            soa_list.saldo =  to_decimal(soa_list.saldo) - to_decimal(bdebt.saldo)
                            soa_list.debt =  to_decimal(soa_list.debt) - to_decimal(bdebt.saldo)
                            soa_list.foreign_exchg =  to_decimal(soa_list.saldo) / to_decimal(dollar_rate)

                            if soa_list.saldo != 0:

                                bdebt1 = get_cache (Debitor, {"debref": [(eq, 0)],"rechnr": [(eq, soa_list.rechnr)]})

                                if bdebt1:
                                    soa_list.arrecid = bdebt1._recid
                                    other_flag = True

                    if bill.billref == 0:
                        soa_list.printed = False
                    else:

                        if other_flag :

                            queasy = get_cache (Queasy, {"key": [(eq, 192)],"number1": [(eq, debitor.rechnr)]})

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

                    if bill.billref != 0:
                        soa_list.inv_str = "INV" + to_string(bill.billref, "9999999")

                    if bill_line:
                        soa_list.voucherno = entry(1, bill_line.bezeich, "/")

                    gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if gast:
                        soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                    else:

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                        if guest:
                            soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if bill.resnr > 0:

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                        if not res_line:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)]})

                        if res_line:
                            soa_list.ankunft = res_line.ankunft
                            soa_list.abreise = res_line.abreise
                            soa_list.zinr = res_line.zinr
                            soa_list.erwachs = res_line.erwachs
                            soa_list.child1 = res_line.kind1
                            soa_list.child2 = res_line.kind2
                            soa_list.roomrate =  to_decimal(res_line.zipreis)
                            soa_list.remarks = soa_list.remarks + chr_unicode(3) + to_string(res_line.resnr)


                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                t_voucherno = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(t_voucherno, 0, 7) == ("voucher").lower() :
                                    soa_list.voucher_res_line = substring(t_voucherno, 7)

                            if soa_list.voucher_res_line == "":

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                if reservation:
                                    soa_list.voucher_res_line = reservation.vesrdepot


                            count_zimm = 0

                            for bresline in db_session.query(Bresline).filter(
                                     (Bresline.resnr == res_line.resnr)).order_by(Bresline._recid).all():
                                count_zimm = count_zimm + res_line.zimmeranz
                                soa_list.zimmeranz = count_zimm

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                            if zimkateg:
                                soa_list.remarks = soa_list.remarks + chr_unicode(3) + zimkateg.kurzbez + chr_unicode(3) + zimkateg.bezeichnung
                            else:
                                soa_list.remarks = soa_list.remarks + chr_unicode(3) + chr_unicode(3)
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(get_room_breakdown(res_line._recid, res_line.ankunft, 0, date_mdy(get_current_date())))
                            soa_list.remarks = soa_list.remarks + chr_unicode(3) + to_string(nett_vat, ">>>,>>>,>>9.99") + chr_unicode(3) + to_string(nett_service, ">>>,>>>,>>9.99")
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                str = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(str, 0, 7) == ("voucher").lower() :
                                    soa_list.voucherno1 = substring(str, 7)

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            if reservation:
                                soa_list.voucherno2 = reservation.vesrdepot
                                soa_list.resv_name = reservation.name


                    else:
                        soa_list.remarks = soa_list.remarks + chr_unicode(3) + chr_unicode(3) + chr_unicode(3) + chr_unicode(3) + chr_unicode(3)


                        soa_list.resv_name = bill.bilname

                    for billine in db_session.query(Billine).filter(
                             (Billine.rechnr == debitor.rechnr) & (Billine.anzahl != 0)).order_by(Billine._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, billine.artnr)]})

                        if artikel:

                            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                soa_list.gst_tot_sales =  to_decimal(soa_list.gst_tot_sales) + to_decimal(billine.betrag)

                                if artikel.artart == 1:
                                    soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((billine.betrag) / to_decimal(1.06) )


                                else:

                                    if artikel.mwst_code != 0:
                                        soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((billine.betrag) / to_decimal(1.06) )

                                    if artikel.mwst_code == 0:
                                        soa_list.gst_tot_non_taxable =  to_decimal(soa_list.gst_tot_non_taxable) + to_decimal(billine.betrag)


                else:

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, debitor.rechnr)],"departement": [(eq, debitor.betriebsnr)]})

                    if not h_bill:
                        continue
                    else:
                        soa_list.ar_flag = 1

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, debitor.betriebsnr)]})
                        soa_list.refno = h_bill.service[5]
                        soa_list.dptnr = debitor.betriebsnr
                        soa_list.outlet = True

                        gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if h_bill.bilname != "":
                            soa_list.name = hoteldpt.depart + " - " + h_bill.bilname
                        else:

                            if gast:
                                soa_list.name = hoteldpt.depart + " - " + Gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                            else:
                                soa_list.name = hoteldpt.depart + " - " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                        if h_bill.service[6] != 0:

                            if length(to_string(h_bill.service[6])) < 8:
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
                                 (Hbilline.rechnr == h_bill.rechnr)).order_by(Hbilline._recid).all():

                            h_artikel = get_cache (H_artikel, {"artnr": [(eq, hbilline.artnr)]})

                            if h_artikel:

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)]})

                                if artikel:

                                    if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                        soa_list.gst_tot_sales =  to_decimal(soa_list.gst_tot_sales) + to_decimal(hbilline.betrag)

                                        if artikel.artart == 1:
                                            soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((hbilline.betrag) / to_decimal(1.06) )


                                        else:

                                            if artikel.mwst_code != 0:
                                                soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((hbilline.betrag) / to_decimal(1.06) )

                                            if artikel.mwst_code == 0:
                                                soa_list.gst_tot_non_taxable =  to_decimal(soa_list.gst_tot_non_taxable) + to_decimal(hbilline.betrag)

        elif show_type == 2:

            debitor_obj_list = {}
            debitor = Debitor()
            artikel = Artikel()
            for debitor.gastnr, debitor.rechnr, debitor.betriebsnr, debitor._recid, debitor.rgdatum, debitor.vesrcod, debitor.artnr, debitor.counter, debitor.debref, debitor.saldo, debitor.vesrdep, debitor.gastnrmember, debitor.zahlkonto, debitor.opart, artikel.artart, artikel.artnr, artikel.mwst_code, artikel._recid in db_session.query(Debitor.gastnr, Debitor.rechnr, Debitor.betriebsnr, Debitor._recid, Debitor.rgdatum, Debitor.vesrcod, Debitor.artnr, Debitor.counter, Debitor.debref, Debitor.saldo, Debitor.vesrdep, Debitor.gastnrmember, Debitor.zahlkonto, Debitor.opart, Artikel.artart, Artikel.artnr, Artikel.mwst_code, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                     (Debitor.gastnr == guestno) & (Debitor.opart <= 1) & (Debitor.saldo != 0) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                soa_list = Soa_list()
                soa_list_data.append(soa_list)

                soa_list.to_sort = 1
                soa_list.arrecid = debitor._recid
                soa_list.rechnr = debitor.rechnr
                soa_list.gastnr = debitor.gastnr
                soa_list.datum = debitor.rgdatum
                soa_list.remarks = debitor.vesrcod
                soa_list.dptnr = debitor.betriebsnr
                soa_list.artno = debitor.artnr
                soa_list.counter = debitor.counter
                soa_list.debref = debitor.debref
                soa_list.saldo =  to_decimal(soa_list.saldo) + to_decimal(debitor.saldo)
                soa_list.vesrdep =  to_decimal(debitor.vesrdep)
                soa_list.foreign_exchg =  to_decimal(soa_list.saldo) / to_decimal(dollar_rate)

            soa_list = query(soa_list_data, filters=(lambda soa_list: soa_list.done_step == 0), first=True)
            while None != soa_list:
                crdt = 0 debt == 0 fcrdt == 0 fdebt == 0
                new_crdt = 0 new_fcrdt == 0
                isprintedb4 = (soa_list.debref > 0)

                for soabuff in query(soabuff_data, filters=(lambda soabuff: soabuff.rechnr == soa_list.rechnr and soabuff.dptnr == soa_list.dptnr and soabuff.artno == soa_list.artno and soabuff.done_step == 0 and soabuff._recid == soa_list._recid)):
                    soabuff.done_step = 1
                    debt =  to_decimal(soabuff.saldo)
                    fdebt =  to_decimal(fdebt) + to_decimal(soabuff.vesrdep)

                    if soabuff.counter > 0:

                        for debt in db_session.query(debt).filter(
                                 (debt.rechnr == soabuff.rechnr) & (debt.counter == soabuff.counter) & (debt.gastnr == guestno) & (debt.zahlkonto > 0)).order_by(debt._recid).all():
                            fcrdt =  to_decimal(fcrdt) + to_decimal(debt.vesrdep)
                            crdt =  to_decimal(crdt) + to_decimal(debt.saldo)

                            if isprintedb4 and debt.debref == 0:
                                new_crdt =  to_decimal(new_crdt) + to_decimal(crdt)
                                new_fcrdt =  to_decimal(new_fcrdt) + to_decimal(fcrdt)


                    debt_obj_list = {}
                    debt = Debitor()
                    artikel = Artikel()
                    for debt.gastnr, debt.rechnr, debt.betriebsnr, debt._recid, debt.rgdatum, debt.vesrcod, debt.artnr, debt.counter, debt.debref, debt.saldo, debt.vesrdep, debt.gastnrmember, debt.zahlkonto, debt.opart, artikel.artart, artikel.artnr, artikel.mwst_code, artikel._recid in db_session.query(debt.gastnr, debt.rechnr, debt.betriebsnr, debt._recid, debt.rgdatum, debt.vesrcod, debt.artnr, debt.counter, debt.debref, debt.saldo, debt.vesrdep, debt.gastnrmember, debt.zahlkonto, debt.opart, Artikel.artart, Artikel.artnr, Artikel.mwst_code, Artikel._recid).join(Artikel,(Artikel.artnr == debt.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                             (debt.rechnr == soabuff.rechnr) & (debt.gastnr == soabuff.gastnr) & (debt.betriebsnr == soabuff.dptnr) & (debt.opart <= 1) & (soabuff.saldo != 0) & (debt.zahlkonto == 0) & (debt._recid != soa_list.arrecid)).order_by(debt._recid).all():
                        if debt_obj_list.get(debt._recid):
                            continue
                        else:
                            debt_obj_list[debt._recid] = True

                        if debt.counter > 0:

                            for debt1 in db_session.query(Debt1).filter(
                                     (Debt1.rechnr == debt.rechnr) & (Debt1.counter == debt.counter) & (Debt1.artnr == debt.artnr) & (Debt1.gastnr == debitor.gastnr) & (Debt1.zahlkonto > 0)).order_by(debt.rgdatum).all():
                                crdt =  to_decimal(crdt) + to_decimal(debt.saldo)
                                fcrdt =  to_decimal(fcrdt) + to_decimal(debt.vesrdep)

                                if isprintedb4 and debt1.debref == 0:
                                    new_crdt =  to_decimal(new_crdt) + to_decimal(crdt)
                                    new_fcrdt =  to_decimal(new_fcrdt) + to_decimal(fcrdt)

                crdt =  - to_decimal(crdt)
                fcrdt =  - to_decimal(fcrdt)
                new_crdt =  - to_decimal(new_crdt)
                new_fcrdt =  - to_decimal(new_fcrdt)

                for soabuff in query(soabuff_data, filters=(lambda soabuff: soabuff.done_step == 1)):
                    soabuff.done_step = 2
                    soabuff.debt =  to_decimal(debt)
                    soabuff.credit =  to_decimal(crdt)
                    soabuff.saldo =  to_decimal(debt) - to_decimal(crdt)
                    soabuff.fdebt =  to_decimal(fdebt)
                    soabuff.fcredit =  to_decimal(fcrdt)
                    soabuff.fsaldo =  to_decimal(fdebt) - to_decimal(fcrdt)
                    soabuff.newpayment =  to_decimal(new_crdt)
                    soabuff.newfpayment =  to_decimal(new_fcrdt)
                    soabuff.foreign_exchg =  to_decimal(soabuff.saldo) / to_decimal(dollar_rate)

                soa_list = query(soa_list_data, filters=(lambda soa_list: soa_list.done_step == 0), next=True)

            for soa_list in query(soa_list_data):
                zeit = get_current_time_in_seconds()

                debitor = get_cache (Debitor, {"_recid": [(eq, soa_list.arrecid)]})

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if not bill:

                        if debitor.debref != 0:

                            queasy = get_cache (Queasy, {"key": [(eq, 192)],"number1": [(eq, debitor.rechnr)]})

                            if queasy:
                                soa_list.printed = True
                                soa_list.refno = debitor.debref
                                soa_list.inv_str = "INV" + to_string(queasy.number2, "9999999")

                            elif not queasy:
                                soa_list.printed = False

                        gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if gast:
                            soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:

                            guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                            if guest:
                                soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        soa_list.ar_flag = 2
                        continue
                    zeit1 = get_current_time_in_seconds()
                    soa_list.ar_flag = 1

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, debitor.rechnr)],"artnr": [(eq, debitor.artnr)],"departement": [(eq, 0)]})
                    soa_list.refno = debitor.debref
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

                    gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if gast:
                        soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                    else:

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                        if guest:
                            soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if bill.resnr > 0:

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                        if not res_line:

                            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)]})

                        if res_line:
                            soa_list.ankunft = res_line.ankunft
                            soa_list.abreise = res_line.abreise
                            soa_list.zinr = res_line.zinr
                            soa_list.erwachs = res_line.erwachs
                            soa_list.child1 = res_line.kind1
                            soa_list.child2 = res_line.kind2
                            soa_list.roomrate =  to_decimal(res_line.zipreis)
                            soa_list.remarks = soa_list.remarks + chr_unicode(3) + to_string(res_line.resnr)


                            count_zimm = 0

                            for bresline in db_session.query(Bresline).filter(
                                     (Bresline.resnr == res_line.resnr)).order_by(Bresline._recid).all():
                                count_zimm = count_zimm + res_line.zimmeranz
                                soa_list.zimmeranz = count_zimm

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                            if zimkateg:
                                soa_list.remarks = soa_list.remarks + chr_unicode(3) + zimkateg.kurzbez + chr_unicode(3) + zimkateg.bezeichnung
                            else:
                                soa_list.remarks = soa_list.remarks + chr_unicode(3) + chr_unicode(3)
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(get_room_breakdown(res_line._recid, res_line.ankunft, 0, date_mdy(get_current_date())))
                            soa_list.remarks = soa_list.remarks + chr_unicode(3) + to_string(nett_vat, ">>>,>>>,>>9.99") + chr_unicode(3) + to_string(nett_service, ">>>,>>>,>>9.99")
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                str = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(str, 0, 7) == ("voucher").lower() :
                                    soa_list.voucherno1 = substring(str, 7)

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            if reservation:
                                soa_list.voucherno2 = reservation.vesrdepot
                                soa_list.resv_name = reservation.name


                    else:
                        soa_list.remarks = soa_list.remarks + chr_unicode(3) + chr_unicode(3) + chr_unicode(3) + chr_unicode(3) + chr_unicode(3)


                        soa_list.resv_name = bill.bilname

                    for billine in db_session.query(Billine).filter(
                             (Billine.rechnr == debitor.rechnr) & (Billine.anzahl != 0)).order_by(Billine._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, billine.artnr)]})

                        if artikel:

                            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                soa_list.gst_tot_sales =  to_decimal(soa_list.gst_tot_sales) + to_decimal(billine.betrag)

                                if artikel.artart == 1:
                                    soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((billine.betrag) / to_decimal(1.06) )


                                else:

                                    if artikel.mwst_code != 0:
                                        soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((billine.betrag) / to_decimal(1.06) )

                                    if artikel.mwst_code == 0:
                                        soa_list.gst_tot_non_taxable =  to_decimal(soa_list.gst_tot_non_taxable) + to_decimal(billine.betrag)


                else:

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, debitor.rechnr)],"departement": [(eq, debitor.betriebsnr)]})

                    if not h_bill:
                        continue
                    else:
                        soa_list.ar_flag = 1

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, debitor.betriebsnr)]})
                        soa_list.refno = h_bill.service[5]
                        soa_list.dptnr = debitor.betriebsnr
                        soa_list.outlet = True

                        gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if h_bill.bilname != "":
                            soa_list.name = hoteldpt.depart + " - " + h_bill.bilname
                        else:

                            if gast:
                                soa_list.name = hoteldpt.depart + " - " + Gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                            else:
                                soa_list.name = hoteldpt.depart + " - " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                        if h_bill.service[6] != 0:

                            if length(to_string(h_bill.service[6])) < 8:
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
                                 (Hbilline.rechnr == h_bill.rechnr)).order_by(Hbilline._recid).all():

                            h_artikel = get_cache (H_artikel, {"artnr": [(eq, hbilline.artnr)]})

                            if h_artikel:

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)]})

                                if artikel:

                                    if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                        soa_list.gst_tot_sales =  to_decimal(soa_list.gst_tot_sales) + to_decimal(hbilline.betrag)

                                        if artikel.artart == 1:
                                            soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((hbilline.betrag) / to_decimal(1.06) )


                                        else:

                                            if artikel.mwst_code != 0:
                                                soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((hbilline.betrag) / to_decimal(1.06) )

                                            if artikel.mwst_code == 0:
                                                soa_list.gst_tot_non_taxable =  to_decimal(soa_list.gst_tot_non_taxable) + to_decimal(hbilline.betrag)


        else:
            param4 = call_paramar(4)

            if param4 == "":
                due_date = curr_day
            else:
                var_param = substring(param4, length(param4) - 1, 1)
                val_param = to_int(substring(param4, 0, length(param4) - 1))

                if var_param.lower()  == ("D").lower()  or var_param.lower()  == ("d").lower() :
                    due_date = eof_month + timedelta(days=val_param)

                elif var_param.lower()  == ("M").lower()  or var_param.lower()  == ("m").lower() :
                    nmonth = get_month(eof_month) + val_param

                    if nmonth > 12:
                        mnth1 = 1
                        year2 = get_year(eof_month) + 1


                    else:
                        mnth1 = nmonth
                        year2 = get_year(eof_month)


                    due_date = lastdate_inmonth(mnth1, year2)

                elif var_param.lower()  == ("Y").lower()  or var_param.lower()  == ("y").lower() :
                    mnth1 = get_month(eof_month)
                    year2 = get_year(eof_month) + val_param


                    due_date = lastdate_inmonth(mnth1, year2)
                else:
                    mnth1 = get_month(eof_month)
                    year2 = get_year(eof_month)


                    due_date = lastdate_inmonth(mnth1, year2)

            for debitor in db_session.query(Debitor).filter(
                     (Debitor.gastnr == guestno) & (Debitor.zahlkonto == 0) & (Debitor.saldo != 0) & (Debitor.rgdatum < bof_month)).order_by(Debitor._recid).all():
                saldo1 =  to_decimal(saldo1) + to_decimal(debitor.saldo)

            for debitor in db_session.query(Debitor).filter(
                     (Debitor.gastnr == guestno) & (Debitor.zahlkonto > 0) & (Debitor.rgdatum < bof_month) & (Debitor.saldo != 0) & (Debitor.opart <= 2)).order_by(Debitor._recid).all():
                saldo2 =  to_decimal(saldo2) + to_decimal(debitor.saldo)

            for debitor in db_session.query(Debitor).filter(
                     (Debitor.gastnr == guestno) & (Debitor.zahlkonto > 0) & (Debitor.rgdatum >= bof_month) & (Debitor.rgdatum <= eof_month) & (Debitor.saldo != 0) & (Debitor.opart <= 2)).order_by(Debitor._recid).all():
                saldo4 =  to_decimal(saldo4) + to_decimal(debitor.saldo)
            param2 = call_paramar(2)
            soa_list = Soa_list()
            soa_list_data.append(soa_list)

            soa_list.to_sort = 0
            soa_list.name = param2
            soa_list.debt =  to_decimal("0")
            soa_list.credit =  to_decimal("0")
            soa_list.saldo =  to_decimal(saldo1) + to_decimal(saldo2)
            soa_list.fsaldo =  to_decimal(saldo1) + to_decimal(saldo2)
            soa_list.foreign_exchg =  to_decimal(soa_list.saldo) / to_decimal(dollar_rate)


            param1 = call_paramar(1)

            if param1.lower()  == ("yes").lower() :
                counter_saldo =  to_decimal(counter_saldo) + to_decimal(saldo1) + to_decimal(saldo2)
            else:
                counter_saldo =  to_decimal("0")

            debitor_obj_list = {}
            debitor = Debitor()
            artikel = Artikel()
            for debitor.gastnr, debitor.rechnr, debitor.betriebsnr, debitor._recid, debitor.rgdatum, debitor.vesrcod, debitor.artnr, debitor.counter, debitor.debref, debitor.saldo, debitor.vesrdep, debitor.gastnrmember, debitor.zahlkonto, debitor.opart, artikel.artart, artikel.artnr, artikel.mwst_code, artikel._recid in db_session.query(Debitor.gastnr, Debitor.rechnr, Debitor.betriebsnr, Debitor._recid, Debitor.rgdatum, Debitor.vesrcod, Debitor.artnr, Debitor.counter, Debitor.debref, Debitor.saldo, Debitor.vesrdep, Debitor.gastnrmember, Debitor.zahlkonto, Debitor.opart, Artikel.artart, Artikel.artnr, Artikel.mwst_code, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                     (Debitor.gastnr == guestno) & (Debitor.saldo != 0) & (Debitor.zahlkonto == 0) & (Debitor.rgdatum >= bof_month) & (Debitor.rgdatum <= eof_month)).order_by(Debitor.rgdatum, Debitor.rechnr).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True

                if param1.lower()  == ("yes").lower() :
                    counter_saldo =  to_decimal(counter_saldo) + to_decimal(debitor.saldo)
                else:
                    counter_saldo =  to_decimal(debitor.saldo)
                soa_list = Soa_list()
                soa_list_data.append(soa_list)

                soa_list.to_sort = 1
                soa_list.arrecid = debitor._recid
                soa_list.rechnr = debitor.rechnr
                soa_list.gastnr = debitor.gastnr
                soa_list.datum = debitor.rgdatum
                soa_list.remarks = debitor.vesrcod
                soa_list.dptnr = debitor.betriebsnr
                soa_list.debt =  to_decimal(debitor.saldo)
                soa_list.credit =  to_decimal("0")
                soa_list.saldo =  to_decimal(counter_saldo)
                soa_list.fsaldo =  to_decimal(counter_saldo)
                soa_list.foreign_exchg =  to_decimal(soa_list.saldo) / to_decimal(dollar_rate)

            debitor_obj_list = {}
            for debitor in db_session.query(Debitor).filter(
                     ((to_int(Debitor._recid).in_(list(set([soa_list.arrecid for soa_list in soa_list_data])))))).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True

                soa_list = query(soa_list_data, (lambda soa_list: (to_int(debitor._recid) == soa_list.arrecid)), first=True)
                crdt = 0 debt == 0 fcrdt == 0 fdebt == 0
                new_crdt = 0 new_fcrdt == 0 isprintedb4 == True

                if debitor.debref != 0:
                    isprintedb4 = True
                debt =  to_decimal(debitor.saldo)
                fdebt =  to_decimal(debitor.vesrdep)

                if debitor.counter > 0:

                    for debt in db_session.query(debt).filter(
                             (debt.rechnr == debitor.rechnr) & (debt.counter == debitor.counter) & (debt.artnr == debitor.artnr) & (debt.betriebsnr == debitor.betriebsnr) & (debt.gastnr == debitor.gastnr) & (debt.zahlkonto > 0)).order_by(debt.rgdatum).all():
                        fcrdt =  to_decimal(fcrdt) + to_decimal(debt.vesrdep)
                        crdt =  to_decimal(crdt) + to_decimal(debt.saldo)

                        if isprintedb4 and debt.debref == 0:
                            new_crdt =  to_decimal(new_crdt) + to_decimal(crdt)
                            new_fcrdt =  to_decimal(new_fcrdt) + to_decimal(fcrdt)


                debt_obj_list = {}
                debt = Debitor()
                artikel = Artikel()
                for debt.gastnr, debt.rechnr, debt.betriebsnr, debt._recid, debt.rgdatum, debt.vesrcod, debt.artnr, debt.counter, debt.debref, debt.saldo, debt.vesrdep, debt.gastnrmember, debt.zahlkonto, debt.opart, artikel.artart, artikel.artnr, artikel.mwst_code, artikel._recid in db_session.query(debt.gastnr, debt.rechnr, debt.betriebsnr, debt._recid, debt.rgdatum, debt.vesrcod, debt.artnr, debt.counter, debt.debref, debt.saldo, debt.vesrdep, debt.gastnrmember, debt.zahlkonto, debt.opart, Artikel.artart, Artikel.artnr, Artikel.mwst_code, Artikel._recid).join(Artikel,(Artikel.artnr == debt.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                         (debt.rechnr == debitor.rechnr) & (debt.gastnr == debitor.gastnr) & (debt.betriebsnr == debitor.betriebsnr) & (debt.opart <= 1) & (debitor.saldo != 0) & (debt.zahlkonto == 0) & (debt._recid != debitor._recid)).order_by(debt._recid).all():
                    if debt_obj_list.get(debt._recid):
                        continue
                    else:
                        debt_obj_list[debt._recid] = True


                    debt =  to_decimal(debt) + to_decimal(debt.saldo)
                    fdebt =  to_decimal(fdebt) + to_decimal(debt.vesrdep)

                    if debt.counter > 0:

                        for debt1 in db_session.query(Debt1).filter(
                                 (Debt1.rechnr == debt.rechnr) & (Debt1.counter == debt.counter) & (Debt1.artnr == debt.artnr) & (Debt1.gastnr == debitor.gastnr) & (Debt1.zahlkonto > 0)).order_by(debt.rgdatum).all():
                            crdt =  to_decimal(crdt) + to_decimal(debt.saldo)
                            fcrdt =  to_decimal(fcrdt) + to_decimal(debt.vesrdep)

                            if isprintedb4 and debt1.debref == 0:
                                new_crdt =  to_decimal(new_crdt) + to_decimal(crdt)
                                new_fcrdt =  to_decimal(new_fcrdt) + to_decimal(fcrdt)

                crdt =  - to_decimal(crdt)
                fcrdt =  - to_decimal(fcrdt)
                new_crdt =  - to_decimal(new_crdt)
                new_fcrdt =  - to_decimal(new_fcrdt)

                if debitor.betriebsnr == 0:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if not bill:
                        rech_nr = debitor.rechnr
                        bet_nr = debitor.betriebsnr
                        msg_int = 1
                        continue

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)]})
                    soa_list.refno = bill.billref
                    soa_list.dptnr = 0

                    if bill.billref == 0:
                        soa_list.printed = False
                    else:
                        soa_list.printed = True

                    if bill.logidat != None:
                        soa_list.printdate = bill.logidat
                    else:
                        soa_list.printdate = get_current_date()

                    if bill.billref != 0:
                        soa_list.inv_str = "INV" + to_string(bill.billref, "9999999")

                    if bill_line:
                        soa_list.voucherno = entry(1, bill_line.bezeich, "/")

                    gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                    if gast:
                        soa_list.name = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                    else:

                        guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                        if guest:
                            soa_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                    if not res_line:

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)]})

                    if res_line:
                        soa_list.ankunft = res_line.ankunft
                        soa_list.abreise = res_line.abreise
                        soa_list.zinr = res_line.zinr
                        soa_list.erwachs = res_line.erwachs
                        soa_list.child1 = res_line.kind1
                        soa_list.child2 = res_line.kind2
                        soa_list.roomrate =  to_decimal(res_line.zipreis)
                        soa_list.remarks = soa_list.remarks + chr_unicode(3) + to_string(res_line.resnr)


                        count_zimm = 0

                        for bresline in db_session.query(Bresline).filter(
                                 (Bresline.resnr == res_line.resnr)).order_by(Bresline._recid).all():
                            count_zimm = count_zimm + res_line.zimmeranz
                            soa_list.zimmeranz = count_zimm

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            soa_list.remarks = soa_list.remarks + chr_unicode(3) + zimkateg.kurzbez + chr_unicode(3) + zimkateg.bezeichnung
                        else:
                            soa_list.remarks = soa_list.remarks + chr_unicode(3) + chr_unicode(3)
                        fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(get_room_breakdown(res_line._recid, res_line.ankunft, 0, date_mdy(get_current_date())))
                        soa_list.remarks = soa_list.remarks + chr_unicode(3) + to_string(nett_vat, ">>>,>>>,>>9.99") + chr_unicode(3) + to_string(nett_service, ">>>,>>>,>>9.99")
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 7) == ("voucher").lower() :
                                soa_list.voucherno1 = substring(str, 7)

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        if reservation:
                            soa_list.voucherno2 = reservation.vesrdepot
                            soa_list.resv_name = reservation.name


                    else:
                        soa_list.remarks = soa_list.remarks + chr_unicode(3) + chr_unicode(3) + chr_unicode(3) + chr_unicode(3) + chr_unicode(3)


                        soa_list.resv_name = bill.bilname

                    for billine in db_session.query(Billine).filter(
                             (Billine.rechnr == debitor.rechnr) & (Billine.anzahl != 0)).order_by(Billine._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, billine.artnr)]})

                        if artikel:

                            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                soa_list.gst_tot_sales =  to_decimal(soa_list.gst_tot_sales) + to_decimal(billine.betrag)

                                if artikel.artart == 1:
                                    soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((billine.betrag) / to_decimal(1.06) )


                                else:

                                    if artikel.mwst_code != 0:
                                        soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((billine.betrag) / to_decimal(1.06) )

                                    if artikel.mwst_code == 0:
                                        soa_list.gst_tot_non_taxable =  to_decimal(soa_list.gst_tot_non_taxable) + to_decimal(billine.betrag)


                else:

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, debitor.rechnr)],"departement": [(eq, debitor.betriebsnr)]})

                    if not h_bill:
                        rech_nr = debitor.rechnr
                        bet_nr = debitor.betriebsnr
                        msg_int = 2
                        continue
                    else:

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, debitor.betriebsnr)]})
                        soa_list.refno = h_bill.service[5]
                        soa_list.dptnr = debitor.betriebsnr
                        soa_list.outlet = True

                        gast = get_cache (Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                        if h_bill.bilname != "":
                            soa_list.name = hoteldpt.depart + " - " + h_bill.bilname
                        else:

                            if gast:
                                soa_list.name = hoteldpt.depart + " - " + Gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                            else:
                                soa_list.name = hoteldpt.depart + " - " + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                        if h_bill.service[6] != 0:

                            if length(to_string(h_bill.service[6])) < 8:
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
                                 (Hbilline.rechnr == h_bill.rechnr)).order_by(Hbilline._recid).all():

                            h_artikel = get_cache (H_artikel, {"artnr": [(eq, hbilline.artnr)]})

                            if h_artikel:

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)]})

                                if artikel:

                                    if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                                        soa_list.gst_tot_sales =  to_decimal(soa_list.gst_tot_sales) + to_decimal(hbilline.betrag)

                                        if artikel.artart == 1:
                                            soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((hbilline.betrag) / to_decimal(1.06) )


                                        else:

                                            if artikel.mwst_code != 0:
                                                soa_list.gst_amount =  to_decimal(soa_list.gst_amount) + to_decimal((hbilline.betrag) / to_decimal(1.06) )

                                            if artikel.mwst_code == 0:
                                                soa_list.gst_tot_non_taxable =  to_decimal(soa_list.gst_tot_non_taxable) + to_decimal(hbilline.betrag)

        if show_type == 1:
            param3 = call_paramar(3)

            if param1.lower()  == ("yes").lower() :
                counter_saldo =  to_decimal(counter_saldo) + to_decimal(saldo3) + to_decimal(saldo4)
            else:
                counter_saldo =  to_decimal(saldo3) + to_decimal(saldo4)
            soa_list = Soa_list()
            soa_list_data.append(soa_list)

            soa_list.to_sort = 2
            soa_list.name = param3
            soa_list.debt =  to_decimal("0")
            soa_list.credit =  to_decimal(saldo3) + to_decimal(saldo4)
            soa_list.saldo =  to_decimal(counter_saldo)
            soa_list.fsaldo =  to_decimal(counter_saldo)
            soa_list.foreign_exchg =  to_decimal(soa_list.saldo) / to_decimal(dollar_rate)

        for soa_list in query(soa_list_data, filters=(lambda soa_list: soa_list.saldo == 0 and soa_list.to_sort == 1)):
            soa_list_data.remove(soa_list)


    def call_paramar(nr:int):

        nonlocal zeit, zeit1, str, due_date, soa_list_data, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, t_voucherno, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, reservation, zimkateg, h_bill, hoteldpt, h_artikel
        nonlocal show_type, bof_month, eof_month, guestno, curr_day, dollar_rate
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline
        nonlocal soa_list_data

        param_val = ""

        def generate_inner_output():
            return (param_val)


        param_ar = query(param_ar_data, filters=(lambda param_ar: param_ar.param_nr == nr), first=True)

        if param_ar:
            param_val = param_ar.param_val
        else:
            param_val = ""

        return generate_inner_output()


    def lastdate_inmonth(imonth:int, iyear:int):

        nonlocal zeit, zeit1, str, due_date, soa_list_data, rech_nr, bet_nr, msg_int, param1, param2, param3, param4, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, curr_gastnr, curr_refno, new_refno, cl_exist, saldo, s, i, arrival, departure, debt, crdt, fdebt, fcrdt, new_crdt, new_fcrdt, isprintedb4, saldo1, saldo2, saldo3, saldo4, other_flag, count_zimm, t_voucherno, nmonth, mnth1, year2, val_param, var_param, guest, bill, debitor, bill_line, h_bill_line, res_line, artikel, queasy, reservation, zimkateg, h_bill, hoteldpt, h_artikel
        nonlocal show_type, bof_month, eof_month, guestno, curr_day, dollar_rate
        nonlocal soabuff, gast, bill1, debt, debt1, billine, hbilline, bresline


        nonlocal soa_list, soabuff, param_ar, gast, bill1, debt, debt1, billine, hbilline, bresline
        nonlocal soa_list_data

        lastdate = None
        newmonth:int = 0
        newyear:int = 0
        newdate:date = None

        def generate_inner_output():
            return (lastdate)

        newmonth = imonth + 1

        if newmonth > 12:
            newmonth = newmonth - 12
            newyear = iyear + 1
            newdate = date_mdy(newmonth, 1, newyear)
            lastdate = newdate - timedelta(days=1)
        else:
            newdate = date_mdy(newmonth , 1, iyear)
            lastdate = newdate - timedelta(days=1)

        return generate_inner_output()


    create_soalist()

    return generate_output()