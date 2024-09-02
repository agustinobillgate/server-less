from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_artikel, L_ophis, L_op

def rcv_annual_btn_gobl(pvilanguage:int, from_grp:int, mm:int, yy:int, sorttype:int):
    str_list_list = []
    lvcarea:str = "rcv_annual"
    htparam = l_artikel = l_ophis = l_op = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"num":int, "artnr":int, "bezeich":str, "qty":int, "avrg":decimal, "amt":decimal, "tot_qty":int, "tot_amt":decimal, "del_flag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, lvcarea, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def create_list(mm:int, yy:int):

        nonlocal str_list_list, lvcarea, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        to_date:date = None
        from_date:date = None
        datum:date = None
        closed_date:date = None
        date_mat:date = None
        date_fb:date = None
        tot_qty:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tot_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        del_flag:bool = True

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
        str_list_list.clear()
        for i in range(9,9 + 1) :
            from_date = date_mdy(i, 1, yy)
            to_date = date_mdy(i + 1, 1, yy)
            to_date = to_date - 1
            for datum in range(from_date,to_date + 1) :

                if datum <= closed_date:

                    l_ophis_obj_list = []
                    for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                            (L_ophis.datum == datum) &  (L_ophis.op_art == 1)).all():
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


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_ophis.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_ophis.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]

                else:

                    l_op_obj_list = []
                    for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                            (L_op.datum == datum) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1)).all():
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


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_op.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_op.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]

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

        nonlocal str_list_list, lvcarea, htparam, l_artikel, l_ophis, l_op


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        to_date:date = None
        from_date:date = None
        datum:date = None
        closed_date:date = None
        date_mat:date = None
        date_fb:date = None
        tot_qty:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tot_amt:[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        del_flag:bool = True

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
        str_list_list.clear()
        for i in range(1,mm + 1) :
            from_date = date_mdy(i, 1, yy)
            to_date = from_date + 32
            to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
            for datum in range(from_date,to_date + 1) :

                if datum <= closed_date:

                    l_ophis_obj_list = []
                    for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum == from_grp)).filter(
                            (L_ophis.datum == datum) &  (L_ophis.op_art == 1)).all():
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


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_ophis.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_ophis.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]

                else:

                    l_op_obj_list = []
                    for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).filter(
                            (L_op.datum == datum) &  (L_op.op_art == 1) &  (L_op.loeschflag < 2)).all():
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


                        str_list.qty[i - 1] = str_list.qty[i - 1] + l_op.anzahl
                        str_list.amt[i - 1] = str_list.amt[i - 1] + l_op.warenwert

                        if str_list.qty[i - 1] > 0:
                            str_list.avrg[i - 1] = str_list.amt[i - 1] / str_list.qty[i - 1]


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

    if from_grp == 0:
        create_list(mm, yy)
    else:
        create_list1(mm, yy)

    return generate_output()