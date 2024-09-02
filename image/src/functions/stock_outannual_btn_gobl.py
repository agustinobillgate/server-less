from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_artikel, L_ophis, L_op

def stock_outannual_btn_gobl(pvilanguage:int, sorttype:int, from_grp:int, mm:int, yy:int):
    str_list_list = []
    lvcarea:str = "stock_outannual"
    end_date:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_date1:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    to_date:date = None
    from_date:date = None
    datum:date = None
    closed_date:date = None
    date_mat:date = None
    date_fb:date = None
    htparam = l_artikel = l_ophis = l_op = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"num":int, "artnr":int, "bezeich":str, "qty":int, "avrg":decimal, "amt":decimal, "tot_qty":int, "tot_amt":decimal, "del_flag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def create_list(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tot_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()
        sdate = from_date
        edate = to_date

        l_ophis_obj_list = []
        for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                (L_ophis.datum >= sdate) &  (L_ophis.datum <= edate) &  (L_ophis.op_art == 3)).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)

            str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_ophis.artnr), first=True)

            if not str_list:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.artnr = l_artikel.artnr
                str_list.bezeich = l_artikel.bezeich


            str_list.qty[get_month(l_ophis.datum) - 1] = str_list.qty[get_month(l_ophis.datum) - 1] + l_ophis.anzahl
            str_list.amt[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] + l_ophis.warenwert

            if str_list.qty[get_month(l_ophis.datum) - 1] > 0:
                str_list.avrg[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] / str_list.qty[get_month(l_ophis.datum) - 1]
        sdate = closed_date + 1
        edate = to_date

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.datum >= sdate) &  (L_op.datum <= edate) &  (L_op.op_art == 3) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_op.artnr), first=True)

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
                str_list.tot_amt = str_list.tot_amt + str_list.amt[i - 1]
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_qty == 0)):
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

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_amt == 0)):
                str_list_list.remove(str_list)


        if sorttype != 1:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]

    def create_list1(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tot_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()
        sdate = from_date
        edate = to_date

        l_ophis_obj_list = []
        for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum == from_grp)).filter(
                (L_ophis.datum >= sdate) &  (L_ophis.datum <= edate) &  (L_ophis.op_art == 3)).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)

            str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_ophis.artnr), first=True)

            if not str_list:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.artnr = l_artikel.artnr
                str_list.bezeich = l_artikel.bezeich


            str_list.qty[get_month(l_ophis.datum) - 1] = str_list.qty[get_month(l_ophis.datum) - 1] + l_ophis.anzahl
            str_list.amt[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] + l_ophis.warenwert

            if str_list.qty[get_month(l_ophis.datum) - 1] > 0:
                str_list.avrg[get_month(l_ophis.datum) - 1] = str_list.amt[get_month(l_ophis.datum) - 1] / str_list.qty[get_month(l_ophis.datum) - 1]
        sdate = closed_date + 1
        edate = to_date

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).filter(
                (L_op.datum >= sdate) &  (L_op.datum <= edate) &  (L_op.op_art == 3) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_op.artnr), first=True)

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
                str_list.tot_amt = str_list.tot_amt + str_list.amt[i - 1]
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_qty == 0)):
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

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_amt == 0)):
                str_list_list.remove(str_list)


        if sorttype != 1:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]

    def create_list2(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tot_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.op_art == 3) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_op.artnr), first=True)

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
                str_list.tot_amt = str_list.tot_amt + str_list.amt[i - 1]
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_qty == 0)):
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

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_amt == 0)):
                str_list_list.remove(str_list)


        if sorttype != 1:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]

    def create_list3(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, end_date, end_date1, to_date, from_date, datum, closed_date, date_mat, date_fb, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        tot_qty:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tot_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        del_flag:bool = True
        sdate:date = None
        edate:date = None
        str_list_list.clear()

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).filter(
                (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.op_art == 3) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_op.artnr), first=True)

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
                str_list.tot_amt = str_list.tot_amt + str_list.amt[i - 1]
                tot_qty[i - 1] = tot_qty[i - 1] + str_list.qty[i - 1]
                tot_amt[i - 1] = tot_amt[i - 1] + str_list.amt[i - 1]

        if sorttype == 0:

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_qty == 0)):
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

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.tot_amt == 0)):
                str_list_list.remove(str_list)


        if sorttype != 1:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")


            for i in range(1,12 + 1) :
                str_list.qty[i - 1] = tot_qty[i - 1]
                str_list.amt[i - 1] = tot_amt[i - 1]

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    date_mat = fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    date_fb = fdate

    if date_mat > date_fb:
        closed_date = date_mat
    else:
        closed_date = date_fb
    from_date = date_mdy(1, 1, yy)

    if yy % 4 != 0:
        to_date = date_mdy(mm, end_date1[mm - 1], yy)
    else:
        to_date = date_mdy(mm, end_date[mm - 1], yy)

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