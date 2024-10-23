 
 
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER ankunft      AS DATE. 
DEFINE INPUT PARAMETER abreise      AS DATE. 
DEFINE INPUT PARAMETER sharer       AS LOGICAL. 
DEFINE INPUT PARAMETER resnr        AS INTEGER. 
DEFINE INPUT PARAMETER reslinnr     AS INTEGER. 
DEFINE INPUT-OUTPUT PARAMETER rmcat AS CHAR FORMAT "x(6)". 
DEFINE INPUT PARAMETER zinr         LIKE zimmer.zinr.
DEFINE OUTPUT PARAMETER error-code  AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER msg-str     AS CHAR INIT "" NO-UNDO.
/* 
DEFINE VARIABLE ankunft AS DATE INITIAL 11/28/07. 
DEFINE VARIABLE abreise AS DATE INITIAL 11/29/07. 
DEFINE VARIABLE sharer AS LOGICAL INITIAL NO. 
DEFINE VARIABLE resnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE rmcat AS CHAR FORMAT "x(6)" INITIAL "XGV". 
DEFINE VARIABLE zinr AS CHAR FORMAT "x(4)" INITIAL "111". 
DEFINE VARIABLE error-code AS INTEGER INITIAL 0. 
RUN add-persist-procedure. 
setTransLanguage(INPUT 1). /* FOR supertrans */ 
PROCEDURE add-persist-procedure: 
    DEFINE VARIABLE lvHS AS HANDLE              NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE lFound AS LOGICAL INIT FALSE    NO-UNDO. 
 
    DO lvI = 1 TO NUM-ENTRIES(SESSION:SUPER-PROCEDURES): 
        lvHS = WIDGET-HANDLE(ENTRY(lvI, SESSION:SUPER-PROCEDURES)). 
        IF VALID-HANDLE(lvHS) THEN DO: 
            IF lvHS:NAME BEGINS "supertrans" THEN 
                lFound = TRUE. 
        END. 
    END. 
 
    IF NOT lFound THEN DO: 
        RUN supertrans.p PERSISTENT SET lvHS. 
        SESSION:ADD-SUPER-PROCEDURE(lvHS). 
    END. 
END. 
*/ 
/* error-code = -1  room NO NOT found FOR the specific room catagory 
                -2  room out-of-order 
                -3  room already blocked 
                -4  room NOT cleaned 
                -5  NEW: 09/30/00 Off-Market 
                -6  NEW: 01/27/02 Room sharer already inhouse */ 
 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-czinr". 

DEFINE VARIABLE found           AS LOGICAL INITIAL NO. 
DEFINE VARIABLE answer          AS LOGICAL INITIAL NO. 
DEFINE VARIABLE resline-recid   AS INTEGER. 
DEFINE VARIABLE ci-date         AS DATE. 
DEFINE VARIABLE from-date       AS DATE. 
DEFINE VARIABLE to-date         AS DATE. 
DEFINE BUFFER resline           FOR res-line. 
  
IF resnr > 0 THEN 
FIND FIRST res-line WHERE res-line.resnr = resnr 
   AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. 
 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ASSIGN ci-date = htparam.fdate. 

IF AVAILABLE res-line AND res-line.active-flag = 1 THEN from-date = ci-date. 
ELSE from-date = ankunft. 
to-date = abreise. 
 
FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmcat NO-LOCK NO-ERROR.
IF NOT AVAILABLE zimkateg THEN
DO:
    error-code = -7. 
    RETURN. 
END.
 
IF sharer AND AVAILABLE res-line THEN 
DO: 
  FIND FIRST resline WHERE resline.resnr = resnr AND resline.zinr EQ zinr 
    AND resline.reslinnr NE reslinnr NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE resline AND NOT found: 
    IF resline.ankunft LE ankunft AND resline.abreise GE abreise THEN 
    DO: 
       found = YES. 
       FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK NO-ERROR.
       FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
       rmcat = zimkateg.kurzbez.
       RETURN. 
    END. 
    FIND NEXT resline WHERE resline.resnr = resnr AND resline.zinr EQ zinr 
      AND resline.reslinnr NE reslinnr NO-LOCK NO-ERROR. 
  END. 
  IF NOT found AND res-line.active-flag = 0 THEN  /* Sharer Reservation */ 
  DO: 
    error-code = -1. 
    RETURN. 
  END. 
  ELSE IF NOT found AND res-line.active-flag = 1 THEN /* sharer Inhouse */ 
  DO: 
    FIND FIRST resline WHERE resline.resstatus = 6 AND resline.active-flag = 1 
      AND resline.zinr = zinr AND resline.abreise GE abreise AND resline.zikatnr 
      = zimkateg.zikatnr NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN found = YES. 
    ELSE error-code = -1. 
    RETURN. 
  END. 
