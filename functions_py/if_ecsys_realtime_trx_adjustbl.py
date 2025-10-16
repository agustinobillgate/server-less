#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Billjournal, H_bill_line, Htparam, Queasy, Artikel, H_artikel

def if_ecsys_realtime_trx_adjustbl(inp_excl_art:string):

    prepare_cache ([Billjournal, H_bill_line, Htparam, Queasy, Artikel, H_artikel])

    adj_list_data = []
    t_queasy_data = []
    bill_date:date = None
    userinit:string = ""
    department:string = ""
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
    billjournal = h_bill_line = htparam = queasy = artikel = h_artikel = None

    adj_list = t_queasy = journal_list = h_bill_list = t_invoice = t_excl = buffjournal = h_bill_buff = None

    adj_list_data, Adj_list = create_model("Adj_list", {"flag_void":string, "invoice_no":string, "trans_date":string, "trans_time":string, "seq_unique":string, "item_name":string, "item_code":string, "item_qty":string, "item_uprice":string, "item_amount":string, "item_vat":string, "item_tamount":string, "item_tvat":string, "item_tserv":string, "adj_amount":string})
    t_queasy_data, T_queasy = create_model("T_queasy", {"rec_id":int})
    journal_list_data, Journal_list = create_model("Journal_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal}, {"do_it": True})
    h_bill_list_data, H_bill_list = create_model("H_bill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":Decimal}, {"do_it": True})
    t_invoice_data, T_invoice = create_model("T_invoice", {"number":string, "service":Decimal})
    t_excl_data, T_excl = create_model("T_excl", {"art":string, "dept":string})

    Buffjournal = create_buffer("Buffjournal",Billjournal)
    H_bill_buff = create_buffer("H_bill_buff",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal adj_list_data, t_queasy_data, bill_date, userinit, department, i, excl_pair, excl_art, excl_dept, serv, vat, fact, netto, serv_charge, serv_betrag, vat_proz, service_proz, service_code, tot_service, curr_rechnr, billjournal, h_bill_line, htparam, queasy, artikel, h_artikel
        nonlocal inp_excl_art
        nonlocal buffjournal, h_bill_buff


        nonlocal adj_list, t_queasy, journal_list, h_bill_list, t_invoice, t_excl, buffjournal, h_bill_buff
        nonlocal adj_list_data, t_queasy_data, journal_list_data, h_bill_list_data, t_invoice_data, t_excl_data

        return {"adj-list": adj_list_data, "t-queasy": t_queasy_data}

    t_queasy_data.clear()

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

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 366) & (Queasy.logi1) & (Queasy.logi2 == False)).order_by(Queasy._recid).all():
        bill_date = queasy.date1
        userinit = queasy.char1
        department = queasy.char2

        if department != "":

            if to_int(department) == 0:
                tot_service =  to_decimal("0")
                curr_rechnr = 0

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.bill_datum == bill_date) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.bill_datum, Billjournal.departement, Billjournal.rechnr, Billjournal.zeit).all():

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

                                adj_list = query(adj_list_data, filters=(lambda adj_list: adj_list.invoice_no == to_string(billjournal.rechnr) and adj_list.item_code == to_string(artikel.artnr)), first=True)

                                if adj_list:
                                    adj_list.item_qty = to_string(to_int(adj_list.item_qty) + billjournal.anzahl)
                                    adj_list.item_tamount = to_string(to_decimal(adj_list.item_tamount) + netto)
                                    adj_list.item_tvat = to_string(to_decimal(adj_list.item_tvat) + (netto * vat))
                                    adj_list.adj_amount = to_string(to_decimal(adj_list.adj_amount) + (netto + (netto * vat)))


                                else:
                                    adj_list = Adj_list()
                                    adj_list_data.append(adj_list)

                                    adj_list.flag_void = "false"
                                    adj_list.invoice_no = to_string(billjournal.rechnr)
                                    adj_list.trans_date = to_string(get_year(billjournal.bill_datum) , "9999") + "-" +\
                                            to_string(get_month(billjournal.bill_datum) , "99") + "-" +\
                                            to_string(get_day(billjournal.bill_datum) , "99")
                                    adj_list.trans_time = adj_list.trans_date + " " + to_string(billjournal.zeit, "HH:MM:SS")
                                    adj_list.seq_unique = "1"
                                    adj_list.item_name = artikel.bezeich
                                    adj_list.item_code = to_string(artikel.artnr)
                                    adj_list.item_qty = to_string(billjournal.anzahl)
                                    adj_list.item_uprice = to_string(netto / billjournal.anzahl)
                                    adj_list.item_amount = to_string(adj_list.item_uprice)
                                    adj_list.item_vat = to_string(netto / billjournal.anzahl * vat)
                                    adj_list.item_tamount = to_string(netto)
                                    adj_list.item_tvat = to_string(netto * vat)
                                    adj_list.adj_amount = to_string(netto + (netto * vat))
                                    curr_rechnr = billjournal.rechnr


            else:
                tot_service =  to_decimal("0")
                curr_rechnr = 0

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_date) & (H_bill_line.departement == to_int(department)) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

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

                                adj_list = query(adj_list_data, filters=(lambda adj_list: adj_list.invoice_no == to_string(h_bill_line.rechnr) and adj_list.item_code == to_string(h_artikel.artnr)), first=True)

                                if adj_list:
                                    adj_list.item_qty = to_string(to_int(adj_list.item_qty) + h_bill_line.anzahl)
                                    adj_list.item_tamount = to_string(to_decimal(adj_list.item_tamount) + netto)
                                    adj_list.item_tvat = to_string(to_decimal(adj_list.item_tvat) + (netto * vat))
                                    adj_list.adj_amount = to_string(to_decimal(adj_list.adj_amount) + (netto + (netto * vat)))


                                else:
                                    adj_list = Adj_list()
                                    adj_list_data.append(adj_list)

                                    adj_list.flag_void = "false"
                                    adj_list.invoice_no = to_string(h_bill_line.rechnr)
                                    adj_list.trans_date = to_string(get_year(h_bill_line.bill_datum) , "9999") + "-" +\
                                            to_string(get_month(h_bill_line.bill_datum) , "99") + "-" +\
                                            to_string(get_day(h_bill_line.bill_datum) , "99")
                                    adj_list.trans_time = adj_list.trans_date + " " + to_string(h_bill_line.zeit, "HH:MM:SS")
                                    adj_list.seq_unique = "1"
                                    adj_list.item_name = h_artikel.bezeich
                                    adj_list.item_code = to_string(h_artikel.artnr)
                                    adj_list.item_qty = to_string(h_bill_line.anzahl)
                                    adj_list.item_uprice = to_string(netto / h_bill_line.anzahl)
                                    adj_list.item_amount = to_string(adj_list.item_uprice)
                                    adj_list.item_vat = to_string(netto / h_bill_line.anzahl * vat)
                                    adj_list.item_tamount = to_string(netto)
                                    adj_list.item_tvat = to_string(netto * vat)
                                    adj_list.adj_amount = to_string(netto + (netto * vat))
                                    curr_rechnr = h_bill_line.rechnr

            for t_invoice in query(t_invoice_data):

                for adj_list in query(adj_list_data, filters=(lambda adj_list: adj_list.invoice_no == t_invoice.number)):
                    adj_list.item_tserv = to_string(t_invoice.service)


        else:
            tot_service =  to_decimal("0")
            curr_rechnr = 0

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.bill_datum == bill_date) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.bill_datum, Billjournal.departement, Billjournal.rechnr, Billjournal.zeit).all():

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

                            adj_list = query(adj_list_data, filters=(lambda adj_list: adj_list.invoice_no == to_string(billjournal.rechnr) and adj_list.item_code == to_string(artikel.artnr)), first=True)

                            if adj_list:
                                adj_list.item_qty = to_string(to_int(adj_list.item_qty) + billjournal.anzahl)
                                adj_list.item_tamount = to_string(to_decimal(adj_list.item_tamount) + netto)
                                adj_list.item_tvat = to_string(to_decimal(adj_list.item_tvat) + (netto * vat))
                                adj_list.adj_amount = to_string(to_decimal(adj_list.adj_amount) + (netto + (netto * vat)))


                            else:
                                adj_list = Adj_list()
                                adj_list_data.append(adj_list)

                                adj_list.flag_void = "false"
                                adj_list.invoice_no = to_string(billjournal.rechnr)
                                adj_list.trans_date = to_string(get_year(billjournal.bill_datum) , "9999") + "-" +\
                                        to_string(get_month(billjournal.bill_datum) , "99") + "-" +\
                                        to_string(get_day(billjournal.bill_datum) , "99")
                                adj_list.trans_time = adj_list.trans_date + " " + to_string(billjournal.zeit, "HH:MM:SS")
                                adj_list.seq_unique = "1"
                                adj_list.item_name = artikel.bezeich
                                adj_list.item_code = to_string(artikel.artnr)
                                adj_list.item_qty = to_string(billjournal.anzahl)
                                adj_list.item_uprice = to_string(netto / billjournal.anzahl)
                                adj_list.item_amount = to_string(adj_list.item_uprice)
                                adj_list.item_vat = to_string(netto / billjournal.anzahl * vat)
                                adj_list.item_tamount = to_string(netto)
                                adj_list.item_tvat = to_string(netto * vat)
                                adj_list.adj_amount = to_string(netto + (netto * vat))
                                curr_rechnr = billjournal.rechnr


            tot_service =  to_decimal("0")
            curr_rechnr = 0

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_date) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

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

                            adj_list = query(adj_list_data, filters=(lambda adj_list: adj_list.invoice_no == to_string(h_bill_line.rechnr) and adj_list.item_code == to_string(h_artikel.artnr)), first=True)

                            if adj_list:
                                adj_list.item_qty = to_string(to_int(adj_list.item_qty) + h_bill_line.anzahl)
                                adj_list.item_tamount = to_string(to_decimal(adj_list.item_tamount) + netto)
                                adj_list.item_tvat = to_string(to_decimal(adj_list.item_tvat) + (netto * vat))
                                adj_list.adj_amount = to_string(to_decimal(adj_list.adj_amount) + (netto + (netto * vat)))


                            else:
                                adj_list = Adj_list()
                                adj_list_data.append(adj_list)

                                adj_list.flag_void = "false"
                                adj_list.invoice_no = to_string(h_bill_line.rechnr)
                                adj_list.trans_date = to_string(get_year(h_bill_line.bill_datum) , "9999") + "-" +\
                                        to_string(get_month(h_bill_line.bill_datum) , "99") + "-" +\
                                        to_string(get_day(h_bill_line.bill_datum) , "99")
                                adj_list.trans_time = adj_list.trans_date + " " + to_string(h_bill_line.zeit, "HH:MM:SS")
                                adj_list.seq_unique = "1"
                                adj_list.item_name = h_artikel.bezeich
                                adj_list.item_code = to_string(h_artikel.artnr)
                                adj_list.item_qty = to_string(h_bill_line.anzahl)
                                adj_list.item_uprice = to_string(netto / h_bill_line.anzahl)
                                adj_list.item_amount = to_string(adj_list.item_uprice)
                                adj_list.item_vat = to_string(netto / h_bill_line.anzahl * vat)
                                adj_list.item_tamount = to_string(netto)
                                adj_list.item_tvat = to_string(netto * vat)
                                adj_list.adj_amount = to_string(netto + (netto * vat))
                                curr_rechnr = h_bill_line.rechnr

            for t_invoice in query(t_invoice_data):

                for adj_list in query(adj_list_data, filters=(lambda adj_list: adj_list.invoice_no == t_invoice.number)):
                    adj_list.item_tserv = to_string(t_invoice.service)


        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        t_queasy.rec_id = queasy._recid

    return generate_output()