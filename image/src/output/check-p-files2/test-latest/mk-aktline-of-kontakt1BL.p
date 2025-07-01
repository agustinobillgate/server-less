
DEF INPUT  PARAMETER gastnr                 AS INT.
DEF INPUT  PARAMETER gname                  AS CHAR.
DEF INPUT  PARAMETER akt-line1-gastnr       AS INT.
DEF INPUT  PARAMETER akt-line1-kontakt-nr   AS INT.
DEF OUTPUT PARAMETER t-kontakt              AS CHAR.
DEF OUTPUT PARAMETER t-gastnr               AS INT.
DEF OUTPUT PARAMETER t-kontakt-nr           AS INT.
DEF OUTPUT PARAMETER avail-guest            AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-akt-kont         AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-akt-kont1        AS LOGICAL INIT NO.

FIND FIRST guest WHERE guest.gastnr = akt-line1-gastnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN RETURN.
ELSE
DO :
    avail-guest = YES.
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastnr AND akt-kont.NAME = gname 
        OR (akt-kont.name + ", " + akt-kont.anrede) = gname NO-LOCK NO-ERROR.
    IF NOT AVAILABLE akt-kont THEN RETURN.
    ELSE
    DO:
        avail-akt-kont = YES.
        t-kontakt-nr = akt-kont.kontakt-nr.
        /*FIND FIRST akt-kont WHERE akt-kont.gastnr = akt-line1-kontakt-nr NO-LOCK NO-ERROR.*/
        FIND FIRST akt-kont WHERE akt-kont.gastnr = gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE akt-kont AND akt-kont.name NE "" THEN
        DO:
            avail-akt-kont1 = YES.
            t-kontakt = akt-kont.name + ", " + akt-kont.anrede. 
            t-gastnr = guest.gastnr. 
        END.
    END.
END.

