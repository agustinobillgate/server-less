DEF TEMP-TABLE online-tax
    FIELD line-nr   AS INTEGER
    FIELD ct        AS CHAR
    FIELD departement AS INTEGER
.
/*
DEFINE VAR curr-date AS DATE        NO-UNDO INIT 04/06/13.
DEFINE VAR already-read AS LOGICAL NO-UNDO INIT NO.
*/
DEFINE INPUT PARAMETER curr-date AS DATE        NO-UNDO.
DEFINE OUTPUT PARAMETER already-read AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR online-tax.

DEFINE VARIABLE bill-date   AS DATE NO-UNDO.
DEFINE BUFFER nbuff FOR nitehis.

FIND FIRST nightaudit WHERE nightaudit.programm = "nt-onlinetax.p" 
   NO-LOCK NO-ERROR.
IF NOT AVAILABLE nightaudit THEN RETURN.

RUN htpdate.p(110, OUTPUT bill-date).
IF curr-date = 01/01/2000 THEN curr-date = bill-date - 1.

FIND FIRST nitehis WHERE nitehis.datum = curr-date
    AND nitehis.reihenfolge = nightaudit.reihenfolge
    AND nitehis.LINE = "END-OF-RECORD" NO-LOCK NO-ERROR.
IF NOT AVAILABLE nitehis THEN RETURN.
ELSE IF AVAILABLE nitehis AND nitehis.line-nr = 99999999 THEN
DO:
    ASSIGN already-read = YES.
    RETURN.
END.
FOR EACH nitehis WHERE nitehis.datum = curr-date
    AND nitehis.reihenfolge = nightaudit.reihenfolge
    NO-LOCK BY nitehis.line-nr:
    IF nitehis.LINE = "END-OF-RECORD" THEN 
    DO: 
        FIND FIRST nbuff WHERE RECID(nbuff) = RECID(nitehis).
        ASSIGN nbuff.line-nr = 99999999.
        FIND CURRENT nbuff NO-LOCK.
        LEAVE.
    END.
    CREATE online-tax.
    ASSIGN 
        online-tax.line-nr      = nitehis.line-nr
        online-tax.ct           = ENTRY(1, nitehis.LINE ,CHR(2))
        online-tax.departement  = INTEGER(ENTRY(2, nitehis.LINE ,CHR(2)))
    .
END.

