

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER seg-lsegmcode AS INT.
DEF INPUT PARAMETER segmcode AS INT.
DEF INPUT PARAMETER bezeich AS CHAR.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "check-delart".

FIND FIRST guestseg WHERE guestseg.segmentcode = segmcode NO-LOCK NO-ERROR. 
IF AVAILABLE guestseg THEN 
DO: 
  DEFINE VARIABLE name AS CHAR FORMAT "x(24)". 
  FIND FIRST guest WHERE guest.gastnr = guestseg.gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE guest  THEN name = guest.name. 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Segment used by  guestname",lvCAREA,"") + " " + name.
END.
ELSE 
DO: 
  msg-str = msg-str + CHR(2) + "&Q"
          + translateExtended ("Do you really want to REMOVE the segment",lvCAREA,"")
          + CHR(10)
          + STRING(segmcode) + " - "
          + bezeich + " ?".
END. 
