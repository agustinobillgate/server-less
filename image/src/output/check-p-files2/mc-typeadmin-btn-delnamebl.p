
DEF INPUT PARAMETER nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.

FOR EACH mc-disc WHERE mc-disc.nr = nr:
    DELETE mc-disc.
END.

FIND FIRST mc-types WHERE RECID(mc-types) = rec-id EXCLUSIVE-LOCK.  
DELETE mc-types.
