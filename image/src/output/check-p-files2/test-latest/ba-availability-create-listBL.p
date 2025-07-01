DEFINE TEMP-TABLE art-list 
  FIELD artnr AS INTEGER FORMAT ">>9" LABEL "Art" FONT 2 
  FIELD bezeich AS CHAR FORMAT "x(32)" LABEL "Article Description" FONT 2 
  FIELD h-our AS INTEGER EXTENT 48 FORMAT "-99" FONT 2 
  FIELD astatus AS INTEGER EXTENT 48. 

DEFINE TEMP-TABLE r-list LIKE bk-rart. 

DEFINE TEMP-TABLE q3-list LIKE r-list
    FIELD uhrzeit           LIKE bk-func.uhrzeit
    FIELD raeume            LIKE bk-func.raeume[1]
    FIELD bestellt_durch    LIKE bk-func.bestellt_durch.

DEF INPUT PARAMETER ba-dept AS INT.
DEF INPUT PARAMETER z-zknr AS INT.
DEF INPUT PARAMETER curr-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR art-list.
DEF OUTPUT PARAMETER TABLE FOR q3-list.

RUN create-list.
FOR EACH r-list NO-LOCK BY r-list.raum: 
    FIND FIRST bk-func WHERE bk-func.veran-nr = r-list.veran-nr 
    AND bk-func.veran-seite = r-list.veran-seite NO-LOCK NO-ERROR. 
    /*BY bk-func.uhrzeit BY r-list.raum:FT serverless*/
    IF AVAILABLE bk-func THEN
    DO:
        CREATE q3-list.
        ASSIGN
            q3-list.uhrzeit           = bk-func.uhrzeit
            q3-list.raeume            = bk-func.raeume[1]
            q3-list.bestellt_durch    = bk-func.bestellt_durch.
    END.
END.

PROCEDURE create-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE from-i AS INTEGER. 
DEFINE VARIABLE to-i AS INTEGER. 
 
  FOR EACH art-list: 
    DELETE art-list. 
  END. 
  FOR EACH r-list: 
    DELETE r-list. 
  END. 
 
  FOR EACH artikel WHERE artikel.departement = ba-dept 
    AND artikel.zwkum = z-zknr USE-INDEX depart_index NO-LOCK: 
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
      AND bk-rese.resstatus = 1 AND bk-reser.datum = curr-date 
      USE-INDEX vernr-ix NO-LOCK: 
      FIND FIRST r-list WHERE r-list.veran-artnr = bk-rart.veran-artnr 
        AND r-list.veran-nr = bk-rart.veran-nr 
        AND r-list.veran-resnr = bk-rart.veran-resnr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE r-list THEN 
      DO: 
        CREATE r-list. 
        BUFFER-COPY bk-rart TO r-list. 
      END. 
      ELSE r-list.anzahl = r-list.anzahl + bk-rart.anzahl. 
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
