
DEF INPUT PARAMETER gastnr AS INT.
DEF OUTPUT PARAMETER fdate AS DATE.
DEF OUTPUT PARAMETER t-tittle AS CHAR.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-ERROR. 
IF AVAILABLE guest THEN t-tittle = t-tittle + " - " + 
    (guest.name + ", " + guest.vorname1 + guest.anredefirma). 

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
fdate = htparam.fdate.
