
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
vhp.h-bill.rgdruck = 1. 
FIND CURRENT vhp.h-bill NO-LOCK.
