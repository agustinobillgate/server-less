DEF TEMP-TABLE t-history LIKE history.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resNo     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER reslinNo  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rmNo      AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER arrive    AS DATE    NO-UNDO.
DEF INPUT  PARAMETER depart    AS DATE    NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-history.

DEF VARIABLE ind-gastnr AS INTEGER NO-UNDO.
DEF VARIABLE wig-gastnr AS INTEGER NO-UNDO.
DEF VARIABLE i-anzahl   AS INTEGER NO-UNDO INIT 0.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST history WHERE history.gastnr = gastNo 
      AND history.resnr = resNo AND history.reslinnr = reslinNo 
      USE-INDEX res_ix NO-LOCK NO-ERROR.
    IF AVAILABLE history THEN
    DO:
      CREATE t-history.
      BUFFER-COPY history TO t-history.
    END.
  END.
  WHEN 2 THEN
  DO:
    RUN htpint.p(109, OUTPUT wig-gastnr).
    RUN htpint.p(123, OUTPUT ind-gastnr).
    FOR EACH history WHERE history.gastnr = gastNo NO-LOCK:
      CREATE t-history.
      BUFFER-COPY history TO t-history.
      IF gastno = wig-gastnr OR gastno = ind-gastnr 
          THEN i-anzahl = i-anzahl + 1.
      IF i-anzahl = 4 THEN RETURN.
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST history WHERE RECID(history) = gastNo NO-LOCK NO-ERROR.
    IF AVAILABLE history THEN
    DO:
      CREATE t-history.
      BUFFER-COPY history TO t-history.
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST history WHERE history.resnr = resNo
          AND history.reslinnr = reslinNo
          AND NUM-ENTRIES(history.bemerk, ":=") GE 2
          AND TRIM(ENTRY(2, history.bemerk, ":=")) = "=" + TRIM(rmNo) /*old reason*/
          NO-LOCK NO-ERROR.
    IF AVAILABLE history THEN
    DO:
      CREATE t-history.
      BUFFER-COPY history TO t-history.
    END.
  END.
  WHEN 5 THEN
  DO:
    FOR EACH history WHERE history.gastnr = gastNo 
        AND history.abreise LE TODAY NO-LOCK:
        CREATE t-history.
        BUFFER-COPY history TO t-history.
    END.
  END.
  WHEN 6 THEN
  DO:
    FIND FIRST history WHERE history.resnr = resNo 
        AND history.reslinnr = reslinNo
        AND history.zi-wechsel = NO
        NO-LOCK NO-ERROR.
    IF AVAILABLE history THEN
    DO:
      CREATE t-history.
      BUFFER-COPY history TO t-history.
    END.
  END.
  WHEN 7 THEN
  DO:
    FIND FIRST history WHERE history.resnr = resNo 
      AND history.reslinnr = reslinNo 
      USE-INDEX res_ix NO-LOCK NO-ERROR.
    IF AVAILABLE history THEN
    DO:
      CREATE t-history.
      BUFFER-COPY history TO t-history.
    END.
  END.
END CASE.
