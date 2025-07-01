
DEF INPUT PARAMETER all-flag AS LOGICAL.
DEF INPUT PARAMETER dept1 AS INT.
DEF OUTPUT PARAMETER art1 AS INT.
DEF OUTPUT PARAMETER art2 AS INT.
DEF OUTPUT PARAMETER bezeich1 AS CHAR.
DEF OUTPUT PARAMETER bezeich2 AS CHAR.

IF NOT all-flag THEN RUN find-artnr. 
ELSE RUN find-artnr1. 

/***************************** PROCEDURES *************************************/
PROCEDURE find-artnr:
  art1 = 999999. 
  art2 = 0. 
  FOR EACH h-artikel WHERE h-artikel.departement = dept1 
    AND h-artikel.activeflag AND h-artikel.artart = 0 NO-LOCK: 
    IF art1 GT h-artikel.artnr THEN art1 = h-artikel.artnr. 
    IF art2 LT h-artikel.artnr THEN art2 = h-artikel.artnr. 
  END. 
  bezeich1 = "". 
  bezeich2 = "". 
  FIND FIRST h-artikel WHERE h-artikel.artnr = art1 
    AND h-artikel.departement = dept1 NO-LOCK NO-ERROR. 
  IF AVAILABLE h-artikel THEN bezeich1 = h-artikel.bezeich. 
  FIND FIRST h-artikel WHERE h-artikel.artnr = art2 
    AND h-artikel.departement = dept1 NO-LOCK NO-ERROR. 
  IF AVAILABLE h-artikel THEN bezeich2 = h-artikel.bezeich. 
  /*MTDISP art1 art2 bezeich1 bezeich2 WITH FRAME frame1. */
END. 
 
PROCEDURE find-artnr1: 
  art1 = 999999. 
  art2 = 0. 
  FOR EACH h-artikel WHERE h-artikel.departement = dept1 
    AND h-artikel.activeflag NO-LOCK: 
    IF art1 GT h-artikel.artnr THEN art1 = h-artikel.artnr. 
    IF art2 LT h-artikel.artnr THEN art2 = h-artikel.artnr. 
  END. 
  bezeich1 = "". 
  bezeich2 = "". 
  FIND FIRST h-artikel WHERE h-artikel.artnr = art1 
    AND h-artikel.departement = dept1 NO-LOCK NO-ERROR. 
  IF AVAILABLE h-artikel THEN bezeich1 = h-artikel.bezeich. 
  FIND FIRST h-artikel WHERE h-artikel.artnr = art2 
    AND h-artikel.departement = dept1 NO-LOCK NO-ERROR. 
  IF AVAILABLE h-artikel THEN bezeich2 = h-artikel.bezeich. 
  /*MTDISP art1 art2 bezeich1 bezeich2 WITH FRAME frame1. */
END.
