DEF TEMP-TABLE segment-a
    FIELD bezeich LIKE segment.bezeich.

DEF INPUT PARAMETER gastnr AS INT.
DEF OUTPUT PARAMETER mainsegm AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR segment-a.

FOR EACH guestseg WHERE guestseg.gastnr = gastnr NO-LOCK:
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
        NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
        CREATE segment-a.
        ASSIGN segment-a.bezeich = segment.bezeich.
    END.
END. 

FIND FIRST guestseg WHERE guestseg.gastnr = gastnr AND guestseg.reihenfolge = 1 
    NO-LOCK NO-ERROR.
IF AVAILABLE guestseg THEN 
DO: 
  FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
      NO-LOCK NO-ERROR. 
  IF AVAILABLE segment THEN mainsegm = ENTRY(1, segment.bezeich, "$$0"). 
END. 
