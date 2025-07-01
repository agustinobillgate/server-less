DEFINE TEMP-TABLE age-list 
  FIELD selected        AS LOGICAL   INITIAL NO 
  FIELD ap-recid        AS INTEGER 
  FIELD counter         AS INTEGER 
  FIELD docu-nr         AS CHARACTER FORMAT "x(10)" 
  FIELD rechnr          AS INTEGER 
  FIELD lief-nr         AS INTEGER 
  FIELD lscheinnr       AS CHARACTER FORMAT "x(23)" 
  FIELD supplier        AS CHARACTER FORMAT "x(24)" 
  FIELD rgdatum         AS DATE 
  FIELD rabatt          AS DECIMAL   FORMAT ">9.99" 
  FIELD rabattbetrag    AS DECIMAL   FORMAT "->,>>>,>>9.99" 
  FIELD ziel            AS DATE 
  FIELD netto           AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD user-init       AS CHARACTER FORMAT "x(4)" 
  FIELD debt            AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD credit          AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD bemerk          AS CHARACTER 
  FIELD tot-debt        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
  FIELD rec-id          AS INTEGER
  FIELD resname         AS CHARACTER
  FIELD comments        AS CHARACTER.
 
DEF TEMP-TABLE artikel-list
  FIELD artnr       LIKE artikel.artnr
  FIELD departement LIKE artikel.departement
  FIELD bezeich     LIKE artikel.bezeich
  FIELD artart      LIKE artikel.artart.

DEFINE TEMP-TABLE t-queasy  LIKE queasy.
DEFINE TEMP-TABLE t-artikel LIKE artikel.

DEFINE INPUT PARAMETER TABLE FOR age-list.
DEFINE INPUT PARAMETER rundung AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER outstand AS DECIMAL.
DEFINE OUTPUT PARAMETER outstand1 AS DECIMAL.
DEFINE OUTPUT PARAMETER msg-str AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR artikel-list.

DEF VAR p-786 AS CHAR.
RUN htpchar.p(786, OUTPUT p-786).

FIND FIRST age-list NO-LOCK NO-ERROR.
IF p-786 NE "" AND AVAILABLE age-list THEN
    RUN ap-read-approvalbl.p(1, age-list.lief-nr, "", OUTPUT TABLE t-queasy).

FIND FIRST age-list WHERE age-list.SELECTED EQ YES NO-LOCK NO-ERROR.
IF NOT AVAILABLE age-list THEN
DO:
    msg-str = "No Selected Record, payment not possible!".
    RETURN.
END.

DEFINE BUFFER age-list-buff FOR age-list.
FOR EACH age-list-buff WHERE age-list-buff.SELECTED:
    IF p-786 NE "" AND age-list-buff.rechnr = 0 THEN DO:       
        msg-str = "A/P Voucher No not attched, transaction is not possible".
        RETURN.
    END.
    FIND FIRST t-queasy WHERE t-queasy.number1 = age-list-buff.lief-nr
        AND t-queasy.number2 = age-list-buff.rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE t-queasy THEN DO:
        msg-str = "A/P Voucher No, not approved completedly".
        RETURN.
    END.
END.

RUN load-artikelbl.p (9, ?, OUTPUT TABLE artikel-list, OUTPUT TABLE t-artikel).

outstand = round(outstand, rundung). 
outstand1 = outstand.
