/*FD Oct 27, 2020 => BL for vhp web*/
DEF TEMP-TABLE g-list
    FIELD rcode AS CHAR FORMAT "x(45)"
.

DEFINE INPUT PARAMETER inpChar3 AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR g-list.

RUN fill-list.

PROCEDURE fill-list: 
  DEF VAR tokcounter AS INTEGER NO-UNDO.
  DEF VAR mesValue   AS CHAR    NO-UNDO.
  DEF VAR ct         AS CHAR    NO-UNDO.

  IF inpChar3 MATCHES("*;*") THEN ct = ENTRY(2, inpChar3,";").
  ELSE ct = inpChar3.

  DO tokcounter = 1 TO NUM-ENTRIES(ct, ","):
    mesValue = ENTRY(tokcounter, ct, ",").
    IF mesValue NE "" THEN
    DO:
      CREATE g-list.
      ASSIGN g-list.rcode  = mesValue.
    END.
  END.
END.
