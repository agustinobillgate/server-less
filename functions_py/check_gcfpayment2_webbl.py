#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Htparam, Guest, Res_line, Bill_line, Debitor

input_list_data, Input_list = create_model("Input_list", {"pvilanguage":int, "gastnr":int, "rechnr":int, "resnr":int, "reslinnr":int, "price":Decimal, "payment":int})

def check_gcfpayment2_webbl(input_list_data:[Input_list]):

    prepare_cache ([Artikel, Htparam, Guest, Res_line, Bill_line, Debitor])

    pvilanguage:int = 0
    gastnr:int = 0
    rechnr:int = 0
    resnr:int = 0
    reslinnr:int = 0
    price:Decimal = to_decimal("0.0")
    payment:int = 0
    msg_str:string = ""
    msg_str2:string = ""
    guest_kreditlimit:int = 0
    enter_passwd1:bool = False
    enter_passwd2:bool = False
    voucher_number:string = ""
    output_list_data = []
    lvcarea:string = "check-gcfpayment"
    zahlungsart:int = 0
    outstand:Decimal = to_decimal("0.0")
    i:int = 0
    str:string = ""
    outstanding:Decimal = to_decimal("0.0")
    allow_cl:bool = True
    artikel = htparam = guest = res_line = bill_line = debitor = None

    input_list = output_list = None

    output_list_data, Output_list = create_model("Output_list", {"msg_str":string, "msg_str2":string, "guest_kreditlimit":Decimal, "enter_passwd1":bool, "enter_passwd2":bool, "voucher_number":string, "outstand":Decimal, "payment":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, gastnr, rechnr, resnr, reslinnr, price, payment, msg_str, msg_str2, guest_kreditlimit, enter_passwd1, enter_passwd2, voucher_number, output_list_data, lvcarea, zahlungsart, outstand, i, str, outstanding, allow_cl, artikel, htparam, guest, res_line, bill_line, debitor


        nonlocal input_list, output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_output():

        nonlocal pvilanguage, gastnr, rechnr, resnr, reslinnr, price, payment, msg_str, msg_str2, guest_kreditlimit, enter_passwd1, enter_passwd2, voucher_number, output_list_data, lvcarea, zahlungsart, outstand, i, str, outstanding, allow_cl, artikel, htparam, guest, res_line, bill_line, debitor


        nonlocal input_list, output_list
        nonlocal output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.msg_str = msg_str
        output_list.msg_str2 = msg_str2
        output_list.guest_kreditlimit =  to_decimal(guest_kreditlimit)
        output_list.enter_passwd1 = enter_passwd1
        output_list.enter_passwd2 = enter_passwd2
        output_list.voucher_number = voucher_number
        output_list.outstand =  to_decimal(outstand)
        output_list.payment = payment

    input_list = query(input_list_data, first=True)

    if input_list:
        pvilanguage = input_list.pvilanguage
        gastnr = input_list.gastnr
        rechnr = input_list.rechnr
        resnr = input_list.resnr
        reslinnr = input_list.reslinnr
        price =  to_decimal(input_list.price)
        payment = input_list.payment


    else:

        return generate_output()

    artikel = get_cache (Artikel, {"artnr": [(eq, payment)],"departement": [(eq, 0)]})

    if artikel and artikel.artart == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1026)]})

        if htparam and htparam.bezeichnung.lower()  != ("not used").lower() :
            allow_cl = htparam.flogical
        else:
            allow_cl = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 116)]})

        if artikel.zwkum == htparam.finteger:
            create_output()

            return generate_output()

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:
            zahlungsart = guest.zahlungsart

        if zahlungsart == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

            if htparam.fchar != "":
                enter_passwd1 = True
            else:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("No C/L payment Articles have been defined for this Guest.", lvcarea, "")

        elif guest.zahlungsart != payment:

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, guest.zahlungsart)]})

            if artikel:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("C/L payment Article for this guest is", lvcarea, "") + chr_unicode(10) + to_string(artikel.artnr) + " - " + artikel.bezeich
                payment = 0
                create_output()

                return generate_output()

        if guest.karteityp == 2:

            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

            if res_line:
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == ("voucher").lower() :
                        voucher_number = substring(str, 7)
                        i = 9999

        if guest.karteityp >= 1 and guest.kreditlimit > 0:

            if price == 0:

                for bill_line in db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                    outstand =  to_decimal(outstand) + to_decimal(bill_line.betrag)


            else:
                outstand =  - to_decimal(price)

            debitor_obj_list = {}
            debitor = Debitor()
            artikel = Artikel()
            for debitor.saldo, debitor._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel.zwkum, artikel._recid in db_session.query(Debitor.saldo, Debitor._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                     (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)
                outstanding =  to_decimal(outstanding) + to_decimal(debitor.saldo)

            if outstand > guest.kreditlimit:

                if allow_cl:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 320)]})

                    if htparam.flogical:

                        if price != 0:
                            msg_str2 = msg_str2 + chr_unicode(2) + translateExtended ("Over Credit Limit:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                        htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

                        if htparam.fchar != "":

                            if price == 0:
                                enter_passwd2 = False
                            else:
                                enter_passwd2 = True
                            guest_kreditlimit = guest.kreditlimit
                    else:
                        msg_str2 = msg_str2 + chr_unicode(2) + "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("Cancel the C/L payment?", lvcarea, "")
                        guest_kreditlimit = guest.kreditlimit
                else:
                    msg_str2 = "&w" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("payment is not possible", lvcarea, "")
                    guest_kreditlimit = guest.kreditlimit
                    create_output()

                    return generate_output()
    create_output()

    return generate_output()