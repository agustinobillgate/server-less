from functions.additional_functions import *
import decimal
import re
from models import Htparam, Paramtext

def add_htp5bl():
    htparam = paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, paramtext


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 41)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "Membership points:0 == guest 1 == reserve,2 == booker"
        htparam.reihenfolge = 83


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1074)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1074)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Order Taker Mobile"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1075
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1075)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1075)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for HouseKeeping Mobile"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1076
        htparam.fchar = " "

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 30)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "Misc. Article Number for Booking Engine"
        htparam.reihenfolge = 69


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 786)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 786)).first()
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2320
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) A/P Approval by System (01;xx;99)"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 279)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 279)).first()
        htparam.paramgruppe = 6
        htparam.reihenfolge = 69
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is GCF's Mobile_No Mandatory upon C/I?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 930)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 930)).first()
        htparam.bezeichnung = "Max allowed extended c/o time [HH:MM]"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 78)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 78)).first()
        htparam.bezeichnung = "Web CI (IP;Port;Website)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 79)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 79)).first()
        htparam.bezeichnung = "LetterNo for WebCI email (NAT,No;..;DEF,No)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 787)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 787)).first()
        htparam.bezeichnung = "Loyalty Setup eg loyaltyui.r|Silver,1;Gold,2"
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 787)).first()
        htparam.bezeichnung = "Loyalty Name & types eg GHS_Silver,1;Gold,2"

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 789)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 789)).first()
        htparam.bezeichnung = "Loyalty Setup"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 453)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 453)).first()
        htparam.bezeichnung = "CashRefund & Rebate Articles [c1,.;r1,r2.]"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 299)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 299)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Golf Module"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 110
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 454)).first()

    if not re.match(".*Main Group.*",htparam.bezeichnung):

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 454)).first()
        htparam.bezeichnung = "Main Group No for Disc Articles"
        htparam.finteger = 0
        htparam.feldtyp = 1

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1034)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1034)).first()
        htparam.paramgruppe ppe = 38
        htparam.bezeichnung = "Digit number of G/L main acct (default 4)"
        htparam.finteger = 0
        htparam.reihenfolge = 33
        htparam.feldtyp = 1

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1341)).first()

    if htparam.paramgruppe == 30:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1341)).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "LetterNo for Bill's Term&Condition"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 974)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "C/O w/ unbalanced bill allowed? (def == No)"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 393)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "User PSWD expiry after xx days (def == 0)"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 394)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Next PSWD expired date (param 393)"
        htparam.feldtyp = 3
        htparam.fdate = None

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 929)).first()

    if htparam.paramgruppe == 25:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Add Keycard Program ($KCard1 == xx#$KCard2 == yy)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 19)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Access Right 3 required to modify GL Journal?"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 32

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 277)).first()

    if htparam.paramgruppe != 9:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 277)).first()
        htparam.paramgruppe = 9
        htparam.bezeichnung = "Save FO statistic (762 / 2000 days)"
        htparam.feldtyp = 1
        htparam.finteger = 762
        htparam.fchar = ""
        htparam.reihenfolge = 267

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 371)).first()
        htparam.paramgruppe = 9
        htparam.bezeichnung = "Save system log files (60 / 180 days)"
        htparam.feldtyp = 1
        htparam.finteger = 60
        htparam.fchar = ""
        htparam.reihenfolge = 268

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2843)).first()

    if htparam and htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Transfer GL to Head Office IP:Port"
        htparam.feldtyp = 5
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.reihenfolge = 31

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 51)).first()

    if htparam and htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Letter No for RC Term & Condition"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.reihenfolge = 136

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1102)).first()

    if htparam and htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR VHP Mobile"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1074

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1013)).first()
    htparam.paramgruppe = 27
    htparam.feldtyp = 5
    htparam.bezeichnung = "Rounding Rate amount for the Child Rate Codes?"
    htparam.reihenfolge = 23

    if htparam.fchar == "":
        htparam.fchar = to_string(htparam.finteger) + ";0"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 834)).first()

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 834)).first()
    htparam.feldtyp = 4
    htparam.bezeichnung = "Allow Cashless Transaction using Pre_paid card?"
    htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 569)).first()

    if htparam.bezeichnung.lower()  == "Not Used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 569)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Restaurant Article for Cashless Payment"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 472)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 472)).first()
        htparam.paramgruppe = 99
        htparam.feldtyp = 4
        htparam.bezeichnung = "License for Guest ID scan Program"
        htparam.flogical = False
        htparam.reihenfolge = 108
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 368)).first()

    if htparam.paramgruppe != 24:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 368)).first()
        htparam.paramgruppe = 24
        htparam.feldtyp = 5
        htparam.bezeichnung = "APT ArtNo for Water;Electricity;VAT"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 256)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 256)).first()
        htparam.paramgruppe = 10
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate Strong VHP User Password Mode?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1109)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1109)).first()
        htparam.paramgruppe = 27
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate Guest Command? (Table guest_remark)"
        htparam.flogical = False
        htparam.reihenfolge = 25

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 991)).first()
    htparam.bezeichnung = "License for General Cashier"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1006)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1006)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Default SOB for Walk_in Guest"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 719)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 719)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Cut_off_days of Banquet Booking (in days)"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1373)).first()

    if htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1373)).first()
        htparam.paramgruppe = 15
        htparam.feldtyp = 5
        htparam.bezeichnung = "Program Path for PDF"
        htparam.fchar = ""
        htparam.reihenfolge = 13

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1374)).first()

    if htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1374)).first()
        htparam.paramgruppe = 15
        htparam.feldtyp = 5
        htparam.bezeichnung = "Program name of PDF"
        htparam.fchar = ""
        htparam.reihenfolge = 14

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1058)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1058)).first()
        htparam.paramgruppe = 27
        htparam.feldtyp = 5
        htparam.bezeichnung = "ThisYR Nat KeyAcct gastNo eg 10,35,."
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1025)).first()
        htparam.paramgruppe = 27
        htparam.feldtyp = 5
        htparam.bezeichnung = "LastYR Nat KeyAcct gastNo eg 10,35,."
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 278)).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.bezeichnung = "SOB Code for Web Production Report"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 378)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 378)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "MiniBar ArtNo needed for PABX IF"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1379)).first()

    if htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1379)).first()
        htparam.paramgruppe = 15
        htparam.reihenfolge = 133
        htparam.feldtyp = 5
        htparam.bezeichnung = "Param for GreetMail (server;port;usrnm;pwd)"
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1396)).first()
        htparam.paramgruppe = 15
        htparam.reihenfolge = 134
        htparam.feldtyp = 5
        htparam.bezeichnung = "LetterNo for C/I emails (NAT,No;.;DEF,No)"
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1397)).first()
        htparam.paramgruppe = 15
        htparam.reihenfolge = 135
        htparam.feldtyp = 5
        htparam.bezeichnung = "LetterNo for C/O emails (NAT,No;.;DEF,No)"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 322)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 322)).first()
        htparam.paramgruppe = 6
        htparam.reihenfolge = 68
        htparam.feldtyp = 1
        htparam.bezeichnung = "Delaytion of sending e_mails in minutes (249)"
        htparam.finteger = 60

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1070)).first()

    if htparam.bezeichnung.lower()  == "Not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1070)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate Voice Mail Box?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 249)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 249)).first()
        htparam.paramgruppe = 6
        htparam.reihenfolge = 67
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is GCF's Email Address Mandatory upon C/I?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 250)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 250)).first()
        htparam.paramgruppe = 6
        htparam.reihenfolge = 85
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is GCF's Guest Phone Mandatory upon C/I?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 737)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 737)).first()
        htparam.paramgruppe = 6
        htparam.reihenfolge = 40
        htparam.feldtyp = 5
        htparam.bezeichnung = "R_Codes for Report by Ratecode [C1;C2;]"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 836)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 836)).first()
        htparam.paramgruppe = 21
        htparam.reihenfolge = 73
        htparam.feldtyp = 4
        htparam.bezeichnung = "PR: hierarchical approval? (Def NO)"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 439)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 439)).first()
        htparam.paramgruppe = 27
        htparam.feldtyp = 1
        htparam.bezeichnung = "DynaRate Occ: 0 == RmType 1 == Global 2 == Optimized"
        htparam.finteger = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1203)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1203)).first()
        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.bezeichnung = "Alert if Disc Article's VAT&Srv doesnt match?"
        htparam.flogical = True
        htparam.reihenfolge = 428

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1019)).first()

    if htparam.paramgruppe != 8:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1019)).first()
        htparam.paramgruppe = 8
        htparam.feldtyp = 5
        htparam.bezeichnung = "Number of Day_Use (rooms)"
        htparam.fchar = "DAY_USE"
        htparam.reihenfolge = 184

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 341)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 341)).first()
        htparam.feldtyp = 5
        htparam.bezeichnung = "IF_Program for WiFi_Internet"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 342)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 342)).first()
        htparam.feldtyp = 5
        htparam.bezeichnung = "Program to display Room Rate"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 946)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 963)).first()

        if htparam and htparam.paramgruppe == 6 and htparam.reihenfolge == 57:
            htparam.reihenfolge = 999

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 946)).first()
        htparam.paramgruppe = 6
        htparam.bezeichnung = "Ask deposit transfer when C/I the guest?"
        htparam.reihenfolge = 57
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 947)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 947)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Deduct Stocks of POS compliment bills in NA?"
        htparam.reihenfolge = 72
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 911)).first()

    if htparam.paramgruppe == 13:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 911)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Enable Button Option in Stock Article Setup?"
        htparam.reihenfolge = 71
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 429)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 429)).first()
        htparam.paramgruppe = 6
        htparam.bezeichnung = "Check user's Printing Access Right?"
        htparam.reihenfolge = 66
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 281)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 281)).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Print Food/Bev DISC separately on bill?"
        htparam.reihenfolge = 84
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2405)).first()

    if htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2405)).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending BEO(server;port;usernm;pw)"
        htparam.reihenfolge = 129
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2406)).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending CRM(server;port;usernm;pw)"
        htparam.reihenfolge = 130
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2407)).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending SMS/email report(server;port;usernm;pw)"
        htparam.reihenfolge = 131
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2408)).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending Questionnaire(server;port;usernm;pw)"
        htparam.reihenfolge = 132
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 962)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 962)).first()
        htparam.bezeichnung = "Post 0 Room Rate in NA program? (DEF  ==  NO)"
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 695)).first()
    htparam.paramgruppe = 17
    htparam.bezeichnung = "Type of Document"
    htparam.feldtyp = 5
    htparam.fchar = "DOCU_TYPE"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 397)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 397)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETA Flight Number"
        htparam.reihenfolge = 171
        htparam.feldtyp = 5
        htparam.fchar = "ETAFL"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 713)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETA Time"
        htparam.reihenfolge = 172
        htparam.feldtyp = 5
        htparam.fchar = "ETATIME"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 714)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETD Flight Number"
        htparam.reihenfolge = 173
        htparam.feldtyp = 5
        htparam.fchar = "ETDFL"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 715)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETD Time"
        htparam.reihenfolge = 174
        htparam.feldtyp = 5
        htparam.fchar = "ETDTIME"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 725)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Birth Place"
        htparam.reihenfolge = 175
        htparam.feldtyp = 5
        htparam.fchar = "BIRTHPLACE"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 726)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Passport / ID Expired Date"
        htparam.reihenfolge = 176
        htparam.feldtyp = 5
        htparam.fchar = "ID_EXPIRED"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 730)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Purpose of Stay"
        htparam.reihenfolge = 177
        htparam.feldtyp = 5
        htparam.fchar = "PURPOSE"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 731)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Mobile Number"
        htparam.reihenfolge = 178
        htparam.feldtyp = 5
        htparam.fchar = "MOBILE"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 733)).first()

    if htparam.paramgruppe != 17 or htparam.fchar.lower()  == "COMPANY":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 733)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Company Name of the hotel guest"
        htparam.reihenfolge = 179
        htparam.feldtyp = 5
        htparam.fchar = "GCOMPANY"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 759)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 759)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Address 1"
        htparam.reihenfolge = 180
        htparam.feldtyp = 5
        htparam.fchar = "RSV_adr1"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 760)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Address 2"
        htparam.reihenfolge = 181
        htparam.feldtyp = 5
        htparam.fchar = "RSV_adr2"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 761)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Address 3"
        htparam.reihenfolge = 182
        htparam.feldtyp = 5
        htparam.fchar = "RSV_adr3"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 762)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name City"
        htparam.reihenfolge = 183
        htparam.feldtyp = 5
        htparam.fchar = "RSV_city"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 763)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name ZIP code"
        htparam.reihenfolge = 184
        htparam.feldtyp = 5
        htparam.fchar = "RSV_ZIP"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 765)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Country"
        htparam.reihenfolge = 185
        htparam.feldtyp = 5
        htparam.fchar = "RSV_country"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 766)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "CreditCard No, Expiry MM/YYYY"
        htparam.reihenfolge = 186
        htparam.feldtyp = 5
        htparam.fchar = "CCard"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 839)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Letter Category Number for SMS Report CFG"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1459)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR CRM Module"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1073

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 347)).first()

    if htparam.paramgruppe != 13 or htparam.bezeichnung.lower()  == "Not used" or htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 347)).first()
        htparam.paramgruppe = 13
        htparam.reihenfolge = 11
        htparam.bezeichnung = "PF Path file for VHPArchive DB"
        htparam.fchar = ""
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1202)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1202)).first()
        htparam.paramgruppe = 27
        htparam.reihenfolge = 3
        htparam.bezeichnung = "Restriction on GCF modification applied? (DEF == No)"
        htparam.flogical = False
        htparam.feldtyp = 4

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1018)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1018)).first()
        htparam.paramgruppe = 38
        htparam.reihenfolge = 30
        htparam.bezeichnung = "PI Cheque/Giro Temporary AcctNo"
        htparam.fchar = ""
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 931)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 931)).first()
        htparam.paramgruppe = 38
        htparam.reihenfolge = 29
        htparam.bezeichnung = "Proforma Invoice Temporary AcctNo"
        htparam.fchar = ""
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2999)).first()

    if htparam.paramgruppe != 5:

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 2999)).first()
        htparam.paramgruppe = 5
        htparam.reihenfolge = 68
        htparam.bezeichnung = "Article Number for Extra Bed [eg n1;n2;n3;]"
        htparam.fchar = ""
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 893)).first()

    if htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 893)).first()
        htparam.bezeichnung = "LetterNo for Advance GUEST Bill"
        htparam.feldtyp = 1
        htparam.paramgruppe = 15
        htparam.reihenfolge = 99

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 173)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password for Posting FO VOID Item"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 810)).first()

    if re.match(".*PAYING.*",htparam.bezeichnung):

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 810)).first()
        htparam.bezeichnung = "Number of Guests(Adult + compl + ch1 + ch2)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 961)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 961)).first()
        htparam.bezeichnung = "Is Guest Title mandatory in GCF? (Def NO)"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 369)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 369)).first()
        htparam.bezeichnung = "nt_KNGfbRev.r param:D1,F1,.,F4,B1.B4;D2,F1.F4"
        htparam.feldtyp = 5
        htparam.fchar = ""


        pass

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 567)).first()

    if (not re.match(".*ACCOR.*",htparam.bezeichnung)) or htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 567)).first()
        htparam.bezeichnung = "Enable ACCOR Reports? (CNTL_P)"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 960)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 960)).first()
        htparam.paramgruppe = 27
        htparam.reihenfolge = 15
        htparam.bezeichnung = "Cutoff days for Not sending back questionnair"
        htparam.finteger = 30
        htparam.fdecimal = 0
        htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 794)).first()

    if htparam.paramgruppe != 27 or htparam.feldtyp == 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 794)).first()
        htparam.paramgruppe = 27
        htparam.reihenfolge = 13
        htparam.bezeichnung = 'Quesionnaire "EventNo;DeptNo;" for c/o guests'
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2073)).first()

    if not re.match(".*P\$L.*",htparam.bezeichnung):

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2073)).first()
        htparam.bezeichnung = "Keyword for P&L Report in Foreign Currency"
        htparam.fchar = "IN_FOREIGN"

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1072)).first()
    htparam.bezeichnung = "License for VHP Report Generator"

    htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 711)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 711)).first()
        htparam.paramgruppe = 17
        htparam.reihenfolge = 170
        htparam.bezeichnung = "(Turkish) Citizen ID Number"
        htparam.feldtyp = 5
        htparam.fchar = "TCID"

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 430)).first()

    if htparam.bezeichnung.lower()  == "Not used" or htparam.fchar == "":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 430)).first()
        htparam.bezeichnung = "Directory for Confirmation Attached File"
        htparam.fchar = "c:\\vhp\\"

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 478)).first()
    htparam.bezeichnung = "Default Rsv Stat: 0GTD 1Tent 2 == 6PM 3 == OralConf"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 948)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 948)).first()
        htparam.feldtyp = 4
        htparam.reihenfolge = 83
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Print TOTAL Food/Bev/Other Amount? (Def == NO)"
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 938)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 938)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Use 'ORAL CONFIRM' Reservation Status?"
        htparam.flogical = True
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 939)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Use 'FIRST NAME' in individual GCF?"
        htparam.flogical = True
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1200)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "User GroupNo for Engineering Department"
        htparam.finteger = 0

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1203)).first()
        htparam.bezeichnung = "Not used"

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1204)).first()
        htparam.bezeichnung = "Not used"

        htparam = db_session.query(Htparam).first()

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 152)).first()
        paramtext.ptexte = "Engineering Module"

        paramtext = db_session.query(Paramtext).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 358)).first()

    if htparam.bezeichnung.lower()  != "License for Internet Billing System":

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "License for Internet Billing System"

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 887)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Acct_No for FA A/P (default  ==  A/P Trade)"
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 793)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Transfer F/O journal for departments e.g. 0,1,2"
        htparam.feldtyp = 5
        htparam.paramgruppe = 38
        htparam.reihenfolge = 28
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 129)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 129)).first()
        htparam.bezeichnung = "Number of VACANT rooms"
        htparam.feldtyp = 5
        htparam.reihenfolge = 17
        htparam.paramgruppe = 8
        htparam.fchar = "VACANT"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1110)).first()

    if htparam.fchar == "":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1110)).first()
        htparam.bezeichnung = "Today's Billing Date"
        htparam.reihenfolge = 161
        htparam.fchar = "BillDate"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 132)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 132)).first()
        htparam.feldtyp = 5
        htparam.bezeichnung = htparam.bezeichnung + " [e.g. n1;n2;n3;]"
        htparam.fchar = trim(to_string(htparam.finteger, ">>>>9")) + ";"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 933)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 933)).first()
        htparam.bezeichnung = "Stay_Pay Nite Use AvrgRate Option? (Def NO)"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 736)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 736)).first()
        htparam.bezeichnung = "ProgName for Calculating ResNo (HV)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 431)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 431)).first()
        htparam.bezeichnung = "Default Confirmation Letter Number"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 571)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 571)).first()
        htparam.bezeichnung = "Floor Plan BOX Height x Width [eg 70 x 500]"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 968)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 968)).first()
        htparam.bezeichnung = "Search Guest Name Start Field: 0 == Name 1 == ID"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 123)).first()

    if htparam.paramgruppe != 7:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 123)).first()
        htparam.bezeichnung = "Dummy INDIVIDUAL Company GuestNo"
        htparam.paramgruppe = 7
        htparam.reihenfolge = 32
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 455)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 455)).first()
        htparam.bezeichnung = "ProgName for Money Exchange Receipt"


        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1009)).first()

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1009)).first()
    htparam.bezeichnung = "Rest. Discount ArtNo for 2nd VAT"

    if htparam.feldtyp != 1:
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 271)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 271)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Apply Multi VAT in the POS?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 764)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 764)).first()
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.reihenfolge = 78
        htparam.bezeichnung = "Summary of VAT% - VAT - Net - Amount"
        htparam.fchar = "VAT_SUM"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 237)).first()

    if htparam.paramgruppe != 9:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 237)).first()
        htparam.paramgruppe = 9
        htparam.feldtyp = 1
        htparam.bezeichnung = "Storage Duration for closed P/O"
        htparam.finteger = 60

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1012)).first()
        htparam.paramgruppe = 38
        htparam.reihe = 27
        htparam.feldtyp = 1
        htparam.bezeichnung = "G/L Transaction: MaxChar allowed for RefNo"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 325)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 325)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Create Calls Record when PABX rate  ==  0?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 172)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password for Posting Misc POS Item"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1398)).first()

    if htparam.paramgruppe != 39:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1398)).first()
        htparam.paramgruppe = 39
        htparam.bezeichnung = "Deactive YTD amount when calc JAN.DEC balance"
        htparam.feldtyp = 5
        htparam.fchar = "YTDaus"
        htparam.reihenfolge = 78

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2200)).first()

    if not htparam:
        htparam = Htparam()
        db_session.add(htparam)

        htparam.paramnr = 2200
        htparam.paramgruppe = 39
        htparam.bezeichnung = "To_date's Exchange Rate"
        htparam.feldtyp = 5
        htparam.fchar = "EXRATE"
        htparam.reihenfolge = 77

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 88)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 88)).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Print official Rest Bill (Turkey)?"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 13

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1080)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1080)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Store Stocks Onhand when closing inventory?"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 70

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 109)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 109)).first()
        htparam.bezeichnung = "Dummy Walk_in Company GuestNo"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 116)).first()

    if htparam.bezeichnung.lower()  == "Not Used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 116)).first()
        htparam.bezeichnung = "F/O SubgrpNo for unallocated C/L article"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 738)).first()

    if htparam.bezeichnung.lower()  == "Not Used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 738)).first()
        htparam.bezeichnung = "F/O Article for rounding of Bill Amount"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 262)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 262)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "No of Adult(s) for new reservation (def  ==  1)"
        htparam.finteger = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 437)).first()

    if htparam.bezeichnung.lower()  == "Not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 437)).first()
        htparam.bezeichnung = "Allow cancel Reservation after generating keycard?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 949)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 949)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Department No for MiniBar"
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 82
        htparam.paramgruppe = 19

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 716)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 716)).first()
        htparam.feldtyp = 5
        htparam.bezeichnung = "Parameters for Daily Sales Report I"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 732)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 732)).first()
        htparam.feldtyp = 5
        htparam.bezeichnung = "Parameters for Daily Sales Report II"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 297)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 297)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Change 6PM to other time, eg. 4 == 4PM (Param373)"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1047)).first()

    if htparam.feldtyp == 4 and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "F/O ArtNo for Club Initial Fee"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1048)).first()
        htparam.bezeichnung = "F/O ArtNo for Club Discount"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1049)).first()
        htparam.bezeichnung = "Create renewal .. days before expired"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1050)).first()
        htparam.bezeichnung = "Display warning for segment VIP?"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1056)).first()
        htparam.bezeichnung = "Display warning for segment Black List?"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1057)).first()
        htparam.bezeichnung = "Save Check_In history (Days)"
        htparam.feldtyp = 1
        htparam.finteger = 365

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 118)).first()

    if htparam.reihenfolge != 22:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 118)).first()
        htparam.reihenfolge = 22
        htparam.bezeichnung = "Article Number for Internet Charges"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1004)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1004)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "P/O Order Name"
        htparam.feldtyp = 5
        reihenfolge = 168
        htparam.fchar = "odname"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1005)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "P/O Order Item's Remark"
        htparam.feldtyp = 5
        reihenfolge = 169
        htparam.fchar = "bl_remark"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1064)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1064)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Subgroups for HK Onhand List (format n1;n2;)"
        htparam.feldtyp = 5
        reihenfolge = 43
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 496)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 496)).first()
        htparam.bezeichnung = "Argt Code for All Inclusive (argt1;argt2;.)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 252)).first()

    if htparam.paramgruppe != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 252)).first()
        htparam.bezeichnung = "KitchPrinter:#-Lines before cutting (def 4)"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.paramgruppe = 1
        htparam.reihenfolge = 100

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 562)).first()
        htparam.bezeichnung = "KitchPrinter:#-Lines after cutting (def 5)"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.paramgruppe = 1
        htparam.reihenfolge = 101

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1080)).first()

    if not htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1080)).first()
        htparam.bezeichnung = "Storage Number for House Keeping Items"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.paramgruppe = 21
        htparam.reihenfolge = 36

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 495)).first()

    if not re.match(".*Single Line.*",htparam.bezeichnung):

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 495)).first()
        htparam.bezeichnung = "LetterNo MasterBill Single Line - Foreign Currency"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 208)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 208)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Allow opened Master Bill when all guests C/O?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2076)).first()
    htparam.bezeichnung = "YTD option for Monthly Balance (PnL Acct)"
    htparam.fchar = "YTDein"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1099)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1099)).first()
        htparam.paramgruppe = 27
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Send email to guest when guest checks out?"
        htparam.reihenfolge = 12

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1071)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password for Parameter Group 10 (Password)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 239)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 47)).first()
        htparam.reihenfolge = 16

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 239)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Above xx rooms (param 97, default  ==  20)"
        htparam.reihenfolge = 15
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 418)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "Output Directory for F/O & G/L Excel Report"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 170)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password of Excel .xls files - F/O Reports"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 171)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password of Excel .xls files - G/L Reports"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 932)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 932)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Generate F/O BillNo when guest C/I (def == NO)?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1060)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1060)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "User GroupNo for Engineering Department"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1061)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Storage Number for Engineering Department"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1062)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Engineering's Cost Department Number"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2401)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2401)).first()
        htparam.paramgruppe = 17
        htparam.reihenfolge = 157
        htparam.bezeichnung = "Current User Name"
        htparam.feldtyp = 5
        htparam.fchar = "UserName"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 550)).first()
        htparam.bezeichnung = "Use Advance Contract Rate Setup (PRO Version)?"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 549)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 549)).first()
        htparam.bezeichnung = "Rate Disc: 0 == Average 1 == As_Is 2 == Min 3 == Max"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.reihenfolge = 11

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 739)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 739)).first()
        htparam.reihenfolge = 427
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Ask Bill counter number when closing the bill?"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 179)).first()

    if htparam.paramgruppe != 8:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 179)).first()
        htparam.paramgruppe = 8
        htparam.reihenfolge = 183
        htparam.bezeichnung = "Room Number of selected Room Type"
        htparam.feldtyp = 5
        htparam.fchar = "RM_RMCAT"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 85)).first()

    if htparam.paramgruppe != 8:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 85)).first()
        htparam.paramgruppe = 8
        htparam.reihenfolge = 179
        htparam.bezeichnung = "Arrivals thru Reservation (Rooms)"
        htparam.feldtyp = 5
        htparam.fchar = "RM_RSV"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 86)).first()
        htparam.paramgruppe = 8
        htparam.reihenfolge = 180
        htparam.bezeichnung = "Arrivals thru Reservation (Adults)"
        htparam.feldtyp = 5
        htparam.fchar = "PRS_RSV"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 106)).first()
        htparam.paramgruppe = 8
        htparam.reihenfolge = 181
        htparam.bezeichnung = "Arrivals thru Walk_in Guest (Rooms)"
        htparam.feldtyp = 5
        htparam.fchar = "RM_WIG"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 107)).first()
        htparam.paramgruppe = 8
        htparam.reihenfolge = 182
        htparam.bezeichnung = "Arrivals thru Walk_in Guest (Adults)"
        htparam.feldtyp = 5
        htparam.fchar = "PRS_WIG"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 833)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 833)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "Cash Payment: USE Multi_Currency Mode?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 830)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 830)).first()
        htparam.feldtyp = 5
        htparam.bezeichnung = "MultiCurr Total Amount in bill (eg. USD;EURO)"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 874)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 874)).first()
        htparam.feldtyp = 4
        htparam.bezeichnung = "POS Bill: Always print all items? (roll printer)"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1040)).first()

    if htparam.feldtyp != 1:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 149)).first()
        paramtext.ptexte = "CLUB Module"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1040)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Max number of member freezing allowed"
        htparam.finteger = 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1041)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Max age valid for Child/Junior Member"
        htparam.finteger = 16

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1042)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Club Opening Hour (1 - 24)"
        htparam.finteger = 6

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1044)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Club Closing Hour (1 - 24)"
        htparam.finteger = 22

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1045)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "Department number of the CLUB"
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1046)).first()
        htparam.feldtyp = 1
        htparam.bezeichnung = "F/O ArtNo for Club Membership Fee"
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 928)).first()

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "Read Card: get direct result? (VHPIF -> YES)"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1114)).first()

    if htparam.bezeichnung.lower()  != "License for CLUB Software":
        htparam.feldtyp = 4
        htparam.bezeichnung = "License for CLUB Software"
        htparam.flogical = False
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "License for Membership Card"
        htparam.flogical = False
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 872)).first()

    if htparam.feldtyp != 5:
        htparam.feldtyp = 5
        htparam.bezeichnung = "Description for VAT on the POS Bill"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 395)).first()

    if htparam.paramgruppe != 38:
        htparam.paramgruppe = 38
        htparam.feldtyp = 5
        htparam.bezeichnung = "G/L AcctNo for A/P Others (Optional)"
        htparam.reihenfolge = 26
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1079)).first()

    if htparam.paramgruppe != 19:
        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.bezeichnung = "Waiter transfer: Ask waiter passwd? (DEF NO)"
        htparam.reihenfolge = 424
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 799)).first()

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "RegNo for C/I guests? (DEF NO, bill.rechnr2)"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1077)).first()

    if htparam.feldtyp != 5:
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.reihenfolge = 2318
        htparam.bezeichnung = "Inhouse Guest Registration No (Param 799)"
        htparam.fchar = "RegNo"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1078)).first()

    if htparam.feldtyp != 5:
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.reihenfolge = 2319
        htparam.bezeichnung = "RmRate Discount (%) to publish rate"
        htparam.fchar = "RateDisc"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 857)).first()
    htparam.bezeichnung = "Print Discount AFTER sales items?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    htparam.bezeichnung = "Local Currency Code (Short Form)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1063)).first()

    if htparam.paramgruppe != 17:
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.bezeichnung = "Print Bill: Skip to Line (e.g. $ROW50)"
        htparam.reihenfolge = 2317
        htparam.fchar = "ROW"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 936)).first()

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is Deposit mandatory in the reservation?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 937)).first()

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "Read Birthdate from the Guest ID?"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 970)).first()

    if htparam.feldtyp != 1:
        htparam.feldtyp = 1
        htparam.bezeichnung = "Max Hours for Day_Use w/o Disc_Rate Control"
        htparam.finteger = 3

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2311)).first()
    htparam.bezeichnung = "Current Time"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2312)).first()
    htparam.bezeichnung = "Current User ID"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1117)).first()
    htparam.bezeichnung = "Bill_line User ID"
    htparam.feldtyp = 5
    htparam.fchar = "bl_usrinit"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 967)).first()

    if htparam.paramgruppe != 38:
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Consider Table gl_coa for HOTEL/CONDOTEL P&L?"
        htparam.feldtyp = 4
        htparam.reihenfolge = 25
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 195)).first()

    if htparam.paramgruppe != 8:
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Average Stay (in nights) of Paying Guests"
        htparam.feldtyp = 5
        htparam.reihenfolge = 13
        htparam.fchar = "AVRG_STAY"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 318)).first()
    htparam.reihenfolge = 99

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 192)).first()

    if htparam.paramgruppe != 8:
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Total Food Cover of selected department"
        htparam.feldtyp = 5
        htparam.reihenfolge = 15
        htparam.fchar = "F_COVER"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 197)).first()

    if htparam.paramgruppe != 8:
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Total Beverage Cover of selected department"
        htparam.feldtyp = 5
        htparam.reihenfolge = 16
        htparam.fchar = "B_COVER"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 83)).first()
    htparam.bezeichnung = "Pop up warning when transactions go over limit?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 564)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 564)).first()
        htparam.bezeichnung = "Default Room Availability SET to after allotment?"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 480)).first()

    if htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 480)).first()
        htparam.paramgruppe = 15
        htparam.bezeichnung = "LetterNo for Advance Bill II (option)"
        htparam.feldtyp = 1
        htparam.reihenfolge = 98

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 419)).first()
    htparam.bezeichnung = "LetterNo debt list Invoice (Non Stay Guest)"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 424)).first()
    htparam.bezeichnung = "LetterNo for debt list's Invoice"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 321)).first()
    htparam.bezeichnung = "MaxChar length for Name_Display (def 32)"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 752)).first()
    htparam.bezeichnung = "Out_of_Service"
    htparam.feldtyp = 5
    htparam.fchar = "OOS"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 187)).first()
    htparam.bezeichnung = "Arrivals (Room)"
    htparam.feldtyp = 5
    htparam.fchar = "RM_ARR"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 188)).first()
    htparam.bezeichnung = "Arrivals (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS_ARR"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 189)).first()
    htparam.bezeichnung = "Departures (Room)"
    htparam.feldtyp = 5
    htparam.fchar = "RM_DEP"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 190)).first()
    htparam.bezeichnung = "Departures (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS_DEP"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 191)).first()
    htparam.bezeichnung = "Number of VIP Guests"
    htparam.feldtyp = 5
    htparam.fchar = "VIP"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 193)).first()
    htparam.bezeichnung = "Reservation Made Today (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "NEW_RES"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 194)).first()
    htparam.bezeichnung = "Cancellation Today (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "CANC_RES"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 211)).first()
    htparam.bezeichnung = "Arrivals Tommorow (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "RM_ARRTMR"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 231)).first()
    htparam.bezeichnung = "Arrival Tomorrows (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS_ARRTMR"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 750)).first()
    htparam.bezeichnung = "Departure Tomorrow (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "RM_DEPTMR"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 751)).first()
    htparam.bezeichnung = "Departure Tomorrow (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS_DEPTMR"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 969)).first()
    htparam.bezeichnung = "No_Show Rooms"
    htparam.feldtyp = 5
    htparam.fchar = "NOSHOW"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 742)).first()

    if htparam.paramgruppe != 8:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 742)).first()
        htparam.paramgruppe = 8
        htparam.reihenfolge = 178
        htparam.bezeichnung = "Early Checkout (Rooms)"
        htparam.feldtyp = 5
        htparam.fchar = "EARLY_CO"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 570)).first()
    htparam.bezeichnung = "Minibar Department No (needed by PABX IF)"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 724)).first()
    htparam.bezeichnung = "Auto Update Billing Date when signing on?"
    htparam.paramgruppe = 24
    htparam.feldtyp = 4
    htparam.reihenfolge = 10

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 904)).first()
    htparam.bezeichnung = "Default C/L payment ArtNo"
    htparam.paramgruppe = 24
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 17)).first()
    htparam.bezeichnung = "Service Charge Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 18)).first()
    htparam.bezeichnung = "Sinking Fund Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 500)).first()
    htparam.bezeichnung = "LetterNo Invoicing - ServiceCharge"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 613)).first()
    htparam.bezeichnung = "LetterNo Invoicing - Water & Electricity"
    htparam.paramgruppe = 24
    htparam.feldtyp = 1
    htparam.reihenfolge = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 981)).first()
    htparam.bezeichnung = "License for Condominium"

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 147)).first()
    paramtext.ptexte = "Condominium Admin"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 796)).first()

    if htparam.feldtyp != 5:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 500)).first()
        htparam.bezeichnung = "Not used"

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 796)).first()
        htparam.paramgruppe = 24
        htparam.bezeichnung = "Label for Tenant Card Type"
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 797)).first()
        htparam.paramgruppe = 24
        htparam.bezeichnung = "Label for Company Card Type"
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 798)).first()
        htparam.paramgruppe = 24
        htparam.bezeichnung = "Label for Owner Card Type"
        htparam.feldtyp = 5

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 934)).first()
        htparam.paramgruppe = 24
        htparam.bezeichnung = "F/O Article No for Service Charge"
        htparam.feldtyp = 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 935)).first()
        htparam.paramgruppe = 24
        htparam.bezeichnung = "F/O Article No for Sinking Fund"
        htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 17)).first()
    htparam.bezeichnung = "Service Charge Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 18)).first()
    htparam.bezeichnung = "Sinking Fund Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 17)).first()

    if htparam.feldtyp != 5:
        htparam.bezeichnung = "ServCharge Unit Fee by AptType(xx;yy;.;)"
        htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 18)).first()

    if htparam.feldtyp != 5:
        htparam.bezeichnung = "Sinking Fund Unit Fee by AptType(xx;yy;.;)"


    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 728)).first()
    htparam.bezeichnung = "Name Display: Send Sharer Name to PABX?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()
    htparam.bezeichnung = "ProgPath of LnL *.lst files (def. \\vhp\\LnL\\)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 242)).first()
    htparam.bezeichnung = "Subgroup No for F/O Paid_Out Billing Article"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 320)).first()

    if htparam:

        if htparam.bezeichnung.lower()  == "Not used" or htparam.paramgruppe != 14:

            htparam = db_session.query(Htparam).first()
            htparam.paramgruppe = 14
            htparam.bezeichnung = "Block new reservation when A/R Over CrLimit?"
            htparam.flogical = False

            htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 333)).first()
    htparam.bezeichnung = "PDA MC Reader Start Char Position (Param 336)"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 334)).first()
    htparam.bezeichnung = "PDA MC Reader End Char Position (Param 336)"
    htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 376)).first()
    htparam.bezeichnung = "Print Net&VAT amt for CASH & CC payment?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 829)).first()
    htparam.bezeichnung = "Word Program Name for Param 825"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 825)).first()
    htparam.bezeichnung = "Print Total POS bill amount in Word?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 824)).first()
    htparam.bezeichnung = "Exclude Tax&Service for Compliment Payment?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 314)).first()
    htparam.bezeichnung = "PAUSE in SEC for ifstart.r (min == 2 max == 10)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 323)).first()
    htparam.bezeichnung = "Check duplicate calls record in ifstart.r?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 312)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 312)).first()
        htparam.bezeichnung = "Debugging Mode for ifstart.r (0  ==  No Debug)"
        htparam.feldtyp = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 186)).first()

    if htparam.feldtyp != 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 186)).first()
        htparam.bezeichnung = "Hotel Opening ( ==  statistic starting) Date"
        htparam.fdate = None
        htparam.feldtyp = 3

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 236)).first()
    htparam.bezeichnung = "N/A allowed with opened restaurant bill(s)?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1076)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1076)).first()
        htparam.bezeichnung = "Control C/O time when Checking out the guest?"
        htparam.flogical = False


        htparam.feldtyp = 4

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 373)).first()
    htparam.bezeichnung = "Change 6PM_Rsv Status to No_Show after 6PM?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1589)).first()
    htparam.paramgruppe = 17
    htparam.reihenfolge = 156
    htparam.bezeichnung = "Bill_line Voucher"
    htparam.fchar = "bl_voucher"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 244)).first()

    if htparam.feldtyp != 5:
        htparam.bezeichnung = "External Main Program Filename (CNTRL_P)"
        htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1103)).first()
    htparam.bezeichnung = "Bill_Line arrival date"
    htparam.paramgruppe = 17
    htparam.reihenfolge = 2315
    htparam.fchar = "bl_arrive"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1104)).first()
    htparam.bezeichnung = "Bill_line departure date"
    htparam.paramgruppe = 17
    htparam.reihenfolge = 2316
    htparam.fchar = "bl_depart"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1083)).first()

    if htparam.bezeichnung.lower()  != "Store Duration for FB Compliment":
        htparam.bezeichnung = "Store Duration for FB Compliment"
        htparam.finteger = 180

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 814)).first()
    htparam.bezeichnung = "No of Persons for selected Segment"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 753)).first()
    htparam.bezeichnung = "Number of ADULT guest"
    htparam.fchar = "NUMADULT"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 754)).first()
    htparam.bezeichnung = "Number of CHILD1 guest"
    htparam.fchar = "NUMCHLD1"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 755)).first()
    htparam.bezeichnung = "Number of CHILD2 guest"
    htparam.fchar = "NUMCHLD2"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 756)).first()
    htparam.bezeichnung = "No of Adults for selected Segment"
    htparam.fchar = "SEGADULT"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 757)).first()
    htparam.bezeichnung = "No of Child1 for selected Segment"
    htparam.fchar = "SEGMCH1"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 758)).first()
    htparam.bezeichnung = "No of Child2 for selected Segment"
    htparam.fchar = "SEGMCH2"
    htparam.feldtyp = 5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 230)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 230)).first()
        htparam.bezeichnung = "Should the system store N/A daily outputs?"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 238)).first()
        htparam.bezeichnung = "If 230 == YES, Enter store duration (Days)"
        htparam.feldtyp = 1
        htparam.finteger = 180

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 497)).first()
    htparam.bezeichnung = "LetterNo for Single Line NS Bill (option)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 413)).first()

    if htparam.paramgruppe != 17:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 414)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Number of Night Stay"
        htparam.feldtyp = 5
        htparam.fchar = "Nites"
        htparam.reihenfolge = 49

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 413)).first()
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Mobile Number"
        htparam.feldtyp = 5
        htparam.fchar = "HP_No"
        htparam.reihenfolge = 85

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 465)).first()
    htparam.bezeichnung = "Ask Invoice Counter# when printing the bill?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 432)).first()

    if htparam.feldtyp != 1:
        htparam.feldtyp = 1
        htparam.bezeichnung = "LetterNo for Printing Hotel Guest Passport"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 219)).first()
    htparam.bezeichnung = "Closed Bill: Enable to change billing date?"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1086)).first()

    if htparam.bezeichnung.lower()  == "Not Used":
        htparam.bezeichnung = "Max F/O Unit Price in local currency"
        htparam.feldtyp = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 688)).first()
    htparam.bezeichnung = "LetterNo for Master Bill Single Line (Option)"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()
    htparam.bezeichnung = "Rest. ArtNo for other type of Discount"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 148)).first()

    if htparam.feldtyp != 5:
        htparam.feldtyp = 5
        htparam.bezeichnung = "ExtChar xx for mk_gcfxx.p and chg_gcfxx.p"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 141)).first()

    if trim(htparam.bezeichnung) == "":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 141)).first()
        htparam.bezeichnung = "C/L Payment when no Credit Facility yet"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 185)).first()

    if htparam.bezeichnung.lower()  == "Not Used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 185)).first()
        htparam.fchar = ".LYTODAY"
        htparam.bezeichnung = "Last Year TODAY Value"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 415)).first()

    if htparam.feldtyp != 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 415)).first()
        htparam.reihenfolge = 125
        htparam.bezeichnung = "2nd LetterNo for Master Bill"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 416)).first()
        htparam.reihenfolge = 21
        htparam.bezeichnung = "Word Prog for foreign amt balance (Param 415)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 68)).first()

    if htparam.feldtyp != 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 68)).first()
        htparam.fdecimal = htparam.finteger
        htparam.feldtyp = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()
    htparam.bezeichnung = "Rest Article for the VOUCHER"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1201)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1201)).first()
        htparam.paramgruppe = 38
        htparam.bezeichnung = "G/L AcctNo for WIP (Stock Transform)"
        htparam.feldtyp = 5
        htparam.reihenfolge = 24
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 43)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Receiving and Outgoing: SHOW UNIT PRICE?"
        htparam.feldtyp = 4
        htparam.reihenfolge = 7
        htparam.finteger = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 138)).first()

    if htparam.bezeichnung.lower()  == "Not Used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 138)).first()
        htparam.bezeichnung = "ArtNo with Cash Receipt Printout [A1;A2;..]"

        if htparam.feldtyp != 5:
            htparam.feldtyp = 5
            htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 127)).first()

    if htparam:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "V.A.T. included in Room Rate ?"

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 128)).first()

    if htparam:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Service included in Room Rate ?"

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()

    if htparam:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Article's Service charge is VAT chargeable"

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 483)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 483)).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 4
        htparam.bezeichnung = "Article's tax is VAT chargeable"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 740)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 740)).first()
        htparam.paramgruppe = 7
        htparam.reihenfolge = 419
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) Journal Voucher Approval by System (01;xx;99)"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1378)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Statistic Budget Articles(<Keyword>-<Department>-<ArticleNr>;xxxx;)"
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.reihenfolge = 34

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1343)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Transfer BI to Head Office IP:Port"
        htparam.feldtyp = 5
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.reihenfolge = 35

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 259)).first()

    if htparam.feldtyp != 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 259)).first()
        htparam.paramgruppe = 10
        htparam.feldtyp = 5
        htparam.bezeichnung = "Password For Posting Room Charge"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 676)).first()

    if htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.reihenfolge = 84
        htparam.feldtyp = 5
        htparam.bezeichnung = "Parameter for Print Deposit, Refund, Void [D == 1,2,;..]"
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 494)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 494)).first()
        htparam.paramgruppe = 7
        htparam.reihenfolge = 98
        htparam.feldtyp = 4
        htparam.bezeichnung = "Automatically changing the room rate in the FixedRate screen"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 493)).first()

    if htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 493)).first()
        htparam.paramgruppe = 7
        htparam.reihenfolge = 97
        htparam.feldtyp = 4
        htparam.bezeichnung = "Automatically deleting the fixed rate"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 459)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 27
        htparam.reihenfolge = 26
        htparam.feldtyp = 4
        htparam.bezeichnung = "The room rate is calculated based on room category"
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 792)).first()

    if htparam.paramgruppe != 38:
        htparam.feldtyp = 5
        htparam.bezeichnung = "Password for Creating Supplier"
        htparam.paramgruppe = 10

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 396)).first()

    htparam = db_session.query(Htparam).first()
    htparam.paramgruppe = 7
    htparam.reihenfolge = 24
    htparam.feldtyp = 1
    htparam.bezeichnung = "Article for CSR Donation (Tauzia Property's)"

    htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 458)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "Minimum Stay For Repeater Guest"
        htparam.reihenfolge = 403


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 792)).first()

    if htparam.paramgruppe != 38:
        htparam.feldtyp = 5
        htparam.bezeichnung = "Password for Creating Supplier"
        htparam.paramgruppe = 10

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 235)).first()

    if htparam.bezeichnung.lower()  == "not used" or htparam.bezeichnung.lower()  == "":

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Access Right to release P/O (2 or 3, def  ==  2)"
        htparam.paramgruppe = 21
        htparam.feldtyp = 1
        htparam.reihenfolge = 8
        htparam.finteger = 2

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 243)).first()

    if htparam.bezeichnung.lower()  == "not used" or htparam.bezeichnung.lower()  == "":

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Access Right to Approve DML (2 or 3, def  ==  2)"
        htparam.paramgruppe = 21
        htparam.feldtyp = 1
        htparam.reihenfolge = 9
        htparam.finteger = 2

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 473)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate For Villa Setup"
        htparam.reihenfolge = 406


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 451)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 5
        htparam.bezeichnung = "Restaurant Articles for SC Discount [eg n1;n2;n3]"
        htparam.reihenfolge = 73
        htparam.fchar = " "


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 452)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 5
        htparam.bezeichnung = "Rest. for VAT, SC and Other Taxes [eg n1;n2;n3]"
        htparam.reihenfolge = 74
        htparam.fchar = " "


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 461)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 5
        htparam.bezeichnung = "Billing Articles for SC Discount [eg n1;n2;n3]"
        htparam.reihenfolge = 72
        htparam.fchar = " "


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 462)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 2
        htparam.bezeichnung = "Discount in % for SC Discount"
        htparam.reihenfolge = 75
        htparam.fdecimal = 0


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 466)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "Keep Guest Profile (if using GDPR  ==  xxx days)"
        htparam.reihenfolge = 396


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 346)).first()

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activated GDPR Rules"
        htparam.reihenfolge = 86
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1345)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "No. of ISO nationality code"
        htparam.reihenfolge = 2324


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 615)).first()

    if htparam.bezeichnung.lower()  == "not used" and htparam.reihenfolge == 417:

        htparam = db_session.query(Htparam).first()
        htparam.bezeichnung = "Dummy Guest Card for OTA"
        htparam.paramgruppe = 7
        htparam.feldtyp = 5
        htparam.reihenfolge = 417
        htparam.fchar = "1"

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1020)).first()

    if htparam.paramgruppe != 23 and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 23
        htparam.feldtyp = 5
        htparam.bezeichnung = "Ratecode Room For Reservation Banquet"
        htparam.reihenfolge = 29
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1073)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR Dashboard Mobile"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1077

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1055)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR Mobile CI/CO"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1078

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 344)).first()

    if htparam.paramgruppe != 7:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Article number can not be split item (99;xx;)"
        htparam.feldtyp = 5
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 2325

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 486)).first()

    if htparam.paramgruppe != 27:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 27
        htparam.bezeichnung = "Calculating ratecode based on occupancy"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 27

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 467)).first()

    if htparam:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Date format for web version"
        htparam.feldtyp = 5
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 2326

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 390)).first()

    if htparam and htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Automatically to approve DML"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 74

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 370)).first()

    if htparam and htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Automatically to blocking budget"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 75

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 450)).first()

    if htparam and htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Show Subgroup in Kitchen Printer"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 429

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 747)).first()

    if htparam.bezeichnung.lower()  == "not used":
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2327
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) can be attached contract rate (01;xx;99)"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 598)).first()

    if htparam.bezeichnung.lower()  == "not used":
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2328
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) can be modify rate code (01;xx;99)"
        htparam.fchar = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 80)).first()

    if htparam.bezeichnung.lower()  == "not used":
        htparam.paramgruppe = 40
        htparam.reihenfolge = 102
        htparam.feldtyp = 4
        htparam.bezeichnung = "Show Pickup Required to Web Pre_checkin"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 345)).first()

    if htparam.bezeichnung.lower()  == "not used":
        htparam.paramgruppe = 13
        htparam.reihenfolge = 39
        htparam.feldtyp = 5
        htparam.bezeichnung = "Departement To Billing Charges - IPTV Interface"
        htparam.fchar = " "

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 735)).first()

    if htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 7:
        htparam.paramgruppe = 7
        htparam.reihenfolge = 420
        htparam.feldtyp = 4
        htparam.bezeichnung = "Blocking Resevation Without Ratecode"
        htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 360)).first()

    if htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 7:
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2329
        htparam.feldtyp = 5
        htparam.bezeichnung = "Currency conventer (1;2;xxx;)"
        htparam.fchar = " "

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 953)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 953)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Self CI Apps"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1079
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 954)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 954)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Broadcast Notification MCI "
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1080
        htparam.fchar = ""

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1021)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1021)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Adjustment Inventory Greather Than Actual Qty ?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 76

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 477)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 7
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Activated Marketing Features ?"
        htparam.reihenfolge = 397


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1344)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 4:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "V.A.T Code 16"
        htparam.reihenfolge = 22


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1346)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 4:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "V.A.T Code 17"
        htparam.reihenfolge = 23


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1347)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 4:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "V.A.T Code 18"
        htparam.reihenfolge = 24


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1348)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 4:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "V.A.T Code 19"
        htparam.reihenfolge = 25


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1349)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 4:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.fint = 0
        htparam.bezeichnung = "V.A.T Code 20"
        htparam.reihenfolge = 26


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 90)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 15
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Date Split Activation For Fixed Rate"
        htparam.reihenfolge = 137


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1350)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Activated guest search is 100 % same"
        htparam.reihenfolge = 87


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1351)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "RoomNo must be entered when pay use room transfer"
        htparam.reihenfolge = 430


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1352)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 3:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 3
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Group for Night Audit Program (web version only)"
        htparam.reihenfolge = 21


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1353)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 5:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Article Number for Deposit (SelfCheckin)"
        htparam.reihenfolge = 76


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1354)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 21
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Receiving is not allowed greather than date of created PO"
        htparam.reihenfolge = 77


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1355)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 3:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 3
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Activated system date using server date"
        htparam.reihenfolge = 22


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1357)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1357)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for VHP Self Order"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1081

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1358)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1358)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for VHP PreArrival Checkin"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1082

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1359)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1359)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for VHP Business Intelligence(BI)"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1083

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1356)).first()

    if htparam.paramgruppe != 7:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1356)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Description For RefNo Number 2"
        htparam.fchar = " "
        htparam.feldtyp = 5
        htparam.reihenfolge = 2330

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1342)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1342)).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Allow Posting at One Table From Several Waiter(s)"
        htparam.flogical = True
        htparam.feldtyp = 4
        htparam.reihenfolge = 431

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1360)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1360)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Is Partial Inventory Closing Allowed?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 78

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 50)).first()

    if htparam.paramgruppe != 38:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 50)).first()
        htparam.paramgruppe = 38
        htparam.bezeichnung = "G/L AcctNo for Journal A/R (ABI)"
        htparam.fchar = " "
        htparam.feldtyp = 5
        htparam.reihenfolge = 36

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 147)).first()

    if htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 147)).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Sort by SubGroup in Kitchen Printer?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 432

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 485)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 485)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "SegmentCode OTA to Room Production Report (OTA;xxx)"
        htparam.fchar = " "
        htparam.feldtyp = 5
        htparam.reihenfolge = 2331

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 71)).first()

    if htparam.paramgruppe != 21:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 71)).first()
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Actived 4 Approval for PO"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 79

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 561)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 561)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Maximum Time Day Use In ABF List (05:00)"
        htparam.fchar = " "
        htparam.flogical = False
        htparam.finteger = 0
        htparam.feldtyp = 5
        htparam.reihenfolge = 2332

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 586)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 586)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Minimum Balance For Cashless NS Guest Bill"
        htparam.fdecimal = 0
        htparam.feldtyp = 2
        htparam.reihenfolge = 2333

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 5:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 5
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Article Number for Deposit (Restaurant)"
        htparam.reihenfolge = 77


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 978)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 6:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.finteger = 0
        htparam.bezeichnung = "MainGroup to be displayed on the VHP Cloud [eg. D1:1,2,xx;]"
        htparam.reihenfolge = 77


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 583)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 9:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 9
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Store Duration for GuestBook"
        htparam.flogical = False
        htparam.reihenfolge = 269


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.finteger = 0
        htparam.bezeichnung = "Activate Restaurant Deposit"
        htparam.flogical = False
        htparam.reihenfolge = 433


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1022)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1022)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Cashless Payment"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1084
        htparam.fchar = " "

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 589)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 589)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Activate User Access For Nonstay Guest Bill"
        htparam.fdecimal = 0
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 2334

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 594)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 594)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Activate Dialog Queuing Room List"
        htparam.fdecimal = 0
        htparam.feldtyp = 4
        htparam.flogical = True
        htparam.reihenfolge = 2335

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 174)).first()
    htparam.feldtyp = 5
    htparam.bezeichnung = "NS Cashless Minimum Balance Post as Revenue"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 438)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 15:

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 15
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.bezeichnung = "List of Standard Letter No vhpCloud [eg. 1;2;x;x]"
        htparam.reihenfolge = 138


        pass

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1204)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1204)).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Access for Setup Restaurant Articles"
        htparam.fdecimal = 0
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 434

        htparam = db_session.query(Htparam).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1204)).first()

    if htparam:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1204)).first()
        htparam.bezeichnung = "Disable Access for Setup Restaurant Articles"

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 838)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used" and htparam.paramgruppe != 19:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 838)).first()
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Sort by SubGroup Priority in Kitchen Printer?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 435

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 448)).first()

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.bezeichnung = "Regions complying GDPR rules [eg. 1;2;x;x]"
        htparam.reihenfolge = 88
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 449)).first()

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).first()
        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.bezeichnung = "Nationality complying GDPR rules [eg. 1;2;x;x]"
        htparam.reihenfolge = 89
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1023)).first()

    if htparam.paramgruppe != 99:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1023)).first()
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Salesboard Interface"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1085
        htparam.fchar = " "

        htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 585)).first()

    if htparam and htparam.bezeichnung.lower()  == "not used":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 585)).first()
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Activate User Access for Release OOO Room"
        htparam.fdecimal = 0
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 2336

        htparam = db_session.query(Htparam).first()

    return generate_output()