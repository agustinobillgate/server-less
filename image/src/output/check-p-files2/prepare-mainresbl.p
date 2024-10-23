
DEF TEMP-TABLE t-reservation LIKE reservation.

DEF TEMP-TABLE f-mainres
    FIELD mainres-comment   AS CHAR
    FIELD groupname         AS CHAR
    FIELD main-voucher      AS CHAR
    FIELD contact           AS CHAR
    FIELD main-segm         AS CHAR
    FIELD curr-segm         AS CHAR
    FIELD curr-source       AS CHAR
    FIELD letter            AS CHAR
    FIELD rc-fname          AS CHAR INIT ""
    
    FIELD l-grpnr           AS INTEGER
    FIELD cutoff-days       AS INTEGER
    FIELD contact-nr        AS INTEGER
    FIELD curr-resart       AS INTEGER
    FIELD masterno          AS INTEGER
    FIELD rc-briefnr        AS INTEGER

    FIELD deposit           AS DECIMAL
    FIELD depopay1          AS DECIMAL
    FIELD depopay2          AS DECIMAL
    FIELD depobalan         AS DECIMAL

    FIELD cutoff-date       AS DATE
    FIELD limitdate         AS DATE
    FIELD paydate1          AS DATE
    FIELD paydate2          AS DATE

    FIELD init-fixrate      AS LOGICAL
    FIELD invno-flag        AS LOGICAL
    FIELD master-active     AS LOGICAL
.

DEFINE INPUT PARAMETER res-mode  AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER user-init AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER origCode  AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER gastnr    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER resnr     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER reslinnr  AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER msg-str AS CHAR INIT "".
DEFINE OUTPUT PARAMETER TABLE   FOR f-mainres.
DEFINE OUTPUT PARAMETER TABLE   FOR t-reservation.

DEF VAR    ci-date     AS DATE              NO-UNDO.
DEF VAR    confLetter  AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR    curr-resart AS INTEGER INITIAL 0 NO-UNDO.

DEF BUFFER rline FOR res-line.

CREATE f-mainres.
RUN prepare-mainres.

