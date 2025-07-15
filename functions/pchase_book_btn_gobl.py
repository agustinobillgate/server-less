#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_lieferant, L_pprice, L_order

def pchase_book_btn_gobl(s_artnr:int):

    prepare_cache ([L_artikel, L_lieferant, L_pprice, L_order])

    pchase_list_data = []
    l_artikel = l_lieferant = l_pprice = l_order = None

    pchase_list = l_art = None

    pchase_list_data, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":string, "docu_nr":string, "traubensort":string, "lief_einheit":Decimal, "betriebsnr":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "remark":string})

    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_data, l_artikel, l_lieferant, l_pprice, l_order
        nonlocal s_artnr
        nonlocal l_art


        nonlocal pchase_list, l_art
        nonlocal pchase_list_data

        return {"pchase-list": pchase_list_data}

    l_pprice_obj_list = {}
    l_pprice = L_pprice()
    l_art = L_artikel()
    l_lieferant = L_lieferant()
    for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
             (L_pprice.artnr == s_artnr)).order_by(L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():
        if l_pprice_obj_list.get(l_pprice._recid):
            continue
        else:
            l_pprice_obj_list[l_pprice._recid] = True


        pchase_list = Pchase_list()
        pchase_list_data.append(pchase_list)

        pchase_list.bestelldatum = l_pprice.bestelldatum
        pchase_list.firma = l_lieferant.firma
        pchase_list.docu_nr = l_pprice.docu_nr
        pchase_list.traubensort = l_art.traubensorte
        pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
        pchase_list.betriebsnr = l_pprice.betriebsnr
        pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
        pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
        pchase_list.warenwert =  to_decimal(l_pprice.warenwert)

        l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

        if l_order:
            pchase_list.remark = l_order.besteller

    return generate_output()