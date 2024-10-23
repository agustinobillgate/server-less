
DEF INPUT  PARAMETER resnr              AS INT.
DEF INPUT  PARAMETER resline            AS INT.
DEF INPUT  PARAMETER rsvsort            AS INT.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF INPUT  PARAMETER fsl-segmentcode    LIKE bk-func.segmentcode.
DEF INPUT  PARAMETER fsl-in-sales       /*LIKE bk-veran.payment-userinit[9]*/ AS CHAR.
DEF INPUT  PARAMETER fsl-in-conv        /*LIKE bk-veran.payment-userinit[9]*/ AS CHAR.
DEF INPUT  PARAMETER fsl-cutoff         LIKE bk-reser.limitdate.
DEF OUTPUT PARAMETER fsl-geschenk       LIKE bk-func.geschenk.
DEF OUTPUT PARAMETER fsl-vkontrolliert  LIKE bk-func.vkontrolliert.
DEF OUTPUT PARAMETER fsl-personen       LIKE bk-func.personen.
DEF OUTPUT PARAMETER total-depo         LIKE bk-veran.deposit. 

DEFINE buffer bkreser FOR bk-reser. 

FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK NO-ERROR. 

RUN assign-changes.

PROCEDURE assign-changes: 
DEFINE buffer bk-f FOR bk-func. 
  total-depo = 0. 
 
  FIND CURRENT bk-func EXCLUSIVE-LOCK. 
  FOR EACH bk-f WHERE bk-f.veran-nr = bk-func.veran-nr NO-LOCK, 
    FIRST bkreser WHERE bkreser.veran-nr = bk-func.veran-nr 
    AND bkreser.veran-resnr = bk-func.veran-seite 
    AND bkreser.resstatus = rsvsort NO-LOCK: 
    total-depo = total-depo + bk-f.rpreis[1] + (bk-f.rpersonen[1] 
      * bk-f.rpreis[7]). 
    bk-func.vkontrolliert = user-init. 
    bk-func.geschenk = STRING(TODAY) + "-" + STRING(TIME,"hh:mm:ss"). 
  END. 
  FIND CURRENT bk-func NO-LOCK. 
  FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr NO-LOCK: 
    total-depo = total-depo + bk-rart.preis. 
  END. 
  fsl-geschenk = bk-func.geschenk. 
  fsl-vkontrolliert = bk-func.vkontrolliert. 
  fsl-personen = bk-func.personen. 

  FIND FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr.
  IF AVAILABLE bk-veran THEN
  DO:
      bk-veran.segmentcode = fsl-segmentcode.
      bk-veran.payment-userinit[9] = fsl-in-sales.
      bk-veran.payment-userinit[9] = bk-veran.payment-userinit[9] + CHR(2) + fsl-in-conv.
  END.
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr.
  IF AVAILABLE bk-reser THEN
  DO:
      bk-reser.limitdate = fsl-cutoff.
  END.
/* 
  fsl.deposit = total-depo. 
  FIND FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK NO-ERROR. 
  IF AVAILABLE bk-veran THEN 
  DO: 
    FIND CURRENT bk-veran EXCLUSIVE-LOCK. 
    bk-veran.deposit = total-depo. 
    FIND CURRENT bk-veran NO-LOCK. 
  END. 
*/ 
END. 
