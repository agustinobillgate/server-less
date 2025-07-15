#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, H_bill, Tisch, Kellner, Res_line

def opened_tischbl(dept:int):

    prepare_cache ([Hoteldpt, H_bill, Tisch, Kellner, Res_line])

    tot_saldo = to_decimal("0.0")
    t_list_data = []
    hoteldpt = h_bill = tisch = kellner = res_line = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":string, "normalbeleg":int, "name":string, "occupied":bool, "belegung":int, "balance":Decimal, "zinr":string, "gname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_saldo, t_list_data, hoteldpt, h_bill, tisch, kellner, res_line
        nonlocal dept


        nonlocal t_list
        nonlocal t_list_data

        return {"tot_saldo": tot_saldo, "t-list": t_list_data}

    def build_list0():

        nonlocal tot_saldo, t_list_data, hoteldpt, h_bill, tisch, kellner, res_line
        nonlocal dept


        nonlocal t_list
        nonlocal t_list_data

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():

            tisch_obj_list = {}
            tisch = Tisch()
            h_bill = H_bill()
            for tisch.tischnr, tisch.bezeich, tisch.normalbeleg, tisch._recid, h_bill.belegung, h_bill.bilname, h_bill.saldo, h_bill.kellner_nr, h_bill.resnr, h_bill.reslinnr, h_bill._recid in db_session.query(Tisch.tischnr, Tisch.bezeich, Tisch.normalbeleg, Tisch._recid, H_bill.belegung, H_bill.bilname, H_bill.saldo, H_bill.kellner_nr, H_bill.resnr, H_bill.reslinnr, H_bill._recid).join(H_bill,(H_bill.departement == hoteldpt.num) & (H_bill.tischnr == Tisch.tischnr) & (H_bill.flag == 0)).filter(
                     (Tisch.departement == hoteldpt.num)).order_by(Tisch.tischnr).all():
                if tisch_obj_list.get(tisch._recid):
                    continue
                else:
                    tisch_obj_list[tisch._recid] = True


                t_list = T_list()
                t_list_data.append(t_list)

                t_list.dept = hoteldpt.num
                t_list.tischnr = tisch.tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg
                t_list.occupied = True
                t_list.belegung = h_bill.belegung
                t_list.gname = h_bill.bilname
                t_list.balance =  to_decimal(h_bill.saldo)

                kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, hoteldpt.num)]})

                if kellner:
                    t_list.name = kellner.kellnername

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    t_list.zinr = res_line.zinr
                    t_list.gname = res_line.name


                tot_saldo =  to_decimal(tot_saldo) + to_decimal(h_bill.saldo)


    def build_list():

        nonlocal tot_saldo, t_list_data, hoteldpt, h_bill, tisch, kellner, res_line
        nonlocal dept


        nonlocal t_list
        nonlocal t_list_data

        tisch_obj_list = {}
        tisch = Tisch()
        h_bill = H_bill()
        for tisch.tischnr, tisch.bezeich, tisch.normalbeleg, tisch._recid, h_bill.belegung, h_bill.bilname, h_bill.saldo, h_bill.kellner_nr, h_bill.resnr, h_bill.reslinnr, h_bill._recid in db_session.query(Tisch.tischnr, Tisch.bezeich, Tisch.normalbeleg, Tisch._recid, H_bill.belegung, H_bill.bilname, H_bill.saldo, H_bill.kellner_nr, H_bill.resnr, H_bill.reslinnr, H_bill._recid).join(H_bill,(H_bill.departement == dept) & (H_bill.tisch == Tisch.tischnr) & (H_bill.flag == 0)).filter(
                 (Tisch.departement == dept)).order_by(Tisch.tischnr).all():
            if tisch_obj_list.get(tisch._recid):
                continue
            else:
                tisch_obj_list[tisch._recid] = True


            t_list = T_list()
            t_list_data.append(t_list)

            t_list.dept = dept
            t_list.tischnr = tisch.tischnr
            t_list.bezeich = tisch.bezeich
            t_list.normalbeleg = tisch.normalbeleg
            t_list.occupied = True
            t_list.belegung = h_bill.belegung
            t_list.gname = h_bill.bilname
            t_list.balance =  to_decimal(h_bill.saldo)

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, dept)]})

            if kellner:
                t_list.name = kellner.kellnername

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                t_list.zinr = res_line.zinr
                t_list.gname = res_line.name


            tot_saldo =  to_decimal(tot_saldo) + to_decimal(h_bill.saldo)


    if dept > 0:
        build_list()
    else:
        build_list0()

    return generate_output()