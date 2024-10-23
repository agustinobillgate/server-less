
DEFINE INPUT PARAMETER rset-bezeich AS CHARACTER.

FIND FIRST bk-rset WHERE bk-rset.bezeich = rset-bezeich EXCLUSIVE-LOCK.
DELETE bk-rset.

