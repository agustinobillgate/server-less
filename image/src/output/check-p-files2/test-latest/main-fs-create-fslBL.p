
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

DEFINE TEMP-TABLE bkf 
    FIELD veran-nr    LIKE bk-func.veran-nr 
    FIELD veran-seite LIKE bk-func.veran-seite 
    FIELD zweck       LIKE bk-func.zweck 
    FIELD datum       LIKE bk-func.datum 
    FIELD uhrzeit     LIKE bk-func.uhrzeit 
    FIELD resstatus   LIKE bk-func.resstatus 
    FIELD r-resstatus LIKE bk-func.r-resstatus 
    FIELD c-resstatus LIKE bk-func.c-resstatus 
    FIELD raeume      LIKE bk-func.raeume 
    FIELD uhrzeiten   LIKE bk-func.uhrzeiten 
    FIELD rpersonen   LIKE bk-func.rpersonen 
    FIELD tischform   LIKE bk-func.tischform 
    FIELD rpreis      LIKE bk-func.rpreis 
    FIELD dekoration  LIKE bk-func.dekoration 
    FIELD begin-time  LIKE bk-reser.von-zeit 
    FIELD ending-time LIKE bk-reser.bis-zeit 
    FIELD begin-i     AS INTEGER 
    FIELD ending-i    AS INTEGER
    FIELD bezeich     LIKE bk-raum.bezeich. /*FD*/

DEFINE TEMP-TABLE bstorno LIKE b-storno.

DEFINE TEMP-TABLE zinr-list
    FIELD room-cat AS CHAR
    FIELD jml-room AS INTEGER.


DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER b1-resline     AS INT.
DEF INPUT  PARAMETER bk-veran-recid AS INT.
DEF INPUT  PARAMETER rsvsort        AS INT.
DEF INPUT  PARAMETER curr-gastnr    AS INT.

DEF OUTPUT PARAMETER resnr          AS INT.
DEF OUTPUT PARAMETER resline        AS INT.
DEF OUTPUT PARAMETER sales-id       AS CHAR.
DEF OUTPUT PARAMETER sob            AS CHAR.
DEF OUTPUT PARAMETER segcode        AS CHAR.
DEF OUTPUT PARAMETER rmtype         AS CHAR.
DEF OUTPUT PARAMETER rmno           AS CHAR.
DEF OUTPUT PARAMETER roomrate       AS CHAR.
DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER co-date        AS DATE.
DEF OUTPUT PARAMETER sum-room       AS INTEGER INIT 0.
DEF OUTPUT PARAMETER sum-room-cat   AS CHAR.
DEF OUTPUT PARAMETER venue          AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR fsl.
DEF OUTPUT PARAMETER TABLE FOR bkf.
DEF OUTPUT PARAMETER TABLE FOR bstorno.

FIND FIRST bk-veran WHERE RECID(bk-veran) = bk-veran-recid NO-LOCK NO-ERROR.
IF NOT AVAILABLE bk-veran THEN RETURN. /*FT serverless*/
FIND FIRST bk-reser WHERE bk-reser.veran-nr = b1-resnr 
    AND bk-reser.veran-resnr = b1-resline NO-LOCK NO-ERROR.
IF NOT AVAILABLE bk-reser THEN RETURN. /*FT serverless*/

resnr = bk-veran.veran-nr. 
resline = bk-reser.veran-seite. 

resline = bk-reser.veran-seite.
FOR EACH fsl: 
    DELETE fsl. 
END. 
FOR EACH bkf: 
    DELETE bkf. 
