
DEF OUTPUT PARAMETER foot1 AS CHAR.
DEF OUTPUT PARAMETER foot2 AS CHAR.
DEF OUTPUT PARAMETER foot3 AS CHAR.

RUN fill-list.

PROCEDURE fill-list: 
  FIND FIRST paramtext WHERE txtnr = 711 NO-LOCK. 
  foot1 = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 712 NO-LOCK. 
  foot2 = paramtext.ptexte.
  FIND FIRST paramtext WHERE txtnr = 713 NO-LOCK.
  foot3 = paramtext.ptexte.
END.
