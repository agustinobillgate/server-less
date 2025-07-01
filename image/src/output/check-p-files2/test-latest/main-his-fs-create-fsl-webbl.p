DEFINE TEMP-TABLE bkf LIKE b-history. 
DEFINE TEMP-TABLE fsl LIKE b-history
  FIELD cutoff           LIKE bk-reser.limitdate 
  FIELD grund            LIKE b-storno.grund
   FIELD in-sales        LIKE bk-veran.payment-userinit[9]
  FIELD in-conv          LIKE bk-veran.payment-userinit[9]. 

DEFINE INPUT PARAMETER inResnr AS INTEGER.
DEFINE INPUT PARAMETER inResline AS INTEGER.
DEFINE OUTPUT PARAMETER curr-gastnr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR bkf.
DEFINE OUTPUT PARAMETER TABLE FOR fsl.
DEFINE OUTPUT PARAMETER flag-his AS LOGICAL INITIAL YES.

FOR EACH b-history WHERE b-history.veran-nr = inResnr AND b-history.veran-seite = inResline NO-LOCK: 
  CREATE bkf. 
    bkf.veran-nr = b-history.veran-nr. 
    bkf.veran-seite = b-history.veran-seite. 
    bkf.zweck[1] = ENTRY(1, b-history.zweck[1], CHR(2)). 
    bkf.datum = b-history.datum. 
    bkf.uhrzeit = b-history.uhrzeit. 
    bkf.r-resstatus[1] = b-history.r-resstatus[1]. 
    bkf.c-resstatus[1] = b-history.c-resstatus[1]. 
    bkf.raeume[1] = b-history.raeume[1]. 
    /*bkf.zweck[1] = b-history.zweck[1]. */
    bkf.uhrzeiten[1] = b-history.uhrzeiten[1]. 
    bkf.rpersonen[1] = b-history.rpersonen[1]. 
    bkf.tischform[1] = b-history.tischform[1]. 
    bkf.rpreis[1] = b-history.rpreis[1]. 
    bkf.dekoration[1] = b-history.dekoration[1]. 
