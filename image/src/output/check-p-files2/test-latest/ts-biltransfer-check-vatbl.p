DEF TEMP-TABLE vat-list
    FIELD vat AS DECIMAL
.

DEF INPUT  PARAMETER rec-id     AS INT.
DEF INPUT  PARAMETER multi-vat  AS LOGICAL.
DEF INPUT  PARAMETER balance    AS DECIMAL. 
DEF INPUT  PARAMETER closed     AS LOGICAL. 
DEF INPUT  PARAMETER splitted   AS LOGICAL. 
DEF OUTPUT PARAMETER fl-code    AS INT INIT 0.
DEF OUTPUT PARAMETER its-ok     AS LOGICAL INIT YES.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
RUN check-vat.

FOR EACH vat-list:
    DELETE vat-list.
END.

PROCEDURE check-vat:
DEF VAR anz-vat AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR anz-pay AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR tot-rev AS DECIMAL INITIAL 0 NO-UNDO.

  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
      AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK.
      IF vhp.h-bill-line.artnr = 0 THEN anz-pay = anz-pay + 1.
      ELSE
      DO:
          FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr
              AND vhp.h-artikel.departement = vhp.h-bill-line.departement
              NO-LOCK.
          IF vhp.h-artikel.artart NE 0 THEN anz-pay = anz-pay + 1.
          ELSE
          DO:
            tot-rev = tot-rev + vhp.h-bill-line.betrag.
            FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = vhp.h-artikel.mwst-code
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE vhp.htparam THEN
            DO:
                FIND FIRST vat-list /*WHERE vat-list.vat = 0*/ NO-ERROR.
                IF NOT AVAILABLE vat-list THEN
                DO:
                    CREATE vat-list.
                    ASSIGN vat-list.vat = 0
                           anz-vat = anz-vat + 1.
                END.
            END.
            ELSE
            DO:
                FIND FIRST vat-list /*WHERE vat-list.vat = vhp.htparam.fdecimal*/ NO-ERROR.
                IF NOT AVAILABLE vat-list THEN
                DO:
                    CREATE vat-list.
                    ASSIGN vat-list.vat = vhp.htparam.fdecimal
                           anz-vat = anz-vat + 1.
                END.
            END.
          END.
      END.
  END.
  IF anz-vat LE 1 AND NOT multi-vat THEN RETURN.
  IF (tot-rev = balance) OR (tot-rev = - balance) AND closed THEN RETURN.

  IF anz-pay GE 1 AND NOT splitted THEN 
  DO:
    fl-code = 1.
    its-ok = NO.
  END.
END.
