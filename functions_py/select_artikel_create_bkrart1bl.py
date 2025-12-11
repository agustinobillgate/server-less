#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rart

bkrart_data, Bkrart = create_model_like(Bk_rart, {"recid_bk_rart":int, "amount":Decimal})

def select_artikel_create_bkrart1bl(veran_nr:int, veran_seite:int, sub_group:int, bkrart_data:[Bkrart]):
    bk_rart = None

    bkrart = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_rart
        nonlocal veran_nr, veran_seite, sub_group


        nonlocal bkrart

        return {}

    for bk_rart in db_session.query(Bk_rart).filter(
             (Bk_rart.veran_nr == veran_nr) & (Bk_rart.veran_seite == veran_seite) & (Bk_rart.zwkum == sub_group)).order_by(Bk_rart._recid).with_for_update().all():
        db_session.delete(bk_rart)

    for bkrart in query(bkrart_data, filters=(lambda bkrart: bkrart.veran_nr == veran_nr and bkrart.veran_seite == veran_seite and bkrart.zwkum == sub_group)):
        bk_rart = Bk_rart()
        db_session.add(bk_rart)

        bk_rart.veran_nr = bkrart.veran_nr
        bk_rart.veran_resnr = bkrart.veran_resnr
        bk_rart.veran_seite = bkrart.veran_seite
        bk_rart.zwkum = bkrart.zwkum
        bk_rart.veran_artnr = bkrart.veran_artnr
        bk_rart.bezeich = bkrart.bezeich
        bk_rart.anzahl = bkrart.anzahl
        bk_rart.preis =  to_decimal(bkrart.preis)
        bk_rart.departement = bkrart.departement
        bk_rart.fakturiert = bkrart.fakturiert
        bk_rart.setup_id = bkrart.setup_id
        bkrart.recid_bk_rart = bk_rart._recid
        bk_rart.von_zeit = bkrart.von_zeit
        bk_rart.raum = bkrart.raum
        bk_rart.resstatus = bkrart.resstatus

        db_session.flush()

    return generate_output()