END. 

ELSE IF AVAILABLE res-line AND res-line.zinr NE zinr 
  AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN
DO: /* check if room sharer exists and already in-house */
  FIND FIRST resline WHERE resline.resnr = resnr AND resline.resstatus = 13 
    AND resline.zinr = res-line.zinr NO-LOCK NO-ERROR. 
  IF AVAILABLE resline THEN 
  DO: 
    error-code = -6. 
    RETURN. 
  END. 
END. 
 
IF zinr = "" THEN RETURN. 
 
FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE zimmer THEN 
DO: 
  error-code = -1. 
  RETURN. 
END. 
 
IF AVAILABLE res-line AND res-line.active-flag = 1 
    AND NOT sharer AND abreise = ci-date THEN
DO:
    FIND FIRST resline WHERE resline.zinr = zinr 
        AND resline.resstatus = 6 
        AND RECID(resline) NE RECID(res-line) NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN
    DO:
        error-code = -3. 
        RETURN. 
    END.
END.

FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
IF zimkateg.kurzbez NE rmcat THEN 
DO: 
DEFINE VARIABLE accept-it AS LOGICAL INITIAL NO NO-UNDO. 
  
  msg-str = "&W" + translateExtended ("Room Type changed to",lvCAREA,"")
    + " " + zimkateg.kurzbez + "." + CHR(10).
/*  + " " + translateExtended ("Accept it?",lvCAREA,"")

  HIDE MESSAGE NO-PAUSE. 
  MESSAGE translateExtended ("Room Type changed to",lvCAREA,"") 
      + " " + zimkateg.kurzbez + ". " 
      + translateExtended ("Accept it?",lvCAREA,"") 
    VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE accept-it. 

  IF NOT accept-it THEN 
  DO: 
    error-code = -1. 
    RETURN. 
  END.
*/ 
END. 
 
IF resnr > 0 THEN 
FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
  AND outorder.betriebsnr NE resnr 
  AND NOT to-date   LE outorder.gespstart
  AND NOT from-date GT outorder.gespende NO-LOCK NO-ERROR.
/*
  AND ((from-date GE gespstart AND from-date LE gespende) 
  OR (to-date GT gespstart AND to-date LE gespende) 
  OR (gespstart GE from-date AND gespstart LT to-date) 
  OR (gespende GE from-date AND gespende LE to-date)) NO-LOCK NO-ERROR. 
*/
ELSE 
FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
  AND NOT to-date   LE outorder.gespstart
  AND NOT from-date GT outorder.gespende NO-LOCK NO-ERROR.
/*
  AND ((from-date GE gespstart AND from-date LE gespende) 
  OR (to-date GT gespstart AND to-date LE gespende) 
  OR (gespstart GE from-date AND gespstart LT to-date) 
  OR (gespende GE from-date AND gespende LE to-date)) NO-LOCK NO-ERROR. 
*/ 
IF AVAILABLE outorder THEN 
DO: 
  IF outorder.betriebsnr LE 1 THEN error-code = -2. 
  ELSE error-code = -5. 
  RETURN. 
END. 
 
RUN check-roomplan. 
IF error-code NE 0 THEN RETURN. 
 
/*MT ???
IF AVAILABLE res-line AND (res-line.active-flag = 0) AND (res-line.ankunft = ci-date) 
  AND (res-line.zinr NE zinr) AND (zinr NE "") THEN
DO:
  FIND FIRST resline WHERE resline.resstatus = 6 
    AND resline.zinr = zinr 
    AND RECID(resline) NE RECID(res-line) NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE resline THEN
  FIND FIRST resline WHERE resline.resstatus = 13 
    AND resline.zinr = zinr AND resline.l-zuordnung[3] = 0
    AND resline.resnr NE res-line.resnr NO-LOCK NO-ERROR. 
  IF AVAILABLE resline THEN
  DO:
    error-code = -3. 
    RETURN. 
  END.
END.
*/

