from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Bill_line, Bill, Guest, Hoteldpt

def approve_listbl():
    approve_list_list = []
    queasy = bill_line = bill = guest = hoteldpt = None

    approve_list = None

    approve_list_list, Approve_list = create_model("Approve_list", {"datum":date, "zeit":str, "keywrd":str, "usrid":str, "billno":int, "gastnr":int, "resnr":int, "reslinnr":int, "gname":str, "remarks":str, "keystr":str, "outstand":decimal, "crlimit":decimal, "max_comp":int, "com_rm":int, "pswd":str, "bl_recid":int, "trecid":int, "karteityp":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal approve_list_list, queasy, bill_line, bill, guest, hoteldpt


        nonlocal approve_list
        nonlocal approve_list_list
        return {"approve-list": approve_list_list}

    def create_list():

        nonlocal approve_list_list, queasy, bill_line, bill, guest, hoteldpt


        nonlocal approve_list
        nonlocal approve_list_list

        srecid:int = 0
        approve_list_list.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 36) & (Queasy.logi1 == False) & (Queasy.betriebsnr == 0)).order_by(Queasy.date1, Queasy.number1).all():
            approve_list = Approve_list()
            approve_list_list.append(approve_list)

            datum = date1
            keywrd = char1
            zeit = to_string(number1, "HH:MM:SS")
            usrid = entry(0, char2, ";")
            keywrd = char1
            trecid = queasy._recid

            if char1 == "RSV":
                keystr = "Reservation"
                pswd = entry(2, char3, ";")
                outstand = to_decimal(entry(3, char3, ";"))
                crlimit = to_decimal(entry(4, char3, ";"))
                remarks = entry(1, char3, ";")
                gastnr = to_int(entry(0, char3, ";"))


            elif char1 == "CI":
                keystr = "Check In"
                gastnr = to_int(entry(0, char3, ";"))
                resnr = to_int(entry(1, char3, ";"))
                reslinnr = to_int(entry(2, char3, ";"))
                pswd = entry(4, char3, ";")
                outstand = to_decimal(entry(5, char3, ";"))
                crlimit = to_decimal(entry(6, char3, ";"))


            elif char1 == "CO":
                keystr = "Check Out"
                gastnr = to_int(entry(0, char3, ";"))
                resnr = to_int(entry(1, char3, ";"))
                reslinnr = to_int(entry(2, char3, ";"))
                pswd = entry(4, char3, ";")
                outstand = to_decimal(entry(5, char3, ";"))
                crlimit = to_decimal(entry(6, char3, ";"))


            elif char1 == "COMP":
                keystr = "Compliment"
                gastnr = to_int(entry(0, char3, ";"))
                max_comp = to_int(entry(1, char3, ";"))
                com_rm = to_int(entry(2, char3, ";"))
                pswd = entry(4, char3, ";")
                outstand = to_decimal(entry(5, char3, ";"))
                crlimit = to_decimal(entry(6, char3, ";"))


            elif char1 == "AR":
                keystr = "Account Receivable"
                pswd = entry(2, char3, ";")
                outstand = to_decimal(entry(3, char3, ";"))
                crlimit = to_decimal(entry(4, char3, ";"))
                gastnr = to_int(entry(0, char3, ";"))


            elif char1 == "CL":
                keystr = "Credit Limit"
                pswd = entry(2, char3, ";")
                outstand = to_decimal(entry(3, char3, ";"))
                crlimit = to_decimal(entry(4, char3, ";"))
                gastnr = to_int(entry(0, char3, ";"))


            elif char1 == "POS":
                keystr = "Misc Item"
                pswd = entry(2, char3, ";")
                remark = entry(1, char3, ";")


            elif char1 == "VOID":
                keystr = "VOID Item"
                pswd = entry(2, char3, ";")
                remark = entry(1, char3, ";")
                srecid = to_int(entry(3, char3, ";"))

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line._recid == srecid)).first()

                if bill_line:

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == bill_line.rechnr)).first()

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == bill.gastnr)).first()
                    approve_list.gastnr = guest.gastnr
                    approve_list.gname = guest.name + " " + guest.vorname1 +\
                            guest.anredefirma
                    approve_list.billno = bill.rechnr
                    approve_list.bl_recid = srecid

            if queasy.char1.lower()  == ("POS").lower() :

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == to_int(entry(3, char3, ";")))).first()

                if hoteldpt:
                    approve_list.gname = hoteldpt.depart


            else:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == approve_list.gastnr)).first()

                if guest:
                    approve_list.gname = guest.name + " " + guest.vorname1 + guest.anredefirma
                    approve_list.karteityp = guest.karteityp

    create_list()

    return generate_output()