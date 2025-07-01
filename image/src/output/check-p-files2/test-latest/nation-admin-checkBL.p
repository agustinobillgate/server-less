
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kurzbez AS CHAR.

DEF INPUT PARAMETER nationnr AS INT.
DEF INPUT PARAMETER natbez AS CHAR.
DEF INPUT PARAMETER untergruppe AS INT.
DEF INPUT PARAMETER hauptgruppe AS INT.
DEF INPUT PARAMETER language AS INT.
DEF INPUT PARAMETER marksegm AS CHAR.

DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "nation-admin-check".

FIND FIRST nation WHERE nation.kurzbez = kurzbez 
  AND nation.natcode = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE nation AND kurzbez NE "" THEN 
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Nation code already exists, use other code.",lvCAREA,"").
  RETURN NO-APPLY.
END.

FIND FIRST nation WHERE nation.kurzbez = kurzbez 
   AND nation.natcode > 0 NO-LOCK NO-ERROR. 
IF AVAILABLE nation AND kurzbez NE "" THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("nation code used for a region code, use other code.",lvCAREA,"").
  RETURN NO-APPLY. 
END.

IF msg-str EQ "" THEN
DO :
    CREATE nation.
    RUN fill-new-nation.
END.


PROCEDURE fill-new-nation:
  nation.nationnr = nationnr. 
  nation.kurzbez = kurzbez. 
  nation.bezeich = natbez . 
  nation.untergruppe= untergruppe.
  nation.hauptgruppe = hauptgruppe. 
  nation.language = language.

  FIND FIRST prmarket WHERE prmarket.bezeich = marksegm NO-LOCK NO-ERROR.
  IF AVAILABLE prmarket THEN
      nation.bezeich = nation.bezeich + ";" + STRING(prmarket.nr).
END.
