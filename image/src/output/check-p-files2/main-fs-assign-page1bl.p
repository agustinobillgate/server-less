
DEFINE buffer bkfc FOR bk-func. 
DEFINE buffer bkreser FOR bk-reser. 

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
  FIELD in-sales         AS CHARACTER
  FIELD in-conv          AS CHARACTER
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

DEFINE TEMP-TABLE glist 
  FIELD gastnr          LIKE guest.gastnr 
  FIELD karteityp       LIKE guest.karteityp 
  FIELD name            AS CHAR FORMAT "x(40)" 
  FIELD telefon         LIKE guest.telefon 
  FIELD land            LIKE guest.land 
  FIELD plz             LIKE guest.plz 
  FIELD wohnort         LIKE guest.wohnort 
  FIELD adresse1        LIKE guest.adresse1 
  FIELD adresse2        LIKE guest.adresse1 
  FIELD adresse3        LIKE guest.adresse1 
  FIELD namekontakt     LIKE guest.namekontakt 
  FIELD von-datum       LIKE bk-reser.datum 
  FIELD bis-datum       LIKE bk-reser.bis-datum 
  FIELD von-zeit        LIKE bk-reser.von-zeit 
  FIELD bis-zeit        LIKE bk-reser.bis-zeit 
  FIELD rstatus         AS INTEGER
  FIELD fax             LIKE guest.fax
  FIELD firmen-nr       LIKE guest.firmen-nr. 


DEF INPUT  PARAMETER TABLE FOR bkf.
DEF INPUT  PARAMETER TABLE FOR fsl.
DEF INPUT  PARAMETER resnr               AS INT.
DEF INPUT  PARAMETER resline             AS INT.
DEF INPUT  PARAMETER bill-gastnr         AS INT.
DEF INPUT  PARAMETER en-gastnr           AS INT.
DEF INPUT  PARAMETER bkf-veran-nr        AS INT.
DEF INPUT  PARAMETER q3-list-veran-nr    AS INT.
DEF INPUT  PARAMETER q3-list-veran-seite AS INT.
DEF INPUT  PARAMETER rsvsort             AS INT.
DEF INPUT  PARAMETER user-init           AS CHAR.
DEF OUTPUT PARAMETER total-depo          AS DECIMAL. 
DEF INPUT-OUTPUT PARAMETER TABLE FOR glist. 

DEFINE buffer bk-reser1 FOR bk-reser.
DEFINE VARIABLE name-contact AS CHARACTER. 

/*FD Dec 20, 19 - Req Chanti tiket no 7241F8*/
DEFINE VARIABLE flag1 AS LOGICAL NO-UNDO.
DEFINE VARIABLE flag2 AS LOGICAL NO-UNDO.
DEFINE VARIABLE flag3 AS LOGICAL NO-UNDO.
/*End FD*/

FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK NO-ERROR. 
flag3 = AVAILABLE bk-func.

IF bill-gastnr NE 0 THEN 
DO: 
  FIND FIRST bk-veran WHERE bk-veran.veran-nr = bkf-veran-nr EXCLUSIVE-LOCK. 
  DO:
      bk-veran.gastnrver = bill-gastnr.
  END.
  FIND CURRENT bk-veran NO-LOCK. 
  IF bk-veran.rechnr NE 0 THEN 
  DO: 
    FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnrver NO-LOCK.
    FIND FIRST bill WHERE bill.rechnr = bk-veran.rechnr EXCLUSIVE-LOCK. 
    bill.gastnr = bk-veran.gastnrver. 
    bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma. 
    FIND CURRENT bill NO-LOCK. 
  END. 
END. 