PROCEDURE prepare-mainres:
DEF VAR segmcode AS CHAR NO-UNDO.

  FIND FIRST htparam WHERE htparam.paramnr = 435 NO-LOCK. 
  f-mainres.rc-briefnr = htparam.finteger. 

  /* Rulita | Fixing for serverless */
  /*FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK NO-ERROR.*/
  FIND FIRST brief WHERE brief.briefnr = f-mainres.rc-briefnr NO-LOCK NO-ERROR.
  IF AVAILABLE brief THEN ASSIGN f-mainres.rc-fname = brief.fname.

  FIND FIRST htparam WHERE paramnr = 440 NO-LOCK. 
  f-mainres.l-grpnr = htparam.finteger. 
  
  FIND FIRST htparam WHERE htparam.paramnr = 264 NO-LOCK.
  f-mainres.init-fixrate = htparam.flogical.

  FIND FIRST htparam WHERE paramnr = 391 NO-LOCK. 
  f-mainres.invno-flag = htparam.flogical. 

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
  ci-date = htparam.fdate. 

  FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK. 
  CREATE t-reservation.
  BUFFER-COPY reservation TO t-reservation.

  IF reslinnr NE 0 THEN
  FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
  ELSE FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
  
  IF res-mode = "new" OR res-mode = "qci" THEN
  DO:
    FIND CURRENT reservation EXCLUSIVE-LOCK.  
    FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
      AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE guestseg THEN 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
    ASSIGN 
      reservation.gastnr        = guest.gastnr 
      reservation.gastnrherk    = guest.gastnr 
      reservation.useridanlage  = user-init 
      reservation.name          = guest.name + ", " 
                                + guest.vorname1 + guest.anredefirma 
      reservation.resart        = 1 
      reservation.resdat        = ci-date 
      reservation.insurance     = f-mainres.init-fixrate 
                               /* fixed rate during whole stay */
    .
    IF guest.segment3 NE 0 THEN reservation.resart = guest.segment3.
    IF AVAILABLE guestseg THEN reservation.segmentcode = guestseg.segmentcode. 
  END.

  IF res-mode = "new" OR res-mode = "qci" THEN
  DO:
      FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = origCode 
          NO-LOCK NO-ERROR.
      IF AVAILABLE queasy AND ENTRY(1, queasy.char3, ";") NE "" THEN
      DO:
          FIND FIRST segment WHERE segment.bezeich = ENTRY(1, queasy.char3, ";")
              NO-LOCK NO-ERROR.
          /*MT 05/07/14 */
          IF AVAILABLE segment THEN
          DO:
              /*IF res-mode EQ "modify" THEN
              DO:*/
                  FIND FIRST rline WHERE rline.resnr = resnr AND rline.reslinnr NE reslinnr
                      AND rline.zipreis GT 0
                      NO-LOCK NO-ERROR.
                  IF res-mode EQ "modify" AND NOT AVAILABLE rline 
                      AND res-line.gratis GT 0 AND res-line.erwachs = 0
                      AND res-line.zipreis = 0 THEN.
                  ELSE IF (res-mode EQ "modify" AND AVAILABLE rline) 
                      OR (res-mode NE "modify")
                      THEN
                  DO:
                      FIND CURRENT reservation EXCLUSIVE-LOCK.  
                      reservation.segmentcode = segment.segmentcode.
                  END.
              /*END.*/

          END.

          /*MT 05/07/14 
          FIND FIRST rline WHERE rline.resnr = resnr AND rline.reslinnr NE reslinnr
              AND rline.zipreis GT 0
              NO-LOCK NO-ERROR.
          IF res-mode EQ "modify" THEN
          DO:
              IF NOT AVAILABLE rline AND res-line.gratis GT 0 AND res-line.erwachs = 0
                  AND res-line.zipreis = 0 THEN.
              ELSE IF AVAILABLE segment THEN 
              DO:    
                  FIND CURRENT reservation EXCLUSIVE-LOCK.  
                  reservation.segmentcode = segment.segmentcode.
              END.
          END.
          */
      END.
  END.

  f-mainres.cutoff-days = reservation.point-resnr.
  IF f-mainres.cutoff-days NE 0 THEN 
    f-mainres.cutoff-date = res-line.ankunft - f-mainres.cutoff-days.
  ASSIGN
    f-mainres.mainres-comment = reservation.bemerk 
    f-mainres.groupname       = reservation.groupname
    f-mainres.contact-nr      = reservation.kontakt-nr
    f-mainres.main-voucher    = reservation.vesrdepot
    f-mainres.limitdate       = reservation.limitdate
    f-mainres.deposit         = reservation.depositgef
    f-mainres.depopay1        = reservation.depositbez
    f-mainres.depopay2        = reservation.depositbez2
    f-mainres.paydate1        = reservation.zahldatum
    f-mainres.paydate2        = reservation.zahldatum2
    f-mainres.depobalan       = f-mainres.deposit - f-mainres.depopay1 
                              - f-mainres.depopay2
  .
  IF f-mainres.depopay1 = 0 THEN f-mainres.paydate1 = ?.
  IF f-mainres.depopay2 = 0 THEN f-mainres.paydate2 = ?.

  IF f-mainres.contact-nr NE 0 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.kontakt-nr = f-mainres.contact-nr
      AND akt-kont.gastnr = gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN 
      f-mainres.contact = akt-kont.NAME + ", " + akt-kont.vorname
                        + CHR(2) + akt-kont.telefon
                        + CHR(2) + akt-kont.durchwahl.
  END.

  IF reservation.segmentcode GT 0 THEN
  DO:
    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
      NO-LOCK.
    ASSIGN 
        segmcode = REPLACE(segment.bezeich, ",", "/")
        f-mainres.curr-segm  = STRING(segment.segmentcode) 
          + " " + segmcode + ";". 
  END.

  FOR EACH guestseg WHERE guestseg.gastnr = reservation.gastnr NO-LOCK, 
    FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
    AND segment.betriebsnr LE 2
    AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 /* $$0 --> SEGM not active */
    NO-LOCK BY segment.betriebsnr BY segment.segmentcode:
    IF guestseg.segmentcode EQ reservation.segmentcode THEN .
    ELSE
    ASSIGN 
        segmcode             = REPLACE(segment.bezeich, ",", "/")
        f-mainres.curr-segm  = f-mainres.curr-segm
                             + STRING(segment.segmentcode) 
                             + " " + segmcode + ";"
    . 
    IF guestseg.reihenfolge = 1 THEN 
        f-mainres.main-segm = STRING(segment.segmentcode) + " " + segmcode. 
  END.

  FOR EACH segment WHERE segment.betriebsnr LE 2 
    AND segment.segmentcode NE reservation.segmentcode 
    AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 /* $$0 --> SEGM not active */
    NO-LOCK BY segment.betriebsnr BY segment.segmentcode:
    FIND FIRST guestseg WHERE guestseg.gastnr = reservation.gastnr
      AND guestseg.segmentcode = segment.segmentcode NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guestseg THEN
    ASSIGN 
        segmcode = REPLACE(segment.bezeich, ",", "/")
        f-mainres.curr-segm  = f-mainres.curr-segm
          + STRING(segment.segmentcode) + " " + segmcode + ";". 
  END.
  
  IF reservation.resart NE 0 THEN
  DO:
    FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart 
      AND sourccod.betriebsnr = 0 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE sourccod OR (AVAILABLE sourccod AND sourccod.betriebsnr NE 0) THEN
     FIND FIRST sourccod WHERE sourccod.betriebsnr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE sourccod THEN
    DO:
      ASSIGN
        curr-resart           = sourccod.source-code
        f-mainres.curr-source = STRING(sourccod.source-code) 
                              + " " + sourccod.bezeich + ";".
        f-mainres.curr-resart = sourccod.source-code          
      .
    END.
  END.
  FOR EACH sourccod WHERE sourccod.betriebsnr = 0
    AND sourccod.source-code NE curr-resart NO-LOCK BY sourccod.source-cod:
    f-mainres.curr-source = f-mainres.curr-source
        + STRING(sourccod.source-code) + " " + sourccod.bezeich + ";". 
  END.

  IF reservation.briefnr NE 0 THEN
  DO:
    FIND FIRST brief WHERE brief.briefnr = reservation.briefnr
      NO-LOCK NO-ERROR. 
    IF AVAILABLE brief THEN 
      f-mainres.letter = STRING(brief.briefnr) + " " 
                      + brief.briefbezeich + ";".
  END.
  ELSE
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = 431 NO-LOCK.
    IF htparam.feldtyp = 1 THEN confLetter = htparam.finteger.
    FIND FIRST brief WHERE brief.briefnr = confLetter NO-LOCK NO-ERROR. 
    IF AVAILABLE brief THEN f-mainres.letter = STRING(brief.briefnr) 
        + " " + brief.briefbezeich + ";".
  END.
  
  FOR EACH brief WHERE brief.briefkateg = l-grpnr 
    AND brief.briefnr NE reservation.briefnr 
    AND brief.briefnr NE confLetter NO-LOCK BY brief.briefnr:
    f-mainres.letter = f-mainres.letter + STRING(brief.briefnr) 
      + " " + brief.briefbezeich + ";". 
  END.

  FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR.
  IF AVAILABLE master THEN 
  ASSIGN 
      f-mainres.master-active = master.ACTIVE
      f-mainres.masterno      = master.rechnr
  .
  FIND CURRENT reservation NO-LOCK.  
END.

