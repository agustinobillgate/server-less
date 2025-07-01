
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST gl-jouhdr WHERE RECID(gl-jouhdr) = rec-id.
FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
gl-jouhdr.batch = NO.
FIND CURRENT gl-jouhdr NO-LOCK.
