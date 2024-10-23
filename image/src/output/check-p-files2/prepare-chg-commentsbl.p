
DEF INPUT  PARAMETER bill-recid AS INT.
DEF OUTPUT PARAMETER rechnr     AS INT.
DEF OUTPUT PARAMETER res-com    AS CHAR.
DEF OUTPUT PARAMETER resl-com   AS CHAR.
DEF OUTPUT PARAMETER g-com      AS CHAR.
DEF OUTPUT PARAMETER bill-com   AS CHAR.
DEF OUTPUT PARAMETER bill-resnr AS INT.

FIND FIRST bill WHERE RECID(bill) = bill-recid NO-LOCK. 
rechnr = bill.rechnr. 

FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK.

IF bill.resnr GT 0 THEN 
DO:
  FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK. 
  res-com  = reservation.bemerk. 
END.

IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN
DO:
  FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.reslinnr NO-LOCK. 
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
  ASSIGN resl-com = res-line.bemerk.
END.

ASSIGN
  g-com    = guest.bemerkung
  bill-com = bill.vesrdepot
. 
bill-resnr = bill.resnr.
