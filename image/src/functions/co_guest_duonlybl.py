from functions.additional_functions import *
import decimal

def co_guest_duonlybl(pvilanguage:int, cl_list:[Cl_list]):
    t_deposit:decimal = 0
    t_cash:decimal = 0
    t_cc:decimal = 0
    t_cl:decimal = 0
    t_tot:decimal = 0
    t_rm:int = 0
    counter:int = 0
    lvcarea:str = "co_guest"

    cl_list = cl_list1 = None

    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "reihe":int, "zinr":str, "name":str, "zipreis":decimal, "s_zipreis":str, "rechnr":int, "ankunft":date, "abreise":date, "cotime":str, "deposit":decimal, "s_deposit":str, "cash":decimal, "s_cash":str, "cc":decimal, "s_cc":str, "cl":decimal, "s_cl":str, "tot":decimal, "s_tot":str, "resnr":int, "company":str}, {"ankunft": None, "abreise": None})
    cl_list1_list, Cl_list1 = create_model_like(Cl_list)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_deposit, t_cash, t_cc, t_cl, t_tot, t_rm, counter, lvcarea


        nonlocal cl_list, cl_list1
        nonlocal cl_list_list, cl_list1_list
        return {}

    cl_list1._list.clear()

    for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.flag == 1)):
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_list.append(cl_list1)

        buffer_copy(cl_list, cl_list1)
        cl_list1.s_deposit = to_string(cl_list.deposit, "->,>>>,>>9.99")
        cl_list1.s_cc = to_string(cl_list.cc, "->,>>>,>>9.99")
        cl_list1.s_cl = to_string(cl_list.cl, "->,>>>,>>9.99")
        cl_list1.s_cash = to_string(cl_list.cash, "->,>>>,>>9.99")
        cl_list1.s_tot = to_string(cl_list.tot, "->,>>>,>>9.99")
        cl_list1.reihe = counter


        t_deposit = t_deposit + cl_list.deposit
        t_cash = t_cash + cl_list.cash
        t_cc = t_cc + cl_list.cc
        t_cl = t_cl + cl_list.cl
        t_tot = t_tot + cl_list.tot
        t_rm = t_rm + 1


    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_list.append(cl_list1)

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
    cl_list1_list.append(cl_list1)

    cl_list1.reihe = counter
    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_list.append(cl_list1)

    cl_list1.reihe = counter
    cl_list1.name = translateExtended ("Additional Day Use", lvcarea, "")
    t_deposit = 0
    t_cc = 0
    t_cl = 0
    t_cash = 0
    t_tot = 0
    t_rm = 0

    for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.flag == 0)):
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_list.append(cl_list1)

        buffer_copy(cl_list, cl_list1)
        cl_list1.reihe = counter
        cl_list1.s_deposit = to_string(cl_list.deposit, "->,>>>,>>9.99")
        cl_list1.s_cc = to_string(cl_list.cc, "->,>>>,>>9.99")
        cl_list1.s_cl = to_string(cl_list.cl, "->,>>>,>>9.99")
        cl_list1.s_cash = to_string(cl_list.cash, "->,>>>,>>9.99")
        cl_list1.s_tot = to_string(cl_list.tot, "->,>>>,>>9.99")


        t_deposit = t_deposit + cl_list.deposit
        t_cash = t_cash + cl_list.cash
        t_cc = t_cc + cl_list.cc
        t_cl = t_cl + cl_list.cl
        t_tot = t_tot + cl_list.tot
        t_rm = t_rm + 1


    counter = counter + 1
    cl_list1 = Cl_list1()
    cl_list1_list.append(cl_list1)

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
    cl_list1_list.append(cl_list1)

    cl_list1.reihe = counter

    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.flag == 2), first=True)

    if cl_list:
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_list.append(cl_list1)

        buffer_copy(cl_list, cl_list1)
        cl_list1.reihe = counter
    cl_list._list.clear()

    for cl_list1 in query(cl_list1_list):
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        buffer_copy(cl_list1, cl_list)

    return generate_output()