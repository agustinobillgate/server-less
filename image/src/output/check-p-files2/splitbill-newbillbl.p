
 
/*  Program FOR Check-in a guest  */ 
 
DEFINE INPUT  PARAMETER s-recid     AS INTEGER. 
DEFINE OUTPUT PARAMETER bil-recid   AS INTEGER INITIAL 0. 
 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 1 NO-UNDO. 
DEFINE VARIABLE rechnr2  AS INTEGER INITIAL 0 NO-UNDO.  
DEFINE VARIABLE billnr   AS INTEGER INITIAL 1 NO-UNDO.

DEFINE BUFFER resline   FOR res-line. 
DEFINE BUFFER mainbill  FOR bill. 
 
FIND FIRST bill WHERE RECID(bill) = s-recid NO-LOCK.
FIND FIRST resline WHERE resline.resnr = bill.resnr
  AND resline.reslinnr = bill.parent-nr NO-LOCK. /* main bill */ 
 
FIND FIRST htparam WHERE htparam.paramnr = 799 NO-LOCK. 
IF htparam.flogical AND htparam.feldtyp = 4 THEN 
DO: 
  FIND FIRST mainbill WHERE mainbill.resnr = resline.resnr 
    AND mainbill.reslinnr = resline.reslinnr NO-LOCK NO-ERROR. 
  IF AVAILABLE mainbill THEN rechnr2 = mainbill.rechnr2. 
END. 
  
FOR EACH res-line WHERE res-line.gastnr = resline.gastnr 
  AND res-line.resnr = resline.resnr NO-LOCK 
  BY res-line.reslinnr DESCENDING: 
  reslinnr = res-line.reslinnr + 1.
  LEAVE.
END. 
 
CREATE res-line. 
BUFFER-COPY resline EXCEPT resline.reslinnr resstatus active-flag 
  zipreis TO res-line. 
ASSIGN 
  res-line.reslinnr     = reslinnr 
  res-line.resstatus    = 12 
  res-line.active-flag  = 1 
  res-line.gastnrpay    = resline.gastnrmember
. 

FOR EACH bill WHERE bill.resnr = resline.resnr
  AND bill.parent-nr = resline.reslinnr 
  AND bill.flag = 0 NO-LOCK: /*FD - Add bill-flag = 0*/
  billnr = billnr + 1.
END.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
CREATE bill. 
ASSIGN 
  bill.flag         = 0 
  bill.zinr         = res-line.zinr 
  bill.gastnr       = res-line.gastnrpay 
  bill.datum        = htparam.fdate 
  bill.resnr        = res-line.resnr 
  bill.reslinnr     = res-line.reslinnr 
  bill.parent-nr    = resline.reslinnr 
  bill.billnr       = billnr 
  bill.rgdruck      = 1 
  bill.rechnr2      = rechnr2 
. 
 
FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay. 
bill.name = guest.name. 
FIND FIRST reservation WHERE reservation.resnr = resline.resnr 
     AND reservation.gastnr = resline.gastnr NO-LOCK. 
bill.segmentcode = reservation.segmentcode. 
 
bil-recid = RECID(bill). 

