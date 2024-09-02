from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def selforder_post_payment_gatewaybl(outletno:int, billno:int, paymentstring:str, session_parameter:str):
    result_message = ""
    mestoken:str = ""
    meskeyword:str = ""
    mesvalue:str = ""
    loop_i:int = 0
    payment_type:str = ""
    found_flag:bool = False
    do_it:bool = False
    paymentcode:int = 0
    bankname:str = ""
    noref:str = ""
    resultmsg:str = ""
    ccnumber:str = ""
    amount:str = ""
    transdat:str = ""
    transid_merchant:str = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, mestoken, meskeyword, mesvalue, loop_i, payment_type, found_flag, do_it, paymentcode, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, queasy


        return {"result_message": result_message}


    if paymentstring == None:
        paymentstring = ""

    if paymentstring != "":
        do_it = False
        payment_type = entry(0, paymentstring, ";")
        paymentstring = substring(paymentstring, 5)

        if payment_type == "DOKU":
            paymentcode = 1
            do_it = True
            for loop_i in range(1,num_entries(paymentstring, ";")  + 1) :
                mestoken = entry(loop_i - 1, paymentstring, ";")
                meskeyword = entry(0, mestoken, " == ")
                mesvalue = entry(1, mestoken, " == ")

                if meskeyword == "BANK":
                    bankname = mesvalue
                elif meskeyword == "resultmsg":
                    resultmsg = mesvalue
                elif meskeyword == "MCN":
                    ccnumber = mesvalue
                elif meskeyword == "amount":
                    amount = mesvalue
                elif meskeyword == "TRANSIDMERCHANT":
                    transid_merchant = mesvalue
                elif meskeyword == "PAYMENTDATETIME":
                    transdat = mesvalue
    elif meskeyword == "QRIS":
        paymentcode = 2
        do_it = True
        for loop_i in range(1,num_entries(paymentstring, ";")  + 1) :
            mestoken = entry(loop_i - 1, paymentstring, ";")
            meskeyword = entry(0, mestoken, " == ")
            mesvalue = entry(1, mestoken, " == ")

            if meskeyword == "DPMALLID":
                bankname = mesvalue
            elif meskeyword == "resultmsg":
                resultmsg = mesvalue
            elif meskeyword == "CLIENTID":
                ccnumber = mesvalue
            elif meskeyword == "amount":
                amount = mesvalue
            elif meskeyword == "TRANSIDMERCHANT":
                transid_merchant = mesvalue
            elif meskeyword == "TRANSACTIONDATETIME":
                transdat = mesvalue

    if do_it:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == outletno) &  (func.lower(Queasy.char3) == (session_parameter).lower())).first()

        if queasy:
            queasy.char1 = resultmsg
            queasy.char2 = transid_merchant + "|" + entry(1, queasy.char2, "|")
            queasy.char3 = session_parameter


        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 223
            queasy.number1 = outletno
            queasy.number2 = billno
            queasy.number3 = paymentcode
            queasy.char1 = resultmsg
            queasy.char2 = transid_merchant
            queasy.char3 = session_parameter
            queasy.date1 = get_current_date()


        result_message = "0 - Update Payment Success!"
    else:
        result_message = "1 - Update Payment FAILED! check your paymentstring."
    else:
        result_message = "2 - paymentstring cannot be empty string."

    return generate_output()