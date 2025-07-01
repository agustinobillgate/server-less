
DEFINE BUFFER queri FOR queasy.
define TEMP-TABLE build like queasy.

DEF INPUT PARAMETER TABLE FOR build.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST build.

IF case-type = 1 THEN   /*MT add */
DO:
    FIND FIRST queri WHERE queri.number1 = build.number1 AND queri.KEY = 135 NO-LOCK NO-ERROR.
    IF AVAILABLE queri THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        FIND FIRST queri WHERE queri.char1 = build.char1 AND queri.KEY = 135 NO-LOCK NO-ERROR.
        IF AVAILABLE queri THEN
        DO:
            fl-code = 2.
            RETURN NO-APPLY.
        END.
        ELSE
        DO:
            CREATE  queasy.  
            RUN fill-new-queasy.  
            fl-code = 3.
        END.
    END.
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST queasy WHERE RECID(queasy) = rec-id.
    FIND FIRST queri WHERE queri.char1 = build.char1 AND queri.KEY = 135  AND ROWID(queri) NE ROWID(queasy)  NO-LOCK NO-ERROR.
    IF AVAILABLE queri THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        FIND FIRST queri WHERE queri.number1 = build.number1   
            and queri.number2 = 0 and queri.deci2 = 0  
            and queri.key = 135 AND ROWID(queri) NE ROWID(queasy)
            NO-LOCK NO-ERROR.
        IF AVAILABLE queri THEN
        DO:
          fl-code = 2.
          RETURN NO-APPLY.
        END.
        ELSE
        DO:
            FIND FIRST queri WHERE queri.number1 = build.number1   
                and queri.number2 = 0 and queri.deci2 = 0  
                and queri.key = 135 AND ROWID(queri) NE ROWID(queasy)
                NO-LOCK NO-ERROR.
            IF AVAILABLE queri THEN
            DO:
                fl-code = 3.
                RETURN NO-APPLY.
            END.
            ELSE
            DO:
                FIND FIRST queasy WHERE RECID(queasy) = rec-id.
                FIND CURRENT queasy EXCLUSIVE-LOCK.  
                queasy.number1 = build.number1.
                queasy.char1 = build.char1.  
                FIND CURRENT queasy NO-LOCK .
                fl-code = 4.
            END.
        END.
    END.
END.

PROCEDURE fill-new-queasy:  
    queasy.KEY = 135.  
    queasy.number1 = build.number1.  
    queasy.char1 = build.char1.  
END.  

