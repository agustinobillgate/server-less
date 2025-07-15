#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Bediener, Debitor

def view_history4bl(artno:int, rechno:int):

    prepare_cache ([Guest, Bediener])

    balance = to_decimal("0.0")
    debit_list_data = []
    guest = bediener = debitor = None

    debit_list = gast = usr = None

    debit_list_data, Debit_list = create_model("Debit_list", {"artnr":int, "gname":string, "saldo":Decimal, "vesrdep":Decimal, "betrieb_gastmem":int, "zahlkonto":int, "rgdatum":date, "transzeit":int, "userinit":string, "vesrcod":string, "receiver":string})

    Gast = create_buffer("Gast",Guest)
    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, debit_list_data, guest, bediener, debitor
        nonlocal artno, rechno
        nonlocal gast, usr


        nonlocal debit_list, gast, usr
        nonlocal debit_list_data

        return {"balance": balance, "debit-list": debit_list_data}

    debitor_obj_list = {}
    for debitor, gast, usr in db_session.query(Debitor, Gast, Usr).join(Gast,(Gast.gastnr == Debitor.gastnrmember)).join(Usr,(Usr.nr == Debitor.bediener_nr)).filter(
             (Debitor.artnr == artno) & (Debitor.rechnr == rechno)).order_by(Debitor.zahlkonto, Debitor.rgdatum).all():
        if debitor_obj_list.get(debitor._recid):
            continue
        else:
            debitor_obj_list[debitor._recid] = True


        balance =  to_decimal(balance) + to_decimal(debitor.saldo)
        debit_list = Debit_list()
        debit_list_data.append(debit_list)

        buffer_copy(debitor, debit_list)
        debit_list.gname = gast.name
        debit_list.userinit = usr.userinit
        debit_list.receiver = debitor.name

    return generate_output()