
DEF TEMP-TABLE t-nation       LIKE nation.
DEF INPUT  PARAMETER natNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER natBez   AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER natName  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-nation.

/* for loading each nation please refer to load-nationBL.p */
IF natNo GT 0 THEN
FIND FIRST nation WHERE nation.nationnr = natNo NO-LOCK NO-ERROR.

ELSE IF natBez NE "" THEN
FIND FIRST nation WHERE nation.kurzbez = natBez NO-LOCK NO-ERROR.

ELSE IF natBez NE "" AND natName EQ "1" THEN
FIND FIRST nation WHERE nation.kurzbez = natBez 
    AND nation.natcode > 0 NO-LOCK NO-ERROR.    /* Local Region */

ELSE IF natBez = "" AND natName NE "" THEN
FIND FIRST nation WHERE nation.bezeich = natName NO-LOCK NO-ERROR.

IF AVAILABLE nation THEN
DO:
  CREATE t-nation.
  BUFFER-COPY nation TO t-nation.
END.

