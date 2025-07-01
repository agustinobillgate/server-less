DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

FIND FIRST t-queasy NO-ERROR.
  
CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY AND queasy.char1 
            EQ t-queasy.char1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            ASSIGN success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY
            AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            ASSIGN success-flag = YES.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY
            AND queasy.number1 = t-queasy.number1
            AND queasy.char1 EQ t-queasy.char1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            ASSIGN success-flag = YES.
        END.
    END.
    WHEN 11 THEN  /* special for hk-preference !!!! */
    DO:
        FIND FIRST queasy WHERE RECID(queasy) = t-queasy.number3
          EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.

