from functions.additional_functions import *
import decimal
from models import Htparam, Tisch, H_bill

def prepare_ts_helptischbl(dept:int):
    tablestr = ""
    max_pos = 0
    t_list_list = []
    htparam = tisch = h_bill = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"pos":int, "tischnr":int, "beleg":bool, "balance":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tablestr, max_pos, t_list_list, htparam, tisch, h_bill


        nonlocal t_list
        nonlocal t_list_list
        return {"tablestr": tablestr, "max_pos": max_pos, "t-list": t_list_list}

    def build_list():

        nonlocal tablestr, max_pos, t_list_list, htparam, tisch, h_bill


        nonlocal t_list
        nonlocal t_list_list

        i:int = 0

        for tisch in db_session.query(Tisch).filter(
                (Tisch.departement == dept)).all():

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.tischnr == tischnr) &  (H_bill.departement == dept) &  (H_bill.flag == 0)).first()
            i = i + 1
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.pos = i
            t_list.tischnr = tischnr

            if h_bill:
                t_list.beleg = True
                t_list.balance = h_bill.saldo
        max_pos = i

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1007)).first()

    if htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 200)).first()

        if htparam.finteger == dept:
            tablestr = "Cabin:"
    build_list()

    return generate_output()