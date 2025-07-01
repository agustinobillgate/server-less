DEFINE INPUT PARAMETER veran-nr  AS INTEGER.
DEFINE INPUT PARAMETER veran-seite AS INTEGER.
DEFINE INPUT PARAMETER curr-date AS DATE.
DEFINE OUTPUT PARAMETER error-nr AS INTEGER.

FIND FIRST bk-reser WHERE bk-reser.veran-nr = veran-nr 
    AND bk-reser.veran-seite = veran-seite
    AND bk-reser.resstatus EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE bk-reser THEN DO:
    ASSIGN error-nr = 1.
    RETURN NO-APPLY.
END.

IF bk-reser.datum LE curr-date AND AVAILABLE bk-reser THEN DO:
    ASSIGN error-nr = 2.
    RETURN NO-APPLY.
END.
