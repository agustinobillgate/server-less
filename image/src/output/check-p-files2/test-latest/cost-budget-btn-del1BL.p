
DEF INPUT PARAMETER cost-list-rec-id AS INT.

FIND FIRST parameters WHERE RECID(parameters) = cost-list-rec-id EXCLUSIVE-LOCK. 
delete parameters. 
/*MTFIND CURRENT cost-list EXCLUSIVE-LOCK. 
delete cost-list. 
last-name = "".*/
