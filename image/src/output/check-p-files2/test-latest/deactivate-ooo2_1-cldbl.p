/*
MESSAGE "DEBUG deactivate-ooo2-cldBL.p - Start"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
*/

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID" 
  FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE ooo-list2
    FIELD zinr       LIKE outorder.zinr  
    FIELD gespgrund  LIKE outorder.gespgrund  
    FIELD gespstart  LIKE outorder.gespstart  
    FIELD gespende   LIKE outorder.gespende  
    FIELD userinit   LIKE om-list.userinit  
    FIELD etage      LIKE zimmer.etage  
    FIELD ind        LIKE om-list.ind  
    FIELD bezeich    LIKE zimmer.bezeich  
    FIELD betriebsnr LIKE outorder.betriebsnr    
    FIELD selected-om AS LOGICAL INITIAL NO
    .


DEFINE INPUT PARAMETER user-nr      AS INTEGER.
DEFINE INPUT PARAMETER oos-flag     AS LOGICAL.
DEFINE INPUT PARAMETER ci-date      AS DATE.

DEFINE INPUT PARAMETER TABLE FOR ooo-list2.

FIND FIRST ooo-list2.

DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE roomnr   AS INT INIT 0.
DEFINE BUFFER zbuff FOR zimkateg.
DEFINE BUFFER qsy FOR queasy.

FIND FIRST outorder WHERE outorder.zinr = ooo-list2.zinr 
    AND outorder.betriebsnr = ooo-list2.betriebsnr AND outorder.gespstart = ooo-list2.gespstart
    AND outorder.gespende = ooo-list2.gespende NO-ERROR.
    
IF outorder.betriebsnr LE 1 THEN /*Out-of-Order*/
DO:
    CREATE res-history. 
    ASSIGN 
      res-history.nr = user-nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.aenderung = "Remove O-O-O Record of Room " + outorder.zinr 
         + " " + STRING(outorder.gespstart) + "-" + STRING(outorder.gespende)
      res-history.action = "HouseKeeping". 
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
    FIND FIRST zimmer WHERE zimmer.zinr = ooo-list2.zinr NO-LOCK NO-ERROR.

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
    END.
END.

/*Alder - Ticket C2CAD7 - Start*/
IF outorder.betriebsnr EQ 2 THEN /*Off-Market*/
DO:
    CREATE res-history. 
    ASSIGN 
      res-history.nr = user-nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.aenderung = "Remove Off Market Record of Room " + outorder.zinr 
         + " " + STRING(outorder.gespstart) + "-" + STRING(outorder.gespende)
      res-history.action = "HouseKeeping". 
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
    FIND FIRST zimmer WHERE zimmer.zinr = ooo-list2.zinr NO-LOCK NO-ERROR.

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
    END.
END.
/*Alder - Ticket C2CAD7 - End*/

IF oos-flag AND (outorder.gespstart = outorder.gespende) THEN 
DO: 
  FIND FIRST zinrstat WHERE zinrstat.zinr = "oos" 
    AND zinrstat.datum = ci-date NO-ERROR. 
  IF NOT AVAILABLE zinrstat THEN 
  DO: 
    CREATE zinrstat. 
    ASSIGN 
      zinrstat.datum = ci-date 
      zinrstat.zinr = "oos". 
  END. 
  zinrstat.zimmeranz = zinrstat.zimmeranz + 1. 
END. 

FIND CURRENT outorder EXCLUSIVE-LOCK. 
delete outorder. 
FIND FIRST zimmer WHERE zimmer.zinr = ooo-list2.zinr EXCLUSIVE-LOCK.
IF zimmer.zistatus = 6 THEN zimmer.zistatus = 2. 
zimmer.bediener-nr-stat = user-nr. 
FIND CURRENT zimmer NO-LOCK.

/*
MESSAGE "DEBUG deactivate-ooo2-cldBL.p - End"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
*/
