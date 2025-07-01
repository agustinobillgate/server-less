 /*IMPORTANT:
If adding or changing source code please put in the last line
*/

/*FT 011216 add art miscellaneous article for booking engine*/
FIND FIRST htparam WHERE htparam.paramnr = 41 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "Membership points:0=guest 1=reserve,2=booker"
        htparam.reihenfolge = 83.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA 29Apr2017, Order Taker License*/
FIND FIRST htparam WHERE htparam.paramnr = 1074 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1074.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Order Taker Mobile" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 1075
        htparam.fchar       = "".
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 13Sept2017, Housekepping License*/
FIND FIRST htparam WHERE htparam.paramnr = 1075 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1075.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for HouseKeeping Mobile" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 1076
        htparam.fchar       = " ".
    FIND CURRENT htparam NO-LOCK.
END.

/*FT 011216 add art miscellaneous article for booking engine*/
FIND FIRST htparam WHERE htparam.paramnr = 30 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "Misc. Article Number for Booking Engine"
        htparam.reihenfolge = 69.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END. 

/*Eko : Jul 18, 2016 A/P Voucher Approval UID Data (Bediener.nr, delimited by ";")*/
FIND FIRST htparam WHERE htparam.paramnr = 786 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 786.
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 2320
        htparam.feldtyp     = 5
        htparam.bezeich     = "User(s) A/P Approval by System (01;xx;99)"
        htparam.fchar       = ""
      .

END.

/* Jun 24, 2016 Phone Number upon C/I Mandatory */
FIND FIRST htparam WHERE htparam.paramnr = 279 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 279.
    ASSIGN
      htparam.paramgr     = 6
      htparam.reihenfolge = 69
      htparam.feldtyp     = 4
      htparam.bezeich     = "Is GCF's Mobile-No Mandatory upon C/I?"
      htparam.flogical    = NO
    .
END.


/* SY: group 25, 27 JAN 2016 */
FIND FIRST htparam WHERE htparam.paramnr = 930 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 930.
    ASSIGN
        htparam.bezeich = "Max allowed extended c/o time [HH:MM]"
        htparam.feldtyp = 5
        htparam.fchar   = ""
    .
END.

/* SY: group 40 05 JAN 2016 */
FIND FIRST htparam WHERE htparam.paramnr = 78 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 78.
    ASSIGN
        htparam.bezeich = "Web CI (IP;Port;Website)"
        htparam.feldtyp = 5
        htparam.fchar   = ""
    .
END.
FIND FIRST htparam WHERE htparam.paramnr = 79 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 79.
    ASSIGN
        htparam.bezeich = "LetterNo for WebCI email (NAT,No;...;DEF,No)"
        htparam.feldtyp = 5
        htparam.fchar   = ""
    .
END.

/* SY: group 26 24 Nov 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 787 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 787 EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich = "Loyalty Setup eg loyaltyui.r|Silver,1;Gold,2"
        htparam.feldtyp = 5
        htparam.fchar   = ""
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.  
END.
ELSE
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 787 EXCLUSIVE-LOCK.
  ASSIGN
    htparam.bezeich = "Loyalty Name & types eg GHS-Silver,1;Gold,2".
  FIND CURRENT htparam NO-LOCK.
  RELEASE htparam. 
END.

FIND FIRST htparam WHERE htparam.paramnr = 789 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 789.
    ASSIGN
        htparam.bezeich = "Loyalty Setup"
        htparam.feldtyp = 5
        htparam.fchar   = ""
    .
END.


/* SY: group 5 19 Oct 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 453 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 453.
    ASSIGN
        htparam.bezeich = "CashRefund & Rebate Articles [c1,..;r1,r2..]"
        htparam.feldtyp = 5
        htparam.fchar   = ""
    .
END.

/* SY: License for GOLF Software  14 AUG 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 299 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 299.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Golf Module" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 110
        htparam.fchar       = ""
    .
    FIND CURRENT htparam NO-LOCK.
END.

/* SY: Main group Number for discount articles  30 AUG 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 454 NO-LOCK.
IF NOT htparam.bezeich MATCHES ("*Main Group*")THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 454.
    ASSIGN
        htparam.bezeich     = "Main Group No for Disc Articles" 
        htparam.finteger    = 0
        htparam.feldtyp     = 1
    .
    FIND CURRENT htparam NO-LOCK.
END.
/* SY: GL main format 21 Juli 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 1034 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1034.
    ASSIGN
        htparam.paramgr     = 38
        htparam.bezeich     = "Digit number of G/L main acct (default 4)" 
        htparam.finteger    = 0
        htparam.reihenfolge = 33
        htparam.feldtyp     = 1
    .
    FIND CURRENT htparam NO-LOCK.
END.

/* 12/06/2015 Password Expiration, Unbalanced Bill, briefnr for Term&Condition */
FIND FIRST htparam WHERE htparam.paramnr = 1341 NO-LOCK.
IF htparam.paramgr = 30 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1341.
    ASSIGN
        htparam.paramgr  = 15
        htparam.bezeich  = "LetterNo for Bill's Term&Condition"
        htparam.feldtyp  = 1
        htparam.finteger = 0
    .
    FIND FIRST htparam WHERE htparam.paramnr = 974.
    ASSIGN
        htparam.paramgr  = 7
        htparam.bezeich  = "C/O w/ unbalanced bill allowed? (def=No)"
        htparam.feldtyp  = 4
        htparam.flogical = NO
    .
    FIND FIRST htparam WHERE htparam.paramnr = 393.
    ASSIGN
        htparam.paramgr  = 7
        htparam.bezeich  = "User PSWD expiry after xx days (def=0)"
        htparam.feldtyp  = 1
        htparam.finteger = 0
    .
    FIND FIRST htparam WHERE htparam.paramnr = 394.
    ASSIGN
        htparam.paramgr  = 7
        htparam.bezeich  = "Next PSWD expired date (param 393)"
        htparam.feldtyp  = 3
        htparam.fdate = ?
    .
END.

/* 05/06/15 Keycard Interface */
FIND FIRST htparam WHERE htparam.paramnr = 929 NO-LOCK.
IF htparam.paramgr EQ 25 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich     = "Add Keycard Program ($KCard1=xx#$KCard2=yy)"
        htparam.feldtyp     = 5
        htparam.fchar       = ""
    .
END.

/* 20/04/2015 GL */
FIND FIRST htparam WHERE htparam.paramnr = 19 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 38
        htparam.bezeich     = "Access Right 3 required to modify GL Journal?"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 32
    .
END.

/* 04/12/2014 Storage Duration */
FIND FIRST htparam WHERE htparam.paramnr = 277 NO-LOCK.
IF htparam.paramgr NE 9 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 277.
    ASSIGN
        htparam.paramgr     = 9
        htparam.bezeich     = "Save FO statistic (762 / 2000 days)"
        htparam.feldtyp     = 1
        htparam.finteger    = 762
        htparam.fchar       = ""
        htparam.reihenfolge = 267
    .
    FIND FIRST htparam WHERE htparam.paramnr = 371.
    ASSIGN
        htparam.paramgr     = 9
        htparam.bezeich     = "Save system log files (60 / 180 days)"
        htparam.feldtyp     = 1
        htparam.finteger    = 60
        htparam.fchar       = ""
        htparam.reihenfolge = 268
    .
END.

/* 18/11/2014 GL close month transfer to HO */
FIND FIRST htparam WHERE htparam.paramnr = 2843 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.paramgr NE 38 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 38
        htparam.bezeich     = "Transfer GL to Head Office IP:Port"
        htparam.feldtyp     = 5
        htparam.finteger    = 0
        htparam.fchar       = ""
        htparam.reihenfolge = 31
    .
END.


/* 30/07/2014 letterNo for RC Term and Condition */
FIND FIRST htparam WHERE htparam.paramnr = 51 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.paramgr NE 15 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 15
        htparam.bezeich     = "Letter No for RC Term & Condition"
        htparam.feldtyp     = 1
        htparam.finteger    = 0
        htparam.fchar       = ""
        htparam.reihenfolge = 136
    .
END.


/* license for VHP Mobile */
FIND FIRST htparam WHERE htparam.paramnr = 1102 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.paramgr NE 99 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License FOR VHP Mobile"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 1074
    .
END.


/* May 11/2014, Group 27 Sales Marketing */
FIND FIRST htparam WHERE paramnr = 1013.
ASSIGN
  htparam.paramgr     = 27
  htparam.feldtyp     = 5
  htparam.bezeich     = "Rounding Rate amount for the Child Rate Codes?"
  htparam.reihenfolge = 23
.
IF htparam.fchar = "" THEN 
    ASSIGN htparam.fchar = STRING(htparam.finteger) + ";0". 
/* 0 rounding, 1 round up, 2 round down */  

/* Feb 27/2014, Group 19 Cash Less Payment in  POS  */
FIND FIRST htparam WHERE htparam.paramnr = 834 NO-LOCK NO-ERROR.
DO:
    FIND FIRST htparam WHERE paramnr = 834.
    ASSIGN
      htparam.feldtyp     = 4
      htparam.bezeich     = "Allow Cashless Transaction using Pre-paid card?"
      htparam.flogical    = NO
    .
END.


FIND FIRST htparam WHERE htparam.paramnr = 569 NO-LOCK NO-ERROR.
IF htparam.bezeich = "Not Used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 569.
    ASSIGN
      htparam.feldtyp     = 1
      htparam.bezeich     = "Restaurant Article for Cashless Payment"
      htparam.finteger    = 0
    .
END.


/* November 26/2013, Group 99 License for Document Scanner  */
FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 472.
    ASSIGN
      htparam.paramgr     = 99
      htparam.feldtyp     = 4
      htparam.bezeich     = "License for Guest ID scan Program"
      htparam.flogical    = NO
      htparam.reihenfolge = 108 
      htparam.fchar       = ""
    .
END.

/* June 12/2013, Group 5 special article for APT  */
FIND FIRST htparam WHERE htparam.paramnr = 368 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 24 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 368.
    ASSIGN
      htparam.paramgr     = 24
      htparam.feldtyp     = 5
      htparam.bezeich     = "APT ArtNo for Water;Electricity;VAT"
      htparam.fchar    = ""
    .
END.

/* June 04/2013, Group 10 Password  */
FIND FIRST htparam WHERE htparam.paramnr = 256 NO-LOCK NO-ERROR.
IF htparam.feldtyp NE 4 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 256.
    ASSIGN
      htparam.paramgr     = 10
      htparam.feldtyp     = 4
      htparam.bezeich     = "Activate Strong VHP User Password Mode?"
      htparam.flogical    = NO
    .
END.

/* June 03/2013, Group 27 Sales Marketing  */
FIND FIRST htparam WHERE htparam.paramnr = 1109 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 27 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1109.
    ASSIGN
      htparam.paramgr     = 27
      htparam.feldtyp     = 4
      htparam.bezeich     = "Activate Guest Command? (Table guest-remark)"
      htparam.flogical    = NO
      htparam.reihenfolge = 25
    .
END.

/* SY 21/02/2013  */
FIND FIRST htparam WHERE htparam.paramnr = 991.
ASSIGN htparam.bezeich     = "License for General Cashier".

FIND FIRST htparam WHERE htparam.paramnr = 1006 NO-LOCK NO-ERROR.
IF htparam.feldtyp NE 1 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1006.
    ASSIGN
      htparam.feldtyp     = 1
      htparam.bezeich     = "Default SOB for Walk-in Guest"
      htparam.finteger    = 0
    .
END.

/* Dec 17, 2012 Group 30 Banquet  */
FIND FIRST htparam WHERE htparam.paramnr = 719 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 719.
    ASSIGN
      htparam.feldtyp     = 1
      htparam.bezeich     = "Cut-off-days of Banquet Booking (in days)"
      htparam.finteger    = 0
    .
END.
FIND FIRST htparam WHERE htparam.paramnr = 1373 NO-LOCK.
IF htparam.paramgr NE 15 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1373.
    ASSIGN
      htparam.paramgr     = 15
      htparam.feldtyp     = 5
      htparam.bezeich     = "Program Path for PDF"
      htparam.fchar       = ""
      htparam.reihenfolge = 13
    .
END.
FIND FIRST htparam WHERE htparam.paramnr = 1374 NO-LOCK.
IF htparam.paramgr NE 15 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1374.
    ASSIGN
      htparam.paramgr     = 15
      htparam.feldtyp     = 5
      htparam.bezeich     = "Program name of PDF"
      htparam.fchar       = ""
      htparam.reihenfolge = 14
    .
END.

/* Oct 03, 2012 Group 27 Sales Marketing  */
FIND FIRST htparam WHERE htparam.paramnr = 1058 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1058.
    ASSIGN
      htparam.paramgr     = 27
      htparam.feldtyp     = 5
      htparam.bezeich     = "ThisYR Nat KeyAcct gastNo eg 10,35,.."
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE paramnr = 1025.
    ASSIGN
      htparam.paramgr     = 27
      htparam.feldtyp     = 5
      htparam.bezeich     = "LastYR Nat KeyAcct gastNo eg 10,35,.."
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE paramnr = 278.
    ASSIGN
      htparam.paramgr     = 7
      htparam.feldtyp     = 1
      htparam.bezeich     = "SOB Code for Web Production Report"
      htparam.finteger    = 0
    .
END.


/* Sept 05, 2012 MiniBar ArtNo needed for PABX IF  */
FIND FIRST htparam WHERE htparam.paramnr = 378 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 378.
    ASSIGN
      htparam.feldtyp     = 1
      htparam.bezeich     = "MiniBar ArtNo needed for PABX IF"
      htparam.finteger    = 0
    .
END.

/* Aug 01, 2012 Send Greet Emailas Parameters  */
FIND FIRST htparam WHERE htparam.paramnr = 1379 NO-LOCK.
IF htparam.paramgr NE 15 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1379.
    ASSIGN
      htparam.paramgr     = 15
      htparam.reihenfolge = 133
      htparam.feldtyp     = 5
      htparam.bezeich     = "Param for GreetMail (server;port;usrnm;pwd)"
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE paramnr = 1396.
    ASSIGN
      htparam.paramgr     = 15
      htparam.reihenfolge = 134
      htparam.feldtyp     = 5
      htparam.bezeich     = "LetterNo for C/I emails (NAT,No;..;DEF,No)"
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE paramnr = 1397.
    ASSIGN
      htparam.paramgr     = 15
      htparam.reihenfolge = 135
      htparam.feldtyp     = 5
      htparam.bezeich     = "LetterNo for C/O emails (NAT,No;..;DEF,No)"
      htparam.fchar       = ""
    .
END.
FIND FIRST htparam WHERE htparam.paramnr = 322 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 322.
    ASSIGN
      htparam.paramgr     = 6
      htparam.reihenfolge = 68
      htparam.feldtyp     = 1
      htparam.bezeich     = "Delaytion of sending e-mails in minutes (249)"
      htparam.finteger    = 60
    .
END.

/* Jul 29, 2012 Activate Voice Mail Box */
FIND FIRST htparam WHERE htparam.paramnr = 1070 NO-LOCK.
IF htparam.bezeich EQ "Not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1070.
    ASSIGN
      htparam.feldtyp     = 4
      htparam.bezeich     = "Activate Voice Mail Box?"
      htparam.flogical    = NO
    .
END.

/* Jun 25, 2012 Email Mandatory */
FIND FIRST htparam WHERE htparam.paramnr = 249 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 249.
    ASSIGN
      htparam.paramgr     = 6
      htparam.reihenfolge = 67
      htparam.feldtyp     = 4
      htparam.bezeich     = "Is GCF's Email Address Mandatory upon C/I?"
      htparam.flogical    = NO
    .
END.

/* Jun 22, 2016 Phone Mandatory, MGM request */
FIND FIRST htparam WHERE htparam.paramnr = 250 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 250.
    ASSIGN
      htparam.paramgr     = 6
      htparam.reihenfolge = 85
      htparam.feldtyp     = 4
      htparam.bezeich     = "Is GCF's Guest Phone Mandatory upon C/I?"
      htparam.flogical    = NO
    .
