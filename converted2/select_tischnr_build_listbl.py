#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Kellner, Tisch, H_bill

def select_tischnr_build_listbl(dept:int, nr:int):

    prepare_cache ([Kellner, Tisch, H_bill])

    t_list_data = []
    masterkey:bool = False
    kellner = tisch = h_bill = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"tischnr":int, "bezeich":string, "normalbeleg":int, "name":string, "occupied":bool, "belegung":int, "balance":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, masterkey, kellner, tisch, h_bill
        nonlocal dept, nr


        nonlocal t_list
        nonlocal t_list_data

        return {"t-list": t_list_data}

    def build_list():

        nonlocal t_list_data, masterkey, kellner, tisch, h_bill
        nonlocal dept, nr


        nonlocal t_list
        nonlocal t_list_data

        kellner = get_cache (Kellner, {"departement": [(eq, dept)],"kellner_nr": [(eq, nr)]})

        if kellner:
            masterkey = kellner.masterkey

        if masterkey:

            for tisch in db_session.query(Tisch).filter(
                         (Tisch.departement == dept)).order_by(Tisch.tischnr).all():
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.tischnr = tisch.tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg

                h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, tisch.tischnr)],"flag": [(eq, 0)]})

                if h_bill:

                    kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, dept)]})
                    t_list.occupied = True
                    t_list.belegung = h_bill.belegung

                    if kellner:
                        t_list.name = kellner.kellnername
                    t_list.balance =  to_decimal(h_bill.saldo)
        else:

            for tisch in db_session.query(Tisch).filter(
                         (Tisch.departement == dept) & ((Tisch.kellner_nr == 0) | (Tisch.kellner_nr == nr))).order_by(Tisch.tischnr).all():
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.tischnr = tisch.tischnr
                t_list.bezeich = tisch.bezeich
                t_list.normalbeleg = tisch.normalbeleg

                h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, tisch.tischnr)],"flag": [(eq, 0)]})

                if h_bill:

                    kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, dept)]})
                    t_list.occupied = True
                    t_list.belegung = h_bill.belegung

                    if kellner:
                        t_list.name = kellner.kellnername
                    t_list.balance =  to_decimal(h_bill.saldo)

    build_list()

    return generate_output()