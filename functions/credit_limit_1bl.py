#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Htparam, Bill, Res_line, Arrangement, Queasy

def credit_limit_1bl(incl_master:bool, by_room:bool):

    prepare_cache ([Guest, Htparam, Bill, Res_line, Arrangement, Queasy])

    cl_list_data = []
    saldo:Decimal = to_decimal("0.0")
    climit:int = 0
    g_climit:Decimal = to_decimal("0.0")
    loopi:int = 0
    str:string = ""
    guest = htparam = bill = res_line = arrangement = queasy = None

    cl_list = bguest = None

    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "rechnr":int, "zinr":string, "receiver":string, "ankunft":date, "abreise":date, "c_limit":Decimal, "saldo":Decimal, "name":string, "resnr":int, "comp_name":string, "rmrate":Decimal, "rate_code":string, "argt_code":string, "pay_type":string, "over":Decimal, "remark":string, "stafid":string}, {"ankunft": None, "abreise": None})

    Bguest = create_buffer("Bguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, saldo, climit, g_climit, loopi, str, guest, htparam, bill, res_line, arrangement, queasy
        nonlocal incl_master, by_room
        nonlocal bguest


        nonlocal cl_list, bguest
        nonlocal cl_list_data

        return {"cl-list": cl_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

    if htparam.fdecimal != 0:
        g_climit =  to_decimal(htparam.fdecimal)
    else:
        g_climit =  to_decimal(htparam.finteger)
    cl_list_data.clear()

    for bill in db_session.query(Bill).filter(
             (Bill.flag == 0) & (Bill.resnr == 0)).order_by(Bill.name).all():

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

        if guest and guest.kreditlimit > 0:
            climit = guest.kreditlimit
        else:
            climit = g_climit

        if bill.saldo > climit:
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = "NS"
            cl_list.name = bill.name
            cl_list.receiver = bill.name
            cl_list.c_limit =  to_decimal(climit)
            cl_list.rechnr = bill.rechnr
            cl_list.saldo =  to_decimal(bill.saldo)
            cl_list.ankunft = None
            cl_list.abreise = None
            cl_list.comp_name = guest.name
            cl_list.rmrate =  to_decimal("0")
            cl_list.rate_code = " "
            cl_list.argt_code = " "
            cl_list.pay_type = " "
            cl_list.over =  to_decimal(bill.saldo) - to_decimal(climit)
            cl_list.remark = " "
            cl_list.stafid = " "

    if incl_master:

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr == "")).order_by(Bill.name).all():

            guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

            if guest and guest.kreditlimit > 0:
                climit = guest.kreditlimit
            else:
                climit = g_climit

            if bill.saldo > climit:

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, 1)]})
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.flag = "M"
                cl_list.name = bill.name
                cl_list.receiver = bill.name
                cl_list.c_limit =  to_decimal(climit)
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(bill.saldo)

                if res_line:
                    cl_list.ankunft = res_line.ankunft
                    cl_list.abreise = res_line.abreise
                    cl_list.rmrate =  to_decimal(res_line.zipreis)
                    cl_list.over =  to_decimal(bill.saldo) - to_decimal(climit)
                    cl_list.remark = " "
                    cl_list.stafid = " "

                    bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if bguest:
                        cl_list.comp_name = guest.name

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:
                        cl_list.argt_code = arrangement.argt_bez

                    if res_line.code != "" and res_line.code.lower()  != ("0").lower() :

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy:
                            cl_list.pay_type = queasy.char1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.rate_code = substring(str, 6)
                            break


    if not by_room:

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "")).order_by(Bill.name).all():

            guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

            if guest and guest.kreditlimit > 0:
                climit = guest.kreditlimit
            else:
                climit = g_climit

            if bill.saldo > climit:

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.resnr = bill.resnr
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                cl_list.c_limit =  to_decimal(climit)
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(bill.saldo)
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise

                if res_line:
                    cl_list.name = res_line.name
                    cl_list.rmrate =  to_decimal(res_line.zipreis)
                    cl_list.over =  to_decimal(bill.saldo) - to_decimal(climit)
                    cl_list.remark = " "
                    cl_list.stafid = " "

                    bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if bguest:
                        cl_list.comp_name = guest.name

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:
                        cl_list.argt_code = arrangement.argt_bez

                    if res_line.code != "" and res_line.code.lower()  != ("0").lower() :

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy:
                            cl_list.pay_type = queasy.char1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.rate_code = substring(str, 6)
                            break

    else:

        for bill in db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.zinr != "")).order_by(to_int(Bill.zinr), Bill.name).all():

            guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

            if guest and guest.kreditlimit > 0:
                climit = guest.kreditlimit
            else:
                climit = g_climit

            if bill.saldo > climit:

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = bill.zinr
                cl_list.resnr = bill.resnr
                cl_list.receiver = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                cl_list.c_limit =  to_decimal(climit)
                cl_list.rechnr = bill.rechnr
                cl_list.saldo =  to_decimal(bill.saldo)
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise

                if res_line:
                    cl_list.name = res_line.name
                    cl_list.rmrate =  to_decimal(res_line.zipreis)
                    cl_list.over =  to_decimal(bill.saldo) - to_decimal(climit)
                    cl_list.remark = " "
                    cl_list.stafid = " "

                    bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if bguest:
                        cl_list.comp_name = guest.name

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    if arrangement:
                        cl_list.argt_code = arrangement.argt_bez

                    if res_line.code != "" and res_line.code.lower()  != ("0").lower() :

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy:
                            cl_list.pay_type = queasy.char1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.rate_code = substring(str, 6)
                            break


    return generate_output()