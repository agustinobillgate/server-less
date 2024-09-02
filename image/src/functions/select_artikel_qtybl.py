from functions.additional_functions import *
import decimal
from models import Bk_rart, Artikel, Bk_reser, Bk_func

def select_artikel_qtybl(veran_nr:int, veran_seite:int, departement:int, q2_artnr:int, qty:int, bediener_nr:int, selection:int):
    bkrart_list = []
    bk_rart = artikel = bk_reser = bk_func = None

    bkrart = None

    bkrart_list, Bkrart = create_model_like(Bk_rart, {"recid_bk_rart":int, "amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bkrart_list, bk_rart, artikel, bk_reser, bk_func


        nonlocal bkrart
        nonlocal bkrart_list
        return {"bkrart": bkrart_list}

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == q2_artnr) &  (Artikel.departement == departement) &  (Artikel.activeflag)).first()

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == veran_nr) &  (Bk_reser.veran_resnr == veran_seite)).first()

    bk_func = db_session.query(Bk_func).filter(
            (Bk_func.veran_nr == veran_nr) &  (Bk_func.veran_seite == veran_seite)).first()
    bk_rart = Bk_rart()
    db_session.add(bk_rart)

    bk_rart.veran_nr = bk_reser.veran_nr
    bk_rart.veran_resnr = bk_func.veran_seite
    bk_rart.veran_seite = bk_func.veran_seite
    bk_rart.von_zeit = bk_reser.von_zeit
    bk_rart.raum = bk_reser.raum
    bk_rart.departement = departement
    bk_rart.veran_artnr = artikel.artnr
    bk_rart.bezeich = artikel.bezeich
    bk_rart.anzahl = qty
    bk_rart.resstatus = bk_reser.resstatus
    bk_rart.zwkum = artikel.zwkum
    bk_rart.setup_id = bediener_nr

    if selection == 1:
        bk_rart.preis = artikel.epreis

    bk_rart = db_session.query(Bk_rart).first()
    bkrart = Bkrart()
    bkrart_list.append(bkrart)

    buffer_copy(bk_rart, bkrart)

    return generate_output()