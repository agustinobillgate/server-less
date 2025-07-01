
DEF INPUT  PARAMETER billNo    AS INTEGER.
DEF INPUT  PARAMETER start-pos AS INTEGER.
DEF OUTPUT PARAMETER vat-str   AS CHAR INITIAL "".

/*
DEF VAR billNo    AS INTEGER INITIAL 2420.
DEF VAR start-pos AS INTEGER INITIAL 1.
DEF VAR vat-str   AS CHAR INITIAL "".
*/
DEF VARIABLE         ind       AS INTEGER               NO-UNDO.
DEF VARIABLE         curr-vat  AS DECIMAL               NO-UNDO.
DEF VARIABLE         vatAmt    AS DECIMAL               NO-UNDO.
DEF VARIABLE         curr-str  AS CHAR                  NO-UNDO.
DEF VARIABLE         gdelimit  AS CHAR INITIAL "VAT%,"  NO-UNDO.
DEF VARIABLE         prozSpace AS CHAR                  NO-UNDO.
DEF VARIABLE         vatSpace  AS CHAR                  NO-UNDO.
DEF VARIABLE         netSpace  AS CHAR                  NO-UNDO.
DEF VARIABLE         curr-pos  AS INTEGER               NO-UNDO.
DEF VARIABLE         nextLoop  AS LOGICAL INITIAL NO    NO-UNDO.

/* user's customizable value */
ASSIGN
    prozSpace = FILL("KDV% ", 1)
    vatSpace  = FILL("KDV ", 1)
    netSpace  = FILL("NET ", 1)
.

DEF TEMP-TABLE vat-artlist
    FIELD artnr AS INTEGER.

DEFINE WORKFILE vat-list
    FIELD vatProz AS DECIMAL INITIAL 0
    FIELD vatAmt  AS DECIMAL INITIAL 0
    FIELD netto   AS DECIMAL INITIAL 0
    FIELD amount  AS DECIMAL INITIAL 0
.

DEFINE SHARED VARIABLE spbill-flag AS LOGICAL.
DEFINE SHARED WORKFILE spbill-list 
  FIELD selected AS LOGICAL INITIAL YES 
  FIELD bl-recid AS INTEGER
. 

FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK.
IF htparam.fchar NE "" THEN
DO ind = 1 TO NUM-ENTRIES(htparam.fchar, ";"):
    IF INTEGER(ENTRY(ind, htparam.fchar, ";")) NE 0 THEN
    DO:
        CREATE vat-artlist.
        ASSIGN vat-artlist.artnr = INTEGER(ENTRY(ind, htparam.fchar, ";")).
    END.
END.

IF spbill-flag THEN
FOR EACH spbill-list WHERE spbill-list.selected = YES:
  FIND FIRST bill-line WHERE RECID(bill-line) = spbill-list.bl-recid NO-LOCK.
  RUN calc-vat.
END.
ELSE /* spbill-flag = FALSE */
FOR EACH bill-line WHERE bill-line.rechnr = billNo NO-LOCK:
  RUN calc-vat.
END.

FOR EACH vat-list.
  IF nextLoop THEN
  DO ind = 1 TO (start-pos - 1):
     vat-str = vat-str + " ".
  END.
  nextLoop = YES.
  
  vat-str = vat-str  + prozSpace + TRIM(STRING(vat-list.vatProz, ">9.99")) + FILL(" ", LENGTH(STRING(vat-list.vatProz, ">9.99")) - LENGTH(TRIM(STRING(vat-list.vatProz, ">9.99")))) 
          + vatSpace + TRIM(STRING(vat-list.vatAmt,  "->,>>>,>>9.99"))     + FILL(" ", LENGTH(STRING(vat-list.vatAmt,  "->,>>>,>>9.99")) - LENGTH(TRIM(STRING(vat-list.vatAmt,  "->,>>>,>>9.99")))) 
          + netSpace +  TRIM(STRING(vat-list.netto,   "->>,>>>,>>9.99"))   + FILL(" ", LENGTH(STRING(vat-list.netto,   "->>,>>>,>>9.99")) - LENGTH(TRIM(STRING(vat-list.netto,   "->>,>>>,>>9.99")))) 
          + "Total "  + TRIM(STRING(vat-list.amount,  "->>,>>>,>>9.99"))    + CHR(10).

END.


PROCEDURE calc-vat:
    curr-vat = 0.
    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr
        AND artikel.departement = bill-line.departement NO-LOCK.
    IF artikel.artart NE 2 AND artikel.artart NE 6
        AND artikel.artart NE 7 THEN
    DO:
      FIND FIRST vat-artlist WHERE vat-artlist.artnr = artikel.artnr
          NO-ERROR.
      IF INDEX(bill-line.origin-id, gdelimit) GT 0 THEN 
      ASSIGN
        curr-pos = INDEX(bill-line.origin-id, gdelimit)
        curr-str = SUBSTR(bill-line.origin-id, curr-pos + LENGTH(gdelimit)) 
        curr-vat = DECIMAL(ENTRY(1, curr-str, ";")) * 0.01.
      ELSE 
      DO:
        FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK
            NO-ERROR.
        IF AVAILABLE htparam THEN curr-vat = htparam.fdecimal.
      END.
      FIND FIRST vat-list WHERE vat-list.vatProz = curr-vat NO-ERROR.
      IF NOT AVAILABLE vat-list THEN
      DO:
        CREATE vat-list.
        ASSIGN vat-list.vatProz = curr-vat.
      END.
      IF AVAILABLE vat-artlist THEN vatAmt = bill-line.betrag.
      ELSE
      DO:
        IF bill-line.orts-tax NE 0 THEN vatAmt = bill-line.orts-tax.
        ELSE vatAmt = bill-line.betrag / (1 + curr-vat * 0.01) * curr-vat * 0.01. /* was 0.001, Izzet changed to 0.01 */
      END.
             
      ASSIGN vat-list.amount = vat-list.amount + bill-line.betrag
        vat-list.netto       = vat-list.netto  + bill-line.betrag - vatAmt
        vat-list.vatAmt      = vat-list.vatAmt + vatAmt
      .
    END.
END.
