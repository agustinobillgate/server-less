DEFINE INPUT PARAMETER t-l-zwkum    LIKE l-artikel.zwkum.
DEFINE INPUT PARAMETER t-l-endkum   LIKE l-artikel.endkum.
DEFINE INPUT PARAMETER t-l-artnr    LIKE l-artikel.artnr.
DEFINE INPUT PARAMETER l-zwkum      LIKE l-artikel.zwkum.
DEFINE INPUT PARAMETER l-endkum     LIKE l-artikel.endkum.
DEFINE INPUT PARAMETER l-artnr      LIKE l-artikel.artnr.
DEFINE INPUT-OUTPUT PARAMETER artnr        AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER artnr-ok    AS LOGICAL  NO-UNDO INIT NO.


RUN find-new-artnr(YES, OUTPUT artnr). 
RUN check-artno(OUTPUT artnr-ok). 

PROCEDURE find-new-artnr: 
DEFINE INPUT PARAMETER update-flag AS LOGICAL. 
DEFINE OUTPUT PARAMETER new-artnr AS INTEGER INITIAL 0. 
DEFINE buffer l-artikel1 FOR l-artikel. 
DEFINE buffer l-art1 FOR l-artikel. 
  IF l-zwkum = t-l-zwkum AND l-endkum = t-l-endkum AND NOT update-flag THEN 
  DO: 
    new-artnr = t-l-artnr. 
    RETURN. 
  END. 
  FOR EACH l-art1 WHERE l-art1.zwkum = l-zwkum 
    AND l-art1.endkum = l-endkum NO-LOCK BY l-art1.artnr descending: 
    IF l-art1.zwkum LE 99 
      AND SUBSTR(STRING(l-art1.artnr),2,2) EQ STRING(l-art1.zwkum,"99") 
      AND SUBSTR(STRING(l-art1.artnr),1,1) EQ STRING(l-art1.endkum,"9") THEN 
    DO: 
      new-artnr = l-art1.artnr + 1. 
      RETURN. 
    END. 
    ELSE IF l-art1.zwkum GE 100 
      AND SUBSTR(STRING(l-art1.artnr),2,3) EQ STRING(l-art1.zwkum,"999") 
      AND SUBSTR(STRING(l-art1.artnr),1,1) EQ STRING(l-art1.endkum,"9") THEN 
    DO: 
      new-artnr = l-art1.artnr + 1. 
      RETURN. 
    END. 
  END. 
  IF l-zwkum LE 99 THEN 
    new-artnr = l-endkum * 1000000 + l-zwkum * 10000 + 1. 
  ELSE IF l-zwkum GE 100 THEN 
    new-artnr = l-endkum * 1000000 + l-zwkum * 1000 + 1. 
  FIND FIRST l-artikel1 WHERE l-artikel1.artnr = new-artnr NO-LOCK NO-ERROR. 
  IF AVAILABLE l-artikel1 THEN new-artnr = 0. 
END.   

PROCEDURE check-artno: 
DEFINE OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 
DEFINE VARIABLE nr AS INTEGER. 
DEFINE VARIABLE s AS CHAR. 
  IF l-zwkum GT 99 THEN nr = l-endkum * 1000 + l-zwkum. 
  ELSE nr = l-endkum * 100 + l-zwkum. 
  IF nr GT 999 THEN s = SUBSTR(STRING(l-artnr),1,4). 
  ELSE s = SUBSTR(STRING(l-artnr),1,3). 
  its-ok = (s = STRING(nr)). 
END. 
 
