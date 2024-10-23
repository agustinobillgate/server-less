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

DEF INPUT  PARAMETER TABLE FOR fsl.
DEF INPUT  PARAMETER oresnr     AS INT.
DEF INPUT  PARAMETER oresline   AS INT.
DEF INPUT  PARAMETER rsvsort    AS INT.
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER total-depo LIKE bk-veran.deposit. 

DEFINE buffer bkfunc  FOR bk-func. 
DEFINE buffer bkreser FOR bk-reser. 

FIND FIRST fsl.
FIND FIRST bkfunc WHERE bkfunc.veran-nr = oresnr 
    AND bkfunc.veran-seite = oresline NO-LOCK NO-ERROR. 
IF AVAILABLE bkfunc THEN 
DO: 
    FIND CURRENT bkfunc EXCLUSIVE-LOCK. 
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

    bkfunc.f-menu[1] = fsl.f-menu[1]. 
    bkfunc.gema = fsl.gema. 
    bkfunc.weine[1] = fsl.weine[1]. 
    bkfunc.weine[2] = fsl.weine[2]. 
    bkfunc.weine[3] = fsl.weine[3]. 
    bkfunc.weine[4] = fsl.weine[4]. 
    bkfunc.weine[5] = fsl.weine[5]. 
    bkfunc.weine[6] = fsl.weine[6]. 
    bkfunc.menue[1] = fsl.menue[1]. 
    bkfunc.menue[2] = fsl.menue[2]. 
    bkfunc.menue[3] = fsl.menue[3]. 
    bkfunc.menue[4] = fsl.menue[4]. 
    bkfunc.menue[5] = fsl.menue[5]. 
    bkfunc.menue[6] = fsl.menue[6]. 

    bkfunc.vkontrolliert = user-init. 
    bkfunc.geschenk = STRING(TODAY) + "-" + STRING(TIME,"hh:mm:ss"). 
    FIND CURRENT bkfunc NO-LOCK. 
    FOR EACH bkfunc WHERE bkfunc.veran-nr = oresnr NO-LOCK, 
      FIRST bkreser WHERE bkreser.veran-nr = oresnr 
      AND bkreser.veran-resnr = bkfunc.veran-seite 
      AND bkreser.resstatus = rsvsort NO-LOCK: 
      total-depo = total-depo + bkfunc.rpreis[1] + (bkfunc.rpersonen[1] * bkfunc.rpreis[7]). 
    END. 
    FOR EACH bk-rart WHERE bk-rart.veran-nr = oresnr NO-LOCK, 
      FIRST bkreser WHERE bkreser.veran-nr = oresnr 
      AND bkreser.veran-resnr = bk-rart.veran-seite 
      AND bkreser.resstatus = rsvsort NO-LOCK: 
      total-depo = total-depo + bk-rart.preis. 
    END. 
/* 
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = oresnr NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-veran THEN 
    DO: 
      FIND CURRENT bk-veran EXCLUSIVE-LOCK. 
      bk-veran.deposit = total-depo. 
      FIND CURRENT bk-veran NO-LOCK. 
    END. 
*/ 
END. 
