

DEF INPUT  PARAMETER usr-init AS CHAR.
DEF OUTPUT PARAMETER usr-name AS CHAR.

FIND FIRST bediener WHERE bediener.userinit = usr-init NO-LOCK. 
usr-name = bediener.username. 

