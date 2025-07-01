#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rart

def select_artikel_create_bkrartbl(veran_nr:int, veran_seite:int, sub_group:int):

    prepare_cache ([Bk_rart])

    bkrart_list = []
    bk_rart = None

    bkrart = None

    bkrart_list, Bkrart = create_model_like(Bk_rart, {"recid_bk_rart":int, "amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bkrart_list, bk_rart
        nonlocal veran_nr, veran_seite, sub_group


        nonlocal bkrart
        nonlocal bkrart_list

        return {"bkrart": bkrart_list}


    bkrart_list.clear()

    for bk_rart in db_session.query(Bk_rart).filter(
             (Bk_rart.veran_nr == veran_nr) & (Bk_rart.veran_seite == veran_seite) & (Bk_rart.zwkum == sub_group)).order_by(Bk_rart._recid).all():
        bkrart = Bkrart()
        bkrart_list.append(bkrart)

        bkrart.veran_nr = bk_rart.veran_nr
        bkrart.veran_resnr = bk_rart.veran_resnr
        bkrart.veran_seite = bk_rart.veran_seite
        bkrart.zwkum = bk_rart.zwkum
        bkrart.veran_artnr = bk_rart.veran_artnr
        bkrart.bezeich = bk_rart.bezeich
        bkrart.anzahl = bk_rart.anzahl
        bkrart.preis =  to_decimal(bk_rart.preis)
        bkrart.amount = ( to_decimal(bk_rart.anzahl) * to_decimal(bk_rart.preis) )
        bkrart.departement = bk_rart.departement
        bkrart.fakturiert = bk_rart.fakturiert
        bkrart.setup_id = bk_rart.setup_id
        bkrart.recid_bk_rart = bk_rart._recid
        bkrart.von_zeit = bk_rart.von_zeit
        bkrart.raum = bk_rart.raum
        bkrart.resstatus = bk_rart.resstatus

    return generate_output()