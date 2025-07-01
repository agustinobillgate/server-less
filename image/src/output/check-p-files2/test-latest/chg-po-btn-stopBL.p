
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id-l-orderhdr       AS INT.
DEF INPUT PARAMETER waehrung-waehrungsnr    AS INT.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id-l-orderhdr.

IF case-type = 1 THEN   /*MT btn-stop*/
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
    ASSIGN l-orderhdr.gedruckt = ?.
    FIND CURRENT l-orderhdr NO-LOCK.
END.
IF case-type = 2 THEN   /*MT value-changed of currency*/
DO :
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
    ASSIGN l-orderhdr.angebot-lief[3] = waehrung-waehrungsnr.
    FIND CURRENT l-orderhdr NO-LOCK.
END.
