#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mealcoup, H_bill, H_artikel, H_journal, Res_line

def mealcoup_list_create_listbl(from_date:date, to_date:date):

    prepare_cache ([H_bill, H_journal, Res_line])

    mlist_list = []
    mealcoup = h_bill = h_artikel = h_journal = res_line = None

    mlist = None

    mlist_list, Mlist = create_model_like(Mealcoup)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mlist_list, mealcoup, h_bill, h_artikel, h_journal, res_line
        nonlocal from_date, to_date


        nonlocal mlist
        nonlocal mlist_list

        return {"mlist": mlist_list}

    def create_list():

        nonlocal mlist_list, mealcoup, h_bill, h_artikel, h_journal, res_line
        nonlocal from_date, to_date


        nonlocal mlist
        nonlocal mlist_list

        rmno:string = ""
        mlist_list.clear()

        h_journal_obj_list = {}
        for h_journal, h_bill, h_artikel in db_session.query(H_journal, H_bill, H_artikel).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement)).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_journal.departement == H_artikel.departement) & (H_artikel.artart == 12)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(H_journal.bill_datum).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                rmno = res_line.zinr
            else:
                rmno = ""

            mlist = query(mlist_list, filters=(lambda mlist: mlist.resnr == h_bill.resnr and mlist.zinr == rmno), first=True)

            if not mlist:
                mlist = Mlist()
                mlist_list.append(mlist)

                mlist.resnr = h_bill.resnr
                mlist.zinr = rmno
                mlist.name = h_bill.bilname


                if res_line:
                    mlist.ankunft = res_line.ankunft
                    mlist.abreise = res_line.abreise


            mlist.verbrauch[get_day(h_journal.bill_datum) - 1] = h_journal.anzahl
            mlist.verbrauch[31] = mlist.verbrauch[31] + h_journal.anzahl

    create_list()

    return generate_output()