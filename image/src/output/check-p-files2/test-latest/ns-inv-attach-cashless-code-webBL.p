DEFINE TEMP-TABLE b1-list
    FIELD resnr         LIKE bill.resnr
    FIELD rechnr        LIKE bill.rechnr
    FIELD name          LIKE guest.name
    FIELD vorname1      LIKE guest.vorname1
    FIELD anrede1       LIKE guest.anrede1
    FIELD saldo         LIKE bill.saldo
    FIELD printnr       LIKE bill.printnr
    FIELD datum         LIKE bill.datum
    FIELD b-recid       AS INTEGER
    FIELD adresse1      LIKE guest.adresse1
    FIELD wohnort       LIKE guest.wohnort
    FIELD bemerk        LIKE guest.bemerkung
    FIELD plz           LIKE guest.plz
    FIELD bill-datum    AS DATE
    FIELD qr-code       AS CHARACTER
    .

DEFINE TEMP-TABLE t-reservation LIKE reservation.
DEFINE TEMP-TABLE t-bk-reser    LIKE bk-reser.
DEFINE TEMP-TABLE t-bk-veran    LIKE bk-veran.

DEFINE INPUT PARAMETER sorttype AS INTEGER.
DEFINE INPUT PARAMETER gastname AS CHARACTER.
DEFINE INPUT PARAMETER dept     AS INTEGER.
DEFINE INPUT PARAMETER rechnr   AS INTEGER.
DEFINE OUTPUT PARAMETER resname AS CHARACTER.
DEFINE OUTPUT PARAMETER address AS CHARACTER.
DEFINE OUTPUT PARAMETER city    AS CHARACTER.
DEFINE OUTPUT PARAMETER comments AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

DEFINE VARIABLE ba-dept AS INTEGER NO-UNDO.
DEFINE VARIABLE fr-name AS CHAR INITIAL "".
DEFINE VARIABLE to-name AS CHAR.
DEFINE VARIABLE stat AS CHAR FORMAT "x(10)" EXTENT 9 
    INITIAL ["Fix", "Tentative", "", "", "", "", "", "Closed", "Cancelled"]. 

RUN htpint.p(900, OUTPUT ba-dept).

RUN ns-inv-attach-cashless-codebl.p (0, sorttype, gastname, dept, ba-dept, rechnr, OUTPUT TABLE b1-list).

FIND FIRST b1-list NO-LOCK NO-ERROR.
IF AVAILABLE b1-list THEN
DO:
    resname = b1-list.name. 
    address = b1-list.adresse1. 
    city = b1-list.wohnort + " " + b1-list.plz. 
    
    IF dept = ba-dept AND b1-list.rechnr NE 0 THEN 
    DO:
        RUN read-bk-veranbl.p(2, ?,?, b1-list.rechnr, ?, OUTPUT TABLE t-bk-veran).
        FIND FIRST t-bk-veran NO-ERROR.
        IF AVAILABLE t-bk-veran THEN
        DO: 
            comments = "RefNo: " + STRING(t-bk-veran.veran-nr) + CHR(10).
            RUN read-bk-reserbl.p(5, t-bk-veran.veran-nr, ?, 9, ?, OUTPUT TABLE t-bk-reser).
            FOR EACH t-bk-reser :
              comments = comments + STRING(t-bk-reser.veran-resnr) 
                + ": " + stat[t-bk-reser.resstatus] 
                + " " + STRING(t-bk-reser.datum) + CHR(10) 
                + t-bk-reser.raum + " " + STRING(t-bk-reser.von-zeit,"99:99") + " - " 
                + STRING(t-bk-reser.bis-zeit,"99:99") + CHR(10). 
            END. 
        END. 
    END.
    comments = comments +  b1-list.bemerk.
    
    RUN read-reservationbl.p(1, b1-list.resnr, ?, "", OUTPUT TABLE t-reservation).
    FIND FIRST t-reservation NO-ERROR.
    IF AVAILABLE t-reservation AND t-reservation.bemerk NE "" THEN
    DO:
        comments = comments + CHR(10) + t-reservation.bemerk.
    END.
END.
