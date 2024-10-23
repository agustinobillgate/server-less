
DEF INPUT PARAMETER rec-id      AS INT.
DEF INPUT PARAMETER order-taker AS INT.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
vhp.h-bill.betriebsnr = order-taker. 
FIND CURRENT vhp.h-bill NO-LOCK. 
