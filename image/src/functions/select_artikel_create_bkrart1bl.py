from functions.additional_functions import *
import decimal
from models import Bk_rart

def select_artikel_create_bkrart1bl(veran_nr:int, veran_seite:int, sub_group:int, bkrart:[Bkrart]):
    bk_rart = None

    bkrart = None

    bkrart_list, Bkrart = create_model_like(Bk_rart, {"recid_bk_rart":int, "amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_rart


        nonlocal bkrart
        nonlocal bkrart_list
        return {}

    for bk_rart in db_session.query(Bk_rart).filter(
            (Bk_rart.veran_nr == veran_nr) &  (Bk_rart.veran_seite == veran_seite) &  (Bk_rart.zwkum == sub_group)).all():
        db_session.delete(bk_rart)

    for bkrart in query(bkrart_list, filters=(lambda bkrart :bkrart.veran_nr == veran_nr and bkrart.veran_seite == veran_seite and bkrart.zwkum == sub_group)):
        bk_rart = Bk_rart()
        db_session.add(bk_rart)

        bk_rart.veran_nr = bkrart.veran_nr
        bk_rart.veran_resnr = bkrart.veran_resnr
        bk_rart.veran_seite = bkrart.veran_seite
        bk_rart.zwkum = bkrart.zwkum
        bk_rart.veran_artnr = bkrart.veran_artnr
        bk_rart.bezeich = bkrart.bezeich
        bk_rart.anzahl = bkrart.anzahl
        bk_rart.preis = bkrart.preis
        bk_rart.departement = bkrart.departement
        bk_rart.fakturiert = bkrart.fakturiert
        bk_rart.setup_id = bkrart.setup_id
        bkrart.recid_bk_rart = bk_rart._recid
        bk_rart.von_zeit = bkrart.von_zeit
        bk_rart.raum = bkrart.raum
        bk_rart.resstatus = bkrart.resstatus

    return generate_output()