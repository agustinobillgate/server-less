DEF INPUT PARAMETER resno        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinno     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init    AS CHAR.
DEF INPUT PARAMETER all-flag     AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER deposit-flag AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER new-resno   AS INTEGER NO-UNDO.


DEF VARIABLE ci-date            AS DATE    NO-UNDO.
DEF VARIABLE ci                 AS DATE    NO-UNDO.
DEF VARIABLE co                 AS DATE    NO-UNDO.
/*DEF VARIABLE new-resno          AS INTEGER NO-UNDO.*/

DEFINE BUFFER t-reservation FOR reservation.
DEFINE BUFFER t-resline FOR res-line.
DEFINE BUFFER bresline  FOR res-line.
DEFINE BUFFER buf-rline FOR res-line.

DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INITIAL YES.
DEFINE VARIABLE curr-resnr       AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-reslinnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-ankunft     AS DATE    NO-UNDO.

RUN htpdate.p(87, OUTPUT ci-date).

IF deposit-flag THEN DO:
    FOR EACH reservation BY reservation.resnr DESC:
        ASSIGN new-resno = reservation.resnr + 1.
        LEAVE.
    END.
    
    FIND FIRST reservation WHERE reservation.resnr = resno NO-LOCK.
    IF AVAILABLE reservation THEN DO:
        CREATE t-reservation.
        BUFFER-COPY reservation EXCEPT reservation.resnr TO t-reservation.
        ASSIGN t-reservation.resnr       = new-resno
               t-reservation.depositbez  = 0
               t-reservation.depositgef  = 0.
    END.

    FIND FIRST res-line WHERE res-line.resnr = resno AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        CREATE t-resline.
        BUFFER-COPY res-line EXCEPT res-line.resnr TO t-resline.
        ASSIGN t-resline.resnr = new-resno.
    END.

    FIND FIRST bresline WHERE bresline.resnr = new-resno NO-LOCK NO-ERROR.
    IF AVAILABLE bresline THEN DO:
        IF priscilla-active THEN
        DO:
            RUN intevent-1.p(12, bresline.zinr, "Priscilla", bresline.resnr, bresline.reslinnr). 
        END.

        RUN update-resline-copy.
        RUN update-queasy-copy.
    END.    

    /*FD Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/
    IF NOT all-flag THEN
    DO:
        FIND FIRST buf-rline WHERE buf-rline.resnr EQ resno
            AND buf-rline.reslinnr EQ reslinno NO-LOCK NO-ERROR.
        IF AVAILABLE buf-rline THEN
        DO:
            CREATE reslin-queasy.
            ASSIGN
                reslin-queasy.key       = "ResChanges"
                reslin-queasy.resnr     = buf-rline.resnr 
                reslin-queasy.reslinnr  = buf-rline.reslinnr 
                reslin-queasy.date2     = TODAY 
                reslin-queasy.number2   = TIME
            .
        
            reslin-queasy.char3 = STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.arrangement) + ";" 
                                + STRING(buf-rline.arrangement) + ";"
                                + STRING(buf-rline.zipreis) + ";" 
                                + STRING(buf-rline.zipreis) + ";"
                                + STRING(user-init) + ";" 
                                + STRING(user-init) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(buf-rline.name) + ";" 
                                + STRING("RE-ACTIVATE RSV") + ";"
                                + STRING(" ") + ";" 
                                + STRING(" ") + ";"
                                .      
        
            FIND CURRENT reslin-queasy NO-LOCK.
            RELEASE reslin-queasy. 
        END.
    END.    
    ELSE
    DO:
        FOR EACH buf-rline WHERE buf-rline.resnr EQ resno NO-LOCK BY buf-rline.reslinnr:       
            
            CREATE reslin-queasy.
            ASSIGN
                reslin-queasy.key       = "ResChanges"
                reslin-queasy.resnr     = buf-rline.resnr 
                reslin-queasy.reslinnr  = buf-rline.reslinnr 
                reslin-queasy.date2     = TODAY 
                reslin-queasy.number2   = TIME
            .
        
            reslin-queasy.char3 = STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.arrangement) + ";" 
                                + STRING(buf-rline.arrangement) + ";"
                                + STRING(buf-rline.zipreis) + ";" 
                                + STRING(buf-rline.zipreis) + ";"
                                + STRING(user-init) + ";" 
                                + STRING(user-init) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(buf-rline.name) + ";" 
                                + STRING("RE-ACTIVATE RSV") + ";"
                                + STRING(" ") + ";" 
                                + STRING(" ") + ";"
                                .      
        
            FIND CURRENT reslin-queasy NO-LOCK.
            RELEASE reslin-queasy. 
        END.
    END.
END.
ELSE DO:
    FIND FIRST res-line WHERE res-line.resnr = resno AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.

    IF priscilla-active THEN
    DO:
        RUN intevent-1.p(12, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
    END.
    FIND FIRST reservation WHERE reservation.resnr = resno NO-LOCK.

    RUN update-resline.
    RUN update-queasy.

    /*FD Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/
    IF NOT all-flag THEN
    DO:        
        FIND FIRST buf-rline WHERE buf-rline.resnr EQ resno
            AND buf-rline.reslinnr EQ reslinno NO-LOCK NO-ERROR.
        IF AVAILABLE buf-rline THEN
        DO:
            CREATE reslin-queasy.
            ASSIGN
                reslin-queasy.key       = "ResChanges"
                reslin-queasy.resnr     = buf-rline.resnr 
                reslin-queasy.reslinnr  = buf-rline.reslinnr 
                reslin-queasy.date2     = TODAY 
                reslin-queasy.number2   = TIME
            .
        
            reslin-queasy.char3 = STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.arrangement) + ";" 
                                + STRING(buf-rline.arrangement) + ";"
                                + STRING(buf-rline.zipreis) + ";" 
                                + STRING(buf-rline.zipreis) + ";"
                                + STRING(user-init) + ";" 
                                + STRING(user-init) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(buf-rline.name) + ";" 
                                + STRING("RE-ACTIVATE RSV") + ";"
                                + STRING(" ") + ";" 
                                + STRING(" ") + ";"
                                .      
        
            FIND CURRENT reslin-queasy NO-LOCK.
            RELEASE reslin-queasy. 
        END.
    END.
    ELSE
    DO:
        FOR EACH buf-rline WHERE buf-rline.resnr EQ resno NO-LOCK BY buf-rline.reslinnr:
        
            CREATE reslin-queasy.
            ASSIGN
                reslin-queasy.key       = "ResChanges"
                reslin-queasy.resnr     = buf-rline.resnr 
                reslin-queasy.reslinnr  = buf-rline.reslinnr 
                reslin-queasy.date2     = TODAY 
                reslin-queasy.number2   = TIME
            .
        
            reslin-queasy.char3 = STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.ankunft) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.abreise) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.zimmeranz) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.erwachs) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.kind1) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.gratis) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zikatnr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.zinr) + ";" 
                                + STRING(buf-rline.arrangement) + ";" 
                                + STRING(buf-rline.arrangement) + ";"
                                + STRING(buf-rline.zipreis) + ";" 
                                + STRING(buf-rline.zipreis) + ";"
                                + STRING(user-init) + ";" 
                                + STRING(user-init) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(TODAY) + ";" 
                                + STRING(buf-rline.name) + ";" 
                                + STRING("RE-ACTIVATE RSV") + ";"
                                + STRING(" ") + ";" 
                                + STRING(" ") + ";"
                                .      
        
            FIND CURRENT reslin-queasy NO-LOCK.
            RELEASE reslin-queasy. 
        END.
    END.    
END.


PROCEDURE update-resline:
DEF VAR new-status   AS INTEGER  NO-UNDO.
DEF BUFFER rbuff     FOR res-line.  
DEF BUFFER rline     FOR res-line.
DEF BUFFER resline   FOR res-line.
DEF BUFFER zinrbuff  FOR zinrstat.
DEF BUFFER mbuff     FOR master.

DEF VAR curr-ress AS INT NO-UNDO. /*ragung*/


  DO TRANSACTION: 
    IF res-line.resstatus = 9 AND (res-line.betrieb-gastpay LE 2 
       OR res-line.betrieb-gastpay = 5) THEN
    DO: 
      FIND FIRST zinrstat WHERE zinrstat.zinr = "CancRes" 
        AND zinrstat.datum = res-line.CANCELLED NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN 
      DO:
        FIND FIRST zinrbuff WHERE RECID(zinrbuff) = RECID(zinrstat)
            EXCLUSIVE-LOCK.
        ASSIGN
          zinrbuff.zimmeranz = zinrbuff.zimmeranz - res-line.zimmeranz 
          zinrbuff.personen = zinrbuff.personen 
            - res-line.zimmeranz * res-line.erwachs
        .
         FIND CURRENT zinrbuff NO-LOCK.
         RELEASE zinrbuff.
      END.  
      IF all-flag THEN
      FOR EACH rbuff WHERE rbuff.resnr = res-line.resnr
        AND rbuff.reslinnr NE res-line.reslinnr
        AND rbuff.resstatus = 9 AND (res-line.betrieb-gastpay LE 2 
        OR res-line.betrieb-gastpay = 5) NO-LOCK:
        FIND FIRST zinrstat WHERE zinrstat.zinr = "CancRes" 
          AND zinrstat.datum = rbuff.CANCELLED NO-LOCK NO-ERROR.
        IF AVAILABLE zinrstat THEN 
        DO:
          FIND FIRST zinrbuff WHERE RECID(zinrbuff) = RECID(zinrstat)
            EXCLUSIVE-LOCK.
          ASSIGN
            zinrbuff.zimmeranz = zinrbuff.zimmeranz - rbuff.zimmeranz 
            zinrbuff.personen = zinrbuff.personen 
              - rbuff.zimmeranz * rbuff.erwachs
          .
          FIND CURRENT zinrbuff NO-LOCK.
          RELEASE zinrbuff.
        END.        
      END.
    END.
        
    FIND CURRENT res-line EXCLUSIVE-LOCK. 
    IF (res-line.erwachs + res-line.kind1 + res-line.kind2) GT 0 THEN 
    DO: 
      IF res-line.betrieb-gastpay GT 0 THEN
         new-status = res-line.betrieb-gastpay. 
      ELSE new-status = 1.
    END.
    ELSE new-status = 11.
    curr-ress = res-line.resstatus.

    ASSIGN curr-ankunft = res-line.ankunft.

    IF res-line.ankunft LT ci-date THEN res-line.ankunft = ci-date. 

    IF res-line.abreise LE res-line.ankunft THEN res-line.abreise = res-line.ankunft + 1. /*ragung delete +1*/

    ASSIGN
        res-line.zinr             = "" 
        res-line.active-flag      = 0 
        res-line.resstatus        = new-status
        res-line.changed          = ci-date 
        res-line.changed-id       = user-init 
        res-line.cancelled-id     = ""
        res-line.betrieb-gastpay  = curr-ress /*9 change resstatus*/
        res-line.zimmer-wunsch    = res-line.zimmer-wunsch + "$cancel;" + "$arrival$" + STRING(curr-ankunft, "99/99/9999") + ";". 
    FIND CURRENT res-line NO-LOCK.

    FOR EACH resline WHERE resline.resnr = res-line.resnr
      AND resline.l-zuordnung[3] = 1 
      AND resline.kontakt-nr = res-line.reslinnr EXCLUSIVE-LOCK:
      curr-ress = resline.resstatus.  
      ASSIGN
        resline.active-flag     = 0
        resline.resstatus       = 11
        resline.ankunft         = res-line.ankunft
        resline.abreise         = res-line.abreise
        resline.zinr            = "" 
        resline.changed         = ci-date
        resline.changed-id      = user-init 
        resline.cancelled-id    = ""
        resline.betrieb-gastpay = curr-ress /*9 change resstatus*/        
      . 
      RELEASE resline.
    END.
    RUN add-resplan(RECID(res-line)). 

    IF all-flag THEN 
    FOR EACH rbuff WHERE rbuff.resnr = res-line.resnr
      AND rbuff.reslinnr NE res-line.reslinnr
      AND (rbuff.resstatus = 9 OR rbuff.resstatus = 10)
      AND rbuff.l-zuordnung[3] = 0 NO-LOCK:

      IF priscilla-active THEN
      DO:
          RUN intevent-1.p(12, rbuff.zinr, "Priscilla", rbuff.resnr, rbuff.reslinnr). 
      END.

      FIND FIRST rline WHERE RECID(rline) = RECID(rbuff) EXCLUSIVE-LOCK.
      
      IF (rline.erwachs + rline.kind1 + rline.kind2) GT 0 THEN 
      DO: 
        IF rline.betrieb-gastpay GT 0 THEN new-status = rline.betrieb-gastpay. 
        ELSE new-status = 1.
      END.
      ELSE new-status = 11. 
       ASSIGN curr-ankunft = rline.ankunft.
      curr-ress = rline.resstatus.

      IF rline.ankunft LT ci-date THEN rline.ankunft = ci-date. 
      IF rline.abreise LE rline.ankunft THEN rline.abreise = rline.ankunft + 1. 
      ASSIGN
        rline.zinr             = "" 
        rline.active-flag      = 0 
        rline.resstatus        = new-status
        rline.changed          = ci-date 
        rline.changed-id       = user-init 
        rline.cancelled-id     = ""
        rline.betrieb-gastpay  = curr-ress /*9 change to resstatus*/    
        ci                     = rline.ankunf
        co                     = rline.abreise
        rline.zimmer-wunsch    = rline.zimmer-wunsch + "$cancel;" + "$arrival$" + STRING(curr-ankunft, "99/99/9999") + ";"
      . 
      FIND CURRENT rline NO-LOCK. 
      RELEASE rline.
    
      FOR EACH resline WHERE resline.resnr = rbuff.resnr
        AND resline.l-zuordnung[3] = 1 
        AND resline.kontakt-nr = rbuff.reslinnr EXCLUSIVE-LOCK:
        
        curr-ress = resline.resstatus.

        IF priscilla-active THEN
        DO:
            RUN intevent-1.p(12, resline.zinr, "Priscilla", resline.resnr, resline.reslinnr). 
        END.

        ASSIGN
          resline.active-flag     = 0
          resline.resstatus       = 11
          resline.ankunft         = ci
          resline.abreise         = co
          resline.zinr            = "" 
          resline.changed         = ci-date
          resline.changed-id      = user-init 
          resline.cancelled-id    = ""
          resline.betrieb-gastpay = curr-ress  /*9 change to resstatus*/     
        . 
        RELEASE resline.
      END.
      RUN add-resplan(RECID(rbuff)).       
    END.
    IF reservation.activeflag = 1 THEN 
    DO: 
      FIND CURRENT reservation EXCLUSIVE-LOCK. 
      reservation.activeflag = 0. 
      FIND CURRENT reservation NO-LOCK. 
    END. 
 
    FIND FIRST master WHERE master.gastnr = res-line.gastnr 
      AND master.resnr = res-line.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE master THEN 
    DO: 
       FIND FIRST mbuff WHERE RECID(mbuff) = RECID(master) EXCLUSIVE-LOCK.
       mbuff.active = YES. 
       FIND CURRENT mbuff NO-LOCK. 
       RELEASE mbuff.
    END. 
            
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR. 
          
    CREATE history. 
    ASSIGN 
      history.gastnr    = res-line.gastnrmember 
      history.ankunft   = curr-ankunft 
      history.abreise   = TODAY 
      history.zimmeranz = res-line.zimmeranz 
      history.zikateg   = zimkateg.kurzbez 
      history.zinr      = res-line.zinr 
      history.erwachs   = res-line.erwachs 
      history.gratis    = res-line.gratis 
      history.zipreis   = res-line.zipreis 
      history.arrangement = res-line.arrangement 
      history.gastinfo  = res-line.name + " - " 
        + guest.adresse1 + ", " + guest.wohnort 
      history.abreisezeit = STRING(TIME, "HH:MM") 
      history.segmentcode = reservation.segmentcode 
      history.zi-wechsel = NO 
      history.resnr = res-line.resnr 
      history.reslinnr = res-line.reslinnr 
      history.bemerk = "Cancel Reservation and Reactive by" 
        + " " + user-init
    . 
    FIND CURRENT history NO-LOCK.
    RELEASE history.

    CREATE res-history. 
    ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.resnr = res-line.resnr 
      res-history.reslinnr = res-line.reslinnr 
      res-history.action = "RE-RES". 
      res-history.aenderung = "Cancel Reservation and Reactive by" 
        + " " + user-init
    . 
    RELEASE res-line.
    RELEASE reservation.
  END. 
