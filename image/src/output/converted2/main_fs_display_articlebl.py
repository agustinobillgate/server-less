#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rart, Bk_func, Bk_reser

def main_fs_display_articlebl(b1_resnr:int, resnr:int, resline:int):

    prepare_cache ([Bk_rart, Bk_func, Bk_reser])

    ol_list = []
    t_bkrart_list = []
    status_chr:string = ""
    bk_rart = bk_func = bk_reser = None

    ol = bkrart = t_bkrart = func_buff = None

    ol_list, Ol = create_model("Ol", {"str":string})
    bkrart_list, Bkrart = create_model_like(Bk_rart, {"tischform":string, "amount":Decimal})
    t_bkrart_list, T_bkrart = create_model_like(Bkrart)

    Func_buff = create_buffer("Func_buff",Bk_func)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ol_list, t_bkrart_list, status_chr, bk_rart, bk_func, bk_reser
        nonlocal b1_resnr, resnr, resline
        nonlocal func_buff


        nonlocal ol, bkrart, t_bkrart, func_buff
        nonlocal ol_list, bkrart_list, t_bkrart_list

        return {"ol": ol_list, "t-bkrart": t_bkrart_list}

    def create_bkrart():

        nonlocal ol_list, t_bkrart_list, status_chr, bk_rart, bk_func, bk_reser
        nonlocal b1_resnr, resnr, resline
        nonlocal func_buff


        nonlocal ol, bkrart, t_bkrart, func_buff
        nonlocal ol_list, bkrart_list, t_bkrart_list


        bkrart_list.clear()

        for bk_rart in db_session.query(Bk_rart).filter(
                 (Bk_rart.veran_nr == b1_resnr) & (Bk_rart.veran_seite == resline)).order_by(Bk_rart._recid).all():
            bkrart = Bkrart()
            bkrart_list.append(bkrart)

            bkrart.veran_nr = bk_rart.veran_nr
            bkrart.veran_seite = bk_rart.veran_seite
            bkrart.von_zeit = bk_rart.von_zeit
            bkrart.raum = bk_rart.raum
            bkrart.departement = bk_rart.departement
            bkrart.veran_artnr = bk_rart.veran_artnr
            bkrart.bezeich = bk_rart.bezeich
            bkrart.anzahl = bk_rart.anzahl
            bkrart.preis =  to_decimal(bk_rart.preis)
            bkrart.amount = ( to_decimal(bk_rart.anzahl) * to_decimal(bk_rart.preis) )
            bkrart.resstatus = bk_rart.resstatus
            bkrart.setup_id = bk_rart.setup_id
            bkrart.zwkum = bk_rart.zwkum
            bkrart.fakturiert = bk_rart.fakturiert

    ol_list.clear()

    bk_rart = get_cache (Bk_rart, {"veran_nr": [(eq, b1_resnr)],"veran_resnr": [(eq, resline)]})

    if bk_rart:

        if bk_rart.resstatus == 1:
            status_chr = "Fix"

        elif bk_rart.resstatus == 2:
            status_chr = "Tentative"

        elif bk_rart.resstatus == 3:
            status_chr = "Waiting List"

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, resline)]})

        for bk_rart in db_session.query(Bk_rart).filter(
                 (Bk_rart.veran_nr == resnr) & (Bk_rart.veran_resnr == resline)).order_by(Bk_rart._recid).all():
            ol = Ol()
            ol_list.append(ol)

            ol.str = to_string(bk_reser.von_zeit, "99:99") + to_string(bk_reser.bis_zeit, "99:99") + to_string(bk_rart.raum, "x(15)") + to_string(bk_rart.veran_nr, ">>>,>>9") + to_string(bk_rart.bezeich, "x(30)") + to_string(bk_rart.anzahl, ">>>,>>9") + to_string(bk_rart.preis, ">>>,>>>,>>9.99") + to_string(status_chr, "x(10)") + to_string(bk_rart.bemerkung, "x(2)")
    create_bkrart()

    for bkrart in query(bkrart_list):

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, bkrart.veran_nr)],"veran_seite": [(eq, bkrart.veran_seite)]})

        if bk_func:
            t_bkrart = T_bkrart()
            t_bkrart_list.append(t_bkrart)

            buffer_copy(bkrart, t_bkrart)
            t_bkrart.tischform = bk_func.tischform[0]

    return generate_output()