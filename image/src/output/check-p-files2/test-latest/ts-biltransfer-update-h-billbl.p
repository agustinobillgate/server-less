
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER char1  AS CHAR.

FIND FIRST vhp.h-bill WHERE RECID(h-bill) = rec-id EXCLUSIVE-LOCK.
vhp.h-bill.bilname = char1.
FIND CURRENT vhp.h-bill NO-LOCK.
