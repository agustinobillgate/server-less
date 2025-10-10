#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Billjournal, H_bill_line, Artikel, Queasy, Htparam, H_artikel

def if_ecsys_autorealtime_inp_trxbl(outlet:string, inp_excl_art:string):

    prepare_cache ([Billjournal, H_bill_line, Artikel, Queasy, Htparam, H_artikel])

    trx_list_data = []
    datechar = ""
    bill_date:date = None
    bill_time1:int = 0
    bill_time2:int = 0
    time_str:string = ""
    i:int = 0
    excl_pair:string = ""
    excl_art:string = ""
    excl_dept:string = ""
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    serv_charge:Decimal = to_decimal("0.0")
    serv_betrag:Decimal = to_decimal("0.0")
    vat_proz:Decimal = to_decimal("0.0")
    service_proz:Decimal = to_decimal("0.0")
    service_code:int = 0
    tot_service:Decimal = to_decimal("0.0")
    curr_rechnr:int = 0
    curr_time1:int = 0
    curr_time2:int = 0
    billjournal = h_bill_line = artikel = queasy = htparam = h_artikel = None

    trx_list = journal_list = h_bill_list = t_invoice = t_excl = b_billjournal = b_h_bill_line = b_artikel = buffjournal = h_bill_buff = bqueasy = None

    trx_list_data, Trx_list = create_model("Trx_list", {"invoice_no":string, "trans_date":string, "trans_time":string, "seq_unique":string, "item_name":string, "item_code":string, "item_qty":string, "item_uprice":string, "item_amount":string, "item_vat":string, "item_tamount":string, "item_tvat":string, "item_tserv":string, "trx_amount":string})
    journal_list_data, Journal_list = create_model("Journal_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal}, {"do_it": True})
    h_bill_list_data, H_bill_list = create_model("H_bill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal}, {"do_it": True})
    t_invoice_data, T_invoice = create_model("T_invoice", {"number":string, "service":Decimal})
    t_excl_data, T_excl = create_model("T_excl", {"art":string, "dept":string})

    B_billjournal = create_buffer("B_billjournal",Billjournal)
    B_h_bill_line = create_buffer("B_h_bill_line",H_bill_line)
    B_artikel = create_buffer("B_artikel",Artikel)
    Buffjournal = create_buffer("Buffjournal",Billjournal)
    H_bill_buff = create_buffer("H_bill_buff",H_bill_line)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal trx_list_data, datechar, bill_date, bill_time1, bill_time2, time_str, i, excl_pair, excl_art, excl_dept, serv, vat, fact, netto, serv_charge, serv_betrag, vat_proz, service_proz, service_code, tot_service, curr_rechnr, curr_time1, curr_time2, billjournal, h_bill_line, artikel, queasy, htparam, h_artikel
        nonlocal outlet, inp_excl_art
        nonlocal b_billjournal, b_h_bill_line, b_artikel, buffjournal, h_bill_buff, bqueasy


        nonlocal trx_list, journal_list, h_bill_list, t_invoice, t_excl, b_billjournal, b_h_bill_line, b_artikel, buffjournal, h_bill_buff, bqueasy
        nonlocal trx_list_data, journal_list_data, h_bill_list_data, t_invoice_data, t_excl_data

        return {"trx-list": trx_list_data, "datechar": datechar}

    def update_time(curr_time1:int, curr_time2:int):

        nonlocal trx_list_data, datechar, bill_date, bill_time1, bill_time2, time_str, i, excl_pair, excl_art, excl_dept, serv, vat, fact, netto, serv_charge, serv_betrag, vat_proz, service_proz, service_code, tot_service, curr_rechnr, billjournal, h_bill_line, artikel, queasy, htparam, h_artikel
        nonlocal outlet, inp_excl_art
        nonlocal b_billjournal, b_h_bill_line, b_artikel, buffjournal, h_bill_buff, bqueasy


        nonlocal trx_list, journal_list, h_bill_list, t_invoice, t_excl, b_billjournal, b_h_bill_line, b_artikel, buffjournal, h_bill_buff, bqueasy
        nonlocal trx_list_data, journal_list_data, h_bill_list_data, t_invoice_data, t_excl_data

        latest_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

        if htparam:
            latest_date = htparam.fdate

        bqueasy = get_cache (Queasy, {"key": [(eq, 370)]})

        if bqueasy:
            pass
            bqueasy.date1 = latest_date

            if curr_time1 != 0:
                bqueasy.number1 = curr_time1

            if curr_time2 != 0:
                bqueasy.number2 = curr_time2


            pass
            pass
        else:
            bqueasy = Queasy()
            db_session.add(bqueasy)

            bqueasy.key = 370
            bqueasy.date1 = latest_date

            if curr_time1 != 0:
                bqueasy.number1 = curr_time1

            if curr_time2 != 0:
                bqueasy.number2 = curr_time2


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate
        datechar = to_string(get_year(bill_date) , "9999") + "-" +\
                to_string(get_month(bill_date) , "99") + "-" +\
                to_string(get_day(bill_date) , "99")

    queasy = get_cache (Queasy, {"key": [(eq, 370)]})

    if queasy:
        bill_date = queasy.date1
        bill_time1 = queasy.number1
        bill_time2 = queasy.number2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1)]})

    if htparam and htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 136)]})

    if htparam:
        service_code = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, service_code)]})

        if htparam:
            service_proz =  to_decimal(htparam.fdecimal)

    if inp_excl_art != "" and num_entries(inp_excl_art, "|") > 0:
        for i in range(1,num_entries(inp_excl_art, "|")  + 1) :
            excl_pair = entry(i - 1, inp_excl_art, "|")
            excl_art = entry(0, excl_pair, ":")
            excl_dept = entry(1, excl_pair, ":")

            if excl_art != "" and excl_dept != "":
                t_excl = T_excl()
                t_excl_data.append(t_excl)

                t_excl.art = excl_art
                t_excl.dept = excl_dept

    if outlet != "":

        if to_int(outlet) == 0:
            tot_service =  to_decimal("0")
            curr_rechnr = 0

            for billjournal in db_session.query(Billjournal).filter(
                     ((Billjournal.bill_datum > bill_date) | ((Billjournal.bill_datum == bill_date) & (Billjournal.zeit >= bill_time1))) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.bill_datum, Billjournal.departement, Billjournal.rechnr, Billjournal.zeit).all():

                t_excl = query(t_excl_data, filters=(lambda t_excl: t_excl.art == to_string(billjournal.artnr) and t_excl.dept == to_string(billjournal.departement)), first=True)

                if not t_excl:

                    artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

                    if artikel:

                        if artikel.artart == 0 or artikel.artart == 8:
                            serv =  to_decimal("0")
                            vat =  to_decimal("0")
                            fact =  to_decimal("0")
                            netto =  to_decimal("0")
                            serv_betrag =  to_decimal("0")


                            serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                            if vat == 1:
                                netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                            else:

                                if serv == 1:
                                    serv_betrag =  to_decimal(netto)

                                elif vat > 0:
                                    netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                    serv_betrag =  to_decimal(netto) * to_decimal(serv)

                                if serv == 0 or vat == 0:
                                    netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )

                            t_invoice = query(t_invoice_data, filters=(lambda t_invoice: t_invoice.number == to_string(billjournal.rechnr)), first=True)

                            if not t_invoice:
                                t_invoice = T_invoice()
                                t_invoice_data.append(t_invoice)

                                t_invoice.number = to_string(billjournal.rechnr)


                            t_invoice.service =  to_decimal(t_invoice.service) + to_decimal(serv_betrag)

                            trx_list = query(trx_list_data, filters=(lambda trx_list: trx_list.invoice_no == to_string(billjournal.rechnr) and trx_list.item_code == to_string(artikel.artnr)), first=True)

                            if trx_list:
                                trx_list.item_qty = to_string(to_int(trx_list.item_qty) + billjournal.anzahl)
                                trx_list.item_tamount = to_string(to_decimal(trx_list.item_tamount) + netto)
                                trx_list.item_tvat = to_string(to_decimal(trx_list.item_tvat) + (netto * vat))
                                trx_list.trx_amount = to_string(to_decimal(trx_list.trx_amount) + (netto + (netto * vat)))
                                curr_time1 = billjournal.zeit


                            else:
                                trx_list = Trx_list()
                                trx_list_data.append(trx_list)

                                trx_list.invoice_no = to_string(billjournal.rechnr)
                                trx_list.trans_date = to_string(get_year(billjournal.bill_datum) , "9999") + "-" +\
                                        to_string(get_month(billjournal.bill_datum) , "99") + "-" +\
                                        to_string(get_day(billjournal.bill_datum) , "99")
                                trx_list.trans_time = trx_list.trans_date + " " + to_string(billjournal.zeit, "HH:MM:SS")
                                trx_list.seq_unique = "1"
                                trx_list.item_name = artikel.bezeich
                                trx_list.item_code = to_string(artikel.artnr)
                                trx_list.item_qty = to_string(billjournal.anzahl)
                                trx_list.item_uprice = to_string(netto / billjournal.anzahl)
                                trx_list.item_amount = to_string(trx_list.item_uprice)
                                trx_list.item_vat = to_string(netto / billjournal.anzahl * vat)
                                trx_list.item_tamount = to_string(netto)
                                trx_list.item_tvat = to_string(netto * vat)
                                trx_list.trx_amount = to_string(netto + (netto * vat))
                                curr_rechnr = billjournal.rechnr
                                curr_time1 = billjournal.zeit


        else:
            tot_service =  to_decimal("0")
            curr_rechnr = 0

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr > 0) & ((H_bill_line.bill_datum > bill_date) | ((H_bill_line.bill_datum == bill_date) & (H_bill_line.zeit >= bill_time2))) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0) & (H_bill_line.departement == to_int(outlet))).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate, H_bill_line.zeit).all():

                h_bill_list = query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.dept == h_bill_line.departement and h_bill_list.rechnr == h_bill_line.rechnr), first=True)

                if not h_bill_list:
                    h_bill_list = H_bill_list()
                    h_bill_list_data.append(h_bill_list)

                    h_bill_list.dept = h_bill_line.departement
                    h_bill_list.rechnr = h_bill_line.rechnr

                    h_bill_buff = get_cache (H_bill_line, {"departement": [(eq, h_bill_line.departement)],"rechnr": [(eq, h_bill_line.rechnr)],"bill_datum": [(gt, h_bill_line.bill_datum)]})

                    if h_bill_buff:
                        h_bill_list.do_it = False


                    else:
                        h_bill_list.do_it = True

            for h_bill_list in query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.do_it)):

                h_bill_line_obj_list = {}
                h_bill_line = H_bill_line()
                h_artikel = H_artikel()
                for h_bill_line.departement, h_bill_line.rechnr, h_bill_line.bill_datum, h_bill_line.betrag, h_bill_line.artnr, h_bill_line.anzahl, h_bill_line.zeit, h_bill_line._recid, h_artikel.artart, h_artikel.artnrfront, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel._recid in db_session.query(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.bill_datum, H_bill_line.betrag, H_bill_line.artnr, H_bill_line.anzahl, H_bill_line.zeit, H_bill_line._recid, H_artikel.artart, H_artikel.artnrfront, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel._recid).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                         (H_bill_line.departement == h_bill_list.dept) & (H_bill_line.rechnr == h_bill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True


                    h_bill_list.tot_sales =  to_decimal(h_bill_list.tot_sales) + to_decimal(h_bill_line.betrag)

            for h_bill_list in query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.do_it  and h_bill_list.tot_sales != 0)):

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.departement == h_bill_list.dept) & (H_bill_line.rechnr == h_bill_list.rechnr) & (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line.zeit, H_bill_line.artnr).all():

                    if h_bill_line.artnr == 0:

                        if h_bill_list.tot_sales * h_bill_line.betrag <= 0:

                            if h_bill_list.i_fact <= 0:
                                h_bill_list.i_fact = h_bill_list.i_fact + 1


                        else:

                            if h_bill_list.i_fact >= 0:
                                h_bill_list.i_fact = h_bill_list.i_fact - 1


                    else:

                        h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

                        if h_artikel:

                            if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                                if not matches(h_bill_line.bezeich,r"*(Change)*"):

                                    if h_bill_list.tot_sales * h_bill_line.betrag <= 0:

                                        if h_bill_list.i_fact <= 0:
                                            h_bill_list.i_fact = h_bill_list.i_fact + 1


                                    else:

                                        if h_bill_list.i_fact >= 0:
                                            h_bill_list.i_fact = h_bill_list.i_fact - 1

            for h_bill_list in query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.do_it and h_bill_list.i_fact != 0)):

                h_bill_line_obj_list = {}
                h_bill_line = H_bill_line()
                h_artikel = H_artikel()
                for h_bill_line.departement, h_bill_line.rechnr, h_bill_line.bill_datum, h_bill_line.betrag, h_bill_line.artnr, h_bill_line.anzahl, h_bill_line.zeit, h_bill_line._recid, h_artikel.artart, h_artikel.artnrfront, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel._recid in db_session.query(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.bill_datum, H_bill_line.betrag, H_bill_line.artnr, H_bill_line.anzahl, H_bill_line.zeit, H_bill_line._recid, H_artikel.artart, H_artikel.artnrfront, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                         (H_bill_line.departement == h_bill_list.dept) & (H_bill_line.rechnr == h_bill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                    if artikel:

                        if artikel.artart != 9:
                            netto =  to_decimal("0")
                            serv_betrag =  to_decimal("0")


                            serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, h_bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                            if vat == 1:
                                netto =  to_decimal(h_bill_line.betrag) * to_decimal("100") / to_decimal(vat_proz)
                                serv_betrag =  to_decimal("0")


                            else:

                                if serv == 1:
                                    serv_betrag =  to_decimal(netto)
                                    netto =  to_decimal("0")

                                elif vat > 0:
                                    netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                    serv_betrag =  to_decimal(netto) * to_decimal(serv)

                                if serv == 0 or vat == 0:
                                    netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )

                            t_invoice = query(t_invoice_data, filters=(lambda t_invoice: t_invoice.number == to_string(h_bill_line.rechnr)), first=True)

                            if not t_invoice:
                                t_invoice = T_invoice()
                                t_invoice_data.append(t_invoice)

                                t_invoice.number = to_string(h_bill_line.rechnr)


                            t_invoice.service =  to_decimal(t_invoice.service) + to_decimal(serv_betrag)

                            trx_list = query(trx_list_data, filters=(lambda trx_list: trx_list.invoice_no == to_string(h_bill_line.rechnr) and trx_list.item_code == to_string(h_artikel.artnr)), first=True)

                            if trx_list:
                                trx_list.item_qty = to_string(to_int(trx_list.item_qty) + h_bill_line.anzahl)
                                trx_list.item_tamount = to_string(to_decimal(trx_list.item_tamount) + netto)
                                trx_list.item_tvat = to_string(to_decimal(trx_list.item_tvat) + (netto * vat))
                                trx_list.trx_amount = to_string(to_decimal(trx_list.trx_amount) + (netto + (netto * vat)))
                                curr_time2 = h_bill_line.zeit


                            else:
                                trx_list = Trx_list()
                                trx_list_data.append(trx_list)

                                trx_list.invoice_no = to_string(h_bill_line.rechnr)
                                trx_list.trans_date = to_string(get_year(h_bill_line.bill_datum) , "9999") + "-" +\
                                        to_string(get_month(h_bill_line.bill_datum) , "99") + "-" +\
                                        to_string(get_day(h_bill_line.bill_datum) , "99")
                                trx_list.trans_time = trx_list.trans_date + " " + to_string(h_bill_line.zeit, "HH:MM:SS")
                                trx_list.seq_unique = "1"
                                trx_list.item_name = h_artikel.bezeich
                                trx_list.item_code = to_string(h_artikel.artnr)
                                trx_list.item_qty = to_string(h_bill_line.anzahl)
                                trx_list.item_uprice = to_string(netto / h_bill_line.anzahl)
                                trx_list.item_amount = to_string(trx_list.item_uprice)
                                trx_list.item_vat = to_string(netto / h_bill_line.anzahl * vat)
                                trx_list.item_tamount = to_string(netto)
                                trx_list.item_tvat = to_string(netto * vat)
                                trx_list.trx_amount = to_string(netto + (netto * vat))
                                curr_rechnr = h_bill_line.rechnr
                                curr_time2 = h_bill_line.zeit

        for t_invoice in query(t_invoice_data):

            for trx_list in query(trx_list_data, filters=(lambda trx_list: trx_list.invoice_no == t_invoice.number)):
                trx_list.item_tserv = to_string(t_invoice.service)


        update_time(curr_time1, curr_time2)
    else:
        tot_service =  to_decimal("0")
        curr_rechnr = 0

        for billjournal in db_session.query(Billjournal).filter(
                 ((Billjournal.bill_datum > bill_date) | ((Billjournal.bill_datum == bill_date) & (Billjournal.zeit >= bill_time1))) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.bill_datum, Billjournal.departement, Billjournal.rechnr, Billjournal.zeit).all():

            t_excl = query(t_excl_data, filters=(lambda t_excl: t_excl.art == to_string(billjournal.artnr) and t_excl.dept == to_string(billjournal.departement)), first=True)

            if not t_excl:

                artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

                if artikel:

                    if artikel.artart == 0 or artikel.artart == 8:
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")
                        fact =  to_decimal("0")
                        netto =  to_decimal("0")
                        serv_betrag =  to_decimal("0")


                        serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                        if vat == 1:
                            netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                        else:

                            if serv == 1:
                                serv_betrag =  to_decimal(netto)

                            elif vat > 0:
                                netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                serv_betrag =  to_decimal(netto) * to_decimal(serv)

                            if serv == 0 or vat == 0:
                                netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )

                        t_invoice = query(t_invoice_data, filters=(lambda t_invoice: t_invoice.number == to_string(billjournal.rechnr)), first=True)

                        if not t_invoice:
                            t_invoice = T_invoice()
                            t_invoice_data.append(t_invoice)

                            t_invoice.number = to_string(billjournal.rechnr)


                        t_invoice.service =  to_decimal(t_invoice.service) + to_decimal(serv_betrag)

                        trx_list = query(trx_list_data, filters=(lambda trx_list: trx_list.invoice_no == to_string(billjournal.rechnr) and trx_list.item_code == to_string(artikel.artnr)), first=True)

                        if trx_list:
                            trx_list.item_qty = to_string(to_int(trx_list.item_qty) + billjournal.anzahl)
                            trx_list.item_tamount = to_string(to_decimal(trx_list.item_tamount) + netto)
                            trx_list.item_tvat = to_string(to_decimal(trx_list.item_tvat) + (netto * vat))
                            trx_list.trx_amount = to_string(to_decimal(trx_list.trx_amount) + (netto + (netto * vat)))
                            curr_time1 = billjournal.zeit


                        else:
                            trx_list = Trx_list()
                            trx_list_data.append(trx_list)

                            trx_list.invoice_no = to_string(billjournal.rechnr)
                            trx_list.trans_date = to_string(get_year(billjournal.bill_datum) , "9999") + "-" +\
                                    to_string(get_month(billjournal.bill_datum) , "99") + "-" +\
                                    to_string(get_day(billjournal.bill_datum) , "99")
                            trx_list.trans_time = trx_list.trans_date + " " + to_string(billjournal.zeit, "HH:MM:SS")
                            trx_list.seq_unique = "1"
                            trx_list.item_name = artikel.bezeich
                            trx_list.item_code = to_string(artikel.artnr)
                            trx_list.item_qty = to_string(billjournal.anzahl)
                            trx_list.item_uprice = to_string(netto / billjournal.anzahl)
                            trx_list.item_amount = to_string(trx_list.item_uprice)
                            trx_list.item_vat = to_string(netto / billjournal.anzahl * vat)
                            trx_list.item_tamount = to_string(netto)
                            trx_list.item_tvat = to_string(netto * vat)
                            trx_list.trx_amount = to_string(netto + (netto * vat))
                            curr_rechnr = billjournal.rechnr
                            curr_time1 = billjournal.zeit


        tot_service =  to_decimal("0")
        curr_rechnr = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & ((H_bill_line.bill_datum > bill_date) | ((H_bill_line.bill_datum == bill_date) & (H_bill_line.zeit >= bill_time2))) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate, H_bill_line.zeit).all():

            h_bill_list = query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.dept == h_bill_line.departement and h_bill_list.rechnr == h_bill_line.rechnr), first=True)

            if not h_bill_list:
                h_bill_list = H_bill_list()
                h_bill_list_data.append(h_bill_list)

                h_bill_list.dept = h_bill_line.departement
                h_bill_list.rechnr = h_bill_line.rechnr

                h_bill_buff = get_cache (H_bill_line, {"departement": [(eq, h_bill_line.departement)],"rechnr": [(eq, h_bill_line.rechnr)],"bill_datum": [(gt, h_bill_line.bill_datum)]})

                if h_bill_buff:
                    h_bill_list.do_it = False


                else:
                    h_bill_list.do_it = True

        for h_bill_list in query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.do_it)):

            h_bill_line_obj_list = {}
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            for h_bill_line.departement, h_bill_line.rechnr, h_bill_line.bill_datum, h_bill_line.betrag, h_bill_line.artnr, h_bill_line.anzahl, h_bill_line.zeit, h_bill_line._recid, h_artikel.artart, h_artikel.artnrfront, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel._recid in db_session.query(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.bill_datum, H_bill_line.betrag, H_bill_line.artnr, H_bill_line.anzahl, H_bill_line.zeit, H_bill_line._recid, H_artikel.artart, H_artikel.artnrfront, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel._recid).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == h_bill_list.dept) & (H_bill_line.rechnr == h_bill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True


                h_bill_list.tot_sales =  to_decimal(h_bill_list.tot_sales) + to_decimal(h_bill_line.betrag)

        for h_bill_list in query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.do_it  and h_bill_list.tot_sales != 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == h_bill_list.dept) & (H_bill_line.rechnr == h_bill_list.rechnr) & (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line.zeit, H_bill_line.artnr).all():

                if h_bill_line.artnr == 0:

                    if h_bill_list.tot_sales * h_bill_line.betrag <= 0:

                        if h_bill_list.i_fact <= 0:
                            h_bill_list.i_fact = h_bill_list.i_fact + 1


                    else:

                        if h_bill_list.i_fact >= 0:
                            h_bill_list.i_fact = h_bill_list.i_fact - 1


                else:

                    h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

                    if h_artikel:

                        if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                            if not matches(h_bill_line.bezeich,r"*(Change)*"):

                                if h_bill_list.tot_sales * h_bill_line.betrag <= 0:

                                    if h_bill_list.i_fact <= 0:
                                        h_bill_list.i_fact = h_bill_list.i_fact + 1


                                else:

                                    if h_bill_list.i_fact >= 0:
                                        h_bill_list.i_fact = h_bill_list.i_fact - 1

        for h_bill_list in query(h_bill_list_data, filters=(lambda h_bill_list: h_bill_list.do_it and h_bill_list.i_fact != 0)):

            h_bill_line_obj_list = {}
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            for h_bill_line.departement, h_bill_line.rechnr, h_bill_line.bill_datum, h_bill_line.betrag, h_bill_line.artnr, h_bill_line.anzahl, h_bill_line.zeit, h_bill_line._recid, h_artikel.artart, h_artikel.artnrfront, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel._recid in db_session.query(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.bill_datum, H_bill_line.betrag, H_bill_line.artnr, H_bill_line.anzahl, H_bill_line.zeit, H_bill_line._recid, H_artikel.artart, H_artikel.artnrfront, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == h_bill_list.dept) & (H_bill_line.rechnr == h_bill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel:

                    if artikel.artart != 9:
                        netto =  to_decimal("0")
                        serv_betrag =  to_decimal("0")


                        serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, h_bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                        if vat == 1:
                            netto =  to_decimal(h_bill_line.betrag) * to_decimal("100") / to_decimal(vat_proz)
                            serv_betrag =  to_decimal("0")


                        else:

                            if serv == 1:
                                serv_betrag =  to_decimal(netto)
                                netto =  to_decimal("0")

                            elif vat > 0:
                                netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                serv_betrag =  to_decimal(netto) * to_decimal(serv)

                            if serv == 0 or vat == 0:
                                netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )

                        t_invoice = query(t_invoice_data, filters=(lambda t_invoice: t_invoice.number == to_string(h_bill_line.rechnr)), first=True)

                        if not t_invoice:
                            t_invoice = T_invoice()
                            t_invoice_data.append(t_invoice)

                            t_invoice.number = to_string(h_bill_line.rechnr)


                        t_invoice.service =  to_decimal(t_invoice.service) + to_decimal(serv_betrag)

                        trx_list = query(trx_list_data, filters=(lambda trx_list: trx_list.invoice_no == to_string(h_bill_line.rechnr) and trx_list.item_code == to_string(h_artikel.artnr)), first=True)

                        if trx_list:
                            trx_list.item_qty = to_string(to_int(trx_list.item_qty) + h_bill_line.anzahl)
                            trx_list.item_tamount = to_string(to_decimal(trx_list.item_tamount) + netto)
                            trx_list.item_tvat = to_string(to_decimal(trx_list.item_tvat) + (netto * vat))
                            trx_list.trx_amount = to_string(to_decimal(trx_list.trx_amount) + (netto + (netto * vat)))
                            curr_time2 = h_bill_line.zeit


                        else:
                            trx_list = Trx_list()
                            trx_list_data.append(trx_list)

                            trx_list.invoice_no = to_string(h_bill_line.rechnr)
                            trx_list.trans_date = to_string(get_year(h_bill_line.bill_datum) , "9999") + "-" +\
                                    to_string(get_month(h_bill_line.bill_datum) , "99") + "-" +\
                                    to_string(get_day(h_bill_line.bill_datum) , "99")
                            trx_list.trans_time = trx_list.trans_date + " " + to_string(h_bill_line.zeit, "HH:MM:SS")
                            trx_list.seq_unique = "1"
                            trx_list.item_name = h_artikel.bezeich
                            trx_list.item_code = to_string(h_artikel.artnr)
                            trx_list.item_qty = to_string(h_bill_line.anzahl)
                            trx_list.item_uprice = to_string(netto / h_bill_line.anzahl)
                            trx_list.item_amount = to_string(trx_list.item_uprice)
                            trx_list.item_vat = to_string(netto / h_bill_line.anzahl * vat)
                            trx_list.item_tamount = to_string(netto)
                            trx_list.item_tvat = to_string(netto * vat)
                            trx_list.trx_amount = to_string(netto + (netto * vat))
                            curr_rechnr = h_bill_line.rechnr
                            curr_time2 = h_bill_line.zeit

        for t_invoice in query(t_invoice_data):

            for trx_list in query(trx_list_data, filters=(lambda trx_list: trx_list.invoice_no == t_invoice.number)):
                trx_list.item_tserv = to_string(t_invoice.service)


        update_time(curr_time1, curr_time2)

    return generate_output()