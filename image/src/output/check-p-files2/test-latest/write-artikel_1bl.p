DEFINE TEMP-TABLE t-artikel   LIKE artikel
    FIELD rec-id AS INT
    FIELD minibar AS LOGICAL
    .

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-artikel.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL INITIAL NO.

FIND FIRST t-artikel NO-LOCK NO-ERROR.
IF NOT AVAILABLE t-artikel THEN RETURN.

CASE case-type :
    WHEN 1 THEN
    DO:
        CREATE artikel.
        BUFFER-COPY t-artikel TO artikel.
        RELEASE artikel.
        success-flag = YES.

        CREATE queasy.
        ASSIGN 
            queasy.KEY = 266
            queasy.number1 = t-artikel.departement
            queasy.number2 = t-artikel.artnr
            queasy.logi1   = t-artikel.minibar.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST artikel WHERE RECID(artikel) = t-artikel.rec-id EXCLUSIVE-LOCK.
        IF AVAILABLE artikel THEN
        DO:
            BUFFER-COPY t-artikel TO artikel.
            RELEASE artikel.
            success-flag = YES.
        END.
        
        FIND FIRST queasy WHERE queasy.KEY EQ 266
             AND queasy.number1 EQ t-artikel.departement
             AND queasy.number2 EQ t-artikel.artnr EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
            queasy.KEY = 266
            queasy.number1 = t-artikel.departement
            queasy.number2 = t-artikel.artnr
            queasy.logi1   = t-artikel.minibar.
        END.
        ELSE
        DO:
            queasy.logi1 = t-artikel.minibar.
        END.
        RELEASE queasy.
    END.

END CASE.
