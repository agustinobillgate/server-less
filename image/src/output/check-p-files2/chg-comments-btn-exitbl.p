
DEF INPUT PARAMETER bill-recid              AS INT.
DEF INPUT PARAMETER g-com-screen-value      AS CHAR.
DEF INPUT PARAMETER res-com-screen-value    AS CHAR.
DEF INPUT PARAMETER resl-com-screen-value   AS CHAR.
DEF INPUT PARAMETER bill-com-screen-value   AS CHAR.

FIND FIRST bill WHERE RECID(bill) = bill-recid NO-LOCK.
FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK.
IF bill.resnr GT 0 THEN 
    FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK.
IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN
DO:
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.reslinnr = bill.reslinnr NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
END.

FIND CURRENT guest EXCLUSIVE-LOCK. 
guest.bemerkung = g-com-screen-value. 
FIND CURRENT guest NO-LOCK. 
 
IF AVAILABLE reservation THEN
DO:
    FIND CURRENT reservation EXCLUSIVE-LOCK. 
    reservation.bemerk = res-com-screen-value. 
    FIND CURRENT reservation NO-LOCK. 
END.

IF AVAILABLE res-line THEN
DO:
    FIND CURRENT res-line EXCLUSIVE-LOCK. 
    res-line.bemerk = resl-com-screen-value. 
    FIND CURRENT res-line NO-LOCK. 
END.

FIND CURRENT bill EXCLUSIVE-LOCK. 
bill.vesrdepot = bill-com-screen-value. 
FIND CURRENT bill NO-LOCK. 
