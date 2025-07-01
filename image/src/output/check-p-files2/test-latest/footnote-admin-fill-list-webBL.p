
DEF OUTPUT PARAMETER foot1 AS CHAR.
DEF OUTPUT PARAMETER foot2 AS CHAR.
DEF OUTPUT PARAMETER foot3 AS CHAR.

RUN fill-list.

/* Rulita 300125 | Fixing Serverless Issue git 323 */
PROCEDURE fill-list: 
  FIND FIRST paramtext WHERE txtnr = 711 NO-LOCK NO-ERROR. 
  IF AVAILABLE paramtext THEN
  DO:
    foot1 = paramtext.ptexte. 
  END.
  FIND FIRST paramtext WHERE txtnr = 712 NO-LOCK NO-ERROR.
  IF AVAILABLE paramtext THEN
  DO:
    foot2 = paramtext.ptexte.
  END.
  FIND FIRST paramtext WHERE txtnr = 713 NO-LOCK NO-ERROR.
  IF AVAILABLE paramtext THEN
  DO:
    foot3 = paramtext.ptexte.
  END.
END.
/* End Rulita */
