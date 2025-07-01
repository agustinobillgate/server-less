DEFINE TEMP-TABLE payload-list
    FIELD artnr       AS INTEGER
    FIELD lscheinnr   AS CHARACTER
    FIELD remark      AS CHARACTER
    FIELD einzelpreis AS DECIMAL
.

DEFINE INPUT PARAMETER TABLE FOR payload-list.

DEFINE VARIABLE valid-input AS LOGICAL INITIAL NO.
DEFINE VARIABLE artnr       AS INTEGER.
DEFINE VARIABLE lscheinnr   AS CHARACTER.
DEFINE VARIABLE remark      AS CHARACTER.
DEFINE VARIABLE einzelpreis AS DECIMAL.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        artnr       = payload-list.artnr
        lscheinnr   = payload-list.lscheinnr
        remark      = payload-list.remark
        einzelpreis = payload-list.einzelpreis
    .

    FIND FIRST queasy WHERE queasy.KEY EQ 340
        AND queasy.char1 EQ lscheinnr
        AND queasy.number1 EQ artnr
        AND queasy.deci1 EQ einzelpreis NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY     = 340
            queasy.char1   = lscheinnr
            queasy.number1 = artnr
            queasy.char2   = remark
            queasy.deci1   = einzelpreis
        .
    END.
    ELSE
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN 
            queasy.char2   = remark
        .
        FIND CURRENT queasy NO-LOCK.
    END.
END.

