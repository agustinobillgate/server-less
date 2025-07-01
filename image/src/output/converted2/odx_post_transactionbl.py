#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def odx_post_transactionbl(from_date:date, to_date:date):

    prepare_cache ([Queasy])

    summary_bill_list = []
    loop_i:int = 0
    messtaken:string = ""
    messkeyword:string = ""
    messvalue:string = ""
    response_char:string = ""
    response_code:string = ""
    currdata:string = ""
    time_second:int = 0
    queasy = None

    summary_bill = datalist = None

    summary_bill_list, Summary_bill = create_model("Summary_bill", {"datum":date, "times":string, "department":int, "rechnr":int, "total_food":Decimal, "total_bev":Decimal, "total_other":Decimal, "total_service":Decimal, "total_tax":Decimal, "total_disc":Decimal, "total_tips":Decimal, "total_amount":Decimal, "post_result":string, "body":string, "response":string, "guest_name":string, "res_no":int, "room_no":string})
    datalist_list, Datalist = create_model("Datalist", {"vkey":string, "vvalue":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal summary_bill_list, loop_i, messtaken, messkeyword, messvalue, response_char, response_code, currdata, time_second, queasy
        nonlocal from_date, to_date


        nonlocal summary_bill, datalist
        nonlocal summary_bill_list, datalist_list

        return {"summary-bill": summary_bill_list}

    def get_data(vkey:string):

        nonlocal summary_bill_list, loop_i, messtaken, messkeyword, messvalue, response_char, response_code, currdata, time_second, queasy
        nonlocal from_date, to_date


        nonlocal summary_bill, datalist
        nonlocal summary_bill_list, datalist_list

        datalist = query(datalist_list, filters=(lambda datalist: datalist.dataList.vkey == vkey), first=True)

        if dataList:
            return dataList.vValue
        return ""

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 242) & (Queasy.number1 == 99) & (Queasy.date1 >= from_date) & (Queasy.date1 <= to_date)).order_by(Queasy.date1).all():
        time_second = queasy.deci1
        summary_bill = Summary_bill()
        summary_bill_list.append(summary_bill)

        summary_bill.datum = queasy.date1
        summary_bill.times = to_string(time_second, "HH:MM:SS")
        summary_bill.department = queasy.number3
        summary_bill.rechnr = queasy.number2
        summary_bill.body = queasy.char2
        summary_bill.response = queasy.char3
        summary_bill.total_tax =  to_decimal("0")


        for loop_i in range(1,num_entries(queasy.char1, "|")  + 1) :
            messtaken = entry(loop_i - 1, queasy.char1, "|")
            messkeyword = entry(0, messtaken, "=")
            messvalue = entry(1, messtaken, "=")

            if messkeyword == "FOOD":
                summary_bill.total_food =  to_decimal(to_decimal(messvalue))
            elif messkeyword == "BEVR":
                summary_bill.total_bev =  to_decimal(to_decimal(messvalue))
            elif messkeyword == "OTHR":
                summary_bill.total_other =  to_decimal(to_decimal(messvalue))
            elif messkeyword == "SERV":
                summary_bill.total_service =  to_decimal(to_decimal(messvalue))
            elif messkeyword == "DISC":
                summary_bill.total_disc =  to_decimal(to_decimal(messvalue))
            elif messkeyword == "TIPS":
                summary_bill.total_tips =  to_decimal(to_decimal(messvalue))
            elif messkeyword == "RESN":
                summary_bill.res_no = to_int(messvalue)
            elif messkeyword == "ROOM":
                summary_bill.room_no = messvalue
            elif messkeyword == "NAME":
                summary_bill.guest_name = messvalue
        summary_bill.total_amount =  to_decimal(summary_bill.total_food) + to_decimal(summary_bill.total_bev) + to_decimal(summary_bill.total_other) + to_decimal(summary_bill.total_service) + to_decimal(summary_bill.total_disc) + to_decimal(summary_bill.total_tips)
        response_code = entry(0, queasy.char3, "|")
        response_char = entry(1, queasy.char3, "|")
        response_char = replace_str(response_char, chr_unicode(123) , ",")
        response_char = replace_str(response_char, chr_unicode(125) , ",")
        response_char = replace_str(response_char, chr_unicode(91) , ",")
        response_char = replace_str(response_char, chr_unicode(93) , ",")
        response_char = replace_str(response_char, '"', "")
        dataList_list.clear()
        for loop_i in range(1,num_entries(response_char, ",")  + 1) :
            currdata = entry(loop_i - 1, response_char, ",")

            if matches(currdata,r"*:*"):
                datalist = Datalist()
                datalist_list.append(datalist)

                datalist.vkey = trim(entry(0, currdata, ":"))
                datalist.vvalue = trim(entry(1, currdata, ":"))

        if response_code.lower()  == ("200").lower() :
            summary_bill.post_result = get_data ("status").upper()

        elif response_code.lower()  == ("400").lower() :
            summary_bill.post_result = get_data ("message").upper()

        elif response_code.lower()  == ("500").lower() :
            summary_bill.post_result = get_data ("errorMessage").upper()

    return generate_output()