END.

/* Jun 12, 2012 */
FIND FIRST htparam WHERE htparam.paramnr = 737 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 737.
    ASSIGN
      htparam.paramgr     = 6
      htparam.reihenfolge = 40
      htparam.feldtyp     = 5
      htparam.bezeich     = "R-Codes for Report by Ratecode [C1;C2;]"
      htparam.fchar       = ""
    .
END.

/* Feb 06, 2012 */
FIND FIRST htparam WHERE htparam.paramnr = 836 NO-LOCK.
IF htparam.paramgr NE 21 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 836.
    ASSIGN
      htparam.paramgr     = 21
      htparam.reihenfolge = 73
      htparam.feldtyp     = 4
      htparam.bezeich     = "PR: hierarchical approval? (Def NO)"
      htparam.flogical    = NO
    .
END.

/* Jan 12, 2012 */
FIND FIRST htparam WHERE htparam.paramnr = 439 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 439.
    ASSIGN
      htparam.paramgr     = 27
      htparam.feldtyp     = 1
      htparam.bezeich     = "DynaRate Occ: 0=RmType 1=Global 2=Optimized"
      htparam.finteger    = 1
    .
END.

/* sept 30, 2011 */
FIND FIRST htparam WHERE htparam.paramnr = 1203 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1203.
    ASSIGN
      htparam.paramgr     = 19
      htparam.feldtyp     = 4
      htparam.bezeich     = "Alert if Disc Article's VAT&Srv doesnt match?"
      htparam.flogical    = YES
      htparam.reihenfolge = 428
    .
END.

/* AUG 10, 2011 */
FIND FIRST htparam WHERE htparam.paramnr = 1019 NO-LOCK.
IF htparam.paramgr NE 8 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 1019.
    ASSIGN
      htparam.paramgr     = 8
      htparam.feldtyp     = 5
      htparam.bezeich     = "Number of Day-Use (rooms)"
      htparam.fchar       = "DAY-USE"
      htparam.reihenfolge = 184
    .
END.

/* June 6, 2011 */
FIND FIRST htparam WHERE htparam.paramnr = 341 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 341.
    ASSIGN
      htparam.feldtyp     = 5
      htparam.bezeich     = "IF-Program for WiFi-Internet"
      htparam.fchar       = ""
    .
END.
FIND FIRST htparam WHERE htparam.paramnr = 342 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 342.
    ASSIGN
      htparam.feldtyp     = 5
      htparam.bezeich     = "Program to display Room Rate"
      htparam.fchar       = ""
    .
END.


/* May 21, 2011 */
FIND FIRST htparam WHERE htparam.paramnr = 946 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 963 NO-ERROR.
    IF AVAILABLE htparam AND htparam.paramgr = 6 
      AND htparam.reihenfolge = 57 THEN htparam.reihenfolge = 999.
    FIND FIRST htparam WHERE htparam.paramnr = 946.
    ASSIGN
      htparam.paramgr     = 6
      htparam.bezeich     = "Ask deposit transfer when C/I the guest?"
      htparam.reihenfolge = 57
      htparam.feldtyp     = 4
      htparam.flogical    = NO
    .
END.
/*
/* april 10, 2011 */
RUN create-engineering.p /* htparam 319 */ NO-ERROR.
/* Add CMRS Parameters */
RUN add-htpHO.p.
/* Add CRM License */
RUN add-crmLicense.p.
*/

/* Feb 25 2011 grp 21 */
FIND FIRST htparam WHERE htparam.paramnr = 947 NO-LOCK.
IF htparam.paramgr NE 21 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 947.
    ASSIGN
      htparam.paramgr     = 21
      htparam.bezeich     = "Deduct Stocks of POS compliment bills in NA?"
      htparam.reihenfolge = 72
      htparam.feldtyp     = 4
      htparam.flogical    = NO
    .
END.

/* Oct 10  2010 grp 21 */
FIND FIRST htparam WHERE htparam.paramnr = 911 NO-LOCK.
IF htparam.paramgr EQ 13 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 911.
    ASSIGN
      htparam.paramgr     = 21
      htparam.bezeich     = "Enable Button Option in Stock Article Setup?"
      htparam.reihenfolge = 71
      htparam.feldtyp     = 4
      htparam.flogical    = NO
    .
END.

/* Sept 23 2010 grp 6 */
FIND FIRST htparam WHERE htparam.paramnr = 429 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 429.
    ASSIGN
      htparam.paramgr     = 6
      htparam.bezeich     = "Check user's Printing Access Right?"
      htparam.reihenfolge = 66
      htparam.feldtyp     = 4
      htparam.flogical    = NO
    .
END.


/* May 24 2010 grp 19 */
FIND FIRST htparam WHERE htparam.paramnr = 281 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 281.
    ASSIGN
      htparam.paramgr     = 19
      htparam.bezeich     = "Print Food/Bev DISC separately on bill?"
      htparam.reihenfolge = 84
      htparam.feldtyp     = 4
      htparam.flogical    = NO
    .
END.

/* March 01 2010 move param grp 36 to grp 15 */
FIND FIRST htparam WHERE htparam.paramnr = 2405 NO-LOCK.
IF htparam.paramgr NE 15 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 2405.
    ASSIGN
      htparam.paramgr     = 15
      htparam.bezeich     = "Param sending BEO(server;port;usernm;pw)"
      htparam.reihenfolge = 129
      htparam.feldtyp     = 5
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE htparam.paramnr = 2406.
    ASSIGN
      htparam.paramgr     = 15
      htparam.bezeich     = "Param sending CRM(server;port;usernm;pw)"
      htparam.reihenfolge = 130
      htparam.feldtyp     = 5
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE htparam.paramnr = 2407.
    ASSIGN
      htparam.paramgr     = 15
      htparam.bezeich     = "Param sending SMS/email report(server;port;usernm;pw)"
      htparam.reihenfolge = 131
      htparam.feldtyp     = 5
      htparam.fchar       = ""
    .
    FIND FIRST htparam WHERE htparam.paramnr = 2408.
    ASSIGN
      htparam.paramgr     = 15
      htparam.bezeich     = "Param sending Questionnaire(server;port;usernm;pw)"
      htparam.reihenfolge = 132
      htparam.feldtyp     = 5
      htparam.fchar       = ""
    .
END.

/* grp 6  */
FIND FIRST htparam WHERE htparam.paramnr = 962 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 962.
    ASSIGN
      htparam.bezeich     = "Post 0 Room Rate in NA program? (DEF = NO)"
      htparam.feldtyp     = 4
      htparam.fchar       = ""
      htparam.flogical    = NO
    .
END.
 
/* change description of param 695: from birth-place to type of document */
    FIND FIRST htparam WHERE htparam.paramnr = 695.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Type of Document"
      htparam.feldtyp     = 5
      htparam.fchar       = "DOCU-TYPE"
    .

/* move param grp 22 to grp 17 */
FIND FIRST htparam WHERE htparam.paramnr = 397 NO-LOCK.
IF htparam.paramgr NE 17 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 397.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "ETA Flight Number"
      htparam.reihenfolge = 171
      htparam.feldtyp     = 5
      htparam.fchar       = "ETAFL"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 713.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "ETA Time"
      htparam.reihenfolge = 172
      htparam.feldtyp     = 5
      htparam.fchar       = "ETATIME"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 714.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "ETD Flight Number"
      htparam.reihenfolge = 173
      htparam.feldtyp     = 5
      htparam.fchar       = "ETDFL"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 715.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "ETD Time"
      htparam.reihenfolge = 174
      htparam.feldtyp     = 5
      htparam.fchar       = "ETDTIME"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 725.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Birth Place"
      htparam.reihenfolge = 175
      htparam.feldtyp     = 5
      htparam.fchar       = "BIRTHPLACE"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 726.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Passport / ID Expired Date"
      htparam.reihenfolge = 176
      htparam.feldtyp     = 5
      htparam.fchar       = "ID-EXPIRED"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 730.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Purpose of Stay"
      htparam.reihenfolge = 177
      htparam.feldtyp     = 5
      htparam.fchar       = "PURPOSE"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 731.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Mobile Number"
      htparam.reihenfolge = 178
      htparam.feldtyp     = 5
      htparam.fchar       = "MOBILE"
    .
END.
FIND FIRST htparam WHERE htparam.paramnr = 733 NO-LOCK.
IF htparam.paramgr NE 17 OR htparam.fchar = "COMPANY" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 733.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Company Name of the hotel guest"
      htparam.reihenfolge = 179
      htparam.feldtyp     = 5
      htparam.fchar       = "GCOMPANY"
    .
END.

/* 12 March 2010: move param grp 22 to grp 17 */
FIND FIRST htparam WHERE htparam.paramnr = 759 NO-LOCK.
IF htparam.paramgr NE 17 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 759.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Reserved Name Address 1"
      htparam.reihenfolge = 180
      htparam.feldtyp     = 5
      htparam.fchar       = "RSV-adr1"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 760.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Reserved Name Address 2"
      htparam.reihenfolge = 181
      htparam.feldtyp     = 5
      htparam.fchar       = "RSV-adr2"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 761.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Reserved Name Address 3"
      htparam.reihenfolge = 182
      htparam.feldtyp     = 5
      htparam.fchar       = "RSV-adr3"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 762.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Reserved Name City"
      htparam.reihenfolge = 183
      htparam.feldtyp     = 5
      htparam.fchar       = "RSV-city"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 763.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Reserved Name ZIP code"
      htparam.reihenfolge = 184
      htparam.feldtyp     = 5
      htparam.fchar       = "RSV-ZIP"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 765.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "Reserved Name Country"
      htparam.reihenfolge = 185
      htparam.feldtyp     = 5
      htparam.fchar       = "RSV-country"
    .
    FIND FIRST htparam WHERE htparam.paramnr = 766.
    ASSIGN
      htparam.paramgr     = 17
      htparam.bezeich     = "CreditCard No, Expiry MM/YYYY"
      htparam.reihenfolge = 186
      htparam.feldtyp     = 5
      htparam.fchar       = "CCard"
    .
END.

/* SMS: paramGroup for SMS CFG, 02/18/2010 */
FIND FIRST htparam WHERE htparam.paramnr = 839 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich     = "Letter Category Number for SMS Report CFG"
        htparam.feldtyp     = 1
        htparam.finteger    = 0
    .
END.

/* from add-crmLicens.p, 02/05/2009 */
FIND FIRST htparam WHERE htparam.paramnr = 1459 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License FOR CRM Module"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 1073
    .
END.

/* 07 JAN 2010: Path of PF file for VHParchive */
FIND FIRST htparam WHERE htparam.paramnr = 347 NO-LOCK.
IF htparam.paramgr NE 13 OR htparam.bezeich = "Not used"
    OR htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 347.
    ASSIGN
        htparam.paramgr     = 13
        htparam.reihenfolge = 11
        htparam.bezeich     = "PF Path file for VHPArchive DB"  
        htparam.fchar       = ""
        htparam.feldtyp     = 5
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/* 03 Dec 2009: Apply FLag for Sales Restriction Check */
FIND FIRST htparam WHERE htparam.paramnr = 1202 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1202.
    ASSIGN
        htparam.paramgr     = 27
        htparam.reihenfolge = 3
        htparam.bezeich     = "Restriction on GCF modification applied? (DEF=No)"  
        htparam.flogical    = NO
        htparam.feldtyp     = 4
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/* 24 Oct 2009: GC Proforma Invoice */
FIND FIRST htparam WHERE htparam.paramnr = 1018 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1018.
    ASSIGN
        htparam.paramgr     = 38
        htparam.reihenfolge = 30
        htparam.bezeich     = "PI Cheque/Giro Temporary AcctNo"  
        htparam.fchar       = ""
        htparam.feldtyp     = 5
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


/* 13 Oct 2009: GC Proforma Invoice */
FIND FIRST htparam WHERE htparam.paramnr = 931 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 931.
    ASSIGN
        htparam.paramgr     = 38
        htparam.reihenfolge = 29
        htparam.bezeich     = "Proforma Invoice Temporary AcctNo"  
        htparam.fchar       = ""
        htparam.feldtyp     = 5
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/* 29 Sept 2009: Extra bed + baby cot for HK */
FIND FIRST htparam WHERE htparam.paramnr = 2999 NO-LOCK.
DO:
    IF htparam.paramgr NE 5 THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = 2999.
        ASSIGN
            htparam.paramgr     = 5
            htparam.reihenfolge = 68
            htparam.bezeich     = "Article Number for Extra Bed [eg n1;n2;n3;]"  
            htparam.fchar       = ""
            htparam.feldtyp     = 5
        .
        FIND CURRENT htparam NO-LOCK.
        RELEASE htparam.
    END.
END.

/* 25/06/2009: Group 15 */
FIND FIRST htparam WHERE htparam.paramnr = 893 NO-LOCK.
IF htparam.paramgr NE 15  THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 893.
    ASSIGN
        htparam.bezeich     = "LetterNo for Advance GUEST Bill"
        htparam.feldtyp     = 1
        htparam.paramgr     = 15
        htparam.reihenfolge = 99
    .
END.

/* 20/07/2009 Group 10 */
FIND FIRST htparam WHERE paramnr = 173.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password for Posting FO VOID Item".


/* 02/06/2009: Group 8 */
FIND FIRST htparam WHERE htparam.paramnr = 810 NO-LOCK.
IF htparam.bezeich MATCHES ("*PAYING*") THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 810.
    ASSIGN
        htparam.bezeich     = "Number of Guests(Adult + compl + ch1 + ch2)"  
    .
END.

/* 28/05/2009: Group 6 */
FIND FIRST htparam WHERE htparam.paramnr = 961 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 961.
    ASSIGN
        htparam.bezeich     = "Is Guest Title mandatory in GCF? (Def NO)"  
        htparam.feldtyp     = 4
        htparam.flogical    = NO
    .
END.

/*20/05/09: For nt-KNGfbrev, for splitting FB revenue by shift*/
FIND FIRST htparam WHERE htparam.paramnr = 369 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 369.
    ASSIGN
        htparam.bezeich     = "nt-KNGfbRev.r param:D1,F1,..,F4,B1..B4;D2,F1..F4"
        htparam.feldtyp     = 5
        htparam.fchar       = "".
    .
    FIND CURRENT htparam NO-LOCK.
END.

/* 17/03/2009: Optional ACCOR Reports */
FIND FIRST htparam WHERE htparam.paramnr = 567 NO-LOCK.
IF (NOT htparam.bezeich MATCHES ("*ACCOR*"))
    OR htparam.feldtyp NE 4 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 567.
    ASSIGN
        htparam.bezeich     = "Enable ACCOR Reports? (CNTL-P)"  
        htparam.feldtyp     = 4
        htparam.flogical    = NO
    .
END.


/* 13/02/2009: CRM quesionnair in group sales */
FIND FIRST htparam WHERE htparam.paramnr = 960 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 960.
    ASSIGN
        htparam.paramgr     = 27
        htparam.reihenfolge = 15
        htparam.bezeich     = "Cutoff days for Not sending back questionnair"  
        htparam.finteger    = 30
        htparam.fdecimal    = 0
        htparam.feldtyp     = 1
    .
END.


/* 27/01/2009: CRM in htparam group27 modulesSales */
FIND FIRST htparam WHERE htparam.paramnr = 794 NO-LOCK.
IF htparam.paramgr NE 27 OR htparam.feldtyp = 5 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 794.
    ASSIGN
        htparam.paramgr     = 27
        htparam.reihenfolge = 13
        htparam.bezeich     = 'Quesionnaire "EventNo;DeptNo;" for c/o guests'
        htparam.finteger    = 0
        htparam.fchar       = ""
        htparam.feldtyp     = 5
    .
END.