END.

PROCEDURE add-resplan: 
DEFINE INPUT PARAMETER rint AS INTEGER.
DEFINE VARIABLE curr-date   AS DATE     NO-UNDO. 
DEFINE VARIABLE i           AS INTEGER  NO-UNDO. 
DEFINE VARIABLE tmpdate     AS DATE     NO-UNDO.
DEFINE BUFFER rline         FOR res-line.  
DEFINE BUFFER buffplan      FOR resplan.


  FIND FIRST rline WHERE RECID(rline) = rint NO-LOCK.
  ASSIGN
    i = rline.resstatus
    tmpdate = rline.abreise - 1.
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK. 
  /*DO curr-date = rline.ankunft TO (rline.abreise - 1): FT serverless*/
  DO curr-date = rline.ankunft TO tmpdate: 
     FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr 
        AND resplan.datum = curr-date NO-LOCK NO-ERROR. 
     IF NOT AVAILABLE resplan THEN 
     DO: 
        CREATE resplan. 
        resplan.datum = curr-date. 
        resplan.zikatnr = zimkateg.zikatnr. 
        resplan.anzzim[i] = rline.zimmeranz. 
     END. 
     ELSE IF AVAILABLE resplan THEN
     DO:
         FIND FIRST buffplan WHERE RECID(buffplan) = RECID(resplan)
             EXCLUSIVE-LOCK.
         buffplan.anzzim[i] = buffplan.anzzim[i] + rline.zimmeranz. 
         FIND CURRENT buffplan NO-LOCK.
         RELEASE buffplan.
     END.                 
  END. 
