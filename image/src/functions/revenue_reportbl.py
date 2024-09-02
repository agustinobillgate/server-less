from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Hoteldpt, Artikel, zwkum, Umsatz, Budget, Ekum

def revenue_reportbl(sorttype:int, long_digit:bool, short_flag:bool, from_date:date, to_date:date):
    output_list_list = []
    fact1:int = 0
    price_decimal:int = 0
    curr_dept:str = ""
    curr_art:int = 0
    bezeich:str = ""
    datum:date = None
    ly_datum:date = None
    jan1:date = None
    ly_jan1:date = None
    lm_fdate:date = None
    lm_tdate:date = None
    ly_fdate:date = None
    ly_tdate:date = None
    fact:decimal = 0
    ekum_no:int = 0
    dnet:decimal = 0
    mnet:decimal = 0
    ynet:decimal = 0
    lm_mnet:decimal = 0
    ly_mnet:decimal = 0
    ly_ynet:decimal = 0
    tdnet:decimal = 0
    tmnet:decimal = 0
    tynet:decimal = 0
    tlm_mnet:decimal = 0
    tly_mnet:decimal = 0
    tly_ynet:decimal = 0
    taxnr:int = 0
    servnr:int = 0
    do_it:bool = False
    vat:decimal = 0
    serv:decimal = 0
    nett_serv:decimal = 0
    nett_tax:decimal = 0
    nett_amt:decimal = 0
    dept:int = -1
    zwkum:int = 0
    serv_vat:bool = False
    mbudget:decimal = 0
    t_mbudget:decimal = 0
    lm_mtd_datum:date = None
    htparam = hoteldpt = artikel = zwkum = umsatz = budget = ekum = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":str, "str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "artnr":int, "kum":int, "dept":int, "bezeich":str, "dnet":decimal, "mnet":decimal, "mbudget":decimal, "ynet":decimal, "lm_mnet":decimal, "ly_mnet":decimal, "ly_ynet":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, fact1, price_decimal, curr_dept, curr_art, bezeich, datum, ly_datum, jan1, ly_jan1, lm_fdate, lm_tdate, ly_fdate, ly_tdate, fact, ekum_no, dnet, mnet, ynet, lm_mnet, ly_mnet, ly_ynet, tdnet, tmnet, tynet, tlm_mnet, tly_mnet, tly_ynet, taxnr, servnr, do_it, vat, serv, nett_serv, nett_tax, nett_amt, dept, zwkum, serv_vat, mbudget, t_mbudget, lm_mtd_datum, htparam, hoteldpt, artikel, zwkum, umsatz, budget, ekum


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list
        return {"output-list": output_list_list}

    def cal_tax_service():

        nonlocal output_list_list, fact1, price_decimal, curr_dept, curr_art, bezeich, datum, ly_datum, jan1, ly_jan1, lm_fdate, lm_tdate, ly_fdate, ly_tdate, fact, ekum_no, dnet, mnet, ynet, lm_mnet, ly_mnet, ly_ynet, tdnet, tmnet, tynet, tlm_mnet, tly_mnet, tly_ynet, taxnr, servnr, do_it, vat, serv, nett_serv, nett_tax, nett_amt, dept, zwkum, serv_vat, mbudget, t_mbudget, lm_mtd_datum, htparam, hoteldpt, artikel, zwkum, umsatz, budget, ekum


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        fact = 0
        vat = 0
        serv = 0

        def generate_inner_output():
            return fact, vat, serv
        serv = 0
        vat = 0

        if artikel.service_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.service_code)).first()

            if htparam and htparam.fdecimal != 0:
                serv = htparam.fdecimal / 100

        if artikel.mwst_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat = htparam.fdecimal / 100

                if serv_vat:
                    vat = vat + vat * serv
                vat = round (vat, 2)
        fact = 1.00 + serv + vat
        fact = fact * fact1


        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    serv_vat = htparam.flogical

    if sorttype == 1:

        if not long_digit or not short_flag:
            fact1 = 1
        else:
            fact1 = 1000
        output_list_list.clear()
        cl_list_list.clear()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 132)).first()
        taxnr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 133)).first()
        servnr = finteger
        jan1 = date_mdy(1, 1, get_year(from_date))
        ly_jan1 = date_mdy(1, 1, get_year(jan1) - 1)

        if get_month(to_date) >= 2:

            if get_day(from_date) == 1:
                lm_fdate = date_mdy(get_month(from_date) - 1, 1, get_year(from_date))
            else:
                lm_fdate = from_date - 30

            if get_day(to_date + 1) == 1:
                lm_tdate = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
            else:
                lm_tdate = to_date - 30
        else:
            lm_fdate = from_date - 31
            lm_tdate = to_date - 31

        if get_day(from_date) == 29 and get_month(from_date) == 2:
            ly_fdate = date_mdy(2, 28, get_year(from_date) - 1)
        else:
            ly_fdate = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - 1)

        if get_day(to_date) == 29 and get_month(to_date) == 2:
            ly_tdate = date_mdy(2, 28, get_year(to_date) - 1)
        else:
            ly_tdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - 1)

        for hoteldpt in db_session.query(Hoteldpt).all():
            curr_dept = hoteldpt.depart

            if dept == -1:
                dept = hoteldpt.num

            if dept != hoteldpt.num:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.bezeich = "T o t a l"
                cl_list.flag = "**"
                cl_list.dnet = dnet
                cl_list.mnet = mnet
                cl_list.mbudget = mbudget
                cl_list.ynet = ynet
                cl_list.lm_mnet = lm_mnet
                cl_list.ly_mnet = ly_mnet
                cl_list.ly_ynet = ly_ynet


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                dnet = 0
                mnet = 0
                ynet = 0
                lm_mnet = 0
                ly_mnet = 0
                ly_ynet = 0
                mbudget = 0
                dept = hoteldpt.num


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.flag = "*"
            cl_list.bezeich = hoteldpt.depart
            zwkum = 0

            for artikel in db_session.query(Artikel).filter(
                    ((Artikel.artart == 0) |  (Artikel.artart == 8)) &  (Artikel.departement == hoteldpt.num)).all():
                bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
                do_it = True

                if (artikel.artnr == taxnr or artikel.artnr == servnr) and artikel.departement == 0:
                    do_it = False

                if do_it:

                    if zwkum != artikel.zwkum:
                        zwkum = artikel.zwkum

                        zwkum = db_session.query(zwkum).filter(
                                (zwkum.zknr == artikel.zwkum) &  (zwkum.departement == artikel.departement)).first()

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.kum == artikel.zwkum and cl_list.dept == artikel.departement), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.kum = artikel.zwkum
                        cl_list.artnr = artikel.artnr
                        cl_list.dept = artikel.departement
                        cl_list.bezeich = zwkum.bezeich
                    for datum in range(jan1,to_date + 1) :

                        umsatz = db_session.query(Umsatz).filter(
                                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == datum)).first()

                        if umsatz:
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact = 1.00 + serv + vat
                            fact = fact * fact1
                            nett_amt = umsatz.betrag / fact
                            nett_serv = round(nett_amt * serv, price_decimal)
                            nett_tax = round(nett_amt * vat, price_decimal)
                            nett_amt = umsatz.betrag - nett_serv - nett_tax

                            if umsatz.datum == to_date:
                                cl_list.dnet = cl_list.dnet + nett_amt
                                dnet = dnet + nett_amt
                                tdnet = tdnet + nett_amt

                            if datum >= from_date:
                                cl_list.mnet = cl_list.mnet + nett_amt
                                mnet = mnet + nett_amt
                                tmnet = tmnet + nett_amt

                                for budget in db_session.query(Budget).filter(
                                        (Budget.departement == umsatz.departement) &  (Budget.artnr == umsatz.artnr) &  (Budget.datum == datum)).all():
                                    cl_list.mbudget = cl_list.mbudget + budget.betrag
                                    mbudget = mbudget + budget.betrag
                                    t_mbudget = t_mbudget + budget.betrag


                            cl_list.ynet = cl_list.ynet + nett_amt
                            ynet = ynet + nett_amt
                            tynet = tynet + nett_amt

                        if get_day(datum) == 29 and get_month(datum) == 2:
                            pass
                        else:
                            ly_datum = date_mdy(get_month(datum) , get_day(datum) , get_year(datum) - 1)

                            umsatz = db_session.query(Umsatz).filter(
                                    (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == ly_datum)).first()

                            if umsatz:
                                serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                                fact = 1.00 + serv + vat
                                fact = fact * fact1
                                nett_amt = umsatz.betrag / fact
                                nett_serv = round(nett_amt * serv, price_decimal)
                                nett_tax = round(nett_amt * vat, price_decimal)
                                nett_amt = umsatz.betrag - nett_serv - nett_tax

                                if ly_datum >= ly_fdate:
                                    cl_list.ly_mnet = cl_list.ly_mnet + nett_amt
                                    ly_mnet = ly_mnet + nett_amt
                                    tly_mnet = tly_mnet + nett_amt
                                cl_list.ly_ynet = cl_list.ly_ynet + nett_amt
                                ly_ynet = ly_ynet + nett_amt
                                tly_ynet = tly_ynet + nett_amt

                    for umsatz in db_session.query(Umsatz).filter(
                            (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum >= lm_fdate) &  (Umsatz.datum <= lm_tdate)).all():
                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                        fact = 1.00 + serv + vat
                        fact = fact * fact1
                        nett_amt = umsatz.betrag / fact
                        nett_serv = round(nett_amt * serv, price_decimal)
                        nett_tax = round(nett_amt * vat, price_decimal)
                        nett_amt = umsatz.betrag - nett_serv - nett_tax
                        cl_list.lm_mnet = cl_list.lm_mnet + nett_amt
                        lm_mnet = lm_mnet + nett_amt
                        tlm_mnet = tlm_mnet + nett_amt
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.kum = zwkum
        cl_list.bezeich = "T o t a l"
        cl_list.flag = "**"
        cl_list.dnet = dnet
        cl_list.mnet = mnet
        cl_list.mbudget = mbudget
        cl_list.ynet = ynet
        cl_list.lm_mnet = lm_mnet
        cl_list.ly_mnet = ly_mnet
        cl_list.ly_ynet = ly_ynet


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Grand T o t a l"
        cl_list.flag = "***"
        cl_list.dnet = tdnet
        cl_list.mnet = tmnet
        cl_list.mbudget = t_mbudget
        cl_list.ynet = tynet
        cl_list.lm_mnet = tlm_mnet
        cl_list.ly_mnet = tly_mnet
        cl_list.ly_ynet = tly_ynet

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)


            if cl_list.bezeich != "":
                output_list.flag = cl_list.flag
                STR = to_string(cl_list.bezeich, "x(24)")

                if cl_list.flag.lower()  != "*":

                    if price_decimal == 2:
                        STR = STR + to_string(cl_list.dnet, "->>>,>>9.99") + to_string(cl_list.mnet, "->>>>,>>9.99") + to_string(cl_list.mbudget, "->>>>,>>9.99") + to_string(cl_list.ynet, "->>,>>>,>>9.99") + to_string(cl_list.lm_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_ynet, "->>,>>>,>>9.99")

                    elif not long_digit or (long_digit and short_flag):
                        STR = STR + to_string(cl_list.dnet, "->>,>>>,>>9") + to_string(cl_list.mnet, "->>>,>>>,>>9") + to_string(cl_list.mbudget, "->>>,>>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>9") + to_string(cl_list.lm_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_ynet, "->,>>>,>>>,>>9")
                    else:
                        STR = STR + to_string(cl_list.dnet, "->>>>>>>>>9") + to_string(cl_list.mnet, "->>>>>>>>>>9") + to_string(cl_list.mbudget, "->>>>>>>>>>9") + to_string(cl_list.ynet, "->>>>>>>>>>>>9") + to_string(cl_list.lm_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_ynet, "->>>>>>>>>>>>9")

    if sorttype == 2:

        if not long_digit or not short_flag:
            fact1 = 1
        else:
            fact1 = 1000
        output_list_list.clear()
        cl_list_list.clear()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 132)).first()
        taxnr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 133)).first()
        servnr = finteger
        jan1 = date_mdy(1, 1, get_year(from_date))
        ly_jan1 = date_mdy(1, 1, get_year(jan1) - 1)

        if get_month(to_date) >= 2:

            if get_day(from_date) == 1:
                lm_fdate = date_mdy(get_month(from_date) - 1, 1, get_year(from_date))
            else:
                lm_fdate = from_date - 30

            if get_day(to_date + 1) == 1:
                lm_tdate = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
            else:
                lm_tdate = to_date - 30
        else:
            lm_fdate = from_date - 31
            lm_tdate = to_date - 31

        if get_day(from_date) == 29 and get_month(from_date) == 2:
            ly_fdate = date_mdy(2, 28, get_year(from_date) - 1)
        else:
            ly_fdate = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - 1)

        if get_day(to_date) == 29 and get_month(to_date) == 2:
            ly_tdate = date_mdy(2, 28, get_year(to_date) - 1)
        else:
            ly_tdate = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - 1)
        ekum_no = 0

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 0) |  (Artikel.artart == 8))).all():

            hoteldpt = db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num == artikel.departement)).first()

            if hoteldpt:
                curr_dept = hoteldpt.depart
                bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
            do_it = True

            if (artikel.artnr == taxnr or artikel.artnr == servnr) and artikel.departement == 0:
                do_it = False

            if do_it:

                if ekum_no == 0:
                    ekum_no = artikel.endkum

                    ekum = db_session.query(Ekum).filter(
                            (Ekum.eknr == artikel.endkum)).first()

                    if ekum:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.flag = "**"
                        cl_list.kum = artikel.endkum
                        cl_list.bezeich = ekum.bezeich

                if ekum_no != artikel.endkum:
                    cl_list.dnet = dnet
                    cl_list.mnet = mnet
                    cl_list.mbudget = mbudget
                    cl_list.ynet = ynet
                    cl_list.lm_mnet = lm_mnet
                    cl_list.ly_mnet = ly_mnet
                    cl_list.ly_ynet = ly_ynet
                    ekum_no = artikel.endkum

                    ekum = db_session.query(Ekum).filter(
                            (Ekum.eknr == artikel.endkum)).first()

                    if ekum:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        dnet = 0
                        mnet = 0
                        ynet = 0
                        lm_mnet = 0
                        ly_mnet = 0
                        ly_ynet = 0
                        mbudget = 0
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.flag = "**"
                        cl_list.kum = artikel.endkum
                        cl_list.bezeich = ekum.bezeich

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.kum == artikel.endkum), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.kum = artikel.endkum

                    ekum = db_session.query(Ekum).filter(
                            (Ekum.eknr == artikel.endkum)).first()

                    if ekum:
                        cl_list.bezeich = ekum.bezeich
                for datum in range(jan1,to_date + 1) :

                    umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == datum)).first()

                    if umsatz:
                        serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                        fact = 1.00 + serv + vat
                        fact = fact * fact1
                        nett_amt = umsatz.betrag / fact
                        nett_serv = round(nett_amt * serv, price_decimal)
                        nett_tax = round(nett_amt * vat, price_decimal)
                        nett_amt = umsatz.betrag - nett_serv - nett_tax

                        if umsatz.datum == to_date:
                            cl_list.dnet = cl_list.dnet + nett_amt
                            dnet = dnet + nett_amt
                            tdnet = tdnet + nett_amt

                        if datum >= from_date:
                            cl_list.mnet = cl_list.mnet + nett_amt
                            mnet = mnet + nett_amt
                            tmnet = tmnet + nett_amt

                            for budget in db_session.query(Budget).filter(
                                    (Budget.departement == umsatz.departement) &  (Budget.artnr == umsatz.artnr) &  (Budget.datum == datum)).all():
                                cl_list.mbudget = cl_list.mbudget + budget.betrag
                                mbudget = mbudget + budget.betrag
                                t_mbudget = t_mbudget + budget.betrag


                        cl_list.ynet = cl_list.ynet + nett_amt
                        ynet = ynet + nett_amt
                        tynet = tynet + nett_amt

                    if get_day(datum) == 29 and get_month(datum) == 2:
                        pass
                    else:
                        ly_datum = date_mdy(get_month(datum) , get_day(datum) , get_year(datum) - 1)

                        umsatz = db_session.query(Umsatz).filter(
                                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == ly_datum)).first()

                        if umsatz:
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact = 1.00 + serv + vat
                            fact = fact * fact1
                            nett_amt = umsatz.betrag / fact
                            nett_serv = round(nett_amt * serv, price_decimal)
                            nett_tax = round(nett_amt * vat, price_decimal)
                            nett_amt = umsatz.betrag - nett_serv - nett_tax

                            if ly_datum >= ly_fdate:
                                cl_list.ly_mnet = cl_list.ly_mnet + nett_amt
                                ly_mnet = ly_mnet + nett_amt
                                tly_mnet = tly_mnet + nett_amt
                            cl_list.ly_ynet = cl_list.ly_ynet + nett_amt
                            ly_ynet = ly_ynet + nett_amt
                            tly_ynet = tly_ynet + nett_amt

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum >= lm_fdate) &  (Umsatz.datum <= lm_tdate)).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact = 1.00 + serv + vat
                    fact = fact * fact1
                    nett_amt = umsatz.betrag / fact
                    nett_serv = round(nett_amt * serv, price_decimal)
                    nett_tax = round(nett_amt * vat, price_decimal)
                    nett_amt = umsatz.betrag - nett_serv - nett_tax
                    cl_list.lm_mnet = cl_list.lm_mnet + nett_amt
                    lm_mnet = lm_mnet + nett_amt
                    tlm_mnet = tlm_mnet + nett_amt
        cl_list.dnet = dnet
        cl_list.mnet = mnet
        cl_list.mbudget = mbudget
        cl_list.ynet = ynet
        cl_list.lm_mnet = lm_mnet
        cl_list.ly_mnet = ly_mnet
        cl_list.ly_ynet = ly_ynet
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Grand T o t a l"
        cl_list.flag = "***"
        cl_list.dnet = tdnet
        cl_list.mnet = tmnet
        cl_list.mbudget = t_mbudget
        cl_list.ynet = tynet
        cl_list.lm_mnet = tlm_mnet
        cl_list.ly_mnet = tly_mnet
        cl_list.ly_ynet = tly_ynet

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)


            if cl_list.bezeich != "":
                output_list.flag = cl_list.flag
                STR = to_string(cl_list.bezeich, "x(24)")

                if cl_list.flag.lower()  != "*":

                    if price_decimal == 2:
                        STR = STR + to_string(cl_list.dnet, "->>>,>>9.99") + to_string(cl_list.mnet, "->>>>,>>9.99") + to_string(cl_list.mbudget, "->>>>,>>9.99") + to_string(cl_list.ynet, "->>,>>>,>>9.99") + to_string(cl_list.lm_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_mnet, "->>>>,>>9.99") + to_string(cl_list.ly_ynet, "->>,>>>,>>9.99")

                    elif not long_digit or (long_digit and short_flag):
                        STR = STR + to_string(cl_list.dnet, "->>,>>>,>>9") + to_string(cl_list.mnet, "->>>,>>>,>>9") + to_string(cl_list.mbudget, "->>>,>>>,>>9") + to_string(cl_list.ynet, "->,>>>,>>>,>>9") + to_string(cl_list.lm_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_mnet, "->>>,>>>,>>9") + to_string(cl_list.ly_ynet, "->,>>>,>>>,>>9")
                    else:
                        STR = STR + to_string(cl_list.dnet, "->>>>>>>>>9") + to_string(cl_list.mnet, "->>>>>>>>>>9") + to_string(cl_list.mbudget, "->>>>>>>>>>9") + to_string(cl_list.ynet, "->>>>>>>>>>>>9") + to_string(cl_list.lm_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_mnet, "->>>>>>>>>>9") + to_string(cl_list.ly_ynet, "->>>>>>>>>>>>9")

    return generate_output()