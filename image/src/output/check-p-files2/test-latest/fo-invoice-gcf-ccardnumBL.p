
DEF INPUT  PARAMETER t-rechnr   AS INT.
DEF INPUT  PARAMETER t-artnr    AS INT.
DEF INPUT  PARAMETER curr-department AS INT.
DEF OUTPUT PARAMETER voucher-nr AS CHAR INITIAL "". 

FIND FIRST artikel WHERE artikel.artnr = t-artnr 
    AND artikel.departement = curr-department NO-LOCK.
FIND FIRST bill WHERE bill.rechnr = t-rechnr NO-LOCK.
RUN gcf-ccardnum.

PROCEDURE gcf-ccardnum:
  DEFINE VARIABLE i                  AS INTEGER             NO-UNDO. 
  DEFINE VARIABLE j                  AS INTEGER INITIAL 1   NO-UNDO. 
  DEFINE VARIABLE k                  AS INTEGER             NO-UNDO. 
  DEFINE VARIABLE n                  AS INTEGER INITIAL 0   NO-UNDO.
  DEFINE VARIABLE mm                 AS INTEGER INITIAL 0   NO-UNDO.
  DEFINE VARIABLE yy                 AS INTEGER INITIAL 0   NO-UNDO.
  DEFINE VARIABLE ch                 AS CHAR                NO-UNDO. 
  DEFINE VARIABLE pos2               AS INTEGER             NO-UNDO.

  DEF BUFFER gast FOR guest. 
  FIND FIRST gast WHERE gast.gastnr = bill.gastnr NO-LOCK. 
  DO i = 1 TO NUM-ENTRIES(gast.ausweis-nr2, "|"):
      ch = ENTRY(i, gast.ausweis-nr2, "|").
      IF ch MATCHES ("*" + artikel.bezeich + "*") THEN
      DO:
          ch = ENTRY(2, ch, "\").
          IF NUM-ENTRIES(ch, "\") = 2 THEN 
          DO:
            ASSIGN
                mm = INTEGER(SUBSTR(ENTRY(2, ch, "\"),1,2)) 
                yy = INTEGER(SUBSTR(ENTRY(2, ch, "\"),3,4)) NO-ERROR
            .
            IF yy GT YEAR(TODAY) OR (yy = YEAR(TODAY) AND mm GE MONTH(TODAY))
            THEN voucher-nr = TRIM(ENTRY(1, ch, "\")).
          END.
          ELSE IF NUM-ENTRIES(ch, "\") = 1 THEN voucher-nr = TRIM(ch).
          RETURN.
      END.
  END.
END PROCEDURE. 
