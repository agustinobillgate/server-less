
DEFINE TEMP-TABLE reslin-list  LIKE res-line. 
DEFINE TEMP-TABLE prev-resline LIKE res-line.
DEFINE TEMP-TABLE now-resline  LIKE res-line.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER gastNo       AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER res-mode     AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER curr-segm    AS CHAR     NO-UNDO. /* screen-value */
DEFINE INPUT PARAMETER curr-source  AS CHAR     NO-UNDO. /* screen-value */
DEFINE INPUT PARAMETER currency     AS CHAR     NO-UNDO. /* screen-value */
DEFINE INPUT PARAMETER zikat-screen AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER memo-zinr    AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER guestname    AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER origcontcode AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER contcode     AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER marknr       AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER rm-bcol      AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER inactive-flag AS LOGICAL NO-UNDO.

DEFINE INPUT PARAMETER TABLE FOR reslin-list.
DEFINE INPUT PARAMETER TABLE FOR prev-resline.

DEFINE OUTPUT PARAMETER error-number    AS INTEGER INIT 0   NO-UNDO.
DEFINE OUTPUT PARAMETER still-error     AS LOGICAL INIT YES NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR    INIT ""  NO-UNDO.
DEFINE OUTPUT PARAMETER pswd-str        AS CHAR    INIT ""  NO-UNDO.

DEFINE INPUT-OUTPUT PARAMETER zikatstr  AS CHAR. 
DEFINE OUTPUT PARAMETER flag1           AS LOGICAL INIT NO  NO-UNDO.
DEFINE OUTPUT PARAMETER ci-date1        AS DATE             NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

DEFINE VARIABLE ci-date    AS DATE                  NO-UNDO.
DEFINE VARIABLE min-stay   AS INTEGER INIT 0        NO-UNDO.
DEFINE VARIABLE max-stay   AS INTEGER INIT 0        NO-UNDO.
DEFINE VARIABLE min-adv    AS INTEGER INIT 0        NO-UNDO.
DEFINE VARIABLE max-adv    AS INTEGER INIT 0        NO-UNDO.
DEFINE VARIABLE msg-str1   AS CHAR INIT ""          NO-UNDO.

DEFINE VARIABLE zinr-ecode AS CHAR FORMAT "x(40)"   NO-UNDO EXTENT 6. 
  zinr-ecode[1] = translateExtended( "Wrong room number for selected room catagory", lvCAREA, "":U). 
  zinr-ecode[2] = translateExtended( "Room status: Out-of-order", lvCAREA, "":U). 
  zinr-ecode[3] = translateExtended( "Room already blocked", lvCAREA, "":U). 
  zinr-ecode[4] = translateExtended( "Room status: Vacant dirty", lvCAREA, "":U). 
  zinr-ecode[5] = translateExtended( "Room status: Off-Market", lvCAREA, "":U). 
  zinr-ecode[6] = translateExtended( "Room Sharer already checked-in.", lvCAREA, "":U). 

FIND FIRST reslin-list.
FIND FIRST prev-resline NO-ERROR.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
/*   Put this in GUI part 
  ASSIGN memo-zinr.
  IF (reslin-list.resstatus = 11 OR reslin-list.resstatus = 13) 
    AND (reslin-list.erwachs GT 0 OR reslin-list.gratis GT 0) 
    AND reslin-list.zipreis = 0 THEN 
  ASSIGN 
    reslin-list.erwachs = 0
    reslin-list.gratis  = 0
  . 
  DISABLE btn-help WITH FRAME frame1. 
*/
RUN check-go.

PROCEDURE check-go: 
DEFINE VARIABLE qty             AS INTEGER  NO-UNDO. 
DEFINE VARIABLE max-comp        AS INTEGER  NO-UNDO. 
DEFINE VARIABLE com-rm          AS INTEGER  NO-UNDO.
DEFINE VARIABLE max-com         AS INTEGER  NO-UNDO.
DEFINE VARIABLE max-rate        AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE check-allotment AS LOGICAL INITIAL NO. 
DEFINE VARIABLE its-wrong       AS LOGICAL  NO-UNDO.
DEFINE VARIABLE wrong-room      AS LOGICAL  NO-UNDO.
DEFINE VARIABLE datum           AS DATE     NO-UNDO.
DEFINE VARIABLE from-date       AS DATE     NO-UNDO. 
DEFINE VARIABLE to-date         AS DATE     NO-UNDO. 
DEFINE VARIABLE diff-str        AS CHAR     NO-UNDO.

DEFINE VARIABLE error-code      AS INTEGER INIT 0  NO-UNDO.
DEFINE VARIABLE incl-allotment  AS LOGICAL INITIAL NO. 
DEFINE VARIABLE b-dummy         AS LOGICAL.
DEFINE VARIABLE overbook        AS LOGICAL.
DEFINE VARIABLE overmax         AS LOGICAL.
DEFINE VARIABLE overanz         AS INTEGER.
DEFINE VARIABLE overdate        AS DATE.
DEFINE VARIABLE billdate        AS DATE. 

