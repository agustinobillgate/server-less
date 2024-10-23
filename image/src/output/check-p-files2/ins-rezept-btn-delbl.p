
DEF INPUT PARAMETER h-recid AS INT.

FIND FIRST h-rezlin WHERE RECID(h-rezlin) = h-recid EXCLUSIVE-LOCK. 
delete h-rezlin.
RELEASE h-rezlin.
