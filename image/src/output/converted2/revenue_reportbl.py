#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Hoteldpt, Artikel, zwkum, Umsatz, Budget, Ekum

def revenue_reportbl(sorttype:int, long_digit:bool, short_flag:bool, from_date:date, to_date:date):

    prepare_cache ([Htparam, Hoteldpt, Artikel, zwkum, Umsatz, Budget, Ekum])

    output_list_list = []
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
    ekum_no:int = 0
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
    zwkum:int = 0
    serv_vat:bool = False
    mbudget:Decimal = to_decimal("0.0")
    t_mbudget:Decimal = to_decimal("0.0")
    lm_mtd_datum:date = None
    htparam = hoteldpt = artikel = zwkum = umsatz = budget = ekum = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":string, "str":string})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":string, "artnr":int, "kum":int, "dept":int, "bezeich":string, "dnet":Decimal, "mnet":Decimal, "mbudget":Decimal, "ynet":Decimal, "lm_mnet":Decimal, "ly_mnet":Decimal, "ly_ynet":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, fact1, price_decimal, curr_dept, curr_art, bezeich, datum, ly_datum, jan1, ly_jan1, lm_fdate, lm_tdate, ly_fdate, ly_tdate, fact, ekum_no, dnet, mnet, ynet, lm_mnet, ly_mnet, ly_ynet, tdnet, tmnet, tynet, tlm_mnet, tly_mnet, tly_ynet, taxnr, servnr, do_it, vat, serv, nett_serv, nett_tax, nett_amt, dept, zwkum, serv_vat, mbudget, t_mbudget, lm_mtd_datum, htparam, hoteldpt, artikel, zwkum, umsatz, budget, ekum
        nonlocal sorttype, long_digit, short_flag, from_date, to_date


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {"output-list": output_list_list}

    def cal_tax_service():

        nonlocal output_list_list, fact1, price_decimal, curr_dept, curr_art, bezeich, datum, ly_datum, jan1, ly_jan1, lm_fdate, lm_tdate, ly_fdate, ly_tdate, fact, ekum_no, dnet, mnet, ynet, lm_mnet, ly_mnet, ly_ynet, tdnet, tmnet, tynet, tlm_mnet, tly_mnet, tly_ynet, taxnr, servnr, do_it, vat, serv, nett_serv, nett_tax, nett_amt, dept, zwkum, serv_vat, mbudget, t_mbudget, lm_mtd_datum, htparam, hoteldpt, artikel, zwkum, umsatz, budget, ekum
        nonlocal sorttype, long_digit, short_flag, from_date, to_date


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        fact = to_decimal("0.0")
        vat = to_decimal("0.0")
        serv = to_decimal("0.0")

        def generate_inner_output():
            return (fact, vat, serv)

        serv =  to_decimal("0")
        vat =  to_decimal("0")

        if artikel.service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                serv =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if artikel.mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                if serv_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(serv)
                vat =  to_decimal(round (vat , 2))
        fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
        fact =  to_decimal(fact) * to_decimal(fact1)

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_vat = htparam.flogical

    if sorttype == 1:

        if not long_digit or not short_flag:
            fact1 = 1
        else:
            fact1 = 1000
        output_list_list.clear()
        cl_list_list.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
        taxnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})
        servnr = htparam.finteger
        jan1 = date_mdy(1, 1, get_year(from_date))
        ly_jan1 = date_mdy(1, 1, get_year(jan1) - timedelta(days=1))

        if get_month(to_date) >= 2:

            if get_day(from_date) == 1:
                lm_fdate = date_mdy(get_month(from_date) - timedelta(days=1, 1, get_year(from_date)))
            else:
                lm_fdate = from_date - timedelta(days=30)

            if get_day(to_date + 1) == 1:
                lm_tdate = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)
            else:
                lm_tdate = to_date - timedelta(days=30)
        else:
            lm_fdate = from_date - timedelta(days=31)
            lm_tdate = to_date - timedelta(days=31)

        if get_day(from_date) == 29 and get_month(from_date) == 2:
            ly_fdate = date_mdy(2, 28, get_year(from_date) - timedelta(days=1))
        else:
            ly_fdate = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - timedelta(days=1))

        if get_day(to_date) == 29 and get_month(to_date) == 2:
            ly_tdate = date_mdy(2, 28, get_year(to_date) - timedelta(days=1))
        else:
            ly_tdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt.num).all():
            curr_dept = hoteldpt.depart

            if dept == -1:
                dept = hoteldpt.num

            if dept != hoteldpt.num:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

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
                cl_list_list.append(cl_list)

                dnet =  to_decimal("0")
                mnet =  to_decimal("0")
                ynet =  to_decimal("0")
                lm_mnet =  to_decimal("0")
                ly_mnet =  to_decimal("0")
                ly_ynet =  to_decimal("0")
                mbudget =  to_decimal("0")
                dept = hoteldpt.num


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.flag = "*"
            cl_list.bezeich = hoteldpt.depart
            zwkum = 0

            for artikel in db_session.query(Artikel).filter(
                     ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.departement == hoteldpt.num)).order_by(Artikel.zwkum).all():
                bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
                do_it = True

                if (artikel.artnr == taxnr or artikel.artnr == servnr) and artikel.departement == 0:
                    do_it = False

                if do_it:

                    if zwkum != artikel.zwkum:
                        zwkum = artikel.zwkum

                        zwkum = get_cache (zwkum, {"zknr": [(eq, artikel.zwkum)],"departement": [(eq, artikel.departement)]})

                    cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.kum == artikel.zwkum and cl_list.dept == artikel.departement), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.kum = artikel.zwkum
                        cl_list.artnr = artikel.artnr
                        cl_list.dept = artikel.departement
                        cl_list.bezeich = zwkum.bezeich
                    for datum in date_range(jan1,to_date) :

                        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, datum)]})

                        if umsatz:
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

                                for budget in db_session.query(Budget).filter(
                                         (Budget.departement == umsatz.departement) & (Budget.artnr == umsatz.artnr) & (Budget.datum == datum)).order_by(Budget._recid).all():
                                    cl_list.mbudget =  to_decimal(cl_list.mbudget) + to_decimal(budget.betrag)
                                    mbudget =  to_decimal(mbudget) + to_decimal(budget.betrag)
                                    t_mbudget =  to_decimal(t_mbudget) + to_decimal(budget.betrag)


                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(nett_amt)
                            ynet =  to_decimal(ynet) + to_decimal(nett_amt)
                            tynet =  to_decimal(tynet) + to_decimal(nett_amt)

                        if get_day(datum) == 29 and get_month(datum) == 2:
                            pass
                        else:
                            ly_datum = date_mdy(get_month(datum) , get_day(datum) , get_year(datum) - timedelta(days=1))

                            umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, ly_datum)]})

                            if umsatz:
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

                    for umsatz in db_session.query(Umsatz).filter(
                             (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum >= lm_fdate) & (Umsatz.datum <= lm_tdate)).order_by(Umsatz._recid).all():
                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                        fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                        fact =  to_decimal(fact) * to_decimal(fact1)
                        nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                        nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                        nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                        nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)
                        cl_list.lm_mnet =  to_decimal(cl_list.lm_mnet) + to_decimal(nett_amt)
                        lm_mnet =  to_decimal(lm_mnet) + to_decimal(nett_amt)
                        tlm_mnet =  to_decimal(tlm_mnet) + to_decimal(nett_amt)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.kum = zwkum
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
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Grand T o t a l"
        cl_list.flag = "***"
        cl_list.dnet =  to_decimal(tdnet)
        cl_list.mnet =  to_decimal(tmnet)
        cl_list.mbudget =  to_decimal(t_mbudget)
        cl_list.ynet =  to_decimal(tynet)
        cl_list.lm_mnet =  to_decimal(tlm_mnet)
        cl_list.ly_mnet =  to_decimal(tly_mnet)
        cl_list.ly_ynet =  to_decimal(tly_ynet)

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)


            if cl_list.bezeich != "":
                output_list.flag = cl_list.flag
                str = to_string(cl_list.bezeich, "x(24)")

                if cl_list.flag.lower()  != ("*").lower() :

                    if price_decimal == 2:
                        str = str + to_string(cl_list.dnet, "->>>,>>9.99") + to_string(cl_list.mnet, "->>>>,>>9.99") + to_string(cl_list.mbudget, "->>>>,>>9.99") + to_string(cl_list.ynet, "->>,>>>,>>9.99") + to_string(cl_list.lm_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_ynet, "->>,>>>,>>9.99")

                    elif not long_digit or (long_digit and short_flag):
                        str = str + to_string(cl_list.dnet, "->>,>>>,>>9") + to_string(cl_list.mnet, "->>>,>>>,>>9") + to_string(cl_list.mbudget, "->>>,>>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>9") + to_string(cl_list.lm_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_ynet, "->,>>>,>>>,>>9")
                    else:
                        str = str + to_string(cl_list.dnet, "->>>>>>>>>9") + to_string(cl_list.mnet, "->>>>>>>>>>9") + to_string(cl_list.mbudget, "->>>>>>>>>>9") + to_string(cl_list.ynet, "->>>>>>>>>>>>9") + to_string(cl_list.lm_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_ynet, "->>>>>>>>>>>>9")

    if sorttype == 2:

        if not long_digit or not short_flag:
            fact1 = 1
        else:
            fact1 = 1000
        output_list_list.clear()
        cl_list_list.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
        taxnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})
        servnr = htparam.finteger
        jan1 = date_mdy(1, 1, get_year(from_date))
        ly_jan1 = date_mdy(1, 1, get_year(jan1) - timedelta(days=1))

        if get_month(to_date) >= 2:

            if get_day(from_date) == 1:
                lm_fdate = date_mdy(get_month(from_date) - timedelta(days=1, 1, get_year(from_date)))
            else:
                lm_fdate = from_date - timedelta(days=30)

            if get_day(to_date + 1) == 1:
                lm_tdate = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)
            else:
                lm_tdate = to_date - timedelta(days=30)
        else:
            lm_fdate = from_date - timedelta(days=31)
            lm_tdate = to_date - timedelta(days=31)

        if get_day(from_date) == 29 and get_month(from_date) == 2:
            ly_fdate = date_mdy(2, 28, get_year(from_date) - timedelta(days=1))
        else:
            ly_fdate = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - timedelta(days=1))

        if get_day(to_date) == 29 and get_month(to_date) == 2:
            ly_tdate = date_mdy(2, 28, get_year(to_date) - timedelta(days=1))
        else:
            ly_tdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))
        ekum_no = 0

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

                if ekum_no == 0:
                    ekum_no = artikel.endkum

                    ekum = get_cache (Ekum, {"eknr": [(eq, artikel.endkum)]})

                    if ekum:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.flag = "**"
                        cl_list.kum = artikel.endkum
                        cl_list.bezeich = ekum.bezeich

                if ekum_no != artikel.endkum:
                    cl_list.dnet =  to_decimal(dnet)
                    cl_list.mnet =  to_decimal(mnet)
                    cl_list.mbudget =  to_decimal(mbudget)
                    cl_list.ynet =  to_decimal(ynet)
                    cl_list.lm_mnet =  to_decimal(lm_mnet)
                    cl_list.ly_mnet =  to_decimal(ly_mnet)
                    cl_list.ly_ynet =  to_decimal(ly_ynet)
                    ekum_no = artikel.endkum

                    ekum = get_cache (Ekum, {"eknr": [(eq, artikel.endkum)]})

                    if ekum:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        dnet =  to_decimal("0")
                        mnet =  to_decimal("0")
                        ynet =  to_decimal("0")
                        lm_mnet =  to_decimal("0")
                        ly_mnet =  to_decimal("0")
                        ly_ynet =  to_decimal("0")
                        mbudget =  to_decimal("0")
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.flag = "**"
                        cl_list.kum = artikel.endkum
                        cl_list.bezeich = ekum.bezeich

                cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.kum == artikel.endkum), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.kum = artikel.endkum

                    ekum = get_cache (Ekum, {"eknr": [(eq, artikel.endkum)]})

                    if ekum:
                        cl_list.bezeich = ekum.bezeich
                for datum in date_range(jan1,to_date) :

                    umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, datum)]})

                    if umsatz:
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

                            for budget in db_session.query(Budget).filter(
                                     (Budget.departement == umsatz.departement) & (Budget.artnr == umsatz.artnr) & (Budget.datum == datum)).order_by(Budget._recid).all():
                                cl_list.mbudget =  to_decimal(cl_list.mbudget) + to_decimal(budget.betrag)
                                mbudget =  to_decimal(mbudget) + to_decimal(budget.betrag)
                                t_mbudget =  to_decimal(t_mbudget) + to_decimal(budget.betrag)


                        cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(nett_amt)
                        ynet =  to_decimal(ynet) + to_decimal(nett_amt)
                        tynet =  to_decimal(tynet) + to_decimal(nett_amt)

                    if get_day(datum) == 29 and get_month(datum) == 2:
                        pass
                    else:
                        ly_datum = date_mdy(get_month(datum) , get_day(datum) , get_year(datum) - timedelta(days=1))

                        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, ly_datum)]})

                        if umsatz:
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

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum >= lm_fdate) & (Umsatz.datum <= lm_tdate)).order_by(Umsatz._recid).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                    fact =  to_decimal(fact) * to_decimal(fact1)
                    nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                    nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                    nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                    nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)
                    cl_list.lm_mnet =  to_decimal(cl_list.lm_mnet) + to_decimal(nett_amt)
                    lm_mnet =  to_decimal(lm_mnet) + to_decimal(nett_amt)
                    tlm_mnet =  to_decimal(tlm_mnet) + to_decimal(nett_amt)
        cl_list.dnet =  to_decimal(dnet)
        cl_list.mnet =  to_decimal(mnet)
        cl_list.mbudget =  to_decimal(mbudget)
        cl_list.ynet =  to_decimal(ynet)
        cl_list.lm_mnet =  to_decimal(lm_mnet)
        cl_list.ly_mnet =  to_decimal(ly_mnet)
        cl_list.ly_ynet =  to_decimal(ly_ynet)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Grand T o t a l"
        cl_list.flag = "***"
        cl_list.dnet =  to_decimal(tdnet)
        cl_list.mnet =  to_decimal(tmnet)
        cl_list.mbudget =  to_decimal(t_mbudget)
        cl_list.ynet =  to_decimal(tynet)
        cl_list.lm_mnet =  to_decimal(tlm_mnet)
        cl_list.ly_mnet =  to_decimal(tly_mnet)
        cl_list.ly_ynet =  to_decimal(tly_ynet)

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)


            if cl_list.bezeich != "":
                output_list.flag = cl_list.flag
                str = to_string(cl_list.bezeich, "x(24)")

                if cl_list.flag.lower()  != ("*").lower() :

                    if price_decimal == 2:
                        str = str + to_string(cl_list.dnet, "->>>,>>9.99") + to_string(cl_list.mnet, "->>>>,>>9.99") + to_string(cl_list.mbudget, "->>>>,>>9.99") + to_string(cl_list.ynet, "->>,>>>,>>9.99") + to_string(cl_list.lm_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_ynet, "->>,>>>,>>9.99")

                    elif not long_digit or (long_digit and short_flag):
                        str = str + to_string(cl_list.dnet, "->>,>>>,>>9") + to_string(cl_list.mnet, "->>>,>>>,>>9") + to_string(cl_list.mbudget, "->>>,>>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>9") + to_string(cl_list.lm_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_ynet, "->,>>>,>>>,>>9")
                    else:
                        str = str + to_string(cl_list.dnet, "->>>>>>>>>9") + to_string(cl_list.mnet, "->>>>>>>>>>9") + to_string(cl_list.mbudget, "->>>>>>>>>>9") + to_string(cl_list.ynet, "->>>>>>>>>>>>9") + to_string(cl_list.lm_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_ynet, "->>>>>>>>>>>>9")

    return generate_output()