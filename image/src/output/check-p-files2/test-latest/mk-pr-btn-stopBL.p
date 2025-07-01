
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id EXCLUSIVE-LOCK.
DELETE l-orderhdr.
RELEASE l-orderhdr.