DEFINE BUFFER rline   FOR res-line. 
DEFINE BUFFER arr     FOR arrangement. 
DEFINE BUFFER gmember FOR guest.

  FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 

  FIND FIRST htparam WHERE htparam.paramnr = 1108 NO-LOCK.   
  ASSIGN max-rate = htparam.fdecimal. 

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
  ASSIGN ci-date = htparam.fdate.

  FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr 
   AND res-line.reslinnr = reslin-list.reslinnr NO-LOCK. 

  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" 
      THEN qty = reslin-list.zimmeranz. 
  ELSE 
  DO:
    IF res-mode = "inhouse" THEN
    DO:
      qty = 0.
      IF reslin-list.resstatus = 6 AND res-line.resstatus = 6 THEN
        qty = reslin-list.zimmeranz - res-line.zimmeranz. 
      ELSE IF reslin-list.resstatus = 6 AND res-line.resstatus = 13 THEN
        qty = reslin-list.zimmeranz.
    END.
    ELSE
    DO:
      qty = 0.
      IF (reslin-list.resstatus LE 2 OR reslin-list.resstatus = 5) 
        AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN
        qty = reslin-list.zimmeranz - res-line.zimmeranz. 
      ELSE IF (reslin-list.resstatus LE 2 OR reslin-list.resstatus = 5) 
        AND (res-line.resstatus = 3 OR res-line.resstatus = 4
        OR res-line.resstatus = 11) THEN qty = reslin-list.zimmeranz.
    END.
  END.

  IF reslin-list.erwachs GT 0 AND reslin-list.gratis GT 0 THEN
  DO:
    ASSIGN error-number = 1.
    RETURN. 
  END.

  IF (res-mode = "inhouse" OR res-mode = "qci") AND reslin-list.zinr EQ "" THEN 
  DO: 
    ASSIGN
      msg-str = translateExtended ("Room Number not yet selected.", lvCAREA, "":U) 
      error-number = 30
    . 
    RETURN. 
  END. 

  FIND FIRST arrangement WHERE arrangement.arrangement =
    reslin-list.arrangement NO-LOCK NO-ERROR.
  IF NOT AVAILABLE arrangement THEN
  DO:
      ASSIGN
        msg-str = translateExtended ("No such Arrangement Code:", lvCAREA, "":U)
          + " " + reslin-list.arrangement.
        error-number = 34
      . 
      RETURN.
  END.

  IF arrangement.waeschewechsel NE 0 AND reslin-list.erwachs NE
     arrangement.waeschewechsel THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Wrong Arrangement / Adult", lvCAREA, "":U) 
      error-number = 41
    .
    RETURN.
  END.

  IF arrangement.handtuch NE 0 AND reslin-list.anztage NE
     arrangement.handtuch THEN
  DO:
     ASSIGN
       msg-str = translateExtended ("Wrong Arrangement / Night of Stay", lvCAREA, "":U) 
       error-number = 42 
     .
     RETURN. 
  END.

  FIND FIRST zimkateg WHERE zimkateg.kurzbez = zikatstr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE zimkateg THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("No such Room Type.", lvCAREA, "":U) 
      error-number = 43
    .
    RETURN.
  END.

  IF (reslin-list.active-flag = 0) AND (reslin-list.ankunft LT ci-date) THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Wrong check-in date!", lvCAREA, "":U)
      error-number = 2
    .
    RETURN. 
  END.

  IF reslin-list.abreise LT ci-date THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Wrong check-out date!", lvCAREA, "":U)
      error-number = 3
    .
    RETURN. 
  END.

  IF reslin-list.abreise LT reslin-list.ankunft THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Wrong date!", lvCAREA, "":U)
      error-number = 4
    .
    RETURN.
  END.

  /*MT
  IF reslin-list.betriebsnr = 0 THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Room rate currency not defined!", lvCAREA, "":U)
      error-number = 5
    .
    RETURN. 
  END.
  */

  IF curr-segm = "" THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Segment Code not defined.", lvCAREA, "":U) 
      error-number = 6
    .
    RETURN. 
  END.

  FIND FIRST segment WHERE segment.segmentcode =
    INTEGER(SUBSTR(curr-segm, 1, INDEX(curr-segm," "))) 
    NO-LOCK NO-ERROR.
  IF AVAILABLE segment AND segment.betriebsnr GT 0 THEN
  DO:
    IF reslin-list.erwachs GT 0 THEN
    DO:
      ASSIGN  
        msg-str = translateExtended ("Compliment / HU Segment but adult > 0.", lvCAREA, "":U) 
        error-number = 7
      .
      RETURN. 
    END.
    FIND FIRST rline WHERE rline.resnr = reslin-list.resnr
      AND rline.reslinnr NE reslin-list.reslinnr
      AND rline.active-flag LE 1 AND rline.zipreis GT 0 
      NO-LOCK NO-ERROR.
    IF AVAILABLE rline OR reslin-list.zipreis GT 0 THEN
    DO:
      ASSIGN
        msg-str = translateExtended ("Reservation member found with Rate > 0.",lvCAREA,"") 
        error-number = 8
      .
      RETURN.    
    END.
  END.

  IF curr-source = "" THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Source of Booking not defined.", lvCAREA, "":U) 
      error-number = 9
    .
    RETURN. 
  END.

  IF reslin-list.zimmeranz = 0 THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Wrong Room Quantity!", lvCAREA, "":U) 
      error-number = 10
    . 
    RETURN. 
  END.
  ELSE IF reslin-list.zimmeranz GT 1 AND reslin-list.zinr NE "" THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Room number already assigned.", lvCAREA, "":U) 
      error-number = 11
    .
    RETURN. 
  END.

  IF max-rate NE 0 AND reslin-list.zipreis GT 0 THEN 
  DO: 
    IF reslin-list.betriebsnr GT 0 THEN FIND FIRST waehrung WHERE 
      waehrung.waehrungsnr = reslin-list.betriebsnr NO-LOCK NO-ERROR. 
    ELSE 
    DO: 
      FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
      FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar 
        NO-LOCK NO-ERROR. 
    END. 
    IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
    IF reslin-list.zipreis * exchg-rate GT max-rate THEN 
    DO: 
      ASSIGN
        msg-str = translateExtended ("Room Rate incorrect / too large! Check currency.",lvCAREA, "":U) 
        error-number = 12
      . 
      RETURN. 
    END. 
  END. 

  IF inactive-flag THEN
  DO:
      IF reslin-list.zipreis GT 0 THEN
      DO:
          ASSIGN
            msg-str = translateExtended ("Inactive Room! Room Rate must be 0.", lvCAREA, "":U)
            error-number = 45
          .
          /*APPLY "entry" TO reslin-list.zipreis IN FRAME frame1. 
          still-error = YES.*/
          RETURN. 
      END.
  END.

  IF reslin-list.resstatus = 6 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = res-line.resnr
          AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr
              AND bill-line.bill-datum EQ billdate 
              AND bill-line.zinr = reslin-list.zinr
              AND bill-line.artnr = 99 NO-LOCK NO-ERROR.
          IF AVAILABLE bill-line AND bill-line.betrag NE reslin-list.zipreis THEN
          DO:
              ASSIGN
                  msg-str = translateExtended ("Room charge has been posted for this Rsv.", lvCAREA, "":U)
                  error-number = 46.
              /*APPLY "entry" TO reslin-list.zipreis IN FRAME frame1. 
              still-error = YES.*/
              RETURN. 
          END.
      END.
  END.
 
  IF reslin-list.zimmerfix AND reslin-list.resstatus NE 13 THEN
  DO:
    IF reslin-list.zinr NE "" THEN
    DO:
      FIND FIRST rline WHERE rline.resnr = reslin-list.resnr
        AND rline.reslinnr NE reslin-list.reslinnr
            AND rline.resstatus = 6 AND rline.zinr = reslin-list.zinr
            NO-LOCK NO-ERROR.
        its-wrong = AVAILABLE rline.
      IF NOT its-wrong THEN
      DO:
        FIND FIRST rline WHERE rline.zinr = reslin-list.zinr
          AND rline.active-flag = 1 AND rline.resnr NE reslin-list.resnr
          NO-LOCK NO-ERROR.
        its-wrong = AVAILABLE rline.
      END.
    END.
    IF its-wrong THEN
    DO:
      ASSIGN
        msg-str = translateExtended ("Wrong Status as Room Sharer.", lvCAREA, "":U) 
        error-number = 13
      .
      RETURN. 
    END.
  END.

  IF (reslin-list.resstatus = 11 OR reslin-list.resstatus = 13)
     AND (reslin-list.erwachs GT 0) AND (reslin-list.zipreis = 0) THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Number of Adult for Room Sharer should be 0.", lvCAREA, "":U) 
      error-number = 14
    . 
    RETURN. 
  END.

  IF currency = "" THEN 
  DO: 
    ASSIGN
      msg-str = translateExtended ("Currency not defined.", lvCAREA, "":U) 
      error-number = 15
    . 
    RETURN. 
  END. 
