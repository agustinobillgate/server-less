
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
  FIELD comments        AS CHARACTER
  FIELD fibukonto       LIKE gl-journal.fibukonto     
  FIELD t-bezeich       LIKE gl-acct.bezeich          
  FIELD debt2            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0  
  FIELD recv-date       AS DATE.
 
DEFINE TEMP-TABLE pay-list 
  FIELD dummy    AS CHARACTER   FORMAT "x(30)" 
  FIELD artnr    AS INTEGER     FORMAT ">>>9" 
  FIELD bezeich  AS CHARACTER   FORMAT "x(32)" 
  FIELD proz     AS DECIMAL     FORMAT "->>9.99" 
  FIELD betrag   AS DECIMAL     FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
  FIELD remark   AS CHAR. /*bernatd 2024 677974*/

DEFINE TEMP-TABLE t-l-lieferant 
    FIELD telefon   LIKE l-lieferant.telefon
    FIELD fax       LIKE l-lieferant.fax
    FIELD adresse1  LIKE l-lieferant.adresse1
    FIELD notizen-1 AS CHAR
    FIELD lief-nr   LIKE l-lieferant.lief-nr.

DEFINE INPUT PARAMETER TABLE FOR age-list.
DEFINE INPUT PARAMETER TABLE FOR pay-list.
DEFINE INPUT PARAMETER rundung      AS INTEGER.
DEFINE INPUT PARAMETER outstand     AS DECIMAL.
DEFINE INPUT PARAMETER outstand1    AS DECIMAL.
DEFINE INPUT PARAMETER pay-date     AS DATE.
DEFINE INPUT PARAMETER remark       AS CHARACTER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.

DEFINE OUTPUT PARAMETER msg-str AS CHAR.

DEFINE VARIABLE anzahl AS INTEGER. 
DEFINE VARIABLE okflag AS LOGICAL. 

okflag = NO. 
IF outstand = 0 THEN okflag = YES. 
ELSE 
DO: 
    anzahl = 0. 
    FOR EACH age-list WHERE age-list.selected = YES NO-LOCK: 
        anzahl = anzahl + 1. 
    END. 
    IF anzahl = 1 THEN okflag = YES. 
END. 

IF okflag THEN 
DO: 
    RUN ap-debtpay-settle-paymentbl.p (INPUT-OUTPUT TABLE pay-list, 
        INPUT-OUTPUT TABLE age-list, user-init, outstand, outstand1, rundung, pay-date, remark,
        OUTPUT TABLE t-l-lieferant).
    msg-str = "AP Payment Success".
END. 
ELSE 
DO: 
    msg-str = "Partial Payment for multi-selected A/P records not possible".
    RETURN. 
END. 
