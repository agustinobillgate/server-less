DEF TEMP-TABLE t-kontline LIKE kontline.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kontigNr  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER konstat   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER gastNo    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kontcode  AS CHAR    NO-UNDO.
DEF INPUT PARAMETER datum     AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-kontline.

DEF VAR curr-kontig AS INTEGER NO-UNDO.
IF kontignr LT 0 THEN curr-kontig = - kontignr.
ELSE curr-kontig = kontignr.

CASE case-type:
  WHEN 1 THEN
  FIND FIRST kontline WHERE kontline.kontignr = curr-kontig 
    AND kontline.kontstatus = konstat NO-LOCK NO-ERROR. 
  WHEN 2 THEN
  FIND FIRST kontline WHERE kontline.gastnr = gastNo
    AND kontline.kontcode = kontcode AND kontline.kontstatus = konstat 
    AND datum GE kontline.ankunft AND datum LE kontline.abreise 
    NO-LOCK NO-ERROR. 
  WHEN 3 THEN
  FIND FIRST kontline WHERE kontline.kontignr = curr-kontig 
    AND kontline.kontcode = kontcode AND kontline.kontstatus = konstat 
    NO-LOCK NO-ERROR. 
  WHEN 4 THEN
  FIND FIRST kontline WHERE kontline.gastnr = gastNo
    AND kontline.kontignr = curr-kontig AND kontline.kontstatus = konstat 
    NO-LOCK NO-ERROR. 
  WHEN 5 THEN
  FIND FIRST kontline WHERE kontline.kontignr = curr-kontig 
    AND kontline.kontcode = kontcode AND kontline.kontstatus = konstat 
    NO-LOCK NO-ERROR. 
  WHEN 6 THEN
  DO:
    IF curr-kontig NE 0 AND curr-kontig NE ? THEN
    FIND FIRST kontline WHERE kontline.gastnr = gastNo
      AND kontline.kontignr = curr-kontig 
      AND kontline.kontstatus = konstat 
      AND kontline.betriebsnr = 1 NO-LOCK NO-ERROR. 
    ELSE
    FIND FIRST kontline WHERE kontline.gastnr = gastNo
      AND kontline.kontignr > 0 AND kontline.kontstatus = konstat 
      AND kontline.betriebsnr = 1 NO-LOCK NO-ERROR. 
  END.
  WHEN 7 THEN
  DO:
    IF curr-kontig NE 0 AND curr-kontig NE ? THEN
    FIND FIRST kontline WHERE kontline.gastnr = gastNo
      AND kontline.kontignr = curr-kontig 
      AND kontline.kontstatus = konstat 
      AND kontline.betriebsnr = 0 NO-LOCK NO-ERROR. 
    ELSE
    FIND FIRST kontline WHERE kontline.gastnr = gastNo
      AND kontline.kontignr > 0 AND kontline.kontstatus = konstat 
      AND kontline.betriebsnr = 0 NO-LOCK NO-ERROR. 
  END.
  WHEN 8 THEN
      FIND FIRST kontline WHERE kontline.kontcode = kontcode 
        AND kontline.betriebsnr = 0 
        AND kontline.gastnr NE gastNo
        AND kontline.gastnr GT 0 
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
  WHEN 9 THEN
      FIND FIRST kontline WHERE kontline.kontcode = kontcode 
        AND kontline.gastnr = gastNo NO-LOCK NO-ERROR.
  WHEN 10 THEN
      FIND FIRST kontline WHERE kontline.kontignr = kontigNr 
        AND kontline.gastnr = gastNo NO-LOCK NO-ERROR.
  WHEN 11 THEN
      FIND FIRST kontline WHERE kontline.gastnr = gastNo
        AND kontline.kontignr = kontigNr
        AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
  WHEN 12 THEN
      FIND FIRST kontline WHERE kontline.gastnr = gastNo
        AND kontline.kontignr = kontigNr
        AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
  WHEN 13 THEN
      FIND FIRST kontline WHERE kontline.gastnr = gastNo
        AND kontline.betriebsnr = 1
        AND kontline.kontcode = kontcode
        AND kontline.kontignr NE kontigNr
        AND kontline.zikatnr NE  konstat
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
  WHEN 14 THEN
      FIND FIRST kontline WHERE kontline.kontcode = kontcode 
        AND kontline.betriebsnr = 1
        AND kontline.gastnr NE gastNo
        AND kontline.gastnr GT 0 
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
END CASE.

IF AVAILABLE kontline THEN
DO:
  CREATE t-kontline.
  BUFFER-COPY kontline TO t-kontline.
END.
