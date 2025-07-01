
 
/*  Program FOR Check-in a guest  */ 
 
DEFINE INPUT  PARAMETER resNo       AS INTEGER. 
DEFINE INPUT  PARAMETER reslinNo    AS INTEGER. 
DEFINE INPUT  PARAMETER parent-nr   AS INTEGER. 
DEFINE INPUT  PARAMETER billnr      AS INTEGER. 
DEFINE OUTPUT PARAMETER bil-recid   AS INTEGER INITIAL 0. 
 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 1. 
DEFINE VARIABLE its-ok  AS LOGICAL INITIAL YES. 
DEFINE VARIABLE answer  AS LOGICAL INITIAL YES. 
 
DEFINE VARIABLE rechnr2 AS INTEGER INITIAL 0. 
 
DEFINE buffer res-member FOR res-line. 
DEFINE buffer resline FOR res-line. 
DEFINE BUFFER mainbill FOR bill. 
 
/* SY 04 June 2016 : replace reslinNo with parent-nr */
FIND FIRST resline WHERE resline.resnr = resNo
    AND resline.reslinnr = parent-nr NO-LOCK. /* guest */ 
 
FIND FIRST htparam WHERE htparam.paramnr = 799 NO-LOCK. 
IF htparam.flogical AND htparam.feldtyp = 4 THEN 
DO: 
  FIND FIRST mainbill WHERE mainbill.resnr = resline.resnr 
    AND mainbill.reslinnr = resline.reslinnr NO-LOCK NO-ERROR. 
  IF AVAILABLE mainbill THEN rechnr2 = mainbill.rechnr2. 
END. 
 
 
/* SY 04 June 2016 */
FOR EACH res-line WHERE res-line.gastnr = resline.gastnr 
    AND res-line.resnr = resline.resnr 
    NO-LOCK BY res-line.reslinnr DESCENDING: 
    reslinnr = res-line.reslinnr + 1.
    LEAVE.
END. 
 
CREATE res-line. 
BUFFER-COPY resline EXCEPT resline.reslinnr resstatus active-flag zipreis 
  TO res-line. 
ASSIGN 
  res-line.reslinnr = reslinnr 
  res-line.resstatus = 12 
  res-line.active-flag = 1 
  res-line.gastnrpay = /*resline.gastnrmember*/ resline.gastnrpay. /*FDL June 26, 2032 - E57742*/
 
/* 
res-line.gastnr = resline.gastnr. 
res-line.gastnrpay = resline.gastnrmember. 
res-line.gastnrmember = resline.gastnrmember. 
res-line.resnr = resline.resnr. 
res-line.reslinnr = reslinnr. 
res-line.resstatus = 12. 
res-line.name = resline.name. 
res-line.zinr = resline.zinr. 
res-line.ankunft = resline.ankunft. 
res-line.abreise = resline.abreise. 
res-line.reserve-int = resline.reserve-int. 
res-line.zikatnr = resline.zikatnr. 
res-line.arrangement= resline.arrangement. 
res-line.active-flag = 1. 
*/ 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
CREATE bill. 
ASSIGN 
  bill.flag = 0 
  bill.zinr = res-line.zinr 
  bill.gastnr = res-line.gastnrpay 
  bill.datum = htparam.fdate 
  bill.resnr = res-line.resnr 
  bill.reslinnr = res-line.reslinnr 
  bill.parent-nr = parent-nr 
  bill.billnr = billnr 
  bill.rgdruck = 1 
  bill.rechnr2 = rechnr2 
. 
 
FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay. 
bill.name = guest.name. 
FIND FIRST reservation WHERE reservation.resnr = resline.resnr 
     AND reservation.gastnr = resline.gastnr NO-LOCK. 
bill.segmentcode = reservation.segmentcode. 
 
bil-recid = RECID(bill). 

