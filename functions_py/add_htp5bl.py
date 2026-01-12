# using conversion tools version: 1.0.0.119
"""_yusufwijasena_09/01/2026

        remark: - fix python indentation
                - added new update for new htparam 
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Paramtext


def add_htp5bl():

    prepare_cache([Htparam, Paramtext])

    htparam = paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, paramtext

        return {}

    def adjust_htparam(inp_reihenfolge: int):

        nonlocal htparam, paramtext

        temp_reihenfolge: int = 0
        b_htparam = None
        B_htparam = create_buffer("B_htparam", Htparam)

        b_htparam = get_cache(Htparam, {"reihenfolge": [
                              (eq, inp_reihenfolge)], "paramnr": [(ne, htparam.paramnr)]})

        if b_htparam:
            temp_reihenfolge = htparam.reihenfolge
            htparam.reihenfolge = 999999
            b_htparam.reihenfolge = temp_reihenfolge
            htparam.reihenfolge = inp_reihenfolge

        else:
            htparam.reihenfolge = inp_reihenfolge

    htparam = get_cache(Htparam, {"paramnr": [(eq, 41)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 6
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Membership points:0=guest 1=reserve,2=booker"
        htparam.reihenfolge = 83

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1074)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1074)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Order Taker Mobile"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1075
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1075)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1075)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for HouseKeeping Mobile"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1076
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 30)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 5
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Misc. Article Number for Booking Engine"
        htparam.reihenfolge = 69

    htparam = get_cache(Htparam, {"paramnr": [(eq, 786)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 786)]})
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2320
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) A/P Approval by System (01;xx;99)"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 279)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 279)]})
        htparam.paramgruppe = 6
        htparam.reihenfolge = 69
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is GCF's Mobile-No Mandatory upon C/I?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 930)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 930)]})
        htparam.bezeichnung = "Max allowed extended c/o time [HH:MM]"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 78)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 78)]})
        htparam.bezeichnung = "Web CI (IP;Port;Website)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 79)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 79)]})
        htparam.bezeichnung = "LetterNo for WebCI email (NAT,No;..;DEF,No)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 787)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 787)]})
        htparam.bezeichnung = "Loyalty Setup eg loyaltyui.r|Silver,1;Gold,2"
        htparam.feldtyp = 5
        htparam.fchar = ""

    else:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 787)]})
        htparam.bezeichnung = "Loyalty Name & types eg GHS-Silver,1;Gold,2"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 789)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 789)]})
        htparam.bezeichnung = "Loyalty Setup"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 453)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 453)]})
        htparam.bezeichnung = "CashRefund & Rebate Articles [c1,.;r1,r2.]"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 299)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 299)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Golf Module"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 110
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 454)]})

    if not matches(htparam.bezeichnung, r"*Main Group*"):

        htparam = get_cache(Htparam, {"paramnr": [(eq, 454)]})
        htparam.bezeichnung = "Main Group No for Disc Articles"
        htparam.finteger = 0
        htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1034)]})

    if htparam.paramgruppe != 38:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1034)]})
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Digit number of G/L main acct (default 4)"
        htparam.finteger = 0
        htparam.reihenfolge = 33
        htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1341)]})

    if htparam.paramgruppe == 30:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1341)]})
        htparam.paramgruppe = 15
        htparam.bezeichnung = "LetterNo for Bill's Term&Condition"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 974)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "C/O w/ unbalanced bill allowed? (def=No)"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = get_cache(Htparam, {"paramnr": [(eq, 393)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "User PSWD expiry after xx days (def=0)"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 394)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Next PSWD expired date (param 393)"
        htparam.feldtyp = 3
        htparam.fdate = None

    htparam = get_cache(Htparam, {"paramnr": [(eq, 929)]})

    if htparam.paramgruppe == 25:

        htparam.bezeichnung = "Add Keycard Program ($KCard1=xx#$KCard2=yy)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 19)]})

    if htparam.paramgruppe != 38:

        htparam.paramgruppe = 38
        htparam.bezeichnung = "Access Right 3 required to modify GL Journal?"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 32

    htparam = get_cache(Htparam, {"paramnr": [(eq, 277)]})

    if htparam.paramgruppe != 9:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 277)]})
        htparam.paramgruppe = 9
        htparam.bezeichnung = "Save FO statistic (762 / 2000 days)"
        htparam.feldtyp = 1
        htparam.finteger = 762
        htparam.fchar = ""
        htparam.reihenfolge = 267

        htparam = get_cache(Htparam, {"paramnr": [(eq, 371)]})
        htparam.paramgruppe = 9
        htparam.bezeichnung = "Save system log files (60 / 180 days)"
        htparam.feldtyp = 1
        htparam.finteger = 60
        htparam.fchar = ""
        htparam.reihenfolge = 268

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2843)]})

    if htparam and htparam.paramgruppe != 38:

        htparam.paramgruppe = 38
        htparam.bezeichnung = "Transfer GL to Head Office IP:Port"
        htparam.feldtyp = 5
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.reihenfolge = 31

    htparam = get_cache(Htparam, {"paramnr": [(eq, 51)]})

    if htparam and htparam.paramgruppe != 15:

        htparam.paramgruppe = 15
        htparam.bezeichnung = "Letter No for RC Term & Condition"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.reihenfolge = 136

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1102)]})

    if htparam and htparam.paramgruppe != 99:

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR VHP Mobile"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1074

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1013)]})
    htparam.paramgruppe = 27
    htparam.feldtyp = 5
    htparam.bezeichnung = "Rounding Rate amount for the Child Rate Codes?"
    htparam.reihenfolge = 23

    if htparam.fchar == "":
        htparam.fchar = to_string(htparam.finteger) + ";0"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 834)]})

    htparam = get_cache(Htparam, {"paramnr": [(eq, 834)]})
    htparam.feldtyp = 4
    htparam.bezeichnung = "Allow Cashless Transaction using Pre-paid card?"
    htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 569)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 569)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Restaurant Article for Cashless Payment"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 472)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 472)]})
        htparam.paramgruppe = 99
        htparam.feldtyp = 4
        htparam.bezeichnung = "License for Guest ID scan Program"
        htparam.flogical = False
        htparam.reihenfolge = 108
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 368)]})

    if htparam.paramgruppe != 24:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 368)]})
        htparam.paramgruppe = 24
        htparam.feldtyp = 5
        htparam.bezeichnung = "APT ArtNo for Water;Electricity;VAT"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 256)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 256)]})
        htparam.paramgruppe = 10
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate Strong VHP User Password Mode?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1109)]})

    if htparam.paramgruppe != 27:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1109)]})
        htparam.paramgruppe = 27
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate Guest Command? (Table guest-remark)"
        htparam.flogical = False
        htparam.reihenfolge = 25

    htparam = get_cache(Htparam, {"paramnr": [(eq, 991)]})
    htparam.bezeichnung = "License for General Cashier"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1006)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1006)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Default SOB for Walk-in Guest"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 719)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 719)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Cut-off-days of Banquet Booking (in days)"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1373)]})

    if htparam.paramgruppe != 15:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1373)]})
        htparam.paramgruppe = 15
        htparam.feldtyp = 5
        htparam.bezeichnung = "Program Path for PDF"
        htparam.fchar = ""
        htparam.reihenfolge = 13

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1374)]})

    if htparam.paramgruppe != 15:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1374)]})
        htparam.paramgruppe = 15
        htparam.feldtyp = 5
        htparam.bezeichnung = "Program name of PDF"
        htparam.fchar = ""
        htparam.reihenfolge = 14

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1058)]})

    if htparam.paramgruppe != 27:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1058)]})
        htparam.paramgruppe = 27
        htparam.feldtyp = 5
        htparam.bezeichnung = "ThisYR Nat KeyAcct gastNo eg 10,35,."
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1025)]})
        htparam.paramgruppe = 27
        htparam.feldtyp = 5
        htparam.bezeichnung = "LastYR Nat KeyAcct gastNo eg 10,35,."
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 278)]})
        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.bezeichnung = "SOB Code for Web Production Report"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 378)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 378)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "MiniBar ArtNo needed for PABX IF"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1379)]})

    if htparam.paramgruppe != 15:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1379)]})
        htparam.paramgruppe = 15
        htparam.reihenfolge = 133
        htparam.feldtyp = 5
        htparam.bezeichnung = "Param for GreetMail (server;port;usrnm;pwd)"
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1396)]})
        htparam.paramgruppe = 15
        htparam.reihenfolge = 134
        htparam.feldtyp = 5
        htparam.bezeichnung = "LetterNo for C/I emails (NAT,No;.;DEF,No)"
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1397)]})
        htparam.paramgruppe = 15
        htparam.reihenfolge = 135
        htparam.feldtyp = 5
        htparam.bezeichnung = "LetterNo for C/O emails (NAT,No;.;DEF,No)"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 322)]})

    if htparam.paramgruppe != 6:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 322)]})
        htparam.paramgruppe = 6
        htparam.reihenfolge = 68
        htparam.feldtyp = 1
        htparam.bezeichnung = "Delaytion of sending e-mails in minutes (249)"
        htparam.finteger = 60

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1070)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1070)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate Voice Mail Box?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 249)]})

    if htparam.paramgruppe != 6:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 249)]})
        htparam.paramgruppe = 6
        htparam.reihenfolge = 67
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is GCF's Email Address Mandatory upon C/I?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 250)]})

    if htparam.paramgruppe != 6:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 250)]})
        htparam.paramgruppe = 6
        htparam.reihenfolge = 85
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is GCF's Guest Phone Mandatory upon C/I?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 737)]})

    if htparam.paramgruppe != 6:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 737)]})
        htparam.paramgruppe = 6
        htparam.reihenfolge = 40
        htparam.feldtyp = 5
        htparam.bezeichnung = "R-Codes for Report by Ratecode [C1;C2;]"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 836)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 836)]})
        htparam.paramgruppe = 21
        htparam.reihenfolge = 73
        htparam.feldtyp = 4
        htparam.bezeichnung = "PR: hierarchical approval? (Def NO)"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 439)]})

    if htparam.paramgruppe != 27:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 439)]})
        htparam.paramgruppe = 27
        htparam.feldtyp = 1
        htparam.bezeichnung = "DynaRate Occ: 0=RmType 1=Global 2=Optimized"
        htparam.finteger = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1203)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1203)]})
        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.bezeichnung = "Alert if Disc Article's VAT&Srv doesnt match?"
        htparam.flogical = True
        htparam.reihenfolge = 428

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1019)]})

    if htparam.paramgruppe != 8:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1019)]})
        htparam.paramgruppe = 8
        htparam.feldtyp = 5
        htparam.bezeichnung = "Number of Day-Use (rooms)"
        htparam.fchar = "DAY-USE"
        htparam.reihenfolge = 184

    htparam = get_cache(Htparam, {"paramnr": [(eq, 341)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 341)]})
        htparam.feldtyp = 5
        htparam.bezeichnung = "IF-Program for WiFi-Internet"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 342)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 342)]})
        htparam.feldtyp = 5
        htparam.bezeichnung = "Program to display Room Rate"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 946)]})

    if htparam.paramgruppe != 6:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 963)]})

        if htparam and htparam.paramgruppe == 6 and htparam.reihenfolge == 57:
            htparam.reihenfolge = 999

        htparam = get_cache(Htparam, {"paramnr": [(eq, 946)]})
        htparam.paramgruppe = 6
        htparam.bezeichnung = "Ask deposit transfer when C/I the guest?"
        htparam.reihenfolge = 57
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 947)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 947)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Deduct Stocks of POS compliment bills in NA?"
        htparam.reihenfolge = 72
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 911)]})

    if htparam.paramgruppe == 13:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 911)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Enable Button Option in Stock Article Setup?"
        htparam.reihenfolge = 71
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 429)]})

    if htparam.paramgruppe != 6:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 429)]})
        htparam.paramgruppe = 6
        htparam.bezeichnung = "Check user's Printing Access Right?"
        htparam.reihenfolge = 66
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 281)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 281)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Print Food/Bev DISC separately on bill?"
        htparam.reihenfolge = 84
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2405)]})

    if htparam.paramgruppe != 15:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2405)]})
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending BEO(server;port;usernm;pw)"
        htparam.reihenfolge = 129
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2406)]})
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending CRM(server;port;usernm;pw)"
        htparam.reihenfolge = 130
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2407)]})
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending SMS/email report(server;port;usernm;pw)"
        htparam.reihenfolge = 131
        htparam.feldtyp = 5
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2408)]})
        htparam.paramgruppe = 15
        htparam.bezeichnung = "Param sending Questionnaire(server;port;usernm;pw)"
        htparam.reihenfolge = 132
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 962)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 962)]})
        htparam.bezeichnung = "Post 0 Room Rate in NA program? (DEF = NO)"
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 695)]})
    htparam.paramgruppe = 17
    htparam.bezeichnung = "Type of Document"
    htparam.feldtyp = 5
    htparam.fchar = "DOCU-TYPE"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 397)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 397)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETA Flight Number"
        htparam.reihenfolge = 171
        htparam.feldtyp = 5
        htparam.fchar = "ETAFL"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 713)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETA Time"
        htparam.reihenfolge = 172
        htparam.feldtyp = 5
        htparam.fchar = "ETATIME"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 714)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETD Flight Number"
        htparam.reihenfolge = 173
        htparam.feldtyp = 5
        htparam.fchar = "ETDFL"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 715)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "ETD Time"
        htparam.reihenfolge = 174
        htparam.feldtyp = 5
        htparam.fchar = "ETDTIME"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 725)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Birth Place"
        htparam.reihenfolge = 175
        htparam.feldtyp = 5
        htparam.fchar = "BIRTHPLACE"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 726)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "port / ID Expired Date"
        htparam.reihenfolge = 176
        htparam.feldtyp = 5
        htparam.fchar = "ID-EXPIRED"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 730)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Purpose of Stay"
        htparam.reihenfolge = 177
        htparam.feldtyp = 5
        htparam.fchar = "PURPOSE"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 731)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Mobile Number"
        htparam.reihenfolge = 178
        htparam.feldtyp = 5
        htparam.fchar = "MOBILE"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 733)]})

    if htparam.paramgruppe != 17 or htparam.fchar.lower() == "company":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 733)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Company Name of the hotel guest"
        htparam.reihenfolge = 179
        htparam.feldtyp = 5
        htparam.fchar = "GCOMPANY"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 759)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 759)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Address 1"
        htparam.reihenfolge = 180
        htparam.feldtyp = 5
        htparam.fchar = "RSV-adr1"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 760)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Address 2"
        htparam.reihenfolge = 181
        htparam.feldtyp = 5
        htparam.fchar = "RSV-adr2"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 761)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Address 3"
        htparam.reihenfolge = 182
        htparam.feldtyp = 5
        htparam.fchar = "RSV-adr3"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 762)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name City"
        htparam.reihenfolge = 183
        htparam.feldtyp = 5
        htparam.fchar = "RSV-city"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 763)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name ZIP code"
        htparam.reihenfolge = 184
        htparam.feldtyp = 5
        htparam.fchar = "RSV-ZIP"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 765)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Reserved Name Country"
        htparam.reihenfolge = 185
        htparam.feldtyp = 5
        htparam.fchar = "RSV-country"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 766)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "CreditCard No, Expiry MM/YYYY"
        htparam.reihenfolge = 186
        htparam.feldtyp = 5
        htparam.fchar = "CCard"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 839)]})

    if htparam.feldtyp != 1:

        htparam.bezeichnung = "Letter Category Number for SMS Report CFG"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1459)]})

    if htparam.paramgruppe != 99:

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR CRM Module"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1073

    htparam = get_cache(Htparam, {"paramnr": [(eq, 347)]})

    if htparam.paramgruppe != 13 or htparam.bezeichnung.lower() == "not used" or htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 347)]})
        htparam.paramgruppe = 13
        htparam.reihenfolge = 11
        htparam.bezeichnung = "PF Path file for VHPArchive DB"
        htparam.fchar = ""
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1202)]})

    if htparam.paramgruppe != 27:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1202)]})
        htparam.paramgruppe = 27
        htparam.reihenfolge = 3
        htparam.bezeichnung = "Restriction on GCF modification applied? (DEF=No)"
        htparam.flogical = False
        htparam.feldtyp = 4

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1018)]})

    if htparam.paramgruppe != 38:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1018)]})
        htparam.paramgruppe = 38
        htparam.reihenfolge = 30
        htparam.bezeichnung = "PI Cheque/Giro Temporary AcctNo"
        htparam.fchar = ""
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 931)]})

    if htparam.paramgruppe != 38:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 931)]})
        htparam.paramgruppe = 38
        htparam.reihenfolge = 29
        htparam.bezeichnung = "Proforma Invoice Temporary AcctNo"
        htparam.fchar = ""
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2999)]})

    if htparam.paramgruppe != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2999)]})
        htparam.paramgruppe = 5
        htparam.reihenfolge = 68
        htparam.bezeichnung = "Article Number for Extra Bed [eg n1;n2;n3;]"
        htparam.fchar = ""
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 893)]})

    if htparam.paramgruppe != 15:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 893)]})
        htparam.bezeichnung = "LetterNo for Advance GUEST Bill"
        htparam.feldtyp = 1
        htparam.paramgruppe = 15
        htparam.reihenfolge = 99

    htparam = get_cache(Htparam, {"paramnr": [(eq, 173)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password for Posting FO VOID Item"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 810)]})

    if matches(htparam.bezeichnung, r"*PAYING*"):

        htparam = get_cache(Htparam, {"paramnr": [(eq, 810)]})
        htparam.bezeichnung = "Number of Guests(Adult + compl + ch1 + ch2)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 961)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 961)]})
        htparam.bezeichnung = "Is Guest Title mandatory in GCF? (Def NO)"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 369)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 369)]})
        htparam.bezeichnung = "nt-KNGfbRev.r param:D1,F1,.,F4,B1.B4;D2,F1.F4"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 567)]})

    if (not matches(htparam.bezeichnung, r"*ACCOR*")) or htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 567)]})
        htparam.bezeichnung = "Enable ACCOR Reports? (CNTL-P)"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 960)]})

    if htparam.paramgruppe != 27:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 960)]})
        htparam.paramgruppe = 27
        htparam.reihenfolge = 15
        htparam.bezeichnung = "Cutoff days for Not sending back questionnair"
        htparam.finteger = 30
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 794)]})

    if htparam.paramgruppe != 27 or htparam.feldtyp == 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 794)]})
        htparam.paramgruppe = 27
        htparam.reihenfolge = 13
        htparam.bezeichnung = 'Quesionnaire "EventNo;DeptNo;" for c/o guests'
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2073)]})

    if not matches(htparam.bezeichnung, r"*P$L*"):

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2073)]})
        htparam.bezeichnung = "Keyword for P&L Report in Foreign Currency"
        htparam.fchar = "IN-FOREIGN"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1072)]})
    htparam.bezeichnung = "License for VHP Report Generator"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 711)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 711)]})
        htparam.paramgruppe = 17
        htparam.reihenfolge = 170
        htparam.bezeichnung = "(Turkish) Citizen ID Number"
        htparam.feldtyp = 5
        htparam.fchar = "TCID"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 430)]})

    if htparam.bezeichnung.lower() == "not used" or htparam.fchar == "":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 430)]})
        htparam.bezeichnung = "Directory for Confirmation Attached File"
        htparam.fchar = "c:\\vhp\\"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 478)]})
    htparam.bezeichnung = "Default Rsv Stat: 0GTD 1Tent 2=6PM 3=OralConf"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 948)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 948)]})
        htparam.feldtyp = 4
        htparam.reihenfolge = 83
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Print TOTAL Food/Bev/Other Amount? (Def=NO)"
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 938)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 938)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Use 'ORAL CONFIRM' Reservation Status?"
        htparam.flogical = True
        htparam.fchar = ""

        htparam = get_cache(Htparam, {"paramnr": [(eq, 939)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Use 'FIRST NAME' in individual GCF?"
        htparam.flogical = True
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1200)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1200)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "User GroupNo for Engineering Department"
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1203)]})
        htparam.bezeichnung = "Not used"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1204)]})
        htparam.bezeichnung = "Not used"

        paramtext = get_cache(Paramtext, {"txtnr": [(eq, 152)]})
        paramtext.ptexte = "Engineering Module"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 358)]})

    if htparam.bezeichnung.lower() != ("license for internet billing system"):

        htparam.bezeichnung = "License for Internet Billing System"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 887)]})

    if htparam.feldtyp != 5:

        htparam.bezeichnung = "Acct-No for FA A/P (default = A/P Trade)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 793)]})

    if htparam.paramgruppe != 38:

        htparam.bezeichnung = "Transfer F/O journal for departments e.g. 0,1,2"
        htparam.feldtyp = 5
        htparam.paramgruppe = 38
        htparam.reihenfolge = 28
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 129)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 129)]})
        htparam.bezeichnung = "Number of VACANT rooms"
        htparam.feldtyp = 5
        htparam.reihenfolge = 17
        htparam.paramgruppe = 8
        htparam.fchar = "VACANT"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1110)]})

    if htparam.fchar == "":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1110)]})
        htparam.bezeichnung = "Today's Billing Date"
        htparam.reihenfolge = 161
        htparam.fchar = "BillDate"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 132)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 132)]})
        htparam.feldtyp = 5
        htparam.bezeichnung = htparam.bezeichnung + " [e.g. n1;n2;n3;]"
        htparam.fchar = trim(to_string(htparam.finteger, ">>>>9")) + ";"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 933)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 933)]})
        htparam.bezeichnung = "Stay-Pay Nite Use AvrgRate Option? (Def NO)"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 736)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 736)]})
        htparam.bezeichnung = "ProgName for Calculating ResNo (HV)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 431)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 431)]})
        htparam.bezeichnung = "Default Confirmation Letter Number"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 571)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 571)]})
        htparam.bezeichnung = "Floor Plan BOX Height x Width [eg 70 x 500]"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 968)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 968)]})
        htparam.bezeichnung = "Search Guest Name Start Field: 0=Name 1=ID"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 123)]})

    if htparam.paramgruppe != 7:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 123)]})
        htparam.bezeichnung = "Dummy INDIVIDUAL Company GuestNo"
        htparam.paramgruppe = 7
        htparam.reihenfolge = 32
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 455)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 455)]})
        htparam.bezeichnung = "ProgName for Money Exchange Receipt"

        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1009)]})

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1009)]})
    htparam.bezeichnung = "Rest. Discount ArtNo for 2nd VAT"

    if htparam.feldtyp != 1:
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 271)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 271)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Apply Multi VAT in the POS?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 764)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 764)]})
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.reihenfolge = 78
        htparam.bezeichnung = "Summary of VAT% - VAT - Net - Amount"
        htparam.fchar = "VAT-SUM"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 237)]})

    if htparam.paramgruppe != 9:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 237)]})
        htparam.paramgruppe = 9
        htparam.feldtyp = 1
        htparam.bezeichnung = "Storage Duration for closed P/O"
        htparam.finteger = 60

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe != 38:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1012)]})
        htparam.paramgruppe = 38
        htparam.reihenfolge = 27
        htparam.feldtyp = 1
        htparam.bezeichnung = "G/L Transaction: MaxChar allowed for RefNo"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 325)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 325)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Create Calls Record when PABX rate = 0?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 172)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password for Posting Misc POS Item"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1398)]})

    if htparam.paramgruppe != 39:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1398)]})
        htparam.paramgruppe = 39
        htparam.bezeichnung = "Deactive YTD amount when calc JAN.DEC balance"
        htparam.feldtyp = 5
        htparam.fchar = "YTDaus"
        htparam.reihenfolge = 78

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2200)]})

    if not htparam:
        htparam = Htparam()
        db_session.add(htparam)

        htparam.paramnr = 2200
        htparam.paramgruppe = 39
        htparam.bezeichnung = "To-date's Exchange Rate"
        htparam.feldtyp = 5
        htparam.fchar = "EXRATE"
        htparam.reihenfolge = 77

    htparam = get_cache(Htparam, {"paramnr": [(eq, 88)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 88)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Print official Rest Bill (Turkey)?"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 13

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1080)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1080)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Store Stocks Onhand when closing inventory?"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 70

    htparam = get_cache(Htparam, {"paramnr": [(eq, 109)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 109)]})
        htparam.bezeichnung = "Dummy Walk-in Company GuestNo"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 116)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 116)]})
        htparam.bezeichnung = "F/O SubgrpNo for unallocated C/L article"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 738)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 738)]})
        htparam.bezeichnung = "F/O Article for rounding of Bill Amount"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 262)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 262)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "No of Adult(s) for new reservation (def = 1)"
        htparam.finteger = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 437)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 437)]})
        htparam.bezeichnung = "Allow cancel Reservation after generating keycard?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 949)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 949)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Department No for MiniBar"
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 82
        htparam.paramgruppe = 19

    htparam = get_cache(Htparam, {"paramnr": [(eq, 716)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 716)]})
        htparam.feldtyp = 5
        htparam.bezeichnung = "Parameters for Daily Sales Report I"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 732)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 732)]})
        htparam.feldtyp = 5
        htparam.bezeichnung = "Parameters for Daily Sales Report II"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 297)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 297)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Change 6PM to other time, eg. 4=4PM (Param373)"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1047)]})

    if htparam.feldtyp == 4 and htparam.bezeichnung.lower() == "not used":

        htparam.bezeichnung = "F/O ArtNo for Club Initial Fee"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1048)]})
        htparam.bezeichnung = "F/O ArtNo for Club Discount"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1049)]})
        htparam.bezeichnung = "Create renewal .. days before expired"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1050)]})
        htparam.bezeichnung = "Display warning for segment VIP?"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1056)]})
        htparam.bezeichnung = "Display warning for segment Black List?"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1057)]})
        htparam.bezeichnung = "Save Check-In history (Days)"
        htparam.feldtyp = 1
        htparam.finteger = 365

    htparam = get_cache(Htparam, {"paramnr": [(eq, 118)]})

    if htparam.reihenfolge != 22:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 118)]})
        htparam.reihenfolge = 22
        htparam.bezeichnung = "Article Number for Internet Charges"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1004)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1004)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "P/O Order Name"
        htparam.feldtyp = 5
        reihenfolge = 168
        htparam.fchar = "odname"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1005)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "P/O Order Item's Remark"
        htparam.feldtyp = 5
        reihenfolge = 169
        htparam.fchar = "bl-remark"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1064)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1064)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Subgroups for HK Onhand List (format n1;n2;)"
        htparam.feldtyp = 5
        reihenfolge = 43
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 496)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 496)]})
        htparam.bezeichnung = "Argt Code for All Inclusive (argt1;argt2;.)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 252)]})

    if htparam.paramgruppe != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 252)]})
        htparam.bezeichnung = "KitchPrinter:#-Lines before cutting (def 4)"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.paramgruppe = 1
        htparam.reihenfolge = 100

        htparam = get_cache(Htparam, {"paramnr": [(eq, 562)]})
        htparam.bezeichnung = "KitchPrinter:#-Lines after cutting (def 5)"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.paramgruppe = 1
        htparam.reihenfolge = 101

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1080)]})

    if not htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1080)]})
        htparam.bezeichnung = "Storage Number for House Keeping Items"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.paramgruppe = 21
        htparam.reihenfolge = 36

    htparam = get_cache(Htparam, {"paramnr": [(eq, 495)]})

    if not matches(htparam.bezeichnung, r"*Single Line*"):

        htparam = get_cache(Htparam, {"paramnr": [(eq, 495)]})
        htparam.bezeichnung = "LetterNo MasterBill Single Line - Foreign Currency"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 208)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 208)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Allow opened Master Bill when all guests C/O?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2076)]})
    htparam.bezeichnung = "YTD option for Monthly Balance (PnL Acct)"
    htparam.fchar = "YTDein"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1099)]})

    if htparam.paramgruppe != 27:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1099)]})
        htparam.paramgruppe = 27
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Send email to guest when guest checks out?"
        htparam.reihenfolge = 12

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1071)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password for Parameter Group 10 (Password)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 239)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 47)]})
        htparam.reihenfolge = 16

        htparam = get_cache(Htparam, {"paramnr": [(eq, 239)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Above xx rooms (param 97, default = 20)"
        htparam.reihenfolge = 15
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 418)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "Output Directory for F/O & G/L Excel Report"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 170)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password of Excel .xls files - F/O Reports"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 171)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "Password of Excel .xls files - G/L Reports"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 932)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 932)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Generate F/O BillNo when guest C/I (def=NO)?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1060)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1060)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "User GroupNo for Engineering Department"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1061)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Storage Number for Engineering Department"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1062)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Engineering's Cost Department Number"
        htparam.feldtyp = 1
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2401)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2401)]})
        htparam.paramgruppe = 17
        htparam.reihenfolge = 157
        htparam.bezeichnung = "Current User Name"
        htparam.feldtyp = 5
        htparam.fchar = "UserName"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 550)]})
        htparam.bezeichnung = "Use Advance Contract Rate Setup (PRO Version)?"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 549)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 549)]})
        htparam.bezeichnung = "Rate Disc: 0=Average 1=As-Is 2=Min 3=Max"
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.reihenfolge = 11

    htparam = get_cache(Htparam, {"paramnr": [(eq, 739)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 739)]})
        htparam.reihenfolge = 427
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Ask Bill counter number when closing the bill?"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 179)]})

    if htparam.paramgruppe != 8:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 179)]})
        htparam.paramgruppe = 8
        htparam.reihenfolge = 183
        htparam.bezeichnung = "Room Number of selected Room Type"
        htparam.feldtyp = 5
        htparam.fchar = "RM-RMCAT"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 85)]})

    if htparam.paramgruppe != 8:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 85)]})
        htparam.paramgruppe = 8
        htparam.reihenfolge = 179
        htparam.bezeichnung = "Arrivals thru Reservation (Rooms)"
        htparam.feldtyp = 5
        htparam.fchar = "RM-RSV"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 86)]})
        htparam.paramgruppe = 8
        htparam.reihenfolge = 180
        htparam.bezeichnung = "Arrivals thru Reservation (Adults)"
        htparam.feldtyp = 5
        htparam.fchar = "PRS-RSV"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 106)]})
        htparam.paramgruppe = 8
        htparam.reihenfolge = 181
        htparam.bezeichnung = "Arrivals thru Walk-in Guest (Rooms)"
        htparam.feldtyp = 5
        htparam.fchar = "RM-WIG"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 107)]})
        htparam.paramgruppe = 8
        htparam.reihenfolge = 182
        htparam.bezeichnung = "Arrivals thru Walk-in Guest (Adults)"
        htparam.feldtyp = 5
        htparam.fchar = "PRS-WIG"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 833)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 833)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "Cash Payment: USE Multi-Currency Mode?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 830)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 830)]})
        htparam.feldtyp = 5
        htparam.bezeichnung = "MultiCurr Total Amount in bill (eg. USD;EURO)"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 874)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 874)]})
        htparam.feldtyp = 4
        htparam.bezeichnung = "POS Bill: Always print all items? (roll printer)"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1040)]})

    if htparam.feldtyp != 1:

        paramtext = get_cache(Paramtext, {"txtnr": [(eq, 149)]})
        paramtext.ptexte = "CLUB Module"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1040)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Max number of member freezing allowed"
        htparam.finteger = 1

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1041)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Max age valid for Child/Junior Member"
        htparam.finteger = 16

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1042)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Club Opening Hour (1 - 24)"
        htparam.finteger = 6

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1044)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Club Closing Hour (1 - 24)"
        htparam.finteger = 22

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1045)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "Department number of the CLUB"
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1046)]})
        htparam.feldtyp = 1
        htparam.bezeichnung = "F/O ArtNo for Club Membership Fee"
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 928)]})

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "Read Card: get direct result? (VHPIF -> YES)"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1114)]})

    if htparam.bezeichnung.lower() != ("license for club software"):
        htparam.feldtyp = 4
        htparam.bezeichnung = "License for CLUB Software"
        htparam.flogical = False
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 223)]})

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "License for Membership Card"
        htparam.flogical = False
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 872)]})

    if htparam.feldtyp != 5:
        htparam.feldtyp = 5
        htparam.bezeichnung = "Description for VAT on the POS Bill"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 395)]})

    if htparam.paramgruppe != 38:
        htparam.paramgruppe = 38
        htparam.feldtyp = 5
        htparam.bezeichnung = "G/L AcctNo for A/P Others (Optional)"
        htparam.reihenfolge = 26
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1079)]})

    if htparam.paramgruppe != 19:
        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.bezeichnung = "Waiter transfer: Ask waiter password? (DEF NO)"
        htparam.reihenfolge = 424
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 799)]})

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "RegNo for C/I guests? (DEF NO, bill.rechnr2)"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1077)]})

    if htparam.feldtyp != 5:
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.reihenfolge = 2318
        htparam.bezeichnung = "Inhouse Guest Registration No (Param 799)"
        htparam.fchar = "RegNo"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1078)]})

    if htparam.feldtyp != 5:
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.reihenfolge = 2319
        htparam.bezeichnung = "RmRate Discount (%) to publish rate"
        htparam.fchar = "RateDisc"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 857)]})
    htparam.bezeichnung = "Print Discount AFTER sales items?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 152)]})
    htparam.bezeichnung = "Local Currency Code (Short Form)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1063)]})

    if htparam.paramgruppe != 17:
        htparam.paramgruppe = 17
        htparam.feldtyp = 5
        htparam.bezeichnung = "Print Bill: Skip to Line (e.g. $ROW50)"
        htparam.reihenfolge = 2317
        htparam.fchar = "ROW"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 936)]})

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "Is Deposit mandatory in the reservation?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 937)]})

    if htparam.feldtyp != 4:
        htparam.feldtyp = 4
        htparam.bezeichnung = "Read Birthdate from the Guest ID?"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 970)]})

    if htparam.feldtyp != 1:
        htparam.feldtyp = 1
        htparam.bezeichnung = "Max Hours for Day-Use w/o Disc-Rate Control"
        htparam.finteger = 3

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2311)]})
    htparam.bezeichnung = "Current Time"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2312)]})
    htparam.bezeichnung = "Current User ID"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1117)]})
    htparam.bezeichnung = "Bill-line User ID"
    htparam.feldtyp = 5
    htparam.fchar = "bl-usrinit"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 967)]})

    if htparam.paramgruppe != 38:
        htparam.paramgruppe = 38
        htparam.bezeichnung = "Consider Table gl-coa for HOTEL/CONDOTEL P&L?"
        htparam.feldtyp = 4
        htparam.reihenfolge = 25
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 195)]})

    if htparam.paramgruppe != 8:
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Average Stay (in nights) of Paying Guests"
        htparam.feldtyp = 5
        htparam.reihenfolge = 13
        htparam.fchar = "AVRG-STAY"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 318)]})
    htparam.reihenfolge = 99

    htparam = get_cache(Htparam, {"paramnr": [(eq, 192)]})

    if htparam.paramgruppe != 8:
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Total Food Cover of selected department"
        htparam.feldtyp = 5
        htparam.reihenfolge = 15
        htparam.fchar = "F-COVER"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 197)]})

    if htparam.paramgruppe != 8:
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Total Beverage Cover of selected department"
        htparam.feldtyp = 5
        htparam.reihenfolge = 16
        htparam.fchar = "B-COVER"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 83)]})
    htparam.bezeichnung = "Pop up warning when transactions go over limit?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 564)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 564)]})
        htparam.bezeichnung = "Default Room Availability SET to after allotment?"
        htparam.feldtyp = 4
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 480)]})

    if htparam.paramgruppe != 15:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 480)]})
        htparam.paramgruppe = 15
        htparam.bezeichnung = "LetterNo for Advance Bill II (option)"
        htparam.feldtyp = 1
        htparam.reihenfolge = 98

    htparam = get_cache(Htparam, {"paramnr": [(eq, 419)]})
    htparam.bezeichnung = "LetterNo debt list Invoice (Non Stay Guest)"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 424)]})
    htparam.bezeichnung = "LetterNo for debt list's Invoice"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 321)]})
    htparam.bezeichnung = "MaxChar length for Name-Display (def 32)"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 752)]})
    htparam.bezeichnung = "Out-of-Service"
    htparam.feldtyp = 5
    htparam.fchar = "OOS"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 187)]})
    htparam.bezeichnung = "Arrivals (Room)"
    htparam.feldtyp = 5
    htparam.fchar = "RM-ARR"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 188)]})
    htparam.bezeichnung = "Arrivals (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS-ARR"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 189)]})
    htparam.bezeichnung = "Departures (Room)"
    htparam.feldtyp = 5
    htparam.fchar = "RM-DEP"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 190)]})
    htparam.bezeichnung = "Departures (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS-DEP"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 191)]})
    htparam.bezeichnung = "Number of VIP Guests"
    htparam.feldtyp = 5
    htparam.fchar = "VIP"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 193)]})
    htparam.bezeichnung = "Reservation Made Today (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "NEW-RES"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 194)]})
    htparam.bezeichnung = "Cancellation Today (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "CANC-RES"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 211)]})
    htparam.bezeichnung = "Arrivals Tommorow (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "RM-ARRTMR"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 231)]})
    htparam.bezeichnung = "Arrival Tomorrows (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS-ARRTMR"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 750)]})
    htparam.bezeichnung = "Departure Tomorrow (Rooms)"
    htparam.feldtyp = 5
    htparam.fchar = "RM-DEPTMR"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 751)]})
    htparam.bezeichnung = "Departure Tomorrow (Adults)"
    htparam.feldtyp = 5
    htparam.fchar = "PRS-DEPTMR"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 969)]})
    htparam.bezeichnung = "No-Show Rooms"
    htparam.feldtyp = 5
    htparam.fchar = "NOSHOW"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 742)]})

    if htparam.paramgruppe != 8:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 742)]})
        htparam.paramgruppe = 8
        htparam.reihenfolge = 178
        htparam.bezeichnung = "Early Checkout (Rooms)"
        htparam.feldtyp = 5
        htparam.fchar = "EARLY-CO"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 570)]})
    htparam.bezeichnung = "Minibar Department No (needed by PABX IF)"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 724)]})
    htparam.bezeichnung = "Auto Update Billing Date when signing on?"
    htparam.paramgruppe = 24
    htparam.feldtyp = 4
    htparam.reihenfolge = 10

    htparam = get_cache(Htparam, {"paramnr": [(eq, 904)]})
    htparam.bezeichnung = "Default C/L payment ArtNo"
    htparam.paramgruppe = 24
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 17)]})
    htparam.bezeichnung = "Service Charge Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 18)]})
    htparam.bezeichnung = "Sinking Fund Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 500)]})
    htparam.bezeichnung = "LetterNo Invoicing - ServiceCharge"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 613)]})
    htparam.bezeichnung = "LetterNo Invoicing - Water & Electricity"
    htparam.paramgruppe = 24
    htparam.feldtyp = 1
    htparam.reihenfolge = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 981)]})
    htparam.bezeichnung = "License for Condominium"

    paramtext = get_cache(Paramtext, {"txtnr": [(eq, 147)]})
    paramtext.ptexte = "Condominium Admin"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 796)]})

    if htparam.feldtyp != 5:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 500)]})
        htparam.bezeichnung = "Not used"

        htparam = get_cache(Htparam, {"paramnr": [(eq, 796)]})
        htparam.paramgruppe = 24
        htparam.bezeichnung = "Label for Tenant Card Type"
        htparam.feldtyp = 5

        htparam = get_cache(Htparam, {"paramnr": [(eq, 797)]})
        htparam.paramgruppe = 24
        htparam.bezeichnung = "Label for Company Card Type"
        htparam.feldtyp = 5

        htparam = get_cache(Htparam, {"paramnr": [(eq, 798)]})
        htparam.paramgruppe = 24
        htparam.bezeichnung = "Label for Owner Card Type"
        htparam.feldtyp = 5

        htparam = get_cache(Htparam, {"paramnr": [(eq, 934)]})
        htparam.paramgruppe = 24
        htparam.bezeichnung = "F/O Article No for Service Charge"
        htparam.feldtyp = 1

        htparam = get_cache(Htparam, {"paramnr": [(eq, 935)]})
        htparam.paramgruppe = 24
        htparam.bezeichnung = "F/O Article No for Sinking Fund"
        htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 17)]})
    htparam.bezeichnung = "Service Charge Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 18)]})
    htparam.bezeichnung = "Sinking Fund Unit Fee"
    htparam.paramgruppe = 24
    htparam.feldtyp = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 17)]})

    if htparam.feldtyp != 5:
        htparam.bezeichnung = "ServCharge Unit Fee by AptType(xx;yy;.;)"
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 18)]})

    if htparam.feldtyp != 5:
        htparam.bezeichnung = "Sinking Fund Unit Fee by AptType(xx;yy;.;)"

    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 728)]})
    htparam.bezeichnung = "Name Display: Send Sharer Name to PABX?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 417)]})
    htparam.bezeichnung = "ProgPath of LnL *.lst files (def. \\vhp\\LnL\\)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 242)]})
    htparam.bezeichnung = "Subgroup No for F/O Paid-Out Billing Article"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 320)]})

    if htparam:

        if htparam.bezeichnung.lower() == "not used" or htparam.paramgruppe != 14:

            htparam.paramgruppe = 14
            htparam.bezeichnung = "Block new reservation when A/R Over CrLimit?"
            htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 333)]})
    htparam.bezeichnung = "PDA MC Reader Start Char Position (Param 336)"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 334)]})
    htparam.bezeichnung = "PDA MC Reader End Char Position (Param 336)"
    htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 376)]})
    htparam.bezeichnung = "Print Net&VAT amt for CASH & CC payment?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 829)]})
    htparam.bezeichnung = "Word Program Name for Param 825"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 825)]})
    htparam.bezeichnung = "Print Total POS bill amount in Word?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 824)]})
    htparam.bezeichnung = "Exclude Tax&Service for Compliment Payment?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 314)]})
    htparam.bezeichnung = "PAUSE in SEC for ifstart.r (min=2 max=10)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 323)]})
    htparam.bezeichnung = "Check duplicate calls record in ifstart.r?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 312)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 312)]})
        htparam.bezeichnung = "Debugging Mode for ifstart.r (0 = No Debug)"
        htparam.feldtyp = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 186)]})

    if htparam.feldtyp != 3:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 186)]})
        htparam.bezeichnung = "Hotel Opening (= statistic starting) Date"
        htparam.fdate = None
        htparam.feldtyp = 3

    htparam = get_cache(Htparam, {"paramnr": [(eq, 236)]})
    htparam.bezeichnung = "N/A allowed with opened restaurant bill(s)?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1076)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1076)]})
        htparam.bezeichnung = "Control C/O time when Checking out the guest?"
        htparam.flogical = False

        htparam.feldtyp = 4

    htparam = get_cache(Htparam, {"paramnr": [(eq, 373)]})
    htparam.bezeichnung = "Change 6PM-Rsv Status to No-Show after 6PM?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1589)]})
    htparam.paramgruppe = 17
    htparam.reihenfolge = 156
    htparam.bezeichnung = "Bill-line Voucher"
    htparam.fchar = "bl-voucher"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 244)]})

    if htparam.feldtyp != 5:
        htparam.bezeichnung = "External Main Program Filename (CNTRL-P)"
        htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1103)]})
    htparam.bezeichnung = "Bill-Line arrival date"
    htparam.paramgruppe = 17
    htparam.reihenfolge = 2315
    htparam.fchar = "bl-arrive"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1104)]})
    htparam.bezeichnung = "Bill-line departure date"
    htparam.paramgruppe = 17
    htparam.reihenfolge = 2316
    htparam.fchar = "bl-depart"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1083)]})

    if htparam.bezeichnung.lower() != ("store duration for fb compliment"):
        htparam.bezeichnung = "Store Duration for FB Compliment"
        htparam.finteger = 180

    htparam = get_cache(Htparam, {"paramnr": [(eq, 814)]})
    htparam.bezeichnung = "No of Persons for selected Segment"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 753)]})
    htparam.bezeichnung = "Number of ADULT guest"
    htparam.fchar = "NUMADULT"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 754)]})
    htparam.bezeichnung = "Number of CHILD1 guest"
    htparam.fchar = "NUMCHLD1"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 755)]})
    htparam.bezeichnung = "Number of CHILD2 guest"
    htparam.fchar = "NUMCHLD2"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 756)]})
    htparam.bezeichnung = "No of Adults for selected Segment"
    htparam.fchar = "SEGADULT"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 757)]})
    htparam.bezeichnung = "No of Child1 for selected Segment"
    htparam.fchar = "SEGMCH1"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 758)]})
    htparam.bezeichnung = "No of Child2 for selected Segment"
    htparam.fchar = "SEGMCH2"
    htparam.feldtyp = 5

    htparam = get_cache(Htparam, {"paramnr": [(eq, 230)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 230)]})
        htparam.bezeichnung = "Should the system store N/A daily outputs?"
        htparam.feldtyp = 4
        htparam.flogical = False

        htparam = get_cache(Htparam, {"paramnr": [(eq, 238)]})
        htparam.bezeichnung = "If 230=YES, Enter store duration (Days)"
        htparam.feldtyp = 1
        htparam.finteger = 180

    htparam = get_cache(Htparam, {"paramnr": [(eq, 497)]})
    htparam.bezeichnung = "LetterNo for Single Line NS Bill (option)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 413)]})

    if htparam.paramgruppe != 17:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 414)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Number of Night Stay"
        htparam.feldtyp = 5
        htparam.fchar = "Nites"
        htparam.reihenfolge = 49

        htparam = get_cache(Htparam, {"paramnr": [(eq, 413)]})
        htparam.paramgruppe = 17
        htparam.bezeichnung = "Mobile Number"
        htparam.feldtyp = 5
        htparam.fchar = "HP-No"
        htparam.reihenfolge = 85

    htparam = get_cache(Htparam, {"paramnr": [(eq, 465)]})
    htparam.bezeichnung = "Ask Invoice Counter# when printing the bill?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 432)]})

    if htparam.feldtyp != 1:
        htparam.feldtyp = 1
        htparam.bezeichnung = "LetterNo for Printing Hotel Guest port"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 219)]})
    htparam.bezeichnung = "Closed Bill: Enable to change billing date?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1086)]})

    if htparam.bezeichnung.lower() == "not used":
        htparam.bezeichnung = "Max F/O Unit Price in local currency"
        htparam.feldtyp = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 688)]})
    htparam.bezeichnung = "LetterNo for Master Bill Single Line (Option)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 556)]})
    htparam.bezeichnung = "Rest. ArtNo for other type of Discount"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 148)]})

    if htparam.feldtyp != 5:
        htparam.feldtyp = 5
        htparam.bezeichnung = "ExtChar xx for mk-gcfxx.p and chg-gcfxx.p"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 141)]})

    if trim(htparam.bezeichnung) == "":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 141)]})
        htparam.bezeichnung = "C/L Payment when no Credit Facility yet"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 185)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 185)]})
        htparam.fchar = ".LYTODAY"
        htparam.bezeichnung = "Last Year TODAY Value"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 415)]})

    if htparam.feldtyp != 1:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 415)]})
        htparam.reihenfolge = 125
        htparam.bezeichnung = "2nd LetterNo for Master Bill"
        htparam.feldtyp = 1
        htparam.finteger = 0

        htparam = get_cache(Htparam, {"paramnr": [(eq, 416)]})
        htparam.reihenfolge = 21
        htparam.bezeichnung = "Word Prog for foreign amt balance (Param 415)"
        htparam.feldtyp = 5
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 68)]})

    if htparam.feldtyp != 2:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 68)]})
        htparam.fdecimal = to_decimal(htparam.finteger)
        htparam.feldtyp = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1001)]})
    htparam.bezeichnung = "Rest Article for the VOUCHER"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1201)]})

    if htparam.paramgruppe != 38:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1201)]})
        htparam.paramgruppe = 38
        htparam.bezeichnung = "G/L AcctNo for WIP (Stock Transform)"
        htparam.feldtyp = 5
        htparam.reihenfolge = 24
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 43)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 43)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Receiving and Outgoing: SHOW UNIT PRICE?"
        htparam.feldtyp = 4
        htparam.reihenfolge = 7
        htparam.finteger = 0

    htparam = get_cache(Htparam, {"paramnr": [(eq, 138)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 138)]})
        htparam.bezeichnung = "ArtNo with Cash Receipt Printout [A1;A2;..]"

        if htparam.feldtyp != 5:
            htparam.feldtyp = 5
            htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 127)]})

    if htparam:

        htparam.bezeichnung = "V.A.T. included in Room Rate ?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 128)]})

    if htparam:

        htparam.bezeichnung = "Service included in Room Rate ?"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 479)]})

    if htparam:

        htparam.bezeichnung = "Article's Service charge is VAT chargeable"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 483)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 483)]})
        htparam.paramgruppe = 7
        htparam.feldtyp = 4
        htparam.bezeichnung = "Article's tax is VAT chargeable"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 740)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 740)]})
        htparam.paramgruppe = 7
        htparam.reihenfolge = 419
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) Journal Voucher Approval by System (01;xx;99)"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1378)]})

    if htparam.paramgruppe != 38:

        htparam.paramgruppe = 38
        htparam.bezeichnung = "Statistic Budget Articles(<Keyword>-<Department>-<ArticleNr>;xxxx;)"
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.reihenfolge = 34

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1343)]})

    if htparam.paramgruppe != 38:

        htparam.paramgruppe = 38
        htparam.bezeichnung = "Transfer BI to Head Office IP:Port"
        htparam.feldtyp = 5
        htparam.finteger = 0
        htparam.fchar = ""
        htparam.reihenfolge = 35

    htparam = get_cache(Htparam, {"paramnr": [(eq, 259)]})

    if htparam.feldtyp != 4:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 259)]})
        htparam.paramgruppe = 10
        htparam.feldtyp = 5
        htparam.bezeichnung = "Password For Posting Room Charge"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 676)]})

    if htparam.paramgruppe != 6:

        htparam.paramgruppe = 6
        htparam.reihenfolge = 84
        htparam.feldtyp = 5
        htparam.bezeichnung = "Parameter for Print Deposit, Refund, Void [D=1,2,;..]"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 494)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 494)]})
        htparam.paramgruppe = 7
        htparam.reihenfolge = 98
        htparam.feldtyp = 4
        htparam.bezeichnung = "Automatically changing the room rate in the FixedRate screen"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 493)]})

    if htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 493)]})
        htparam.paramgruppe = 7
        htparam.reihenfolge = 97
        htparam.feldtyp = 4
        htparam.bezeichnung = "Automatically deleting the fixed rate"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 459)]})

    if htparam.paramgruppe != 27:

        htparam.paramgruppe = 27
        htparam.reihenfolge = 26
        htparam.feldtyp = 4
        htparam.bezeichnung = "The room rate is calculated based on room category"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 792)]})

    if htparam.paramgruppe != 38:
        htparam.feldtyp = 5
        htparam.bezeichnung = "Password for Creating Supplier"
        htparam.paramgruppe = 10

    htparam = get_cache(Htparam, {"paramnr": [(eq, 396)]})

    htparam.paramgruppe = 7
    htparam.reihenfolge = 24
    htparam.feldtyp = 1
    htparam.bezeichnung = "Article for CSR Donation (Tauzia Property's)"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 458)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Minimum Stay For Repeater Guest"
        htparam.reihenfolge = 403

    htparam = get_cache(Htparam, {"paramnr": [(eq, 792)]})

    if htparam.paramgruppe != 38:
        htparam.feldtyp = 5
        htparam.bezeichnung = "Password for Creating Supplier"
        htparam.paramgruppe = 10

    htparam = get_cache(Htparam, {"paramnr": [(eq, 235)]})

    if htparam.bezeichnung.lower() == "not used" or htparam.bezeichnung.lower() == "":

        htparam.bezeichnung = "Access Right to release P/O (2 or 3, def = 2)"
        htparam.paramgruppe = 21
        htparam.feldtyp = 1
        htparam.reihenfolge = 8
        htparam.finteger = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 243)]})

    if htparam.bezeichnung.lower() == "not used" or htparam.bezeichnung.lower() == "":

        htparam.bezeichnung = "Access Right to Approve DML (2 or 3, def = 2)"
        htparam.paramgruppe = 21
        htparam.feldtyp = 1
        htparam.reihenfolge = 9
        htparam.finteger = 2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 473)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activate For Villa Setup"
        htparam.reihenfolge = 406

    htparam = get_cache(Htparam, {"paramnr": [(eq, 451)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 5
        htparam.feldtyp = 5
        htparam.bezeichnung = "Restaurant Articles for SC Discount [eg n1;n2;n3]"
        htparam.reihenfolge = 73
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 452)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 5
        htparam.feldtyp = 5
        htparam.bezeichnung = "Rest. for VAT, SC and Other Taxes [eg n1;n2;n3]"
        htparam.reihenfolge = 74
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 461)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 5
        htparam.feldtyp = 5
        htparam.bezeichnung = "Billing Articles for SC Discount [eg n1;n2;n3]"
        htparam.reihenfolge = 72
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 462)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 5
        htparam.feldtyp = 2
        htparam.bezeichnung = "Discount in % for SC Discount"
        htparam.reihenfolge = 75
        htparam.fdecimal = to_decimal("0")

    htparam = get_cache(Htparam, {"paramnr": [(eq, 466)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Keep Guest Profile (if using GDPR = xxx days)"
        htparam.reihenfolge = 396

    htparam = get_cache(Htparam, {"paramnr": [(eq, 346)]})

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 6
        htparam.feldtyp = 4
        htparam.bezeichnung = "Activated GDPR Rules"
        htparam.reihenfolge = 86
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1345)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "No. of ISO nationality code"
        htparam.reihenfolge = 2324

    htparam = get_cache(Htparam, {"paramnr": [(eq, 615)]})

    if htparam.bezeichnung.lower() == "not used" and htparam.reihenfolge == 417:

        htparam.bezeichnung = "Dummy Guest Card for OTA"
        htparam.paramgruppe = 7
        htparam.feldtyp = 5
        htparam.reihenfolge = 417
        htparam.fchar = "1"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1020)]})

    if htparam.paramgruppe != 23 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 23
        htparam.feldtyp = 5
        htparam.bezeichnung = "Ratecode Room For Reservation Banquet"
        htparam.reihenfolge = 29
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1073)]})

    if htparam.paramgruppe != 99:

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR Dashboard Mobile"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1077

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1055)]})

    if htparam.paramgruppe != 99:

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License FOR Mobile CI/CO"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 1078

    htparam = get_cache(Htparam, {"paramnr": [(eq, 344)]})

    if htparam.paramgruppe != 7:

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Article number can not be split item (99;xx;)"
        htparam.feldtyp = 5
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 2325

    htparam = get_cache(Htparam, {"paramnr": [(eq, 486)]})

    if htparam.paramgruppe != 27:

        htparam.paramgruppe = 27
        htparam.bezeichnung = "Calculating ratecode based on occupancy"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 27

    htparam = get_cache(Htparam, {"paramnr": [(eq, 467)]})

    if htparam:

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Date format for web version"
        htparam.feldtyp = 5
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 2326

    htparam = get_cache(Htparam, {"paramnr": [(eq, 390)]})

    if htparam and htparam.paramgruppe != 21:

        htparam.paramgruppe = 21
        htparam.bezeichnung = "Automatically to approve DML"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 74

    htparam = get_cache(Htparam, {"paramnr": [(eq, 370)]})

    if htparam and htparam.paramgruppe != 21:

        htparam.paramgruppe = 21
        htparam.bezeichnung = "Automatically to blocking budget"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 75

    htparam = get_cache(Htparam, {"paramnr": [(eq, 450)]})

    if htparam and htparam.paramgruppe != 19:

        htparam.paramgruppe = 19
        htparam.bezeichnung = "Show Subgroup in Kitchen Printer"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = " "
        htparam.reihenfolge = 429

    htparam = get_cache(Htparam, {"paramnr": [(eq, 747)]})

    if htparam.bezeichnung.lower() == "not used":
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2327
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) can be attached contract rate (01;xx;99)"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 598)]})

    if htparam.bezeichnung.lower() == "not used":
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2328
        htparam.feldtyp = 5
        htparam.bezeichnung = "User(s) can be modify rate code (01;xx;99)"
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 80)]})

    if htparam.bezeichnung.lower() == "not used":
        htparam.paramgruppe = 40
        htparam.reihenfolge = 102
        htparam.feldtyp = 4
        htparam.bezeichnung = "Show Pickup Required to Web Pre-checkin"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 345)]})

    if htparam.bezeichnung.lower() == "not used":
        htparam.paramgruppe = 13
        htparam.reihenfolge = 39
        htparam.feldtyp = 5
        htparam.bezeichnung = "Departement To Billing Charges - IPTV Interface"
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 735)]})

    if htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 7:
        htparam.paramgruppe = 7
        htparam.reihenfolge = 420
        htparam.feldtyp = 4
        htparam.bezeichnung = "Blocking Resevation Without Ratecode"
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 360)]})

    if htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 7:
        htparam.paramgruppe = 7
        htparam.reihenfolge = 2329
        htparam.feldtyp = 5
        htparam.bezeichnung = "Currency conventer (1;2;xxx;)"
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 953)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 953)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Self CI Apps"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1079
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 954)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 954)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Broadcast Notification MCI "
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1080
        htparam.fchar = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1021)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1021)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Adjustment Inventory Greather Than Actual Qty ?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 76

    htparam = get_cache(Htparam, {"paramnr": [(eq, 477)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Activated Marketing Features ?"
        htparam.reihenfolge = 397

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1344)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 4:

        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "V.A.T Code 16"
        htparam.reihenfolge = 22

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1346)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 4:

        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "V.A.T Code 17"
        htparam.reihenfolge = 23

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1347)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 4:

        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "V.A.T Code 18"
        htparam.reihenfolge = 24

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1348)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 4:

        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "V.A.T Code 19"
        htparam.reihenfolge = 25

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1349)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 4:

        htparam.paramgruppe = 4
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "V.A.T Code 20"
        htparam.reihenfolge = 26

    htparam = get_cache(Htparam, {"paramnr": [(eq, 90)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 15:

        htparam.paramgruppe = 15
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Date Split Activation For Fixed Rate"
        htparam.reihenfolge = 137

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1350)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 6:

        htparam.paramgruppe = 6
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Activated guest search is 100 % same"
        htparam.reihenfolge = 87

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1351)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 19:

        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "RoomNo must be entered when pay use room transfer"
        htparam.reihenfolge = 430

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1352)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 3:

        htparam.paramgruppe = 3
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Group for Night Audit Program (web version only)"
        htparam.reihenfolge = 21

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1353)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 5:

        htparam.paramgruppe = 5
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Article Number for Deposit (SelfCheckin)"
        htparam.reihenfolge = 76

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1354)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 21:

        htparam.paramgruppe = 21
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Receiving is not allowed greather than date of created PO"
        htparam.reihenfolge = 77

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1355)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 3:

        htparam.paramgruppe = 3
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.bezeichnung = "Activated system date using server date"
        htparam.reihenfolge = 22

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1357)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1357)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for VHP Self Order"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1081

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1358)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1358)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for VHP PreArrival Checkin"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1082

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1359)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1359)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for VHP Business Intelligence(BI)"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1083

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1356)]})

    if htparam.paramgruppe != 7:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1356)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Description For RefNo Number 2"
        htparam.fchar = " "
        htparam.feldtyp = 5
        htparam.reihenfolge = 2330

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1342)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1342)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Allow Posting at One Table From Several Waiter(s)"
        htparam.flogical = True
        htparam.feldtyp = 4
        htparam.reihenfolge = 431

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1360)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1360)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Is Partial Inventory Closing Allowed?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 78

    htparam = get_cache(Htparam, {"paramnr": [(eq, 50)]})

    if htparam.paramgruppe != 38:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 50)]})
        htparam.paramgruppe = 38
        htparam.bezeichnung = "G/L AcctNo for Journal A/R (ABI)"
        htparam.fchar = " "
        htparam.feldtyp = 5
        htparam.reihenfolge = 36

    htparam = get_cache(Htparam, {"paramnr": [(eq, 147)]})

    if htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 147)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Sort by SubGroup in Kitchen Printer?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 432

    htparam = get_cache(Htparam, {"paramnr": [(eq, 485)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 485)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "SegmentCode OTA to Room Production Report (OTA;xxx)"
        htparam.fchar = " "
        htparam.feldtyp = 5
        htparam.reihenfolge = 2331

    htparam = get_cache(Htparam, {"paramnr": [(eq, 71)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 71)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Actived 4 Approval for PO"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 79

    htparam = get_cache(Htparam, {"paramnr": [(eq, 561)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 561)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Maximum Time Day Use In ABF List (05:00)"
        htparam.fchar = " "
        htparam.flogical = False
        htparam.finteger = 0
        htparam.feldtyp = 5
        htparam.reihenfolge = 2332

    htparam = get_cache(Htparam, {"paramnr": [(eq, 586)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 586)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Minimum Balance For Cashless NS Guest Bill"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 2
        htparam.reihenfolge = 2333

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1361)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 5:

        htparam.paramgruppe = 5
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Article Number for Deposit (Restaurant)"
        htparam.reihenfolge = 77

    htparam = get_cache(Htparam, {"paramnr": [(eq, 978)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 6:

        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.finteger = 0
        htparam.bezeichnung = "MainGroup to be displayed on the VHP Cloud [eg. D1:1,2,xx;]"
        htparam.reihenfolge = 77

    htparam = get_cache(Htparam, {"paramnr": [(eq, 583)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 9:

        htparam.paramgruppe = 9
        htparam.feldtyp = 1
        htparam.finteger = 0
        htparam.bezeichnung = "Store Duration for GuestBook"
        htparam.flogical = False
        htparam.reihenfolge = 269

    htparam = get_cache(Htparam, {"paramnr": [(eq, 588)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 19:

        htparam.paramgruppe = 19
        htparam.feldtyp = 4
        htparam.finteger = 0
        htparam.bezeichnung = "Activate Restaurant Deposit"
        htparam.flogical = False
        htparam.reihenfolge = 433

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1022)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1022)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Cashless Payment"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1084
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 589)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 589)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Activate User Access For Nonstay Guest Bill"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 2334

    htparam = get_cache(Htparam, {"paramnr": [(eq, 594)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 594)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Activate Dialog Queuing Room List"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = True
        htparam.reihenfolge = 2335

    htparam = get_cache(Htparam, {"paramnr": [(eq, 174)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "NS Cashless Minimum Balance Post as Revenue"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 438)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 15:

        htparam.paramgruppe = 15
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.bezeichnung = "List of Standard Letter No vhpCloud [eg. 1;2;x;x]"
        htparam.reihenfolge = 138

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1204)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1204)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Access for Setup Restaurant Articles"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 434

    else:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1204)]})

    if htparam:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1204)]})
        htparam.bezeichnung = "Disable Access for Setup Restaurant Articles"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 838)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 19:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 838)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Sort by SubGroup Priority in Kitchen Printer?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 435

    htparam = get_cache(Htparam, {"paramnr": [(eq, 448)]})

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.bezeichnung = "Regions complying GDPR rules [eg. 1;2;x;x]"
        htparam.reihenfolge = 88
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 449)]})

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.bezeichnung = "Nationality complying GDPR rules [eg. 1;2;x;x]"
        htparam.reihenfolge = 89
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1023)]})

    if htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1023)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Salesboard Interface"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 1085
        htparam.fchar = " "

    htparam = get_cache(Htparam, {"paramnr": [(eq, 585)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 585)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Activate User Access for Release OOO Room"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 2336

    htparam = get_cache(Htparam, {"paramnr": [(eq, 950)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 950)]})
        htparam.paramgruppe = 23
        htparam.bezeichnung = "Room Rental will be charge after NA"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 30

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1362)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1362)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Use Access For Booking Engine Setup"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.reihenfolge = 2337

    htparam = get_cache(Htparam, {"paramnr": [(eq, 175)]})
    htparam.feldtyp = 5
    htparam.bezeichnung = "word Posting POS VOID Sales Item CloseBill"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 89)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 89)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Set DML Article For Main Group Material"
        htparam.fdecimal = to_decimal("0")
        htparam.feldtyp = 4
        htparam.flogical = True
        htparam.reihenfolge = 80

    htparam = get_cache(Htparam, {"paramnr": [(eq, 91)]})

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 6
        htparam.feldtyp = 5
        htparam.bezeichnung = "Local Time Zone"
        htparam.fchar = ""
        htparam.reihenfolge = 90
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 282)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 282)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface Channel Manager"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1088

    htparam = get_cache(Htparam, {"paramnr": [(eq, 292)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 292)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface Revenue Management"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1089

    htparam = get_cache(Htparam, {"paramnr": [(eq, 294)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 294)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface IPTV"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1091

    htparam = get_cache(Htparam, {"paramnr": [(eq, 296)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 296)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface Online Tax"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1092

    htparam = get_cache(Htparam, {"paramnr": [(eq, 298)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 298)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface Guest Concierge"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1093

    htparam = get_cache(Htparam, {"paramnr": [(eq, 379)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 379)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface Running Text / Totem"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1094

    htparam = get_cache(Htparam, {"paramnr": [(eq, 389)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 389)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Interface WiFi"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1095

    htparam = get_cache(Htparam, {"paramnr": [(eq, 420)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 420)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Corporate Financial"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1096

    htparam = get_cache(Htparam, {"paramnr": [(eq, 421)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 421)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for CRM System"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1097

    htparam = get_cache(Htparam, {"paramnr": [(eq, 422)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 422)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Greeting Email"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1098

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1027)]})

    if htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1027)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Active GST for Restaurant"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 81

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1028)]})

    if htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1028)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "SST Percentage"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 78

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1029)]})

    if htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1029)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number for Tourism Tax"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 79

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1030)]})

    if htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1030)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number for Heritage Fee"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 80

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1377)]})

    if htparam.paramgruppe != 8 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1377)]})
        htparam.paramgruppe = 8
        htparam.bezeichnung = "Daily Report Export to Google Sheet / Excel"
        htparam.flogical = True
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 185

    htparam = get_cache(Htparam, {"paramnr": [(eq, 436)]})

    if htparam.paramgruppe != 19 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 436)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Lock Quantity When Split Item POS?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 436

    htparam = get_cache(Htparam, {"paramnr": [(eq, 98)]})

    if htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.feldtyp = 5
        htparam.bezeichnung = "Access For Modify Journal Transaction [01;xx;99]"
        htparam.fchar = ""
        htparam.reihenfolge = 2338
        htparam.flogical = False

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1033)]})

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1033)]})
        htparam.paramgruppe = 6
        htparam.bezeichnung = "Activate Confirmation For Term and Condition"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 91

    htparam = get_cache(Htparam, {"paramnr": [(eq, 280)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 280)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "Activate Kitchen Display System"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 1099

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1363)]})

    if htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1363)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Service Apartement"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 421

    elif htparam.paramgruppe != 99:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1363)]})
        htparam.paramgruppe = 99
        htparam.bezeichnung = "License for Service Apartement"

    htparam = get_cache(Htparam, {"paramnr": [(eq, 108)]})

    if htparam.paramgruppe != 9 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 108)]})
        htparam.paramgruppe = 9
        htparam.bezeichnung = "Store Duration For Quotation Attachment"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.finteger = 1095
        htparam.reihenfolge = 270

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1364)]})

    if htparam.paramgruppe != 6 and htparam.bezeichnung.lower() == "not used":
        adjust_htparam(93)

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1364)]})
        htparam.paramgruppe = 6
        htparam.bezeichnung = "Parameter for Calculated DynamicRate Based On Villa/Hotel"
        htparam.flogical = False
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.finteger = 1095
        htparam.reihenfolge = 93

    if htparam.paramgruppe == 6 and htparam.bezeichnung.lower() != "not used" and htparam.reihenfolge != 93:
        adjust_htparam(93)

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1068)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 6:
        adjust_htparam(92)

        htparam.paramgruppe = 6
        htparam.bezeichnung = "Article Number for Guest Deposit"
        htparam.finteger = 0
        htparam.feldtyp = 1
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 92

    if htparam.paramgruppe == 6 and htparam.bezeichnung.lower() != "not used" and htparam.reihenfolge != 92:
        adjust_htparam(92)

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1366)]})

    if htparam.paramgruppe != 20 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1366)]})
        htparam.paramgruppe = 20
        htparam.bezeichnung = "Depreciation by Month"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 8

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1367)]})

    if htparam.paramgruppe != 20 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1367)]})
        htparam.paramgruppe = 20
        htparam.bezeichnung = " Fixed Asset Breakdown Access"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 9

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1368)]})

    if htparam.paramgruppe != 20 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1368)]})
        htparam.paramgruppe = 20
        htparam.bezeichnung = "Main Group Account for Fixed Asset"
        htparam.flogical = False
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 10

    htparam = get_cache(Htparam, {"paramnr": [(eq, 178)]})

    if htparam and htparam.bezeichnung.lower() == "not used" and htparam.paramgruppe != 10:

        htparam.paramgruppe = 10
        htparam.bezeichnung = "Password For Payment Compliment POS"
        htparam.finteger = 0
        htparam.feldtyp = 5
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 106

    htparam = get_cache(Htparam, {"paramnr": [(eq, 428)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 428)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Input Reason When Change Status Room (HK)"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 108

    htparam = get_cache(Htparam, {"paramnr": [(eq, 392)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 392)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Enable Automation Create Journal Manual AP"
        htparam.flogical = True
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 2339

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For A/R Ledger Leasing"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 82

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1052)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1052)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For Divered Revenue"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 83

    htparam = get_cache(Htparam, {"paramnr": [(eq, 487)]})

    if htparam and htparam.paramgruppe != 21 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 487)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Receiving DML with lower/higher price allowed?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 81

    htparam = get_cache(Htparam, {"paramnr": [(eq, 488)]})

    if htparam and htparam.paramgruppe != 21 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 21
        htparam.bezeichnung = "Max tolerance in % (Param No 487)"
        htparam.finteger = 0
        htparam.feldtyp = 1
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 82

    htparam = get_cache(Htparam, {"paramnr": [(eq, 293)]})

    if htparam and htparam.paramgruppe != 20 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 20
        htparam.bezeichnung = "Activate counter number 6 digit asset number"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 11

    htparam = get_cache(Htparam, {"paramnr": [(eq, 423)]})

    if htparam and htparam.paramgruppe != 19 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 423)]})
        htparam.paramgruppe = 19
        htparam.bezeichnung = "Parameters For Print Bill POS(Param 874=NO)"
        htparam.flogical = False
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.reihenfolge = 437

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1054)]})

    if htparam and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1054)]})
        htparam.paramgruppe = 25
        htparam.bezeichnung = "Default C/I Time (HH:MM)"
        htparam.flogical = False
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.reihenfolge = 56

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1053)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1053)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For Security Deposit"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 84

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1043)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1043)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For Lost and Breakage"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 85

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1039)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1039)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "MainGroup No For Article Arrangement (Leasing Feature)"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 86

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1026)]})

    if htparam and htparam.paramgruppe != 14 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 14
        htparam.bezeichnung = "Allow Payment CL When Over CreditLimit"
        htparam.feldtyp = 4
        htparam.flogical = True
        htparam.fchar = ""
        htparam.reihenfolge = 100

    htparam = get_cache(Htparam, {"paramnr": [(eq, 425)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "TOTP Reminder"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.reihenfolge = 2340

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1365)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1365)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For Additional Room Charge"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 87

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1369)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1369)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For Refund Divered Revenue"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 88

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1370)]})

    if htparam and htparam.paramgruppe != 5 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1370)]})
        htparam.paramgruppe = 5
        htparam.bezeichnung = "Article Number For Room Charge Adjustment"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.reihenfolge = 89

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1371)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam = get_cache(Htparam, {"paramnr": [(eq, 1371)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Enforce mandatory TOTP configuration on first login?"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 2341

    htparam = get_cache(Htparam, {"paramnr": [(eq, 101)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Screen Lock Timeout When Idle (in seconds)"
        htparam.feldtyp = 1
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 2342

    htparam = get_cache(Htparam, {"paramnr": [(eq, 955)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "TOTP Session Timeout Duration (Days)"
        htparam.feldtyp = 1
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 7
        htparam.reihenfolge = 2343

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1372)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Enable Print for QRIS Digital Payment"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 2344

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1375)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Enable Direct Print After Payment"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 2345

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1376)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Minimum Due Days for Payment Link Digital Payment"
        htparam.feldtyp = 1
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 2346

    htparam = get_cache(Htparam, {"paramnr": [(eq, 426)]})

    if htparam and htparam.paramgruppe != 7 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 7
        htparam.bezeichnung = "Digital Payment Secret Key"
        htparam.feldtyp = 5
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 2347

    htparam = get_cache(Htparam, {"paramnr": [(eq, 427)]})

    if htparam and htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License SelfOrder for No. of Total Outlet"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 1100

    htparam = get_cache(Htparam, {"paramnr": [(eq, 951)]})

    if htparam and htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License For Digital Payment"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 1101

    htparam = get_cache(Htparam, {"paramnr": [(eq, 952)]})

    if htparam and htparam.paramgruppe != 99 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 99
        htparam.bezeichnung = "License For Self Service Digital Payment"
        htparam.feldtyp = 4
        htparam.flogical = False
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 1102

    htparam = get_cache(Htparam, {"paramnr": [(eq, 81)]})

    if htparam.paramgruppe != 7 and (htparam.bezeichnung.lower() == "not used" or htparam.bezeichnung.lower() == ("License for Interface Keycard").lower()):

        htparam = get_cache(Htparam, {"paramnr": [(eq, 81)]})
        htparam.paramgruppe = 7
        htparam.bezeichnung = "Payment Expired Duration (Minutes):minutes; D(deptno),D(deptno), minutes;minutes"
        htparam.flogical = False
        htparam.feldtyp = 5
        htparam.fchar = ""
        htparam.reihenfolge = 2348

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2825)]})

    if htparam.paramgruppe != 21:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 2825)]})
        htparam.paramgruppe = 21
        htparam.bezeichnung = "Actived 4 Approval for Fixed Asset by PO"
        htparam.flogical = False
        htparam.feldtyp = 4
        htparam.reihenfolge = 83

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2826)]})

    if htparam and htparam.paramgruppe != 21 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 21
        htparam.bezeichnung = "Actived All Pop-Up E-Signature"
        htparam.flogical = True
        htparam.feldtyp = 4
        htparam.fchar = ""
        htparam.reihenfolge = 84

    htparam = get_cache(Htparam, {"paramnr": [(eq, 2827)]})

    if htparam and htparam.paramgruppe != 40 and htparam.bezeichnung.lower() == "not used":

        htparam.paramgruppe = 40
        htparam.bezeichnung = "Booking Engine No. for VHP CM"
        htparam.flogical = False
        htparam.feldtyp = 1
        htparam.fchar = ""
        htparam.finteger = 0
        htparam.reihenfolge = 148

    return generate_output()