/* 
  FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
  IF htparam.flogical AND reslin-list.ankunft = ci-date THEN 
  DO: 
    ASSIGN 
      msg-str = translateExtended ("Night Audit is running, transaction not possible.",lvCAREA, "":U) 
      error-number = 16
    . 
    RETURN. 
  END. 
*/
  IF (reslin-list.zipreis GT 0) AND (reslin-list.gratis GT 0) THEN
  DO:
    ASSIGN
      msg-str = translateExtended ("Rate > 0 can not be applied to compliment guest.",lvCAREA,"") 
      error-number = 17
    . 
    RETURN.
  END.
   
 
  IF reslin-list.erwachs = 0 AND reslin-list.kind1 = 0 
    AND reslin-list.kind2 = 0 AND reslin-list.zipreis GT 0 THEN 
  DO: 
    ASSIGN
      msg-str = translateExtended ("Input incorrect: Adult = 0 but Room-Rate > 0.", lvCAREA, "":U) 
      error-number = 18
    . 
    RETURN. 
  END. 
 
  IF (reslin-list.erwachs = 0 AND reslin-list.kind1 = 0 
      AND reslin-list.kind2 = 0 AND reslin-list.gratis = 0) 
      AND reslin-list.resstatus NE 11 
      AND reslin-list.resstatus NE 13 THEN 
  DO: /*MT*/
    ASSIGN
      msg-str = translateExtended ("Input of PAX incorrect.", 
                                   lvCAREA, "":U)
      error-number = 44.
    RETURN. 
  END. 

  IF reslin-list.gratis GT 0 AND reslin-list.zipreis GT 0 THEN 
  DO: 
    ASSIGN 
      msg-str = translateExtended ("Input incorrect: Compliment guest but Room-Rate > 0.", lvCAREA, "":U) 
      error-number = 19
    . 
    RETURN. 
  END. 
 
  IF memo-zinr NE "" THEN
  DO:
    FIND FIRST zimmer WHERE zimmer.zinr = memo-zinr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE zimmer THEN
    DO:
      ASSIGN
        msg-str = translateExtended ("Wrong Memo RmNo / no such room number.", lvCAREA, "":U) 
        error-number = 20
      . 
      RETURN. 
    END.
  END.

  IF rm-bcol NE 15 AND reslin-list.zinr = "" THEN 
  DO: 
    ASSIGN
      msg-str = translateExtended ("Off-Market Room number can not be changed.", lvCAREA, "":U) 
      error-number = 21
    . 
    RETURN. 
  END. 
 
  ELSE IF rm-bcol NE 15 AND reslin-list.ankunft NE res-line.ankunft THEN 
  DO: 
    FIND FIRST outorder WHERE outorder.zinr = reslin-list.zinr 
      AND outorder.betriebsnr = reslin-list.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE outorder AND outorder.gespstart LT outorder.gespend THEN 
    DO: 
      ASSIGN
        from-date = reslin-list.ankunft - outorder.gespende + outorder.gespstart
        to-date   = reslin-list.abreise
      . 
      IF from-date NE to-date THEN 
      FIND FIRST rline WHERE rline.active-flag LE 1 
        AND rline.resnr NE reslin-list.resnr AND 
       ((rline.ankunft GE from-date AND rline.ankunft LE to-date) OR 
       (rline.abreise GE from-date AND rline.abreise LE to-date) OR 
       (from-date GE rline.ankunft AND to-date LE rline.abreise)) 
        AND rline.zinr EQ reslin-list.zinr NO-LOCK NO-ERROR. 
      ELSE 
      FIND FIRST rline WHERE rline.active-flag LE 1 
        AND rline.resnr NE reslin-list.resnr AND 
       (from-date GT rline.ankunft AND from-date LT rline.abreise) 
       AND rline.zinr EQ reslin-list.zinr NO-LOCK NO-ERROR. 
 
      IF AVAILABLE rline THEN 
      DO: 
        ASSIGN
          msg-str = translateExtended ("Attention RmNo : ", lvCAREA, "":U) + STRING(rline.zinr) + CHR(10)
           + translateExtended ("Reservation exists under ResNo = ", lvCAREA, "":U) 
           + STRING(rline.resnr) + CHR(10)
           + translateExtended ("Guest Name = ", lvCAREA, "":U) + rline.NAME + CHR(10)
           + translateExtended ("Arrival / Departure : ", lvCAREA, "":U) 
           + STRING(rline.ankunft) + " / " + STRING(rline.abreise) + CHR(10)
          error-number = 22
        . 
        RETURN. 
      END. 
    END. 
  END. 
 
  IF zikatstr = "" THEN 
  DO: 
    ASSIGN
      msg-str = translateExtended ("Room Type not yet defined.", lvCAREA, "":U) 
      error-number = 23
    . 
    RETURN. 
  END. 
 
  IF reslin-list.arrangement = "" THEN 
  DO: 
    ASSIGN
      msg-str = translateExtended ("Arrangement not yet defined.", lvCAREA, "":U) 
      error-number = 24
    . 
    RETURN. 
  END. 
 
  FIND FIRST guest-pr WHERE guest-pr.gastnr = gastNo
    NO-LOCK NO-ERROR. 
  IF AVAILABLE guest-pr AND reslin-list.reserve-int = 0 THEN 
  DO:
    FIND FIRST ratecode WHERE ratecode.code = guest-pr.CODE 
        AND reslin-list.ankunft GE ratecode.startperiode
        AND reslin-list.ankunft LE ratecode.endperiode NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
      ASSIGN
        msg-str = translateExtended ("Market Segment not yet defined.", lvCAREA, "":U) 
        error-number = 25
      . 
      RETURN. 
    END.
  END.

  RUN check-min-maxstay.
  IF error-number GT 0 THEN RETURN.

  IF reslin-list.active-flag = 0 THEN
  DO:
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = reslin-list.resnr 
      AND reslin-queasy.reslinnr = reslin-list.reslinnr 
      AND reslin-queasy.date1 LE reslin-list.ankunft 
      AND reslin-queasy.date2 GE reslin-list.ankunft NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy AND reslin-queasy.char1 NE "" 
       AND reslin-queasy.char1 NE reslin-list.arrangement THEN
    DO:
      ASSIGN
        msg-str = msg-str + CHR(2) 
          + translateExtended ("Wrong arrangement in AdHoc Rate setup, fix it now.", lvCAREA, "":U) 
        error-number = 26
      . 
      RETURN.     
    END.
  END.

  IF res-mode = "inhouse" THEN
  DO:
    FIND FIRST rline WHERE rline.active-flag = 0
        AND rline.zinr = reslin-list.zinr
        AND rline.ankunft GE reslin-list.ankunft
        AND rline.ankunft LT reslin-list.abreise 
        AND rline.resnr NE reslin-list.resnr
        AND rline.resstatus NE 11 NO-LOCK NO-ERROR.
    IF AVAILABLE rline THEN
    DO:
      ASSIGN
        msg-str = msg-str + CHR(2)
                + translateExtended ("Reservation found for the same room within the period of stay:",lvCAREA,"") + CHR(10)
                + rline.NAME + " - " + translateExtended("RmNo",lvCAREA,"") + " " + rline.zinr + CHR(10)
                + STRING(rline.ankunft) + " - " + STRING(rline.abreise) + CHR(10)
        error-number = 27
      . 
      RETURN.
    END.
  END.

  /* check fixed-rate */
  IF reslin-list.ankunft LT reslin-list.abreise THEN 
  DO:
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = res-line.resnr 
      AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN 
    DO:
      datum = reslin-list.abreise - 1. 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND datum GE reslin-queasy.date1 
        AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslin-queasy THEN 
      DO:
        ASSIGN
          msg-str = msg-str + CHR(2) 
             + translateExtended ("Fixed-Rate Period incorrect, re-check it.", lvCAREA, "":U) 
          error-number = 28
        .
        RETURN.
      END.
    END.
  END.
 
  IF reslin-list.kontignr NE 0 AND reslin-list.resstatus NE 11 
    AND reslin-list.resstatus NE 13 THEN 
  DO: 
    IF reslin-list.kontignr NE res-line.kontignr THEN check-allotment = YES. 
    IF reslin-list.ankunft LT res-line.ankunft THEN check-allotment = YES. 
    IF reslin-list.ankunft GE res-line.abreise THEN check-allotment = YES. 
    IF reslin-list.abreise LE res-line.ankunft THEN check-allotment = YES. 
    IF reslin-list.abreise GT res-line.abreise THEN check-allotment = YES. 
    IF reslin-list.zimmeranz GT res-line.zimmeranz THEN check-allotment = YES. 
    IF reslin-list.kontignr GT 0 THEN 
    FIND FIRST kontline WHERE kontline.kontignr = reslin-list.kontignr NO-LOCK NO-ERROR.
    ELSE 
    FIND FIRST kontline WHERE kontline.kontignr = - reslin-list.kontignr NO-LOCK NO-ERROR.
    IF AVAILABLE kontline AND kontline.zikatnr NE 0 AND
      (reslin-list.zikatnr NE res-line.zikatnr) THEN check-allotment = YES. 
  END. 
 
  IF check-allotment THEN 
  DO: 
    IF res-mode = "inhouse" THEN 
    RUN allot-overbookbl.p(pvILanguage, res-mode, reslin-list.resnr, 
      reslin-list.reslinnr, 
      reslin-list.kontignr, reslin-list.zikatnr, reslin-list.setup, 
      reslin-list.arrangement, reslin-list.erwachs, ci-date, 
      reslin-list.abreise, reslin-list.zimmeranz, user-init,
      OUTPUT its-wrong, OUTPUT msg-str). 
    ELSE 
    RUN allot-overbookbl.p(pvILanguage, res-mode, reslin-list.resnr, 
      reslin-list.reslinnr, 
      reslin-list.kontignr, reslin-list.zikatnr, reslin-list.setup, 
      reslin-list.arrangement, reslin-list.erwachs, reslin-list.ankunft, 
      reslin-list.abreise, reslin-list.zimmeranz, user-init,
      OUTPUT its-wrong, OUTPUT msg-str). 
    
    IF its-wrong THEN
    DO: 
      IF NOT msg-str MATCHES ("*&Q*") THEN
        ASSIGN error-number = 29.
      ELSE ASSIGN error-number = 50.
      RETURN. 
    END. 
  END. 
  
  IF zikat-screen NE zikatstr THEN
  DO:
    RUN check-bedsetup. 
    RETURN.
  END.

  IF res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" OR 
    ((res-mode = "modify" OR res-mode = "split" OR res-mode = "inhouse") 
     AND (res-line.zipreis NE 0 AND reslin-list.zipreis = 0) OR 
     (res-line.zimmeranz NE reslin-list.zimmeranz)) THEN 
  DO: 
    RUN check-complimentbl.p(pvILanguage, reslin-list.resnr, 
      reslin-list.reslinnr, 
      reslin-list.gastnr, reslin-list.ankunft, 
      marknr, reslin-list.zikatnr, reslin-list.arrangement, 
      reslin-list.zimmeranz, reslin-list.zipreis, 
      OUTPUT its-wrong, OUTPUT com-rm, OUTPUT max-comp,
      OUTPUT pswd-str, OUTPUT msg-str). 
    IF its-wrong OR pswd-str NE "" OR msg-str NE "" THEN 
    DO:
      ASSIGN error-number = 33.
      RETURN. 
    END. 
  END. 

