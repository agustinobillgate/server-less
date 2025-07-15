#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Artikel, Billjournal, Guest, Bill, Bill_line

payload_list_data, Payload_list = create_model("Payload_list", {"v_mode":int, "user_init":string, "guest_number":int, "guest_name":string})

def guest_deposit_list_webbl(payload_list_data:[Payload_list], pvilanguage:int):

    prepare_cache ([Htparam, Artikel, Guest, Bill_line])

    error_desc = ""
    guest_deposit_data = []
    lvcarea:string = "guest-deposit"
    depoart_guest:int = 0
    depobez_guest:string = ""
    depoart_rsv:int = 0
    depoart_bqt:int = 0
    depoart_pos:int = 0
    total_deposit:Decimal = to_decimal("0.0")
    total_used:Decimal = to_decimal("0.0")
    total_balance:Decimal = to_decimal("0.0")
    htparam = artikel = billjournal = guest = bill = bill_line = None

    guest_deposit = temp_guest_deposit = payload_list = None

    guest_deposit_data, Guest_deposit = create_model("Guest_deposit", {"guest_number":int, "guest_name":string, "guest_type":string, "deposit_amount":Decimal, "deposit_used":Decimal, "deposit_balance":Decimal})
    temp_guest_deposit_data, Temp_guest_deposit = create_model("Temp_guest_deposit", {"guest_number":int, "guest_name":string, "guest_type":string, "deposit_amount":Decimal, "deposit_used":Decimal, "deposit_balance":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_desc, guest_deposit_data, lvcarea, depoart_guest, depobez_guest, depoart_rsv, depoart_bqt, depoart_pos, total_deposit, total_used, total_balance, htparam, artikel, billjournal, guest, bill, bill_line
        nonlocal pvilanguage


        nonlocal guest_deposit, temp_guest_deposit, payload_list
        nonlocal guest_deposit_data, temp_guest_deposit_data

        return {"error_desc": error_desc, "guest-deposit": guest_deposit_data}

    payload_list = query(payload_list_data, first=True)

    if not payload_list:
        error_desc = translateExtended ("No data available.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1068)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 5:
            error_desc = translateExtended ("Deposit article not defined.", lvcarea, "")

            return generate_output()
        depoart_guest = artikel.artnr
        depobez_guest = artikel.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    if htparam:
        depoart_rsv = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 117)]})

    if htparam:
        depoart_bqt = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart_pos = htparam.finteger

    if payload_list.v_mode == 1:

        billjournal = db_session.query(Billjournal).filter(
                 (Billjournal.billjou_ref != 0) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower())).first()

        if billjournal:

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.billjou_ref != 0) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower())).first()
            while None != billjournal:

                temp_guest_deposit = query(temp_guest_deposit_data, filters=(lambda temp_guest_deposit: temp_guest_deposit.guest_number == billjournal.billjou_ref), first=True)

                if not temp_guest_deposit:
                    temp_guest_deposit = Temp_guest_deposit()
                    temp_guest_deposit_data.append(temp_guest_deposit)

                    temp_guest_deposit.guest_number = billjournal.billjou_ref

                    guest = get_cache (Guest, {"gastnr": [(eq, temp_guest_deposit.guest_number)]})

                    if guest:
                        temp_guest_deposit.guest_name = guest.name + ", " + guest.anredefirma

                        if guest.karteityp == 0:
                            temp_guest_deposit.guest_type = "Individual"

                        elif guest.karteityp == 1:
                            temp_guest_deposit.guest_type = "Company"
                        else:
                            temp_guest_deposit.guest_type = "Travel Agent"
                temp_guest_deposit.deposit_amount =  to_decimal(temp_guest_deposit.deposit_amount) + to_decimal(- to_decimal(billjournal.betrag) )
                temp_guest_deposit.deposit_balance =  to_decimal(temp_guest_deposit.deposit_balance) + to_decimal(- to_decimal(billjournal.betrag) )
                total_deposit =  to_decimal(total_deposit) + to_decimal(- to_decimal(billjournal.betrag) )
                total_balance =  to_decimal(total_balance) + to_decimal(- to_decimal(billjournal.betrag) )

                curr_recid = billjournal._recid
                billjournal = db_session.query(Billjournal).filter(
                         (Billjournal.billjou_ref != 0) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower()) & (Billjournal._recid > curr_recid)).first()

            for temp_guest_deposit in query(temp_guest_deposit_data, sort_by=[("guest_name",False)]):
                guest_deposit = Guest_deposit()
                guest_deposit_data.append(guest_deposit)

                buffer_copy(temp_guest_deposit, guest_deposit)

            guest_deposit = query(guest_deposit_data, first=True)

            if guest_deposit:

                for bill, bill_line in db_session.query(Bill, Bill_line).join(Bill_line,(Bill_line.rechnr == Bill.rechnr) & (Bill_line.artnr == depoart_guest)).filter(
                         ((Bill.rechnr > 0) & (Bill.gastnr.in_(list(set([guest_deposit.guest_number for guest_deposit in guest_deposit_data])))))).order_by(Bill._recid).all():                    guest_deposit = query(guest_deposit_data, (lambda guest_deposit: (bill.rechnr > 0)), first=True)
                    guest_deposit.deposit_used =  to_decimal(guest_deposit.deposit_used) + to_decimal(bill_line.betrag)
                    guest_deposit.deposit_balance =  to_decimal(guest_deposit.deposit_balance) + to_decimal(bill_line.betrag)
                    total_used =  to_decimal(total_used) + to_decimal(bill_line.betrag)
                    total_balance =  to_decimal(total_balance) + to_decimal(bill_line.betrag)

            guest_deposit = query(guest_deposit_data, first=True)

            if guest_deposit:
                guest_deposit = Guest_deposit()
                guest_deposit_data.append(guest_deposit)

                guest_deposit.guest_name = "T O T A L"
                guest_deposit.deposit_amount =  to_decimal(total_deposit)
                guest_deposit.deposit_used =  to_decimal(total_used)
                guest_deposit.deposit_balance =  to_decimal(total_balance)


    else:
        guest_deposit = Guest_deposit()
        guest_deposit_data.append(guest_deposit)

        guest_deposit.guest_number = payload_list.guest_number
        guest_deposit.guest_name = payload_list.guest_name

        guest = get_cache (Guest, {"gastnr": [(eq, payload_list.guest_number)]})

        if guest:

            if guest.karteityp == 0:
                guest_deposit.guest_type = "Individual"

            elif guest.karteityp == 1:
                guest_deposit.guest_type = "Company"
            else:
                guest_deposit.guest_type = "Travel Agent"

        billjournal = db_session.query(Billjournal).filter(
                 (Billjournal.billjou_ref == payload_list.guest_number) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower())).first()
        while None != billjournal:
            guest_deposit.deposit_amount =  to_decimal(guest_deposit.deposit_amount) + to_decimal(- to_decimal(billjournal.betrag) )
            guest_deposit.deposit_balance =  to_decimal(guest_deposit.deposit_balance) + to_decimal(- to_decimal(billjournal.betrag) )

            curr_recid = billjournal._recid
            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.billjou_ref == payload_list.guest_number) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower()) & (Billjournal._recid > curr_recid)).first()

        for bill, bill_line in db_session.query(Bill, Bill_line).join(Bill_line,(Bill_line.rechnr == Bill.rechnr) & (Bill_line.artnr == depoart_guest)).filter(
                 (Bill.rechnr > 0) & (Bill.gastnr == payload_list.guest_number)).order_by(Bill._recid).all():
            guest_deposit.deposit_used =  to_decimal(guest_deposit.deposit_used) + to_decimal(bill_line.betrag)
            guest_deposit.deposit_balance =  to_decimal(guest_deposit.deposit_balance) + to_decimal(bill_line.betrag)

    return generate_output()