END. 

PROCEDURE update-queasy:
  DEFINE VARIABLE datum AS DATE.
  DEFINE VARIABLE upto-date AS DATE.
  DEFINE VARIABLE i           AS INT INIT 0.
  DEFINE VARIABLE iftask      AS CHAR INIT "".
  DEFINE VARIABLE origcode    AS CHAR INIT "".
  DEFINE VARIABLE do-it       AS LOGICAL INIT NO.
  DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
  DEFINE VARIABLE roomnr      AS INT INIT 0.

  DEFINE BUFFER qsy   FOR queasy.
  DEFINE BUFFER zbuff FOR zimkateg.

  FIND FIRST res-line WHERE res-line.resnr = resno
    AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.

  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
    DO:
      origcode  = SUBSTR(iftask,11).
      LEAVE.
    END.
  END.

  FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN cat-flag = YES.

  FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
  IF AVAILABLE zbuff THEN
  DO:
    IF cat-flag THEN roomnr = zbuff.typ.
    ELSE roomnr = zbuff.zikatnr.
  END.

  IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise .
  ELSE 
    ASSIGN 
      upto-date = res-line.abreise  - 1. 
  DO datum = res-line.ankunft TO upto-date:
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
        AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
    DO:
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
            qsy.logi2 = YES.
            FIND CURRENT qsy NO-LOCK.
            RELEASE qsy.
        END.
    END. 
    
    IF origcode NE "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
            AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
        DO:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
                qsy.logi2 = YES.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.
            END.
        END.
    END.
  END.
