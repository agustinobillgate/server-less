
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER number1        AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER success-flag   AS LOGICAL NO-UNDO INIT NO.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "room-category-admin".

FIND FIRST zimkateg WHERE zimkateg.typ = number1 NO-LOCK NO-ERROR. 
IF AVAILABLE zimkateg  THEN 
DO: 
   msg-str = msg-str + CHR(2)
           + translateExtended ("Room Type exists, deleting not possible:",lvCAREA,"")
           + " " + zimkateg.kurzbez.
END. 
ELSE 
DO: 
   FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.number1 = number1 
     EXCLUSIVE-LOCK. 
   DELETE queasy. 
   success-flag = YES.
END. 
