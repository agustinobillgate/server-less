#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Bk_veran

def deposit_list_webbl(from_date:date, to_date:date, sorttype:int):

    prepare_cache ([Guest, Bk_veran])

    output_list_data = []
    guest = bk_veran = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"gname":string, "resno":int, "deposit":Decimal, "payment":Decimal, "limit":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, guest, bk_veran
        nonlocal from_date, to_date, sorttype


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_output_list():

        nonlocal output_list_data, guest, bk_veran
        nonlocal from_date, to_date, sorttype


        nonlocal output_list
        nonlocal output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        output_list.resno = bk_veran.veran_nr
        output_list.deposit =  to_decimal(bk_veran.deposit)
        output_list.payment =  to_decimal(bk_veran.total_paid)
        output_list.limit = bk_veran.limit_date

    output_list_data.clear()

    bk_veran_obj_list = {}
    bk_veran = Bk_veran()
    guest = Guest()
    for bk_veran.veran_nr, bk_veran.deposit, bk_veran.total_paid, bk_veran.limit_date, bk_veran._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest._recid in db_session.query(Bk_veran.veran_nr, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran.limit_date, Bk_veran._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest._recid).join(Guest,(Guest.gastnr == Bk_veran.gastnr)).filter(
             (Bk_veran.limit_date >= from_date) & (Bk_veran.limit_date <= to_date)).order_by(Bk_veran._recid).all():
        if bk_veran_obj_list.get(bk_veran._recid):
            continue
        else:
            bk_veran_obj_list[bk_veran._recid] = True

        if sorttype == 0:

            if bk_veran.total_paid < bk_veran.deposit:
                create_output_list()

        elif sorttype == 1:

            if bk_veran.total_paid >= bk_veran.deposit:
                create_output_list()

    return generate_output()