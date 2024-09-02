from functions.additional_functions import *
import decimal
from models import Kellner, Tisch, H_bill

def select_tischnr_build_listbl(dept:int, nr:int):
    t_list_list = []
    masterkey:bool = False
    kellner = tisch = h_bill = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"tischnr":int, "bezeich":str, "normalbeleg":int, "name":str, "occupied":bool, "belegung":int, "balance":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, masterkey, kellner, tisch, h_bill


        nonlocal t_list
        nonlocal t_list_list
        return {"t-list": t_list_list}

    def build_list():

        nonlocal t_list_list, masterkey, kellner, tisch, h_bill


        nonlocal t_list
        nonlocal t_list_list

        kellner = db_session.query(Kellner).filter(
                (Kellner.departement == dept) &  (Kellner_nr == nr)).first()

        if kellner:
            masterkey = kellner.masterkey

        if masterkey:

            for tisch in db_session.query(Tisch).filter(
                        (Tisch.departement == dept)).all():
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.tischnr = tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg

                h_bill = db_session.query(H_bill).filter(
                            (H_bill.departement == dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()

                if h_bill:

                    kellner = db_session.query(Kellner).filter(
                                (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == dept)).first()
                    t_list.occupied = True
                    t_list.belegung = h_bill.belegung

                    if kellner:
                        t_list.name = kellnername
                    t_list.balance = h_bill.saldo
        else:

            for tisch in db_session.query(Tisch).filter(
                        (Tisch.departement == dept) &  ((Tisch.kellner_nr == 0) |  (Tisch.kellner_nr == nr))).all():
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.tischnr = tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg

                h_bill = db_session.query(H_bill).filter(
                            (H_bill.departement == dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()

                if h_bill:

                    kellner = db_session.query(Kellner).filter(
                                (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == dept)).first()
                    t_list.occupied = True
                    t_list.belegung = h_bill.belegung

                    if kellner:
                        t_list.name = kellnername
                    t_list.balance = h_bill.saldo


    build_list()

    return generate_output()