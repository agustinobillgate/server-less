
DEF INPUT PARAMETER recid-l-ophdr AS INT.
DEF INPUT PARAMETER lscheinnr AS CHAR.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = recid-l-ophdr.

FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
l-ophdr.docu-nr = lscheinnr. 
l-ophdr.lscheinnr = lscheinnr. 
FIND CURRENT l-ophdr NO-LOCK. 
