DEFINE TEMP-TABLE output-list 
    FIELD STR AS CHAR
    FIELD refno AS CHAR. 

DEFINE INPUT PARAMETER idFlag       AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag    AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE counter AS INTEGER NO-UNDO.


DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

FIND FIRST queasy WHERE queasy.KEY = 280 AND queasy.char1 = "Journalist by voucher" 
    AND queasy.char3 = idFlag NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:
        ASSIGN counter = counter + 1.
        IF counter GT 7000 THEN LEAVE.

        CREATE output-list.
        ASSIGN output-list.str   = ENTRY(1, queasy.char2, "|")
               output-list.refno = ENTRY(2, queasy.char2, "|")
        .

        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE bqueasy.
        RELEASE bqueasy.
    
     FIND NEXT queasy WHERE queasy.KEY = 280 AND queasy.char1 = "Journalist by voucher" 
            AND queasy.char3 = idFlag NO-LOCK NO-ERROR.
END.

FIND FIRST pqueasy WHERE pqueasy.KEY = 280 
    AND pqueasy.char1 = "Journalist by voucher"
    AND pqueasy.char3 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN doneFlag = NO.
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
        AND tqueasy.char1 = "Journalist by voucher" 
        AND tqueasy.number1 = 1
        AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN doneFlag = NO.
    END.
    ELSE DO: 
        ASSIGN doneFlag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
      AND tqueasy.char1 = "Journalist by voucher" 
      AND tqueasy.number1 = 0
      AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.
