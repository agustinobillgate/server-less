
DEF INPUT-OUTPUT PARAMETER zknr1 AS INT.
DEF INPUT-OUTPUT PARAMETER zknr2 AS INT.
DEF INPUT-OUTPUT PARAMETER zknr3 AS INT.
DEF INPUT-OUTPUT PARAMETER zknr4 AS INT.
DEF INPUT-OUTPUT PARAMETER zknr5 AS INT.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER ldry-dept AS INT.
DEF OUTPUT PARAMETER ekumnr AS INT.
DEF OUTPUT PARAMETER bezeich1 AS CHAR FORMAT "x(12)". 
DEF OUTPUT PARAMETER bezeich2 AS CHAR FORMAT "x(12)". 
DEF OUTPUT PARAMETER bezeich3 AS CHAR FORMAT "x(12)". 
DEF OUTPUT PARAMETER bezeich4 AS CHAR FORMAT "x(12)". 
DEF OUTPUT PARAMETER bezeich5 AS CHAR FORMAT "x(12)". 
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 1081 no-lock.  /* Laundry Dept*/ 
ldry-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
RUN get-zknr. 
FIND FIRST htparam WHERE paramnr = 555 NO-LOCK. 
ekumnr = htparam.finteger. 


PROCEDURE get-zknr: 
  FOR EACH h-artikel WHERE h-artikel.departement = ldry-dept 
      AND h-artikel.artart = 0 AND h-artikel.artnr GT 0
      NO-LOCK BY h-artikel.zwkum: 
    IF zknr1 = 0 THEN 
    DO: 
      zknr1 = h-artikel.zwkum. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = ldry-dept 
        AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
      bezeich1 = wgrpdep.bezeich. 
      /*MTASSIGN s-list.amount[1]:LABEL IN BROWSE b1 = wgrpdep.bezeich.*/
      flag = 1.
    END. 
 
    ELSE IF h-artikel.zwkum NE zknr1 AND zknr2 = 0 THEN 
    DO: 
      zknr2 = h-artikel.zwkum. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = ldry-dept 
        AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
      bezeich2 = wgrpdep.bezeich. 
      /*MTASSIGN s-list.amount[2]:LABEL IN BROWSE b1 = wgrpdep.bezeich. */
      flag = 2.
    END. 
 
    ELSE IF h-artikel.zwkum NE zknr1 
      AND h-artikel.zwkum NE zknr2 AND zknr3 = 0 THEN 
    DO: 
      zknr3 = h-artikel.zwkum. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = ldry-dept 
        AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
      bezeich3 = wgrpdep.bezeich. 
      /*MTASSIGN s-list.amount[3]:LABEL IN BROWSE b1 = wgrpdep.bezeich. */
      flag = 3.
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 
      AND h-artikel.zwkum NE zknr2 
      AND h-artikel.zwkum NE zknr3 
      AND zknr4 = 0 THEN 
    DO: 
      zknr4 = h-artikel.zwkum. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = ldry-dept 
        AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
      bezeich4 = wgrpdep.bezeich. 
      /*MTASSIGN s-list.amount[4]:LABEL IN BROWSE b1 = wgrpdep.bezeich. */
      flag = 4.
    END. 
    ELSE IF h-artikel.zwkum NE zknr1 
      AND h-artikel.zwkum NE zknr2 
      AND h-artikel.zwkum NE zknr3 
      AND h-artikel.zwkum NE zknr4 
      AND zknr5 = 0 THEN 
    DO: 
      zknr5 = h-artikel.zwkum. 
      FIND FIRST wgrpdep WHERE wgrpdep.departement = ldry-dept 
        AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK. 
      bezeich5 = wgrpdep.bezeich. 
      /*MTASSIGN s-list.amount[5]:LABEL IN BROWSE b1 = wgrpdep.bezeich. */
      flag = 5.
    END. 
  END. 
END. 
