#using conversion tools version: 1.0.0.118
#-----------------------------------------
# Rd, 2/8/2025
# Optimasi
#-----------------------------------------


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Hoteldpt, Artikel, Zwkum, Budget, Umsatz, Ekum, Kontplan

def revenue_report_1bl(sorttype:int, long_digit:bool, short_flag:bool, from_date:date, to_date:date):

    prepare_cache ([Htparam, Hoteldpt, Artikel, Zwkum, Budget, Umsatz, Ekum])

    output_list_data = []
    fact1:int = 0
    price_decimal:int = 0
    curr_dept:string = ""
    curr_art:int = 0
    bezeich:string = ""
    datum:date = None
    ly_datum:date = None
    jan1:date = None
    ly_jan1:date = None
    lm_fdate:date = None
    lm_tdate:date = None
    ly_fdate:date = None
    ly_tdate:date = None
    fact:Decimal = to_decimal("0.0")
    ekum_serverless:int = 0
    dnet:Decimal = to_decimal("0.0")
    mnet:Decimal = to_decimal("0.0")
    ynet:Decimal = to_decimal("0.0")
    lm_mnet:Decimal = to_decimal("0.0")
    ly_mnet:Decimal = to_decimal("0.0")
    ly_ynet:Decimal = to_decimal("0.0")
    tdnet:Decimal = to_decimal("0.0")
    tmnet:Decimal = to_decimal("0.0")
    tynet:Decimal = to_decimal("0.0")
    tlm_mnet:Decimal = to_decimal("0.0")
    tly_mnet:Decimal = to_decimal("0.0")
    tly_ynet:Decimal = to_decimal("0.0")
    taxnr:int = 0
    servnr:int = 0
    do_it:bool = False
    vat:Decimal = to_decimal("0.0")
    serv:Decimal = to_decimal("0.0")
    nett_serv:Decimal = to_decimal("0.0")
    nett_tax:Decimal = to_decimal("0.0")
    nett_amt:Decimal = to_decimal("0.0")
    dept:int = -1
    zwkum_serverless:int = 0
    serv_vat:bool = False
    mbudget:Decimal = to_decimal("0.0")
    t_mbudget:Decimal = to_decimal("0.0")
    tmp_month:int = 0
    year_ly_jan1:int = 0
    num_year_ly_jan1:int = 0
    year_ly_fdate:int = 0
    year_ly_tdate:int = 0
    num_year_datum:int = 0
    tmp_day:date = None
    htparam = hoteldpt = artikel = zwkum = budget = umsatz = ekum = kontplan = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":string, "str":string, "bezeich":string, "tnett":Decimal, "mtd":Decimal, "mtd_budget":Decimal, "ytd_budget":Decimal, "lmon_mtd":Decimal, "lyear_mtd":Decimal, "lyear_ytd":Decimal})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "artnr":int, "kum":int, "dept":int, "bezeich":string, "dnet":Decimal, "mnet":Decimal, "mbudget":Decimal, "ynet":Decimal, "lm_mnet":Decimal, "ly_mnet":Decimal, "ly_ynet":Decimal})


    set_cache(Zwkum, None,[["zknr", "departement"]], True,[],[])
    set_cache(Ekum, None,[["eknr"]], True,[],[])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, fact1, price_decimal, curr_dept, curr_art, bezeich, datum, ly_datum, jan1, ly_jan1, lm_fdate, lm_tdate, ly_fdate, ly_tdate, fact, ekum_serverless, dnet, mnet, ynet, lm_mnet, ly_mnet, ly_ynet, tdnet, tmnet, tynet, tlm_mnet, tly_mnet, tly_ynet, taxnr, servnr, do_it, vat, serv, nett_serv, nett_tax, nett_amt, dept, zwkum_serverless, serv_vat, mbudget, t_mbudget, tmp_month, year_ly_jan1, num_year_ly_jan1, year_ly_fdate, year_ly_tdate, num_year_datum, tmp_day, htparam, hoteldpt, artikel, zwkum, budget, umsatz, ekum, kontplan
        nonlocal sorttype, long_digit, short_flag, from_date, to_date


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {"output-list": output_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_vat = htparam.flogical
    jan1 = date_mdy(1, 1, get_year(from_date))
    num_year_ly_jan1 = get_year(jan1) - 1
    ly_jan1 = date_mdy(1, 1, num_year_ly_jan1)

    set_cache(Umsatz, (Umsatz.datum >= ly_jan1) & (Umsatz.datum <= to_date),[["artnr", "departement", "datum"]], True,[],[])


    set_cache(Kontplan, (Kontplan.datum >= ly_jan1) & (Kontplan.datum <= to_date),[["betriebsnr", "kontignr", "datum"]], True,[],[])


    set_cache(Budget, (Budget.datum >= ly_jan1) & (Budget.datum <= to_date),[["departement", "artnr", "datum"]], True,[],[])


    if sorttype == 1:

        if not long_digit or not short_flag:
            fact1 = 1
        else:
            fact1 = 1000
        output_list_data.clear()
        cl_list_data.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
        taxnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})
        servnr = htparam.finteger
        tmp_month = get_month(from_date) - 1

        if get_month(to_date) >= 2:

            if get_day(from_date) == 1:
                lm_fdate = date_mdy(tmp_month, 1, get_year(from_date))
            else:
                lm_fdate = from_date - timedelta(days=30)
            tmp_day = to_date + timedelta(days=1)

            if get_day(tmp_day) == 1:
                lm_tdate = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)
            else:
                lm_tdate = to_date - timedelta(days=30)
        else:
            lm_fdate = from_date - timedelta(days=31)
            lm_tdate = to_date - timedelta(days=31)
        year_ly_tdate = get_year(to_date) - 1
        year_ly_fdate = get_year(from_date) - 1

        if get_day(from_date) == 29 and get_month(from_date) == 2:
            ly_fdate = date_mdy(2, 28, year_ly_fdate)
        else:
            ly_fdate = date_mdy(get_month(from_date) , get_day(from_date) , year_ly_fdate)

        if get_day(to_date) == 29 and get_month(to_date) == 2:
            ly_tdate = date_mdy(2, 28, year_ly_tdate)
        else:
            ly_tdate = date_mdy(get_month(to_date) , get_day(to_date) , year_ly_tdate)

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt.num).all():
            curr_dept = hoteldpt.depart

            if dept == -1:
                dept = hoteldpt.num

            if dept != hoteldpt.num:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.bezeich = "T o t a l"
                cl_list.flag = "**"
                cl_list.dnet =  to_decimal(dnet)
                cl_list.mnet =  to_decimal(mnet)
                cl_list.mbudget =  to_decimal(mbudget)
                cl_list.ynet =  to_decimal(ynet)
                cl_list.lm_mnet =  to_decimal(lm_mnet)
                cl_list.ly_mnet =  to_decimal(ly_mnet)
                cl_list.ly_ynet =  to_decimal(ly_ynet)


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                dnet =  to_decimal("0")
                mnet =  to_decimal("0")
                ynet =  to_decimal("0")
                lm_mnet =  to_decimal("0")
                ly_mnet =  to_decimal("0")
                ly_ynet =  to_decimal("0")
                mbudget =  to_decimal("0")
                dept = hoteldpt.num


            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = "*"
            cl_list.bezeich = hoteldpt.depart
            zwkum_serverless = 0

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == hoteldpt.num) & ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel.zwkum).all():
                bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
                do_it = True

                if (artikel.artnr == taxnr or artikel.artnr == servnr) and artikel.departement == 0:
                    do_it = False

                if do_it:

                    if zwkum_serverless != artikel.zwkum:
                        zwkum_serverless = artikel.zwkum

                        zwkum = get_cache (Zwkum, {"zknr": [(eq, artikel.zwkum)],"departement": [(eq, artikel.departement)]})

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.kum == artikel.zwkum and cl_list.dept == artikel.departement), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.kum = artikel.zwkum
                        cl_list.artnr = artikel.artnr
                        cl_list.dept = artikel.departement

                        if zwkum:
                            cl_list.bezeich = zwkum.bezeich
                    for datum in date_range(jan1,to_date) :

                        if datum >= from_date:

                            budget = get_cache (Budget, {"departement": [(eq, artikel.departement)],"artnr": [(eq, artikel.artnr)],"datum": [(eq, datum)]})

                            if budget:
                                cl_list.mbudget =  to_decimal(cl_list.mbudget) + to_decimal(budget.betrag)
                                mbudget =  to_decimal(mbudget) + to_decimal(budget.betrag)
                                t_mbudget =  to_decimal(t_mbudget) + to_decimal(budget.betrag)

                        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, datum)]})

                        if umsatz:
                            fact =  to_decimal("0")
                            serv =  to_decimal("0")
                            vat =  to_decimal("0")


                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                            fact =  to_decimal(fact) * to_decimal(fact1)
                            nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                            nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                            nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                            nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)

                            if umsatz.datum == to_date:
                                cl_list.dnet =  to_decimal(cl_list.dnet) + to_decimal(nett_amt)
                                dnet =  to_decimal(dnet) + to_decimal(nett_amt)
                                tdnet =  to_decimal(tdnet) + to_decimal(nett_amt)

                            if datum >= from_date:
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(nett_amt)
                                mnet =  to_decimal(mnet) + to_decimal(nett_amt)
                                tmnet =  to_decimal(tmnet) + to_decimal(nett_amt)


                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(nett_amt)
                            ynet =  to_decimal(ynet) + to_decimal(nett_amt)
                            tynet =  to_decimal(tynet) + to_decimal(nett_amt)

                            if datum >= lm_fdate and datum <= lm_tdate:
                                cl_list.lm_mnet =  to_decimal(cl_list.lm_mnet) + to_decimal(nett_amt)
                                lm_mnet =  to_decimal(lm_mnet) + to_decimal(nett_amt)
                                tlm_mnet =  to_decimal(tlm_mnet) + to_decimal(nett_amt)

                        if get_day(datum) == 29 and get_month(datum) == 2:
                            pass
                        else:
                            num_year_datum = get_year(datum) - 1
                            ly_datum = date_mdy(get_month(datum) , get_day(datum) , num_year_datum)

                            umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, ly_datum)]})

                            if umsatz:
                                fact =  to_decimal("0")
                                serv =  to_decimal("0")
                                vat =  to_decimal("0")


                                serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                                fact =  to_decimal(fact) * to_decimal(fact1)
                                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                                nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                                nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)

                                if ly_datum >= ly_fdate:
                                    cl_list.ly_mnet =  to_decimal(cl_list.ly_mnet) + to_decimal(nett_amt)
                                    ly_mnet =  to_decimal(ly_mnet) + to_decimal(nett_amt)
                                    tly_mnet =  to_decimal(tly_mnet) + to_decimal(nett_amt)
                                cl_list.ly_ynet =  to_decimal(cl_list.ly_ynet) + to_decimal(nett_amt)


                                ly_ynet =  to_decimal(ly_ynet) + to_decimal(nett_amt)
                                tly_ynet =  to_decimal(tly_ynet) + to_decimal(nett_amt)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.kum = zwkum_serverless
        cl_list.bezeich = "T o t a l"
        cl_list.flag = "**"
        cl_list.dnet =  to_decimal(dnet)
        cl_list.mnet =  to_decimal(mnet)
        cl_list.mbudget =  to_decimal(mbudget)
        cl_list.ynet =  to_decimal(ynet)
        cl_list.lm_mnet =  to_decimal(lm_mnet)
        cl_list.ly_mnet =  to_decimal(ly_mnet)
        cl_list.ly_ynet =  to_decimal(ly_ynet)


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Grand T o t a l"
        cl_list.flag = "***"
        cl_list.dnet =  to_decimal(tdnet)
        cl_list.mnet =  to_decimal(tmnet)
        cl_list.mbudget =  to_decimal(t_mbudget)
        cl_list.ynet =  to_decimal(tynet)
        cl_list.lm_mnet =  to_decimal(tlm_mnet)
        cl_list.ly_mnet =  to_decimal(tly_mnet)
        cl_list.ly_ynet =  to_decimal(tly_ynet)

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)


            if cl_list.bezeich != "":
                output_list.flag = cl_list.flag
                output_list.str = to_string(cl_list.bezeich, "x(24)")

                if cl_list.flag.lower()  != ("*").lower() :

                    if price_decimal == 2:
                        output_list.str = output_list.str + to_string(cl_list.dnet, "->>>,>>9.99") + to_string(cl_list.mnet, "->>>>,>>9.99") + to_string(cl_list.mbudget, "->,>>>,>>9.99") + to_string(cl_list.ynet, "->>,>>>,>>9.99") + to_string(cl_list.lm_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_ynet, "->>,>>>,>>9.99")

                    elif not long_digit or (long_digit and short_flag):
                        output_list.str = output_list.str + to_string(cl_list.dnet, "->>,>>>,>>9") + to_string(cl_list.mnet, "->>>,>>>,>>9") + to_string(cl_list.mbudget, "->>>,>>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>9") + to_string(cl_list.lm_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_ynet, "->,>>>,>>>,>>9")
                    else:
                        output_list.str = output_list.str + to_string(cl_list.dnet, "->>>>>>>>>9") + to_string(cl_list.mnet, "->>>>>>>>>>9") + to_string(cl_list.mbudget, "->>>>>>>>>>9") + to_string(cl_list.ynet, "->>>>>>>>>>>>9") + to_string(cl_list.lm_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_ynet, "->>>>>>>>>>>>9")
                    output_list.bezeich = cl_list.bezeich
                    output_list.tnett =  to_decimal(cl_list.dnet)
                    output_list.mtd =  to_decimal(cl_list.mnet)
                    output_list.mtd_budget =  to_decimal(cl_list.mbudget)
                    output_list.ytd_budget =  to_decimal(cl_list.ynet)
                    output_list.lmon_mtd =  to_decimal(cl_list.lm_mnet)
                    output_list.lyear_mtd =  to_decimal(cl_list.ly_mnet)
                    output_list.lyear_ytd =  to_decimal(cl_list.ly_ynet)

    if sorttype == 2:

        if not long_digit or not short_flag:
            fact1 = 1
        else:
            fact1 = 1000
        output_list_data.clear()
        cl_list_data.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
        taxnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})
        servnr = htparam.finteger
        year_ly_fdate = get_year(from_date) - 1
        year_ly_tdate = get_year(to_date) - 1
        tmp_day = to_date + timedelta(days=1)
        tmp_month = get_month(from_date) - 1

        if get_month(to_date) >= 2:

            if get_day(from_date) == 1:
                lm_fdate = date_mdy(tmp_month, 1, get_year(from_date))
            else:
                lm_fdate = from_date - timedelta(days=30)

            if get_day(tmp_day) == 1:
                lm_tdate = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)
            else:
                lm_tdate = to_date - timedelta(days=30)
        else:
            lm_fdate = from_date - timedelta(days=31)
            lm_tdate = to_date - timedelta(days=31)

        if get_day(from_date) == 29 and get_month(from_date) == 2:
            ly_fdate = date_mdy(2, 28, year_ly_fdate)
        else:
            ly_fdate = date_mdy(get_month(from_date) , get_day(from_date) , year_ly_fdate)

        if get_day(to_date) == 29 and get_month(to_date) == 2:
            ly_tdate = date_mdy(2, 28, year_ly_tdate)
        else:
            ly_tdate = date_mdy(get_month(to_date) , get_day(to_date) , year_ly_tdate)
        ekum_serverless = 0

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel.endkum, Artikel.bezeich).all():

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})

            if hoteldpt:
                curr_dept = hoteldpt.depart
                bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
            do_it = True

            if (artikel.artnr == taxnr or artikel.artnr == servnr) and artikel.departement == 0:
                do_it = False

            if do_it:

                if ekum_serverless == 0:
                    ekum_serverless = artikel.endkum

                    ekum = get_cache (Ekum, {"eknr": [(eq, artikel.endkum)]})
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.flag = "**"
                    cl_list.kum = artikel.endkum

                    if ekum:
                        cl_list.bezeich = ekum.bezeich

                if ekum_serverless != artikel.endkum:
                    cl_list.dnet =  to_decimal(dnet)
                    cl_list.mnet =  to_decimal(mnet)
                    cl_list.mbudget =  to_decimal(mbudget)
                    cl_list.ynet =  to_decimal(ynet)
                    cl_list.lm_mnet =  to_decimal(lm_mnet)
                    cl_list.ly_mnet =  to_decimal(ly_mnet)
                    cl_list.ly_ynet =  to_decimal(ly_ynet)
                    ekum_serverless = artikel.endkum

                    ekum = get_cache (Ekum, {"eknr": [(eq, artikel.endkum)]})
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    dnet =  to_decimal("0")
                    mnet =  to_decimal("0")
                    ynet =  to_decimal("0")
                    lm_mnet =  to_decimal("0")
                    ly_mnet =  to_decimal("0")
                    ly_ynet =  to_decimal("0")
                    mbudget =  to_decimal("0")


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.flag = "**"
                    cl_list.kum = artikel.endkum

                    if ekum:
                        cl_list.bezeich = ekum.bezeich

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.kum == artikel.endkum), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.kum = artikel.endkum

                    if ekum:
                        cl_list.bezeich = ekum.bezeich
                for datum in date_range(jan1,to_date) :

                    if datum >= from_date:

                        budget = get_cache (Budget, {"departement": [(eq, artikel.departement)],"artnr": [(eq, artikel.artnr)],"datum": [(eq, datum)]})

                        if budget:
                            cl_list.mbudget =  to_decimal(cl_list.mbudget) + to_decimal(budget.betrag)
                            mbudget =  to_decimal(mbudget) + to_decimal(budget.betrag)
                            t_mbudget =  to_decimal(t_mbudget) + to_decimal(budget.betrag)

                    umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, datum)]})

                    if umsatz:
                        fact =  to_decimal("0")
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")


                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                        fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                        fact =  to_decimal(fact) * to_decimal(fact1)
                        nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                        nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                        nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                        nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)

                        if umsatz.datum == to_date:
                            cl_list.dnet =  to_decimal(cl_list.dnet) + to_decimal(nett_amt)
                            dnet =  to_decimal(dnet) + to_decimal(nett_amt)
                            tdnet =  to_decimal(tdnet) + to_decimal(nett_amt)

                        if datum >= from_date:
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(nett_amt)
                            mnet =  to_decimal(mnet) + to_decimal(nett_amt)
                            tmnet =  to_decimal(tmnet) + to_decimal(nett_amt)


                        cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(nett_amt)
                        ynet =  to_decimal(ynet) + to_decimal(nett_amt)
                        tynet =  to_decimal(tynet) + to_decimal(nett_amt)

                        if datum >= lm_fdate and datum <= lm_tdate:
                            cl_list.lm_mnet =  to_decimal(cl_list.lm_mnet) + to_decimal(nett_amt)
                            lm_mnet =  to_decimal(lm_mnet) + to_decimal(nett_amt)


                            tlm_mnet =  to_decimal(tlm_mnet) + to_decimal(nett_amt)

                    if get_day(datum) == 29 and get_month(datum) == 2:
                        pass
                    else:
                        num_year_datum = get_year(datum) - 1
                        ly_datum = date_mdy(get_month(datum) , get_day(datum) , num_year_datum)

                        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, ly_datum)]})

                        if umsatz:
                            fact =  to_decimal("0")
                            serv =  to_decimal("0")
                            vat =  to_decimal("0")


                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                            fact =  to_decimal(fact) * to_decimal(fact1)
                            nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                            nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                            nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                            nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)

                            if ly_datum >= ly_fdate:
                                cl_list.ly_mnet =  to_decimal(cl_list.ly_mnet) + to_decimal(nett_amt)
                                ly_mnet =  to_decimal(ly_mnet) + to_decimal(nett_amt)
                                tly_mnet =  to_decimal(tly_mnet) + to_decimal(nett_amt)


                            cl_list.ly_ynet =  to_decimal(cl_list.ly_ynet) + to_decimal(nett_amt)
                            ly_ynet =  to_decimal(ly_ynet) + to_decimal(nett_amt)
                            tly_ynet =  to_decimal(tly_ynet) + to_decimal(nett_amt)


        cl_list.dnet =  to_decimal(dnet)
        cl_list.mnet =  to_decimal(mnet)
        cl_list.mbudget =  to_decimal(mbudget)
        cl_list.ynet =  to_decimal(ynet)
        cl_list.lm_mnet =  to_decimal(lm_mnet)
        cl_list.ly_mnet =  to_decimal(ly_mnet)
        cl_list.ly_ynet =  to_decimal(ly_ynet)


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Grand T o t a l"
        cl_list.flag = "***"
        cl_list.dnet =  to_decimal(tdnet)
        cl_list.mnet =  to_decimal(tmnet)
        cl_list.mbudget =  to_decimal(t_mbudget)
        cl_list.ynet =  to_decimal(tynet)
        cl_list.lm_mnet =  to_decimal(tlm_mnet)
        cl_list.ly_mnet =  to_decimal(tly_mnet)
        cl_list.ly_ynet =  to_decimal(tly_ynet)

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)


            if cl_list.bezeich != "":
                output_list.flag = cl_list.flag
                output_list.str = to_string(cl_list.bezeich, "x(24)")

                if cl_list.flag.lower()  != ("*").lower() :

                    if price_decimal == 2:
                        output_list.str = output_list.str + to_string(cl_list.dnet, "->>>,>>9.99") + to_string(cl_list.mnet, "->>>>,>>9.99") + to_string(cl_list.mbudget, "->,>>>,>>9.99") + to_string(cl_list.ynet, "->>,>>>,>>9.99") + to_string(cl_list.lm_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_ynet, "->>,>>>,>>9.99")

                    elif not long_digit or (long_digit and short_flag):
                        output_list.str = output_list.str + to_string(cl_list.dnet, "->>,>>>,>>9") + to_string(cl_list.mnet, "->>>,>>>,>>9") + to_string(cl_list.mbudget, "->>>,>>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>9") + to_string(cl_list.lm_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_ynet, "->,>>>,>>>,>>9")
                    else:
                        output_list.str = output_list.str + to_string(cl_list.dnet, "->>>>>>>>>9") + to_string(cl_list.mnet, "->>>>>>>>>>9") + to_string(cl_list.mbudget, "->>>>>>>>>>9") + to_string(cl_list.ynet, "->>>>>>>>>>>>9") + to_string(cl_list.lm_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_ynet, "->>>>>>>>>>>>9")
                    output_list.bezeich = cl_list.bezeich
                    output_list.tnett =  to_decimal(cl_list.dnet)
                    output_list.mtd =  to_decimal(cl_list.mnet)
                    output_list.mtd_budget =  to_decimal(cl_list.mbudget)
                    output_list.ytd_budget =  to_decimal(cl_list.ynet)
                    output_list.lmon_mtd =  to_decimal(cl_list.lm_mnet)
                    output_list.lyear_mtd =  to_decimal(cl_list.ly_mnet)
                    output_list.lyear_ytd =  to_decimal(cl_list.ly_ynet)

    return generate_output()