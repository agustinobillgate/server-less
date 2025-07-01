
DEF TEMP-TABLE g-list
    FIELD gastnr AS INTEGER
    FIELD gname AS CHAR FORMAT "x(48)"
.

DEF INPUT PARAMETER gastno         AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER inp-kontcode   AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR g-list.

RUN fill-list.

PROCEDURE fill-list: 
  DEF VAR tokcounter AS INTEGER NO-UNDO.
  DEF VAR mesValue   AS CHAR    NO-UNDO.
  FIND FIRST queasy WHERE queasy.KEY = 147
    AND queasy.number1 = gastno
    AND queasy.char1   = inp-kontcode NO-LOCK NO-ERROR.
  
  IF AVAILABLE queasy THEN
  DO tokcounter = 1 TO NUM-ENTRIES(queasy.char3, ","):
    mesValue = ENTRY(tokcounter, queasy.char3, ",").
    IF mesValue NE "" THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = INTEGER(mesValue)
          NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
      DO:
          CREATE g-list.
          ASSIGN
              g-list.gastnr = guest.gastnr
              g-list.gname  = guest.NAME + ", " + guest.anredefirma
                            + guest.vorname1
          .
      END.
    END.
  END.

END.
