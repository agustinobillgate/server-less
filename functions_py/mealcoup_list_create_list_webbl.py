# using conversion tools version: 1.0.0.117

# =================================================================
# Rulita, 01-10-2025
# Fixing nilai mealcoup selalu menambah jika di hit terus menerus
# =================================================================

from functions.additional_functions import *
from decimal import Decimal
from models import Mealcoup, H_bill, H_artikel, H_journal, Res_line
# from typing import List

def mealcoup_list_create_list_webbl(curr_month:int, curr_year:int):

    prepare_cache([H_bill, H_journal, Res_line])

    _existing_list, Mlist = create_model_like(Mealcoup)

    mlist_data: List = []
    total_used:int = 0
    total_coupday:List[int] = create_empty_list(31, 0)
    count_i:int = 0
    mealcoup = h_bill = h_artikel = h_journal = res_line = None
    mlist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mlist_data, total_used, total_coupday, count_i, mealcoup, h_bill, h_artikel, h_journal, res_line
        nonlocal curr_month, curr_year
        nonlocal mlist
        return {"mlist": mlist_data}

    def create_list():
        nonlocal mlist_data, total_used, total_coupday, count_i, mealcoup, h_bill, h_artikel, h_journal, res_line
        nonlocal curr_month, curr_year
        nonlocal mlist

        rmno: str = ""

        #clear data
        mlist_data.clear()

        h_journal_obj_list = {}

        for h_journal, h_bill, h_artikel in (
            db_session.query(H_journal, H_bill, H_artikel)
            .join(H_bill, (H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement))
            .join(H_artikel, (H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 12))
            .filter((get_month(H_journal.bill_datum) == curr_month) & (get_year(H_journal.bill_datum) == curr_year))
            .order_by(H_journal.bill_datum)
            .all()
        ):
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True

            res_line = get_cache(Res_line, {"resnr": [(eq, h_bill.resnr)], "reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                rmno = res_line.zinr
            else:
                rmno = ""

            mlist = query(mlist_data, filters=(lambda m: m.resnr == h_bill.resnr and m.zinr == rmno), first=True)

            if not mlist:
                mlist = Mlist()

                # Memastikan instance listnya baru
                try:
                    mlist.verbrauch = [0] * 32
                except Exception:
                    pass

                mlist_data.append(mlist)

                mlist.resnr = h_bill.resnr
                mlist.zinr = rmno
                mlist.name = h_bill.bilname

                if res_line:
                    mlist.ankunft = res_line.ankunft
                    mlist.abreise = res_line.abreise

                if rmno == "":
                    mlist.name = "[OUTSIDER]"
                    mlist.ankunft = None
                    mlist.abreise = None

            # Update konsumsi per hari + total baris 31 (index 31)
            day_idx = get_day(h_journal.bill_datum) - 1
            if 0 <= day_idx < 31:
                mlist.verbrauch[day_idx] = mlist.verbrauch[day_idx] + h_journal.anzahl
            mlist.verbrauch[31] = mlist.verbrauch[31] + h_journal.anzahl

        # Agregasi total (tetap mirip pola asli, tapi diringkas agar aman)
        for row in query(mlist_data):
            total_used = total_used + row.verbrauch[31]
            for i in range(31):
                total_coupday[i] = total_coupday[i] + row.verbrauch[i]

        # Tambah baris tot jika ada data
        if query(mlist_data, first=True):
            tot = Mlist()
            try:
                tot.verbrauch = [0] * 32
            except Exception:
                pass
            tot.zinr = "ALL"
            tot.name = "TOTAL USED:"
            tot.ankunft = None
            tot.abreise = None
            tot.verbrauch[31] = total_used

            for count_i in range(1, 31 + 1):
                tot.verbrauch[count_i - 1] = total_coupday[count_i - 1]

            mlist_data.append(tot)

    create_list()
    return generate_output()