/* 27/11/2008 GL keyword for P&L in Foreign Amount */
FIND FIRST htparam WHERE htparam.paramnr = 2073 NO-LOCK.
IF NOT htparam.bezeich MATCHES ("*P$L*") THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 2073 EXCLUSIVE-LOCK.
  ASSIGN 
    htparam.bezeich = "Keyword for P&L Report in Foreign Currency"
    htparam.fchar   = "IN-FOREIGN"
  .
  FIND CURRENT htparam NO-LOCK.
END.

/* 25/11/2008 License for Report Generator */
FIND FIRST htparam WHERE htparam.paramnr = 1072 EXCLUSIVE-LOCK.
ASSIGN htparam.bezeich     = "License for VHP Report Generator".
FIND CURRENT htparam NO-LOCK.

/* 14/11/2008 keyword bill parser */
FIND FIRST htparam WHERE htparam.paramnr = 711 NO-LOCK.
IF htparam.paramgr NE 17 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 711 EXCLUSIVE-LOCK.
  ASSIGN
      htparam.paramgr     = 17
      htparam.reihenfolge = 170
      htparam.bezeich     = "(Turkish) Citizen ID Number"
      htparam.feldtyp     = 5
      htparam.fchar       = "TCID"
  .
  FIND CURRENT htparam NO-LOCK.
END.

/* 21/10/2008 CRM - Directory for Attachment file */
FIND FIRST htparam WHERE htparam.paramnr = 430 NO-LOCK.
IF htparam.bezeich = "Not used" OR htparam.fchar = "" THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 430 EXCLUSIVE-LOCK.
  ASSIGN
      htparam.bezeich     = "Directory for Confirmation Attached File"
      htparam.fchar       = "c:\vhp\"
  .
  FIND CURRENT htparam NO-LOCK.
END.

/* 23/09/2008 Group 7 */
FIND FIRST htparam WHERE htparam.paramnr = 478.
ASSIGN htparam.bezeich = "Default Rsv Stat: 0GTD 1Tent 2=6PM 3=OralConf".

/* 20/09/2008 Restaurant */
FIND FIRST htparam WHERE htparam.paramnr = 948 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 948 EXCLUSIVE-LOCK.
  ASSIGN
      htparam.feldtyp     = 4
      htparam.reihenfolge = 83
      htparam.paramgr     = 19
      htparam.bezeich     = "Print TOTAL Food/Bev/Other Amount? (Def=NO)"
      htparam.flogical    = NO
      htparam.fchar       = ""
      htparam.finteger    = 0
  .
  FIND CURRENT htparam NO-LOCK.
END.


/* 19/09/2008 FO */
FIND FIRST htparam WHERE htparam.paramnr = 938 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 938 EXCLUSIVE-LOCK.
  ASSIGN
      htparam.feldtyp  = 4
      htparam.bezeich  = "Use 'ORAL CONFIRM' Reservation Status?"
      htparam.flogical = YES
      htparam.fchar = ""
  .
  FIND CURRENT htparam NO-LOCK.
  FIND FIRST htparam WHERE htparam.paramnr = 939 EXCLUSIVE-LOCK.
  ASSIGN
      htparam.feldtyp  = 4
      htparam.bezeich  = "Use 'FIRST NAME' in individual GCF?"
      htparam.flogical = YES
      htparam.fchar = ""
  .
  FIND CURRENT htparam NO-LOCK.
END.



/* 15/09/2008 Engineering */

FIND FIRST htparam WHERE htparam.paramnr = 1200 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1200 EXCLUSIVE-LOCK.
  ASSIGN
      htparam.feldtyp  = 1
      htparam.bezeich  = "User GroupNo for Engineering Department"
      htparam.finteger = 0.
  FIND CURRENT htparam NO-LOCK.
  FIND CURRENT htparam NO-LOCK.
  FIND FIRST htparam WHERE htparam.paramnr = 1203 EXCLUSIVE-LOCK.
  ASSIGN htparam.bezeich = "Not used".
  FIND CURRENT htparam NO-LOCK.
  FIND FIRST htparam WHERE htparam.paramnr = 1204 EXCLUSIVE-LOCK.
  ASSIGN htparam.bezeich = "Not used".
  FIND CURRENT htparam NO-LOCK.
  FIND FIRST paramtext WHERE txtnr = 152 EXCLUSIVE-LOCK. 
  ASSIGN paramtext.ptexte = "Engineering Module".
  FIND CURRENT paramtext NO-LOCK.
END.

/* 15/07/2008  */

FIND FIRST htparam WHERE paramnr = 358 NO-LOCK.
IF htparam.bezeich NE "License for Internet Billing System" THEN
DO:
  FIND CURRENT htparam EXCLUSIVE-LOCK.
  ASSIGN 
      htparam.bezeich     = "License for Internet Billing System"
  .
  FIND CURRENT htparam NO-LOCK.
END.

/* 03/07/2008  */

FIND FIRST htparam WHERE paramnr = 887 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND CURRENT htparam EXCLUSIVE-LOCK.
  ASSIGN 
      htparam.bezeich     = "Acct-No for FA A/P (default = A/P Trade)"
      htparam.feldtyp     = 5
      htparam.fchar       = "". 
  FIND CURRENT htparam NO-LOCK.
END.

/* 22/05/2008  */
FIND FIRST htparam WHERE paramnr = 793 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO:
  FIND CURRENT htparam EXCLUSIVE-LOCK.
  ASSIGN 
      htparam.bezeich     = "Transfer F/O journal for departments e.g. 0,1,2"
      htparam.feldtyp     = 5
      htparam.paramgr     = 38
      htparam.reihenfolge = 28
      htparam.fchar       = "". 
  FIND CURRENT htparam NO-LOCK.
END.

/* 07/04/2008 Group 8 */
FIND FIRST htparam WHERE paramnr = 129 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 129.
  ASSIGN 
      htparam.bezeich     = "Number of VACANT rooms"
      htparam.feldtyp     = 5
      htparam.reihenfolge = 17
      htparam.paramgr     = 8
      htparam.fchar       = "VACANT". 
END.


/* 27/02/2008 Group 17 */
FIND FIRST htparam WHERE paramnr = 1110 NO-LOCK.
IF htparam.fchar = "" THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1110.
  ASSIGN 
      htparam.bezeich = "Today's Billing Date"
      htparam.reihenfolge = 161 
      htparam.fchar   = "BillDate". 
END.


/* 12/02/2008 Group 5 */
FIND FIRST htparam WHERE paramnr = 132 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 132.
  ASSIGN 
      htparam.feldtyp = 5
      htparam.bezeich = htparam.bezeich + " [e.g. n1;n2;n3;]"
      htparam.fchar   = TRIM(STRING(htparam.finteger,">>>>9")) + ";". 
END.

/* 05/02/2008 Group 6 */
FIND FIRST htparam WHERE paramnr = 933 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 933.
  ASSIGN 
      htparam.bezeich  = "Stay-Pay Nite Use AvrgRate Option? (Def NO)"
      htparam.feldtyp  = 4
      htparam.flogical = NO.
END.

/* 28/01/2008 Group 6 */
FIND FIRST htparam WHERE paramnr = 736 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 736.
  ASSIGN 
      htparam.bezeich  = "ProgName for Calculating ResNo (HV)"
      htparam.feldtyp  = 5
      htparam.fchar = "".
END.

/* 24/01/2008 Group 6 */
FIND FIRST htparam WHERE paramnr = 431 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 431.
  ASSIGN 
      htparam.bezeich  = "Default Confirmation Letter Number"
      htparam.feldtyp  = 1
      htparam.finteger = 0.
END.

/* 21/01/2008 Group 6 */
FIND FIRST htparam WHERE paramnr = 571 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 571.
  ASSIGN 
      htparam.bezeich = "Floor Plan BOX Height x Width [eg 70 x 500]"
      htparam.feldtyp = 5
      htparam.fchar   = "".
END.

FIND FIRST htparam WHERE paramnr = 968 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 968.
  ASSIGN 
      htparam.bezeich  = "Search Guest Name Start Field: 0=Name 1=ID"
      htparam.feldtyp  = 1
      htparam.finteger = 0.
END.

FIND FIRST htparam WHERE paramnr = 123 NO-LOCK.
IF htparam.paramgr NE 7 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 123.
  ASSIGN 
      htparam.bezeich     = "Dummy INDIVIDUAL Company GuestNo"
      htparam.paramgr     = 7
      htparam.reihenfolge = 32
      htparam.feldtyp     = 1
      htparam.finteger    = 0.
END.


/* 18/01/2008 Group 15 */
FIND FIRST htparam WHERE paramnr = 455 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 455.
  ASSIGN htparam.bezeich = "ProgName for Money Exchange Receipt".
  ASSIGN
      htparam.feldtyp  = 5
      htparam.fchar    = "".
END.

/* 10/01/2008 Group 5 */
FIND FIRST htparam WHERE paramnr = 1009 NO-LOCK.
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1009.
  ASSIGN htparam.bezeich = "Rest. Discount ArtNo for 2nd VAT".
  IF htparam.feldtyp NE 1 THEN
  ASSIGN
      htparam.feldtyp  = 1
      htparam.finteger = 0.
END.


/* 30/12/2007 Group 7 */
FIND FIRST htparam WHERE paramnr = 271 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 271.
  ASSIGN 
    htparam.feldtyp     = 4
    htparam.bezeich     = "Apply Multi VAT in the POS?"
    htparam.flogical    = NO.
END.


/* 30/12/2007 Group 17 */
FIND FIRST htparam WHERE paramnr = 764 NO-LOCK.
IF htparam.paramgr NE 17 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 764.
  ASSIGN 
    htparam.paramgr     = 17
    htparam.feldtyp     = 5
    htparam.reihenfolge = 78
    htparam.bezeich     = "Summary of VAT% - VAT - Net - Amount"
    htparam.fchar       = "VAT-SUM".
END.


/* 05/12/2007 Group 9 */
FIND FIRST htparam WHERE paramnr = 237 NO-LOCK.
IF htparam.paramgr NE 9 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 237.
  ASSIGN 
    htparam.paramgr     = 9
    htparam.feldtyp     = 1
    htparam.bezeich     = "Storage Duration for closed P/O"
    htparam.finteger    = 60.
END.

/* 23/11/2007 Group 38 */
FIND FIRST htparam WHERE paramnr = 1012 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1012.
  ASSIGN 
    htparam.paramgr     = 38
    htparam.reihe       = 27
    htparam.feldtyp     = 1
    htparam.bezeich     = "G/L Transaction: MaxChar allowed for RefNo"
    htparam.finteger    = 0.
END.

/* 19/10/2007 Group 13 */
FIND FIRST htparam WHERE paramnr = 325 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 325.
  ASSIGN 
    htparam.feldtyp     = 4
    htparam.bezeich     = "Create Calls Record when PABX rate = 0?".
END.

/* 01/09/2007 Group 10 */
FIND FIRST htparam WHERE paramnr = 172.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password for Posting Misc POS Item".


/* 04/08/2007 Group 39 */
FIND FIRST htparam WHERE paramnr = 1398 NO-LOCK.
IF htparam.paramgr NE 39 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 1398. 
  ASSIGN 
    htparam.paramgr     = 39
    htparam.bezeich     = "Deactive YTD amount when calc JAN..DEC balance" 
    htparam.feldtyp     = 5
    htparam.fchar       = "YTDaus"
    htparam.reihenfolge = 78
  . 
END.


/* 02/08/2007 Group 39 */
FIND FIRST htparam WHERE paramnr = 2200 NO-LOCK NO-ERROR.
IF NOT AVAILABLE htparam THEN
DO:
  CREATE htparam. 
  ASSIGN 
    htparam.paramnr     = 2200
    htparam.paramgr     = 39
    htparam.bezeich     = "To-date's Exchange Rate" 
    htparam.feldtyp     = 5
    htparam.fchar       = "EXRATE"
    htparam.reihenfolge = 77
  . 
END.

/* 31/07/2007 Group 19 */
FIND FIRST htparam WHERE paramnr = 88 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 88. 
  ASSIGN 
    htparam.paramgr     = 19
    htparam.bezeich     = "Print official Rest Bill (Turkey)?" 
    htparam.feldtyp     = 4
    htparam.flogical    = NO
    htparam.reihenfolge = 13
  . 
END.

/* 13/07/2007 Group 21 */
FIND FIRST htparam WHERE paramnr = 1080 NO-LOCK.
IF htparam.paramgr NE 21 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 1080. 
  ASSIGN 
    htparam.paramgr     = 21
    htparam.bezeich     = "Store Stocks Onhand when closing inventory?" 
    htparam.feldtyp     = 4
    htparam.flogical    = NO
    htparam.reihenfolge = 70
  . 
END.



/* 11/07/2007 Group 7 */
FIND FIRST htparam WHERE paramnr = 109 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 109. 
  ASSIGN 
    htparam.bezeich  = "Dummy Walk-in Company GuestNo" 
    htparam.feldtyp  = 1
    htparam.finteger = 0
  . 
END.


/* 08/07/2007 Group 5 */
FIND FIRST htparam WHERE paramnr = 116 NO-LOCK.
IF htparam.bezeich = "Not Used" THEN
DO:
  FIND FIRST htparam WHERE paramnr = 116. 
  ASSIGN 
    htparam.bezeich  = "F/O SubgrpNo for unallocated C/L article" 
    htparam.feldtyp  = 1
    htparam.finteger = 0
  . 
END.

/* 21/04/2007 Group 5 */
FIND FIRST htparam WHERE paramnr = 738 NO-LOCK.
IF htparam.bezeich = "Not Used" THEN
DO:
  FIND FIRST htparam WHERE paramnr = 738. 
  ASSIGN 
    htparam.bezeich  = "F/O Article for rounding of Bill Amount" 
    htparam.finteger = 0
  . 
END.


/* 09/04/2007 Group 6 */
FIND FIRST htparam WHERE paramnr = 262 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 262. 
  ASSIGN 
    htparam.feldtyp  = 1
    htparam.bezeich  = "No of Adult(s) for new reservation (def = 1)" 
    htparam.finteger = 1
  . 
END.


/* 11/03/2007 Group 25 */
FIND FIRST htparam WHERE paramnr = 437 NO-LOCK.
IF htparam.bezeich = "Not used" THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 437. 
  ASSIGN 
    htparam.bezeich  = "Allow cancel Reservation after generating keycard?" 
    htparam.flogical = NO
  . 
END.


/* 04/03/2007 Group 19 Restaurant */
FIND FIRST htparam WHERE paramnr = 949 NO-LOCK.
IF htparam.paramgr NE 19 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 949. 
  ASSIGN 
    htparam.feldtyp     = 1
    htparam.bezeich     = "Department No for MiniBar" 
    htparam.fchar       = ""
    htparam.finteger    = 0
    htparam.reihenfolge = 82
    htparam.paramgr     = 19
  . 
END.

/* 19/02/2007 Group 6 Customer Articles */
FIND FIRST htparam WHERE paramnr = 716 NO-LOCK.
IF htparam.feldtyp NE 5 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 716. 
  ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Parameters for Daily Sales Report I" 
    htparam.fchar       = ""
  . 
END.
FIND FIRST htparam WHERE paramnr = 732 NO-LOCK.
IF htparam.feldtyp NE 5 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 732. 
  ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Parameters for Daily Sales Report II" 
    htparam.fchar       = ""
  . 
END.

/* 25/01/2007 Group 6 Customer Articles */
FIND FIRST htparam WHERE paramnr = 297 NO-LOCK.
IF htparam.feldtyp NE 1 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 297. 
  ASSIGN 
    htparam.feldtyp     = 1
    htparam.bezeich     = "Change 6PM to other time, eg. 4=4PM (Param373)" 
    htparam.finteger    = 0
  . 
END.


