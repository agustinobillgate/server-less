DEF INPUT PARAMETER gastno          AS INTEGER NO-UNDO.
DEF INPUT PARAMETER selected-gastnr AS INTEGER.
DEF INPUT PARAMETER user-init       AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER def-natcode    AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER gastID         AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER gname          AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER gnat           AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER gland          AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER gphone         AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER bdate-flag     AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER search-start   AS INTEGER NO-UNDO.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
 
FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK. 
FIND FIRST nation WHERE nation.kurzbez = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE nation THEN def-natcode = nation.kurzbez. 

IF gastno GT 0 THEN
DO:
  FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK NO-ERROR.
  IF AVAILABLE guest THEN 
  DO:
    IF guest.nation1 NE "" THEN def-natcode = guest.nation1.
    ELSE IF guest.land NE "" THEN def-natcode = guest.land.
  END.
END.

RUN create-list. 
RUN htplogic.p (937, OUTPUT bdate-flag).
RUN htpint.p (968, OUTPUT search-start).

PROCEDURE create-list: 
  FIND FIRST guest WHERE guest.gastnr = selected-gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN
  DO:
    ASSIGN
      gastID = guest.ausweis-nr1
      gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1
      gnat  = guest.nation1
      gland = guest.land
    .
    IF AVAILABLE guest AND guest.karteityp = 0 THEN gphone = guest.telefon.
  END.
END. 