/** check IF the record has been checked-in BY other user!! **/ 
  IF reslin-list.active-flag = 0 THEN 
  DO: 
    FIND FIRST rline WHERE rline.resnr = reslin-list.resnr 
      AND rline.reslinnr = reslin-list.reslinnr NO-LOCK. 
    IF rline.active-flag EQ 1 THEN 
    DO: 
      ASSIGN
        msg-str = msg-str + CHR(2) 
          + translateExtended ("Guest checked-in, cancel your changes.", lvCAREA, "":U) 
        error-number = 35
      . 
      RETURN. 
    END. 
  END.
  
  /****
  ASSIGN overmax = NO. 
  IF reslin-list.ankunft  NE res-line.ankunft   OR 
    reslin-list.abreise   NE res-line.abreise   OR 
    reslin-list.zikatnr   NE res-line.zikatnr   OR 
    reslin-list.zimmeranz NE res-line.zimmeranz OR
    reslin-list.resstatus NE res-line.resstatus THEN
  DO: 
    IF res-mode = "inhouse"  AND reslin-list.resstatus NE 13 THEN 
    RUN res-overbookbl.p(pvILanguage, INPUT res-mode, INPUT reslin-list.resnr,
                         reslin-list.reslinnr, INPUT ci-date, reslin-list.abreise,
                         INPUT qty, INPUT zikatstr, INPUT reslin-list.setup,
                         INPUT NO, OUTPUT overbook, OUTPUT overmax,
                         OUTPUT overanz, OUTPUT overdate, OUTPUT incl-allotment,
                         OUTPUT msg-str).
    ELSE IF reslin-list.resstatus LE 2 OR reslin-list.resstatus = 5 THEN 
    RUN res-overbookbl.p(pvILanguage, INPUT res-mode, INPUT reslin-list.resnr,
                         reslin-list.reslinnr, INPUT reslin-list.ankunft,
                         reslin-list.abreise, INPUT qty, INPUT zikatstr,
                         INPUT reslin-list.setup, INPUT NO, OUTPUT overbook,
                         OUTPUT overmax, OUTPUT overanz, OUTPUT overdate,
                         OUTPUT incl-allotment, OUTPUT msg-str). 
  END. 
 
  IF overmax AND (SUBSTR(bediener.perm, 56, 1) LT "2") THEN 
  DO:
    IF incl-allotment THEN 
    ASSIGN
      msg-str = msg-str + CHR(2) 
            + translateExtended ("Overbooking found on : ", lvCAREA, "":U) 
            + STRING(overdate) + CHR(10)
            + translateExtended ("Maxium Overbooking : ", lvCAREA, "":U) 
            + STRING(zimkateg.overbook) + CHR(10) 
            + translateExtended ("Actual Overbooking incl. Allotment/Global Reservation: ", lvCAREA, "":U) 
            + STRING(overanz).
    ELSE 
    ASSIGN
      msg-str = msg-str + CHR(2) 
        + translateExtended ("Overbooking found on : ", lvCAREA, "":U) 
        + STRING(overdate) + CHR(10)
        + translateExtended ("Maxium Overbooking : ", lvCAREA, "":U) 
        + STRING(zimkateg.overbook) + CHR(10) 
        + translateExtended ("Actual Overbooking : ", lvCAREA, "":U) 
        + STRING(overanz). 
    error-number  = 37. 
    RETURN. 
  END. 
 
  ELSE IF overmax AND (SUBSTR(bediener.perm, 56, 1) GE "2") THEN 
    ASSIGN
      msg-str = msg-str + CHR(2) + "&W"
        + translateExtended ("Overbooking found on : ", lvCAREA, "":U) 
        + STRING(overdate) + CHR(10)
        + translateExtended ("Maxium Overbooking : ", lvCAREA, "":U) 
        + STRING(zimkateg.overbook) + CHR(10) 
        + translateExtended ("Actual Overbooking : ", lvCAREA, "":U) 
        + STRING(overanz). 
  ****/
 
  IF reslin-list.zinr NE "" THEN 
  DO: 
    RUN res-czinrbl.p(pvILanguage, reslin-list.ankunft, reslin-list.abreise, 
      (reslin-list.resstatus = 11 OR reslin-list.resstatus = 13), 
      reslin-list.resnr, reslin-list.reslinnr, INPUT-OUTPUT zikatstr, 
      reslin-list.zinr, OUTPUT error-code, OUTPUT msg-str1).  
    IF msg-str1 NE "" THEN msg-str = msg-str + CHR(2) + msg-str1.
    IF error-code NE 0 THEN 
    DO: 
      ASSIGN
        msg-str = msg-str + CHR(2)
          + translateExtended ("Room Assignment not possible.", lvCAREA, "":U) + CHR(10)
          + translateExtended (zinr-ecode[- error-code], lvCAREA, "":U) 
        error-number = 39
      .
      RETURN. 
    END. 
    ELSE 
    DO: 
      IF (res-mode = "modify" OR res-mode = "split") 
        THEN RUN release-zinr(res-line.zinr). 
      ELSE IF res-mode = "inhouse" /* AND sharer */ AND 
        (reslin-list.zinr NE res-line.zinr) THEN 
         RUN release-zinr(res-line.zinr). 
      IF (res-mode = "modify" OR res-mode = "split" 
        OR res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" 
        OR (res-mode = "inhouse" /* AND sharer */ AND 
        (reslin-list.zinr NE res-line.zinr))) 
      THEN 
      DO:    
        RUN assign-zinr(RECID(res-line), reslin-list.ankunft, 
          reslin-list.abreise, reslin-list.zinr, reslin-list.resstatus, 
          reslin-list.gastnrmember, reslin-list.bemerk, guestname, 
          OUTPUT wrong-room). 
        IF wrong-room THEN 
        DO: 
          IF res-line.zinr NE "" THEN 
            RUN assign-zinr(RECID(res-line), res-line.ankunft, 
          res-line.abreise, res-line.zinr, res-line.resstatus, 
          res-line.gastnrmember, res-line.bemerk, res-line.name, 
          OUTPUT b-dummy). 
          error-number = 40.
          RETURN. 
        END.
      END. 
    END. 
  END. 
  
  IF res-mode = "qci" THEN
  DO:
    FIND FIRST gmember WHERE gmember.gastnr = reslin-list.gastnrmember
        NO-LOCK NO-ERROR.
    IF AVAILABLE gmember AND gmember.karteityp GT 0 THEN
    msg-str = msg-str + CHR(2) + "&W"
        + translateExtended ("Do not forget to CHANGE the guest name.",lvCAREA,"").
    FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
    IF htparam.flogical THEN /* NA running */
    DO:
      FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
      IF reslin-list.ankunft LT htparam.fdate THEN
      DO:
        flag1 = YES.
        ci-date1 = htparam.fdate.
      END.
    END.
  END.

  IF reslin-list.erwachs NE 0 AND reslin-list.zipreis = 0 THEN 
  DO: 
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = reslin-list.resnr 
      AND reslin-queasy.reslinnr = reslin-list.reslinnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE reslin-queasy THEN 
    DO: 
      ASSIGN
        msg-str = msg-str + CHR(2) + "&Q"
          + translateExtended ("RoomRate = 0, change it?", lvCAREA, "":U) + CHR(10)
        error-number = ?
      .
    END. 
  END. 

  still-error = NO.

