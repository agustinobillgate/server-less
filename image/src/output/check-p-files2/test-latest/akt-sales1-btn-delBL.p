
DEF INPUT PARAMETER recid-akthdr AS INT.
DEF INPUT PARAMETER bediener-nr  AS INT.

FIND FIRST akthdr WHERE RECID(akthdr) = recid-akthdr NO-LOCK.
FIND CURRENT akthdr EXCLUSIVE-LOCK. 
ASSIGN akthdr.flag = 0. 
FOR EACH akt-line WHERE akt-line.aktnr = akthdr.aktnr EXCLUSIVE-LOCK:
ASSIGN akt-line.flag = 2.
END.
FIND CURRENT akthdr NO-LOCK.

FIND FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK.
CREATE res-history. 
ASSIGN 
res-history.nr = bediener-nr 
res-history.datum = TODAY 
res-history.zeit = TIME 
res-history.aenderung = "Delete Activity: ActNo " + STRING(akthdr.aktnr) 
  + " - " + guest.NAME 
res-history.action = "Sales Activity"
. 
FIND CURRENT res-history NO-LOCK. 
RELEASE res-history. 
