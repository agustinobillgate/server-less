#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import Artikel, Billjournal, H_artikel, H_journal

def gc_cashsummary_webbl(pvilanguage:int, from_date:date, to_date:date):

    prepare_cache ([Artikel, Billjournal, H_artikel, H_journal])

    total_cash_fo = ""
    total_cash_ou = ""
    t_cash_art_data = []
    cash_list_data = []
    lvcarea:string = "gc-cashsummary"
    tot_cash_fo:Decimal = to_decimal("0.0")
    tot_cash_ou:Decimal = to_decimal("0.0")
    p_9900:int = 0
    tot_amount:Decimal = to_decimal("0.0")
    artikel = billjournal = h_artikel = h_journal = None

    cash_list = cash_art = t_cash_art = None

    cash_list_data, Cash_list = create_model("Cash_list", {"flag":int, "datum":date, "artnr":[int,20], "bezeich":[string,20], "amount":[Decimal,20], "str_amount":[string,20], "tot_str_amount":string})
    cash_art_data, Cash_art = create_model("Cash_art", {"pos_nr":int, "datum":date, "artnr":int, "bezeich":string, "amount":Decimal})
    t_cash_art_data, T_cash_art = create_model("T_cash_art", {"artnr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_cash_fo, total_cash_ou, t_cash_art_data, cash_list_data, lvcarea, tot_cash_fo, tot_cash_ou, p_9900, tot_amount, artikel, billjournal, h_artikel, h_journal
        nonlocal pvilanguage, from_date, to_date


        nonlocal cash_list, cash_art, t_cash_art
        nonlocal cash_list_data, cash_art_data, t_cash_art_data

        return {"total_cash_fo": total_cash_fo, "total_cash_ou": total_cash_ou, "t-cash-art": t_cash_art_data, "cash-list": cash_list_data}

    def cash_summ():

        nonlocal total_cash_fo, total_cash_ou, t_cash_art_data, cash_list_data, lvcarea, tot_cash_fo, tot_cash_ou, p_9900, tot_amount, artikel, billjournal, h_artikel, h_journal
        nonlocal pvilanguage, from_date, to_date


        nonlocal cash_list, cash_art, t_cash_art
        nonlocal cash_list_data, cash_art_data, t_cash_art_data

        do_it:bool = False
        i_cash:int = 0
        i:int = 0
        j:int = 0
        loop_date:date = None
        count_date:date = None
        cash_list_data.clear()
        cash_art_data.clear()
        t_cash_art_data.clear()

        billjournal_obj_list = {}
        billjournal = Billjournal()
        artikel = Artikel()
        for billjournal.bill_datum, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.bezeich, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.bezeich, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == 0) & (Artikel.artart == 6)).filter(
                 (Billjournal.bill_datum >= from_date) & (Billjournal.bill_datum <= to_date) & (Billjournal.departement == 0) & (Billjournal.anzahl != 0)).order_by(Billjournal.bill_datum, Billjournal.artnr).all():
            if billjournal_obj_list.get(billjournal._recid):
                continue
            else:
                billjournal_obj_list[billjournal._recid] = True


            do_it = True

            if do_it:

                t_cash_art = query(t_cash_art_data, filters=(lambda t_cash_art: t_cash_art.artnr == artikel.artnr), first=True)

                if not t_cash_art:
                    t_cash_art = T_cash_art()
                    t_cash_art_data.append(t_cash_art)

                    t_cash_art.artnr = artikel.artnr
                    t_cash_art.bezeich = artikel.bezeich

                cash_art = query(cash_art_data, filters=(lambda cash_art: cash_art.artnr == artikel.artnr and cash_art.datum == billjournal.bill_datum), first=True)

                if not cash_art:
                    i_cash = i_cash + 1
                    cash_art = Cash_art()
                    cash_art_data.append(cash_art)

                    cash_art.pos_nr = i_cash
                    cash_art.datum = billjournal.bill_datum
                    cash_art.artnr = artikel.artnr
                    cash_art.bezeich = artikel.bezeich
                    cash_art.amount =  to_decimal(cash_art.amount) + to_decimal(billjournal.betrag)


                else:
                    cash_art.amount =  to_decimal(cash_art.amount) + to_decimal(billjournal.betrag)
                tot_cash_fo =  to_decimal(tot_cash_fo) - to_decimal(billjournal.betrag)

        h_journal_obj_list = {}
        h_journal = H_journal()
        h_artikel = H_artikel()
        for h_journal.bill_datum, h_journal.betrag, h_journal._recid, h_artikel.artnrfront, h_artikel._recid in db_session.query(H_journal.bill_datum, H_journal.betrag, H_journal._recid, H_artikel.artnrfront, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.artnr == p_9900)).order_by(H_journal.bill_datum).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

            if artikel:

                t_cash_art = query(t_cash_art_data, filters=(lambda t_cash_art: t_cash_art.artnr == artikel.artnr), first=True)

                if not t_cash_art:
                    t_cash_art = T_cash_art()
                    t_cash_art_data.append(t_cash_art)

                    t_cash_art.artnr = artikel.artnr
                    t_cash_art.bezeich = artikel.bezeich

                cash_art = query(cash_art_data, filters=(lambda cash_art: cash_art.artnr == h_artikel.artnrfront and cash_art.datum == h_journal.bill_datum), first=True)

                if not cash_art:
                    i_cash = i_cash + 1
                    cash_art = Cash_art()
                    cash_art_data.append(cash_art)

                    cash_art.pos_nr = i_cash
                    cash_art.datum = h_journal.bill_datum
                    cash_art.artnr = artikel.artnr
                    cash_art.bezeich = artikel.bezeich
                    cash_art.amount =  to_decimal(cash_art.amount) + to_decimal(h_journal.betrag)


                else:
                    cash_art.amount =  to_decimal(cash_art.amount) + to_decimal(h_journal.betrag)
                tot_cash_ou =  to_decimal(tot_cash_ou) - to_decimal(h_journal.betrag)
        for count_date in date_range(from_date,to_date) :
            cash_list = Cash_list()
            cash_list_data.append(cash_list)

            cash_list.datum = count_date
            i = 0

            for t_cash_art in query(t_cash_art_data):
                i = i + 1
                cash_list.artnr[i - 1] = t_cash_art.artnr
                cash_list.bezeich[i - 1] = t_cash_art.bezeich

        for cash_list in query(cash_list_data, sort_by=[("datum",False)]):

            for cash_art in query(cash_art_data, filters=(lambda cash_art: cash_art.amount != 0 and cash_art.datum == cash_list.datum)):
                for j in range(1,i + 1) :

                    if cash_list.artnr[j - 1] == cash_art.artnr:
                        cash_list.amount[j - 1] = cash_list.amount[j - 1] + cash_art.amount
                        cash_list.str_amount[j - 1] = to_string(cash_list.amount[j - 1], "->>>,>>>,>>>,>>9.99")


        for i in range(1,20 + 1) :

            for cash_list in query(cash_list_data):
                cash_list.amount[i - 1] = - cash_list.amount[i - 1]
                cash_list.str_amount[i - 1] = to_string(cash_list.amount[i - 1], "->>>,>>>,>>>,>>9.99")

        for cash_list in query(cash_list_data):
            tot_amount =  to_decimal("0")
            tot_amount =  to_decimal(cash_list.amount[0] + cash_list.amount[1] + cash_list.amount[2] + cash_list.amount[3] +\
                    cash_list.amount[4] + cash_list.amount[5] + cash_list.amount[6] + cash_list.amount[7] +\
                    cash_list.amount[8] + cash_list.amount[9] + cash_list.amount[10] + cash_list.amount[11] +\
                    cash_list.amount[12] + cash_list.amount[13] + cash_list.amount[14] + cash_list.amount[15] +\
                    cash_list.amount[16] + cash_list.amount[17] + cash_list.amount[18] + cash_list.amount[19])


            cash_list.tot_str_amount = to_string(tot_amount, "->>>,>>>,>>>,>>9.99")
        total_cash_fo = to_string(tot_cash_fo, "->>>,>>>,>>>,>>9.99")
        total_cash_ou = to_string(tot_cash_ou, "->>>,>>>,>>>,>>9.99")

    p_9900 = get_output(htpint(855))
    cash_summ()

    return generate_output()