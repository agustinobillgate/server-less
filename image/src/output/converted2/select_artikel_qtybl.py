#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rart, Artikel, Bk_reser, Bk_func

def select_artikel_qtybl(veran_nr:int, veran_seite:int, departement:int, q2_artnr:int, qty:int, bediener_nr:int, selection:int):

    prepare_cache ([Artikel, Bk_reser, Bk_func])

    bkrart_list = []
    bk_rart = artikel = bk_reser = bk_func = None

    bkrart = None

    bkrart_list, Bkrart = create_model_like(Bk_rart, {"recid_bk_rart":int, "amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bkrart_list, bk_rart, artikel, bk_reser, bk_func
        nonlocal veran_nr, veran_seite, departement, q2_artnr, qty, bediener_nr, selection


        nonlocal bkrart
        nonlocal bkrart_list

        return {"bkrart": bkrart_list}

    artikel = get_cache (Artikel, {"artnr": [(eq, q2_artnr)],"departement": [(eq, departement)],"activeflag": [(eq, True)]})

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, veran_nr)],"veran_resnr": [(eq, veran_seite)]})

    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, veran_nr)],"veran_seite": [(eq, veran_seite)]})
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
        bk_rart.preis =  to_decimal(artikel.epreis)
    pass
    bkrart = Bkrart()
    bkrart_list.append(bkrart)

    buffer_copy(bk_rart, bkrart)

    return generate_output()