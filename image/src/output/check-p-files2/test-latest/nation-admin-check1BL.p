
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rec-id AS INT.
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
  AND nation.natcode = 0 AND RECID(nation) NE rec-id
  NO-LOCK NO-ERROR. 
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
    FIND FIRST nation WHERE RECID(nation) = rec-id NO-ERROR.
    IF nation.kurzbez NE kurzbez THEN 
          RUN update-nationcode.
    FIND CURRENT nation EXCLUSIVE-LOCK.
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

PROCEDURE update-nationcode:
DEF VARIABLE curr-gastnr AS INTEGER INITIAL 0 NO-UNDO.
DEF BUFFER gbuff FOR guest.
  FIND FIRST guest WHERE (guest.gastnr GT curr-gastnr) AND 
    ((guest.nation1 = nation.kurzbez) OR (guest.land = nation.kurzbez)) 
    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE guest:
    DO TRANSACTION:
      curr-gastnr = guest.gastnr.
      FIND FIRST gbuff WHERE RECID(gbuff) =  RECID(guest) EXCLUSIVE-LOCK.
      IF guest.nation1 = nation.kurzbez THEN gbuff.nation1 = kurzbez.
      IF guest.land = nation.kurzbez THEN gbuff.land = kurzbez.
      FIND CURRENT gbuff NO-LOCK.
      RELEASE gbuff.
    END.
    FIND NEXT guest WHERE (guest.gastnr GT curr-gastnr) AND 
      ((guest.nation1 = nation.kurzbez) OR (guest.land = nation.kurzbez)) 
      USE-INDEX gastnr_index NO-LOCK NO-ERROR.
  END.
  FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK.
  IF htparam.fchar = nation.kurzbez THEN
  DO TRANSACTION:
      FIND CURRENT htparam EXCLUSIVE-LOCK.
      ASSIGN htparam.fchar = kurzbez.
      FIND CURRENT htparam NO-LOCK.
  END.
  FIND FIRST htparam WHERE htparam.paramnr = 276 NO-LOCK.
  IF htparam.fchar = nation.kurzbez THEN
  DO TRANSACTION:
      FIND CURRENT htparam EXCLUSIVE-LOCK.
      ASSIGN htparam.fchar = kurzbez.
      FIND CURRENT htparam NO-LOCK.
  END.
END.
