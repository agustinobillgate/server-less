#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, H_bill_line, Queasy, Hoteldpt

def fb_detailreportbl(from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([H_artikel, H_bill_line, Queasy, Hoteldpt])

    output_list2_data = []
    curr_dept:int = 0
    curr_date:date = None
    bfastqty:int = 0
    billtime:string = ""
    startshift1:int = 0
    endshift1:int = 0
    startshift2:int = 0
    endshift2:int = 0
    startshift3:int = 0
    endshift3:int = 0
    startshift4:int = 0
    endshift4:int = 0
    depbfastqty:int = 0
    depbfastamount:Decimal = to_decimal("0.0")
    deplunchqty:int = 0
    deplunchamount:Decimal = to_decimal("0.0")
    depdinnerqty:int = 0
    depdinneramount:Decimal = to_decimal("0.0")
    depsupperqty:int = 0
    depsupperamount:Decimal = to_decimal("0.0")
    deptotqty:int = 0
    deptotamount:Decimal = to_decimal("0.0")
    totbfastqty:int = 0
    totbfastamount:Decimal = to_decimal("0.0")
    totlunchqty:int = 0
    totlunchamount:Decimal = to_decimal("0.0")
    totdinnerqty:int = 0
    totdinneramount:Decimal = to_decimal("0.0")
    totsupperqty:int = 0
    totsupperamount:Decimal = to_decimal("0.0")
    sumtotqty:int = 0
    sumtotamount:Decimal = to_decimal("0.0")
    sumtotbfastqty:int = 0
    sumtotbfastamount:Decimal = to_decimal("0.0")
    sumtotlunchqty:int = 0
    sumtotlunchamount:Decimal = to_decimal("0.0")
    sumtotdinnerqty:int = 0
    sumtotdinneramount:Decimal = to_decimal("0.0")
    sumtotsupperqty:int = 0
    sumtotsupperamount:Decimal = to_decimal("0.0")
    totsumtotqty:int = 0
    totsumtotamount:Decimal = to_decimal("0.0")
    h_artikel = h_bill_line = queasy = hoteldpt = None

    output_list = output_list2 = h_art = b_hbline = None

    output_list_data, Output_list = create_model("Output_list", {"departement":int, "datum":date, "zeit":string, "artnr":int, "artbezeich":string, "bfastqty":int, "bfastamount":Decimal, "lunchqty":int, "lunchamount":Decimal, "dinnerqty":int, "dinneramount":Decimal, "supperqty":int, "supperamount":Decimal, "totqty":int, "totamount":Decimal})
    output_list2_data, Output_list2 = create_model("Output_list2", {"departement":string, "datum":string, "zeit":string, "artnr":string, "artbezeich":string, "bfastqty":string, "bfastamount":string, "lunchqty":string, "lunchamount":string, "dinnerqty":string, "dinneramount":string, "supperqty":string, "supperamount":string, "totqty":string, "totamount":string})

    H_art = create_buffer("H_art",H_artikel)
    B_hbline = create_buffer("B_hbline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list2_data, curr_dept, curr_date, bfastqty, billtime, startshift1, endshift1, startshift2, endshift2, startshift3, endshift3, startshift4, endshift4, depbfastqty, depbfastamount, deplunchqty, deplunchamount, depdinnerqty, depdinneramount, depsupperqty, depsupperamount, deptotqty, deptotamount, totbfastqty, totbfastamount, totlunchqty, totlunchamount, totdinnerqty, totdinneramount, totsupperqty, totsupperamount, sumtotqty, sumtotamount, sumtotbfastqty, sumtotbfastamount, sumtotlunchqty, sumtotlunchamount, sumtotdinnerqty, sumtotdinneramount, sumtotsupperqty, sumtotsupperamount, totsumtotqty, totsumtotamount, h_artikel, h_bill_line, queasy, hoteldpt
        nonlocal from_dept, to_dept, from_date, to_date
        nonlocal h_art, b_hbline


        nonlocal output_list, output_list2, h_art, b_hbline
        nonlocal output_list_data, output_list2_data

        return {"output-list2": output_list2_data}

    output_list_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 != 0)).order_by(Queasy.number1).all():

        if queasy.number3 == 1:
            startshift1 = queasy.number1
            endshift1 = queasy.number2

        if queasy.number3 == 2:
            startshift2 = queasy.number1
            endshift2 = queasy.number2

        if queasy.number3 == 3:
            startshift3 = queasy.number1
            endshift3 = queasy.number2

        if queasy.number3 == 4:
            startshift4 = queasy.number1
            endshift4 = queasy.number2

    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.departement >= from_dept) & (H_bill_line.departement <= to_dept)).order_by(H_bill_line.departement, H_bill_line.bill_datum).all():

        if curr_dept != h_bill_line.departement:

            if curr_dept != 0:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.artbezeich = "TOTAL"
                output_list.bfastqty = depbfastqty
                output_list.bfastamount =  to_decimal(depbfastamount)
                output_list.lunchqty = deplunchqty
                output_list.lunchamount =  to_decimal(deplunchamount)
                output_list.dinnerqty = depdinnerqty
                output_list.dinneramount =  to_decimal(depdinneramount)
                output_list.supperqty = depsupperqty
                output_list.supperamount =  to_decimal(depsupperamount)
                output_list.totqty = deptotqty
                output_list.totamount =  to_decimal(deptotamount)


                output_list = Output_list()
                output_list_data.append(output_list)

            curr_dept = h_bill_line.departement

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

            if hoteldpt:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.artbezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")

        if curr_date != h_bill_line.bill_datum:
            curr_date = h_bill_line.bill_datum

            for b_hbline in db_session.query(B_hbline).filter(
                     (B_hbline.departement == curr_dept) & (B_hbline.bill_datum == curr_date)).order_by(B_hbline._recid).all():

                h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, b_hbline.artnr)],"artart": [(eq, 0)]})

                if h_artikel:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.departement = curr_dept
                    output_list.datum = b_hbline.bill_datum
                    output_list.zeit = to_string(b_hbline.zeit, "hh:mm")
                    output_list.artnr = b_hbline.artnr
                    output_list.artbezeich = h_artikel.bezeich


                    billtime = to_string(b_hbline.zeit, "HH:MM")
                    billtime = entry(0, billtime, ":") + entry(1, billtime, ":")

                    if to_int(billtime) >= startshift1 and to_int(billtime) < endshift1:
                        output_list.bfastqty = b_hbline.anzahl
                        output_list.bfastamount =  to_decimal(b_hbline.betrag)

                    if to_int(billtime) >= startshift2 and to_int(billtime) < endshift2:
                        output_list.lunchqty = b_hbline.anzahl
                        output_list.lunchamount =  to_decimal(b_hbline.betrag)

                    if to_int(billtime) >= startshift3 and to_int(billtime) < endshift3:
                        output_list.dinnerqty = b_hbline.anzahl
                        output_list.dinneramount =  to_decimal(b_hbline.betrag)

                    if to_int(billtime) >= startshift4 and to_int(billtime) < endshift4:
                        output_list.supperqty = b_hbline.anzahl
                        output_list.supperamount =  to_decimal(b_hbline.betrag)


                    output_list.totqty = output_list.bfastqty + output_list.lunchqty + output_list.dinnerqty + output_list.supperqty
                    output_list.totamount =  to_decimal(output_list.bfastamount) + to_decimal(output_list.lunchamount) + to_decimal(output_list.dinneramount) + to_decimal(output_list.supperamount)


                    totbfastqty = totbfastqty + output_list.bfastqty
                    totbfastamount =  to_decimal(totbfastamount) + to_decimal(output_list.bfastamount)
                    totlunchqty = totlunchqty + output_list.lunchqty
                    totlunchamount =  to_decimal(totlunchamount) + to_decimal(output_list.lunchamount)
                    totdinnerqty = totdinnerqty + output_list.dinnerqty
                    totdinneramount =  to_decimal(totdinneramount) + to_decimal(output_list.dinneramount)
                    totsupperqty = totsupperqty + output_list.supperqty
                    totsupperamount =  to_decimal(totsupperamount) + to_decimal(output_list.supperamount)
                    sumtotqty = sumtotqty + output_list.totqty
                    sumtotamount =  to_decimal(sumtotamount) + to_decimal(output_list.totamount)


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.artbezeich = "SUB TOTAL"
            output_list.bfastqty = totbfastqty
            output_list.bfastamount =  to_decimal(totbfastamount)
            output_list.lunchqty = totlunchqty
            output_list.lunchamount =  to_decimal(totlunchamount)
            output_list.dinnerqty = totdinnerqty
            output_list.dinneramount =  to_decimal(totdinneramount)
            output_list.supperqty = totsupperqty
            output_list.supperamount =  to_decimal(totsupperamount)
            output_list.totqty = sumtotqty
            output_list.totamount =  to_decimal(sumtotamount)


            output_list = Output_list()
            output_list_data.append(output_list)

            totbfastqty = 0
            totbfastamount =  to_decimal("0")
            totlunchqty = 0
            totlunchamount =  to_decimal("0")
            totdinnerqty = 0
            totdinneramount =  to_decimal("0")
            totsupperqty = 0
            totsupperamount =  to_decimal("0")
            sumtotqty = 0
            sumtotamount =  to_decimal("0")


        depbfastqty = 0
        depbfastamount =  to_decimal("0")
        deplunchqty = 0
        deplunchamount =  to_decimal("0")
        depdinnerqty = 0
        depdinneramount =  to_decimal("0")
        depsupperqty = 0
        depsupperamount =  to_decimal("0")
        deptotqty = 0
        deptotamount =  to_decimal("0")

        for output_list in query(output_list_data, filters=(lambda output_list: output_list.departement == curr_dept)):
            depbfastqty = depbfastqty + output_list.bfastqty
            depbfastamount =  to_decimal(depbfastamount) + to_decimal(output_list.bfastamount)
            deplunchqty = deplunchqty + output_list.lunchqty
            deplunchamount =  to_decimal(deplunchamount) + to_decimal(output_list.lunchamount)
            depdinnerqty = depdinnerqty + output_list.dinnerqty
            depdinneramount =  to_decimal(depdinneramount) + to_decimal(output_list.dinneramount)
            depsupperqty = depsupperqty + output_list.supperqty
            depsupperamount =  to_decimal(depsupperamount) + to_decimal(output_list.supperamount)
            deptotqty = deptotqty + output_list.totqty
            deptotamount =  to_decimal(deptotamount) + to_decimal(output_list.totamount)


    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.artbezeich = "TOTAL"
    output_list.bfastqty = depbfastqty
    output_list.bfastamount =  to_decimal(depbfastamount)
    output_list.lunchqty = deplunchqty
    output_list.lunchamount =  to_decimal(deplunchamount)
    output_list.dinnerqty = depdinnerqty
    output_list.dinneramount =  to_decimal(depdinneramount)
    output_list.supperqty = depsupperqty
    output_list.supperamount =  to_decimal(depsupperamount)
    output_list.totqty = deptotqty
    output_list.totamount =  to_decimal(deptotamount)


    output_list = Output_list()
    output_list_data.append(output_list)

    sumtotbfastqty = 0
    sumtotbfastamount =  to_decimal("0")
    sumtotlunchqty = 0
    sumtotlunchamount =  to_decimal("0")
    sumtotdinnerqty = 0
    sumtotdinneramount =  to_decimal("0")
    sumtotsupperqty = 0
    sumtotsupperamount =  to_decimal("0")
    totsumtotqty = 0
    totsumtotamount =  to_decimal("0")

    for output_list in query(output_list_data, filters=(lambda output_list: output_list.artbezeich.lower()  == ("TOTAL").lower())):
        sumtotbfastqty = sumtotbfastqty + output_list.bfastqty
        sumtotbfastamount =  to_decimal(sumtotbfastamount) + to_decimal(output_list.bfastamount)
        sumtotlunchqty = sumtotlunchqty + output_list.lunchqty
        sumtotlunchamount =  to_decimal(sumtotlunchamount) + to_decimal(output_list.lunchamount)
        sumtotdinnerqty = sumtotdinnerqty + output_list.dinnerqty
        sumtotdinneramount =  to_decimal(sumtotdinneramount) + to_decimal(output_list.dinneramount)
        sumtotsupperqty = sumtotsupperqty + output_list.supperqty
        sumtotsupperamount =  to_decimal(sumtotsupperamount) + to_decimal(output_list.supperamount)
        totsumtotqty = totsumtotqty + output_list.totqty
        totsumtotamount =  to_decimal(totsumtotamount) + to_decimal(output_list.totamount)


    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.artbezeich = "G R A N D T O T A L"
    output_list.bfastqty = sumtotbfastqty
    output_list.bfastamount =  to_decimal(sumtotbfastamount)
    output_list.lunchqty = sumtotlunchqty
    output_list.lunchamount =  to_decimal(sumtotlunchamount)
    output_list.dinnerqty = sumtotdinnerqty
    output_list.dinneramount =  to_decimal(sumtotdinneramount)
    output_list.supperqty = sumtotsupperqty
    output_list.supperamount =  to_decimal(sumtotsupperamount)
    output_list.totqty = totsumtotqty
    output_list.totamount =  to_decimal(totsumtotamount)

    for output_list in query(output_list_data):
        output_list2 = Output_list2()
        output_list2_data.append(output_list2)


        if trim(substring(output_list.artbezeich, 0, 1)) == ("0").lower() :
            output_list2.departement = ""
            output_list2.datum = ""
            output_list2.zeit = ""
            output_list2.artnr = ""
            output_list2.artbezeich = to_string(output_list.artbezeich)
            output_list2.bfastqty = ""
            output_list2.bfastamount = ""
            output_list2.lunchqty = ""
            output_list2.lunchamount = ""
            output_list2.dinnerqty = ""
            output_list2.dinneramount = ""
            output_list2.supperqty = ""
            output_list2.supperamount = ""
            output_list2.totqty = ""
            output_list2.totamount = ""

        elif output_list.departement == 0 and output_list.artbezeich != "":
            output_list2.departement = ""
            output_list2.datum = ""
            output_list2.zeit = ""
            output_list2.artnr = ""
            output_list2.artbezeich = to_string(output_list.artbezeich)
            output_list2.bfastqty = to_string(output_list.bfastqty, "->>>>>9")
            output_list2.bfastamount = to_string(output_list.bfastamount, "->>,>>>,>>>,>>9.99")
            output_list2.lunchqty = to_string(output_list.lunchqty, "->>>>>9")
            output_list2.lunchamount = to_string(output_list.lunchamount, "->>,>>>,>>>,>>9.99")
            output_list2.dinnerqty = to_string(output_list.dinnerqty, "->>>>>9")
            output_list2.dinneramount = to_string(output_list.dinneramount, "->>,>>>,>>>,>>9.99")
            output_list2.supperqty = to_string(output_list.supperqty, "->>>>>9")
            output_list2.supperamount = to_string(output_list.supperamount, "->>,>>>,>>>,>>9.99")
            output_list2.totqty = to_string(output_list.totqty, "->>>>>9")
            output_list2.totamount = to_string(output_list.totamount, "->>,>>>,>>>,>>9.99")

        elif output_list.departement == 0 and output_list.artbezeich == "":
            output_list2.departement = ""
            output_list2.datum = ""
            output_list2.zeit = ""
            output_list2.artnr = ""
            output_list2.artbezeich = ""
            output_list2.bfastqty = ""
            output_list2.bfastamount = ""
            output_list2.lunchqty = ""
            output_list2.lunchamount = ""
            output_list2.dinnerqty = ""
            output_list2.dinneramount = ""
            output_list2.supperqty = ""
            output_list2.supperamount = ""
            output_list2.totqty = ""
            output_list2.totamount = ""


        else:
            output_list2.departement = to_string(output_list.departement)
            output_list2.datum = to_string(output_list.datum)
            output_list2.zeit = to_string(output_list.zeit)
            output_list2.artnr = to_string(output_list.artnr, ">>>>>>>>>9")
            output_list2.artbezeich = to_string(output_list.artbezeich)
            output_list2.bfastqty = to_string(output_list.bfastqty, "->>>>>9")
            output_list2.bfastamount = to_string(output_list.bfastamount, "->>,>>>,>>>,>>9.99")
            output_list2.lunchqty = to_string(output_list.lunchqty, "->>>>>9")
            output_list2.lunchamount = to_string(output_list.lunchamount, "->>,>>>,>>>,>>9.99")
            output_list2.dinnerqty = to_string(output_list.dinnerqty, "->>>>>9")
            output_list2.dinneramount = to_string(output_list.dinneramount, "->>,>>>,>>>,>>9.99")
            output_list2.supperqty = to_string(output_list.supperqty, "->>>>>9")
            output_list2.supperamount = to_string(output_list.supperamount, "->>,>>>,>>>,>>9.99")
            output_list2.totqty = to_string(output_list.totqty, "->>>>>9")
            output_list2.totamount = to_string(output_list.totamount, "->>,>>>,>>>,>>9.99")

    return generate_output()