END.


PROCEDURE update-resline-copy:
DEF VAR new-status   AS INTEGER  NO-UNDO.
DEF BUFFER rbuff     FOR res-line.  
DEF BUFFER rline     FOR res-line.
DEF BUFFER resline   FOR res-line.
DEF BUFFER zinrbuff  FOR zinrstat.
DEF BUFFER mbuff     FOR master.

DEF VAR curr-ress AS INT NO-UNDO. /*ragung*/
                       
    FIND CURRENT bresline EXCLUSIVE-LOCK. 
    IF (bresline.erwachs + bresline.kind1 + bresline.kind2) GT 0 THEN 
    DO: 
      IF bresline.betrieb-gastpay GT 0 THEN
         new-status = bresline.betrieb-gastpay. 
      ELSE new-status = 1.
    END.
    ELSE new-status = 11. 
    curr-ress = bresline.resstatus.
    ASSIGN curr-ankunft = bresline.ankunft.

    IF bresline.ankunft LT ci-date THEN bresline.ankunft = ci-date. 
    IF bresline.abreise LE res-line.ankunft THEN bresline.abreise = res-line.ankunft + 1. /*ragung delete +1*/
    ASSIGN
        bresline.zinr             = "" 
        bresline.active-flag      = 0 
        bresline.resstatus        = new-status
        bresline.changed          = ci-date 
        bresline.changed-id       = user-init 
        bresline.cancelled-id     = ""
        bresline.betrieb-gastpay  = curr-ress /*9 change to resstatus*/
        bresline.anztag           = bresline.abreise - bresline.ankunft
        bresline.zimmer-wunsch    = bresline.zimmer-wunsch + "$cancel;" + "$arrival$" + STRING(curr-ankunft, "99/99/9999") + ";". 
    FIND CURRENT bresline NO-LOCK.

    FOR EACH resline WHERE resline.resnr = resno
      AND resline.l-zuordnung[3] = 1 
      AND resline.kontakt-nr = reslinnr NO-LOCK:
      curr-ress = resline.resstatus. 
      CREATE t-resline.
      BUFFER-COPY resline EXCEPT resline.resnr TO t-resline.
      IF resline.ankunft LT ci-date THEN t-resline.ankunft = ci-date. 
      IF resline.abreise LE resline.ankunft THEN t-resline.abreise = resline.ankunft + 1. 
      ASSIGN
        t-resline.resnr           = new-resno
        t-resline.active-flag     = 0
        t-resline.resstatus       = 11
        t-resline.zinr            = "" 
        t-resline.changed         = ci-date
        t-resline.changed-id      = user-init 
        t-resline.cancelled-id    = ""
        t-resline.betrieb-gastpay = curr-ress /*9 change to resstatus*/
        t-resline.anztag          = t-resline.abreise - t-resline.ankunft. 
    END.
    RUN add-resplan(RECID(bresline)).

    IF all-flag THEN
    FOR EACH rbuff WHERE rbuff.resnr = resno
      AND rbuff.reslinnr NE reslinno
      AND (rbuff.resstatus = 9 OR rbuff.resstatus = 10) AND rbuff.l-zuordnung[3] = 0 NO-LOCK:
      
      CREATE t-resline.
      BUFFER-COPY rbuff EXCEPT rbuff.resnr TO t-resline.
      ASSIGN t-resline.resnr  = new-resno.
      
      IF priscilla-active THEN
      DO:
          RUN intevent-1.p(12, rbuff.zinr, "Priscilla", new-resno, rbuff.reslinnr). 
      END.
      
      IF (t-resline.erwachs + t-resline.kind1 + t-resline.kind2) GT 0 THEN 
      DO: 
        IF t-resline.betrieb-gastpay GT 0 THEN new-status = t-resline.betrieb-gastpay. 
        ELSE new-status = 1.
      END.
      ELSE new-status = 11. 

      curr-ress = t-resline.resstatus.  

      ASSIGN curr-ankunft = t-resline.ankunft.
      IF t-resline.ankunft LT ci-date THEN t-resline.ankunft = ci-date. 
      IF t-resline.abreise LE t-resline.ankunft THEN t-resline.abreise = rbuff.ankunft + 1. 
      ASSIGN
        t-resline.zinr             = "" 
        t-resline.active-flag      = 0 
        t-resline.resstatus        = new-status
        t-resline.changed          = ci-date 
        t-resline.changed-id       = user-init 
        t-resline.cancelled-id     = ""
        t-resline.betrieb-gastpay  = curr-ress /*9 change to resstatus*/ 
        ci                         = t-resline.ankunf
        co                         = t-resline.abreise
        t-resline.anztag           = t-resline.abreise - t-resline.ankunft
        t-resline.zimmer-wunsch    = t-resline.zimmer-wunsch + "$cancel;" + "$arrival$" + STRING(curr-ankunft, "99/99/9999") + ";". 

      FOR EACH resline WHERE resline.resnr = rbuff.resnr
        AND resline.l-zuordnung[3] = 1 
        AND resline.kontakt-nr = rbuff.reslinnr EXCLUSIVE-LOCK:
                 
        CREATE t-resline.
        BUFFER-COPY resline EXCEPT resline.resnr TO t-resline.
        ASSIGN t-resline.resnr  = new-resno.
        curr-ress = resline.resstatus.
        IF priscilla-active THEN
        DO:
            RUN intevent-1.p(12, resline.zinr, "Priscilla", new-resno, resline.reslinnr). 
        END.

        ASSIGN
          t-resline.active-flag     = 0
          t-resline.resstatus       = 11
          t-resline.ankunft         = ci
          t-resline.abreise         = co
          t-resline.zinr            = "" 
          t-resline.changed         = ci-date
          t-resline.changed-id      = user-init 
          t-resline.cancelled-id    = ""
          t-resline.betrieb-gastpay = curr-ress /*9 change to resstatus*/
          t-resline.anztag          = t-resline.abreise - t-resline.ankunft. 
      END.
      RUN add-resplan(RECID(t-resline)).       
    END.
    
    
    FIND FIRST master WHERE master.gastnr = bresline.gastnr 
      AND master.resnr = resno NO-LOCK NO-ERROR. 
    IF AVAILABLE master THEN 
    DO: 
       FIND FIRST mbuff WHERE RECID(mbuff) = RECID(master) EXCLUSIVE-LOCK.
       ASSIGN 
           mbuff.resnr  = new-resno
           mbuff.active = YES. 
       FIND CURRENT mbuff NO-LOCK. 
       RELEASE mbuff.
    END. 
            
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    FIND FIRST guest WHERE guest.gastnr = bresline.gastnrmember NO-LOCK NO-ERROR. 
    
    CREATE history. 
    ASSIGN 
      history.gastnr    = bresline.gastnrmember 
      history.ankunft   = curr-ankunft 
      history.abreise   = TODAY 
      history.zimmeranz = bresline.zimmeranz 
      history.zikateg   = zimkateg.kurzbez 
      history.zinr      = bresline.zinr 
      history.erwachs   = bresline.erwachs 
      history.gratis    = bresline.gratis 
      history.zipreis   = bresline.zipreis 
      history.arrangement = bresline.arrangement 
      history.gastinfo  = bresline.name + " - " 
        + guest.adresse1 + ", " + guest.wohnort 
      history.abreisezeit = STRING(TIME, "HH:MM") 
      history.segmentcode = reservation.segmentcode 
      history.zi-wechsel = NO 
      history.resnr = bresline.resnr 
      history.reslinnr = bresline.reslinnr
      /*history.betriebsnr = res-line.resstatus ragung*/. 
      history.bemerk = "Cancel Reservation and Reactive by" 
        + " " + user-init
    . 
    FIND CURRENT history NO-LOCK.
    RELEASE history.

    CREATE res-history. 
    ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.resnr = bresline.resnr 
      res-history.reslinnr = bresline.reslinnr 
      res-history.action = "RE-RES". 
      res-history.aenderung = "Cancel Reservation and Reactive by" 
        + " " + user-init
    . 
  /*END.*/ 
