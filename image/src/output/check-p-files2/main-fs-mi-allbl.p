
DEFINE TEMP-TABLE fsl LIKE bk-func 
  FIELD deposit          LIKE bk-veran.deposit 
  FIELD limit-date       LIKE bk-veran.limit-date 
  FIELD deposit-payment  LIKE bk-veran.deposit-payment 
  FIELD payment-date     LIKE bk-veran.payment-date 
  FIELD total-paid       LIKE bk-veran.total-paid 
  FIELD payment-userinit LIKE bk-veran.payment-userinit
  FIELD betriebsnr2      LIKE bk-func.betriebsnr
  FIELD cutoff           LIKE bk-reser.limitdate 
  FIELD raum             LIKE bk-reser.raum
  FIELD grund            LIKE b-storno.grund
  FIELD in-sales         LIKE bk-veran.payment-userinit[9]
  FIELD in-conv          LIKE bk-veran.payment-userinit[9]
  . 

DEFINE buffer bkfunc FOR bk-func. 
DEFINE buffer bkreser FOR bk-reser. 

DEF INPUT  PARAMETER TABLE FOR fsl.
DEF INPUT  PARAMETER resnr               AS INT.
DEF INPUT  PARAMETER resline             AS INT.
DEF INPUT  PARAMETER q3-list-veran-nr    AS INT.
DEF INPUT  PARAMETER q3-list-veran-seite AS INT.
DEF INPUT  PARAMETER rsvsort             AS INT.
DEF INPUT  PARAMETER user-init           AS CHAR.
DEF OUTPUT PARAMETER total-depo LIKE bk-veran.deposit. 

FIND FIRST fsl.
FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK NO-ERROR. 

FOR EACH bkfunc WHERE bkfunc.veran-nr = fsl.veran-nr 
    AND bkfunc.veran-seite NE fsl.veran-seite EXCLUSIVE-LOCK: 
    bkfunc.ape_getraenke[7] = fsl.ape_getraenke[7]. 
    bkfunc.ape_getraenke[8] = fsl.ape_getraenke[8]. 
    bkfunc.bemerkung = fsl.bemerkung. 
    bkfunc.rpreis[7] = fsl.rpreis[7]. 
    bkfunc.rpreis[8] = fsl.rpreis[8]. 
    bkfunc.rpersonen[1] = fsl.rpersonen[1]. 
    bkfunc.kartentext[1] = fsl.kartentext[1]. 
    bkfunc.kartentext[2] = fsl.kartentext[2]. 
    bkfunc.kartentext[3] = fsl.kartentext[3]. 
    bkfunc.kartentext[4] = fsl.kartentext[4]. 
    bkfunc.kartentext[5] = fsl.kartentext[5]. 
    bkfunc.kartentext[6] = fsl.kartentext[6]. 
    bkfunc.kartentext[7] = fsl.kartentext[7]. 
    bkfunc.kartentext[8] = fsl.kartentext[8]. 
    bkfunc.sonstiges[1] = fsl.sonstiges[1]. 
    bkfunc.sonstiges[2] = fsl.sonstiges[2]. 
    bkfunc.sonstiges[3] = fsl.sonstiges[3]. 
    bkfunc.sonstiges[4] = fsl.sonstiges[4]. 
END. 
RUN assign-changes. 

PROCEDURE assign-changes: 
DEFINE buffer bk-f FOR bk-func. 

  total-depo = 0. 
 
  FIND CURRENT bk-func EXCLUSIVE-LOCK. 
  FOR EACH bk-f WHERE bk-f.veran-nr = q3-list-veran-nr NO-LOCK, 
    FIRST bkreser WHERE bkreser.veran-nr = q3-list-veran-nr
    AND bkreser.veran-resnr = q3-list-veran-seite 
    AND bkreser.resstatus = rsvsort NO-LOCK: 
    total-depo = total-depo + bk-f.rpreis[1] + (bk-f.rpersonen[1] 
      * bk-f.rpreis[7]). 
    bk-func.vkontrolliert = user-init. 
    bk-func.geschenk = STRING(TODAY) + "-" + STRING(TIME,"hh:mm:ss"). 
  END. 
  FIND CURRENT bk-func NO-LOCK. 
  FOR EACH bk-rart WHERE bk-rart.veran-nr = q3-list-veran-nr NO-LOCK: 
    total-depo = total-depo + bk-rart.preis. 
  END. 
  fsl.geschenk = bk-func.geschenk. 
  fsl.vkontrolliert = bk-func.vkontrolliert. 
  fsl.personen = bk-func.personen. 

  FIND FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr.
  IF AVAILABLE bk-veran THEN
  DO:
      bk-veran.segmentcode = fsl.segmentcode.
      bk-veran.payment-userinit[9] = fsl.in-sales.
      bk-veran.payment-userinit[9] = bk-veran.payment-userinit[9] + CHR(2) + fsl.in-conv.
  END.
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr.
  IF AVAILABLE bk-reser THEN
  DO:
      bk-reser.limitdate = fsl.cutoff.
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