/**** CLUB SW, 22 Nov 2006 */
FIND FIRST htparam WHERE paramnr = 1047 NO-LOCK.
IF htparam.feldtyp = 4 AND bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich = "F/O ArtNo for Club Initial Fee"
        htparam.feldtyp = 1
        htparam.finteger = 0.
    FIND CURRENT htparam NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 1048 EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich = "F/O ArtNo for Club Discount"
        htparam.feldtyp = 1
        htparam.finteger = 0.
    FIND CURRENT htparam NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 1049 EXCLUSIVE-LOCK.
    ASSIGN 
        htparam.bezeich = "Create renewal ... days before expired"
        htparam.feldtyp = 1
        htparam.finteger = 0.
    FIND CURRENT htparam NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 1050 EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich = "Display warning for segment VIP?"
        htparam.feldtyp = 4
        htparam.flogical = NO.
    FIND CURRENT htparam NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 1056 EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich = "Display warning for segment Black List?"
        htparam.feldtyp = 4
        htparam.flogical = NO.
    FIND CURRENT htparam NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 1057 EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich  = "Save Check-In history (Days)"
        htparam.feldtyp  = 1
        htparam.finteger = 365.
    FIND CURRENT htparam NO-LOCK.
END.


/* 08/11/2006 Group 5 Special Article */
FIND FIRST htparam WHERE paramnr = 118 NO-LOCK.
IF htparam.reihenfolge NE 22 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 118. 
  ASSIGN 
    htparam.reihenfolge = 22
    htparam.bezeich     = "Article Number for Internet Charges" 
    htparam.finteger    = 0
  . 
END.

/* 04/10/2006 Group 17 Purchase Parser */
FIND FIRST htparam WHERE paramnr = 1004 NO-LOCK.
IF htparam.paramgr NE 17 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 1004. 
  ASSIGN 
    htparam.paramgr     = 17 
    htparam.bezeich     = "P/O Order Name" 
    htparam.feldtyp     = 5
    reihenfolge         = 168
    htparam.fchar       = "odname"
  . 
  FIND FIRST htparam WHERE paramnr = 1005. 
  ASSIGN 
    htparam.paramgr     = 17 
    htparam.bezeich     = "P/O Order Item's Remark" 
    htparam.feldtyp     = 5
    reihenfolge         = 169
    htparam.fchar       = "bl-remark"
  . 
END.

/* 01/10/2006 Group 21 cost control */
FIND FIRST htparam WHERE paramnr = 1064 NO-LOCK.
IF htparam.paramgr NE 21 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 1064. 
  ASSIGN 
    htparam.paramgr     = 21 
    htparam.bezeich     = "Subgroups for HK Onhand List (format n1;n2;)" 
    htparam.feldtyp     = 5
    reihenfolge         = 43
    htparam.fchar       = ""
  . 
END.

/* 30/09/2006 ALL Inclusive Argt for ARL List,group 6 */
FIND FIRST htparam WHERE htparam.paramnr = 496 NO-LOCK.
IF htparam.feldtyp NE 5 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 496.
  ASSIGN
    htparam.bezeich     = "Argt Code for All Inclusive (argt1;argt2;..)"
    htparam.feldtyp     = 5
    htparam.fchar       = ""
  .
END.

/* 06/09/2006 Kitchen Printer */
FIND FIRST htparam WHERE htparam.paramnr = 252 NO-LOCK.
IF htparam.paramgr NE 1 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 252.
  ASSIGN
    htparam.bezeich     = "KitchPrinter:#-Lines before cutting (def 4)"
    htparam.feldtyp     = 1
    htparam.finteger    = 0
    htparam.paramgr     = 1
    htparam.reihenfolge = 100
  .
  FIND FIRST htparam WHERE htparam.paramnr = 562.
  ASSIGN
    htparam.bezeich     = "KitchPrinter:#-Lines after cutting (def 5)"
    htparam.feldtyp     = 1
    htparam.finteger    = 0
    htparam.paramgr     = 1
    htparam.reihenfolge = 101
    .
END.



/* 09/01/2004 Param Group 21 */ 
FIND FIRST htparam WHERE htparam.paramnr = 1080 NO-LOCK.
IF NOT htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1080.
  ASSIGN
    htparam.bezeich     = "Storage Number for House Keeping Items"
    htparam.feldtyp     = 1
    htparam.finteger    = 0
    htparam.paramgr     = 21
    htparam.reihenfolge = 36
  .
END.

/* 08/25/2004 Param Group 15 
  Master Bill Single Line Foreign currncy 
*/ 
FIND FIRST htparam WHERE htparam.paramnr = 495 NO-LOCK.
IF NOT htparam.bezeich MATCHES ("*Single Line*") THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 495.
  ASSIGN
    htparam.bezeich = "LetterNo MasterBill Single Line - Foreign Currency"
    htparam.feldtyp = 1
    htparam.finteger = 0.
END.

/* group 3, 19 Aug 2006 */
FIND FIRST htparam WHERE paramnr = 208 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 208.
  ASSIGN
    htparam.feldtyp  = 4
    htparam.bezeich  = "Allow opened Master Bill when all guests C/O?"
    htparam.flogical = NO
  .
END.


/* group 39 */
FIND FIRST htparam WHERE paramnr = 2076.
ASSIGN
    htparam.bezeich = "YTD option for Monthly Balance (PnL Acct)"
    htparam.fchar   = "YTDein".


/* 27/07/2006 Group 6 */
FIND FIRST htparam WHERE paramnr = 1099 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1099.
  ASSIGN 
    htparam.paramgr     = 27
    htparam.feldtyp     = 4
    htparam.flogical    = NO
    htparam.bezeich     = "Send email to guest when guest checks out?"
    htparam.reihenfolge = 12
  .
END.


/* 26/07/2006 Group 10 Password */
FIND FIRST htparam WHERE paramnr = 1071.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password for Parameter Group 10 (Password)".

/* 20/07/2006 Group 6 */
FIND FIRST htparam WHERE paramnr = 239 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 47.
  ASSIGN htparam.reihenfolge = 16.
  FIND FIRST htparam WHERE htparam.paramnr = 239.
  ASSIGN 
    htparam.feldtyp     = 1
    htparam.bezeich     = "Above xx rooms (param 97, default = 20)"
    htparam.reihenfolge = 15
    htparam.finteger    = 0.
END.

/* 10/04/2006 Group 15 */

FIND FIRST htparam WHERE paramnr = 418.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Output Directory for F/O & G/L Excel Report".

/* 09/04/2006 Group 10 */

FIND FIRST htparam WHERE paramnr = 170.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password of Excel .xls files - F/O Reports".

FIND FIRST htparam WHERE paramnr = 171.
ASSIGN 
    htparam.feldtyp     = 5 
    htparam.bezeich     = "Password of Excel .xls files - G/L Reports".

/* 09/03/2006 Group 6 */

FIND FIRST htparam WHERE paramnr = 932 NO-LOCK.
IF htparam.feldtyp NE 4 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 932. 
  ASSIGN 
    htparam.feldtyp     = 4
    htparam.bezeich     = "Generate F/O BillNo when guest C/I (def=NO)?" 
    htparam.flogical    = NO. 
END.

/* 28/01/2006 Group 21 cost control */
FIND FIRST htparam WHERE paramnr = 1060 NO-LOCK.
IF htparam.paramgr NE 21 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 1060. 
  ASSIGN 
    htparam.paramgr     = 21 
    htparam.bezeich     = "User GroupNo for Engineering Department" 
    htparam.feldtyp     = 1
    htparam.finteger    = 0. 
  
  FIND FIRST htparam WHERE paramnr = 1061. 
  ASSIGN 
    htparam.paramgr     = 21 
    htparam.bezeich     = "Storage Number for Engineering Department" 
    htparam.feldtyp     = 1
    htparam.finteger    = 0. 

  FIND FIRST htparam WHERE paramnr = 1062. 
  ASSIGN 
    htparam.paramgr     = 21 
    htparam.bezeich     = "Engineering's Cost Department Number" 
    htparam.feldtyp     = 1
    htparam.finteger    = 0. 
END.


/* 21/01/2006 Group 17 add keyword  */
FIND FIRST htparam WHERE paramnr = 2401 NO-LOCK.
IF htparam.paramgr NE 17 THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 2401. 
  ASSIGN 
    htparam.paramgr     = 17
    htparam.reihenfolge = 157 
    htparam.bezeich     = "Current User Name" 
    htparam.feldtyp     = 5
    htparam.fchar       = "UserName". 
END.


/* 08/01/2006 Group 27 Sales Marketing */

FIND FIRST htparam WHERE paramnr = 550 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 550. 
  ASSIGN 
    htparam.bezeich  = "Use Advance Contract Rate Setup (PRO Version)?" 
    htparam.feldtyp  = 4 
    htparam.flogical = NO. 
END.

FIND FIRST htparam WHERE paramnr = 549 NO-LOCK.
IF htparam.feldtyp NE 1 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 549. 
  ASSIGN 
    htparam.bezeich  = "Rate Disc: 0=Average 1=As-Is 2=Min 3=Max" 
    htparam.feldtyp  = 1 
    htparam.finteger = 0
    htparam.reihenfolge = 11. 
END.

/* 30/12/2005 Group 19 */

FIND FIRST htparam WHERE paramnr = 739 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 739. 
  ASSIGN 
    htparam.reihenfolge = 427
    htparam.paramgr  = 19
    htparam.bezeich  = "Ask Bill counter number when closing the bill?" 
    htparam.feldtyp  = 4 
    htparam.flogical = NO. 
END.

/* 28/11/2005 Group 8 */

FIND FIRST htparam WHERE paramnr = 179 NO-LOCK.
IF htparam.paramgr NE 8 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 179. 
  ASSIGN 
    htparam.paramgr = 8
    htparam.reihenfolge = 183
    htparam.bezeich = "Room Number of selected Room Type" 
    htparam.feldtyp = 5 
    htparam.fchar = "RM-RMCAT". 
END.

FIND FIRST htparam WHERE paramnr = 85 NO-LOCK.
IF htparam.paramgr NE 8 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 85. 
  ASSIGN 
    htparam.paramgr = 8
    htparam.reihenfolge = 179
    htparam.bezeich = "Arrivals thru Reservation (Rooms)" 
    htparam.feldtyp = 5 
    htparam.fchar = "RM-RSV". 

  FIND FIRST htparam WHERE paramnr = 86. 
  ASSIGN 
    htparam.paramgr = 8
    htparam.reihenfolge = 180
    htparam.bezeich = "Arrivals thru Reservation (Adults)" 
    htparam.feldtyp = 5 
    htparam.fchar = "PRS-RSV". 
  
  FIND FIRST htparam WHERE paramnr = 106. 
  ASSIGN 
    htparam.paramgr = 8
    htparam.reihenfolge = 181
    htparam.bezeich = "Arrivals thru Walk-in Guest (Rooms)" 
    htparam.feldtyp = 5 
    htparam.fchar = "RM-WIG". 
  
  FIND FIRST htparam WHERE paramnr = 107. 
  ASSIGN 
    htparam.paramgr = 8
    htparam.reihenfolge = 182
    htparam.bezeich = "Arrivals thru Walk-in Guest (Adults)" 
    htparam.feldtyp = 5 
    htparam.fchar = "PRS-WIG". 
END.

/* 17/10/2005 Group 19 Restaurant  */ 

FIND FIRST htparam WHERE htparam.paramnr = 833 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 833. 
    ASSIGN 
      htparam.feldtyp = 4 
      htparam.bezeich = "Cash Payment: USE Multi-Currency Mode?" 
      htparam.flogical = NO 
    . 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 830 NO-LOCK. 
IF htparam.feldtyp NE 5 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 830. 
    ASSIGN 
      htparam.feldtyp = 5 
      htparam.bezeich = "MultiCurr Total Amount in bill (eg. USD;EURO)" 
      htparam.fchar = "" 
    . 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 874 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 874. 
    ASSIGN 
      htparam.feldtyp = 4 
      htparam.bezeich = "POS Bill: Always print all items? (roll printer)" 
      htparam.flogical = NO 
    . 
END. 
 
/* 02/10/2005 Group 26 Club Module  */ 
 
FIND FIRST htparam WHERE htparam.paramnr = 1040 NO-LOCK. 
IF htparam.feldtyp NE 1 THEN 
DO: 
    FIND FIRST paramtext WHERE paramtext.txtnr = 149. 
    paramtext.ptexte = "CLUB Module". 
    FIND FIRST htparam WHERE paramnr = 1040. 
    ASSIGN 
      htparam.feldtyp = 1 
      htparam.bezeich = "Max number of member freezing allowed" 
      htparam.finteger = 1 
    . 
    FIND FIRST htparam WHERE paramnr = 1041. 
    ASSIGN 
      htparam.feldtyp = 1 
      htparam.bezeich = "Max age valid for Child/Junior Member" 
      htparam.finteger = 16 
    . 
    FIND FIRST htparam WHERE paramnr = 1042. 
    ASSIGN 
      htparam.feldtyp = 1 
      htparam.bezeich = "Club Opening Hour (1 - 24)" 
      htparam.finteger = 6 
    . 
    FIND FIRST htparam WHERE paramnr = 1044. 
    ASSIGN 
      htparam.feldtyp = 1 
      htparam.bezeich = "Club Closing Hour (1 - 24)" 
      htparam.finteger = 22 
    . 
    FIND FIRST htparam WHERE paramnr = 1045. 
    ASSIGN 
      htparam.feldtyp = 1 
      htparam.bezeich = "Department number of the CLUB" 
      htparam.finteger = 0 
    . 
    FIND FIRST htparam WHERE paramnr = 1046. 
    ASSIGN 
      htparam.feldtyp = 1 
      htparam.bezeich = "F/O ArtNo for Club Membership Fee" 
      htparam.finteger = 0 
    . 
 
END. 
 
/* 02/10/2005 Group 25 KeyCard  */ 
 
FIND FIRST htparam WHERE paramnr = 928. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 4 
        htparam.bezeich = "Read Card: get direct result? (VHPIF -> YES)" 
        htparam.flogical = NO. 
END. 
 
/* 18/09/2005 Group 99 License  */ 
 
FIND FIRST htparam WHERE paramnr = 1114. 
DO: 
    IF htparam.bezeich NE "License for CLUB Software" THEN 
    ASSIGN 
        htparam.feldtyp = 4 
        htparam.bezeich = "License for CLUB Software" 
        htparam.flogical = NO 
        htparam.fchar    = ""
    . 
END. 
 
FIND FIRST htparam WHERE paramnr = 223. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 4 
        htparam.bezeich = "License for Membership Card" 
        htparam.flogical = NO
        htparam.fchar    = "". 

END. 
 
/* 14/09/2005 Group 19 FOR VAT Name  */ 
 
FIND FIRST htparam WHERE paramnr = 872. 
IF htparam.feldtyp NE 5 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 5 
        htparam.bezeich = "Description for VAT on the POS Bill" 
        htparam.fchar = "". 
END. 
 
/* 31/08/2005 Group 38 G/L Htparam  */ 
 
FIND FIRST htparam WHERE paramnr = 395. 
IF htparam.paramgr NE 38 THEN 
DO: 
    ASSIGN 
        htparam.paramgr = 38 
        htparam.feldtyp = 5 
        htparam.bezeich = "G/L AcctNo for A/P Others (Optional)" 
        htparam.reihenfolge = 26 
        htparam.fchar = "" 
    . 
END. 
 
/* 28/08/2005 Group 19 FOR Waiter Transfer  */ 
 
FIND FIRST htparam WHERE paramnr = 1079. 
IF htparam.paramgr NE 19 THEN 
DO: 
    ASSIGN 
        htparam.paramgr = 19 
        htparam.feldtyp = 4 
        htparam.bezeich = "Waiter transfer: Ask waiter passwd? (DEF NO)" 
        htparam.reihenfolge = 424 
        htparam.flogical = NO. 
END. 
 
/* 25/08/2005 Group 6 FOR Registration NO AND bill parser */ 
 
