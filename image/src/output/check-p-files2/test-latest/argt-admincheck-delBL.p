

DEF INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER argtnr AS INT.
DEF INPUT PARAMETER arrangement AS CHAR.

DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "argt-admin-check-del".

DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
DEFINE VARIABLE i AS INTEGER.

FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
  AND reslin-queasy.number2 = argtnr NO-LOCK NO-ERROR. 
IF AVAILABLE reslin-queasy THEN 
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended( "Deleting no possible, arrangement defined in price code : ", 
            lvCAREA, "":U) + reslin-queasy.char1.
  RETURN NO-APPLY. 
END.

FIND FIRST res-line WHERE res-line.arrangement = arrangement NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended( "Reservation exists, deleting not possible.", lvCAREA, "":U).
  RETURN NO-APPLY. 
END.

FIND FIRST prtable NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE prtable AND NOT found: 
  DO i = 1 TO 99: 
      IF prtable.argtnr[i] = argtnr THEN found = YES. 
  END. 
  FIND NEXT prtable NO-LOCK NO-ERROR. 
END. 
IF found THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended( "Price Market Table exists, deleting not possible.", 
      lvCAREA, "":U).
  RETURN NO-APPLY. 
END.
