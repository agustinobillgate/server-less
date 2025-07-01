
DEFINE TEMP-TABLE t-outorder LIKE outorder.

DEFINE INPUT  PARAMETER case-type    AS INTEGER.
DEFINE INPUT  PARAMETER TABLE FOR t-outorder.
DEFINE INPUT  PARAMETER from-date    AS DATE.
DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER service-flag AS LOGICAL.
DEFINE INPUT  PARAMETER zinr         AS CHAR.
DEFINE INPUT  PARAMETER user-nr      AS INTEGER.
DEFINE INPUT  PARAMETER reason       AS CHAR.
DEFINE INPUT  PARAMETER dept         AS INTEGER.
DEFINE INPUT  PARAMETER user-init    AS CHAR.
DEFINE OUTPUT PARAMETER msg-int      AS INTEGER INIT 0.
DEFINE OUTPUT PARAMETER resno        AS INTEGER INIT 0.
DEFINE OUTPUT PARAMETER resname      AS CHAR INIT "".
DEFINE OUTPUT PARAMETER ankunft      AS DATE INIT ?.
DEFINE OUTPUT PARAMETER abreise      AS DATE INIT ?.
DEFINE OUTPUT PARAMETER ooo-list-ind AS INT.

DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE roomnr   AS INT INIT 0.
DEFINE VARIABLE datum    AS DATE.
DEFINE BUFFER zbuff      FOR zimkateg.
DEFINE BUFFER qsy        FOR queasy.

DEFINE BUFFER obuff FOR outorder.
DEFINE VARIABLE do-it    AS LOGICAL INITIAL YES. 
DEFINE VARIABLE i        AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE zistatus AS INTEGER NO-UNDO.
DEFINE VARIABLE ci-date AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.
IF case-type = 1 THEN RUN chg-ooo.
ELSE IF case-type = 2 THEN RUN chg-om.


PROCEDURE chg-ooo:
    /*FDL Oct 20, 2023 => Ticket 9D89FF - Add res-line.abreise - 1*/
    FIND FIRST t-outorder.
    FIND FIRST res-line WHERE (res-line.resstatus = 1 OR res-line.resstatus = 2) AND /* malik serverless: resstatus -> res-line.resstatus */
        ((res-line.ankunft GE from-date AND res-line.ankunft LE to-date) OR 
         ((res-line.abreise - 1) GE from-date AND res-line.abreise LE to-date) OR 
         (from-date GE res-line.ankunft AND from-date LE (res-line.abreise - 1))) 
        AND res-line.zinr EQ zinr NO-LOCK NO-ERROR.

    IF AVAILABLE res-line THEN 
    DO: 
      ASSIGN 
          resno   = res-line.resnr
          resname = res-line.name /* malik serverless: res-line.NAME -> res-line.name */
          ankunft = res-line.ankunft
          abreise = res-line.abreise.
      msg-int = 1.
      RETURN NO-APPLY. 
    END. 

    IF from-date NE to-date AND service-flag THEN 
    DO: 
      msg-int = 2.
      RETURN NO-APPLY. 
    END. 

    FIND FIRST obuff NO-LOCK WHERE obuff.zinr = t-outorder.zinr AND
        NOT obuff.gespstart GT to-date   AND
        NOT obuff.gespende  LT from-date AND
        (obuff.zinr NE t-outorder.zinr 
         AND obuff.gespstart NE t-outorder.gespstart) NO-ERROR.
    IF AVAILABLE obuff THEN
    DO:
      msg-int = 3.
      RETURN NO-APPLY. 
    END.

    IF NOT service-flag 
        AND ((t-outorder.gespstart NE from-date) 
             OR (t-outorder.gespende NE to-date)) THEN
    DO:
            CREATE res-history. 
            ASSIGN 
              res-history.nr = user-nr 
              res-history.datum = TODAY 
              res-history.zeit = TIME 
              res-history.aenderung = "O-O-O Room " + zinr 
                 + " " + STRING(t-outorder.gespstart) 
                 + "-" + STRING(t-outorder.gespende)
                 + " Changed To " + STRING(from-date) + "-" + STRING(to-date)
              res-history.action = "HouseKeeping". 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
    END.

    FIND FIRST outorder WHERE outorder.zinr = t-outorder.zinr 
        AND outorder.betriebsnr = t-outorder.betriebsnr 
        AND outorder.gespstart = t-outorder.gespstart 
        AND outorder.gespende = t-outorder.gespende NO-ERROR.


    ASSIGN 
      outorder.gespstart = from-date
      outorder.gespende  = to-date
      outorder.gespgrund = reason + "$" + user-init.
      outorder.betriebsnr = dept.
    IF service-flag THEN outorder.betriebsnr = outorder.betriebsnr + 3. 


    FIND FIRST zimmer WHERE zimmer.zinr = zinr EXCLUSIVE-LOCK.

    FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN cat-flag = YES.

    FIND FIRST zbuff WHERE zbuff.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zbuff THEN
    DO:
      IF cat-flag THEN roomnr = zbuff.typ.
      ELSE roomnr = zbuff.zikatnr.
    END.

    DO datum = outorder.gespstart TO outorder.gespende:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
            AND queasy.number1 = roomnr AND queasy.char1 = ""
            AND queasy.logi1 = NO AND queasy.logi2 = NO NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
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

    DO datum = from-date TO to-date:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
            AND queasy.number1 = roomnr AND queasy.char1 = "" 
            AND queasy.logi1 = NO AND queasy.logi2 = NO NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
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

     /*ITA 260525 Log Availability*/
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    CREATE res-history. 
    ASSIGN 
      res-history.nr        = bediener.nr 
      res-history.datum     = TODAY
      res-history.zeit      = TIME 
      res-history.aenderung = "Change to OOO - Room : " + zimmer.zinr
      res-history.action    = "Log Availability"
    . 
     FIND CURRENT res-history NO-LOCK. 
     RELEASE res-history. 

   
    /*ITA 230616 --> find first sudah ada diatasnya.
    FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN DO:
        FIND CURRENT zimmer EXCLUSIVE-LOCK.
        ASSIGN zimmer.bediener-nr-stat = user-nr. 
        FIND CURRENT zimmer NO-LOCK.
        RELEASE zimmer.
    END.*/

    ASSIGN zimmer.bediener-nr-stat = user-nr. 
    
    IF ci-date GE from-date AND ci-date LE to-date THEN  
        ASSIGN 
            /*zimmer.zistatus = 6*/
            zistatus        = 6.
    ELSE 
        ASSIGN 
            /*zimmer.zistatus = 2*/
            zistatus        = 2. 

    /*ITA*/
    IF zistatus = 0 OR zistatus = 1 OR zistatus = 2 THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN DO: 
        IF res-line.abreise = ci-date THEN zimmer.zistatus = 3. 
        ELSE DO:
            IF zimmer.zistatus = 4 THEN zimmer.zistatus = 4.
            ELSE zimmer.zistatus = 5. 
        END.
        zimmer.bediener-nr-stat = 0.
      END. 
      ELSE  /*FD July 22, 20222 => Ticket 5F2EE7*/
      DO:
          IF AVAILABLE zimmer AND zimmer.sleeping THEN
          DO:
              zimmer.zistatus = 2.
          END.
      END.
    END. 
    ELSE IF zistatus = 3 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line AND res-line.abreise GT ci-date THEN DO: 
        zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
      END. 
      ELSE IF NOT AVAILABLE res-line THEN 
      DO: 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0. 
      END. 
    END. 
    ELSE IF zistatus = 4 OR zistatus = 5 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line AND res-line.abreise EQ ci-date THEN DO: 
        zimmer.zistatus = 3. 
        zimmer.bediener-nr-stat = 0.         
      END. 
      ELSE IF NOT AVAILABLE res-line THEN DO: 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0.         
      END. 
    END. 
    IF zistatus = 6 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zinr 
        AND res-line.active-flag = 1 
        AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN DO: 
        IF res-line.abreise = ci-date THEN zimmer.zistatus = 3. 
        ELSE zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        
        FIND FIRST obuff WHERE obuff.zinr = zinr 
          AND obuff.gespstart LT res-line.abreise EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE obuff THEN DELETE obuff. 
      END. 
      ELSE DO :
        FIND FIRST obuff WHERE obuff.zinr = zinr
            AND obuff.gespstart LE ci-date
            AND obuff.gespende GE ci-date
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE obuff THEN
        DO:
          ASSIGN
            zimmer.bediener-nr-stat = 0
            zimmer.zistatus = 2.
        END.
        ELSE    /*FD July 22, 20222 => Ticket 5F2EE7*/
        DO:
            IF AVAILABLE zimmer AND zimmer.sleeping THEN
            DO:
                zimmer.zistatus = 6.
            END.
        END.
      END.
    END. /*end*/
          
    FIND CURRENT outorder NO-LOCK. 
    FIND CURRENT zimmer NO-LOCK. 
            
    FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK. 
    ooo-list-ind       = outorder.betriebsnr + 1.
    IF (ooo-list-ind + 1) GE 6 THEN ooo-list-ind = 3.
