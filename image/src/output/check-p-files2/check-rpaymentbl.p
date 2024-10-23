 
  
 
/* Check GCF Payment IN Restaurant */ 
DEFINE INPUT  PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEFINE INPUT  PARAMETER gastnr      AS INTEGER. 
DEFINE INPUT  PARAMETER dept        AS INTEGER. 
DEFINE OUTPUT PARAMETER zahlungsart AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER msg-str     AS CHAR INITIAL ""  NO-UNDO.
/* 
DEFINE VARIABLE gastnr AS INTEGER INITIAL 2. 
DEFINE VARIABLE dept AS INTEGER INITIAL 1. 
DEFINE VARIABLE zahlungsart AS INTEGER INITIAL 0. 
*/ 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "check-rpayment". 

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE guest THEN zahlungsart = guest.zahlungsart. 
IF zahlungsart = 0 THEN 
DO: 
  msg-str = translateExtended ("No C/L Payment Articles defined for this Guest.",lvCAREA,""). 
END. 
ELSE 
DO: 
  FIND FIRST artikel WHERE artikel.artnr = zahlungsart 
    AND artikel.departement = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel OR artikel.artart NE 2 THEN 
  DO: 
    msg-str = translateExtended ("No C/L Payment Articles defined for this Guest.",lvCAREA,""). 
    zahlungsart = 0. 
  END. 
END. 
 
 
 