FIND FIRST htparam WHERE paramnr = 799. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 4 
        htparam.bezeich = "RegNo for C/I guests? (DEF NO, bill.rechnr2)" 
        htparam.flogical = NO. 
END. 
 
FIND FIRST htparam WHERE paramnr = 1077. 
IF htparam.feldtyp NE 5 THEN 
DO: 
    ASSIGN 
        htparam.paramgr = 17 
        htparam.feldtyp = 5 
        htparam.reihenfolge = 2318 
        htparam.bezeich = "Inhouse Guest Registration No (Param 799)" 
        htparam.fchar = "RegNo". 
END. 
 
FIND FIRST htparam WHERE paramnr = 1078. 
IF htparam.feldtyp NE 5 THEN 
DO: 
    ASSIGN 
        htparam.paramgr = 17 
        htparam.feldtyp = 5 
        htparam.reihenfolge = 2319 
        htparam.bezeich = "RmRate Discount (%) to publish rate" 
        htparam.fchar = "RateDisc". 
END. 
 
/* 21/08/2005 Group 19 */ 
FIND FIRST htparam WHERE paramnr = 857. 
htparam.bezeich = "Print Discount AFTER sales items?". 
 
 
/* 17/06/2005 Grou[ 7 */ 
FIND FIRST htparam WHERE paramnr = 152. 
htparam.bezeich = "Local Currency Code (Short Form)". 
 
/* 22/05/2005 Group 17 FOR Bill Parser  */ 
 
FIND FIRST htparam WHERE paramnr = 1063. 
IF htparam.paramgr NE 17 THEN 
DO: 
    ASSIGN 
        htparam.paramgr = 17 
        htparam.feldtyp = 5 
        htparam.bezeich = "Print Bill: Skip to Line (e.g. $ROW50)" 
        htparam.reihenfolge = 2317 
        htparam.fchar = "ROW". 
END. 
 
/* 08/05/2005 Group 6 FOR China */ 
 
FIND FIRST htparam WHERE paramnr = 936. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 4 
        htparam.bezeich = "Is Deposit mandatory in the reservation?" 
        htparam.flogical = NO. 
END. 
 
FIND FIRST htparam WHERE paramnr = 937. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 4 
        htparam.bezeich = "Read Birthdate from the Guest ID?" 
        htparam.flogical = NO. 
END. 
 
FIND FIRST htparam WHERE paramnr = 970. 
IF htparam.feldtyp NE 1 THEN 
DO: 
    ASSIGN 
        htparam.feldtyp = 1 
        htparam.bezeich = "Max Hours for Day-Use w/o Disc-Rate Control" 
        htparam.finteger = 3.  /* default */ 
END. 
 
/* 20/02/2005 Group 17 */ 
FIND FIRST htparam WHERE paramnr = 2311. 
htparam.bezeich = "Current Time". 
 
FIND FIRST htparam WHERE paramnr = 2312. 
htparam.bezeich = "Current User ID". 
 
FIND FIRST htparam WHERE paramnr = 1117. 
ASSIGN 
  htparam.bezeich = "Bill-line User ID" 
  htparam.feldtyp = 5 
  htparam.fchar = "bl-usrinit". 
 
/* 31/01/2005 Group 38: G/L FOR condotel */ 
FIND FIRST htparam WHERE paramnr = 967. 
IF htparam.paramgr NE 38 THEN 
ASSIGN 
  htparam.paramgr = 38 
  htparam.bezeich = "Consider Table gl-coa for HOTEL/CONDOTEL P&L?" 
  htparam.feldtyp = 4 
  htparam.reihenfolge = 25 
  htparam.flogical = NO. 
 
/* 24/01/2005 Group 8: Statistics */ 
FIND FIRST htparam WHERE paramnr = 195. 
IF htparam.paramgr NE 8 THEN 
ASSIGN 
  htparam.paramgr = 8 
  htparam.bezeich = "Average Stay (in nights) of Paying Guests" 
  htparam.feldtyp = 5 
  htparam.reihenfolge = 13 
  htparam.fchar = "AVRG-STAY". 
 
FIND FIRST htparam WHERE htparam.paramnr = 318.
ASSIGN htparam.reihenfolge = 99.

FIND FIRST htparam WHERE paramnr = 192. 
IF htparam.paramgr NE 8 THEN 
ASSIGN 
  htparam.paramgr = 8 
  htparam.bezeich = "Total Food Cover of selected department" 
  htparam.feldtyp = 5 
  htparam.reihenfolge = 15 
  htparam.fchar = "F-COVER". 
 
FIND FIRST htparam WHERE paramnr = 197. 
IF htparam.paramgr NE 8 THEN 
ASSIGN 
  htparam.paramgr = 8 
  htparam.bezeich = "Total Beverage Cover of selected department" 
  htparam.feldtyp = 5 
  htparam.reihenfolge = 16 
  htparam.fchar = "B-COVER". 
 
/* 222/01/2005  Group 6 */ 
FIND FIRST htparam WHERE paramnr = 83. 
htparam.bezeich = "Pop up warning when transactions go over limit?". 
 
FIND FIRST htparam WHERE paramnr = 564 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 564. 
    ASSIGN 
      htparam.bezeich = "Default Room Availability SET to after allotment?" 
      htparam.feldtyp = 4 
      htparam.flogical = NO. 
END. 
 
/* 16/01/2005  Group 15 */ 
FIND FIRST htparam WHERE paramnr = 480 NO-LOCK. 
IF htparam.paramgr NE 15 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 480. 
    ASSIGN 
      htparam.paramgr = 15 
      htparam.bezeich = "LetterNo for Advance Bill II (option)" 
      htparam.feldtyp = 1 
      htparam.reihenfolge = 98. 
END. 
 
/* 12/12/04   Group 15 */  
FIND FIRST htparam WHERE paramnr = 419. 
ASSIGN 
  htparam.bezeich = "LetterNo debt list Invoice (Non Stay Guest)" 
  htparam.feldtyp = 1. 
 
FIND FIRST htparam WHERE paramnr = 424. 
ASSIGN 
  htparam.bezeich = "LetterNo for debt list's Invoice" 
  htparam.feldtyp = 1. 
 
/* 03/12/04  Tel Interface */ 
FIND FIRST htparam WHERE paramnr = 321. 
ASSIGN 
  htparam.bezeich = "MaxChar length for Name-Display (def 32)" 
  htparam.feldtyp = 1. 
 
/* 30/11/2004 Group 8: Statistics */ 
FIND FIRST htparam WHERE paramnr = 752. 
ASSIGN 
  htparam.bezeich = "Out-of-Service" 
  htparam.feldtyp = 5 
  htparam.fchar = "OOS". 
 
FIND FIRST htparam WHERE paramnr = 187. 
ASSIGN 
  htparam.bezeich = "Arrivals (Room)" 
  htparam.feldtyp = 5 
  htparam.fchar = "RM-ARR". 
 
FIND FIRST htparam WHERE paramnr = 188. 
ASSIGN 
  htparam.bezeich = "Arrivals (Adults)" 
  htparam.feldtyp = 5 
  htparam.fchar = "PRS-ARR". 
 
FIND FIRST htparam WHERE paramnr = 189. 
ASSIGN 
  htparam.bezeich = "Departures (Room)" 
  htparam.feldtyp = 5 
  htparam.fchar = "RM-DEP". 
 
FIND FIRST htparam WHERE paramnr = 190. 
ASSIGN 
  htparam.bezeich = "Departures (Adults)" 
  htparam.feldtyp = 5 
  htparam.fchar = "PRS-DEP". 
 
FIND FIRST htparam WHERE paramnr = 191. 
ASSIGN 
  htparam.bezeich = "Number of VIP Guests" 
  htparam.feldtyp = 5 
  htparam.fchar = "VIP". 
 
FIND FIRST htparam WHERE paramnr = 193. 
ASSIGN 
  htparam.bezeich = "Reservation Made Today (Rooms)" 
  htparam.feldtyp = 5 
  htparam.fchar = "NEW-RES". 
 
FIND FIRST htparam WHERE paramnr = 194. 
ASSIGN 
  htparam.bezeich = "Cancellation Today (Rooms)" 
  htparam.feldtyp = 5 
  htparam.fchar = "CANC-RES". 
 
FIND FIRST htparam WHERE paramnr = 211. 
ASSIGN 
  htparam.bezeich = "Arrivals Tommorow (Rooms)" 
  htparam.feldtyp = 5 
  htparam.fchar = "RM-ARRTMR". 
 
FIND FIRST htparam WHERE paramnr = 231. 
ASSIGN 
  htparam.bezeich = "Arrival Tomorrows (Adults)" 
  htparam.feldtyp = 5 
  htparam.fchar = "PRS-ARRTMR". 
 
FIND FIRST htparam WHERE paramnr = 750. 
ASSIGN 
  htparam.bezeich = "Departure Tomorrow (Rooms)" 
  htparam.feldtyp = 5 
  htparam.fchar = "RM-DEPTMR". 
 
FIND FIRST htparam WHERE paramnr = 751. 
ASSIGN 
  htparam.bezeich = "Departure Tomorrow (Adults)" 
  htparam.feldtyp = 5 
  htparam.fchar = "PRS-DEPTMR". 
 
FIND FIRST htparam WHERE paramnr = 969. 
ASSIGN 
  htparam.bezeich = "No-Show Rooms" 
  htparam.feldtyp = 5 
  htparam.fchar = "NOSHOW". 
 
FIND FIRST htparam WHERE paramnr = 742 NO-LOCK. 
IF htparam.paramgr NE 8 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 742. 
  ASSIGN 
    htparam.paramgr = 8 
    htparam.reihenfolge = 178 
    htparam.bezeich = "Early Checkout (Rooms)" 
    htparam.feldtyp = 5 
    htparam.fchar = "EARLY-CO". 
END. 
 
/* 22/11/2004 Parameters FOR Group 19 */ 
FIND FIRST htparam WHERE paramnr = 570. 
ASSIGN 
  htparam.bezeich = "Minibar Department No (needed by PABX IF)" 
  htparam.feldtyp = 1. 
 
 
/* 24/10/2004 Parameters FOR Apartments */ 
 
FIND FIRST htparam WHERE paramnr = 724. 
ASSIGN 
  htparam.bezeich = "Auto Update Billing Date when signing on?" 
  htparam.paramgr = 24 
  htparam.feldtyp = 4 
  htparam.reihenfolge = 10. 
 
FIND FIRST htparam WHERE paramnr = 904. 
ASSIGN 
  htparam.bezeich = "Default C/L payment ArtNo" 
  htparam.paramgr = 24 
  htparam.feldtyp = 1. 
 
FIND FIRST htparam WHERE paramnr = 17. 
ASSIGN 
  htparam.bezeich = "Service Charge Unit Fee" 
  htparam.paramgr = 24 
  htparam.feldtyp = 2. 
 
FIND FIRST htparam WHERE paramnr = 18. 
ASSIGN 
  htparam.bezeich = "Sinking Fund Unit Fee" 
  htparam.paramgr = 24 
  htparam.feldtyp = 2. 
 
FIND FIRST htparam WHERE paramnr = 500. 
htparam.bezeich = "LetterNo Invoicing - ServiceCharge". 
htparam.feldtyp = 1. 
 
FIND FIRST htparam WHERE paramnr = 613. 
ASSIGN 
  htparam.bezeich = "LetterNo Invoicing - Water & Electricity" 
  htparam.paramgr = 24 
  htparam.feldtyp = 1 
  htparam.reihenfolge = 2. 
 
FIND FIRST htparam WHERE paramnr = 981. 
htparam.bezeich = "License for Condominium". 
 
FIND FIRST paramtext WHERE txtnr = 147. 
paramtext.ptext = "Condominium Admin". 
 
FIND FIRST htparam WHERE paramnr = 796 NO-LOCK. 
IF htparam.feldtyp NE 5 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 500. 
    htparam.bezeich = "Not used". 
 
    FIND FIRST htparam WHERE paramnr = 796. 
    ASSIGN 
        htparam.paramgr = 24 
        htparam.bezeich = "Label for Tenant Card Type" 
        htparam.feldtyp = 5. 
    FIND FIRST htparam WHERE paramnr = 797. 
    ASSIGN 
        htparam.paramgr = 24 
        htparam.bezeich = "Label for Company Card Type" 
        htparam.feldtyp = 5. 
    FIND FIRST htparam WHERE paramnr = 798. 
    ASSIGN 
        htparam.paramgr = 24 
        htparam.bezeich = "Label for Owner Card Type" 
        htparam.feldtyp = 5. 
    FIND FIRST htparam WHERE paramnr = 934. 
    ASSIGN 
        htparam.paramgr = 24 
        htparam.bezeich = "F/O Article No for Service Charge" 
        htparam.feldtyp = 1. 
    FIND FIRST htparam WHERE paramnr = 935. 
    ASSIGN 
        htparam.paramgr = 24 
        htparam.bezeich = "F/O Article No for Sinking Fund" 
        htparam.feldtyp = 1. 
 
END. 
 
FIND FIRST htparam WHERE paramnr = 17. 
ASSIGN 
  htparam.bezeich = "Service Charge Unit Fee" 
  htparam.paramgr = 24 
  htparam.feldtyp = 2. 
 
FIND FIRST htparam WHERE paramnr = 18. 
ASSIGN 
  htparam.bezeich = "Sinking Fund Unit Fee" 
  htparam.paramgr = 24 
  htparam.feldtyp = 2. 

FIND FIRST htparam WHERE paramnr = 17. 
IF htparam.feldtyp NE 5 THEN
ASSIGN 
  htparam.bezeich = "ServCharge Unit Fee by AptType(xx;yy;.;)" 
  htparam.feldtyp = 5
.  
FIND FIRST htparam WHERE paramnr = 18. 
IF htparam.feldtyp NE 5 THEN
ASSIGN 
  htparam.bezeich = "Sinking Fund Unit Fee by AptType(xx;yy;.;)". 
  htparam.feldtyp = 5
. 
 
/* 23/10/2004 Group 13 */ 
FIND FIRST htparam WHERE paramnr = 728. 
htparam.bezeich = "Name Display: Send Sharer Name to PABX?". 
 
 
/* 10/10/2004 Group 15 */ 
FIND FIRST htparam WHERE paramnr = 417. 
htparam.bezeich = "ProgPath of LnL *.lst files (def. \vhp\LnL\)". 
 
FIND FIRST htparam WHERE paramnr = 242. 
htparam.bezeich = "Subgroup No for F/O Paid-Out Billing Article". 
 
/* 17/09/2004 Group 14 */ 
FIND FIRST htparam WHERE paramnr = 320 NO-LOCK.
IF AVAILABLE htparam THEN DO:
    IF htparam.bezeich = "Not used" OR htparam.paramgr NE 14 THEN 
    DO:
      /*Eko 29 Mar 2016 Fix Deadlock Locking record*/
      FIND CURRENT htparam EXCLUSIVE-LOCK. 
      ASSIGN 
        htparam.paramgr = 14 
        htparam.bezeich = "Block new reservation when A/R Over CrLimit?" 
        htparam.flogical = NO. 
      FIND CURRENT htparam NO-LOCK. 
      RELEASE htparam.
    END. 
END.
 
    /* 25/06/2004 Group 13 */ 
FIND FIRST htparam WHERE paramnr = 333. 
ASSIGN 
  htparam.bezeich = "PDA MC Reader Start Char Position (Param 336)" 
  htparam.feldtyp = 1. 
 
FIND FIRST htparam WHERE paramnr = 334. 
ASSIGN 
  htparam.bezeich = "PDA MC Reader End Char Position (Param 336)" 
  htparam.feldtyp = 1. 
 
 
/* 12/06/2004 Param Group 19 */ 
 
FIND FIRST htparam WHERE paramnr = 376. 
ASSIGN htparam.bezeich = "Print Net&VAT amt for CASH & CC payment?". 
 
FIND FIRST htparam WHERE paramnr = 829. 
ASSIGN 
  htparam.bezeich = "Word Program Name for Param 825" 
  htparam.feldtyp = 5. 
 