IF AVAILABLE res-line AND ((res-line.active-flag = 0 AND res-line.ankunft = ci-date) 
  OR res-line.active-flag = 1) 
  AND zimmer.zistatus GE 1 AND zimmer.zistatus LE 2 THEN 
DO: 
/*
  FIND FIRST htparam WHERE paramnr = 226 NO-LOCK. 
  IF htparam.flogical = YES THEN 
  DO: 
    answer = YES. 
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Change the room status to VACANT CLEANED?",lvCAREA,"") 
      VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
  END. 
  IF answer THEN 
  DO TRANSACTION: 
    FIND CURRENT zimmer EXCLUSIVE-LOCK. 
    zimmer.zistatus = 0. 
    FIND CURRENT zimmer NO-LOCK. 
  END. 
  ELSE 
*/  
  DO: 
    IF res-line.active-flag = 1 THEN 
    DO: 
      error-code = -4. 
      RETURN. 
    END. 
  END. 
END. 
 
IF error-code = 0 THEN rmcat = zimkateg.kurzbez. 
 
PROCEDURE check-roomplan-old: 
DEFINE buffer resline FOR res-line. 
DEFINE buffer zimplan1 FOR zimplan. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE res-recid AS INTEGER. 

  IF from-date = to-date THEN 
  DO: 
    IF AVAILABLE res-line THEN 
    DO:
    FIND FIRST resline WHERE RECID(resline) NE RECID(res-line) 
      AND resline.resstatus LE 6 AND resline.active-flag EQ 1 
      AND resline.ankunft LE to-date AND resline.abreise GT to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    END.
    ELSE FIND FIRST resline WHERE resline.resstatus LE 6 
      AND resline.active-flag EQ 1 
      AND resline.ankunft LE to-date AND resline.abreise GT to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN error-code = -3. 
    RETURN. 
  END. 
 
  IF AVAILABLE res-line THEN 
  DO:
    IF res-line.active-flag = 1 THEN
    FIND FIRST resline WHERE RECID(resline) NE RECID(res-line) 
      AND resline.resstatus LE 6 AND resline.active-flag LE 1 
      AND resline.abreise GE from-date AND resline.abreise LE to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    ELSE
    DO:
      FIND FIRST resline WHERE RECID(resline) NE RECID(res-line) 
        AND resline.active-flag = 0 
        AND resline.abreise GE from-date AND resline.abreise LE to-date 
        AND resline.zinr = zinr 
        AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN
      FIND FIRST resline WHERE RECID(resline) NE RECID(res-line) 
        AND resline.active-flag = 1 
        AND resline.abreise GT from-date AND resline.abreise LE to-date 
        AND resline.zinr = zinr 
        AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    END.
  END.
  ELSE
  DO:
    FIND FIRST resline WHERE resline.active-flag = 0 
      AND resline.abreise GE from-date AND resline.abreise LE to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE resline THEN
    FIND FIRST resline WHERE resline.active-flag = 1 
      AND resline.abreise GT from-date AND resline.abreise LE to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
  END.
  IF AVAILABLE resline THEN 
  DO: 
    error-code = -3. 
    RETURN. 
  END. 
 
  IF AVAILABLE res-line THEN 
  FIND FIRST resline WHERE RECID(resline) NE RECID(res-line) 
    AND resline.resstatus LE 6 AND resline.active-flag LE 1 
    AND to-date GT resline.ankunft 
    AND to-date LE resline.abreise 
    AND resline.zinr = zinr NO-LOCK NO-ERROR. 
  ELSE FIND FIRST resline WHERE resline.resstatus LE 6 
    AND resline.active-flag LE 1 AND to-date GT resline.ankunft 
    AND to-date LE resline.abreise AND resline.zinr = zinr 
    AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE resline THEN 
  DO: 
    error-code = -3. 
    RETURN. 
  END.
END. 
 
