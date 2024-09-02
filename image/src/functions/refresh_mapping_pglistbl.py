from functions.additional_functions import *
import decimal
from models import Queasy, Hoteldpt

def refresh_mapping_pglistbl(pg_number:int, pg_name:str):
    mess_str = ""
    queasy = hoteldpt = None

    t_queasy = t_hoteldpt = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, queasy, hoteldpt


        nonlocal t_queasy, t_hoteldpt
        nonlocal t_queasy_list, t_hoteldpt_list
        return {"mess_str": mess_str}

    def create_t_queasy():

        nonlocal mess_str, queasy, hoteldpt


        nonlocal t_queasy, t_hoteldpt
        nonlocal t_queasy_list, t_hoteldpt_list

        for t_hoteldpt in query(t_hoteldpt_list):

            if pg_number == 1:
                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1_QRIS"
                t_queasy.char2 = "4_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "15_Debit/Credit Card Payment"
                t_queasy.char2 = "1_Debit/Credit Card"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "16_Credit Card Authorization"
                t_queasy.char2 = "2_Credit Card Authorization"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "22_Sinarmas VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "29_BCA VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "32_CIMB VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "33_Danamon VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "34_BRI VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "36_Permata VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "38_BNI VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "41_Mandiri VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "42_QNB VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "43_BTN VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "44_Maybank VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "47_Arta Jasa VA"
                t_queasy.char2 = "3_Virtual Account"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "50_LinkAja!"
                t_queasy.char2 = "4_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "51_Jenius Pay"
                t_queasy.char2 = "4_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "53_OVO"
                t_queasy.char2 = "4_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999

            elif pg_number == 2:
                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1_CREDIT__CARD"
                t_queasy.char2 = "1_Debit/Credit Card"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "2_GOPAY"
                t_queasy.char2 = "2_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "3_QRIS"
                t_queasy.char2 = "2_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "4_SHOPEEPAY"
                t_queasy.char2 = "2_Digital Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "5_BANK__TRANSFER|PERMATA"
                t_queasy.char2 = "6_Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "6_BANK__TRANSFER|BCA"
                t_queasy.char2 = "6_Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "7_BANK__TRANSFER|BNI"
                t_queasy.char2 = "6_Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "8_BANK__TRANSFER|BRI"
                t_queasy.char2 = "6_Bank Transfer"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "9_ECHANNEL"
                t_queasy.char2 = "3_Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "10_BCA__KLIKPAY"
                t_queasy.char2 = "3_Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "11_BCA__KLIKBCA"
                t_queasy.char2 = "3_Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "12_CIMB__CLICKS"
                t_queasy.char2 = "3_Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "13_DANAMON__ONLINE"
                t_queasy.char2 = "3_Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "14_BRI__EPAY"
                t_queasy.char2 = "3_Internet Banking"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "15_CSTORE|INDOMARET"
                t_queasy.char2 = "4_Other Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "16_CSTORE|ALFAMART"
                t_queasy.char2 = "4_Other Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "17_AKULAKU"
                t_queasy.char2 = "4_Other Payment"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999

            elif pg_number == 3:
                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1_BRI"
                t_queasy.char2 = "1_BANK__TRANSFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "2_BNI"
                t_queasy.char2 = "1_BANK__TRANSFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "3_MANDIRI"
                t_queasy.char2 = "1_BANK__TRANSFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "4_PERMATA"
                t_queasy.char2 = "1_BANK__TRANSFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "5_BCA"
                t_queasy.char2 = "1_BANK__TRANSFER"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1_SHOPEEPAY"
                t_queasy.char2 = "2_EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "2_DANA"
                t_queasy.char2 = "2_EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "3_OVO"
                t_queasy.char2 = "2_EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "4_LINKAJA"
                t_queasy.char2 = "2_EWALLET"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                t_queasy.key = 224
                t_queasy.number1 = pg_number
                t_queasy.number2 = t_hoteldpt.num
                t_queasy.char1 = "1_CREDIT__CARD"
                t_queasy.char2 = "3_CREDIT__CARD"
                t_queasy.logi1 = False
                t_queasy.betriebsnr = 999


    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)
    create_t_queasy()

    for t_queasy in query(t_queasy_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 224) &  (Queasy.number1 == pg_number) &  (Queasy.char1 == t_Queasy.char1)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)
            mess_str = "Update Payment Gateway Article Done"
        else:
            mess_str = "No New Article Found"

        queasy = db_session.query(Queasy).first()

    return generate_output()