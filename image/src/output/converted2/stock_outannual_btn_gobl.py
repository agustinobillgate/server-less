#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_ophis, L_op

def stock_outannual_btn_gobl(pvilanguage:int, sorttype:int, from_grp:int, mm:int, yy:int):

    prepare_cache ([Htparam, L_artikel, L_ophis, L_op])

    str_list_list = []
    lvcarea:string = "stock-outannual"
    end_date:List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    end_date1:List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    to_date:date = None
    from_date:date = None
    datum:date = None
    closed_date:date = None
    date_mat:date = None
    date_fb:date = None
    num_date:int = 0
    htparam = l_artikel = l_ophis = l_op = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"num":int, "artnr":int, "bezeich":string, "qty":[int,12], "avrg":[Decimal,12], "amt":[Decimal,12], "tot_qty":int, "tot_amt":Decimal, "del_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, num_date, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, sorttype, from_grp, mm, yy


        nonlocal str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def create_list(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, num_date, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, sorttype, from_grp, str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:List[int] = create_empty_list(12,0)
        tot_amt:List[Decimal] = create_empty_list(12,to_decimal("0"))
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()
        sdate = from_date
        edate = to_date

        l_ophis_obj_list = {}
        l_ophis = L_ophis()
        l_artikel = L_artikel()
        for l_ophis.artnr, l_ophis.datum, l_ophis.anzahl, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.artnr, L_ophis.datum, L_ophis.anzahl, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                 (L_ophis.datum >= sdate) & (L_ophis.datum <= edate) & (L_ophis.op_art == 3)).order_by(L_ophis.artnr).all():
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


            str_list.qty[get_month(l_ophis.datum) - 1] = str_list.qty[get_month(l_ophis.datum) - 1] + l_ophis.anzahl
            str_list.amt[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] + l_ophis.warenwert

            if str_list.qty[get_month(l_ophis.datum) - 1] > 0:
                str_list.avrg[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] / str_list.qty[get_month(l_ophis.datum) - 1]
        sdate = closed_date + timedelta(days=1)
        edate = to_date

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.artnr, l_op.datum, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.artnr, L_op.datum, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.datum >= sdate) & (L_op.datum <= edate) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.artnr).all():
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


            str_list.qty[get_month(l_op.datum) - 1] = str_list.qty[get_month(l_op.datum) - 1] + l_op.anzahl
            str_list.amt[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] + l_op.warenwert

            if str_list.qty[get_month(l_op.datum) - 1] > 0:
                str_list.avrg[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] / str_list.qty[get_month(l_op.datum) - 1]

        for str_list in query(str_list_list):
            for i in range(1,12 + 1) :
                str_list.tot_qty = str_list.tot_qty + str_list.qty[i - 1]
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal(str_list.amt[i - 1])
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_qty == 0)):
                str_list_list.remove(str_list)


        elif sorttype == 1:

            for str_list in query(str_list_list):
                del_flag = True
                for i in range(1,12 + 1) :

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


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]


    def create_list1(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, num_date, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, sorttype, from_grp, str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:List[int] = create_empty_list(12,0)
        tot_amt:List[Decimal] = create_empty_list(12,to_decimal("0"))
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()
        sdate = from_date
        edate = to_date

        l_ophis_obj_list = {}
        l_ophis = L_ophis()
        l_artikel = L_artikel()
        for l_ophis.artnr, l_ophis.datum, l_ophis.anzahl, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.artnr, L_ophis.datum, L_ophis.anzahl, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).filter(
                 (L_ophis.datum >= sdate) & (L_ophis.datum <= edate) & (L_ophis.op_art == 3)).order_by(L_ophis.artnr).all():
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


            str_list.qty[get_month(l_ophis.datum) - 1] = str_list.qty[get_month(l_ophis.datum) - 1] + l_ophis.anzahl
            str_list.amt[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] + l_ophis.warenwert

            if str_list.qty[get_month(l_ophis.datum) - 1] > 0:
                str_list.avrg[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] / str_list.qty[get_month(l_ophis.datum) - 1]
        sdate = closed_date + timedelta(days=1)
        edate = to_date

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.artnr, l_op.datum, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.artnr, L_op.datum, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).filter(
                 (L_op.datum >= sdate) & (L_op.datum <= edate) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.artnr).all():
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


            str_list.qty[get_month(l_op.datum) - 1] = str_list.qty[get_month(l_op.datum) - 1] + l_op.anzahl
            str_list.amt[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] + l_op.warenwert

            if str_list.qty[get_month(l_op.datum) - 1] > 0:
                str_list.avrg[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] / str_list.qty[get_month(l_op.datum) - 1]

        for str_list in query(str_list_list):
            for i in range(1,12 + 1) :
                str_list.tot_qty = str_list.tot_qty + str_list.qty[i - 1]
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal(str_list.amt[i - 1])
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_qty == 0)):
                str_list_list.remove(str_list)


        elif sorttype == 1:

            for str_list in query(str_list_list):
                del_flag = True
                for i in range(1,12 + 1) :

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


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]


    def create_list2(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, num_date, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, sorttype, from_grp, str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:List[int] = create_empty_list(12,0)
        tot_amt:List[Decimal] = create_empty_list(12,to_decimal("0"))
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.artnr, l_op.datum, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.artnr, L_op.datum, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.artnr).all():
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


            str_list.qty[get_month(l_op.datum) - 1] = str_list.qty[get_month(l_op.datum) - 1] + l_op.anzahl
            str_list.amt[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] + l_op.warenwert

            if str_list.qty[get_month(l_op.datum) - 1] > 0:
                str_list.avrg[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] / str_list.qty[get_month(l_op.datum) - 1]

        for str_list in query(str_list_list):
            for i in range(1,12 + 1) :
                str_list.tot_qty = str_list.tot_qty + str_list.qty[i - 1]
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal(str_list.amt[i - 1])
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_qty == 0)):
                str_list_list.remove(str_list)


        elif sorttype == 1:

            for str_list in query(str_list_list):
                del_flag = True
                for i in range(1,12 + 1) :

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


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]


    def create_list3(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, num_date, htparam, l_artikel, l_ophis, l_op
        nonlocal pvilanguage, sorttype, from_grp, str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:List[int] = create_empty_list(12,0)
        tot_amt:List[Decimal] = create_empty_list(12,to_decimal("0"))
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.artnr, l_op.datum, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.artnr, L_op.datum, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).filter(
                 (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.artnr).all():
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


            str_list.qty[get_month(l_op.datum) - 1] = str_list.qty[get_month(l_op.datum) - 1] + l_op.anzahl
            str_list.amt[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] + l_op.warenwert

            if str_list.qty[get_month(l_op.datum) - 1] > 0:
                str_list.avrg[get_month(l_op.datum) - 1] = str_list.amt[get_month(l_op.datum) - 1] / str_list.qty[get_month(l_op.datum) - 1]

        for str_list in query(str_list_list):
            for i in range(1,12 + 1) :
                str_list.tot_qty = str_list.tot_qty + str_list.qty[i - 1]
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal(str_list.amt[i - 1])
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list: str_list.tot_qty == 0)):
                str_list_list.remove(str_list)


        elif sorttype == 1:

            for str_list in query(str_list_list):
                del_flag = True
                for i in range(1,12 + 1) :

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


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]


    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    date_mat = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    date_fb = htparam.fdate

    if date_mat > date_fb:
        closed_date = date_mat
    else:
        closed_date = date_fb
    from_date = date_mdy(1, 1, yy)

    if yy % 4 != 0:
        num_date = end_date1[mm - 1]
        to_date = date_mdy(mm, num_date, yy)
    else:
        num_date = end_date1[mm - 1]
        to_date = date_mdy(mm, num_date, yy)

    if from_date <= closed_date:

        if from_grp == 0:
            create_list(mm, yy)
        else:
            create_list1(mm, yy)
    else:

        if from_grp == 0:
            create_list2(mm, yy)
        else:
            create_list3(mm, yy)

    return generate_output()