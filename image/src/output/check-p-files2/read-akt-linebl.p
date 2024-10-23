DEFINE TEMP-TABLE t-akt-line LIKE akt-line.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER lineNr    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER datum     AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER usrinit   AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-akt-line.

CASE case-type:
  WHEN 1 THEN
  DO:
      FIND FIRST akt-line WHERE akt-line.linenr = lineNr NO-LOCK NO-ERROR.
      IF AVAILABLE akt-line THEN
      DO :
          CREATE t-akt-line.
          BUFFER-COPY akt-line TO t-akt-line.
      END.
  END.
  WHEN 2 THEN
  DO:
      FIND FIRST akt-line WHERE akt-line.linenr = lineNr EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE akt-line THEN
      DO :
          CREATE t-akt-line.
          BUFFER-COPY akt-line TO t-akt-line.
      END.
  END.
  WHEN 3 THEN
  DO:
      FIND FIRST akt-line WHERE akt-line.userinit = usrinit
          AND akt-line.datum GE (datum - 1) AND akt-line.datum LE datum
          NO-LOCK NO-ERROR.
      DO :
          CREATE t-akt-line.
          BUFFER-COPY akt-line TO t-akt-line.
      END.
  END.
END CASE.
