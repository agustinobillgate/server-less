
DEF INPUT PARAMETER currency-screen-value AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER int1 AS INT.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id EXCLUSIVE-LOCK.
FIND FIRST waehrung WHERE waehrung.wabkurz = currency-screen-value NO-LOCK. 
l-orderhdr.angebot-lief[3] = waehrung.waehrungsnr.
FIND CURRENT l-orderhdr NO-LOCK.
int1 = l-orderhdr.angebot-lief[3].