END. 
FOR EACH bk-func WHERE bk-func.veran-nr = bk-veran.veran-nr 
    AND bk-func.resstatus = rsvsort NO-LOCK: 
    CREATE bkf. 
    ASSIGN 
      bkf.veran-nr = bk-func.veran-nr 
      bkf.veran-seite = bk-func.veran-seite 
      /*bkf.zweck[1] = ENTRY(1, bk-func.zweck[1], CHR(2)) */
      bkf.datum = bk-func.datum 
      bkf.uhrzeit = bk-func.uhrzeit 
      bkf.resstatus = bk-func.resstatus 
      bkf.r-resstatus[1] = bk-func.r-resstatus[1] 
      bkf.c-resstatus[1] = bk-func.c-resstatus[1] 
      bkf.raeume[1] = bk-func.raeume[1] 
      /*bkf.zweck[1] = bk-func.zweck[1] 
      bkf.uhrzeit = bk-func.uhrzeiten[1] */
      bkf.rpersonen[1] = bk-func.rpersonen[1] 
      bkf.tischform[1] = bk-func.tischform[1] 
      bkf.rpreis[1] = bk-func.rpreis[1] 
      bkf.dekoration[1] = bk-func.dekoration[1]. 

    IF NUM-ENTRIES(bk-func.zweck[1], CHR(2)) GE 2 THEN
    DO:
        bkf.zweck[1] = ENTRY(1, bk-func.zweck[1], CHR(2)).
    END.
    ELSE
    DO:
        bkf.zweck[1] = bk-func.zweck[1].
    END.

    /*FD Dec 19, 19 - Req Chanti tiket no 7241F8*/
    FIND FIRST bk-raum WHERE bk-raum.raum = bk-func.raeume[1] NO-LOCK NO-ERROR.
    IF AVAILABLE bk-raum THEN
    DO:        
        FIND FIRST queasy WHERE queasy.KEY = 210
            AND queasy.number1 = bk-func.veran-nr
            AND queasy.number2 = bk-func.veran-seite NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                bkf.bezeich = queasy.char1.
        END.
        ELSE
        DO:
            ASSIGN
                bkf.bezeich = bk-raum.bezeich.
        END.
    END.
    /*FD End*/