FIND FIRST htparam WHERE paramnr = 825. 
ASSIGN htparam.bezeich = "Print Total POS bill amount in Word?". 
 
FIND FIRST htparam WHERE paramnr = 824. 
ASSIGN htparam.bezeich = "Exclude Tax&Service for Compliment Payment?". 
 
/* 10/06/2004 Param Group 13 */ 
FIND FIRST htparam WHERE paramnr = 314. 
ASSIGN htparam.bezeich = "PAUSE in SEC for ifstart.r (min=2 max=10)". 
 
FIND FIRST htparam WHERE paramnr = 323. 
ASSIGN htparam.bezeich = "Check duplicate calls record in ifstart.r?". 
 
FIND FIRST htparam WHERE paramnr = 312 NO-LOCK. 
IF htparam.feldtyp NE 1 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 312. 
  ASSIGN 
    htparam.bezeich = "Debugging Mode for ifstart.r (0 = No Debug)" 
    htparam.feldtyp = 1. 
END. 
 
/* 29/05/2004 Param Group 8 */ 
FIND FIRST htparam WHERE paramnr = 186 NO-LOCK. 
IF htparam.feldtyp NE 3 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 186. 
  ASSIGN 
    htparam.bezeich = "Hotel Opening (= statistic starting) Date" 
    htparam.fdate = ? 
    htparam.feldtyp = 3. 
END. 
 
/* 23/05/2004 Param Group 3 */ 
FIND FIRST htparam WHERE paramnr = 236. 
ASSIGN 
  htparam.bezeich = "N/A allowed with opened restaurant bill(s)?". 
 
/* 16/05/2004 Param Group 6 */ 
FIND FIRST htparam WHERE paramnr = 1076 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 1076. 
  ASSIGN 
    htparam.bezeich = "Control C/O time when Checking out the guest?" 
    htparam.flogical = NO. 
    htparam.feldtyp = 4. 
END. 
 
/* 29/04/2004 Param Group 17 */ 
FIND FIRST htparam WHERE paramnr = 373. 
htparam.bezeich = "Change 6PM-Rsv Status to No-Show after 6PM?". 
 
/* 26/04/2004 Param Group 17 */ 
FIND FIRST htparam WHERE paramnr = 1589. 
ASSIGN 
  htparam.paramgr = 17 
  htparam.reihenfolge = 156 
  htparam.bezeich = "Bill-line Voucher" 
  htparam.fchar = "bl-voucher" 
  htparam.feldtyp = 5. 
 
/* 10/04/2004 Param Group 6: 
*/ 
FIND FIRST htparam WHERE paramnr = 244. 
IF htparam.feldtyp NE 5 THEN 
DO: 
  ASSIGN 
    htparam.bezeich = "External Main Program Filename (CNTRL-P)" 
    htparam.feldtyp = 5. 
END. 
 
 
/* 05/04/2004 Param Group 17: */ 
DO: 
  FIND FIRST htparam WHERE paramnr = 1103. 
  ASSIGN 
    htparam.bezeich = "Bill-Line arrival date" 
    htparam.paramgr = 17 
    htparam.reihenfolge = 2315 
    htparam.fchar = "bl-arrive" 
    htparam.feldtyp = 5. 
  FIND FIRST htparam WHERE paramnr = 1104. 
  ASSIGN 
    htparam.bezeich = "Bill-line departure date" 
    htparam.paramgr = 17 
    htparam.reihenfolge = 2316 
    htparam.fchar = "bl-depart" 
    htparam.feldtyp = 5. 
END. 
 
 
/* 19/03/2004 Param Group 9: 
*/ 
FIND FIRST htparam WHERE paramnr = 1083. 
IF htparam.bezeich NE "Store Duration for FB Compliment" THEN 
DO: 
  ASSIGN 
    htparam.bezeich = "Store Duration for FB Compliment" 
    htparam.finteger = 180. 
END. 
 
/* 18/03/2004 Param Group 8: 
*/ 
FIND FIRST htparam WHERE paramnr = 814. 
htparam.bezeich = "No of Persons for selected Segment". 
 
FIND FIRST htparam WHERE paramnr = 753. 
ASSIGN 
  htparam.bezeich = "Number of ADULT guest" 
  htparam.fchar = "NUMADULT" 
  htparam.feldtyp = 5. 
 
FIND FIRST htparam WHERE paramnr = 754. 
ASSIGN 
  htparam.bezeich = "Number of CHILD1 guest" 
  htparam.fchar = "NUMCHLD1" 
  htparam.feldtyp = 5. 
 
FIND FIRST htparam WHERE paramnr = 755. 
ASSIGN 
  htparam.bezeich = "Number of CHILD2 guest" 
  htparam.fchar = "NUMCHLD2" 
  htparam.feldtyp = 5. 
 
FIND FIRST htparam WHERE paramnr = 756. 
ASSIGN 
  htparam.bezeich = "No of Adults for selected Segment" 
  htparam.fchar = "SEGADULT" 
  htparam.feldtyp = 5. 
 
FIND FIRST htparam WHERE paramnr = 757. 
ASSIGN 
  htparam.bezeich = "No of Child1 for selected Segment" 
  htparam.fchar = "SEGMCH1" 
  htparam.feldtyp = 5. 
 
FIND FIRST htparam WHERE paramnr = 758. 
ASSIGN 
  htparam.bezeich = "No of Child2 for selected Segment" 
  htparam.fchar = "SEGMCH2" 
  htparam.feldtyp = 5. 
 
 
/* 16/03/2004 Param Group 9: PARAMETER TO store nitestore optionally. 
*/ 
FIND FIRST htparam WHERE paramnr = 230 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 230. 
  ASSIGN 
    htparam.bezeich = "Should the system store N/A daily outputs?" 
    htparam.feldtyp = 4 
    htparam.flogical = NO. 
  FIND FIRST htparam WHERE paramnr = 238. 
  ASSIGN 
    htparam.bezeich = "If 230=YES, Enter store duration (Days)" 
    htparam.feldtyp = 1 
    htparam.finteger = 180. 
END. 
 
/* 21/02/2004 Param Group 15: 
*/ 
FIND FIRST htparam WHERE paramnr = 497. 
htparam.bezeich = "LetterNo for Single Line NS Bill (option)". 
 
/* 15/01/2004 Param Group 17: Keyword FOR Confirmation Letter 
*/ 
FIND FIRST htparam WHERE paramnr = 413 NO-LOCK. 
IF htparam.paramgr NE 17 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 414. 
  ASSIGN 
    htparam.paramgr = 17 
    htparam.bezeich = "Number of Night Stay" 
    htparam.feldtyp = 5 
    htparam.fchar = "Nites" 
    htparam.reihenfolge = 49. 
  FIND FIRST htparam WHERE paramnr = 413. 
  ASSIGN 
    htparam.paramgr = 17 
    htparam.bezeich = "Mobile Number" 
    htparam.feldtyp = 5 
    htparam.fchar = "HP-No" 
    htparam.reihenfolge = 85. 
END. 
 
 
/* 10/01/2004 Param Group 6: control purpose 
*/ 
 
FIND FIRST htparam WHERE htparam.paramnr = 465. 
  htparam.bezeich = "Ask Invoice Counter# when printing the bill?". 
 
FIND FIRST htparam WHERE htparam.paramnr = 432. 
IF htparam.feldtyp NE 1 THEN 
DO: 
  ASSIGN 
    htparam.feldtyp = 1 
    htparam.bezeich = "LetterNo for Printing Hotel Guest Passport". 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 219. 
DO: 
  htparam.bezeich = "Closed Bill: Enable to change billing date?". 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 1086. 
IF htparam.bezeich = "Not Used" THEN 
DO: 
  ASSIGN 
    htparam.bezeich = "Max F/O Unit Price in local currency" 
    htparam.feldtyp = 2. 
END. 
 
/* 08/01/2004 Param Group 15 
  Master Bill Single Line 
*/ 
FIND FIRST htparam WHERE htparam.paramnr = 688. 
htparam.bezeich = "LetterNo for Master Bill Single Line (Option)". 
 
/* 26/11/2003 Param Group 5 
  Rest Non FB Discount ArtNo 
*/ 
FIND FIRST htparam WHERE htparam.paramnr = 556. 
  htparam.bezeich = "Rest. ArtNo for other type of Discount". 
 
 
/* 24/11/2003 Param Group 6 
  Extension xx FOR mk-gcfxx. AND chg-gcfxx.p TO provide individual guest file 
  layout 
*/ 
FIND FIRST htparam WHERE htparam.paramnr = 148. 
IF htparam.feldtyp NE 5 THEN 
DO: 
  ASSIGN 
    htparam.feldtyp = 5 
    htparam.bezeich = "ExtChar xx for mk-gcfxx.p and chg-gcfxx.p". 
END. 
 
/*** 21/10/2003 PARAMETER Group 10: Password  ***/ 
 
  FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
  IF TRIM(htparam.bezeich) = "" THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 141. 
    htparam.bezeich = "C/L Payment when no Credit Facility yet". 
  END. 
 
/*** 20/10/2003 PARAMETER Group 8, LAST Year Today ***/ 
 
  FIND FIRST htparam WHERE paramnr = 185 NO-LOCK. 
  IF htparam.bezeich = "Not Used" THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 185. 
    ASSIGN 
      htparam.fchar = ".LYTODAY" 
      htparam.bezeich = "Last Year TODAY Value". 
  END. 
 
/*** 24/08/2003 PARAMETER Group 15, 2nd LetterNo FOR MasterBill ***/ 
 
  FIND FIRST htparam WHERE paramnr = 415 NO-LOCK. 
  IF htparam.feldtyp NE 1 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 415. 
    ASSIGN 
      htparam.reihenfolge = 125 
      htparam.bezeich = "2nd LetterNo for Master Bill" 
      htparam.feldtyp = 1 
      htparam.finteger = 0. 
    FIND FIRST htparam WHERE htparam.paramnr = 416. 
    ASSIGN 
      htparam.reihenfolge = 21 
      htparam.bezeich = "Word Prog for foreign amt balance (Param 415)" 
      htparam.feldtyp = 5 
      htparam.fchar = "". 
  END. 
 
/*** 24/08/2003 PARAMETER Group 6, Creditlimit ***/ 
  FIND FIRST htparam WHERE paramnr = 68 NO-LOCK. 
  IF htparam.feldtyp NE 2 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 68. 
    htparam.fdecimal = htparam.finteger. 
    htparam.feldtyp = 2. 
  END. 
 
/*** 12/07/2003 PARAMETER Group 5, Special VHP Articles ***/ 
  FIND FIRST htparam WHERE paramnr = 1001. 
  htparam.bezeich = "Rest Article for the VOUCHER". 
 
/*** 12/07/2003 PARAMETER Group 38 ***/ 
  FIND FIRST htparam WHERE paramnr = 1201 NO-LOCK. 
  IF htparam.paramgruppe NE 38 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 1201. 
    ASSIGN 
      htparam.paramgruppe = 38 
      htparam.bezeich = "G/L AcctNo for WIP (Stock Transform)" 
      htparam.feldtyp = 5 
      htparam.reihenfolge = 24 
      htparam.fchar = "". 
  END. 
 
/*** 07/08/2003 PARAMETER Group 21 ***/ 
  FIND FIRST htparam WHERE paramnr = 43 NO-LOCK. 
  IF htparam.paramgruppe NE 21 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 43. 
    ASSIGN 
      htparam.paramgruppe = 21 
      htparam.bezeich = "Receiving and Outgoing: SHOW UNIT PRICE?" 
      htparam.feldtyp = 4 
      htparam.reihenfolge = 7 
      htparam.finteger = 0. 
  END. 

/* ITA 24/10/16 Group 5  */
FIND FIRST htparam WHERE paramnr = 138 NO-LOCK NO-ERROR.
IF htparam.bezeich = "Not Used" THEN DO:
FIND FIRST htparam WHERE htparam.paramnr = 138.
ASSIGN htparam.bezeich = "ArtNo with Cash Receipt Printout [A1;A2;....]".
IF htparam.feldtyp NE 5 THEN
ASSIGN
   htparam.feldtyp = 5
   htparam.fchar   = "".
END.


FIND FIRST htparam WHERE paramnr = 127 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN htparam.bezeich = "V.A.T. included in Room Rate ?".
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE paramnr = 128 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN htparam.bezeich = "Service included in Room Rate ?".
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE paramnr = 479 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN htparam.bezeich = "Article's Service charge is VAT chargeable".
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE paramnr = 483 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 483.
    ASSIGN
      htparam.paramgr     = 7
      htparam.feldtyp     = 4
      htparam.bezeich     = "Article's tax is VAT chargeable"
      htparam.flogical    = NO.
END.

FIND FIRST htparam WHERE htparam.paramnr = 740 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 740.
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 419
        htparam.feldtyp     = 5
        htparam.bezeich     = "User(s) Journal Voucher Approval by System (01;xx;99)"
        htparam.fchar       = ""
      .
END.

/* 21/01/18 send budget to BI*/
FIND FIRST htparam WHERE htparam.paramnr = 1378 NO-LOCK.
IF htparam.paramgr NE 38 THEN DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 38
        htparam.bezeich     = "Statistic Budget Articles(<Keyword>-<Department>-<ArticleNr>;xxxx;)"
        htparam.feldtyp     = 5
        htparam.fchar       = ""
        htparam.reihenfolge = 34.
END.

/* 08/02/2018 transfer BI to HO*/
FIND FIRST htparam WHERE htparam.paramnr = 1343 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 38
        htparam.bezeich     = "Transfer BI to Head Office IP:Port"
        htparam.feldtyp     = 5
        htparam.finteger    = 0
        htparam.fchar       = ""
        htparam.reihenfolge = 35
    .
END.

/*ITA 140318 --> add validation if room charge active*/ 
FIND FIRST htparam WHERE htparam.paramnr = 259 NO-LOCK.
IF htparam.feldtyp NE 4 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 259.
    ASSIGN
      htparam.paramgr     = 10
      htparam.feldtyp     = 5
      htparam.bezeich     = "Password For Posting Room Charge"
      htparam.flogical    = NO
    .
END.

/* ITA 250318 --> parameter for artikel deposit, refund, void */
FIND FIRST htparam WHERE htparam.paramnr = 676 NO-LOCK.
IF htparam.paramgr NE 6 THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
      htparam.paramgr     = 6
      htparam.reihenfolge = 84
      htparam.feldtyp     = 5
      htparam.bezeich     = "Parameter for Print Deposit, Refund, Void [D=1,2,;...]"
      htparam.flogical    = NO.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 260418 --> parameter for changed Room Rate in Fixed rate*/
FIND FIRST htparam WHERE htparam.paramnr = 494 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 494.
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 98
        htparam.feldtyp     = 4
        htparam.bezeich     = "Automatically changing the room rate in the FixedRate screen"
        htparam.flogical    = NO.
END.

/*ITA 260418 --> parameter for Automatically deleting Fixed Rate*/
FIND FIRST htparam WHERE htparam.paramnr = 493 NO-LOCK.
IF htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE paramnr = 493.
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 97
        htparam.feldtyp     = 4
        htparam.bezeich     = "Automatically deleting the fixed rate"
        htparam.flogical    = NO.
END.

/* ITA 040518 --> parameter for room rate based on Room Category*/
FIND FIRST htparam WHERE htparam.paramnr = 459 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
      htparam.paramgr     = 27
      htparam.reihenfolge = 26
      htparam.feldtyp     = 4
      htparam.bezeich     = "The room rate is calculated based on room category"
      htparam.flogical    = NO.
    FIND CURRENT htparam NO-LOCK.
END.

/* Wen 09/07/18 Group 10 Password for creating supplier */
FIND FIRST htparam WHERE paramnr = 792.
IF htparam.paramgr NE 38 THEN
DO:
    ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password for Creating Supplier"
    htparam.paramgr     = 10.

