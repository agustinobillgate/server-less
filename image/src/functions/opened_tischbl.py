from functions.additional_functions import *
import decimal
from models import Hoteldpt, H_bill, Tisch, Kellner, Res_line

def opened_tischbl(dept:int):
    tot_saldo = 0
    t_list_list = []
    hoteldpt = h_bill = tisch = kellner = res_line = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":str, "normalbeleg":int, "name":str, "occupied":bool, "belegung":int, "balance":decimal, "zinr":str, "gname":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_saldo, t_list_list, hoteldpt, h_bill, tisch, kellner, res_line


        nonlocal t_list
        nonlocal t_list_list
        return {"tot_saldo": tot_saldo, "t-list": t_list_list}

    def build_list0():

        nonlocal tot_saldo, t_list_list, hoteldpt, h_bill, tisch, kellner, res_line


        nonlocal t_list
        nonlocal t_list_list

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num > 0)).all():

            tisch_obj_list = []
            for tisch, h_bill in db_session.query(Tisch, H_bill).join(H_bill,(H_bill.departement == hoteldpt.num) &  (H_bill.tisch == Tischnr) &  (H_bill.flag == 0)).filter(
                    (Tisch.departement == hoteldpt.num)).all():
                if tisch._recid in tisch_obj_list:
                    continue
                else:
                    tisch_obj_list.append(tisch._recid)


                t_list = T_list()
                t_list_list.append(t_list)

                t_list.dept = hoteldpt.num
                t_list.tischnr = tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg
                t_list.occupied = True
                t_list.belegung = h_bill.belegung
                t_list.gname = h_bill.bilname
                t_list.balance = h_bill.saldo

                kellner = db_session.query(Kellner).filter(
                        (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == hoteldpt.num)).first()

                if kellner:
                    t_list.name = kellnername

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                if res_line:
                    t_list.zinr = res_line.zinr
                    t_list.gname = res_line.name


                tot_saldo = tot_saldo + h_bill.saldo

    def build_list():

        nonlocal tot_saldo, t_list_list, hoteldpt, h_bill, tisch, kellner, res_line


        nonlocal t_list
        nonlocal t_list_list

        tisch_obj_list = []
        for tisch, h_bill in db_session.query(Tisch, H_bill).join(H_bill,(H_bill.departement == dept) &  (H_bill.tisch == Tischnr) &  (H_bill.flag == 0)).filter(
                (Tisch.departement == dept)).all():
            if tisch._recid in tisch_obj_list:
                continue
            else:
                tisch_obj_list.append(tisch._recid)


            t_list = T_list()
            t_list_list.append(t_list)

            t_list.dept = dept
            t_list.tischnr = tischnr
            t_list.bezeich = tisch.bezeich
            t_list.normalbeleg = tisch.normalbeleg
            t_list.occupied = True
            t_list.belegung = h_bill.belegung
            t_list.gname = h_bill.bilname
            t_list.balance = h_bill.saldo

            kellner = db_session.query(Kellner).filter(
                    (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == dept)).first()

            if kellner:
                t_list.name = kellnername

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

            if res_line:
                t_list.zinr = res_line.zinr
                t_list.gname = res_line.name


            tot_saldo = tot_saldo + h_bill.saldo

    if dept > 0:
        build_list()
    else:
        build_list0()

    return generate_output()