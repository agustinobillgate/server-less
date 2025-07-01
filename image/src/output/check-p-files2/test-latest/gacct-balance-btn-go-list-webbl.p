
DEFINE TEMP-TABLE gacct-balance-list
    FIELD i-counter AS INTEGER INITIAL 0
    FIELD flag      AS INTEGER INITIAL 0
    FIELD artnr     AS INTEGER
    FIELD dept      AS INTEGER
    FIELD ankunft   AS DATE 
    FIELD ankzeit   AS CHAR 
    FIELD typeBill  AS CHAR FORMAT "x(2)" 
    FIELD billdatum AS DATE
    FIELD guest     AS CHAR FORMAT "x(24)"
    FIELD roomNo    AS CHAR FORMAT "x(4)"
    FIELD billNo    AS INT  FORMAT ">>>>>>>"
    FIELD billnr    AS INTEGER FORMAT "9"
    FIELD bezeich   AS CHAR FORMAT "x(16)"
    FIELD prevBala  AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD debit     AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD credit    AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD balance   AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD depart    AS DATE
    .

DEF TEMP-TABLE bill-alert
    FIELD rechnr AS INTEGER.


DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR bill-alert.
DEF INPUT  PARAMETER heute         AS DATE.
DEF INPUT  PARAMETER billdate      AS DATE.
DEF INPUT  PARAMETER ank-flag      AS LOGICAL.
DEF INPUT  PARAMETER sorttype      AS INT.
DEF INPUT  PARAMETER fact1         AS INT.
DEF INPUT  PARAMETER price-decimal AS INT.
DEF INPUT  PARAMETER short-flag    AS LOGICAL.
DEFINE INPUT PARAMETER idFlag      AS CHAR.
DEF OUTPUT PARAMETER msg-str       AS CHAR.
DEF OUTPUT PARAMETER msg-str2      AS CHAR.


DEFINE VARIABLE i-counter AS CHAR.
DEFINE VARIABLE flag      AS CHAR.
DEFINE VARIABLE artnr     AS CHAR.
DEFINE VARIABLE dept      AS CHAR.
DEFINE VARIABLE ankunft   AS CHAR.
DEFINE VARIABLE ankzeit   AS CHAR.
DEFINE VARIABLE typeBill  AS CHAR.
DEFINE VARIABLE bill-datum AS CHAR.
DEFINE VARIABLE guest     AS CHAR.
DEFINE VARIABLE roomNo    AS CHAR.
DEFINE VARIABLE billNo    AS CHAR.
DEFINE VARIABLE billnr    AS CHAR.
DEFINE VARIABLE bezeich   AS CHAR.
DEFINE VARIABLE prevBala  AS CHAR.
DEFINE VARIABLE debit     AS CHAR.
DEFINE VARIABLE credit    AS CHAR.
DEFINE VARIABLE balance   AS CHAR.
DEFINE VARIABLE depart    AS CHAR.




DEFINE VARIABLE counter AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE str    AS CHAR NO-UNDO.
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE STREAM s1.


DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.
DEFINE BUFFER t-list  FOR gacct-balance-list.


    CREATE queasy.
    ASSIGN queasy.KEY     = 285
           queasy.char1   = "Guest Ledger Report"
           queasy.number1 = 1
           queasy.char2   = idFlag.
    RELEASE queasy.

    FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
        RUN decode-string(paramtext.ptexte, OUTPUT htl-no).

    RUN gacct-balance-btn-go-listbl.p(pvILanguage, INPUT TABLE bill-alert,heute, 
                                      billdate, ank-flag,sorttype, fact1, price-decimal,
                                      short-flag, OUTPUT msg-str, OUTPUT msg-str2, 
                                      OUTPUT TABLE gacct-balance-list).

    FIND FIRST gacct-balance-list NO-ERROR.
     DO WHILE AVAILABLE gacct-balance-list:
        IF gacct-balance-list.ankunft = ? THEN ankunft = "".
        ELSE ankunft = STRING(gacct-balance-list.ankunft).

        IF gacct-balance-list.billdatum = ? THEN bill-datum = "".
        ELSE bill-datum = STRING(gacct-balance-list.billdatum).

        IF gacct-balance-list.depart = ? THEN depart = "".
        ELSE depart = STRING(gacct-balance-list.depart).

        IF gacct-balance-list.guest MATCHES "*|*" THEN guest = REPLACE(gacct-balance-list.guest,"|","&").
        ELSE guest = gacct-balance-list.guest.

        IF gacct-balance-list.bezeich MATCHES "*|*" THEN bezeich = REPLACE(gacct-balance-list.bezeich,"|"," ").
        ELSE bezeich = gacct-balance-list.bezeich.


        CREATE queasy.
        ASSIGN 
               counter = counter + 1
               queasy.KEY   = 280
               queasy.char1 = "Guest Ledger Report"
               queasy.char3 = idFlag
               queasy.char2 = STRING(gacct-balance-list.i-counter) + "|" +  
                              STRING(gacct-balance-list.flag)      + "|" +  
                              STRING(gacct-balance-list.artnr)     + "|" +  
                              STRING(gacct-balance-list.dept)      + "|" +  
                              ankunft                              + "|" +  
                              gacct-balance-list.ankzeit           + "|" +  
                              gacct-balance-list.typeBill          + "|" +  
                              bill-datum                           + "|" +  
                              guest                                + "|" +  
                              gacct-balance-list.roomNo            + "|" +  
                              STRING (gacct-balance-list.billNo)   + "|" +  
                              STRING (gacct-balance-list.billnr)   + "|" +  
                              bezeich                              + "|" +  
                              STRING(gacct-balance-list.prevBala)  + "|" +  
                              STRING(gacct-balance-list.debit)     + "|" +  
                              STRING(gacct-balance-list.credit)    + "|" +  
                              STRING(gacct-balance-list.balance)   + "|" +  
                              depart.            
                     queasy.number1 = INT(counter).
      
      FIND NEXT gacct-balance-list NO-ERROR.
    END.
   
    FIND FIRST bqueasy WHERE bqueasy.KEY = 285
        AND bqueasy.char1 = "Guest Ledger Report"
        AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN DO:
        FIND CURRENT bqueasy EXCLUSIVE-LOCK.
        ASSIGN bqueasy.number1 = 0.
        FIND CURRENT bqueasy NO-LOCK.
        RELEASE bqueasy.
    END.
 
PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END.
   
    
    







