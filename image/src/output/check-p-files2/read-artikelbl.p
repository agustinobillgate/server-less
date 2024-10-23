DEF TEMP-TABLE t-artikel LIKE artikel.

DEF INPUT  PARAMETER artNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER aName   AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

IF artNo NE 0 THEN
FIND FIRST artikel WHERE artikel.artnr = artNo 
  AND artikel.departement = dept NO-LOCK NO-ERROR.

ELSE IF aName NE "" THEN
FIND FIRST artikel WHERE artikel.bezeich = aName 
  AND artikel.departement = dept NO-LOCK NO-ERROR.

IF AVAILABLE artikel THEN
DO:
  CREATE t-artikel.
  BUFFER-COPY artikel TO t-artikel.
END.