END.


PROCEDURE chg-om:
    
    FIND FIRST t-outorder.
    IF t-outorder.betriebsnr GT 2 THEN /* with reseration */
    FIND FIRST res-line WHERE res-line.active-flag LE 1 AND
      res-line.resnr NE t-outorder.betriebsnr             AND
      res-line.resstatus NE 12                          AND 
      NOT res-line.abreise LE from-date                 AND
      NOT res-line.ankunft GT to-date                   AND
      res-line.zinr EQ zinr NO-LOCK NO-ERROR.
    ELSE /* without reseration */
    FIND FIRST res-line WHERE res-line.active-flag LE 1 AND
        res-line.resstatus NE 12                        AND 
        NOT res-line.abreise LE from-date               AND
        NOT res-line.ankunft GT to-date                 AND
        res-line.zinr EQ zinr NO-LOCK NO-ERROR.
    
    IF AVAILABLE res-line THEN 
    DO: 
      do-it = NO. 
      resno = res-line.resnr.
      resname = res-line.name.
      ankunft = res-line.ankunft.
      abreise = res-line.abreise.
      msg-int = 1.
      RETURN NO-APPLY. 
    END.
    IF do-it THEN
    DO:
      FIND FIRST obuff NO-LOCK WHERE obuff.zinr = outorder.zinr AND
        NOT obuff.gespstart GT to-date  AND
        NOT obuff.gespende  LT from-date AND
        RECID(obuff) NE RECID(outorder) NO-ERROR.
      IF AVAILABLE obuff THEN
      DO:
          msg-int = 2.
        do-it = NO.
      END.
    END.
    
    IF do-it THEN 
    DO:
      FIND FIRST outorder WHERE outorder.zinr = t-outorder.zinr EXCLUSIVE-LOCK.
      ASSIGN . 
      outorder.gespstart  = from-date. 
      outorder.gespende = to-date. 
      outorder.gespgrund = reason + "$" + user-init.
      FIND FIRST zimmer WHERE zimmer.zinr = t-outorder.zinr EXCLUSIVE-LOCK. 
      zimmer.bediener-nr-stat = user-nr. 
      FIND CURRENT outorder NO-LOCK. 
      FIND CURRENT zimmer NO-LOCK. 
    END. 
    ELSE 
    DO:
        msg-int = 3.
    END. 
END.
