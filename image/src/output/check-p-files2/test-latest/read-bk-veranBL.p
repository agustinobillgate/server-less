
DEFINE TEMP-TABLE t-bk-veran LIKE bk-veran.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER gastNo    AS INTEGER.
DEFINE INPUT PARAMETER resstat   AS INTEGER.
DEFINE INPUT PARAMETER rechNo    AS INTEGER.
DEFINE INPUT PARAMETER actFlag   AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-veran.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST bk-veran WHERE bk-veran.gastnr = gastNo
            AND bk-veran.resstatus LE resstat NO-LOCK NO-ERROR.
        IF AVAILABLE bk-veran THEN
        DO:
            CREATE t-bk-veran.
            BUFFER-COPY bk-veran TO t-bk-veran.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST bk-veran WHERE bk-veran.rechnr = rechNo NO-LOCK NO-ERROR.
        IF AVAILABLE bk-veran THEN
        DO:
            CREATE t-bk-veran.
            BUFFER-COPY bk-veran TO t-bk-veran.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST bk-veran WHERE bk-veran.rechnr = rechNo
            AND bk-veran.activeflag = actFlag NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-veran THEN
        DO:
            CREATE t-bk-veran.
            BUFFER-COPY bk-veran TO t-bk-veran.
        END.
    END.
END CASE.
