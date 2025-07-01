
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST guestbud WHERE RECID(guestbud) = rec-id.
FIND CURRENT guestbud EXCLUSIVE-LOCK. 
delete guestbud.                             
