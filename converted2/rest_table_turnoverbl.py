#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam, H_bill, H_artikel, Artikel, H_bill_line, H_compli, Tisch, Kontplan

def rest_table_turnoverbl(from_date:date, to_date:date, dept_number:int, excl_compli:bool, excl_taxserv:bool):

    prepare_cache ([Hoteldpt, Htparam, H_bill, H_artikel, Artikel, H_bill_line, Tisch, Kontplan])

    turnover_table_list_data = []
    start_jan:date = None
    i:int = 0
    curr_rechnr:int = 0
    curr_amount:Decimal = to_decimal("0.0")
    tot_food_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_bev_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_other_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_mtd_food_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_mtd_bev_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_mtd_other_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_ytd_food_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_ytd_bev_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    tot_ytd_other_amount:List[Decimal] = create_empty_list(4,to_decimal("0"))
    total_pax:int = 0
    total_mtd_pax:int = 0
    total_ytd_pax:int = 0
    servtax_use_foart:bool = False
    serv_percent:Decimal = to_decimal("0.0")
    mwst_percent:Decimal = to_decimal("0.0")
    fact:Decimal = 1
    bill_date110:date = None
    bill_date:date = None
    service_taxable:bool = False
    hoteldpt = htparam = h_bill = h_artikel = artikel = h_bill_line = h_compli = tisch = kontplan = None

    turnover_table_list = t_table_list = None

    turnover_table_list_data, Turnover_table_list = create_model("Turnover_table_list", {"table_no":string, "table_desc":string, "pax":int, "food_amount":[string,4], "bev_amount":[string,4], "other_amount":[string,4], "mtd_pax":int, "mtd_food_amount":[string,4], "mtd_bev_amount":[string,4], "mtd_other_amount":[string,4], "ytd_pax":int, "ytd_food_amount":[string,4], "ytd_bev_amount":[string,4], "ytd_other_amount":[string,4]})
    t_table_list_data, T_table_list = create_model("T_table_list", {"table_no":int, "table_desc":string, "pax":int, "food_amount":[Decimal,4], "bev_amount":[Decimal,4], "other_amount":[Decimal,4], "mtd_pax":int, "mtd_food_amount":[Decimal,4], "mtd_bev_amount":[Decimal,4], "mtd_other_amount":[Decimal,4], "ytd_pax":int, "ytd_food_amount":[Decimal,4], "ytd_bev_amount":[Decimal,4], "ytd_other_amount":[Decimal,4]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal turnover_table_list_data, start_jan, i, curr_rechnr, curr_amount, tot_food_amount, tot_bev_amount, tot_other_amount, tot_mtd_food_amount, tot_mtd_bev_amount, tot_mtd_other_amount, tot_ytd_food_amount, tot_ytd_bev_amount, tot_ytd_other_amount, total_pax, total_mtd_pax, total_ytd_pax, servtax_use_foart, serv_percent, mwst_percent, fact, bill_date110, bill_date, service_taxable, hoteldpt, htparam, h_bill, h_artikel, artikel, h_bill_line, h_compli, tisch, kontplan
        nonlocal from_date, to_date, dept_number, excl_compli, excl_taxserv


        nonlocal turnover_table_list, t_table_list
        nonlocal turnover_table_list_data, t_table_list_data

        return {"turnover-table-list": turnover_table_list_data}

    def create_turnover_table():

        nonlocal turnover_table_list_data, start_jan, i, curr_rechnr, curr_amount, tot_food_amount, tot_bev_amount, tot_other_amount, tot_mtd_food_amount, tot_mtd_bev_amount, tot_mtd_other_amount, tot_ytd_food_amount, tot_ytd_bev_amount, tot_ytd_other_amount, total_pax, total_mtd_pax, total_ytd_pax, servtax_use_foart, serv_percent, mwst_percent, fact, bill_date110, bill_date, service_taxable, hoteldpt, htparam, h_bill, h_artikel, artikel, h_bill_line, h_compli, tisch, kontplan
        nonlocal from_date, to_date, dept_number, excl_compli, excl_taxserv


        nonlocal turnover_table_list, t_table_list
        nonlocal turnover_table_list_data, t_table_list_data

        h_bill_line_obj_list = {}
        h_bill_line = H_bill_line()
        h_bill = H_bill()
        h_artikel = H_artikel()
        artikel = Artikel()
        for h_bill_line.rechnr, h_bill_line.departement, h_bill_line.bill_datum, h_bill_line.betrag, h_bill_line.tischnr, h_bill_line.betriebsnr, h_bill_line._recid, h_bill.belegung, h_bill._recid, h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_artikel._recid, h_artikel.artnrfront, artikel.umsatzart, artikel._recid, artikel.artnr, artikel.service_code, artikel.mwst_code in db_session.query(H_bill_line.rechnr, H_bill_line.departement, H_bill_line.bill_datum, H_bill_line.betrag, H_bill_line.tischnr, H_bill_line.betriebsnr, H_bill_line._recid, H_bill.belegung, H_bill._recid, H_artikel.departement, H_artikel.artnr, H_artikel.service_code, H_artikel.mwst_code, H_artikel._recid, H_artikel.artnrfront, Artikel.umsatzart, Artikel._recid, Artikel.artnr, Artikel.service_code, Artikel.mwst_code).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement)).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_bill_line.departement)).filter(
                 (H_bill_line.departement == dept_number) & (H_bill_line.bill_datum >= start_jan) & (H_bill_line.bill_datum <= to_date)).order_by(H_bill_line.bill_datum, H_bill_line.rechnr, H_bill_line.tischnr).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True

            if excl_compli:

                h_compli = get_cache (H_compli, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

                if h_compli:
                    continue
            serv_percent, mwst_percent, fact = cal_servat(h_artikel.departement, h_artikel.artnr, h_artikel.service_code, h_artikel.mwst_code, h_bill_line.bill_datum)

            if excl_taxserv:
                curr_amount =  to_decimal(h_bill_line.betrag) / to_decimal(fact)
            else:
                curr_amount =  to_decimal(h_bill_line.betrag)

            t_table_list = query(t_table_list_data, filters=(lambda t_table_list: t_table_list.table_no == h_bill_line.tischnr), first=True)

            if not t_table_list:
                t_table_list = T_table_list()
                t_table_list_data.append(t_table_list)

                t_table_list.table_no = h_bill_line.tischnr

                tisch = get_cache (Tisch, {"tischnr": [(eq, h_bill_line.tischnr)],"departement": [(eq, h_bill_line.departement)]})

                if tisch:
                    t_table_list.table_desc = tisch.bezeich

            if h_bill_line.bill_datum == to_date:

                if (artikel.umsatzart == 3 or artikel.umsatzart == 5):

                    if h_bill_line.betriebsnr == 1:
                        t_table_list.food_amount[0] = t_table_list.food_amount[0] + curr_amount

                    elif h_bill_line.betriebsnr == 2:
                        t_table_list.food_amount[1] = t_table_list.food_amount[1] + curr_amount

                    elif h_bill_line.betriebsnr == 3:
                        t_table_list.food_amount[2] = t_table_list.food_amount[2] + curr_amount

                    elif h_bill_line.betriebsnr == 4:
                        t_table_list.food_amount[3] = t_table_list.food_amount[3] + curr_amount

                elif artikel.umsatzart == 6:

                    if h_bill_line.betriebsnr == 1:
                        t_table_list.bev_amount[0] = t_table_list.bev_amount[0] + curr_amount

                    elif h_bill_line.betriebsnr == 2:
                        t_table_list.bev_amount[1] = t_table_list.bev_amount[1] + curr_amount

                    elif h_bill_line.betriebsnr == 3:
                        t_table_list.bev_amount[2] = t_table_list.bev_amount[2] + curr_amount

                    elif h_bill_line.betriebsnr == 4:
                        t_table_list.bev_amount[3] = t_table_list.bev_amount[3] + curr_amount
                else:

                    if h_bill_line.betriebsnr == 1:
                        t_table_list.other_amount[0] = t_table_list.other_amount[0] + curr_amount

                    elif h_bill_line.betriebsnr == 2:
                        t_table_list.other_amount[1] = t_table_list.other_amount[1] + curr_amount

                    elif h_bill_line.betriebsnr == 3:
                        t_table_list.other_amount[2] = t_table_list.other_amount[2] + curr_amount

                    elif h_bill_line.betriebsnr == 4:
                        t_table_list.other_amount[3] = t_table_list.other_amount[3] + curr_amount

                if h_bill_line.betriebsnr != 0 and curr_rechnr != h_bill_line.rechnr:
                    t_table_list.pax = t_table_list.pax + h_bill.belegung
                    total_pax = total_pax + h_bill.belegung

            if h_bill_line.bill_datum >= from_date and h_bill_line.bill_datum <= to_date:

                if (artikel.umsatzart == 3 or artikel.umsatzart == 5):

                    if h_bill_line.betriebsnr == 1:
                        t_table_list.mtd_food_amount[0] = t_table_list.mtd_food_amount[0] + curr_amount

                    elif h_bill_line.betriebsnr == 2:
                        t_table_list.mtd_food_amount[1] = t_table_list.mtd_food_amount[1] + curr_amount

                    elif h_bill_line.betriebsnr == 3:
                        t_table_list.mtd_food_amount[2] = t_table_list.mtd_food_amount[2] + curr_amount

                    elif h_bill_line.betriebsnr == 4:
                        t_table_list.mtd_food_amount[3] = t_table_list.mtd_food_amount[3] + curr_amount

                elif artikel.umsatzart == 6:

                    if h_bill_line.betriebsnr == 1:
                        t_table_list.mtd_bev_amount[0] = t_table_list.mtd_bev_amount[0] + curr_amount

                    elif h_bill_line.betriebsnr == 2:
                        t_table_list.mtd_bev_amount[1] = t_table_list.mtd_bev_amount[1] + curr_amount

                    elif h_bill_line.betriebsnr == 3:
                        t_table_list.mtd_bev_amount[2] = t_table_list.mtd_bev_amount[2] + curr_amount

                    elif h_bill_line.betriebsnr == 4:
                        t_table_list.mtd_bev_amount[3] = t_table_list.mtd_bev_amount[3] + curr_amount
                else:

                    if h_bill_line.betriebsnr == 1:
                        t_table_list.mtd_other_amount[0] = t_table_list.mtd_other_amount[0] + curr_amount

                    elif h_bill_line.betriebsnr == 2:
                        t_table_list.mtd_other_amount[1] = t_table_list.mtd_other_amount[1] + curr_amount

                    elif h_bill_line.betriebsnr == 3:
                        t_table_list.mtd_other_amount[2] = t_table_list.mtd_other_amount[2] + curr_amount

                    elif h_bill_line.betriebsnr == 4:
                        t_table_list.mtd_other_amount[3] = t_table_list.mtd_other_amount[3] + curr_amount

                if h_bill_line.betriebsnr != 0 and curr_rechnr != h_bill_line.rechnr:
                    t_table_list.mtd_pax = t_table_list.mtd_pax + h_bill.belegung
                    total_mtd_pax = total_mtd_pax + h_bill.belegung

            if (artikel.umsatzart == 3 or artikel.umsatzart == 5):

                if h_bill_line.betriebsnr == 1:
                    t_table_list.ytd_food_amount[0] = t_table_list.ytd_food_amount[0] + curr_amount

                elif h_bill_line.betriebsnr == 2:
                    t_table_list.ytd_food_amount[1] = t_table_list.ytd_food_amount[1] + curr_amount

                elif h_bill_line.betriebsnr == 3:
                    t_table_list.ytd_food_amount[2] = t_table_list.ytd_food_amount[2] + curr_amount

                elif h_bill_line.betriebsnr == 4:
                    t_table_list.ytd_food_amount[3] = t_table_list.ytd_food_amount[3] + curr_amount

            elif artikel.umsatzart == 6:

                if h_bill_line.betriebsnr == 1:
                    t_table_list.ytd_bev_amount[0] = t_table_list.ytd_bev_amount[0] + curr_amount

                elif h_bill_line.betriebsnr == 2:
                    t_table_list.ytd_bev_amount[1] = t_table_list.ytd_bev_amount[1] + curr_amount

                elif h_bill_line.betriebsnr == 3:
                    t_table_list.ytd_bev_amount[2] = t_table_list.ytd_bev_amount[2] + curr_amount

                elif h_bill_line.betriebsnr == 4:
                    t_table_list.ytd_bev_amount[3] = t_table_list.ytd_bev_amount[3] + curr_amount
            else:

                if h_bill_line.betriebsnr == 1:
                    t_table_list.ytd_other_amount[0] = t_table_list.ytd_other_amount[0] + curr_amount

                elif h_bill_line.betriebsnr == 2:
                    t_table_list.ytd_other_amount[1] = t_table_list.ytd_other_amount[1] + curr_amount

                elif h_bill_line.betriebsnr == 3:
                    t_table_list.ytd_other_amount[2] = t_table_list.ytd_other_amount[2] + curr_amount

                elif h_bill_line.betriebsnr == 4:
                    t_table_list.ytd_other_amount[3] = t_table_list.ytd_other_amount[3] + curr_amount

            if h_bill_line.betriebsnr != 0 and curr_rechnr != h_bill_line.rechnr:
                t_table_list.ytd_pax = t_table_list.ytd_pax + h_bill.belegung
                total_ytd_pax = total_ytd_pax + h_bill.belegung
            curr_rechnr = h_bill_line.rechnr

        for t_table_list in query(t_table_list_data, sort_by=[("to_int(",False))]:
            turnover_table_list = Turnover_table_list()
            turnover_table_list_data.append(turnover_table_list)

            turnover_table_list.table_no = to_string(t_table_list.table_no, ">>>,>>>")
            turnover_table_list.table_desc = t_table_list.table_desc
            turnover_table_list.pax = t_table_list.pax
            turnover_table_list.mtd_pax = t_table_list.mtd_pax
            turnover_table_list.ytd_pax = t_table_list.ytd_pax


            for i in range(1,4 + 1) :
                turnover_table_list.food_amount[i - 1] = to_string(t_table_list.food_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.bev_amount[i - 1] = to_string(t_table_list.bev_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.other_amount[i - 1] = to_string(t_table_list.other_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.mtd_food_amount[i - 1] = to_string(t_table_list.mtd_food_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.mtd_bev_amount[i - 1] = to_string(t_table_list.mtd_bev_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.mtd_other_amount[i - 1] = to_string(t_table_list.mtd_other_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.ytd_food_amount[i - 1] = to_string(t_table_list.ytd_food_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.ytd_bev_amount[i - 1] = to_string(t_table_list.ytd_bev_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.ytd_other_amount[i - 1] = to_string(t_table_list.ytd_other_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")


                tot_food_amount[i - 1] = tot_food_amount[i - 1] + t_table_list.food_amount[i - 1]
                tot_bev_amount[i - 1] = tot_bev_amount[i - 1] + t_table_list.bev_amount[i - 1]
                tot_other_amount[i - 1] = tot_other_amount[i - 1] + t_table_list.other_amount[i - 1]
                tot_mtd_food_amount[i - 1] = tot_mtd_food_amount[i - 1] + t_table_list.mtd_food_amount[i - 1]
                tot_mtd_bev_amount[i - 1] = tot_mtd_bev_amount[i - 1] + t_table_list.mtd_bev_amount[i - 1]
                tot_mtd_other_amount[i - 1] = tot_mtd_other_amount[i - 1] + t_table_list.mtd_other_amount[i - 1]
                tot_ytd_food_amount[i - 1] = tot_ytd_food_amount[i - 1] + t_table_list.ytd_food_amount[i - 1]
                tot_ytd_bev_amount[i - 1] = tot_ytd_bev_amount[i - 1] + t_table_list.ytd_bev_amount[i - 1]
                tot_ytd_other_amount[i - 1] = tot_ytd_other_amount[i - 1] + t_table_list.ytd_other_amount[i - 1]

        turnover_table_list = query(turnover_table_list_data, first=True)

        if turnover_table_list:
            turnover_table_list = Turnover_table_list()
            turnover_table_list_data.append(turnover_table_list)

            turnover_table_list.table_desc = "T O T A L"
            turnover_table_list.pax = total_pax
            turnover_table_list.mtd_pax = total_mtd_pax
            turnover_table_list.ytd_pax = total_ytd_pax


            for i in range(1,4 + 1) :
                turnover_table_list.food_amount[i - 1] = to_string(tot_food_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.bev_amount[i - 1] = to_string(tot_bev_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.other_amount[i - 1] = to_string(tot_other_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.mtd_food_amount[i - 1] = to_string(tot_mtd_food_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.mtd_bev_amount[i - 1] = to_string(tot_mtd_bev_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.mtd_other_amount[i - 1] = to_string(tot_mtd_other_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.ytd_food_amount[i - 1] = to_string(tot_ytd_food_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.ytd_bev_amount[i - 1] = to_string(tot_ytd_bev_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")
                turnover_table_list.ytd_other_amount[i - 1] = to_string(tot_ytd_other_amount[i - 1], "->>,>>>,>>>,>>>,>>9.99")


    def cal_servat(depart:int, h_artnr:int, service_code:int, mwst_code:int, inpdate:date):

        nonlocal turnover_table_list_data, start_jan, i, curr_rechnr, curr_amount, tot_food_amount, tot_bev_amount, tot_other_amount, tot_mtd_food_amount, tot_mtd_bev_amount, tot_mtd_other_amount, tot_ytd_food_amount, tot_ytd_bev_amount, tot_ytd_other_amount, total_pax, total_mtd_pax, total_ytd_pax, servtax_use_foart, serv_percent, mwst_percent, fact, bill_date110, bill_date, service_taxable, hoteldpt, htparam, h_bill, h_artikel, artikel, h_bill_line, h_compli, tisch, kontplan
        nonlocal from_date, to_date, dept_number, excl_compli, excl_taxserv


        nonlocal turnover_table_list, t_table_list
        nonlocal turnover_table_list_data, t_table_list_data

        serv_percent = to_decimal("0.0")
        mwst_percent = to_decimal("0.0")
        servat = to_decimal("0.0")
        serv_htp:Decimal = to_decimal("0.0")
        vat_htp:Decimal = to_decimal("0.0")
        ct:string = ""
        l_deci:int = 2
        hbuff = None
        abuff = None

        def generate_inner_output():
            return (serv_percent, mwst_percent, servat)

        Hbuff =  create_buffer("Hbuff",H_artikel)
        Abuff =  create_buffer("Abuff",Artikel)

        if bill_date < bill_date110 and (service_code != 0 or mwst_code != 0):

            hbuff = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, depart)]})

            abuff = get_cache (Artikel, {"artnr": [(eq, hbuff.artnrfront)],"departement": [(eq, depart)]})

            kontplan = get_cache (Kontplan, {"betriebsnr": [(eq, depart)],"kontignr": [(eq, abuff.artnr)],"datum": [(eq, inpdate)]})

            if kontplan:
                serv_htp =  to_decimal(kontplan.anzkont) / to_decimal("10000")
                vat_htp =  to_decimal(kontplan.anzconf) / to_decimal("10000")


                serv_percent =  to_decimal(serv_htp)
                mwst_percent =  to_decimal(vat_htp)
                servat =  to_decimal("1") + to_decimal(serv_percent) + to_decimal(mwst_percent)

                return generate_inner_output()
        serv_htp =  to_decimal("0")
        vat_htp =  to_decimal("0")

        if servtax_use_foart:

            hbuff = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, depart)]})

            abuff = get_cache (Artikel, {"artnr": [(eq, hbuff.artnrfront)],"departement": [(eq, depart)]})

            if abuff:
                service_code = abuff.service_code
                mwst_code = abuff.mwst_code
        else:

            hbuff = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, depart)]})

            if hbuff:
                service_code = hbuff.service_code
                mwst_code = hbuff.mwst_code

        if service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, service_code)]})
            serv_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, mwst_code)]})
            vat_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if service_taxable:
            serv_percent =  to_decimal(serv_htp)
            mwst_percent = ( to_decimal("1") + to_decimal(serv_htp)) * to_decimal(vat_htp)
            servat =  to_decimal("1") + to_decimal(serv_percent) + to_decimal(mwst_percent)


        else:
            serv_percent =  to_decimal(serv_htp)
            mwst_percent =  to_decimal(vat_htp)
            servat =  to_decimal("1") + to_decimal(serv_percent) + to_decimal(mwst_percent)


        ct = replace_str(to_string(mwst_percent) , ".", ",")
        l_deci = length(entry(1, ct, ","))

        if l_deci <= 2:
            mwst_percent = to_decimal(round(mwst_percent , 2))

        elif l_deci == 3:
            mwst_percent = to_decimal(round(mwst_percent , 3))
        else:
            mwst_percent = to_decimal(round(mwst_percent , 4))
        ct = replace_str(to_string(servat) , ".", ",")
        l_deci = length(entry(1, ct, ","))

        if l_deci <= 2:
            servat = to_decimal(round(servat , 2))

        elif l_deci == 3:
            servat = to_decimal(round(servat , 3))
        else:
            servat = to_decimal(round(servat , 4))

        return generate_inner_output()


    start_jan = date_mdy(1, 1, get_year(to_date))

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept_number)]})

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date110 = htparam.fdate
        bill_date = htparam.fdate


    create_turnover_table()

    return generate_output()