END.

PROCEDURE update-queasy-copy:
  DEFINE VARIABLE datum AS DATE.
  DEFINE VARIABLE upto-date AS DATE.
  DEFINE VARIABLE i           AS INT INIT 0.
  DEFINE VARIABLE iftask      AS CHAR INIT "".
  DEFINE VARIABLE origcode    AS CHAR INIT "".
  DEFINE VARIABLE do-it       AS LOGICAL INIT NO.
  DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
  DEFINE VARIABLE roomnr      AS INT INIT 0.

  DEFINE BUFFER qsy   FOR queasy.
  DEFINE BUFFER zbuff FOR zimkateg.

  FIND FIRST res-line WHERE res-line.resnr = new-resno
    AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.

  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
    DO:
      origcode  = SUBSTR(iftask,11).
      LEAVE.
    END.
  END.

  FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN cat-flag = YES.

  FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
  IF AVAILABLE zbuff THEN
  DO:
    IF cat-flag THEN roomnr = zbuff.typ.
    ELSE roomnr = zbuff.zikatnr.
  END.

  IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise .
  ELSE upto-date = res-line.abreise  - 1. 
  DO datum = res-line.ankunft TO upto-date:
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
        AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
    DO:
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
            qsy.logi2 = YES.
            FIND CURRENT qsy NO-LOCK.
            RELEASE qsy.
        END.
    END. 
    
    IF origcode NE "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
            AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
        DO:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
                qsy.logi2 = YES.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.
            END.
        END.
    END.
  END.
END.
 