IF en-gastnr NE 0 THEN
DO:
  FIND FIRST bk-veran WHERE bk-veran.veran-nr = bkf-veran-nr EXCLUSIVE-LOCK. 
   bk-veran.gastnr = en-gastnr.
  FIND CURRENT bk-veran NO-LOCK.

  /*ITA 010814*/
  FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
  FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE akt-kont THEN name-contact = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
  ELSE name-contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
  FIND FIRST glist WHERE glist.gastnr = bk-veran.gastnr EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE glist THEN 
  DO: 
      FOR EACH glist:
          DELETE glist.
      END.
      CREATE glist.
      glist.gastnr = guest.gastnr. 
      glist.karteityp = guest.karteityp. 
      glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
      glist.adresse1 = guest.adresse1. 
      glist.adresse2 = guest.adresse2. 
      glist.adresse3 = guest.adresse3. 
      glist.telefon = guest.telefon. 
      glist.land = guest.land. 
      glist.plz = guest.plz. 
      glist.wohnort = guest.wohnort. 
      glist.namekontakt = name-contact. 
      glist.rstatus = bk-veran.resstatus.
      glist.fax = guest.fax.
      glist.firmen-nr = guest.firmen-nr.
  END. 
END.

FIND FIRST fsl.
FOR EACH bkf: 
    /* FD Comment
    FIND FIRST bkfc WHERE bkfc.veran-nr = bkf.veran-nr 
      AND bkfc.veran-seite = bkf.veran-seite EXCLUSIVE-LOCK. 
    FIND FIRST bk-reser1 WHERE bk-reser1.veran-nr = bkf.veran-nr AND 
      bk-reser1.veran-resnr = bkf.veran-seite USE-INDEX vernr-ix EXCLUSIVE-LOCK. 
    */

    /*FD Dec 20, 19 - Req Chanti tiket no 7241F8*/
    FIND FIRST bkfc WHERE bkfc.veran-nr = bkf.veran-nr 
      AND bkfc.veran-seite = bkf.veran-seite NO-LOCK NO-ERROR. 
    FIND FIRST bk-reser1 WHERE bk-reser1.veran-nr = bkf.veran-nr AND 
      bk-reser1.veran-resnr = bkf.veran-seite USE-INDEX vernr-ix NO-LOCK NO-ERROR.

    flag1 = AVAILABLE bkfc.
    flag2 = AVAILABLE bk-reser1.
    /*End FD*/

    /*MT
    IF bkfc.c-resstatus[1] NE bkf.c-resstatus[1] THEN 
    DO: 
      MESSAGE "min prog check-oth-rl-sts.p" VIEW-AS ALERT-BOX INFO.
      /*MT
      RUN check-oth-rl-sts.p(bkfc.veran-nr,bkfc.veran-seite,bkfc.r-resstatus[1]). 
      */
    END. 
    */

    IF flag1 AND flag2 THEN
    DO:
        FIND CURRENT bkfc EXCLUSIVE-LOCK.
        FIND CURRENT bk-reser1 EXCLUSIVE-LOCK.

        IF bkfc.zweck[1] NE bkf.zweck[1] THEN 
        DO: 
          FIND FIRST bk-veran WHERE bk-veran.veran-nr = bkf.veran-nr EXCLUSIVE-LOCK. 
          bk-veran.anlass = bkf.zweck[1]. 
          FIND CURRENT bk-veran NO-LOCK. 
        END.
    
        IF fsl.betriebsnr NE 0 THEN bkfc.betriebsnr = fsl.betriebsnr. 
        bkfc.v-kontaktperson[1] = fsl.v-kontaktperson[1]. 
        bkfc.v-telefon = fsl.v-telefon. 
        bkfc.v-telefax = fsl.v-telefax. 
        bkfc.bestellt_durch = fsl.bestellt_durch.
        bkfc.veranstalteranschrift[1] = fsl.veranstalteranschrift[1].
        bkfc.veranstalteranschrift[2] = fsl.veranstalteranschrift[2].
        bkfc.veranstalteranschrift[3] = fsl.veranstalteranschrift[3].
        bkfc.veranstalteranschrift[4] = fsl.veranstalteranschrift[4].
        bkfc.Veranstalteranschrift[5] = fsl.Veranstalteranschrift[5]. /*MU Email*/
        bkfc.technik[1] = fsl.technik[1]. /*MU rsvno hotel*/
        bkfc.technik[2] = fsl.technik[2]. /*MU sob banquet*/
        bkfc.adurch = fsl.adurch. 
        bkfc.rechnungsanschrift[1] = fsl.rechnungsanschrift[1]. 
        bkfc.rechnungsanschrift[2] = fsl.rechnungsanschrift[2]. 
        bkfc.rechnungsanschrift[3] = fsl.rechnungsanschrift[3]. 
        bkfc.rechnungsanschrift[4] = fsl.rechnungsanschrift[4]. 
        bkfc.kontaktperson[1] = fsl.kontaktperson[1]. 
        bkfc.telefon = fsl.telefon. 
        bkfc.telefax = fsl.telefax. 
    
        bkfc.c-resstatus[1] = bkf.c-resstatus[1]. 
        bkfc.r-resstatus[1] = bkf.r-resstatus[1]. 
        bkfc.resstatus = bkf.resstatus. 
        bkfc.raeume[1] = bkf.raeume[1]. 
        bkfc.datum = bkf.datum. 
        bkfc.bis-datum = bkf.datum.         
        bkfc.zweck[1] = TRIM(bkf.zweck[1]) /*+ CHR(2) + fsl.zweck[1]*/.
		bkfc.raumbezeichnung[8] = fsl.raumbezeichnung[8]. /*Naufal*/
        bkfc.rpreis[1] = bkf.rpreis[1]. 
        bkfc.rpersonen[1] = bkf.rpersonen[1]. 
        bkfc.personen = bkf.rpersonen[1]. 
        bkfc.tischform[1] = bkf.tischform[1]. 
        bkfc.dekoration[1] = bkf.dekoration[1]. 
    
        bk-reser1.resstatus = bkfc.r-resstatus[1]. 
        bk-reser1.raum = bkfc.raeume[1]. 
        bk-reser1.datum = bkf.datum. 
        bk-reser1.bis-datum = bkf.datum. 
        bk-reser1.limitdate = fsl.cutoff.
    
        IF bkfc.uhrzeit NE bkf.uhrzeit THEN 
        DO: 
          bkfc.uhrzeit = STRING(bkf.begin-time,"99:99" ) + " - " 
            + STRING(bkf.ending-time,"99:99"). 
          bkfc.uhrzeit = STRING(bkf.begin-time,"99:99" ) + " - " 
            + STRING(bkf.ending-time,"99:99"). 
          bk-reser1.von-zeit = bkf.begin-time. 
          bk-reser1.von-i = bkf.begin-i. 
          bk-reser1.bis-zeit = bkf.ending-time. 
          bk-reser1.bis-i = bkf.ending-i. 
        END. 
    
        fsl.rpersonen[1] = bkf.rpersonen[1]. 
    
        FIND CURRENT bkfc NO-LOCK. 
        FIND CURRENT bk-reser1 NO-LOCK. 
    END.

    /*FD Dec 19, 19 - Req Chanti tiket no 7241F8*/
    FIND FIRST bk-raum WHERE bk-raum.raum = bkf.raeume[1] 
        AND bk-raum.bezeich = bkf.bezeich NO-LOCK NO-ERROR.
    IF AVAILABLE bk-raum THEN
    DO:        
        FIND CURRENT bk-raum EXCLUSIVE-LOCK.
        ASSIGN bk-raum.bezeich = bkf.bezeich.
        FIND CURRENT bk-raum NO-LOCK.

        FIND FIRST queasy WHERE queasy.KEY = 210
            AND queasy.number1 = bkf.veran-nr
            AND queasy.number2 = bkf.veran-seite EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
        END.
    END.
    ELSE
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 210
            AND queasy.number1 = bkf.veran-nr
            AND queasy.number2 = bkf.veran-seite NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY      = 210
                queasy.number1  = bkf.veran-nr
                queasy.number2  = bkf.veran-seite
                queasy.char1    = bkf.bezeich.
        END.
        ELSE
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN
                queasy.KEY      = 210
                queasy.number1  = bkf.veran-nr
                queasy.number2  = bkf.veran-seite
                queasy.char1    = bkf.bezeich.
            FIND CURRENT queasy NO-LOCK.
        END.
    END. 
    /*End FD*/
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
