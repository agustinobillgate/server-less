#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_ophis, L_op

def rcv_annual_btn_gobl(pvilanguage:int, from_grp:int, mm:int, yy:int, sorttype:int):

    prepare_cache ([Htparam, L_artikel, L_ophis, L_op])

    str_list_list = []
    lvcarea:string = "rcv-annual"
    htparam = l_artikel = l_ophis = l_op = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"num":int, "artnr":int, "bezeich":string, "qty":[Decimal,12], "avrg":[Decimal,12], "amt":[Decimal,12], "tot_qty":Decimal, "tot_amt":Decimal, "del_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, lvcarea, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, from_grp, mm, yy, sorttype


        nonlocal str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def create_list(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, from_grp, sorttype


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        to_date:date = None
        from_date:date = None
        datum:date = None
        closed_date:date = None
        date_mat:date = None
        date_fb:date = None
        tot_qty:List[int] = create_empty_list(12,0)
        tot_amt:List[Decimal] = create_empty_list(12,to_decimal("0"))
        del_flag:bool = True
        zeit:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        date_mat = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        date_fb = htparam.fdate

        if date_mat > date_fb:
            closed_date = date_mat
        else:
            closed_date = date_fb
        str_list_list.clear()
        for i in range(mm,mm + 1) :
            from_date = date_mdy(i, 1, yy)
            to_date = date_mdy(i + 1, 1, yy)
            to_date = to_date - timedelta(days=1)
            for datum in date_range(from_date,to_date) :

                if datum <= closed_date:

                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    for l_ophis.artnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.artnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                             (L_ophis.datum == datum) & (L_ophis.op_art == 1)).order_by(L_ophis.artnr).all():
                        if l_ophis_obj_list.get(l_ophis._recid):
                            continue
                        else:
                            l_ophis_obj_list[l_ophis._recid] = True

                        str_list = query(str_list_list, filters=(lambda str_list: str_list.artnr == l_ophis.artnr), first=True)

                        if not str_list:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.artnr = l_artikel.artnr
                            str_list.bezeich = l_artikel.bezeich


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_ophis.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_ophis.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]
                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    for l_op.artnr, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.artnr, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                             (L_op.datum == datum) & (L_op.op_art == 1) & (L_op.loeschflag <= 1)).order_by(L_op.artnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        str_list = query(str_list_list, filters=(lambda str_list: str_list.artnr == l_op.artnr), first=True)

                        if not str_list:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.artnr = l_artikel.artnr
                            str_list.bezeich = l_artikel.bezeich


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_op.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_op.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]

        for str_list in query(str_list_list):
            for i in range(mm,mm + 1) :
                str_list.tot_qty =  to_decimal(str_list.tot_qty) + to_decimal(str_list.qty[i - 1])
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal(str_list.amt[i - 1])
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_qty == 0)):
                str_list_list.remove(str_list)

        elif sorttype == 1:

            for str_list in query(str_list_list):
                del_flag = True
                for i in range(mm,mm + 1) :

                    if str_list.avrg[i - 1] != 0:
                        del_flag = False

                if del_flag:
                    str_list_list.remove(str_list)
        else:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_amt == 0)):
                str_list_list.remove(str_list)

        if sorttype != 1:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")


            for i in range(mm,mm + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]


    def create_list1(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, from_grp, sorttype


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        to_date:date = None
        from_date:date = None
        datum:date = None
        closed_date:date = None
        date_mat:date = None
        date_fb:date = None
        tot_qty:List[int] = create_empty_list(12,0)
        tot_amt:List[Decimal] = create_empty_list(12,to_decimal("0"))
        del_flag:bool = True
        zeit:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        date_mat = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        date_fb = htparam.fdate

        if date_mat > date_fb:
            closed_date = date_mat
        else:
            closed_date = date_fb
        str_list_list.clear()
        for i in range(mm,mm + 1) :
            from_date = date_mdy(i, 1, yy)
            to_date = date_mdy(i + 1, 1, yy)
            to_date = to_date - timedelta(days=1)
            for datum in date_range(from_date,to_date) :

                if datum <= closed_date:

                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    for l_ophis.artnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.artnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).filter(
                             (L_ophis.datum == datum) & (L_ophis.op_art == 1)).order_by(L_ophis.artnr).all():
                        if l_ophis_obj_list.get(l_ophis._recid):
                            continue
                        else:
                            l_ophis_obj_list[l_ophis._recid] = True

                        str_list = query(str_list_list, filters=(lambda str_list: str_list.artnr == l_ophis.artnr), first=True)

                        if not str_list:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.artnr = l_artikel.artnr
                            str_list.bezeich = l_artikel.bezeich


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_ophis.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_ophis.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]
                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    for l_op.artnr, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.artnr, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).filter(
                             (L_op.datum == datum) & (L_op.op_art == 1) & (L_op.loeschflag < 2)).order_by(L_op.artnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        str_list = query(str_list_list, filters=(lambda str_list: str_list.artnr == l_op.artnr), first=True)

                        if not str_list:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.artnr = l_artikel.artnr
                            str_list.bezeich = l_artikel.bezeich


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_op.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_op.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]

        for str_list in query(str_list_list):
            for i in range(mm,mm + 1) :
                str_list.tot_qty =  to_decimal(str_list.tot_qty) + to_decimal(str_list.qty[i - 1])
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal(str_list.amt[i - 1])
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_qty == 0)):
                str_list_list.remove(str_list)

        elif sorttype == 1:

            for str_list in query(str_list_list):
                del_flag = True
                for i in range(mm,mm + 1) :

                    if str_list.avrg[i - 1] != 0:
                        del_flag = False

                if del_flag:
                    str_list_list.remove(str_list)
        else:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_amt == 0)):
                str_list_list.remove(str_list)

        if sorttype != 1:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")


            for i in range(mm,mm + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]


    if from_grp == 0:
        create_list(mm, yy)
    else:
        create_list1(mm, yy)

    return generate_output()