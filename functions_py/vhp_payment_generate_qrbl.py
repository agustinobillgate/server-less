#using conversion tools version: 1.0.0.119
#-----------------------------------------
# Rd, 02/12/2025, QRIS Payment Integration
#-----------------------------------------
# Testing Environment:
# URL: https://python.staging.e1-vhp.com:10443/dev/Common/paymentGenerateQR
# Payload Example:
"""{
        "request": {
            "baseUrl": "https://python.staging.e1-vhp.com:10443/dev/",
            "inputUsername": "it",
            "inputUserkey": "95EE44CBF839764A7690C157AC66C9C902905E01",
            "userInit": "41",
            "deptNumber": 0,
            "billNumber": 133874,
            "rsvNumber": 96873,
            "rsvLineNumber": 1,
            "paymentChannel": "XENDIT",
            "paymentAmount": 100000,
            "splitbillNumber": 0,
            "hotel_schema": "qcserverless3"
        }
    }"""
#-----------------------------------------

import requests
import json
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Paramtext, Reservation, Hoteldpt, Res_line, Guest, Bill, Bill_line, H_bill, H_bill_line, Bediener

def vhp_payment_generate_qrbl(dept_number:int, bill_number:int, splitbill_number:int, rsv_number:int, 
                              rsv_line_number:int, user_init:string, payment_channel:string, base_url:string, 
                              hotel__schema:string, payment_amount:Decimal):

    prepare_cache ([Queasy, Paramtext, Reservation, Hoteldpt, Res_line, Bill, H_bill, H_bill_line, Bediener])

    result_message = ""
    epoch_signature = 0
    signature_list_data = []
    payment_information_data = []
    cid:string = ""
    cbusinessid:string = ""
    ctype:string = ""
    ccountry:string = ""
    creferenceid:string = ""
    cstats:string = ""
    creusability:string = ""
    cactions:string = ""
    ccreated:string = ""
    cupdated:string = ""
    camount:string = ""
    ccurrency:string = ""
    cchannelcode:string = ""
    cqrstring:string = ""
    cexpiresat:string = ""
    response_pg:string = ""
    hotelname:string = ""
    paymentcode:int = 0
    vhpbill_number:int = 0
    do_it:bool = False
    pg_usr_name:string = ""
    pg_usr_key:string = ""
    secret_key:string = ""
    url_pg:string = ""
    email:string = ""
    phone:string = ""
    payment_duration:string = ""
    duration_str:string = ""
    default_duration:int = 0
    duration_deptnr:List[string] = create_empty_list(10,"")
    duration_perdept:List[int] = create_empty_list(10,0)
    loop_dur:int = 0
    using_duration:int = 0
    using_duration_second:int = 0
    expired_at:string = ""
    dtlocal:datetime = None
    dtutc:datetime = None
    dtexp:datetime = None
    curr_balance:Decimal = to_decimal("0.0")
    queasy = paramtext = reservation = hoteldpt = res_line = guest = bill = bill_line = h_bill = h_bill_line = bediener = None

    payment_information = value_list = signature_list = paymentrecord = None

    payment_information_data, Payment_information = create_model("Payment_information", {"id":string, "businessid":string, "type":string, "country":string, "referenceid":string, "stats":string, "reusability":string, "actions":string, "created":string, "updated":string, "amount":string, "currency":string, "channelcode":string, "qrstring":string, "expiresat":string, "originalresponse":string})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    Paymentrecord = create_buffer("Paymentrecord",Queasy)

    db_session = local_storage.db_session
    log_message = []
    payment_channel = payment_channel.strip()
    base_url = base_url.strip()
    hotel__schema = hotel__schema.strip()

    def get_json_value(pc_json: str, pc_key: str) -> str:
        
        """
        j = '{"name":"John","age":30,"active":true}'
        print(get_json_value(j, "name"))    # "John"
        """
        # Cari posisi "key":
        search = f'"{pc_key}":'
        i_pos = pc_json.find(search)

        if i_pos == -1:
            return ""

        # Cari awal nilai setelah titik dua
        i_start = pc_json.find(":", i_pos) + 1

        # Lewati spasi
        while i_start < len(pc_json) and pc_json[i_start] == " ":
            i_start += 1

        # Jika nilai adalah STRING (diawali dengan ")
        if i_start < len(pc_json) and pc_json[i_start] == '"':
            i_start += 1  # skip opening quote
            i_end = pc_json.find('"', i_start)
            if i_end == -1:
                return ""  # tidak ada penutup
            return pc_json[i_start:i_end]

        # Jika nilai adalah NUMBER / BOOLEAN / lain, ambil sampai koma atau tutup }
        i_end = i_start
        while (
            i_end < len(pc_json)
            and pc_json[i_end] not in [",", "}"]
        ):
            i_end += 1

        return pc_json[i_start:i_end].strip()


    def generate_output():
        nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, secret_key, url_pg, email, phone, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
        nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, payment_channel, base_url, hotel__schema, payment_amount
        nonlocal paymentrecord


        nonlocal payment_information, value_list, signature_list, paymentrecord
        nonlocal payment_information_data, value_list_data, signature_list_data

        return {"log": log_message, "payment_amount": payment_amount, "result_message": result_message, "epoch_signature": epoch_signature, "signature-list": signature_list_data, "payment-information": payment_information_data}

    # def get_json_value(pcjson:string, pckey:string):

    #     nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, secret_key, url_pg, email, phone, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
    #     nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, payment_channel, base_url, hotel__schema, payment_amount
    #     nonlocal paymentrecord


    #     nonlocal payment_information, value_list, signature_list, paymentrecord
    #     nonlocal payment_information_data, value_list_data, signature_list_data

    #     ipos:int = 0
    #     istart:int = 0
    #     iend:int = 0
    #     cvalue:string = ""
    #     ipos = get_index(pcjson, '"' + pckey + '":')

    #     if ipos > 0:
    #         istart = get_index(pcjson, ":", ipos) + 1


    #         while substring(pcjson, istart - 1, 1) == " ":
    #             istart = istart + 1

    #         if substring(pcjson, istart - 1, 1) == '"':
    #             istart = istart + 1
    #             iend = get_index(pcjson, '"', istart)
    #             cvalue = substring(pcjson, istart - 1, iend - istart)
    #         else:
    #             iend = istart
    #             while iend <= length(pcjson) and get_index(",}", substring(pcjson, iend - 1, 1)) == 0:
    #                 iend = iend + 1
    #             cvalue = trim(substring(pcjson, istart - 1, iend - istart))
    #     return cvalue


    def process_query():

        nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, secret_key, url_pg, email, phone, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
        nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, payment_channel, base_url, hotel__schema, payment_amount
        nonlocal paymentrecord


        nonlocal payment_information, value_list, signature_list, paymentrecord
        nonlocal payment_information_data, value_list_data, signature_list_data


        response_pg = connect_to_pg(payment_channel, payment_amount, dept_number, hoteldpt.depart, hotelname, hotel__schema, base_url, vhpbill_number, pg_usr_name, pg_usr_key, "", "", secret_key)

        if response_pg != "":

            if matches(response_pg,r"*error*"):
                do_it = False
                result_message = response_pg
                result_message = replace_str(result_message, chr_unicode(123) , "")
                result_message = replace_str(result_message, chr_unicode(123) , "")
                result_message = replace_str(result_message, '"', "")

                return generate_output()
            else:
                do_it = True
                cid = get_json_value (response_pg, "id")
                cbusinessid = get_json_value (response_pg, "businessId")
                ctype = get_json_value (response_pg, "type")
                ccountry = get_json_value (response_pg, "country")
                creferenceid = get_json_value (response_pg, "referenceId")
                cstats = get_json_value (response_pg, "status")
                creusability = get_json_value (response_pg, "reusability")
                cactions = get_json_value (response_pg, "actions")
                ccreated = get_json_value (response_pg, "created")
                cupdated = get_json_value (response_pg, "updated")
                camount = get_json_value (response_pg, "amount")
                ccurrency = get_json_value (response_pg, "currency")
                cchannelcode = get_json_value (response_pg, "channelCode")
                cqrstring = get_json_value (response_pg, "qrString")
                cexpiresat = get_json_value (response_pg, "expiresAt")


                payment_information = Payment_information()
                payment_information_data.append(payment_information)

                payment_information.id = cid
                payment_information.businessid = cbusinessid
                payment_information.type = ctype
                payment_information.country = ccountry
                payment_information.referenceid = creferenceid
                payment_information.stats = cstats
                payment_information.reusability = creusability
                payment_information.actions = cactions
                payment_information.created = ccreated
                payment_information.updated = cupdated
                payment_information.amount = camount
                payment_information.currency = ccurrency
                payment_information.channelcode = cchannelcode
                payment_information.qrstring = cqrstring
                payment_information.expiresat = expired_at
                payment_information.originalresponse = response_pg


        else:
            result_message = "Failed to Connect Payment Server"
            log_message.append(result_message)
            return generate_output()

        if do_it:
            email = "-"
            phone = "-"

            if bill_number == 0:

                paymentrecord = get_cache (Queasy, {"key": [(eq, 372)],"number1": [(eq, dept_number)],"betriebsnr": [(eq, paymentcode)],"char1": [(eq, cid)],"deci3": [(eq, rsv_number)]})

                if paymentrecord:
                    pass
                    paymentrecord.char2 = cstats
                    paymentrecord.char3 = payment_channel + "|" + cchannelcode + "|" + ccreated + "|" + user_init + "|" + expired_at + "|" + email + "|" + phone
                    paymentrecord.date1 = get_current_date()
                    paymentrecord.date2 = get_current_date()
                    paymentrecord.number3 = get_current_time_in_seconds()
                    paymentrecord.deci1 =  to_decimal(payment_amount)
                    paymentrecord.deci2 =  to_decimal(bill_number)


                    pass
                    pass
                else:
                    paymentrecord = Queasy()
                    db_session.add(paymentrecord)

                    paymentrecord.key = 372
                    paymentrecord.betriebsnr = paymentcode
                    paymentrecord.char1 = cid
                    paymentrecord.char2 = cstats
                    paymentrecord.char3 = payment_channel + "|" + cchannelcode + "|" + ccreated + "|" + user_init + "|" + expired_at + "|" + email + "|" + phone
                    paymentrecord.date1 = get_current_date()
                    paymentrecord.date2 = get_current_date()
                    paymentrecord.number1 = dept_number
                    paymentrecord.number2 = splitbill_number
                    paymentrecord.number3 = get_current_time_in_seconds()
                    paymentrecord.deci1 =  to_decimal(payment_amount)
                    paymentrecord.deci2 =  to_decimal(bill_number)
                    paymentrecord.deci3 =  to_decimal(rsv_number)


            else:

                paymentrecord = get_cache (Queasy, {"key": [(eq, 372)],"number1": [(eq, dept_number)],"number2": [(eq, splitbill_number)],"betriebsnr": [(eq, paymentcode)],"char1": [(eq, cid)],"deci2": [(eq, bill_number)]})

                if paymentrecord:
                    pass
                    paymentrecord.char2 = cstats
                    paymentrecord.char3 = payment_channel + "|" + cchannelcode + "|" + ccreated + "|" + user_init + "|" + expired_at + "|" + email + "|" + phone
                    paymentrecord.date1 = get_current_date()
                    paymentrecord.date2 = get_current_date()
                    paymentrecord.number3 = get_current_time_in_seconds()
                    paymentrecord.deci1 =  to_decimal(payment_amount)
                    paymentrecord.deci3 =  to_decimal(rsv_number)


                    pass
                    pass
                else:
                    paymentrecord = Queasy()
                    db_session.add(paymentrecord)

                    paymentrecord.key = 372
                    paymentrecord.betriebsnr = paymentcode
                    paymentrecord.char1 = cid
                    paymentrecord.char2 = cstats
                    paymentrecord.char3 = payment_channel + "|" + cchannelcode + "|" + ccreated + "|" + user_init + "|" + expired_at + "|" + email + "|" + phone
                    paymentrecord.date1 = get_current_date()
                    paymentrecord.date2 = get_current_date()
                    paymentrecord.number1 = dept_number
                    paymentrecord.number2 = splitbill_number
                    paymentrecord.number3 = get_current_time_in_seconds()
                    paymentrecord.deci1 =  to_decimal(payment_amount)
                    paymentrecord.deci2 =  to_decimal(bill_number)
                    paymentrecord.deci3 =  to_decimal(rsv_number)


            value_list = Value_list()
            value_list_data.append(value_list)

            value_list.var_name = "paymentAmount"
            value_list.value_str = to_string(payment_amount)

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
            result_message = "Generate QR Success"
            log_message.append(result_message)


    # def connect_to_pg(payment_channel:string, payment_amount:Decimal, dept_code:string, dept_name:string, hotel_name:string, hotel_code:string, base_url:string, bill_no:int, usr_name:string, usr_key:string, email:string, phone:string, secret_key:string):

    #     nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, url_pg, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
    #     nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, hotel__schema, paymentrecord


    #     nonlocal payment_information, value_list, signature_list, paymentrecord
    #     nonlocal payment_information_data, value_list_data, signature_list_data

    #     response_pg = ""
    #     ccmd:string = ""

    #     def generate_inner_output():
    #         return (response_pg)


    #     if SEARCH ("/usr1/vhp/qr_result.json") != None:
    #         OS_COMMAND SILENT DELETE ("/usr1/vhp/qr_result.json")

    #     if payment_channel.lower()  == ("XENDIT").lower() :
    #         ccmd = "curl -k --location --request POST " + chr_unicode(34) + url_pg + chr_unicode(34) + " " +\
    #                 "-H 'Content-Type: application/json' " +\
    #                 "-d " + chr_unicode(39) + chr_unicode(123) +\
    #                 '"amount":' + to_string(payment_amount) + "," +\
    #                 '"department_code":' + '"' + dept_code + '",' +\
    #                 '"department_name":' + '"' + dept_name + '",' +\
    #                 '"hotel_name":' + '"' + hotel_name + '",' +\
    #                 '"hotel_code":' + '"' + hotel_code + '",' +\
    #                 '"base_url":' + '"' + base_url + '",' +\
    #                 '"bill_number":' + to_string(bill_no) + "," +\
    #                 '"username":' + '"' + usr_name + '",' +\
    #                 '"user_key":' + '"' + usr_key + '",' +\
    #                 '"secretKey":' + '"' + secret_key + '",' +\
    #                 '"email":' + '"' + email + '",' +\
    #                 '"expiresAt":' + '"' + expired_at + '",' +\
    #                 '"mobile_number":' + '"' + phone + '"' +\
    #                 chr_unicode(125) + chr_unicode(39) + " " +\
    #                 "> /usr1/vhp/qr_result.json"


    #         OS_COMMAND SILENT VALUE (ccmd)
    #         response_pg = ""


    #     return generate_inner_output()

    def connect_to_pg(payment_channel: str,
                  payment_amount: Decimal,
                  dept_code: str,
                  dept_name: str,
                  hotel_name: str,
                  hotel_code: str,
                  base_url: str,
                  bill_no: int,
                  usr_name: str,
                  usr_key: str,
                  email: str,
                  phone: str,
                  secret_key: str,
                  expires_at: str):

        url = base_url.strip()

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "amount": float(payment_amount),
            "department_code": dept_code,
            "department_name": dept_name,
            "hotel_name": hotel_name,
            "hotel_code": hotel_code,
            "base_url": base_url,
            "bill_number": bill_no,
            "username": usr_name,
            "user_key": usr_key,
            "secretKey": secret_key,
            "email": email,
            "expiresAt": expires_at,
            "mobile_number": phone
        }

        # Hanya untuk XENDIT (sesuai script OE-mu)
        if payment_channel.lower() != "xendit":
            return f"Unsupported payment channel: {payment_channel}"

        try:
            response = requests.post(url, json=payload, timeout=15)

            # Jika HTTP error: 400/500 dll
            if response.status_code >= 400:
                return f"error: HTTP {response.status_code} - {response.text}"

            # Coba parse JSON
            try:
                return response.text  # biarkan string JSON mentah, sama seperti OE
            except:
                return "error: invalid JSON response"

        except requests.exceptions.Timeout:
            return "error: timeout connecting to payment server"

        except requests.exceptions.ConnectionError:
            return "error: payment server unreachable"

        except Exception as e:
            return f"error: {str(e)}"

    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, secret_key, url_pg, email, phone, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
        nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, payment_channel, base_url, hotel__schema, payment_amount
        nonlocal paymentrecord


        nonlocal payment_information, value_list, signature_list, paymentrecord
        nonlocal payment_information_data, signature_list_data

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_data)


        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_data):
            value_str = value_list.value_str.lower()

            if value_str == "yes":
                value_str = "true"
            elif value_str == "no":
                value_str = "false"
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_data.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, secret_key, url_pg, email, phone, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
        nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, payment_channel, base_url, hotel__schema, payment_amount
        nonlocal paymentrecord


        nonlocal payment_information, value_list, signature_list, paymentrecord
        nonlocal payment_information_data, value_list_data, signature_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def converttoutc(plocaltime:datetime, poffsethrs:Decimal):

        nonlocal result_message, epoch_signature, signature_list_data, payment_information_data, cid, cbusinessid, ctype, ccountry, creferenceid, cstats, creusability, cactions, ccreated, cupdated, camount, ccurrency, cchannelcode, cqrstring, cexpiresat, response_pg, hotelname, paymentcode, vhpbill_number, do_it, pg_usr_name, pg_usr_key, secret_key, url_pg, email, phone, payment_duration, duration_str, default_duration, duration_deptnr, duration_perdept, loop_dur, using_duration, using_duration_second, expired_at, dtlocal, dtutc, dtexp, curr_balance, queasy, paramtext, reservation, hoteldpt, res_line, guest, bill, bill_line, h_bill, h_bill_line, bediener
        nonlocal dept_number, bill_number, splitbill_number, rsv_number, rsv_line_number, user_init, payment_channel, base_url, hotel__schema, payment_amount
        nonlocal paymentrecord


        nonlocal payment_information, value_list, signature_list, paymentrecord
        nonlocal payment_information_data, value_list_data, signature_list_data

        putc = None
        isecondsoffset:int = 0
        dttemp:datetime = None

        def generate_inner_output():
            return (putc)

        isecondsoffset = to_int(poffsethrs * 3600)


        dttemp = plocaltime


        putc = add_interval(dttemp, - isecondsoffset, "seconds")

        return generate_inner_output()


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 379) & (Queasy.betriebsnr == 1)).order_by(Queasy.number1).all():

        if queasy.number1 == 1:
            pg_usr_name = queasy.char2

        elif queasy.number1 == 2:
            pg_usr_key = queasy.char2

        elif queasy.number1 == 3:
            url_pg = queasy.char2

        elif queasy.number1 == 426:
            secret_key = queasy.char2

        elif queasy.number1 == 81:
            payment_duration = queasy.char2

    if pg_usr_name == "":
        result_message = "Param No 1.Payment Gateway WebHook Username Can't be Null in Payment Gateway Setup Parameters"
        log_message.append(result_message)

        return generate_output()

    if pg_usr_key == "":
        result_message = "Param No 2.Payment Gateway WebHook USerkey Can't be Null in Payment Gateway Setup Parameters"
        log_message.append(result_message)
        return generate_output()

    if url_pg == "":
        result_message = "Param No 3.URL QRIS Payment Can't be Null in Payment Gateway Setup Parameters"
        log_message.append(result_message)

        return generate_output()    

    if secret_key == "":
        result_message = "Param No 426.Digital Payment Secret Key Can't be Null in Payment Gateway Setup Parameters"
        log_message.append(result_message)
        return generate_output()

    if payment_duration != "":

        if num_entries(payment_duration, ";") >= 2:
            for loop_dur in range(1,num_entries(payment_duration, ";")  + 1) :

                if loop_dur == 1:
                    default_duration = to_int(entry(0, payment_duration, ";"))
                else:
                    duration_str = entry(loop_dur - 1, payment_duration, ";")

                    if duration_str != "":

                        if num_entries(duration_str, ",") >= 2:
                            duration_deptnr[loop_dur - 1 - 1] = trim(entry(0, duration_str, ","))
                            duration_perdept[loop_dur - 1 - 1] = to_int(entry(1, duration_str, ","))
        else:
            using_duration = 15

    if using_duration == 0:
        for loop_dur in range(1,10 + 1) :

            if duration_deptnr[loop_dur - 1] == ("D" + trim(to_string(dept_number)).lower()):
                using_duration = duration_perdept[loop_dur - 1]
    using_duration_second = using_duration * 60
    dtlocal = get_current_datetime()
    dtutc = converttoutc(dtlocal, 7)
    dtexp = add_interval(dtutc, + using_duration_second, "seconds")
    expired_at = to_string(dtexp)
    expired_at = replace_str(expired_at, " ", "T")
    expired_at = expired_at + "Z"
    expired_at = substring(expired_at, 6, 4) + "-" + substring(expired_at, 3, 2) + "-" + substring(expired_at, 0, 2) + "T" + entry(1, expired_at, "T")

    if payment_channel.lower()  == ("XENDIT").lower() :
        paymentcode = 1

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    hotelname = paramtext.ptexte

    if dept_number == 0:

        if bill_number == 0:

            reservation = get_cache (Reservation, {"resnr": [(eq, rsv_number)]})

            if not reservation:
                result_message = "Reservation Not Found for Reservation No: " + to_string(rsv_number)
                log_message.append(result_message)
                return generate_output()
            else:
                payment_amount =  to_decimal(reservation.depositgef)
                vhpbill_number = 0

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept_number)]})

                res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"reslinnr": [(eq, rsv_line_number)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                process_query()
        else:

            bill = get_cache (Bill, {"resnr": [(eq, rsv_number)],"rechnr": [(eq, bill_number)]})

            if not bill:
                result_message = "Bill Not Found for Bill Number: " + to_string(bill_number) + " in Reservation No: " + to_string(rsv_number)
                log_message.append(result_message)
                return generate_output()
            else:

                if payment_amount != 0:

                    if payment_amount > bill.saldo:
                        result_message = "Payment Amount Greater Than Current Bill Balance!"
                        log_message.append(result_message)
                        return generate_output()
                else:
                    payment_amount =  to_decimal(bill.saldo)
                vhpbill_number = bill.rechnr

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)]})

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept_number)]})

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                process_query()
    else:

        h_bill = get_cache (H_bill, {"departement": [(eq, dept_number)],"rechnr": [(eq, bill_number)]})

        if not h_bill:
            result_message = "Bill Not Found for Dept No: " + to_string(dept_number) + " Bill Number: " + to_string(bill_number)
            log_message.append(result_message)
            return generate_output()
        else:

            if splitbill_number == 0:

                if payment_amount != 0:

                    if payment_amount - h_bill.saldo > 1000:
                        result_message = "Payment Amount Greater Than Current Bill Balance!"
                        log_message.append(result_message)
                        return generate_output()
                else:
                    payment_amount =  to_decimal(h_bill.saldo)
                vhpbill_number = h_bill.rechnr

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept_number)]})
                process_query()
            else:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.waehrungsnr == splitbill_number)).order_by(H_bill_line._recid).all():
                    curr_balance =  to_decimal(curr_balance) + to_decimal(h_bill_line.betrag)

                if payment_amount != 0:

                    if payment_amount - curr_balance > 1000:
                        result_message = "Payment Amount Greater Than Current Bill Balance!"
                        log_message.append(result_message)
                        return generate_output()
                else:
                    payment_amount =  to_decimal(curr_balance)
                vhpbill_number = h_bill.rechnr

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept_number)]})
                process_query()

    return generate_output()