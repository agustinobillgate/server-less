#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, Htparam, Waehrung, H_bill

def prepare_ts_disc1_1bl(dept:int, tischnr:int):

    prepare_cache ([Htparam, Waehrung, H_bill])

    price_decimal = 0
    exchg_rate = to_decimal("0.0")
    p_134 = False
    p_135 = False
    p_479 = False
    t_h_bill_line_data = []
    h_bill_line = htparam = waehrung = h_bill = None

    t_h_bill_line = void_items = hbline = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line)
    void_items_data, Void_items = create_model("Void_items", {"artnr":int, "anzahl":int, "betrag":Decimal, "dept":int})

    Hbline = create_buffer("Hbline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, exchg_rate, p_134, p_135, p_479, t_h_bill_line_data, h_bill_line, htparam, waehrung, h_bill
        nonlocal dept, tischnr
        nonlocal hbline


        nonlocal t_h_bill_line, void_items, hbline
        nonlocal t_h_bill_line_data, void_items_data

        return {"price_decimal": price_decimal, "exchg_rate": exchg_rate, "p_134": p_134, "p_135": p_135, "p_479": p_479, "t-h-bill-line": t_h_bill_line_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam:

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


        else:
            exchg_rate =  to_decimal("1")

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, tischnr)],"flag": [(eq, 0)]})

    if h_bill:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept) & (H_bill_line.betrag < 0) & (H_bill_line.anzahl < 0) & (H_bill_line.epreis > 0)).order_by(H_bill_line.bezeich).all():
            void_items = Void_items()
            void_items_data.append(void_items)

            void_items.artnr = h_bill_line.artnr
            void_items.anzahl = h_bill_line.anzahl
            void_items.betrag =  to_decimal(h_bill_line.betrag)
            void_items.dept = h_bill_line.departement

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept) & (H_bill_line.anzahl > 0)).order_by(H_bill_line.bezeich).all():

            void_items = query(void_items_data, filters=(lambda void_items: void_items.artnr == h_bill_line.artnr and void_items.dept == h_bill_line.departement and void_items.betrag == - (h_bill_line.betrag) and void_items.anzahl == - (h_bill_line.anzahl)), first=True)

            if not void_items:
                t_h_bill_line = T_h_bill_line()
                t_h_bill_line_data.append(t_h_bill_line)

                buffer_copy(h_bill_line, t_h_bill_line)
            else:
                pass
                void_items_data.remove(void_items)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

    if htparam:
        p_134 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

    if htparam:
        p_135 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

    if htparam:
        p_479 = htparam.flogical

    return generate_output()