END. 

PROCEDURE check-bedsetup: 
  IF reslin-list.setup NE 0 THEN 
  DO: 
    FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
      AND zimmer.setup = reslin-list.setup NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE zimmer THEN 
    ASSIGN
      msg-str = msg-str + CHR(2)
      + translateExtended ("Bed Setup not found, click HELP-Button to choose",lvCAREA,"")
      error-number = 31
    . 
    ELSE error-number = 32.
    RETURN.
  END. 
  ELSE 
  ASSIGN
    msg-str = msg-str + CHR(2) 
      + translateExtended ("Bed Setup not found, click HELP-Button to choose",lvCAREA,"")
    error-number = 31
  . 
END. 

PROCEDURE assign-zinr:
  DEFINE INPUT  PARAMETER resline-recid AS INTEGER.
  DEFINE INPUT  PARAMETER ankunft AS DATE.
  DEFINE INPUT  PARAMETER abreise AS DATE.
  DEFINE INPUT  PARAMETER zinr LIKE zimmer.zinr.
  DEFINE INPUT  PARAMETER resstatus AS INTEGER.
  DEFINE INPUT  PARAMETER gastnrmember AS INTEGER.
  DEFINE INPUT  PARAMETER bemerk AS CHAR.
  DEFINE INPUT  PARAMETER name AS CHAR.
  DEFINE output PARAMETER room-blocked AS LOGICAL INITIAL NO.
  
  DEFINE VARIABLE sharer AS LOGICAL.
  DEFINE VARIABLE curr-datum AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE res-recid AS INTEGER.
  DEFINE BUFFER res-line1 FOR res-line.
  DEFINE BUFFER zimplan1 FOR zimplan.
  DEFINE BUFFER resline FOR res-line.
    
  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  sharer = (resstatus = 11) OR (resstatus = 13).
  if zinr NE "" AND NOT sharer THEN
  DO:
    if res-mode = "inhouse" THEN beg-datum = htparam.fdate.
    ELSE beg-datum = ankunft.
    room-blocked = no.
    do curr-datum = beg-datum TO (abreise - 1): 
      FIND FIRST zimplan1 WHERE zimplan1.datum = curr-datum
          AND zimplan1.zinr = zinr NO-LOCK NO-ERROR.
      if (NOT AVAILABLE zimplan1) AND (NOT room-blocked) THEN 
      DO:
        CREATE zimplan.
        zimplan.datum = curr-datum.
        zimplan.zinr = zinr.
        zimplan.res-recid = resline-recid.
        zimplan.gastnrmember = gastnrmember.
        zimplan.bemerk = bemerk.
        zimplan.resstatus = resstatus.
        zimplan.name = name.
        FIND CURRENT zimplan NO-LOCK.
        RELEASE zimplan.
      END.
      ELSE 
      DO: 