/* New Algorithm: 15/06/2007 */
PROCEDURE check-roomplan: 
DEFINE buffer resline FOR res-line. 
DEFINE buffer zimplan1 FOR zimplan. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE res-recid AS INTEGER. 
  
  IF from-date = to-date THEN 
  DO: 
    IF AVAILABLE res-line THEN 
    DO:
    FIND FIRST resline WHERE RECID(resline) NE RECID(res-line) 
      AND resline.resstatus LE 6 AND resline.active-flag EQ 1 
      AND resline.ankunft LE to-date AND resline.abreise GT to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    END.
    ELSE FIND FIRST resline WHERE resline.resstatus LE 6 
      AND resline.active-flag EQ 1 
      AND resline.ankunft LE to-date AND resline.abreise GT to-date 
      AND resline.zinr = zinr 
      AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN error-code = -3. 
    RETURN. 
  END. 
  
  IF AVAILABLE res-line THEN
  DO:
    IF res-line.active-flag = 0 OR res-line.active-flag = 2 /* New res */ THEN
    DO:
      FIND FIRST resline WHERE resline.active-flag EQ 1
        AND resline.resstatus = 6
        AND resline.zinr = zinr 
        AND resline.abreise GT from-date 
        USE-INDEX res-zinr_ix NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN
      FIND FIRST resline WHERE resline.active-flag EQ 0
        AND resline.resstatus LE 5
        AND resline.zinr = zinr 
        AND resline.ankunft LT to-date 
        AND resline.abreise GT from-date 
        AND RECID(resline) NE RECID(res-line)
        USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
      IF NOT AVAILABLE resline THEN
      FIND FIRST resline WHERE resline.active-flag EQ 0
        AND resline.resstatus LE 5
        AND resline.zinr = zinr 
        AND from-date LT resline.abreise 
        AND to-date   GT resline.ankunft 
        AND RECID(resline) NE RECID(res-line)
        USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN error-code = -3. 
    END.
    ELSE IF res-line.active-flag = 1 THEN
    DO:
      FIND FIRST resline WHERE  resline.active-flag EQ 1
        AND resline.resstatus EQ 6
        AND resline.zinr = zinr 
        AND RECID(resline) NE RECID(res-line)
        NO-LOCK NO-ERROR.
      IF NOT AVAILABLE resline THEN
      FIND FIRST resline WHERE  resline.active-flag EQ 0
        AND resline.resstatus LE 5
        AND resline.zinr = zinr 
        AND resline.ankunft LT to-date 
        USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.      
      IF AVAILABLE resline THEN error-code = -3. 
    END.
  END.
  ELSE /* new reservation */
  DO:
    FIND FIRST resline WHERE resline.active-flag EQ 1
      AND resline.resstatus = 6
      AND resline.zinr = zinr 
      AND resline.abreise GT from-date 
      USE-INDEX res-zinr_ix NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE resline THEN
    FIND FIRST resline WHERE resline.active-flag EQ 0
      AND resline.resstatus LE 5
      AND resline.zinr = zinr 
      AND resline.ankunft LT to-date 
      AND resline.abreise GT from-date 
      USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    FIND FIRST resline WHERE resline.active-flag EQ 0
      AND resline.resstatus LE 5
      AND resline.zinr = zinr 
      AND from-date LT resline.abreise 
      AND to-date   GT resline.ankunft 
      USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN error-code = -3. 
  END. 

/* 
  IF AVAILABLE res-line THEN
  DO:
    IF res-line.active-flag = 0 THEN
    DO:
      FIND FIRST resline WHERE  resline.active-flag LE 1
        AND resline.resstatus LT 11
        AND resline.zinr = zinr 
        AND NOT resline.ankunft GE to-date 
        AND NOT resline.abreise LE from-date 
        AND RECID(resline) NE RECID(res-line)
        USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN error-code = -3. 
    END.
    ELSE IF res-line.active-flag = 1 THEN
    DO:
      FIND FIRST resline WHERE  resline.active-flag LE 1
        AND resline.resstatus LT 11
        AND resline.zinr = zinr 
        AND resline.abreise EQ from-date 
        AND RECID(resline) NE RECID(res-line)
        NO-LOCK NO-ERROR.

      IF NOT AVAILABLE resline THEN
      FIND FIRST resline WHERE  resline.active-flag LE 1
        AND resline.zinr = zinr 
        AND NOT resline.ankunft GE to-date 
        AND NOT resline.abreise LE from-date 
        AND RECID(resline) NE RECID(res-line)
        AND resline.resstatus LT 11
        USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN error-code = -3. 

    END.
  END.
  ELSE /* new reservation */
  DO:
    FIND FIRST resline WHERE  resline.active-flag LE 1
      AND resline.zinr = zinr 
      AND NOT resline.ankunft GE to-date 
      AND NOT resline.abreise LE from-date 
      USE-INDEX res-zinr_ix NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN error-code = -3. 
  END. 
*/
END. 
