

DEFINE INPUT-OUTPUT PARAMETER gnat AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER gland AS CHAR.
DEFINE INPUT PARAMETER def-natcode AS CHAR.
DEFINE INPUT PARAMETER gastID AS CHAR.
DEFINE INPUT PARAMETER name AS CHAR.
DEFINE INPUT PARAMETER fname AS CHAR.
DEFINE INPUT PARAMETER ftitle AS CHAR.
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER gphone AS CHAR.
DEFINE INPUT PARAMETER gastno AS INTEGER.

DEFINE INPUT-OUTPUT PARAMETER selected-gastnr AS INT.

RUN create-gcf.

PROCEDURE create-gcf: 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE del-gastnr AS INTEGER. 
DEFINE BUFFER gastsegm FOR guestseg.
  /*FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR. FT serverless*/

  curr-gastnr = 0.
  FIND FIRST guest WHERE guest.gastnr < 0 NO-ERROR. 
  IF AVAILABLE guest THEN 
  DO: 
    curr-gastnr = - guest.gastnr. 
    DELETE guest. 
    FIND FIRST guest WHERE guest.gastnr = curr-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN curr-gastnr = 0.
  END. 
  IF curr-gastnr = 0 THEN
  DO: 
    FIND LAST guest NO-LOCK NO-ERROR. 
    IF AVAILABLE guest THEN curr-gastnr = guest.gastnr + 1. 
    ELSE curr-gastnr = 1. 
  END. 
  IF gnat  = "" THEN gnat  = def-natcode.
  IF gland = "" THEN gland = def-natcode.
  CREATE guest. 
  ASSIGN
    guest.gastnr = curr-gastnr 
    selected-gastnr = guest.gastnr 
    guest.karteityp = 0
    guest.ausweis-nr1 = gastID
    guest.nation1 = gnat
    guest.land = gland
    guest.name = name
    guest.vorname1 = fname 
    guest.anrede1 = ftitle 
    guest.char1 = user-init
    guest.telefon = gphone
  . 
  FIND CURRENT guest NO-LOCK. 
 
  FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr
      AND guestseg.reihenfolge = 1 EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE guestseg THEN
  DO:
    CREATE guestseg. 
    ASSIGN
      guestseg.gastnr = guest.gastnr
      guestseg.reihenfolge = 1
   . 
  END.

  /*IF AVAILABLE reservation AND reservation.segmentcode NE 0 THEN 
    guestseg.segmentcode = reservation.segmentcode. 
  ELSE FT serverless*/
  DO:
    FIND FIRST gastsegm WHERE gastsegm.gastnr = /*MTgastno*/ guest.gastnr
      AND gastsegm.reihenfolge = 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gastsegm THEN
    FIND FIRST gastsegm WHERE gastsegm.gastnr = /*MTgastno*/ guest.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE gastsegm THEN 
        ASSIGN guestseg.segmentcode = gastsegm.segmentcode.
    ELSE 
    DO: 
      FIND FIRST segment NO-LOCK NO-ERROR. 
      IF AVAILABLE segment THEN
        guestseg.segmentcode = segment.segmentcode. 
    END.
  END.
  FIND CURRENT guestseg NO-LOCK.
  RELEASE guestseg. 
END. 