/* it is possible that it is the zimplan of it's own res-line exists, 
   THEN room-blocked is false */       
        if AVAILABLE zimplan1 AND (zimplan1.res-recid NE resline-recid) THEN
        DO:
          FIND FIRST resline WHERE RECID(resline) = zimplan1.res-recid 
            NO-LOCK NO-ERROR.
          if AVAILABLE resline AND resline.zinr = zinr 
            AND resline.active-flag LT 2 
            AND resline.ankunft LE zimplan1.datum
            AND resline.abreise GT zimplan1.datum THEN
          DO:
            curr-datum = abreise.
            room-blocked = yes.
          END.
          ELSE
          DO: /* try to fix the room plan by deleting wrong zimplan records */
            FIND CURRENT zimplan1 EXCLUSIVE-LOCK.
            zimplan1.res-recid = resline-recid.
            zimplan1.gastnrmember = gastnrmember.
            zimplan1.bemerk = bemerk.
            zimplan1.resstatus = resstatus.
            zimplan1.name = name.
            FIND CURRENT zimplan1 NO-LOCK.
            release zimplan1.
          END.
        END.
      END.
    END.
    if room-blocked THEN
    DO:
      do curr-datum = beg-datum TO (abreise - 1): 
        FIND FIRST zimplan WHERE zimplan.datum = curr-datum
          AND zimplan.zinr = zinr 
          AND zimplan.res-recid = resline-recid EXCLUSIVE-LOCK NO-ERROR.
        if AVAILABLE zimplan THEN 
        DO:
          DELETE zimplan.
          FIND CURRENT zimplan NO-LOCK.
          RELEASE zimplan.
        END.
      END.
      msg-str =  msg-str + CHR(2)
        + translateExtended ("Room Number", lvCAREA, "":U) + " " + zinr
        + " " 
        + translateExtended ("already blocked.", lvCAREA, "":U)
        + CHR(10)
        + translateExtended ("Room assignment not possible.", lvCAREA, "":U).
    END.
    ELSE DO:
      IF resstatus = 6 OR resstatus = 13 THEN
      DO:
        FIND FIRST zimmer WHERE zimmer.zinr = zinr EXCLUSIVE-LOCK.
        if abreise GT htparam.fdate AND zimmer.zistatus = 0 
          THEN zimmer.zistatus = 5. /* occupied clean */
        ELSE IF abreise GT htparam.fdate AND zimmer.zistatus = 3 /* ED */
          THEN zimmer.zistatus = 4. /* occupied dirty */
        ELSE if abreise = htparam.fdate THEN
        DO:
          FIND FIRST res-line1 WHERE RECID(res-line1) NE resline-recid 
            AND res-line1.abreise = abreise 
            AND res-line1.zinr = zimmer.zinr AND
            (res-line1.resstatus = 6 OR res-line1.resstatus = 13) 
            NO-LOCK NO-ERROR.
          if not AVAILABLE res-line1 THEN zimmer.zistatus = 3. /* ED */
        END.
