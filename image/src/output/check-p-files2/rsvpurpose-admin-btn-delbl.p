
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER number1        AS INT.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER success-flag   AS LOGICAL INIT NO.

DEF VARIABLE search-str AS CHAR NO-UNDO INIT "segm_pur".

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "rsvpurpose-admin".

ASSIGN search-str = "segm_pur" + STRING(number1) + ";".

FIND FIRST res-line WHERE res-line.active-flag LE 1 
    AND INDEX(res-line.zimmer-wunsch, search-str) GT 0 NO-LOCK NO-ERROR.
IF AVAILABLE res-line  THEN 
DO: 
   msg-str = msg-str + CHR(2)
           + translateExtended ("Reservation exists, deleting not possible.",lvCAREA,"").
END. 
ELSE 
DO: 
   FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.number1 = number1 
      EXCLUSIVE-LOCK. 
   DELETE queasy. 
   success-flag = YES.
   /*MTb1:DELETE-CURRENT-ROW( ). 
   IF AVAILABLE queasy THEN 
   DO: 
      selected = YES. 
      RUN fill-g-list. 
      RUN disp-g-list. 
   END. 
   ELSE 
   DO: 
     selected = NO. 
     RUN init-g-list. 
     RUN disp-g-list. 
   END. */
END. 
