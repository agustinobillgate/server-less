from functions.additional_functions import *
import decimal
from models import Hoteldpt, Queasy

def selforder_addhtp5bl():
    hoteldpt = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hoteldpt, queasy


        return {}


    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt.num).all():

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 1) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 1
            queasy.char1 = "URL Image Logo Hotel"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 2) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 2
            queasy.char1 = "Font Color 1"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 3) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 3
            queasy.char1 = "Font Color 2"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 4) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 4
            queasy.char1 = "Background Color"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 5) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 5
            queasy.char1 = "Using Payment Gateway"
            queasy.number3 = 4
            queasy.char2 = ""
            queasy.logi1 = True
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 6) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 6
            queasy.char1 = "URL Endpoint WebServices"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 7) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 7
            queasy.char1 = "Parameter Payment Gateway MIDTRANS"
            queasy.number3 = 5
            queasy.char2 = "MERCHANTID=11129189"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 8) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 8
            queasy.char1 = "Parameter Payment Gateway QRIS"
            queasy.number3 = 5
            queasy.char2 = "MALLID=3836;CLIENTID=3836"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 9) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 9
            queasy.char1 = "UserInit For SelfOrder"
            queasy.number3 = 5
            queasy.char2 = "01"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 10) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 10
            queasy.char1 = "Parameter Payment Gateway DOKU"
            queasy.number3 = 5
            queasy.char2 = "MERCHANTID=11129189"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 11) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 11
            queasy.char1 = "Price Include Tax and Services"
            queasy.number3 = 4
            queasy.logi1 = False
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 12) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 12
            queasy.char1 = "Enable Item Notes"
            queasy.number3 = 4
            queasy.logi1 = False
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 13) & (Queasy.number3 == 1) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 13
            queasy.char1 = "Interval Refresh Selforder Dashboard"
            queasy.number3 = 1
            queasy.char2 = "60"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 14) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 14
            queasy.char1 = "Use Dinamic QRCode"
            queasy.number3 = 4
            queasy.logi1 = True
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 15) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 15
            queasy.char1 = "Allow Post Menu Without Confirmation"
            queasy.number3 = 4
            queasy.logi1 = True
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 16) & (Queasy.number3 == 1) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 16
            queasy.char1 = "Range For Geofancing (in meters)"
            queasy.number3 = 1
            queasy.char2 = "1000"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 17) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 17
            queasy.char1 = "Location For Geofancing (longitude, latitude)"
            queasy.number3 = 5
            queasy.char2 = "-6.147497652789192, 106.89989726843324"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 18) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 18
            queasy.char1 = "Hotel Additional Info"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 19) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 19
            queasy.char1 = "Hotel Additional Link"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 20) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 20
            queasy.char1 = "Email Receiver For Copy Bill"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 21) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 21
            queasy.char1 = "Set This Outlet As Room Service"
            queasy.number3 = 4
            queasy.logi1 = False
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 22) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 22
            queasy.char1 = "Item Price depends on VAT Admin"
            queasy.number3 = 4
            queasy.logi1 = False
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 23) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 23
            queasy.char1 = "Additional Info for Price Item"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 24) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 24
            queasy.char1 = "Parameter Payment Gateway XENDIT"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 25) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 25
            queasy.char1 = "Outlet Closing Time (e.g 23:00|07:00)"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 26) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 26
            queasy.char1 = "Change Description ASK FOR BILL To"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 27) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 27
            queasy.char1 = "Home Icon URL"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 28) & (Queasy.number3 == 2) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 28
            queasy.char1 = "Minimum Amount for Online Payment"
            queasy.number3 = 2
            queasy.char2 = "0.00"
            queasy.betriebsnr = hoteldpt.num

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 29) & (Queasy.number3 == 5) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 1
            queasy.number2 = 29
            queasy.char1 = "Sound Link Notification"
            queasy.number3 = 5
            queasy.char2 = ""
            queasy.betriebsnr = hoteldpt.num

    return generate_output()