END. 
FIND FIRST b-history WHERE b-history.veran-nr = inResnr AND b-history.veran-seite = inResline NO-LOCK NO-ERROR. /* Malik Serverless 600 add if available */
IF AVAILABLE b-history THEN 
DO:
  CREATE fsl. 
  fsl.datum = b-history.datum. 
  fsl.uhrzeit = b-history.uhrzeit. 
  fsl.veran-nr = b-history.veran-nr. 
  fsl.veran-seite = b-history.veran-seite. 
  fsl.wochentag = b-history.wochentag. 
  fsl.bestellt_durch = b-history.bestellt_durch. 
  fsl.segmentcode = b-history.segmentcode.
  fsl.veranstalteranschrift[1] = b-history.veranstalteranschrift[1]. 
  fsl.veranstalteranschrift[2] = b-history.veranstalteranschrift[2]. 
  fsl.veranstalteranschrift[3] = b-history.veranstalteranschrift[3]. 
  fsl.veranstalteranschrift[4] = b-history.veranstalteranschrift[4]. 
  fsl.veranstalteranschrift[5] = b-history.veranstalteranschrift[5].
  fsl.segmentcode = b-history.segmentcode. 
  fsl.limit-date = b-history.limit-date.
  fsl.v-kontaktperson[1] = b-history.v-kontaktperson[1]. 
  fsl.v-telefon = b-history.v-telefon. 
  fsl.v-telefax = b-history.v-telefax. 
  fsl.adurch = b-history.adurch. 
  fsl.rechnungsanschrift[1] = b-history.rechnungsanschrift[1]. 
  fsl.rechnungsanschrift[2] = b-history.rechnungsanschrift[2]. 
  fsl.rechnungsanschrift[3] = b-history.rechnungsanschrift[3]. 
  fsl.rechnungsanschrift[4] = b-history.rechnungsanschrift[4]. 
  fsl.kontaktperson[1] = b-history.kontaktperson[1]. 
  fsl.telefon = b-history.telefon. 
  fsl.telefax = b-history.telefax. 
  fsl.r-resstatus[1] = b-history.r-resstatus[1]. 
  fsl.c-resstatus[1] = b-history.c-resstatus[1]. 
  fsl.raeume[1] = b-history.raeume[1]. 
  fsl.uhrzeiten[1] = b-history.uhrzeiten[1]. 
  fsl.rpersonen[1] = b-history.rpersonen[1]. 
  fsl.tischform[1] = b-history.tischform[1]. 
  fsl.rpreis[1] = b-history.rpreis[1]. 
  fsl.dekoration[1] = b-history.dekoration[1]. 
  fsl.ape_getraenke[1] = b-history.ape_getraenke[1]. 
  fsl.ape_getraenke[2] = b-history.ape_getraenke[2]. 
  fsl.ape_getraenke[3] = b-history.ape_getraenke[3]. 
  fsl.ape_getraenke[4] = b-history.ape_getraenke[4]. 
  fsl.ape_getraenke[5] = b-history.ape_getraenke[5]. 
  fsl.ape_getraenke[6] = b-history.ape_getraenke[6]. 
  fsl.ape_getraenke[7] = b-history.ape_getraenke[7]. 
  fsl.ape_getraenke[8] = b-history.ape_getraenke[8]. 
  fsl.ape_getraenke[3] = b-history.ape_getraenke[3]. 
  fsl.bemerkung = b-history.bemerkung. 
  fsl.f-menu[1] = b-history.f-menu[1]. 
  fsl.gema = b-history.gema. 
  fsl.rpreis[7] = b-history.rpreis[7]. 
  fsl.rpreis[8] = b-history.rpreis[8]. 
  fsl.kartentext[1] = b-history.kartentext[1]. 
  fsl.kartentext[2] = b-history.kartentext[2]. 
  fsl.kartentext[3] = b-history.kartentext[3]. 
  fsl.kartentext[4] = b-history.kartentext[4]. 
  fsl.kartentext[5] = b-history.kartentext[5]. 
  fsl.kartentext[6] = b-history.kartentext[6]. 
  fsl.kartentext[7] = b-history.kartentext[7]. 
  fsl.kartentext[8] = b-history.kartentext[8]. 
  fsl.sonstiges[1] = b-history.sonstiges[1]. 
  fsl.sonstiges[2] = b-history.sonstiges[2]. 
  fsl.sonstiges[3] = b-history.sonstiges[3]. 
  fsl.sonstiges[4] = b-history.sonstiges[4]. 
  fsl.auf_datum = b-history.auf_datum. 
  fsl.vgeschrieben = b-history.vgeschrieben. 
  fsl.vkontrolliert = b-history.vkontrolliert. 
  fsl.geschenk = b-history.geschenk. 
  fsl.nadkarte[1] = b-history.nadkarte[1]. 
  fsl.deposit = b-history.deposit. 
  fsl.limit-date = b-history.limit-date. 
  fsl.deposit-payment[1] = b-history.deposit-payment[1]. 
  fsl.deposit-payment[2] = b-history.deposit-payment[2]. 
  fsl.deposit-payment[3] = b-history.deposit-payment[3]. 
  fsl.deposit-payment[4] = b-history.deposit-payment[4]. 
  fsl.deposit-payment[5] = b-history.deposit-payment[5]. 
  fsl.payment-date[1] = b-history.payment-date[1]. 
  fsl.payment-date[2] = b-history.payment-date[2]. 
  fsl.payment-date[3] = b-history.payment-date[3]. 
  fsl.payment-date[4] = b-history.payment-date[4]. 
  fsl.payment-date[5] = b-history.payment-date[5]. 
  fsl.payment-userinit[1] = b-history.payment-userinit[1]. 
  fsl.payment-userinit[2] = b-history.payment-userinit[2]. 
  fsl.payment-userinit[3] = b-history.payment-userinit[3]. 
  fsl.payment-userinit[4] = b-history.payment-userinit[4]. 
  fsl.payment-userinit[5] = b-history.payment-userinit[5]. 
  fsl.total-paid = b-history.total-paid. 
  fsl.raumbezeichnung[8] = b-history.raumbezeichnung[8]. /*Naufal*/

  IF NUM-ENTRIES(b-history.zweck[1], CHR(2)) GE 2 THEN
  DO:
        fsl.zweck[1] = ENTRY(2, b-history.zweck[1], CHR(2)).
  END.
  ELSE
  DO:
        fsl.zweck[1] = b-history.zweck[1].
  END.

  

  FIND FIRST bk-veran WHERE bk-veran.veran-nr = b-history.veran-nr NO-LOCK NO-ERROR.
  curr-gastnr = bk-veran.gastnr.

  FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
    

  IF NUM-ENTRIES(b-history.payment-userinit[9], CHR(2)) GE 2 THEN
  DO:
        fsl.in-sales = ENTRY(1, b-history.payment-userinit[9], CHR(2)). 
        fsl.in-conv =  ENTRY(2, b-history.payment-userinit[9], CHR(2)).
  END.
  ELSE
  DO:
        fsl.in-sales =  guest.phonetik3. 
        fsl.in-conv =   guest.phonetik2.
  END.

  FIND FIRST b-storno WHERE b-storno.bankettnr = inResnr 
      AND b-storno.breslinnr = inResline NO-LOCK NO-ERROR.
  IF AVAILABLE b-storno THEN
  DO:
      fsl.grund[1] = b-storno.grund[1].
      fsl.grund[2] = b-storno.grund[2].
      fsl.grund[3] = b-storno.grund[3].
      fsl.grund[4] = b-storno.grund[4].
      fsl.grund[5] = b-storno.grund[5].
      fsl.grund[6] = b-storno.grund[6].
      fsl.grund[7] = b-storno.grund[7].
      fsl.grund[8] = b-storno.grund[8].
      fsl.grund[9] = b-storno.grund[9].
      fsl.grund[10] = b-storno.grund[10].
  END.

  FIND FIRST bk-reser WHERE bk-reser.veran-nr = inResnr NO-LOCK NO-ERROR.
  IF AVAILABLE bk-reser THEN
  fsl.cutoff = bk-reser.limitdate. 
END.

