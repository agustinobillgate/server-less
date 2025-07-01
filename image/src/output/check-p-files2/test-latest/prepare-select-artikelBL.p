
DEFINE TEMP-TABLE art-list 
  FIELD artnr   AS INTEGER  FORMAT ">>>9"   LABEL "Art" FONT 2 
  FIELD bezeich AS CHAR     FORMAT "x(24)"  LABEL "Article Description" FONT 2 
  FIELD h-our   AS INTEGER EXTENT 48 FORMAT "-99" FONT 2 
  FIELD astatus AS INTEGER EXTENT 48. 

DEF INPUT  PARAMETER veran-nr           AS INT.
DEF INPUT  PARAMETER veran-seite        AS INT.
DEF INPUT  PARAMETER sub-group          AS INT.
DEF OUTPUT PARAMETER curr-date          AS DATE.
DEF OUTPUT PARAMETER bill-date          AS DATE.
DEF OUTPUT PARAMETER ba-dept            AS INT.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate       AS LOGICAL.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER TABLE FOR art-list.

FIND FIRST bk-reser WHERE bk-reser.veran-nr = veran-nr 
  AND bk-reser.veran-resnr = veran-seite NO-LOCK. 
curr-date = bk-reser.datum. 
 
FIND FIRST htparam WHERE htparam.paramnr = 110 USE-INDEX paramnr_ix NO-LOCK. 
bill-date = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 900 USE-INDEX paramnr_ix NO-LOCK. 
ba-dept = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 

IF foreign-rate OR double-currency THEN 
DO: 
  FIND FIRST htparam  WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 

RUN create-availability. 

PROCEDURE create-availability: 
DEF VAR i      AS INTEGER. 
DEF VAR from-i AS INTEGER. 
DEF VAR to-i   AS INTEGER. 
 
  FOR EACH art-list: 
      DELETE art-list. 
  END. 
 
  FOR EACH artikel WHERE artikel.departement = ba-dept 
    AND artikel.zwkum = sub-group AND artikel.activeflag = YES
    USE-INDEX depart_index NO-LOCK BY artikel.artnr: 
    CREATE art-list. 
    art-list.bezeich = artikel.bezeich. 
    art-list.artnr = artikel.artnr. 
    DO i = 1 TO 48: 
      art-list.h-our[i] = artikel.anzahl. 
    END. 
    FOR EACH bk-rart WHERE bk-rart.veran-artnr = artikel.artnr 
      USE-INDEX nr-artnr-ix NO-LOCK, 
      FIRST bk-reser WHERE bk-reser.veran-nr = bk-rart.veran-nr 
      AND bk-reser.veran-resnr = bk-rart.veran-resnr 
      AND bk-reser.datum = curr-date 
      USE-INDEX vernr-ix NO-LOCK: 
      from-i = bk-reser.von-i. 
      to-i = bk-reser.bis-i. 
      DO i = from-i TO to-i: 
        art-list.h-our[i] = art-list.h-our[i] - bk-rart.anzahl. 
      END. 
    END. 
    DO i = 1 TO 48: 
      IF art-list.h-our[i] EQ artikel.anzahl THEN art-list.astatus[i] = 15. 
      ELSE 
      DO: 
        IF art-list.h-our[i] GT 0 THEN art-list.astatus[i] = 10. 
        ELSE IF art-list.h-our[i] EQ 0 THEN art-list.astatus[i] = 14. 
        ELSE IF art-list.h-our[i] LT 0 THEN art-list.astatus[i] = 12. 
      END. 
    END. 
  END. 
END. 

