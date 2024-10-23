
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER location AS INT.
DEF INPUT  PARAMETER floor AS INT.
DEF INPUT  PARAMETER from-room AS CHAR.
DEF INPUT-OUTPUT  PARAMETER curr-n AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR INIT "".
DEF OUTPUT PARAMETER msg-ans AS LOGICAL INIT YES.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "check-btn-add-flplan".

FIND FIRST queasy WHERE queasy.KEY = 25 AND queasy.number1 = location 
   AND queasy.number2 = floor 
   AND queasy.char1 = from-room NO-LOCK NO-ERROR. 
IF AVAILABLE queasy THEN 
DO: 
   msg-str = msg-str + CHR(2)
           + translateExtended ("Room already assigned.",lvCAREA,"").
   msg-ans = NO.
   RETURN NO-APPLY. 
END. 
 
FIND FIRST zimmer WHERE zimmer.zinr = from-room NO-LOCK. 
IF zimmer.etage NE floor THEN 
DO: 
   msg-str = msg-str + CHR(2) + "&W"
           + translateExtended ("Room is not located on the selected floor.",lvCAREA,"").
   msg-ans = YES.
END. 
 
IF curr-n = 100 THEN 
DO: 
   msg-str = msg-str + CHR(2)
           + translateExtended ("Number rooms of 100 reached.",lvCAREA,"").
   msg-ans = NO.
   RETURN NO-APPLY. 
END. 
curr-n = curr-n + 1. 
