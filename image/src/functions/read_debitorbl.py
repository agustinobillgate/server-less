from functions.additional_functions import *
import decimal
from datetime import date
from models import Debitor

def read_debitorbl(case_type:int, artno:int, billno:int, billdate:date, saldo:decimal, inp_opart:int, inp_konto:int):
    t_debitor_list = []
    debitor = None

    t_debitor = None

    t_debitor_list, T_debitor = create_model_like(Debitor, {"tb_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_debitor_list, debitor


        nonlocal t_debitor
        nonlocal t_debitor_list
        return {"t-debitor": t_debitor_list}

    if case_type == 1:

        debitor = db_session.query(Debitor).filter(
                (Debitor.artnr == artno) &  (Debitor.rechnr == billno) &  (Debitor.opart == inp_opart) &  (Debitor.zahlkonto == inp_konto)).first()
    elif case_type == 2:

        debitor = db_session.query(Debitor).filter(
                (Debitor.artnr == artno) &  (Debitor.rechnr == billno) &  (Debitor.opart == inp_opart) &  (Debitor.zahlkonto > inp_konto)).first()
    elif case_type == 3:

        debitor = db_session.query(Debitor).filter(
                (Debitor.artnr == artno) &  (Debitor.rechnr == billno) &  (Debitor.opart == inp_opart) &  (Debitor.zahlkonto == inp_konto)).first()
    elif case_type == 4:

        debitor = db_session.query(Debitor).filter(
                (Debitor.artnr == artno) &  (Debitor.rechnr == billno) &  (Debitor.rgdatum == billdate) &  (Debitor.opart == inp_opart) &  (Debitor.zahlkonto == inp_konto)).first()
    elif case_type == 5:

        debitor = db_session.query(Debitor).filter(
                (Debitor.artnr == artno) &  (Debitor.rechnr == billno) &  (Debitor.rgdatum == billdate) &  (Debitor.saldo == saldo) &  (Debitor.opart == inp_opart) &  (Debitor.zahlkonto == inp_konto)).first()
    elif case_type == 6:

        debitor = db_session.query(Debitor).filter(
                (Debitor.artnr == artno) &  (Debitor.rechnr == billno) &  (Debitor.rgdatum == billdate) &  (Debitor.saldo == - saldo) &  (Debitor.counter == inp_opart)).first()
    elif case_type == 7:

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == artno)).first()
    elif case_type == 8:

        debitor = db_session.query(Debitor).filter(
                (Debitor.counter == inp_opart) &  (Debitor.zahlkonto > 0) &  (Debitor.rgdatum <= billdate)).first()
    elif case_type == 9:

        debitor = db_session.query(Debitor).filter(
                (Debitor.rechnr == billno) &  (Debitor.artnr == artno) &  (Debitor.gastnr == inp_konto) &  (Debitor.gastnrmember == inp_konto) &  (Debitor.rgdatum == billdate) &  (Debitor.saldo == - saldo) &  (Debitor.counter == 0)).first()
    elif case_type == 99:

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == artno)).first()

    if debitor:
        t_debitor = T_debitor()
        t_debitor_list.append(t_debitor)

        buffer_copy(debitor, t_debitor)
        t_debitor.tb_recid = debitor._recid

    return generate_output()