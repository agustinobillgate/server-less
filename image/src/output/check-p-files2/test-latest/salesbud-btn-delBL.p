
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST salesbud WHERE RECID(salesbud) = rec-id EXCLUSIVE-LOCK.
DELETE salesbud.
RELEASE salesbud.