/*      zimmer.bediener-nr-stat = 0.   */
        FIND CURRENT zimmer NO-LOCK.
        RELEASE zimmer.
      END.
    END.
  END.
END.

PROCEDURE release-zinr:
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.
DEFINE VARIABLE res-recid1 AS INTEGER.
DEFINE VARIABLE beg-datum AS DATE.
DEFINE VARIABLE answer AS LOGICAL.
DEFINE VARIABLE parent-nr AS INTEGER.

DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.
DEFINE BUFFER res-line3 FOR res-line.
DEFINE BUFFER rline FOR res-line.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  FIND FIRST rline WHERE rline.resnr = resnr 
      AND rline.reslinnr = reslinnr NO-LOCK.
  if rline.zinr NE "" THEN
  DO: 
    beg-datum = rline.ankunft. 
    res-recid1 = 0.

    if res-mode = "delete" OR res-mode = "cancel" 
      AND rline.resstatus = 1 THEN 
    DO TRANSACTION:
      FIND FIRST res-line1 WHERE res-line1.resnr = reslin-list.resnr
        AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 11
        NO-LOCK NO-ERROR.
      if AVAILABLE res-line1 THEN 
      DO:
        FIND CURRENT res-line1 EXCLUSIVE-LOCK.
        res-line1.resstatus = 1.
        FIND CURRENT res-line1 NO-LOCK.
        res-recid1 = RECID(res-line1).
      END.
    END.    
    if res-mode = "inhouse" THEN 
    DO:
      answer = yes.
      beg-datum = htparam.fdate.

      if rline.resstatus = 6 AND (rline.zinr NE new-zinr) THEN
      DO TRANSACTION:
        FIND FIRST res-line1 WHERE res-line1.resnr = reslin-list.resnr
          AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 13 
          NO-LOCK NO-ERROR.
        if AVAILABLE res-line1 THEN 
/*        
        DO:
          HIDE MESSAGE NO-PAUSE.
          MESSAGE "Room-change FOR the RoomSharer too?"         
            VIEW-AS ALERT-BOX question buttons yes-no update answer.
        END.
        if answer = no THEN 
        DO:
          FIND CURRENT res-line1 EXCLUSIVE-LOCK.
          res-line1.resstatus = 6.
          FIND CURRENT res-line1 NO-LOCK.
          res-recid1 = RECID(res-line1).
        END.
        ELSE 
*/
        DO:       
          FOR EACH res-line3 WHERE res-line3.resnr = resnr
            AND res-line3.zinr = rline.zinr AND res-line3.resstatus = 13 
            NO-LOCK:
            FIND FIRST res-line2 WHERE RECID(res-line2) = RECID(res-line3)
              EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE res-line2 THEN
            DO:
              FIND FIRST bill WHERE bill.resnr = res-line2.resnr
                AND bill.reslinnr = res-line2.reslinnr AND bill.flag = 0 
                AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK.
              bill.zinr = new-zinr.
              parent-nr = bill.parent-nr.
              FIND CURRENT bill NO-LOCK.
              FOR EACH bill WHERE bill.resnr = res-line2.resnr 
                AND bill.parent-nr = parent-nr AND bill.flag = 0
                AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:
                bill.zinr = new-zinr.
                release bill.
              END.
              res-line2.zinr = new-zinr.
              FIND CURRENT res-line2 NO-LOCK.
            END.
          END.
          FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr EXCLUSIVE-LOCK.
          zimmer.zistatus = 2.
          FIND CURRENT zimmer NO-LOCK.
        END.
      END.
    END.
    DO:
      FOR EACH zimplan WHERE zimplan.zinr = rline.zinr 
          AND zimplan.datum GE beg-datum
          AND zimplan.datum LT rline.abreise EXCLUSIVE-LOCK:
        if res-recid1 NE 0 THEN zimplan.res-recid = res-recid1.
        ELSE delete zimplan.
      END.
    END.
  END.
END. 

/* "qci" "new" "newXX" "insert" "modify" "split" "inhouse" "earlyci" 
   "newXX" means "new" with XX as INPUT RmQty */

