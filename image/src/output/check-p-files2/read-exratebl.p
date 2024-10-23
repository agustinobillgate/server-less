DEFINE TEMP-TABLE t-exrate      LIKE exrate.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER artNo        AS INTEGER.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-exrate.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST exrate WHERE exrate.artnr = artNo
            AND exrate.datum = datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN 
        DO:
            CREATE t-exrate.
            BUFFER-COPY exrate TO t-exrate.
        END.                               
    END.
END CASE.
