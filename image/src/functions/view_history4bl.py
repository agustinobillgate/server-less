from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Bediener, Debitor

def view_history4bl(artno:int, rechno:int):
    balance = 0
    debit_list_list = []
    guest = bediener = debitor = None

    debit_list = gast = usr = None

    debit_list_list, Debit_list = create_model("Debit_list", {"artnr":int, "gname":str, "saldo":decimal, "vesrdep":decimal, "betrieb_gastmem":int, "zahlkonto":int, "rgdatum":date, "transzeit":int, "userinit":str, "vesrcod":str, "receiver":str})

    Gast = Guest
    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, debit_list_list, guest, bediener, debitor
        nonlocal gast, usr


        nonlocal debit_list, gast, usr
        nonlocal debit_list_list
        return {"balance": balance, "debit-list": debit_list_list}

    debitor_obj_list = []
    for debitor, gast, usr in db_session.query(Debitor, Gast, Usr).join(Gast,(Gast.gastnr == Debitor.gastnrmember)).join(Usr,(Usr.nr == Debitor.bediener_nr)).filter(
            (Debitor.artnr == artno) &  (Debitor.rechnr == rechno)).all():
        if debitor._recid in debitor_obj_list:
            continue
        else:
            debitor_obj_list.append(debitor._recid)


        balance = balance + debitor.saldo
        debit_list = Debit_list()
        debit_list_list.append(debit_list)

        buffer_copy(debitor, debit_list)
        debit_list.gname = gast.name
        debit_list.userinit = usr.userinit
        debit_list.receiver = debitor.name

    return generate_output()