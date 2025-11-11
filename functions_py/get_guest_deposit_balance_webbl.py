#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 13/8/2025
# num_entries
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Artikel, Guest, Billjournal, Bill_line, Bill

def get_guest_deposit_balance_webbl(guest_number:int):

    prepare_cache ([Htparam, Artikel, Guest, Bill_line])

    gdeposit_list_data = []
    depoart_guest:int = 0
    depobez_guest:string = ""
    depoart_rsv:int = 0
    depoart_bqt:int = 0
    depoart_pos:int = 0
    depo_balance:Decimal = to_decimal("0.0")
    htparam = artikel = guest = billjournal = bill_line = bill = None

    gdeposit_list = None

    gdeposit_list_data, Gdeposit_list = create_model("Gdeposit_list", {"gdeposit_balance":Decimal, "guest_deposit_num":int, "guest_type":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gdeposit_list_data, depoart_guest, depobez_guest, depoart_rsv, depoart_bqt, depoart_pos, depo_balance, htparam, artikel, guest, billjournal, bill_line, bill
        nonlocal guest_number


        nonlocal gdeposit_list
        nonlocal gdeposit_list_data

        return {"gdeposit-list": gdeposit_list_data}


    gdeposit_list = Gdeposit_list()
    gdeposit_list_data.append(gdeposit_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1068)]})

    if htparam:
        gdeposit_list.guest_deposit_num = htparam.finteger

        # artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0)).first()

        if artikel and artikel.artart == 5:
            depoart_guest = artikel.artnr
            depobez_guest = artikel.bezeich

    # guest = get_cache (Guest, {"gastnr": [(eq, guest_number)]})
    guest = db_session.query(Guest).filter(
             (Guest.gastnr == guest_number)).first()

    if guest:

        if guest.karteityp == 0:
            gdeposit_list.guest_type = "Individual"

        elif guest.karteityp == 1:
            gdeposit_list.guest_type = "Company"
        else:
            gdeposit_list.guest_type = "Travel Agent"

    if gdeposit_list.guest_deposit_num != 0 and gdeposit_list.guest_type  != ("Individual") :

        htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

        if htparam:
            depoart_rsv = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 117)]})

        if htparam:
            depoart_bqt = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

        if htparam:
            depoart_pos = htparam.finteger

        # Rd, 13/8/2025
        # billjournal = db_session.query(Billjournal).filter(
        #          (Billjournal.billjou_ref == guest_number) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit"))).first()
        billjournal = db_session.query(Billjournal).filter(
                 (Billjournal.billjou_ref == guest_number) & 
                 (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & 
                 (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & 
                 (Billjournal.artnr != depoart_pos) & 
                 (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit"))).first()

        if billjournal:
            if (num_entries(billjournal.bezeich, "[") > 1):
                # Rd, 13/8/2025
                # billjournal = db_session.query(Billjournal).filter(
                #         (Billjournal.billjou_ref == guest_number) & 
                #         (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & 
                #         (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & 
                #         (Billjournal.artnr != depoart_pos) & 
                #         (num_entries(Billjournal.bezeich, "[") > 1) & 
                #         (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit"))).first()
                billjournal = db_session.query(Billjournal).filter(
                        (Billjournal.billjou_ref == guest_number) & 
                        (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & 
                        (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & 
                        (Billjournal.artnr != depoart_pos) & 
                        (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit"))).first()

                while None != billjournal:
                    if (num_entries(Billjournal.bezeich, "[") > 1):
                        depo_balance =  to_decimal(depo_balance) + to_decimal(- to_decimal(billjournal.betrag))

                        curr_recid = billjournal._recid
                        # billjournal = db_session.query(Billjournal).filter(
                        #         (Billjournal.billjou_ref == guest_number) & (Billjournal.artnr != 0) & 
                        #         (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & 
                        #         (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & 
                        #         (num_entries(Billjournal.bezeich, "[") > 1) & 
                        #         (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit")) & 
                        #         (Billjournal._recid > curr_recid)).first()
                        billjournal = db_session.query(Billjournal).filter(
                                (Billjournal.billjou_ref == guest_number) & (Billjournal.artnr != 0) & 
                                (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & 
                                (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & 
                                (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit")) & 
                                (Billjournal._recid > curr_recid)).first()

                for bill, bill_line in db_session.query(Bill, Bill_line)\
                    .join(Bill_line,(Bill_line.rechnr == Bill.rechnr) & 
                          (Bill_line.artnr == depoart_guest)).filter(
                        (Bill.rechnr > 0) & 
                        (Bill.gastnr == guest_number)).order_by(Bill._recid).all():
                    depo_balance =  to_decimal(depo_balance) + to_decimal(bill_line.betrag)
                gdeposit_list.gdeposit_balance =  to_decimal(depo_balance)

    return generate_output()