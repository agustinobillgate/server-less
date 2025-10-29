#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 06-10-2025
# Tiket ID : 133E12, First compile
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.calc_servvat import calc_servvat
from models import Htparam, Billjournal, Artikel, Hoteldpt, H_bill, H_bill_line, H_artikel, Queasy

fbartikel_data, Fbartikel = create_model(
    "Fbartikel", {
        "artnr":int, 
        "artdesc":string, 
        "outletcode":int, 
        "outletname":string, 
        "maingrp":int, 
        "subgrp":int, 
        "rev_excltax":Decimal, 
        "tax_total":Decimal, 
        "totalrev__incltax":Decimal, 
        "covers":int, 
        "billno":int, 
        "shift":int, 
        "billdate":date, 
        "timestamp":string, 
        "stay_flag":int, 
        "ascott_code":string, 
        "tot_bill":int
        }
    )

def ascott_fbartikelbl(fdate:date, tdate:date, propid:string, fbartikel_data:[Fbartikel]):

    prepare_cache ([Htparam, Billjournal, Artikel, Hoteldpt, H_bill, H_bill_line, H_artikel, Queasy])

    flag_artnr:bool = False
    billflag:bool = False
    billno:int = 0
    totalfb:Decimal = to_decimal("0.0")
    totgrossfb:Decimal = to_decimal("0.0")
    totalother:Decimal = to_decimal("0.0")
    totgrossother:Decimal = to_decimal("0.0")
    flodging:Decimal = to_decimal("0.0")
    lodging:Decimal = to_decimal("0.0")
    breakfast:Decimal = to_decimal("0.0")
    lunch:Decimal = to_decimal("0.0")
    dinner:Decimal = to_decimal("0.0")
    others:Decimal = to_decimal("0.0")
    rmrate:Decimal = to_decimal("0.0")
    net_vat:Decimal = to_decimal("0.0")
    net_service:Decimal = to_decimal("0.0")
    loop_i:int = 0
    betragvalue:Decimal = to_decimal("0.0")
    grossbetrag:Decimal = to_decimal("0.0")
    newbetrag:Decimal = to_decimal("0.0")
    deptdesc:string = ""
    subgroup:int = 0
    maingroup:int = 0
    coversvalue:int = 0
    service:int = 0
    tstamp:string = ""
    stay_flag:int = 0
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    serv_betrag:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    vat_betrag:Decimal = to_decimal("0.0")
    fact_scvat:Decimal = to_decimal("0.0")
    vat_proz:Decimal = 10
    bqt_dept:int = 0
    htparam = billjournal = artikel = hoteldpt = h_bill = h_bill_line = h_artikel = queasy = None

    fbartikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_artnr, billflag, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, loop_i, betragvalue, grossbetrag, newbetrag, deptdesc, subgroup, maingroup, coversvalue, service, tstamp, stay_flag, serv, vat, netto, serv_betrag, vat2, vat_betrag, fact_scvat, vat_proz, bqt_dept, htparam, billjournal, artikel, hoteldpt, h_bill, h_bill_line, h_artikel, queasy
        nonlocal fdate, tdate, propid
        nonlocal fbartikel

        return {"fbartikel": fbartikel_data}

    def fo_bill():
        nonlocal flag_artnr, billflag, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, loop_i, betragvalue, grossbetrag, newbetrag, deptdesc, subgroup, maingroup, coversvalue, service, tstamp, stay_flag, serv, vat, netto, serv_betrag, vat2, vat_betrag, fact_scvat, vat_proz, bqt_dept, htparam, billjournal, artikel, hoteldpt, h_bill, h_bill_line, h_artikel, queasy
        nonlocal fdate, tdate, propid
        nonlocal fbartikel

        doit:bool = False
        curr_shift:int = 0

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.departement > 0) & (Billjournal.bill_datum >= fdate) & (Billjournal.bill_datum <= tdate) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.rechnr, Billjournal.departement, Billjournal.artnr).all():
            doit = False

            artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

            if artikel and artikel.artart == 0 and (artikel.umsatzart == 4 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
                doit = True

            if doit:
                subgroup = artikel.zwkum
                maingroup = artikel.endkum
                tstamp = to_string(get_year(billjournal.bill_datum) , "9999") + "-" + to_string(get_month(billjournal.bill_datum) , "99") + "-" +\
                        to_string(get_day(billjournal.bill_datum) , "99") + " " + to_string(billjournal.zeit, "HH:MM:SS")


                deptdesc = "NULL"

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})

                if hoteldpt:
                    deptdesc = hoteldpt.depart

                if billjournal.zinr != "":
                    stay_flag = 0


                else:
                    stay_flag = 1


                serv =  to_decimal("0")
                vat =  to_decimal("0")
                vat2 =  to_decimal("0")
                netto =  to_decimal("0")
                serv_betrag =  to_decimal("0")
                vat_betrag =  to_decimal("0")


                serv, vat, vat2, fact_scvat = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, billjournal.bill_datum))

                if vat == 1:
                    netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                else:

                    if serv == 1:
                        serv_betrag =  to_decimal(netto)

                    elif vat > 0:
                        netto =  to_decimal(billjournal.betrag) / to_decimal(fact_scvat)
                        serv_betrag =  to_decimal(netto) * to_decimal(serv)
                        vat_betrag =  to_decimal(netto) * to_decimal(vat)


                curr_shift = 0

                if billjournal.zeit >= 10860 and billjournal.zeit <= 43140:
                    curr_shift = 1

                elif billjournal.zeit >= 43200 and billjournal.zeit <= 64740:
                    curr_shift = 2

                elif billjournal.zeit >= 64800 and billjournal.zeit <= 79200:
                    curr_shift = 3

                elif (billjournal.zeit >= 79260 and billjournal.zeit <= 86340) or (billjournal.zeit >= 0 and billjournal.zeit <= 10800):
                    curr_shift = 4


                create_bill_list(artikel.artnr, artikel.bezeich, billjournal.bill_datum, artikel.departement, deptdesc, maingroup, subgroup, netto, (vat_betrag + serv_betrag), billjournal.betrag, 0, billjournal.rechnr, curr_shift, tstamp, stay_flag)


    def pos_nonstay_bill():
        nonlocal flag_artnr, billflag, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, loop_i, betragvalue, grossbetrag, newbetrag, deptdesc, subgroup, maingroup, coversvalue, service, tstamp, stay_flag, serv, vat, netto, serv_betrag, vat2, vat_betrag, fact_scvat, vat_proz, bqt_dept, htparam, billjournal, artikel, hoteldpt, h_bill, h_bill_line, h_artikel, queasy
        nonlocal fdate, tdate, propid
        nonlocal fbartikel

        curr_shift:int = 0

        for h_bill in db_session.query(H_bill).filter(
                 (H_bill.rechnr > 0) & (H_bill.flag == 1)).order_by(H_bill._recid).all():
            totalfb =  to_decimal("0")
            totgrossfb =  to_decimal("0")
            totalother =  to_decimal("0")
            totgrossother =  to_decimal("0")
            flag_artnr = False

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                if h_artikel:

                    if h_artikel.artart == 11 or h_artikel.artart == 12:
                        flag_artnr = True

            if flag_artnr == False:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum >= fdate) & (H_bill_line.bill_datum <= tdate) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
                    billflag = False
                    for loop_i in range(1,length(h_bill_line.bezeich)  + 1) :

                        if substring(h_bill_line.bezeich, loop_i - 1, 1) == ("*").lower() :
                            loop_i = 999
                            billflag = True

                    if not billflag:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"artart": [(eq, 0)],"departement": [(eq, h_bill_line.departement)]})

                        if h_artikel:
                            deptdesc = "NULL"

                            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_artikel.departement)]})

                            if hoteldpt:
                                deptdesc = hoteldpt.depart
                            subgroup = h_artikel.zwkum
                            maingroup = h_artikel.endkum
                            coversvalue = 0
                            coversvalue = h_bill.belegung
                            tstamp = to_string(get_year(h_bill_line.bill_datum) , "9999") + "-" + to_string(get_month(h_bill_line.bill_datum) , "99") + "-" + to_string(get_day(h_bill_line.bill_datum) , "99") + " " + to_string(h_bill_line.zeit, "HH:MM:SS")

                            if h_bill.resnr != 0:
                                stay_flag = 0


                            else:
                                stay_flag = 1


                            serv =  to_decimal("0")
                            vat =  to_decimal("0")
                            vat2 =  to_decimal("0")
                            netto =  to_decimal("0")
                            serv_betrag =  to_decimal("0")
                            vat_betrag =  to_decimal("0")

                            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
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
                                    vat_betrag =  to_decimal(netto) * to_decimal(vat)

                            if h_bill_line.betriebsnr == 0:

                                if h_bill_line.zeit >= 10860 and h_bill_line.zeit <= 43140:
                                    curr_shift = 1

                                elif h_bill_line.zeit >= 43200 and h_bill_line.zeit <= 64740:
                                    curr_shift = 2

                                elif h_bill_line.zeit >= 64800 and h_bill_line.zeit <= 79200:
                                    curr_shift = 3

                                elif (h_bill_line.zeit >= 79260 and h_bill_line.zeit <= 86340) or (h_bill_line.zeit >= 0 and h_bill_line.zeit <= 10800):
                                    curr_shift = 4


                            else:
                                curr_shift = h_bill_line.betriebsnr
                            create_bill_list(h_artikel.artnr, h_artikel.bezeich, h_bill_line.bill_datum, h_artikel.departement, deptdesc, maingroup, subgroup, netto, (vat_betrag + serv_betrag), h_bill_line.betrag, coversvalue, h_bill.rechnr, curr_shift, tstamp, stay_flag)


    def create_bill_list(artnum:int, artdesc:string, bill_date:date, outlet_code:int, outlet_name:string, main_grp:int, sub_grp:int, revenueexcltax:Decimal, totaltaxes:Decimal, revenueincltax:Decimal, covers:int, bill_rechnr:int, shift:int, tstamp:string, stay_flag:int):
        nonlocal flag_artnr, billflag, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, loop_i, betragvalue, grossbetrag, newbetrag, deptdesc, subgroup, maingroup, coversvalue, service, serv, vat, netto, serv_betrag, vat2, vat_betrag, fact_scvat, vat_proz, bqt_dept, htparam, billjournal, artikel, hoteldpt, h_bill, h_bill_line, h_artikel, queasy
        nonlocal fdate, tdate, propid
        nonlocal fbartikel

        mgrp:int = 0
        sgrp:int = 0
        ocode:int = 0
        oname:string = ""
        artdesc = replace_str(artdesc, chr_unicode(34) , chr_unicode(39))

        queasy = get_cache (Queasy, {"key": [(eq, 369)],"char1": [(eq, "maingroup-fb")],"number2": [(eq, main_grp)]})

        if queasy:
            mgrp = queasy.number3


        else:
            mgrp = main_grp

        queasy = get_cache (Queasy, {"key": [(eq, 369)],"char1": [(eq, "subgroup-fb")],"number2": [(eq, sub_grp)]})

        if queasy:
            sgrp = queasy.number3


        else:
            sgrp = sub_grp

        queasy = get_cache (Queasy, {"key": [(eq, 369)],"char1": [(eq, "outlet-fb")],"number2": [(eq, outlet_code)]})

        if queasy:
            ocode = queasy.number3
            oname = queasy.char3


        else:
            ocode = outlet_code
            oname = outlet_name

        fbartikel = query(fbartikel_data, filters=(lambda fbartikel: fbartikel.billdate == bill_date and fbartikel.outletname.lower()  == (outlet_name).lower()  and fbartikel.maingrp == main_grp and fbartikel.subgrp == sub_grp), first=True)

        if not fbartikel:
            fbartikel = Fbartikel()
            fbartikel_data.append(fbartikel)

            fbartikel.artnr = artnum
            fbartikel.artdesc = artdesc
            fbartikel.outletcode = ocode
            fbartikel.outletname = oname
            fbartikel.maingrp = mgrp
            fbartikel.subgrp = sgrp
            fbartikel.billno = bill_rechnr
            fbartikel.shift = shift
            fbartikel.billdate = bill_date
            fbartikel.timestamp = tstamp
            fbartikel.stay_flag = stay_flag
            fbartikel.ascott_code = propid

        if bill_rechnr != 0:
            fbartikel.tot_bill = fbartikel.tot_bill + 1


        fbartikel.covers = fbartikel.covers + covers
        fbartikel.rev_excltax =  to_decimal(fbartikel.rev_excltax) + to_decimal(revenueexcltax)
        fbartikel.tax_total =  to_decimal(fbartikel.tax_total) + to_decimal(totaltaxes)
        fbartikel.totalrev__incltax =  to_decimal(fbartikel.totalrev__incltax) + to_decimal(revenueincltax)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    if htparam:
        bqt_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1)]})

    if htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)
    pos_nonstay_bill()
    fo_bill()

    return generate_output()