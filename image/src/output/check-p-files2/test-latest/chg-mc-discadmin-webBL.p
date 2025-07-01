DEFINE TEMP-TABLE disc-list LIKE mc-disc
    FIELD depart  AS CHAR
    FIELD rec-id  AS INTEGER
    FIELD counter AS INTEGER.


DEFINE INPUT PARAMETER TABLE FOR disc-list.
DEFINE INPUT PARAMETER curr-nr AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-mode AS CHAR.

IF curr-mode = "add" THEN
DO:
  FOR EACH disc-list WHERE disc-list.nr = curr-nr NO-LOCK:
    FIND FIRST mc-disc WHERE mc-disc.nr = disc-list.nr 
       AND RECID(mc-disc) = disc-list.rec-id NO-ERROR.
    IF NOT AVAILABLE mc-disc THEN
    DO:
     CREATE mc-disc.
     BUFFER-COPY disc-list TO mc-disc.
    END.
  END.
END.

ELSE IF curr-mode = "chg" THEN
DO:
  FIND FIRST disc-list NO-LOCK NO-ERROR.
  IF AVAILABLE disc-list THEN DO:
      FIND FIRST mc-disc WHERE mc-disc.nr = curr-nr
          AND RECID(mc-disc) = disc-list.rec-id NO-LOCK NO-ERROR.
      IF AVAILABLE mc-disc THEN DO:
          FIND CURRENT mc-disc EXCLUSIVE-LOCK.
          BUFFER-COPY disc-list TO mc-disc.
          FIND CURRENT mc-disc NO-LOCK.
          RELEASE mc-disc.
      END.
  END.
END.
