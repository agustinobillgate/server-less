#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Hoteldpt

def refresh_mapping_pglistbl(pg_number:int, pg_name:string):
    mess_str = ""
    count_i:int = 0
    queasy = hoteldpt = None

    t_queasy = t_hoteldpt = None

    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, count_i, queasy, hoteldpt
        nonlocal pg_number, pg_name


        nonlocal t_queasy, t_hoteldpt
        nonlocal t_queasy_data, t_hoteldpt_data

        return {"mess_str": mess_str}

    def create_t_queasy():

        nonlocal mess_str, count_i, queasy, hoteldpt
        nonlocal pg_number, pg_name


        nonlocal t_queasy, t_hoteldpt
        nonlocal t_queasy_data, t_hoteldpt_data

        for t_hoteldpt in query(t_hoteldpt_data, sort_by=[("num",False)]):

            if pg_number == 1:
                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1-QRIS"
                t_queasy.char2 = "4-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "15-Debit/Credit Card Payment"
                t_queasy.char2 = "1-Debit/Credit Card"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "16-Credit Card Authorization"
                t_queasy.char2 = "2-Credit Card Authorization"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "22-Sinarmas VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "29-BCA VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "32-CIMB VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "33-Danamon VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "34-BRI VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "36-Permata VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "38-BNI VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "41-Mandiri VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "42-QNB VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "43-BTN VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "44-Maybank VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "47-Arta Jasa VA"
                t_queasy.char2 = "3-Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "50-LinkAja!"
                t_queasy.char2 = "4-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "51-Jenius Pay"
                t_queasy.char2 = "4-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "53-OVO"
                t_queasy.char2 = "4-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999

            elif pg_number == 2:
                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1-CREDIT_CARD"
                t_queasy.char2 = "1-Debit/Credit Card"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "2-GOPAY"
                t_queasy.char2 = "2-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "3-QRIS"
                t_queasy.char2 = "2-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "4-SHOPEEPAY"
                t_queasy.char2 = "2-Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "5-BANK_transFER|PERMATA"
                t_queasy.char2 = "6-Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "6-BANK_transFER|BCA"
                t_queasy.char2 = "6-Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "7-BANK_transFER|BNI"
                t_queasy.char2 = "6-Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "8-BANK_transFER|BRI"
                t_queasy.char2 = "6-Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "9-ECHANNEL"
                t_queasy.char2 = "3-Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "10-BCA_KLIKPAY"
                t_queasy.char2 = "3-Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "11-BCA_KLIKBCA"
                t_queasy.char2 = "3-Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "12-CIMB_CLICKS"
                t_queasy.char2 = "3-Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "13-DANAMON_ONLINE"
                t_queasy.char2 = "3-Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "14-BRI_EPAY"
                t_queasy.char2 = "3-Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "15-CSTORE|INDOMARET"
                t_queasy.char2 = "4-Other Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "16-CSTORE|ALFAMART"
                t_queasy.char2 = "4-Other Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "17-AKULAKU"
                t_queasy.char2 = "4-Other Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999

            elif pg_number == 3:
                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1-BRI"
                t_queasy.char2 = "1-BANK_transFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "2-BNI"
                t_queasy.char2 = "1-BANK_transFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "3-MANDIRI"
                t_queasy.char2 = "1-BANK_transFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "4-PERMATA"
                t_queasy.char2 = "1-BANK_transFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "5-BCA"
                t_queasy.char2 = "1-BANK_transFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1-SHOPEEPAY"
                t_queasy.char2 = "2-EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "2-DANA"
                t_queasy.char2 = "2-EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "3-OVO"
                t_queasy.char2 = "2-EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "4-LINKAJA"
                t_queasy.char2 = "2-EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1-CREDIT_CARD"
                t_queasy.char2 = "3-CREDIT_CARD"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1-QRIS"
                t_queasy.char2 = "4-DIGITAL PAYMENT"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)
    create_t_queasy()

    for t_queasy in query(t_queasy_data):

        queasy = get_cache (Queasy, {"key": [(eq, 224)],"number1": [(eq, pg_number)],"number2": [(eq, t_queasy.number2)],"char1": [(eq, t_queasy.char1)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)
            count_i = 1
        pass

    if count_i == 1:
        mess_str = "Update Payment Gateway Article Done"
    else:
        mess_str = "No New Article Found"

    return generate_output()