from functions.additional_functions import *
import decimal
from models import Hoteldpt, Queasy, Artikel, H_artikel

def mapping_pglistbl(case_type:int, load_type:int, pg_number:int, pg_name:str, art_dept:int, art_name:str):
    payment_gateway_list_list = []
    vhp_payment_list_list = []
    hoteldpt = queasy = artikel = h_artikel = None

    payment_gateway_list = vhp_payment_list = t_hoteldpt = None

    payment_gateway_list_list, Payment_gateway_list = create_model("Payment_gateway_list", {"pg_art_no":int, "pg_art_name":str, "pg_grp_no":int, "pg_grp_name":str, "pg_art_activate":bool, "vhp_art_no":int, "vhp_art_name":str, "vhp_art_dept":int})
    vhp_payment_list_list, Vhp_payment_list = create_model("Vhp_payment_list", {"vhp_art_no":int, "vhp_art_name":str})
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_gateway_list_list, vhp_payment_list_list, hoteldpt, queasy, artikel, h_artikel


        nonlocal payment_gateway_list, vhp_payment_list, t_hoteldpt
        nonlocal payment_gateway_list_list, vhp_payment_list_list, t_hoteldpt_list
        return {"payment-gateway-list": payment_gateway_list_list, "vhp-payment-list": vhp_payment_list_list}

    def create_queasy():

        nonlocal payment_gateway_list_list, vhp_payment_list_list, hoteldpt, queasy, artikel, h_artikel


        nonlocal payment_gateway_list, vhp_payment_list, t_hoteldpt
        nonlocal payment_gateway_list_list, vhp_payment_list_list, t_hoteldpt_list

        for t_hoteldpt in query(t_hoteldpt_list):

            if pg_number == 1:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1_QRIS"
                queasy.char2 = "4_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "15_Debit/Credit Card Payment"
                queasy.char2 = "1_Debit/Credit Card"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "16_Credit Card Authorization"
                queasy.char2 = "2_Credit Card Authorization"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "22_Sinarmas VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "29_BCA VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "32_CIMB VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "33_Danamon VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "34_BRI VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "36_Permata VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "38_BNI VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "41_Mandiri VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "42_QNB VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "43_BTN VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "44_Maybank VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "47_Arta Jasa VA"
                queasy.char2 = "3_Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "50_LinkAja!"
                queasy.char2 = "4_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "51_Jenius Pay"
                queasy.char2 = "4_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "53_OVO"
                queasy.char2 = "4_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999

            elif pg_number == 2:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1_CREDIT__CARD"
                queasy.char2 = "1_Debit/Credit Card"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "2_GOPAY"
                queasy.char2 = "2_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "3_QRIS"
                queasy.char2 = "2_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "4_SHOPEEPAY"
                queasy.char2 = "2_Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "5_BANK__TRANSFER|PERMATA"
                queasy.char2 = "6_Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "6_BANK__TRANSFER|BCA"
                queasy.char2 = "6_Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "7_BANK__TRANSFER|BNI"
                queasy.char2 = "6_Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "8_BANK__TRANSFER|BRI"
                queasy.char2 = "6_Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "9_ECHANNEL"
                queasy.char2 = "3_Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "10_BCA__KLIKPAY"
                queasy.char2 = "3_Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "11_BCA__KLIKBCA"
                queasy.char2 = "3_Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "12_CIMB__CLICKS"
                queasy.char2 = "3_Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "13_DANAMON__ONLINE"
                queasy.char2 = "3_Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "14_BRI__EPAY"
                queasy.char2 = "3_Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "15_CSTORE|INDOMARET"
                queasy.char2 = "4_Other Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "16_CSTORE|ALFAMART"
                queasy.char2 = "4_Other Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "17_AKULAKU"
                queasy.char2 = "4_Other Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999

            elif pg_number == 3:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1_BRI"
                queasy.char2 = "1_BANK__TRANSFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "2_BNI"
                queasy.char2 = "1_BANK__TRANSFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "3_MANDIRI"
                queasy.char2 = "1_BANK__TRANSFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "4_PERMATA"
                queasy.char2 = "1_BANK__TRANSFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "5_BCA"
                queasy.char2 = "1_BANK__TRANSFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1_SHOPEEPAY"
                queasy.char2 = "2_EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "2_DANA"
                queasy.char2 = "2_EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "3_OVO"
                queasy.char2 = "2_EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "4_LINKAJA"
                queasy.char2 = "2_EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1_CREDIT__CARD"
                queasy.char2 = "3_CREDIT__CARD"
                queasy.logi1 = False
                queasy.betriebsnr = 999

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    if case_type == 1:

        if load_type == 1:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 224) &  (Queasy.number1 == pg_number)).first()

            if not queasy:
                create_queasy()

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 224) &  (Queasy.number1 == pg_number)).all():
                payment_gateway_list = Payment_gateway_list()
                payment_gateway_list_list.append(payment_gateway_list)

                payment_gateway_list.pg_art_no = to_int(entry(0, queasy.char1, "-"))
                payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

                if queasy.number1 == 2:
                    payment_gateway_list.pg_grp_no = to_int(entry(0, queasy.char2, "-"))
                    payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
                payment_gateway_list.pg_art_activate = queasy.logi1

                if num_entries(queasy.char3, "-") >= 2:
                    payment_gateway_list.vhp_art_no = to_int(entry(0, queasy.char3, "-"))
                    payment_gateway_list.vhp_art_name = entry(1, queasy.char3, "-")
                payment_gateway_list.vhp_art_dept = queasy.number2

        elif load_type == 2:

            if art_dept == 0:

                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == art_dept) &  ((Artikel.artart == 2) |  (Artikel.artart == 5) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
                    vhp_payment_list = Vhp_payment_list()
                    vhp_payment_list_list.append(vhp_payment_list)

                    vhp_payment_list.vhp_art_no = artikel.artnr
                    vhp_payment_list.vhp_art_name = artikel.bezeich


            else:

                for h_artikel in db_session.query(H_artikel).filter(
                        (H_artikel.departement == art_dept) &  ((H_artikel.artart == 2) |  (H_artikel.artart == 5) |  (H_artikel.artart == 6) |  (H_artikel.artart == 7)) &  (H_artikel.activeflag)).all():
                    vhp_payment_list = Vhp_payment_list()
                    vhp_payment_list_list.append(vhp_payment_list)

                    vhp_payment_list.vhp_art_no = h_artikel.artnr
                    vhp_payment_list.vhp_art_name = h_artikel.bezeich


    else:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 224) &  (Queasy.number1 == pg_number) &  (Queasy.number2 == art_dept)).all():
            payment_gateway_list = Payment_gateway_list()
            payment_gateway_list_list.append(payment_gateway_list)

            payment_gateway_list.pg_art_no = to_int(entry(0, queasy.char1, "-"))
            payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

            if queasy.number1 == 2:
                payment_gateway_list.pg_grp_no = to_int(entry(0, queasy.char2, "-"))
                payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
            payment_gateway_list.pg_art_activate = queasy.logi1

            if num_entries(queasy.char3, "-") >= 2:
                payment_gateway_list.vhp_art_no = to_int(entry(0, queasy.char3, "-"))
                payment_gateway_list.vhp_art_name = entry(1, queasy.char3, "-")
            payment_gateway_list.vhp_art_dept = queasy.number2

        if art_dept == 0:

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == art_dept) &  ((Artikel.artart == 2) |  (Artikel.artart == 5) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
                vhp_payment_list = Vhp_payment_list()
                vhp_payment_list_list.append(vhp_payment_list)

                vhp_payment_list.vhp_art_no = artikel.artnr
                vhp_payment_list.vhp_art_name = artikel.bezeich


        else:

            for h_artikel in db_session.query(H_artikel).filter(
                    (H_artikel.departement == art_dept) &  ((H_artikel.artart == 2) |  (H_artikel.artart == 5) |  (H_artikel.artart == 6) |  (H_artikel.artart == 7)) &  (H_artikel.activeflag)).all():
                vhp_payment_list = Vhp_payment_list()
                vhp_payment_list_list.append(vhp_payment_list)

                vhp_payment_list.vhp_art_no = h_artikel.artnr
                vhp_payment_list.vhp_art_name = h_artikel.bezeich

    return generate_output()