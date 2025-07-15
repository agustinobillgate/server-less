#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal

cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "reihe":int, "zinr":string, "name":string, "zipreis":Decimal, "s_zipreis":string, "rechnr":int, "ankunft":date, "abreise":date, "cotime":string, "deposit":Decimal, "s_deposit":string, "cash":Decimal, "s_cash":string, "cc":Decimal, "s_cc":string, "cl":Decimal, "s_cl":string, "tot":Decimal, "s_tot":string, "resnr":int, "company":string, "bill_balance":Decimal, "reslin_no":int}, {"ankunft": None, "abreise": None})

def co_guest_duonlybl(pvilanguage:int, cl_list_data:[Cl_list]):
    t_deposit:Decimal = to_decimal("0.0")
    t_cash:Decimal = to_decimal("0.0")
    t_cc:Decimal = to_decimal("0.0")
    t_cl:Decimal = to_decimal("0.0")
    t_tot:Decimal = to_decimal("0.0")
    t_rm:int = 0
    counter:int = 0
    lvcarea:string = "co-guest"

    cl_list = cl_list1 = None

    cl_list1_data, Cl_list1 = create_model_like(Cl_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_deposit, t_cash, t_cc, t_cl, t_tot, t_rm, counter, lvcarea
        nonlocal pvilanguage


        nonlocal cl_list, cl_list1
        nonlocal cl_list1_data

        return {"cl-list": cl_list_data}

    cl_list1_data.clear()

    for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.flag == 1)):
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_data.append(cl_list1)

        buffer_copy(cl_list, cl_list1)
        cl_list1.s_deposit = to_string(cl_list.deposit, "->,>>>,>>9.99")
        cl_list1.s_cc = to_string(cl_list.cc, "->,>>>,>>9.99")
        cl_list1.s_cl = to_string(cl_list.cl, "->,>>>,>>9.99")
        cl_list1.s_cash = to_string(cl_list.cash, "->,>>>,>>9.99")
        cl_list1.s_tot = to_string(cl_list.tot, "->,>>>,>>9.99")
        cl_list1.reihe = counter


        t_deposit =  to_decimal(t_deposit) + to_decimal(cl_list.deposit)
        t_cash =  to_decimal(t_cash) + to_decimal(cl_list.cash)
        t_cc =  to_decimal(t_cc) + to_decimal(cl_list.cc)
        t_cl =  to_decimal(t_cl) + to_decimal(cl_list.cl)
        t_tot =  to_decimal(t_tot) + to_decimal(cl_list.tot)
        t_rm = t_rm + 1


    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_data.append(cl_list1)

    cl_list1.reihe = counter
    cl_list1.name = translateExtended ("Total C/O Room(s)", lvcarea, "")
    cl_list1.s_zipreis = to_string(t_rm, ">>>>>>>>>>>9")
    cl_list1.s_deposit = to_string(t_deposit, "->,>>>,>>9.99")
    cl_list1.s_cash = to_string(t_cash, "->,>>>,>>9.99")
    cl_list1.s_cc = to_string(t_cc, "->,>>>,>>9.99")
    cl_list1.s_cl = to_string(t_cl, "->,>>>,>>9.99")
    cl_list1.s_tot = to_string(t_tot, "->,>>>,>>9.99")


    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_data.append(cl_list1)

    cl_list1.reihe = counter
    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_data.append(cl_list1)

    cl_list1.reihe = counter
    cl_list1.name = translateExtended ("Additional Day Use", lvcarea, "")
    t_deposit =  to_decimal("0")
    t_cc =  to_decimal("0")
    t_cl =  to_decimal("0")
    t_cash =  to_decimal("0")
    t_tot =  to_decimal("0")
    t_rm = 0

    for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.flag == 0)):
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_data.append(cl_list1)

        buffer_copy(cl_list, cl_list1)
        cl_list1.reihe = counter
        cl_list1.s_deposit = to_string(cl_list.deposit, "->,>>>,>>9.99")
        cl_list1.s_cc = to_string(cl_list.cc, "->,>>>,>>9.99")
        cl_list1.s_cl = to_string(cl_list.cl, "->,>>>,>>9.99")
        cl_list1.s_cash = to_string(cl_list.cash, "->,>>>,>>9.99")
        cl_list1.s_tot = to_string(cl_list.tot, "->,>>>,>>9.99")


        t_deposit =  to_decimal(t_deposit) + to_decimal(cl_list.deposit)
        t_cash =  to_decimal(t_cash) + to_decimal(cl_list.cash)
        t_cc =  to_decimal(t_cc) + to_decimal(cl_list.cc)
        t_cl =  to_decimal(t_cl) + to_decimal(cl_list.cl)
        t_tot =  to_decimal(t_tot) + to_decimal(cl_list.tot)
        t_rm = t_rm + 1


    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_data.append(cl_list1)

    cl_list1.reihe = counter
    cl_list1.name = translateExtended ("Total C/O Room(s)", lvcarea, "")
    cl_list1.s_zipreis = to_string(t_rm, ">>>>>>>>>>>9")
    cl_list1.s_deposit = to_string(t_deposit, "->,>>>,>>9.99")
    cl_list1.s_cash = to_string(t_cash, "->,>>>,>>9.99")
    cl_list1.s_cc = to_string(t_cc, "->,>>>,>>9.99")
    cl_list1.s_cl = to_string(t_cl, "->,>>>,>>9.99")
    cl_list1.s_tot = to_string(t_tot, "->,>>>,>>9.99")


    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_data.append(cl_list1)

    cl_list1.reihe = counter

    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.flag == 2), first=True)

    if cl_list:
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_data.append(cl_list1)

        buffer_copy(cl_list, cl_list1)
        cl_list1.reihe = counter
    cl_list_data.clear()

    for cl_list1 in query(cl_list1_data):
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        buffer_copy(cl_list1, cl_list)

    return generate_output()