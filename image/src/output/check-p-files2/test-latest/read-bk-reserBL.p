
DEFINE TEMP-TABLE t-bk-reser LIKE bk-reser.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER veranNo      AS INTEGER.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE INPUT PARAMETER resstatus    AS INTEGER.
DEFINE INPUT PARAMETER zeit         AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-reser.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST bk-reser WHERE bk-reser.veran-nr = veranNo
            AND bk-reser.datum GT datum
            AND bk-reser.resstatus LE resstatus NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-reser THEN
        DO:
            CREATE t-bk-reser.
            BUFFER-COPY bk-reser TO t-bk-reser.
        END.
    END.
    WHEN 2 THEN
    DO: 
        FIND FIRST t-bk-reser WHERE t-bk-reser.veran-nr = veranNo
            AND t-bk-reser.datum = datum AND t-bk-reser.resstatus = resstatus
            AND (t-bk-reser.bis-i * 1800) GT zeit NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-reser THEN
        DO:
            CREATE t-bk-reser.
            BUFFER-COPY bk-reser TO t-bk-reser.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH bk-reser WHERE bk-reser.veran-nr = veranNo
            AND bk-reser.resstatus = resstatus NO-LOCK :
            CREATE t-bk-reser.
            BUFFER-COPY bk-reser TO t-bk-reser.
        END.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST bk-reser WHERE bk-reser.veran-nr = veranNo
            AND bk-reser.resstatus = resstatus NO-LOCK NO-ERROR.
        IF AVAILABLE bk-reser THEN
        DO:
            CREATE t-bk-reser.
            BUFFER-COPY bk-reser TO t-bk-reser.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH bk-reser WHERE bk-reser.veran-nr = veranNo
            AND bk-reser.resstatus NE resstatus NO-LOCK :
            CREATE t-bk-reser.
            BUFFER-COPY bk-reser TO t-bk-reser.
        END.
    END.
END CASE.
