DEFINE TEMP-TABLE gacct-balance-list
    FIELD i-counter AS INTEGER INITIAL 0
    FIELD flag      AS INTEGER INITIAL 0
    FIELD artnr     AS INTEGER
    FIELD dept      AS INTEGER
    FIELD ankunft   AS CHAR 
    FIELD ankzeit   AS CHAR 
    FIELD typeBill  AS CHAR FORMAT "x(2)" 
    FIELD billdatum AS CHAR
    FIELD guest     AS CHAR 
    FIELD roomNo    AS CHAR 
    FIELD billNo    AS INT   
    FIELD billnr    AS INTEGER 
    FIELD bezeich   AS CHAR
    FIELD prevBala  AS DEC  
    FIELD debit     AS DEC  
    FIELD credit    AS DEC  
    FIELD balance   AS DEC  
    FIELD depart    AS CHAR
    .


DEFINE INPUT PARAMETER idFlag AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR gacct-balance-list.

DEFINE VARIABLE counter AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE VARIABLE temp-char AS CHAR NO-UNDO.
DEFINE VARIABLE ankunft AS CHAR.
DEFINE VARIABLE bill-datum AS CHAR.
DEFINE VARIABLE depart AS CHAR.
DEFINE STREAM s1.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.



FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR.
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
DO:
    RUN decode-string(paramtext.ptexte, OUTPUT htl-no).
END.
    

FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "Guest Ledger Report"
    AND queasy.char3 = idFlag NO-LOCK BY queasy.number1:


    ASSIGN counter = counter + 1.
    IF counter GT 1000 THEN LEAVE.
   
    CREATE gacct-balance-list.
    ASSIGN
        gacct-balance-list.i-counter = INTEGER(ENTRY(1, queasy.char2, "|"))
        gacct-balance-list.flag      = INTEGER(ENTRY(2, queasy.char2, "|"))
        gacct-balance-list.artnr     = INTEGER(ENTRY(3, queasy.char2, "|"))
        gacct-balance-list.dept      = INTEGER(ENTRY(4, queasy.char2, "|"))
        gacct-balance-list.ankunft   = ENTRY(5, queasy.char2, "|")
        gacct-balance-list.ankzeit   = ENTRY(6, queasy.char2, "|")
        gacct-balance-list.typeBill  = ENTRY(7, queasy.char2, "|")
        gacct-balance-list.billdatum = ENTRY(8, queasy.char2, "|")
        gacct-balance-list.guest     = ENTRY(9, queasy.char2, "|")
        gacct-balance-list.roomNo    = ENTRY(10, queasy.char2, "|")
        gacct-balance-list.billNo    = INTEGER(ENTRY(11, queasy.char2, "|"))
        gacct-balance-list.billnr    = INTEGER(ENTRY(12, queasy.char2, "|"))
        gacct-balance-list.bezeich   = ENTRY(13, queasy.char2, "|")
        gacct-balance-list.prevBala  = DECIMAL(ENTRY(14, queasy.char2, "|"))
        gacct-balance-list.debit     = DECIMAL(ENTRY(15, queasy.char2, "|"))
        gacct-balance-list.credit    = DECIMAL(ENTRY(16, queasy.char2, "|"))
        gacct-balance-list.balance   = DECIMAL(ENTRY(17, queasy.char2, "|"))
        gacct-balance-list.depart    = ENTRY(18, queasy.char2, "|")
   .
      
   FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
   DELETE bqueasy.
   RELEASE bqueasy.
END. 


FIND FIRST pqueasy WHERE pqueasy.KEY = 280
    AND pqueasy.char1 = "Guest Ledger Report" 
    AND pqueasy.char3 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN 
DO:
    ASSIGN doneFlag = NO.
END.
ELSE 
DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285
        AND tqueasy.char1 = "Guest Ledger Report"
        AND tqueasy.number1 = 1 
        AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN
    DO:
        ASSIGN doneFlag = NO.
    END.
    ELSE 
    DO:
        ASSIGN doneFlag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285
    AND tqueasy.char1 = "Guest Ledger Report"
    AND tqueasy.number1 = 0 
    AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.

IF AVAILABLE tqueasy THEN 
DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
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


