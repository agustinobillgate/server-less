from functions.additional_functions import *
import decimal

def fo_daysale_daysale_list_webbl(bline_list:[Bline_list], summary1:[Summary1], cash_art:[Cash_art]):
    label_list = ""
    summary_list_list = []
    i:int = 0

    bline_list = cash_art = summary1 = summary_list = cbuff = None

    bline_list_list, Bline_list = create_model("Bline_list", {"flag":int, "userinit":str, "selected":bool, "name":str, "bl_recid":int})
    cash_art_list, Cash_art = create_model("Cash_art", {"pos_nr":int, "artnr":int, "bezeich":str, "amount":decimal, "tamount":decimal})
    summary1_list, Summary1 = create_model("Summary1", {"usrinit":str, "username":str, "artnr":int, "amount":decimal})
    summary_list_list, Summary_list = create_model("Summary_list", {"username":str, "price":[decimal, 20], "total_price":decimal})

    Cbuff = Cash_art
    cbuff_list = cash_art_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal label_list, summary_list_list, i
        nonlocal cbuff


        nonlocal bline_list, cash_art, summary1, summary_list, cbuff
        nonlocal bline_list_list, cash_art_list, summary1_list, summary_list_list
        return {"label_list": label_list, "summary-list": summary_list_list}

    def daysale_list():

        nonlocal label_list, summary_list_list, i
        nonlocal cbuff


        nonlocal bline_list, cash_art, summary1, summary_list, cbuff
        nonlocal bline_list_list, cash_art_list, summary1_list, summary_list_list

        str1:str = ""
        ttl:decimal = 0
        gttl:decimal = 0
        counter:int = 0

        summary1 = query(summary1_list, first=True)

        if not summary1:

            return

        for cash_art in query(cash_art_list):
            counter = counter + 1
            label_list[counter - 1] = cash_art.bezeich

        for bline_list in query(bline_list_list, filters=(lambda bline_list :bline_list.SELECTED)):

            for cash_art in query(cash_art_list):
                cash_art.amount = 0

            for cash_art in query(cash_art_list):

                summary1 = query(summary1_list, filters=(lambda summary1 :summary1.artnr == cash_art.artnr and summary1.usrinit == bline_list.userinit), first=True)

                if summary1:

                    cbuff = query(cbuff_list, filters=(lambda cbuff :cbuff._recid == cash_art._recid), first=True)
                    cbuff.amount = summary1.amount
                    cbuff.tamount = cbuff.tamount + summary1.amount

            cbuff = query(cbuff_list, filters=(lambda cbuff :cbuff.amount != 0), first=True)

            if cbuff:
                summary_list = Summary_list()
                summary_list_list.append(summary_list)

                summary_list.username = bline_list.name
                ttl = 0
                counter = 0

                for cash_art in query(cash_art_list):
                    counter = counter + 1
                    summary_list.price[counter - 1] = cash_art.amount
                    ttl = ttl + cash_art.amount
                    gttl = gttl + cash_art.amount
                summary_list.total_price = ttl
        summary_list = Summary_list()
        summary_list_list.append(summary_list)

        summary_list = Summary_list()
        summary_list_list.append(summary_list)

        summary_list.username = "G_TOTAL"


        counter = 0

        for cash_art in query(cash_art_list):
            counter = counter + 1
            summary_list.price[counter - 1] = cash_art.tamount
        summary_list.total_price = gttl

    daysale_list()

    return generate_output()