
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST parameters WHERE RECID(parameters) = rec-id EXCLUSIVE-LOCK.
delete parameters.