PROCEDURE check-min-maxstay:
DEF VARIABLE error-flag1    AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE error-flag2    AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE error-flag3    AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE error-flag4    AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE i              AS INTEGER  NO-UNDO.
DEF VARIABLE prev-contcode  AS CHAR     NO-UNDO INIT "".
DEF VARIABLE prev-origcode  AS CHAR     NO-UNDO INIT "".
DEF VARIABLE str            AS CHAR     NO-UNDO.
  FIND FIRST arr WHERE arr.arrangement = reslin-list.arrangement NO-LOCK 
   NO-ERROR. 
  IF AVAILABLE arr THEN min-stay = arr.intervall.
  IF contcode NE "" THEN
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = contcode
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.number2 GT min-stay THEN
        min-stay = queasy.number2.
    IF AVAILABLE queasy THEN
    ASSIGN
        max-stay = queasy.deci2
        min-adv  = queasy.number3
        max-adv  = queasy.deci3
    .
  END.
  IF origcontcode NE "" THEN
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = origcontcode
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.number2 GT min-stay THEN
        min-stay = queasy.number2.
    IF AVAILABLE queasy THEN /* origcode overwrite new ratecode */
    ASSIGN
        max-stay = queasy.deci2
        min-adv  = queasy.number3
        max-adv  = queasy.deci3
    .
  END.
  
  IF min-stay GT (reslin-list.abreise - reslin-list.ankunft) THEN  
  DO:
    IF SUBSTR(res-mode,1,3) = "new" OR res-mode = "insert" 
      OR res-mode = "qci" THEN error-flag1 = 2.
    ELSE
    DO:
      error-flag1 = 1.
      DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN prev-contcode  = SUBSTR(str,7).
        IF SUBSTR(str,1,10) = "$OrigCode$" THEN prev-origCode  = SUBSTR(str,11).
      END.
      IF reslin-list.abreise NE res-line.abreise
        OR reslin-list.ankunft NE res-line.ankunft 
        THEN error-flag1 = 2.
      ELSE IF reslin-list.arrangement NE res-line.arrangement 
        THEN error-flag1 = 2.
      ELSE IF prev-contcode NE contcode THEN error-flag1 = 2.
      ELSE IF prev-origcode NE origContcode THEN error-flag1 = 2.
    END.
  END.

  IF max-stay NE 0 AND max-stay LT (reslin-list.abreise - reslin-list.ankunft) THEN  
  DO:
    IF SUBSTR(res-mode,1,3) = "new" OR res-mode = "insert" 
      OR res-mode = "qci" THEN error-flag2 = 2.
    ELSE
    DO:
      error-flag2 = 3.
      DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN prev-contcode  = SUBSTR(str,7).
        IF SUBSTR(str,1,10) = "$OrigCode$" THEN prev-origCode  = SUBSTR(str,11).
      END.
      IF reslin-list.abreise NE res-line.abreise
        OR reslin-list.ankunft NE res-line.ankunft 
        THEN error-flag2 = 4.
      ELSE IF reslin-list.arrangement NE res-line.arrangement 
        THEN error-flag2 = 2.
      ELSE IF prev-contcode NE contcode THEN error-flag2 = 2.
      ELSE IF prev-origcode NE origContcode THEN error-flag2 = 2.
    END.
  END.

  IF min-adv NE 0 AND (SUBSTR(res-mode,1,3) = "new" 
    OR res-mode = "insert" OR res-mode = "qci") THEN
  DO:
    IF (reslin-list.ankunft - ci-date) LT min-adv THEN error-flag3 = 2.
  END.

  IF max-adv NE 0 AND (SUBSTR(res-mode,1,3) = "new" 
    OR res-mode = "insert" OR res-mode = "qci") THEN
  DO:
    IF (reslin-list.ankunft - ci-date) GT max-adv THEN error-flag4 = 2.
  END.

  IF error-flag1 = 2 THEN
  DO:
      msg-str = msg-str + CHR(2) 
        + translateExtended ("Booking nights", lvCAREA, "":U)
        + STRING((reslin-list.abreise - reslin-list.ankunft),">>9 ") 
        + translateExtended ("LESS than minimum stay =", lvCAREA, "":U) 
        + " " + STRING(min-stay, ">>9"). 
      error-number = 3.
  END.
  ELSE IF error-flag1 = 1 THEN
  DO:
      msg-str =  msg-str + CHR(2) + "&W"
        + translateExtended ("Booking nights", lvCAREA, "":U)
        + STRING((reslin-list.abreise - reslin-list.ankunft),">>9 ") 
        + CHR(10)
        + translateExtended ("LESS than minimum stay =", lvCAREA, "":U) 
        + " " + STRING(min-stay, ">>9"). 
  END.

  IF error-flag2 = 2 THEN
  DO:
      msg-str = msg-str + CHR(2) 
        + translateExtended ("Booking nights", lvCAREA, "":U)
        + STRING((reslin-list.abreise - reslin-list.ankunft),">>9 ") 
        + translateExtended ("MORE than maximum stay =", lvCAREA, "":U) 
        + " " + STRING(max-stay, ">>9"). 
      error-number = 3.
  END.
  ELSE IF error-flag2 = 1 THEN
  DO:
      msg-str =  msg-str + CHR(2) + "&W"
        + translateExtended ("Booking nights", lvCAREA, "":U)
        + STRING((reslin-list.abreise - reslin-list.ankunft),">>9 ") 
        + CHR(10)
        + translateExtended ("MORE than maximum stay =", lvCAREA, "":U) 
        + " " + STRING(max-stay, ">>9"). 
  END.

  IF error-flag3 = 2 THEN
  DO:
      msg-str = msg-str + CHR(2) 
        + translateExtended ("Minimum Advance Booking (in days):", lvCAREA, "":U)
        + " " + STRING(min-adv).
      error-number = 3.
  END.

  IF error-flag4 = 2 THEN
  DO:
      msg-str = msg-str + CHR(2) 
        + translateExtended ("Maximum Advance Booking (in days):", lvCAREA, "":U)
        + " " + STRING(max-adv).
      error-number = 3.
  END.

END.
