#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_bill_line, H_journal, H_mjourn

def ts_restinv_show_submenubl(rec_id:int):

    prepare_cache ([H_artikel, H_bill_line, H_journal, H_mjourn])

    q2_list_data = []
    h_artikel = h_bill_line = h_journal = h_mjourn = None

    h_art2 = q2_list = None

    q2_list_data, Q2_list = create_model("Q2_list", {"bezeich":string, "request":string, "zwkum":int})

    H_art2 = create_buffer("H_art2",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_data, h_artikel, h_bill_line, h_journal, h_mjourn
        nonlocal rec_id
        nonlocal h_art2


        nonlocal h_art2, q2_list
        nonlocal q2_list_data

        return {"q2-list": q2_list_data}

    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, rec_id)]})

    if h_bill_line:

        h_journal = get_cache (H_journal, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)],"rechnr": [(eq, h_bill_line.rechnr)],"bill_datum": [(eq, h_bill_line.bill_datum)],"zeit": [(eq, h_bill_line.zeit)],"sysdate": [(eq, h_bill_line.sysdate)],"schankbuch": [(eq, rec_id)]})

        if h_journal:

            h_mjourn_obj_list = {}
            h_mjourn = H_mjourn()
            h_art2 = H_artikel()
            for h_mjourn.request, h_mjourn._recid, h_art2.bezeich, h_art2._recid in db_session.query(H_mjourn.request, H_mjourn._recid, H_art2.bezeich, H_art2._recid).join(H_art2,(H_art2.artnr == H_mjourn.artnr) & (H_art2.departement == H_mjourn.departement)).filter(
                     (H_mjourn.departement == h_journal.departement) & (H_mjourn.h_artnr == h_journal.artnr) & (H_mjourn.rechnr == h_journal.rechnr) & (H_mjourn.bill_datum == h_journal.bill_datum) & (H_mjourn.sysdate == h_journal.sysdate) & (H_mjourn.zeit == h_journal.zeit) & (num_entries(H_mjourn.request, "|") > 1) & (to_int(entry(0, H_mjourn.request, "|")) == rec_id)).order_by(H_art2.zwkum, H_art2.bezeich).all():
                if h_mjourn_obj_list.get(h_mjourn._recid):
                    continue
                else:
                    h_mjourn_obj_list[h_mjourn._recid] = True

                if num_entries(h_mjourn.request, "|") > 1 and to_int(entry(0, h_mjourn.request, "|")) == rec_id:
                    q2_list = Q2_list()
                    q2_list_data.append(q2_list)

                    q2_list.bezeich = h_art2.bezeich
                    q2_list.request = entry(1, h_mjourn.request, "|")


                else:
                    q2_list = Q2_list()
                    q2_list_data.append(q2_list)

                    q2_list.bezeich = h_art2.bezeich
                    q2_list.request = h_mjourn.request

    return generate_output()