END.


/* ITA 040518 --> parameter for CSR Donation Tauzia*/
FIND FIRST htparam WHERE htparam.paramnr = 396 NO-LOCK.
FIND CURRENT htparam EXCLUSIVE-LOCK.
ASSIGN
  htparam.paramgr     = 7
  htparam.reihenfolge = 24
  htparam.feldtyp     = 1
  htparam.bezeich     = "Article for CSR Donation (Tauzia Property's)".
FIND CURRENT htparam NO-LOCK.

/*IT 090818 --> parameter for calculate how many times a repeater guest */
FIND FIRST htparam WHERE htparam.paramnr = 458  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "Minimum Stay For Repeater Guest"
        htparam.reihenfolge = 403.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/* Wen 09/07/18 Group 10 Password for creating supplier */
FIND FIRST htparam WHERE paramnr = 792.
IF htparam.paramgr NE 38 THEN
DO:
    ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password for Creating Supplier"
    htparam.paramgr     = 10.

END.

/* Wen 09/08/18 Group 10 Access Right to release P/O (2 or 3, def = 2) */
FIND FIRST htparam WHERE htparam.paramnr = 235 NO-LOCK.
IF htparam.bezeich = "not used" OR htparam.bezeich = "" THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich     = "Access Right to release P/O (2 or 3, def = 2)"
        htparam.paramgr     = 21
        htparam.feldtyp     = 1
        htparam.reihenfolge = 8
        htparam.finteger    = 2 
    .
    FIND CURRENT htparam NO-LOCK.
END.

/* Wen 09/08/18 Group 10 Access Right to Approve DML (2 or 3, def = 2) */
FIND FIRST htparam WHERE htparam.paramnr = 243 NO-LOCK.
IF htparam.bezeich = "not used" OR htparam.bezeich = "" THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich     = "Access Right to Approve DML (2 or 3, def = 2)"
        htparam.paramgr     = 21
        htparam.feldtyp     = 1
        htparam.reihenfolge = 9
        htparam.finteger    = 2 
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*IT 270818 --> parameter for villa setup */
FIND FIRST htparam WHERE htparam.paramnr = 473  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.feldtyp     = 4
        htparam.bezeich     = "Activate For Villa Setup"
        htparam.reihenfolge = 406.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


/*101018*/
FIND FIRST htparam WHERE htparam.paramnr = 451  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 5
        htparam.bezeich     = "Restaurant Articles for SC Discount [eg n1;n2;n3]"
        htparam.reihenfolge = 73
        htparam.fchar       = " ".
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 452  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 5
        htparam.bezeich     = "Rest. for VAT, SC and Other Taxes [eg n1;n2;n3]"
        htparam.reihenfolge = 74
        htparam.fchar       = " ".
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 461  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 5
        htparam.bezeich     = "Billing Articles for SC Discount [eg n1;n2;n3]"
        htparam.reihenfolge = 72
        htparam.fchar       = " ".
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 462  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 2
        htparam.bezeich     = "Discount in % for SC Discount"
        htparam.reihenfolge = 75
        htparam.fdecimal    = 0.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*IT 021018 --> parameter for saving data tamu if use GDPR*/
FIND FIRST htparam WHERE htparam.paramnr = 466  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "Keep Guest Profile (if using GDPR = xxx days)"
        htparam.reihenfolge = 396.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*IT 121118 --> parameter for GDPR all guest*/
FIND FIRST htparam WHERE paramnr = 346 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 6 AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 4
        htparam.bezeich     = "Activated GDPR Rules"
        htparam.reihenfolge = 86
        htparam.flogical    = NO.

    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*IT 211118 --> parameter using of ISO*/
FIND FIRST htparam WHERE htparam.paramnr = 1345 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "No. of ISO nationality code"
        htparam.reihenfolge = 2324.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


/* IF 08/03/19 Group 07 Parameter for Dummy OTA (gastnr) - Faisal */
FIND FIRST htparam WHERE htparam.paramnr = 615 NO-LOCK.
IF htparam.bezeich = "not used" AND htparam.reihenfolge EQ 417 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.bezeich     = "Dummy Guest Card for OTA"
        htparam.paramgr     = 7
        htparam.feldtyp     = 5
        htparam.reihenfolge = 417
        htparam.fchar       = "1" 
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*IT 08/05/19 --> parameter for Banquet Ratecode*/
FIND FIRST htparam WHERE paramnr = 1020 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 23 AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 23
        htparam.feldtyp     = 5
        htparam.bezeich     = "Ratecode Room For Reservation Banquet"
        htparam.reihenfolge = 29
        htparam.flogical    = NO.

    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


/* IT 140519 -> license for dashboard mobile */
FIND FIRST htparam WHERE htparam.paramnr = 1073 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License FOR Dashboard Mobile"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 1077
    .
END.

/* IT 140519 -> license for mobile Apps*/
FIND FIRST htparam WHERE htparam.paramnr = 1055 NO-LOCK.
IF htparam.paramgr NE 99 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License FOR Mobile CI/CO"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 1078
    .
END.


/* IT 270519 -> Parameter for Split Item */
FIND FIRST htparam WHERE htparam.paramnr = 344 NO-LOCK.
IF htparam.paramgr NE 7 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Article number can not be split item (99;xx;)" 
        htparam.feldtyp     = 5
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 2325
    .
END.

/* IT 020819 -> Parameter Calculating ratecode based on occupancy */
FIND FIRST htparam WHERE htparam.paramnr = 486 NO-LOCK.
IF htparam.paramgr NE 27 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 27
        htparam.bezeich     = "Calculating ratecode based on occupancy" 
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = " "
        htparam.reihenfolge = 27
    .
END.

/* IT 020819 -> Parameter date format for web*/
FIND FIRST htparam WHERE htparam.paramnr = 467 NO-LOCK.
IF AVAILABLE htparam THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Date format for web version" 
        htparam.feldtyp     = 5
        htparam.flogical    = NO
        htparam.fchar       = " "
        htparam.reihenfolge = 2326
    .
END.


/* IT 241219 -> Parameter for DML approve*/
FIND FIRST htparam WHERE htparam.paramnr = 390 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 21 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Automatically to approve DML"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = " "
        htparam.reihenfolge = 74.
END.

/* IT 241219 -> Parameter for blocking budget*/
FIND FIRST htparam WHERE htparam.paramnr = 370 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 21 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Automatically to blocking budget"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = " "
        htparam.reihenfolge = 75.
END.


/* IT 160120 -> Parameter for print subgrp*/
FIND FIRST htparam WHERE htparam.paramnr = 450 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 19 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Show Subgroup in Kitchen Printer"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = " "
        htparam.reihenfolge = 429.
END.

/*IT 160620 -> user(s) who can be attached contract rate to guest*/
FIND FIRST htparam WHERE htparam.paramnr = 747.
IF htparam.bezeich = "not used" THEN
DO:
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 2327
        htparam.feldtyp     = 5
        htparam.bezeich     = "User(s) can be attached contract rate (01;xx;99)"
        htparam.fchar       = ""
      .
END.

/*IT 160620 -> user(s) who can be modify rate code*/
FIND FIRST htparam WHERE htparam.paramnr = 598.
IF htparam.bezeich = "not used" THEN
DO:
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 2328
        htparam.feldtyp     = 5
        htparam.bezeich     = "User(s) can be modify rate code (01;xx;99)"
        htparam.fchar       = ""
      .
END.

/*IT 160620 -> show pickup service for Web Precheckin*/
FIND FIRST htparam WHERE htparam.paramnr = 80.
IF htparam.bezeich = "not used" THEN
DO:
    ASSIGN
        htparam.paramgr     = 40
        htparam.reihenfolge = 102
        htparam.feldtyp     = 4
        htparam.bezeich     = "Show Pickup Required to Web Pre-checkin"
        htparam.flogical    = NO
      .
END.


/*IT 160720 -> Deapartement setup for IPTV*/
FIND FIRST htparam WHERE htparam.paramnr = 345.
IF htparam.bezeich = "not used" THEN
DO:
    ASSIGN
        htparam.paramgr     = 13
        htparam.reihenfolge = 39
        htparam.feldtyp     = 5
        htparam.bezeich     = "Departement To Billing Charges - IPTV Interface"
        htparam.fchar       = " "
      .
END.

/*IT 110820 -> Blocking reservasi without ratecode*/
FIND FIRST htparam WHERE htparam.paramnr = 735.
IF htparam.bezeich = "not used" AND htparam.paramgr NE 7 THEN
DO:
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 420
        htparam.feldtyp     = 4
        htparam.bezeich     = "Blocking Resevation Without Ratecode"
        htparam.flogical    = NO
      .
END.


/*IT 100920 -> Converter for AVC*/
FIND FIRST htparam WHERE htparam.paramnr = 360.
IF htparam.bezeich = "not used" AND htparam.paramgr NE 7 THEN
DO:
    ASSIGN
        htparam.paramgr     = 7
        htparam.reihenfolge = 2329
        htparam.feldtyp     = 5
        htparam.bezeich     = "Currency conventer (1;2;xxx;)"
        htparam.fchar       = " "
      .
END.


/*ITA 29Nov2020, MCI License*/
FIND FIRST htparam WHERE htparam.paramnr = 953 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 953.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Self CI Apps" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 1079
        htparam.fchar       = "".
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 29Nov2020, WA License*/
FIND FIRST htparam WHERE htparam.paramnr = 954 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 954.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Broadcast Notification MCI " 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 1080
        htparam.fchar       = "".
    FIND CURRENT htparam NO-LOCK.
END.


/*ITA 29Nov2020, adjustment inventory*/
FIND FIRST htparam WHERE htparam.paramnr = 1021 NO-LOCK.
IF htparam.paramgr NE 21 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1021.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Adjustment Inventory Greather Than Actual Qty ?" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 76.
    FIND CURRENT htparam NO-LOCK.
END.

/*IT 211220 --> parameter for saving marketing subcribe*/
FIND FIRST htparam WHERE htparam.paramnr = 477  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.bezeich     = "Activated Marketing Features ?"
        htparam.reihenfolge = 397.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*IT 01/02/21 --> parameter for VAT admin*/
FIND FIRST htparam WHERE htparam.paramnr = 1344  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 4 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 4
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "V.A.T Code 16"
        htparam.reihenfolge = 22.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1346  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 4 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 4
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "V.A.T Code 17"
        htparam.reihenfolge = 23.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1347  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 4 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 4
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "V.A.T Code 18"
        htparam.reihenfolge = 24.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1348  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 4 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 4
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "V.A.T Code 19"
        htparam.reihenfolge = 25.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1349  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 4 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 4
        htparam.feldtyp     = 1
        htparam.fint        = 0
        htparam.bezeich     = "V.A.T Code 20"
        htparam.reihenfolge = 26.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 90  NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 15 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 15
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.bezeich     = "Date Split Activation For Fixed Rate"
        htparam.reihenfolge = 137.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


FIND FIRST htparam WHERE htparam.paramnr = 1350 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 6 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.bezeich     = "Activated guest search is 100 % same"
        htparam.reihenfolge = 87.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


FIND FIRST htparam WHERE htparam.paramnr = 1351 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 19 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 19
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.bezeich     = "RoomNo must be entered when pay use room transfer"
        htparam.reihenfolge = 430.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1352 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 3 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 3
        htparam.feldtyp     = 1
        htparam.finteger    = 0
        htparam.bezeich     = "Group for Night Audit Program (web version only)"
        htparam.reihenfolge = 21.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1353 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 5 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 1
        htparam.finteger    = 0
        htparam.bezeich     = "Article Number for Deposit (SelfCheckin)"
        htparam.reihenfolge = 76.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1354 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 21 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 21
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.bezeich     = "Receiving is not allowed greather than date of created PO"
        htparam.reihenfolge = 77.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


FIND FIRST htparam WHERE htparam.paramnr = 1355 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used"
    AND htparam.paramgr NE 3 THEN DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 3
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.bezeich     = "Activated system date using server date"
        htparam.reihenfolge = 22.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA 24Nov2021, Self order License*/
FIND FIRST htparam WHERE htparam.paramnr = 1357 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1357.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for VHP Self Order" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1081.
    FIND CURRENT htparam NO-LOCK.
END.


/*ITA 24Nov2021, PreArrival Checkin License*/
FIND FIRST htparam WHERE htparam.paramnr = 1358 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1358.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for VHP PreArrival Checkin" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1082.
    FIND CURRENT htparam NO-LOCK.
END.


/*ITA 24Nov2021, VHP BI License*/
FIND FIRST htparam WHERE htparam.paramnr = 1359 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1359.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for VHP Business Intelligence(BI)" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1083.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 07Dec2021, Change Description*/
FIND FIRST htparam WHERE htparam.paramnr = 1356 NO-LOCK.
IF htparam.paramgr NE 7 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1356.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Description For RefNo Number 2" 
        htparam.fchar       = " "
        htparam.feldtyp     = 5
        htparam.reihenfolge = 2330.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 17Dec2021, */
FIND FIRST htparam WHERE htparam.paramnr = 1342 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1342.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Allow Posting at One Table From Several Waiter(s)" 
        htparam.flogical    = YES
        htparam.feldtyp     = 4
        htparam.reihenfolge = 431.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 25Feb2022*/
FIND FIRST htparam WHERE htparam.paramnr = 1360 NO-LOCK.
IF htparam.paramgr NE 21 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1360.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Is Partial Inventory Closing Allowed?" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 78.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 18 Maret 2022*/
FIND FIRST htparam WHERE htparam.paramnr = 50 NO-LOCK.
IF htparam.paramgr NE 38 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 50.
    ASSIGN
        htparam.paramgr     = 38
        htparam.bezeich     = "G/L AcctNo for Journal A/R (ABI)" 
        htparam.fchar       = " "
        htparam.feldtyp     = 5
        htparam.reihenfolge = 36.
    FIND CURRENT htparam NO-LOCK.
END.


/*ITA 04 April 2022, sorting by subgroup for kitchen Printer*/
FIND FIRST htparam WHERE htparam.paramnr = 147 NO-LOCK.
IF htparam.paramgr NE 19 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 147.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Sort by SubGroup in Kitchen Printer?" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 432.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 04 April 2022, sorting by subgroup for kitchen Printer*/
FIND FIRST htparam WHERE htparam.paramnr = 485 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 485.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "SegmentCode OTA to Room Production Report (OTA;xxx)" 
        htparam.fchar       = " "
        htparam.feldtyp     = 5
        htparam.reihenfolge = 2331
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA 13 June 2022, Actived 4 aprroval PO*/
FIND FIRST htparam WHERE htparam.paramnr = 71 NO-LOCK.
IF htparam.paramgr NE 21 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 71.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Actived 4 Approval for PO" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 79.
    FIND CURRENT htparam NO-LOCK.
END.

/*FD August 29, 2022 => Maximum Time Day Use In ABF List*/
FIND FIRST htparam WHERE htparam.paramnr = 561 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 561.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Maximum Time Day Use In ABF List (05:00)" 
        htparam.fchar       = " "
        htparam.flogical    = NO
        htparam.finteger    = 0
        htparam.feldtyp     = 5     
        htparam.reihenfolge = 2332
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*FD Sept 16, 2022 => Mininmum Balance For Cashless NS Guest Bill*/
FIND FIRST htparam WHERE htparam.paramnr = 586 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 586.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Minimum Balance For Cashless NS Guest Bill"         
        htparam.fdecimal    = 0
        htparam.feldtyp     = 2     
        htparam.reihenfolge = 2333
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*FD Oct 19, 2022*/
FIND FIRST htparam WHERE htparam.paramnr = 1361 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 5 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 5
        htparam.feldtyp     = 1
        htparam.finteger    = 0
        htparam.bezeich     = "Article Number for Deposit (Restaurant)"
        htparam.reihenfolge = 77.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA Oct 25, 2022*/
