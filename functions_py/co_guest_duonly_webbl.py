#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal

cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "reihe":int, "zinr":string, "name":string, "zipreis":Decimal, "s_zipreis":string, "rechnr":int, "ankunft":date, "abreise":date, "cotime":string, "deposit":Decimal, "s_deposit":string, "cash":Decimal, "s_cash":string, "cc":Decimal, "s_cc":string, "cl":Decimal, "s_cl":string, "tot":Decimal, "s_tot":string, "resnr":int, "company":string, "bill_balance":Decimal, "reslin_no":int, "bill_flag":int, "bill_type":string, "guest_bl_recid":int, "master_bl_recid":int, "guest_nr":int, "guest_typ":int, "gastnr":int, "fg_col":bool, "rm_type":string}, {"ankunft": None, "abreise": None})

def co_guest_duonly_webbl(pvilanguage:int, cl_list):
    t_deposit:Decimal = to_decimal("0.0")
    t_cash:Decimal = to_decimal("0.0")
    t_cc:Decimal = to_decimal("0.0")
    t_cl:Decimal = to_decimal("0.0")
    t_tot:Decimal = to_decimal("0.0")
    t_rm:int = 0
    counter:int = 0
    lvcarea:string = "co-guest"

    cl_list_save = cl_list1 = None

    cl_list1_data, Cl_list1 = create_model_like(Cl_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_deposit, t_cash, t_cc, t_cl, t_tot, t_rm, counter, lvcarea
        nonlocal pvilanguage


        nonlocal cl_list, cl_list1
        nonlocal cl_list1_data

        return {"cl-list": cl_list_data}

    cl_list1_data.clear()

    cl_list = [Cl_list
        (
            flag=item.get("flag"),
            reihe=item.get("reihe"),
            zinr=item.get("zinr"),
            name=item.get("name"),
            zipreis=Decimal(item.get("zipreis", 0)),
            rechnr=item.get("rechnr"),
            ankunft=item.get("ankunft"),
            abreise=item.get("abreise"),
            cotime=item.get("cotime"),
            deposit=Decimal(item.get("deposit", 0)),
            cash=Decimal(item.get("cash", 0)),
            cc=Decimal(item.get("cc", 0)),
            cl=Decimal(item.get("cl", 0)),
            tot=Decimal(item.get("tot", 0)),
            resnr=item.get("resnr"),
            company=item.get("company"),
            gastnr=item.get("gastnr"),
            s_zipreis=item.get("s-zipreis"),
            s_deposit=item.get("s-deposit"),
            s_cash=item.get("s-cash"),
            s_cc=item.get("s-cc"),
            s_cl=item.get("s-cl"),
            s_tot=item.get("s-tot"),
            bill_balance=item.get("bill-balance"),
            reslin_no=item.get("reslin-no"),
            bill_flag=item.get("bill-flag"),
            bill_type=item.get("bill-type"),
            guest_bl_recid=item.get("guest-bl-recid"),
            master_bl_recid=item.get("master-bl-recid"),
            fg_col=item.get("fg-col"),
            guest_nr=item.get("guest-nr"),
            guest_typ=item.get("guest-typ"),
            rm_type=item.get("rm-type"),
        )

        for item in cl_list["cl-list"]
    ]


    for cl1 in query(cl_list, filters=(lambda cl_list: cl_list.flag == 1)):
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_data.append(cl_list1)

        buffer_copy(cl1, cl_list1)
        cl_list1.s_deposit = to_string(cl1.deposit, "->,>>>,>>9.99")
        cl_list1.s_cc = to_string(cl1.cc, "->,>>>,>>9.99")
        cl_list1.s_cl = to_string(cl1.cl, "->,>>>,>>9.99")
        cl_list1.s_cash = to_string(cl1.cash, "->,>>>,>>9.99")
        cl_list1.s_tot = to_string(cl1.tot, "->,>>>,>>9.99")
        cl_list1.reihe = counter

        t_deposit =  to_decimal(t_deposit) + to_decimal(cl1.deposit)
        t_cash =  to_decimal(t_cash) + to_decimal(cl1.cash)
        t_cc =  to_decimal(t_cc) + to_decimal(cl1.cc)
        t_cl =  to_decimal(t_cl) + to_decimal(cl1.cl)
        t_tot =  to_decimal(t_tot) + to_decimal(cl1.tot)
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

    for cl1 in query(cl_list, filters=(lambda cl_list: cl_list.flag == 0)):
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_data.append(cl_list1)

        buffer_copy(cl1, cl_list1)
        cl_list1.reihe = counter
        cl_list1.s_deposit = to_string(cl1.deposit, "->,>>>,>>9.99")
        cl_list1.s_cc = to_string(cl1.cc, "->,>>>,>>9.99")
        cl_list1.s_cl = to_string(cl1.cl, "->,>>>,>>9.99")
        cl_list1.s_cash = to_string(cl1.cash, "->,>>>,>>9.99")
        cl_list1.s_tot = to_string(cl1.tot, "->,>>>,>>9.99")

        t_deposit =  to_decimal(t_deposit) + to_decimal(cl1.deposit)
        t_cash =  to_decimal(t_cash) + to_decimal(cl1.cash)
        t_cc =  to_decimal(t_cc) + to_decimal(cl1.cc)
        t_cl =  to_decimal(t_cl) + to_decimal(cl1.cl)
        t_tot =  to_decimal(t_tot) + to_decimal(cl1.tot)
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

    cl_list_tmp = query(cl_list, filters=(lambda cl_list: cl_list.flag == 2), first=True)

    if cl_list_tmp:
        counter = counter + 1
        cl_list1 = Cl_list1()
        cl_list1_data.append(cl_list1)

        buffer_copy(cl_list_tmp, cl_list1)
        cl_list1.reihe = counter

    cl_list_data.clear()

    for cl_list1 in query(cl_list1_data):
        cl_list_save = Cl_list()
        cl_list_data.append(cl_list_save)

        buffer_copy(cl_list1, cl_list_save)

    return generate_output()