END. 
FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR. 
FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
FIND FIRST bk-func WHERE bk-func.veran-nr = resnr AND bk-func.veran-seite = resline NO-LOCK NO-ERROR. 
CREATE fsl. 
    /*fsl.zweck[1] = ENTRY(2, bk-func.zweck[1], CHR(2)). */
    fsl.datum = bk-func.datum. 
    fsl.uhrzeit = bk-func.uhrzeit. 
    fsl.technik[1] = bk-func.technik[1].
    fsl.technik[2] = bk-func.technik[2].
    fsl.veran-nr = bk-func.veran-nr. 
    fsl.veran-seite = bk-func.veran-seite. 
    fsl.wochentag = bk-func.wochentag. 
    fsl.bestellt_durch = bk-func.bestellt_durch. 
    fsl.veranstalteranschrift[1] = bk-func.veranstalteranschrift[1]. 
    fsl.veranstalteranschrift[2] = bk-func.veranstalteranschrift[2]. 
    fsl.veranstalteranschrift[3] = bk-func.veranstalteranschrift[3]. 
    fsl.veranstalteranschrift[4] = bk-func.veranstalteranschrift[4]. 
    fsl.Veranstalteranschrift[5] = bk-func.Veranstalteranschrift[5].
    fsl.v-kontaktperson[1] = bk-func.v-kontaktperson[1]. 
    fsl.v-telefon = bk-func.v-telefon. 
    fsl.v-telefax = bk-func.v-telefax. 
    fsl.adurch = bk-func.adurch. 
    fsl.rechnungsanschrift[1] = bk-func.rechnungsanschrift[1]. 
    fsl.rechnungsanschrift[2] = bk-func.rechnungsanschrift[2]. 
    fsl.rechnungsanschrift[3] = bk-func.rechnungsanschrift[3]. 
    fsl.rechnungsanschrift[4] = bk-func.rechnungsanschrift[4]. 
    fsl.kontaktperson[1] = bk-func.kontaktperson[1]. 
    fsl.telefon = bk-func.telefon. 
    fsl.telefax = bk-func.telefax. 
    fsl.r-resstatus[1] = bk-func.r-resstatus[1]. 
    fsl.c-resstatus[1] = bk-func.c-resstatus[1]. 
    fsl.raeume[1] = bk-func.raeume[1]. 
    /*fsl.zweck[1] = bk-func.zweck[1]. */
    fsl.uhrzeiten[1] = bk-func.uhrzeiten[1]. 
    fsl.rpersonen[1] = bk-func.rpersonen[1]. 
    fsl.tischform[1] = bk-func.tischform[1]. 
    fsl.rpreis[1] = bk-func.rpreis[1]. 
    fsl.dekoration[1] = bk-func.dekoration[1]. 
    fsl.ape_getraenke[1] = bk-func.ape_getraenke[1]. 
    fsl.ape_getraenke[2] = bk-func.ape_getraenke[2]. 
    fsl.ape_getraenke[3] = bk-func.ape_getraenke[3]. 
    fsl.ape_getraenke[4] = bk-func.ape_getraenke[4]. 
    fsl.ape_getraenke[5] = bk-func.ape_getraenke[5]. 
    fsl.ape_getraenke[6] = bk-func.ape_getraenke[6]. 
    fsl.ape_getraenke[7] = bk-func.ape_getraenke[7]. 
    fsl.ape_getraenke[8] = bk-func.ape_getraenke[8]. 
    fsl.bemerkung = bk-func.bemerkung. 
    fsl.f-menu[1] = bk-func.f-menu[1]. 
    fsl.gema = bk-func.gema. 
    fsl.rpreis[7] = bk-func.rpreis[7]. 
    fsl.rpreis[8] = bk-func.rpreis[8]. 
    fsl.kartentext[1] = bk-func.kartentext[1]. 
    fsl.kartentext[2] = bk-func.kartentext[2]. 
    fsl.kartentext[3] = bk-func.kartentext[3]. 
    fsl.kartentext[4] = bk-func.kartentext[4]. 
    fsl.kartentext[5] = bk-func.kartentext[5]. 
    fsl.kartentext[6] = bk-func.kartentext[6]. 
    fsl.kartentext[7] = bk-func.kartentext[7]. 
    fsl.kartentext[8] = bk-func.kartentext[8]. 
    fsl.sonstiges[1] = bk-func.sonstiges[1]. 
    fsl.sonstiges[2] = bk-func.sonstiges[2]. 
    fsl.sonstiges[3] = bk-func.sonstiges[3]. 
    fsl.sonstiges[4] = bk-func.sonstiges[4]. 
    fsl.weine[1] = bk-func.weine[1]. 
    fsl.weine[2] = bk-func.weine[2]. 
    fsl.weine[3] = bk-func.weine[3]. 
    fsl.weine[4] = bk-func.weine[4]. 
    fsl.weine[5] = bk-func.weine[5]. 
    fsl.weine[6] = bk-func.weine[6]. 
    fsl.menue[1] = bk-func.menue[1]. 
    fsl.menue[2] = bk-func.menue[2]. 
    fsl.menue[3] = bk-func.menue[3]. 
    fsl.menue[4] = bk-func.menue[4]. 
    fsl.menue[5] = bk-func.menue[5]. 
    fsl.menue[6] = bk-func.menue[6]. 
    fsl.auf_datum = bk-func.auf_datum. 
    fsl.vgeschrieben = bk-func.vgeschrieben. 
    fsl.vkontrolliert = bk-func.vkontrolliert. 
    fsl.geschenk = bk-func.geschenk. 
    fsl.nadkarte[1] = bk-func.nadkarte[1]. 
    fsl.deposit = bk-veran.deposit. 
    fsl.limit-date = bk-veran.limit-date. 
    fsl.deposit-payment[1] = bk-veran.deposit-payment[1]. 
    fsl.deposit-payment[2] = bk-veran.deposit-payment[2]. 
    fsl.deposit-payment[3] = bk-veran.deposit-payment[3]. 
    fsl.deposit-payment[4] = bk-veran.deposit-payment[4]. 
    fsl.deposit-payment[5] = bk-veran.deposit-payment[5]. 
    fsl.deposit-payment[6] = bk-veran.deposit-payment[6]. 
    fsl.deposit-payment[7] = bk-veran.deposit-payment[7]. 
    fsl.deposit-payment[8] = bk-veran.deposit-payment[8]. 
    fsl.deposit-payment[9] = - bk-veran.deposit-payment[9]. 
    fsl.payment-date[1] = bk-veran.payment-date[1]. 
    fsl.payment-date[2] = bk-veran.payment-date[2]. 
    fsl.payment-date[3] = bk-veran.payment-date[3]. 
    fsl.payment-date[4] = bk-veran.payment-date[4]. 
    fsl.payment-date[5] = bk-veran.payment-date[5]. 
    fsl.payment-date[6] = bk-veran.payment-date[6]. 
    fsl.payment-date[7] = bk-veran.payment-date[7]. 
    fsl.payment-date[8] = bk-veran.payment-date[8]. 
    fsl.payment-userinit[1] = bk-veran.payment-userinit[1]. 
    fsl.payment-userinit[2] = bk-veran.payment-userinit[2]. 
    fsl.payment-userinit[3] = bk-veran.payment-userinit[3]. 
    fsl.payment-userinit[4] = bk-veran.payment-userinit[4]. 
    fsl.payment-userinit[5] = bk-veran.payment-userinit[5]. 
    fsl.payment-userinit[6] = bk-veran.payment-userinit[6]. 
    fsl.payment-userinit[7] = bk-veran.payment-userinit[7]. 
    fsl.payment-userinit[8] = bk-veran.payment-userinit[8]. 
    fsl.total-paid = bk-veran.total-paid. 
    fsl.segmentcode = bk-veran.segmentcode.
	fsl.raumbezeichnung[8] = bk-func.raumbezeichnung[8]. /*Naufal*/



    IF NUM-ENTRIES(bk-func.zweck[1], CHR(2)) GE 2 THEN
    DO:
          fsl.zweck[1] = ENTRY(2, bk-func.zweck[1], CHR(2)).
    END.
    ELSE
    DO:
          fsl.zweck[1] = bk-func.zweck[1].
    END.

    IF NUM-ENTRIES(bk-veran.payment-userinit[9], CHR(2)) GE 2 THEN
    DO:
          fsl.in-sales = ENTRY(1, bk-veran.payment-userinit[9], CHR(2)). 
          fsl.in-conv =  ENTRY(2, bk-veran.payment-userinit[9], CHR(2)).
    END.
    ELSE
    DO:
          fsl.in-sales =  guest.phonetik3. 
          fsl.in-conv =   guest.phonetik2.
    END.

