
DEF TEMP-TABLE t-guestseg          LIKE guestseg.

DEF INPUT  PARAMETER case-type     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastNo        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER segmCode      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-guestseg.

DEF VAR vipNr1 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr2 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr3 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr4 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr5 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr6 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr7 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr8 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR vipNr9 AS INTEGER INITIAL 0 NO-UNDO.

CASE case-type:
  WHEN 1 THEN
  DO:
    IF segmCode = 0 THEN
    FIND FIRST guestseg WHERE guestseg.gastnr = gastNo NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST guestseg WHERE guestseg.gastnr = gastNo
      AND guestseg.segmentcode = segmCode NO-LOCK NO-ERROR.
    IF AVAILABLE guestseg THEN
    DO:
      CREATE t-guestseg.
      BUFFER-COPY guestseg TO t-guestseg.
    END.
  END.
  WHEN 2 THEN
  DO:
    RUN get-vipNr.
    FIND FIRST guestseg WHERE guestseg.gastnr = gastNo
      AND (guestseg.segmentcode = vipNr1 OR 
      guestseg.segmentcode = vipNr2 OR 
      guestseg.segmentcode = vipNr3 OR 
      guestseg.segmentcode = vipNr4 OR 
      guestseg.segmentcode = vipNr5 OR 
      guestseg.segmentcode = vipNr6 OR 
      guestseg.segmentcode = vipNr7 OR 
      guestseg.segmentcode = vipNr8 OR 
      guestseg.segmentcode = vipNr9) NO-LOCK NO-ERROR. 
    IF AVAILABLE guestseg THEN
    DO:
      CREATE t-guestseg.
      BUFFER-COPY guestseg TO t-guestseg.
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST guestseg WHERE guestseg.gastnr = gastNo
      AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guestseg THEN
    FIND FIRST guestseg WHERE guestseg.gastnr = gastNo NO-LOCK NO-ERROR.
    IF AVAILABLE guestseg THEN
    DO:
      CREATE t-guestseg.
      BUFFER-COPY guestseg TO t-guestseg.
    END.
  END.
  WHEN 4 THEN
  FOR EACH guestseg WHERE guestseg.gastnr = gastNo NO-LOCK
    BY guestseg.segmentcode:
    CREATE t-guestseg.
    BUFFER-COPY guestseg TO t-guestseg.
  END.
  WHEN 5 THEN
  FOR EACH guestseg WHERE guestseg.gastnr = gastNo NO-LOCK,
    FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
    AND segment.betriebsnr = 4 NO-LOCK:
    CREATE t-guestseg.
    BUFFER-COPY guestseg TO t-guestseg.
    RETURN.
  END.
END CASE.

PROCEDURE get-vipNr: 
DEF VAR intOut AS INTEGER NO-UNDO.
  RUN htpint.p (700, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr1 = intOut.
  RUN htpint.p (701, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr2 = intOut.
  RUN htpint.p (702, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr3 = intOut.
  RUN htpint.p (703, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr4 = intOut.
  RUN htpint.p (704, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr5 = intOut.
  RUN htpint.p (705, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr6 = intOut.
  RUN htpint.p (706, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr7 = intOut.
  RUN htpint.p (707, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr8 = intOut.
  RUN htpint.p (708, OUTPUT intOut).
  IF intOut NE 0 THEN vipNr9 = intOut.
END. 
