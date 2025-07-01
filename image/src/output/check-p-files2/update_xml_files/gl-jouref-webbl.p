
DEFINE TEMP-TABLE output-list 
    FIELD STR AS CHAR
    FIELD refno AS CHAR. 

DEFINE INPUT PARAMETER idFlag      AS CHAR.
DEFINE INPUT  PARAMETER sorttype   AS INTEGER.
DEFINE INPUT  PARAMETER from-date  AS DATE.
DEFINE INPUT  PARAMETER to-date    AS DATE.
DEFINE INPUT  PARAMETER from-refno AS CHAR.

DEFINE VARIABLE counter AS INTEGER NO-UNDO.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.



CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "Journalist by voucher"
       queasy.number1  = 1
       queasy.char2    = idFlag.
RELEASE queasy.


RUN gl-jourefbl.p(sorttype, from-date, to-date, from-refno,
                   OUTPUT TABLE output-list). 

FIND FIRST output-list NO-ERROR.
DO WHILE AVAILABLE output-list:
    
    ASSIGN counter = counter + 1.
        
    CREATE queasy.
    ASSIGN queasy.KEY   = 280
           queasy.char1 = "Journalist by voucher"
           queasy.char3 = idFlag
           queasy.char2 = output-list.str      + "|" + 
                          output-list.refno    
        queasy.number1 = counter.

 FIND NEXT output-list NO-ERROR.
END.


FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Journalist by voucher"
    AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.
