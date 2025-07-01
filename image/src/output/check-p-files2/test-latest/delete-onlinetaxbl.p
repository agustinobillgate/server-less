.
DEFINE INPUT PARAMETER fr-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date AS DATE NO-UNDO.

DEFINE VARIABLE curr-date   AS DATE NO-UNDO.
DEFINE VARIABLE bill-date   AS DATE NO-UNDO.
DEFINE BUFFER nbuff FOR nitehis.

FIND FIRST nightaudit WHERE nightaudit.programm = "nt-onlinetax.p" 
   NO-LOCK NO-ERROR.
IF NOT AVAILABLE nightaudit THEN RETURN.

RUN htpdate.p(110, OUTPUT bill-date).
IF curr-date = 01/01/2000 THEN curr-date = bill-date - 1.

DO curr-date = fr-date TO to-date:
    FIND FIRST nitehis WHERE nitehis.datum = curr-date
        AND nitehis.reihenfolge = nightaudit.reihenfolge
        AND nitehis.LINE = "END-OF-RECORD" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE nitehis THEN RETURN.

    FIND FIRST nitehis WHERE nitehis.datum = curr-date
        AND nitehis.reihenfolge = nightaudit.reihenfolge
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE nitehis:
        FIND FIRST nbuff WHERE RECID(nbuff) = RECID(nitehis).
        DELETE nbuff.
        RELEASE nbuff.
        FIND NEXT nitehis WHERE nitehis.datum = curr-date
            AND nitehis.reihenfolge = nightaudit.reihenfolge
            NO-LOCK NO-ERROR.
    END.

END.
