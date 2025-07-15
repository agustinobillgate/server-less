#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mealcoup, H_bill, H_artikel, H_journal, Res_line

def mealcoup_list_create_list_webbl(curr_month:int, curr_year:int):

    prepare_cache ([H_bill, H_journal, Res_line])

    mlist_data = []
    total_used:int = 0
    total_coupday:List[int] = create_empty_list(31,0)
    count_i:int = 0
    mealcoup = h_bill = h_artikel = h_journal = res_line = None

    mlist = None

    mlist_data, Mlist = create_model_like(Mealcoup)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mlist_data, total_used, total_coupday, count_i, mealcoup, h_bill, h_artikel, h_journal, res_line
        nonlocal curr_month, curr_year


        nonlocal mlist
        nonlocal mlist_data

        return {"mlist": mlist_data}

    def create_list():

        nonlocal mlist_data, total_used, total_coupday, count_i, mealcoup, h_bill, h_artikel, h_journal, res_line
        nonlocal curr_month, curr_year


        nonlocal mlist
        nonlocal mlist_data

        rmno:string = ""
        mlist_data.clear()

        h_journal_obj_list = {}
        for h_journal, h_bill, h_artikel in db_session.query(H_journal, H_bill, H_artikel).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement)).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 12)).filter(
                 (get_month(H_journal.bill_datum) == curr_month) & (get_year(H_journal.bill_datum) == curr_year)).order_by(H_journal.bill_datum).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                rmno = res_line.zinr
            else:
                rmno = ""

            mlist = query(mlist_data, filters=(lambda mlist: mlist.resnr == h_bill.resnr and mlist.zinr == rmno), first=True)

            if not mlist:
                mlist = Mlist()
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


            mlist.verbrauch[get_day(h_journal.bill_datum) - 1] = mlist.verbrauch[get_day(h_journal.bill_datum) - 1] + h_journal.anzahl
            mlist.verbrauch[31] = mlist.verbrauch[31] + h_journal.anzahl

        for mlist in query(mlist_data):
            total_used = total_used + mlist.verbrauch[31]
            total_coupday[0] = total_coupday[0] + mlist.verbrauch[0]
            total_coupday[1] = total_coupday[1] + mlist.verbrauch[1]
            total_coupday[2] = total_coupday[2] + mlist.verbrauch[2]
            total_coupday[3] = total_coupday[3] + mlist.verbrauch[3]
            total_coupday[4] = total_coupday[4] + mlist.verbrauch[4]
            total_coupday[5] = total_coupday[5] + mlist.verbrauch[5]
            total_coupday[6] = total_coupday[6] + mlist.verbrauch[6]
            total_coupday[7] = total_coupday[7] + mlist.verbrauch[7]
            total_coupday[8] = total_coupday[8] + mlist.verbrauch[8]
            total_coupday[9] = total_coupday[9] + mlist.verbrauch[9]
            total_coupday[10] = total_coupday[10] + mlist.verbrauch[10]
            total_coupday[11] = total_coupday[11] + mlist.verbrauch[11]
            total_coupday[12] = total_coupday[12] + mlist.verbrauch[12]
            total_coupday[13] = total_coupday[13] + mlist.verbrauch[13]
            total_coupday[14] = total_coupday[14] + mlist.verbrauch[14]
            total_coupday[15] = total_coupday[15] + mlist.verbrauch[15]
            total_coupday[16] = total_coupday[16] + mlist.verbrauch[16]
            total_coupday[17] = total_coupday[17] + mlist.verbrauch[17]
            total_coupday[18] = total_coupday[18] + mlist.verbrauch[18]
            total_coupday[19] = total_coupday[19] + mlist.verbrauch[19]
            total_coupday[20] = total_coupday[20] + mlist.verbrauch[20]
            total_coupday[21] = total_coupday[21] + mlist.verbrauch[21]
            total_coupday[22] = total_coupday[22] + mlist.verbrauch[22]
            total_coupday[23] = total_coupday[23] + mlist.verbrauch[23]
            total_coupday[24] = total_coupday[24] + mlist.verbrauch[24]
            total_coupday[25] = total_coupday[25] + mlist.verbrauch[25]
            total_coupday[26] = total_coupday[26] + mlist.verbrauch[26]
            total_coupday[27] = total_coupday[27] + mlist.verbrauch[27]
            total_coupday[28] = total_coupday[28] + mlist.verbrauch[28]
            total_coupday[29] = total_coupday[29] + mlist.verbrauch[29]
            total_coupday[30] = total_coupday[30] + mlist.verbrauch[30]

        mlist = query(mlist_data, first=True)

        if mlist:
            mlist = Mlist()
            mlist_data.append(mlist)

            mlist.zinr = "ALL"
            mlist.name = "TOTAL USED:"
            mlist.ankunft = None
            mlist.abreise = None
            mlist.verbrauch[31] = total_used


            for count_i in range(1,31 + 1) :
                mlist.verbrauch[count_i - 1] = total_coupday[count_i - 1]

    create_list()

    return generate_output()