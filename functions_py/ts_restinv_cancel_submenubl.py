#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_bill_line, H_journal, H_mjourn

def ts_restinv_cancel_submenubl(hbline_recid:int):

    prepare_cache ([H_artikel, H_bill_line, H_journal, H_mjourn])

    submenu_cancel_list_data = []
    submenu_number:int = 0
    h_artikel = h_bill_line = h_journal = h_mjourn = None

    submenu_cancel_list = h_art2 = None

    submenu_cancel_list_data, Submenu_cancel_list = create_model("Submenu_cancel_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})

    H_art2 = create_buffer("H_art2",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal submenu_cancel_list_data, submenu_number, h_artikel, h_bill_line, h_journal, h_mjourn
        nonlocal hbline_recid
        nonlocal h_art2


        nonlocal submenu_cancel_list, h_art2
        nonlocal submenu_cancel_list_data

        return {"submenu-cancel-list": submenu_cancel_list_data}

    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, hbline_recid)]})

    if h_bill_line:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

        if h_artikel:
            submenu_number = h_artikel.betriebsnr

        h_journal = get_cache (H_journal, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)],"rechnr": [(eq, h_bill_line.rechnr)],"bill_datum": [(eq, h_bill_line.bill_datum)],"zeit": [(eq, h_bill_line.zeit)],"sysdate": [(eq, h_bill_line.sysdate)],"schankbuch": [(eq, hbline_recid)]})

        if h_journal:

            h_mjourn_obj_list = {}
            h_mjourn = H_mjourn()
            h_art2 = H_artikel()
            for h_mjourn.artnr, h_mjourn.anzahl, h_mjourn.zeit, h_mjourn._recid, h_art2.betriebsnr, h_art2._recid, h_art2.bezeich in db_session.query(H_mjourn.artnr, H_mjourn.anzahl, H_mjourn.zeit, H_mjourn._recid, H_art2.betriebsnr, H_art2._recid, H_art2.bezeich).join(H_art2,(H_art2.artnr == H_mjourn.artnr) & (H_art2.departement == H_mjourn.departement)).filter(
                     (H_mjourn.departement == h_journal.departement) & (H_mjourn.h_artnr == h_journal.artnr) & (H_mjourn.rechnr == h_journal.rechnr) & (H_mjourn.bill_datum == h_journal.bill_datum) & (H_mjourn.sysdate == h_journal.sysdate) & (H_mjourn.zeit == h_journal.zeit) & (num_entries(H_mjourn.request, "|") > 1) & (to_int(entry(0, H_mjourn.request, "|")) == hbline_recid)).order_by(H_art2.zwkum, H_art2.bezeich).all():
                if h_mjourn_obj_list.get(h_mjourn._recid):
                    continue
                else:
                    h_mjourn_obj_list[h_mjourn._recid] = True


                submenu_cancel_list = Submenu_cancel_list()
                submenu_cancel_list_data.append(submenu_cancel_list)

                submenu_cancel_list.nr = submenu_number
                submenu_cancel_list.artnr = h_mjourn.artnr
                submenu_cancel_list.anzahl = - h_mjourn.anzahl
                submenu_cancel_list.zeit = h_mjourn.zeit
                submenu_cancel_list.bezeich = h_art2.bezeich

    return generate_output()