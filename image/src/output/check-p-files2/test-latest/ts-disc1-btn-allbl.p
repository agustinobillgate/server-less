


DEF INPUT PARAMETER menu-artnr          AS INT.
DEF INPUT PARAMETER menu-departement    AS INT.
DEF INPUT PARAMETER food-flag           AS LOGICAL.
DEF INPUT PARAMETER bev-flag            AS LOGICAL.
DEF INPUT PARAMETER other-flag          AS LOGICAL.

DEF OUTPUT PARAMETER menu-prtflag       AS INT.
DEF OUTPUT PARAMETER menu-bcol          AS INT INIT 1.

DEFINE BUFFER h-art FOR vhp.h-artikel. 
DEFINE BUFFER f-art FOR vhp.artikel. 

FIND FIRST h-art WHERE h-art.artnr = menu-artnr 
  AND h-art.departement = menu-departement NO-LOCK NO-ERROR. 
IF AVAILABLE h-art THEN 
DO: 
  FIND FIRST f-art WHERE f-art.departement = h-art.departement 
    AND f-art.artnr = h-art.artnrfront NO-LOCK. 
  IF food-flag AND (f-art.umsatzart = 3 OR f-art.umsatzart = 5) THEN 
  DO: 
    menu-prtflag = 1. 
    menu-bcol = 12. 
  END. 
  IF bev-flag AND (f-art.umsatzart = 3 OR f-art.umsatzart = 6) THEN 
  DO: 
    menu-prtflag = 1. 
    menu-bcol = 12. 
  END. 
  IF other-flag AND f-art.umsatzart = 4 THEN 
  DO: 
    menu-prtflag = 1. 
    menu-bcol = 12. 
  END. 
END. 
