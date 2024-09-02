from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import Artikel, Billjournal, H_artikel, H_journal

def gc_cashsummary_webbl(pvilanguage:int, from_date:date, to_date:date):
    total_cash_fo = ""
    total_cash_ou = ""
    t_cash_art_list = []
    cash_list_list = []
    lvcarea:str = "gc_cashsummary"
    tot_cash_fo:decimal = 0
    tot_cash_ou:decimal = 0
    p_9900:int = 0
    tot_amount:decimal = 0
    artikel = billjournal = h_artikel = h_journal = None

    cash_list = cash_art = t_cash_art = None

    cash_list_list, Cash_list = create_model("Cash_list", {"flag":int, "datum":date, "artnr":[int, 20], "bezeich":[str, 20], "amount":[decimal, 20], "str_amount":[str, 20], "tot_str_amount":str})
    cash_art_list, Cash_art = create_model("Cash_art", {"pos_nr":int, "datum":date, "artnr":int, "bezeich":str, "amount":decimal})
    t_cash_art_list, T_cash_art = create_model("T_cash_art", {"artnr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_cash_fo, total_cash_ou, t_cash_art_list, cash_list_list, lvcarea, tot_cash_fo, tot_cash_ou, p_9900, tot_amount, artikel, billjournal, h_artikel, h_journal


        nonlocal cash_list, cash_art, t_cash_art
        nonlocal cash_list_list, cash_art_list, t_cash_art_list
        return {"total_cash_fo": total_cash_fo, "total_cash_ou": total_cash_ou, "t-cash-art": t_cash_art_list, "cash-list": cash_list_list}

    def cash_summ():

        nonlocal total_cash_fo, total_cash_ou, t_cash_art_list, cash_list_list, lvcarea, tot_cash_fo, tot_cash_ou, p_9900, tot_amount, artikel, billjournal, h_artikel, h_journal


        nonlocal cash_list, cash_art, t_cash_art
        nonlocal cash_list_list, cash_art_list, t_cash_art_list

        do_it:bool = False
        i_cash:int = 0
        i:int = 0
        j:int = 0
        loop_date:date = None
        count_date:date = None
        cash_list_list.clear()
        cash_art_list.clear()
        t_cash_art_list.clear()

        billjournal_obj_list = []
        recs = (
            db_session.query(Billjournal, Artikel)
            .join(Artikel,(Artikel.artnr == Billjournal.artnr) &  (Artikel.departement == 0) &  (Artikel.artart == 6))
            .filter(
                (Billjournal.bill_datum >= from_date) &  
                (Billjournal.bill_datum <= to_date) &  
                (Billjournal.departement == 0) &  
                (Billjournal.anzahl != 0))
            .all()
        )
        for billjournal, artikel in recs:
            if billjournal._recid in billjournal_obj_list:
                continue
            else:
                billjournal_obj_list.append(billjournal._recid)


            do_it = True

            if do_it:

                t_cash_art = query(t_cash_art_list, filters=(lambda t_cash_art :t_cash_art.artnr == artikel.artnr), first=True)

                if not t_cash_art:
                    t_cash_art = T_cash_art()
                    t_cash_art_list.append(t_cash_art)

                    t_cash_art.artnr = artikel.artnr
                    t_cash_art.bezeich = artikel.bezeich

                cash_art = query(cash_art_list, filters=(lambda cash_art :cash_art.artnr == artikel.artnr and cash_art.datum == billjournal.bill_datum), first=True)

                if not cash_art:
                    i_cash = i_cash + 1
                    cash_art = Cash_art()
                    cash_art_list.append(cash_art)

                    cash_art.pos_nr = i_cash
                    cash_art.datum = billjournal.bill_datum
                    cash_art.artnr = artikel.artnr
                    cash_art.bezeich = artikel.bezeich
                    cash_art.amount = cash_art.amount + billjournal.betrag


                else:
                    cash_art.amount = cash_art.amount + billjournal.betrag
                tot_cash_fo = tot_cash_fo - billjournal.betrag

        h_journal_obj_list = []
        for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) &  (H_artikel.departement == H_journal.departement)).filter(
                (H_journal.bill_datum >= from_date) &  (H_journal.bill_datum <= to_date) &  (H_journal.artnr == p_9900)).all():
            if h_journal._recid in h_journal_obj_list:
                continue
            else:
                h_journal_obj_list.append(h_journal._recid)

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == H_artikel.artnrfront) &  (Artikel.departement == 0)).first()

            if artikel:

                t_cash_art = query(t_cash_art_list, filters=(lambda t_cash_art :t_cash_art.artnr == artikel.artnr), first=True)

                if not t_cash_art:
                    t_cash_art = T_cash_art()
                    t_cash_art_list.append(t_cash_art)

                    t_cash_art.artnr = artikel.artnr
                    t_cash_art.bezeich = artikel.bezeich

                cash_art = query(cash_art_list, filters=(lambda cash_art :cash_art.artnr == h_artikel.artnrfront and cash_art.datum == h_journal.bill_datum), first=True)

                if not cash_art:
                    i_cash = i_cash + 1
                    cash_art = Cash_art()
                    cash_art_list.append(cash_art)

                    cash_art.pos_nr = i_cash
                    cash_art.datum = h_journal.bill_datum
                    cash_art.artnr = artikel.artnr
                    cash_art.bezeich = artikel.bezeich
                    cash_art.amount = cash_art.amount + h_journal.betrag


                else:
                    cash_art.amount = cash_art.amount + h_journal.betrag
                tot_cash_ou = tot_cash_ou - h_journal.betrag
        for count_date in date_range(from_date,to_date +  timedelta(days=1)) :
            cash_list = Cash_list()
            cash_list_list.append(cash_list)

            cash_list.datum = count_date
            i = 0

            for t_cash_art in query(t_cash_art_list):
                i = i + 1
                cash_list.artnr[i - 1] = t_cash_art.artnr
                cash_list.bezeich[i - 1] = t_cash_art.bezeich

        for cash_list in query(cash_list_list):

            for cash_art in query(cash_art_list, filters=(lambda cash_art :cash_art.amount != 0 and cash_art.datum == cash_list.datum)):
                for j in range(1,i + 1) :

                    if cash_list.artnr[j - 1] == cash_art.artnr:
                        cash_list.amount[j - 1] = cash_list.amount[j - 1] + cash_art.amount
                        cash_list.str_amount[j - 1] = to_string(cash_list.amount[j - 1], "->>>,>>>,>>>,>>9.99")


        for i in range(1,20 + 1) :

            for cash_list in query(cash_list_list):
                cash_list.amount[i - 1] = - cash_list.amount[i - 1]
                cash_list.str_amount[i - 1] = to_string(cash_list.amount[i - 1], "->>>,>>>,>>>,>>9.99")

        for cash_list in query(cash_list_list):
            tot_amount = 0
            tot_amount = cash_list.amount[0] + cash_list.amount[1] + cash_list.amount[2] + cash_list.amount[3] +\
                    cash_list.amount[4] + cash_list.amount[5] + cash_list.amount[6] + cash_list.amount[7] +\
                    cash_list.amount[8] + cash_list.amount[9] + cash_list.amount[10] + cash_list.amount[11] +\
                    cash_list.amount[12] + cash_list.amount[13] + cash_list.amount[14] + cash_list.amount[15] +\
                    cash_list.amount[16] + cash_list.amount[17] + cash_list.amount[18] + cash_list.amount[19]


            cash_list.tot_str_amount = to_string(tot_amount, "->>>,>>>,>>>,>>9.99")
        total_cash_fo = to_string(tot_cash_fo, "->>>,>>>,>>>,>>9.99")
        total_cash_ou = to_string(tot_cash_ou, "->>>,>>>,>>>,>>9.99")


    p_9900 = get_output(htpint(855))
    cash_summ()

    return generate_output()