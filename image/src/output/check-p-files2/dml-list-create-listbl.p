DEFINE TEMP-TABLE dml-list
    FIELD counter   AS INTEGER
    FIELD dml-nr    AS CHARACTER
    FIELD dept      AS CHARACTER
    FIELD id        AS CHARACTER
    FIELD approved  AS LOGICAL INIT NO.

DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER selected-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR dml-list.

DEFINE BUFFER rqueasy FOR reslin-queasy.
DEFINE VARIABLE nr AS INT INIT 1.


FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
    AND reslin-queasy.date1 EQ selected-date 
    AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE reslin-queasy THEN
DO:
    FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.

    IF curr-dept EQ 0 THEN
    DO:
        FIND FIRST dml-art WHERE dml-art.datum = selected-date 
            AND NUM-ENTRIES(dml-art.chginit, ";") GT 1
            AND ENTRY(2, dml-art.chginit, ";") NE "" NO-LOCK NO-ERROR.
        IF NOT AVAILABLE dml-art THEN
             FIND FIRST dml-art WHERE dml-art.datum = selected-date NO-LOCK NO-ERROR.

        IF AVAILABLE dml-art THEN
        DO:
            CREATE dml-list.
            ASSIGN
                counter = 1
                /*dml-nr  = ENTRY(2, dml-art.chginit, ";")*/
                dept    = hoteldpt.depart
                id      = dml-art.userinit.

            IF NUM-ENTRIES(dml-art.chginit,";") GT 1 THEN
            DO:
                dml-nr  = ENTRY(2, dml-art.chginit, ";").
            END.
            ELSE
            DO:
                dml-nr  = "".
            END.

            IF dml-art.chginit MATCHES "*!*" THEN
                approved = YES.
            ELSE
                approved = NO.
        END.
    END.
    ELSE
    DO:
        FIND FIRST dml-artdep WHERE dml-artdep.datum EQ selected-date
            AND dml-artdep.departement EQ curr-dept
            AND NUM-ENTRIES(dml-artdep.chginit, ";") GT 1
            AND ENTRY(2, dml-artdep.chginit, ";") NE "" NO-LOCK NO-ERROR.
        IF NOT AVAILABLE dml-artdep THEN
            FIND FIRST dml-artdep WHERE dml-artdep.datum EQ selected-date
                AND dml-artdep.departement EQ curr-dept NO-LOCK NO-ERROR.

        IF AVAILABLE dml-artdep THEN
        DO:
            CREATE dml-list.
            ASSIGN
                counter = 1                
                dept    = hoteldpt.depart
                id      = dml-artdep.userinit.

            IF NUM-ENTRIES(dml-artdep.chginit,";") GT 1 THEN
            DO:
                dml-nr  = ENTRY(2, dml-artdep.chginit, ";").
            END.
            ELSE
            DO:
                dml-nr  = "".
            END.

            IF dml-artdep.chginit MATCHES "*!*" THEN
                approved = YES.
            ELSE
                approved = NO.
        END.
    END.

    FOR EACH rqueasy WHERE rqueasy.KEY EQ "DML"
        AND rqueasy.date1 EQ selected-date 
        AND INT(ENTRY(2,rqueasy.char1,";")) EQ curr-dept NO-LOCK:
        IF rqueasy.number2 NE nr THEN
        DO:
            nr = rqueasy.number2.
            CREATE dml-list.
            ASSIGN
                counter = rqueasy.number2
                dml-nr  = ENTRY(2, rqueasy.char3, ";")
                dept    = hoteldpt.depart
                id      = rqueasy.char2.
            IF rqueasy.char3 MATCHES "*!*" THEN
                approved = YES.
            ELSE
                approved = NO.
        END.
        /*FIND NEXT rqueasy WHERE rqueasy.KEY EQ "DML"
            AND rqueasy.date1 EQ selected-date 
            AND INT(ENTRY(2,rqueasy.char1,";")) EQ curr-dept NO-LOCK NO-ERROR.*/
    END.
END.