FIND FIRST htparam WHERE htparam.paramnr = 978 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 6 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 5
        htparam.finteger    = 0
        htparam.bezeich     = "MainGroup to be displayed on the VHP Cloud [eg. D1:1,2,xx;]"
        htparam.reihenfolge = 77.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA Nov 11, 2022*/
FIND FIRST htparam WHERE htparam.paramnr = 583 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 9 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 9
        htparam.feldtyp     = 1
        htparam.finteger    = 0
        htparam.bezeich     = "Store Duration for GuestBook"
        htparam.flogical    = NO
        htparam.reihenfolge = 269.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA Nov 11, 2022*/
FIND FIRST htparam WHERE htparam.paramnr = 588 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 19 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 19
        htparam.feldtyp     = 4
        htparam.finteger    = 0
        htparam.bezeich     = "Activate Restaurant Deposit"
        htparam.flogical    = NO
        htparam.reihenfolge = 433.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA 24Jan2023, Cashless License*/
FIND FIRST htparam WHERE htparam.paramnr = 1022 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1022.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Cashless Payment" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 1084
        htparam.fchar       = " ".
    FIND CURRENT htparam NO-LOCK.
END.

/*FD March 20, 2023 => Nonstay Guest Bill Access*/
FIND FIRST htparam WHERE htparam.paramnr = 589 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 589.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Activate User Access For Nonstay Guest Bill"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = NO
        htparam.reihenfolge = 2334
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*FD May 22, 2023 => Access popup Queuing Room List*/
FIND FIRST htparam WHERE htparam.paramnr = 594 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 594.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Activate Dialog Queuing Room List"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = YES
        htparam.reihenfolge = 2335
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL June 13, 2023 - Group 10*/
FIND FIRST htparam WHERE htparam.paramnr = 174.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "NS Cashless Minimum Balance Post as Revenue"
    .

/*FDL June 16, 2023 - For vhpCloud all modul*/
FIND FIRST htparam WHERE htparam.paramnr = 438 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 15 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 15
        htparam.feldtyp     = 5
        htparam.fchar       = ""
        htparam.bezeich     = "List of Standard Letter No vhpCloud [eg. 1;2;x;x]"
        htparam.reihenfolge = 138.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*FD July 12, 2023 => Access Corporate For CRUD Restaurant Article*/
FIND FIRST htparam WHERE htparam.paramnr = 1204 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1204.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Access for Setup Restaurant Articles"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = NO
        htparam.reihenfolge = 434
    .
    FIND CURRENT htparam NO-LOCK.
END.
ELSE

FIND FIRST htparam WHERE htparam.paramnr = 1204 NO-LOCK.
IF AVAILABLE htparam THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1204.
    htparam.bezeich = "Disable Access for Setup Restaurant Articles".
    FIND CURRENT htparam NO-LOCK.
END.

/*FD August 01, 2023 => Print Kitchen Printer Sorting By Subgroup Priority*/
FIND FIRST htparam WHERE htparam.paramnr = 838 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 19 THEN 
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 838.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Sort by SubGroup Priority in Kitchen Printer?" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 435
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*IT 300823 --> parameter for Region GDPR*/
FIND FIRST htparam WHERE paramnr = 448 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 6 AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 5
        htparam.bezeich     = "Regions complying GDPR rules [eg. 1;2;x;x]"
        htparam.reihenfolge = 88
        htparam.flogical    = NO.

    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


/*IT 300823 --> parameter for Nationality GDPR*/
FIND FIRST htparam WHERE paramnr = 449 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 6 AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 5
        htparam.bezeich     = "Nationality complying GDPR rules [eg. 1;2;x;x]"
        htparam.reihenfolge = 89
        htparam.flogical    = NO.

    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.


/*ITA 13/09/23, Salesboard Interface License*/
FIND FIRST htparam WHERE htparam.paramnr = 1023 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1023.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Salesboard Interface" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.reihenfolge = 1085
        htparam.fchar       = " ".
    FIND CURRENT htparam NO-LOCK.
END.

/*FD Sept 22, 2023 => Access Release OOO*/
FIND FIRST htparam WHERE htparam.paramnr = 585 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 585.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Activate User Access for Release OOO Room"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = NO
        htparam.reihenfolge = 2336
    .
    FIND CURRENT htparam NO-LOCK.
END.


/*ITA 13/10/23, Room Rental Banquet*/
FIND FIRST htparam WHERE htparam.paramnr = 950 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 950.
    ASSIGN
        htparam.paramgr     = 23
        htparam.bezeich     = "Room Rental will be charge after NA"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = NO
        htparam.reihenfolge = 30
    .
    FIND CURRENT htparam NO-LOCK.
END.


/*ITA 13/10/23, */
FIND FIRST htparam WHERE htparam.paramnr = 1362 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1362.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Use Access For Booking Engine Setup"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = NO
        htparam.reihenfolge = 2337
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL Nov 06, 2023 - Group 10*/
FIND FIRST htparam WHERE htparam.paramnr = 175.
ASSIGN 
    htparam.feldtyp     = 5
    htparam.bezeich     = "Password Posting POS VOID Sales Item CloseBill"
    .

/*FDL Nov 16, 2023*/
FIND FIRST htparam WHERE htparam.paramnr = 89 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 89.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Set DML Article For Main Group Material"                              
        htparam.fdecimal    = 0
        htparam.feldtyp     = 4  
        htparam.flogical    = YES
        htparam.reihenfolge = 80
    .
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL Nov 16, 2023 => Local Time Zone for ServerLess*/
FIND FIRST htparam WHERE paramnr = 91 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 6 AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.feldtyp     = 5
        htparam.bezeich     = "Local Time Zone"
        htparam.fchar       = ""
        htparam.reihenfolge = 90
        htparam.flogical    = NO.

    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

FIND FIRST htparam WHERE htparam.paramnr = 282 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 282.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface Channel Manager" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1088.
    FIND CURRENT htparam NO-LOCK.
END.


/*FDL Standarization License Interface - Dec 14, 2023*/
FIND FIRST htparam WHERE htparam.paramnr = 81 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 81.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface Keycard" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1086.
    FIND CURRENT htparam NO-LOCK.
END.


FIND FIRST htparam WHERE htparam.paramnr = 292 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 292.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface Revenue Management" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1089.
    FIND CURRENT htparam NO-LOCK.
END.


FIND FIRST htparam WHERE htparam.paramnr = 294 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 294.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface IPTV" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1091.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 296 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 296.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface Online Tax" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1092.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 298 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 298.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface Guest Concierge" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1093.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 379 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 379.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface Running Text / Totem" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1094.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 389 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 389.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Interface WiFi" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1095.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 420 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 420.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Corporate Financial" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1096.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 421 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 421.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for CRM System" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1097.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 422 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 422.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License for Greeting Email" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1098.
    FIND CURRENT htparam NO-LOCK.
END.
/*End FDL*/


/*ITA: 050124 Penambahan parameter untuk simpan artikel tax tourism dan heritage serta nilai percentnya*/
FIND FIRST htparam WHERE htparam.paramnr = 1027 NO-LOCK.
IF htparam.paramgr NE 5 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1027.
    ASSIGN
        htparam.paramgr     = 5
        htparam.bezeich     = "Active GST for Restaurant" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 81.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1028 NO-LOCK.
IF htparam.paramgr NE 5 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1028.
    ASSIGN
        htparam.paramgr     = 5
        htparam.bezeich     = "SST Percentage" 
        htparam.flogical    = NO
        htparam.feldtyp     = 1
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 78.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1029 NO-LOCK.
IF htparam.paramgr NE 5 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1029.
    ASSIGN
        htparam.paramgr     = 5
        htparam.bezeich     = "Article Number for Tourism Tax" 
        htparam.flogical    = NO
        htparam.feldtyp     = 1
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 79.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1030 NO-LOCK.
IF htparam.paramgr NE 5 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1030.
    ASSIGN
        htparam.paramgr     = 5
        htparam.bezeich     = "Article Number for Heritage Fee" 
        htparam.flogical    = NO
        htparam.feldtyp     = 1
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 80.
    FIND CURRENT htparam NO-LOCK.
END.
/*end*/

FIND FIRST htparam WHERE htparam.paramnr = 1377 NO-LOCK.
IF htparam.paramgr NE 8 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1377.
    ASSIGN
        htparam.paramgr     = 8
        htparam.bezeich     = "Daily Report Export to Google Sheet / Excel" 
        htparam.flogical    = YES
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 185.
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL April 17, 2024 => Lock QTY When Split Item POS*/
FIND FIRST htparam WHERE htparam.paramnr = 436 NO-LOCK.
IF htparam.paramgr NE 19 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 436.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Lock Quantity When Split Item POS?" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 436.
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL May 14, 2024 => Init Access Modify Journal Transaction*/
FIND FIRST htparam WHERE paramnr = 98 NO-LOCK NO-ERROR.
IF htparam.paramgr NE 7 AND htparam.bezeich = "not used" THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 7
        htparam.feldtyp     = 5
        htparam.bezeich     = "Access For Modify Journal Transaction [01;xx;99]"
        htparam.fchar       = ""
        htparam.reihenfolge = 2338
        htparam.flogical    = NO.

    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*FDL June 12, 2024 => Term n Condition Mobile*/
FIND FIRST htparam WHERE htparam.paramnr = 1033 NO-LOCK.
IF htparam.paramgr NE 6 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1033.
    ASSIGN
        htparam.paramgr     = 6
        htparam.bezeich     = "Activate Confirmation For Term and Condition" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 91.
    FIND CURRENT htparam NO-LOCK.
END. 

/*FDL July 18, 2024 => License Kitchen Display System*/
FIND FIRST htparam WHERE htparam.paramnr = 280 NO-LOCK.
IF htparam.paramgr NE 99 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 280.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "Activate Kitchen Display System" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 1099.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA July 18, 2024 => License Leasing Feature*/
FIND FIRST htparam WHERE htparam.paramnr = 1363 NO-LOCK.
IF htparam.paramgr NE 7 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1363.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Activate Leasing Feature" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 421.
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL August 19, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 108 NO-LOCK.
IF htparam.paramgr NE 9 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 108.
    ASSIGN
        htparam.paramgr     = 9
        htparam.bezeich     = "Store Duration For Quotation Attachment" 
        htparam.flogical    = NO
        htparam.feldtyp     = 1
        htparam.fchar       = ""
        htparam.finteger    = 1095
        htparam.reihenfolge = 270.
    FIND CURRENT htparam NO-LOCK.
END.

/*ITA Sept 10, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 1364 NO-LOCK.
IF htparam.paramgr NE 6 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1364.
    ASSIGN
        htparam.paramgr     = 6
        htparam.bezeich     = "Parameter for Calculated DynamicRate Based On Villa/Hotel" 
        htparam.flogical    = NO
        htparam.feldtyp     = 5
        htparam.fchar       = ""
        htparam.finteger    = 1095
        htparam.reihenfolge = 93.
    FIND CURRENT htparam NO-LOCK.
END.

/*FDL Sept 25, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 1068 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 6 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 6
        htparam.bezeich     = "Article Number for Guest Deposit"
        htparam.finteger    = 0
        htparam.feldtyp     = 1
        htparam.flogical    = NO        
        htparam.fchar       = ""        
        htparam.reihenfolge = 92.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*ITA Oct 09, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 1366 NO-LOCK.
IF htparam.paramgr NE 20 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1366.
    ASSIGN
        htparam.paramgr     = 20
        htparam.bezeich     = "Depreciation by Month" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 8.
    FIND CURRENT htparam NO-LOCK.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1367 NO-LOCK.
IF htparam.paramgr NE 20 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1367.
    ASSIGN
        htparam.paramgr     = 20
        htparam.bezeich     = " Fixed Asset Breakdown Access" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 9.
    FIND CURRENT htparam NO-LOCK.
END.
/*end*/

/*ITA Oct 17, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 1368 NO-LOCK.
IF htparam.paramgr NE 20 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1368.
    ASSIGN
        htparam.paramgr     = 20
        htparam.bezeich     = "Main Group Account for Fixed Asset" 
        htparam.flogical    = NO
        htparam.feldtyp     = 5
        htparam.fchar       = ""
        htparam.finteger    = 0
        htparam.reihenfolge = 10.
    FIND CURRENT htparam NO-LOCK.
END.
/*end*/

/*FDL Nov 19, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 178 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich = "not used" AND htparam.paramgr NE 10 THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 10
        htparam.bezeich     = "Password For Payment Compliment POS"
        htparam.finteger    = 0
        htparam.feldtyp     = 5
        htparam.flogical    = NO        
        htparam.fchar       = ""        
        htparam.reihenfolge = 106.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*FDL Nov 26, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 428 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 7 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 428.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Input Reason When Change Status Room (HK)" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 108.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END. 

/*FDL Dec 11, 2024*/
FIND FIRST htparam WHERE htparam.paramnr = 392 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 7 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 392.
    ASSIGN
        htparam.paramgr     = 7
        htparam.bezeich     = "Enable Automation Create Journal Manual AP" 
        htparam.flogical    = YES
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 2339.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END. 

/*ITA Dec 11, 2024 - Leasing Parameter*/
FIND FIRST htparam WHERE htparam.paramnr = 1051 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 5 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1051.
    ASSIGN
        htparam.paramgr     = 5
        htparam.bezeich     = "Article Number For A/R Ledger Leasing" 
        htparam.flogical    = NO
        htparam.feldtyp     = 1
        htparam.fchar       = ""
        htparam.reihenfolge = 82.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END. 


FIND FIRST htparam WHERE htparam.paramnr = 1052 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 5 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1052.
    ASSIGN
        htparam.paramgr     = 5
        htparam.bezeich     = "Article Number For Divered Revenue" 
        htparam.flogical    = NO
        htparam.feldtyp     = 1
        htparam.fchar       = ""
        htparam.reihenfolge = 83.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END. 
/*end*/

/*FDL Jan 16, 2025*/
FIND FIRST htparam WHERE htparam.paramnr = 487 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 21 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 487.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Receiving DML with lower/higher price allowed?" 
        htparam.flogical    = NO
        htparam.feldtyp     = 4
        htparam.fchar       = ""
        htparam.reihenfolge = 81.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END. 

/*FDL Jan 16, 2025*/
FIND FIRST htparam WHERE htparam.paramnr = 488 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.paramgr NE 21 AND htparam.bezeich = "not used" THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 21
        htparam.bezeich     = "Max tolerance in % (Param No 487)"
        htparam.finteger    = 0
        htparam.feldtyp     = 1
        htparam.flogical    = NO        
        htparam.fchar       = ""        
        htparam.reihenfolge = 82.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*FDL March 13, 2025*/
FIND FIRST htparam WHERE htparam.paramnr = 293 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.paramgr NE 20 AND htparam.bezeich = "not used" THEN 
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 20
        htparam.bezeich     = "Activate counter number 6 digit asset number"
        htparam.feldtyp     = 4
        htparam.flogical    = NO        
        htparam.fchar       = ""        
        htparam.reihenfolge = 11.
    .
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*FDL March 20, 2025*/
FIND FIRST htparam WHERE htparam.paramnr = 423 NO-LOCK.
IF AVAILABLE htparam AND htparam.paramgr NE 19 AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 423.
    ASSIGN
        htparam.paramgr     = 19
        htparam.bezeich     = "Parameters For Print Bill POS(Param 874=NO)" 
        htparam.flogical    = NO
        htparam.feldtyp     = 5
        htparam.fchar       = ""
        htparam.reihenfolge = 437.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

/*FDL March 26, 2025*/
FIND FIRST htparam WHERE htparam.paramnr = 1054 NO-LOCK.
IF AVAILABLE htparam AND htparam.bezeich = "not used" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1054.
    ASSIGN
        htparam.paramgr     = 25
        htparam.bezeich     = "Default C/I Time (HH:MM)" 
        htparam.flogical    = NO
        htparam.feldtyp     = 5
        htparam.fchar       = ""
        htparam.reihenfolge = 56.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.
