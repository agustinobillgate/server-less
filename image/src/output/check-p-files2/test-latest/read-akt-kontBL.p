
DEF TEMP-TABLE t-akt-kont LIKE akt-kont.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER gastNo     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER userNo     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER gname      AS CHAR     NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-akt-kont.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo 
      AND akt-kont.kontakt-nr = userNo NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
      CREATE t-akt-kont.
      BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
    WHEN 2 THEN
    DO:
      FOR EACH akt-kont WHERE akt-kont.gastnr = gastNo 
        AND akt-kont.kontakt-nr GE 1
        USE-INDEX kontakt-ix NO-LOCK BY akt-kont.NAME:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
      END.
    END.
  WHEN 3 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo 
      AND akt-kont.hauptkontakt = NO USE-INDEX kontakt-ix NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
      CREATE t-akt-kont.
      BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo 
      AND akt-kont.hauptkontakt = YES USE-INDEX kontakt-ix NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
      CREATE t-akt-kont.
      BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
  WHEN 5 THEN
  DO:
    FOR EACH akt-kont WHERE akt-kont.gastnr = gastNo 
        AND akt-kont.kontakt-nr GT 0 AND akt-kont.name GE gname
        NO-LOCK BY akt-kont.NAME:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
  WHEN 6 THEN
  DO:
    FOR EACH akt-kont WHERE akt-kont.gastnr = gastNo 
        NO-LOCK:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
  WHEN 7 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo AND akt-kont.NAME = gname
        OR (akt-kont.name + ", " + akt-kont.anrede) = gname NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-kont THEN
    DO:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo
          AND akt-kont.name = gname NO-LOCK NO-ERROR. 
      IF AVAILABLE akt-kont THEN
      DO:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
      END.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo
          AND gname MATCHES ("*" + akt-kont.NAME + "*")
          AND gname MATCHES ("*" + akt-kont.vorname + "*")
          NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE akt-kont THEN
          FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo
              AND gname MATCHES ("*" + akt-kont.NAME + "*") 
              NO-LOCK NO-ERROR.
          IF AVAILABLE akt-kont THEN
          DO:
              CREATE t-akt-kont.
              BUFFER-COPY akt-kont TO t-akt-kont.
          END.
  END.
  WHEN 10 THEN
  DO:
      FIND FIRST akt-kont WHERE akt-kont.betrieb-gast = gastNo NO-ERROR. 
      IF AVAILABLE akt-kont THEN
      DO:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
      END.
  END.
  WHEN 11 THEN
  DO:
      FOR EACH akt-kont WHERE akt-kont.betrieb-gast = gastNo NO-LOCK:
        CREATE t-akt-kont.
        BUFFER-COPY akt-kont TO t-akt-kont.
      END.
  END.
  WHEN 12 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo 
      AND SUBSTR(akt-kont.abteilung, 1, 3) = gname NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
      CREATE t-akt-kont.
      BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.
  WHEN 13 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = gastNo NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
      CREATE t-akt-kont.
      BUFFER-COPY akt-kont TO t-akt-kont.
    END.
  END.

END CASE.