FIND FIRST bediener WHERE bediener.userinit = fsl.in-sales NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN ASSIGN sales-id = bediener.username.
    /*FIND FIRST guestseg WHERE guestseg.gastnr = curr-gastnr NO-LOCK NO-ERROR.
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
    fsl.segmentcode = segment.segmentcode.
    DISPLAY fsl.segmentcode WITH FRAME page1.*/
FIND FIRST b-storno WHERE b-storno.bankettnr = b1-resnr 
  AND b-storno.breslinnr = b1-resline AND b-storno.gastnr = curr-gastnr NO-LOCK NO-ERROR.
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

FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE bk-reser THEN
DO:
    fsl.cutoff = bk-reser.limitdate.                 
    fsl.raum = bk-reser.raum.                 
END.    

FOR EACH b-storno WHERE b-storno.bankettnr = b1-resnr 
  AND b-storno.breslinnr = b1-resline AND b-storno.gastnr = curr-gastnr NO-LOCK:
    CREATE bstorno.
    BUFFER-COPY b-storno TO bstorno.
END.

FIND FIRST bk-raum WHERE bk-raum.raum = bk-func.raeume[1] NO-LOCK NO-ERROR.
IF AVAILABLE bk-raum THEN venue = bk-raum.bezeich.

FIND FIRST queasy WHERE queasy.KEY = 151 AND queasy.char1 = STRING(bk-func.technik[2]) 
    NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN sob = queasy.char3.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN DO:
    FIND FIRST queasy WHERE queasy.KEY = 146 AND queasy.char1 = STRING(bk-veran.segmentcode) NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN segcode = queasy.char3.
END.

FOR EACH res-line WHERE res-line.gastnr = bk-func.betriebsnr 
    AND res-line.ankunft LE bk-func.datum AND res-line.abreise GE bk-func.datum NO-LOCK:

        ASSIGN rmno      = res-line.zinr + CHR(10) + rmno
               roomrate  = STRING(res-line.zipreis, ">,>>>,>>>,>>9.99") + CHR(10) + roomrate
               ci-date   = res-line.ankunft
               co-date   = res-line.abreise
               sum-room  = sum-room + 1.

      FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN DO:
              ASSIGN rmtype        = zimkateg.kurzbez + CHR(10) + rmtype.

              FIND FIRST zinr-list WHERE zinr-list.room-cat = zimkateg.kurzbez NO-ERROR.
              IF AVAILABLE zinr-list THEN zinr-list.jml-room = zinr-list.jml-room + 1.
              IF NOT AVAILABLE zinr-list THEN DO:
                  CREATE zinr-list.
                  ASSIGN zinr-list.room-cat = zimkateg.kurzbez
                         zinr-list.jml-room = 1.                        
              END.     
      END.
END.

FOR EACH zinr-list:
    ASSIGN sum-room-cat = STRING(zinr-list.jml-room) + CHR(10) + sum-room-cat.
END.
    
