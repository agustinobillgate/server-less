
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST katpreis WHERE RECID(katpreis) = rec-id NO-LOCK.
FIND CURRENT katpreis EXCLUSIVE-LOCK. 
delete katpreis.
RELEASE katpreis.
