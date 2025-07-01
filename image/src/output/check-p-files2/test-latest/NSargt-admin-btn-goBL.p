
DEFINE TEMP-TABLE p-list LIKE arrangement.

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER q1-recid        AS INT.
DEF INPUT PARAMETER q2-recid        AS INT.
DEF INPUT PARAMETER curr-select     AS CHAR.
DEF INPUT PARAMETER argt-artnr      AS INT.
DEF INPUT PARAMETER argt-dept       AS INT.
DEF INPUT PARAMETER q1-list-argtnr  AS INT.
DEF INPUT PARAMETER argt-price      AS DECIMAL.
DEF INPUT PARAMETER argt-proz       AS DECIMAL.
DEF INPUT PARAMETER comments        AS CHAR.
DEF OUTPUT PARAMETER err            AS INT INIT 0.
DEF OUTPUT PARAMETER artikel-bezeich AS CHAR.

DEFINE buffer argtline FOR argt-line.

FIND FIRST p-list NO-ERROR.
IF curr-select = "ins" THEN 
DO:
    FIND FIRST arrangement WHERE RECID(arrangement) = q1-recid NO-LOCK NO-ERROR. /* Malik Serverless 333 : NO-LOCK -> NO-LOCK NO-ERROR */
    IF NOT AVAILABLE arrangement THEN RETURN. /* Malik Serverless 333 */
    FIND FIRST artikel WHERE artikel.artnr = argt-artnr 
      AND artikel.artart = 0 
      AND artikel.departement = argt-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel THEN 
    DO: 
      err = 1.
      RETURN NO-APPLY. 
    END. 
    FIND FIRST argtline WHERE argtline.argtnr = q1-list-argtnr 
      AND argtline.argt-artnr = argt-artnr 
      AND argtline.departement = argt-dept NO-LOCK NO-ERROR. 
    IF AVAILABLE argtline THEN 
    DO: 
      err = 2.
      RETURN NO-APPLY. 
    END. 
    DO: 
      create argt-line. 
      RUN fill-argtline.
      FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK.
      artikel-bezeich = artikel.bezeich.
    END.
END.

ELSE IF curr-select = "chg2" THEN 
DO:
    FIND FIRST argt-line WHERE RECID(argt-line) = q2-recid NO-LOCK.
    FIND FIRST artikel WHERE artikel.artnr = argt-artnr 
      AND artikel.artart = 0 
      AND artikel.departement = argt-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel THEN 
    DO: 
      err = 1.
      RETURN NO-APPLY. 
    END. 
    FIND CURRENT argt-line EXCLUSIVE-LOCK. 
    argt-line.argt-artnr = argt-artnr. 
    argt-line.departement = argt-dept. 
    argt-line.betrag = argt-price. 
    argt-line.vt-percnt = argt-proz.
    FIND CURRENT argt-line NO-LOCK.
END.

ELSE IF curr-select = "add" THEN 
DO:
    FIND FIRST artikel WHERE artikel.artnr = p-list.artnr-logis 
      AND artikel.artart = 0 
      AND artikel.departement = p-list.intervall NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel THEN 
    DO: 
      err = 1.
      RETURN NO-APPLY. 
    END. 
    DO: 
      create arrangement. 
      RUN fill-argt. 
    END. 
END.

ELSE IF curr-select = "chg" THEN 
DO:
    FIND FIRST arrangement WHERE RECID(arrangement) = q1-recid NO-LOCK NO-ERROR. /* Malik Serverless 333 NO-LOCK -> NO-LOCK NO-ERROR */
    /* Malik Serverless 333 */
    IF AVAILABLE arrangement THEN 
    DO:
      FIND CURRENT arrangement EXCLUSIVE-LOCK.
      RUN fill-argt.
      FIND CURRENT arrangement NO-LOCK. 
    END.
    /* END Malik */
END.



PROCEDURE fill-argtline: 
  ASSIGN 
    argt-line.argtnr = arrangement.argtnr 
    argt-line.argt-artnr = argt-artnr 
    argt-line.departement = argt-dept 
    argt-line.betrag = argt-price. 
    argt-line.vt-percnt = argt-proz. 
END. 


PROCEDURE fill-argt: 
  ASSIGN 
    arrangement.argtnr = p-list.argtnr 
    arrangement.arrangement  = p-list.arrangement 
    arrangement.argt-bez  = p-list.argt-bez 
    arrangement.argt-rgbez = p-list.argt-bez 
    arrangement.artnr-logis  = p-list.artnr-logis 
    arrangement.intervall = p-list.intervall 
    arrangement.segmentcode = 1 
    arrangement.zuordnung = comments. 
END. 
