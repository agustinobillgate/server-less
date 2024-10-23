
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER kurzbez AS CHAR.
DEF INPUT  PARAMETER natcode AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "subnation-admin-check".

FIND FIRST nation WHERE nation.kurzbez = kurzbez
      AND nation.natcode = natcode NO-LOCK NO-ERROR. 
IF AVAILABLE nation AND kurzbez NE "" THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Region Code already exists, use other code.",lvCAREA,"").
  RETURN NO-APPLY. 
END. 
 
FIND FIRST nation WHERE nation.kurzbez = kurzbez 
  AND nation.natcode = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE nation AND kurzbez NE "" THEN 
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Region Code used for a Nation Code, use other code.",lvCAREA,"").
  RETURN NO-APPLY. 
END. 
