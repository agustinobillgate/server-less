DEFINE TEMP-TABLE reslin-list LIKE res-line. 

DEFINE INPUT PARAMETER direct-change    AS LOGICAL NO-UNDO. 
DEFINE INPUT PARAMETER fixed-rate       AS LOGICAL NO-UNDO. 
DEFINE INPUT PARAMETER ebdisc-flag      AS LOGICAL NO-UNDO. 
DEFINE INPUT PARAMETER kbdisc-flag      AS LOGICAL NO-UNDO. 
DEFINE INPUT PARAMETER rate-readonly    AS LOGICAL NO-UNDO. 

DEFINE INPUT PARAMETER gastnr           AS INTEGER NO-UNDO.

DEFINE INPUT PARAMETER res-mode         AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER argt             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER contcode         AS CHAR    NO-UNDO.

DEFINE INPUT PARAMETER bookdate         AS DATE    NO-UNDO.

DEFINE INPUT PARAMETER TABLE FOR reslin-list.

DEFINE OUTPUT PARAMETER restricted-disc AS LOGICAL NO-UNDO. 
DEFINE OUTPUT PARAMETER new-rate        AS DECIMAL NO-UNDO INIT ?.
DEFINE OUTPUT PARAMETER rate-tooltip    AS CHAR    NO-UNDO INIT "?".

DEFINE VARIABLE wd-array        AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

/************************* FUNCTION ****************************************/
FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs  AS INTEGER, 
     INPUT kind1    AS INTEGER, 
     INPUT kind2    AS INTEGER). 
  DEF VAR rate      AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

RUN set-roomrate.

PROCEDURE set-roomrate: 
DEFINE VARIABLE ci-date         AS DATE                 NO-UNDO. 
DEFINE VARIABLE datum           AS DATE                 NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE VARIABLE current-rate    AS DECIMAL              NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INIT NO      NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
  
  FIND FIRST arrangement WHERE arrangement.arrangement = argt 
      NO-LOCK NO-ERROR.
  IF NOT AVAILABLE arrangement THEN RETURN.

  RUN htpdate.p (87, OUTPUT ci-date).
  FIND FIRST reslin-list.
 
  ASSIGN 
      current-rate = reslin-list.zipreis
/*  DO NOT change ! */ 
      datum        = reslin-list.ankunft
  . 
  IF res-mode = "inhouse" THEN datum = ci-date. 
 
  IF reslin-list.l-zuordnung[1] NE 0 THEN curr-zikatnr = reslin-list.l-zuordnung[1]. 
  ELSE curr-zikatnr = reslin-list.zikatnr. 
 
  IF reslin-list.erwachs = 0 AND reslin-list.kind1 = 0
    AND reslin-list.kind2 = 0 THEN 
  DO:    
    ASSIGN new-rate = 0.
    RETURN.
  END.

  IF fixed-rate THEN 
  DO: 
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = reslin-list.resnr 
      AND reslin-queasy.reslinnr = reslin-list.reslinnr 
      AND datum GE reslin-queasy.date1 
      AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN
    DO:
      ASSIGN
        new-rate     = reslin-queasy.deci1
        rate-tooltip = "". 

      RETURN.
    END.
  END. 
 
  FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK NO-ERROR.     
  IF AVAILABLE guest-pr THEN 
  DO: 
    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
      = reslin-list.reserve-int NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.logi3 THEN datum = reslin-list.ankunft. 

    IF bookdate NE ? THEN
    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, reslin-list.resnr, 
      reslin-list.reslinnr, ("!" + contcode), bookdate, datum, reslin-list.ankunft,
      reslin-list.abreise, reslin-list.reserve-int, arrangement.argtnr,
      curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
      reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
      OUTPUT new-rate, OUTPUT restricted-disc, OUTPUT kback-flag).
    ELSE
    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, reslin-list.resnr, 
      reslin-list.reslinnr, ("!" + contcode), ci-date, datum, reslin-list.ankunft,
      reslin-list.abreise, reslin-list.reserve-int, arrangement.argtnr,
      curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
      reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
      OUTPUT new-rate, OUTPUT restricted-disc, OUTPUT kback-flag).
     
    IF rate-found THEN RETURN.
  END. /* IF AVAILABLE guest-pr */ 
     
  IF res-mode = "inhouse" THEN 
  DO: 
    FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE datum 
      AND katpreis.endperiode GE datum 
      AND katpreis.betriebsnr = wd-array[WEEKDAY(datum)] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN 
    FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE datum 
      AND katpreis.endperiode GE datum        
      AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
  END. 
  ELSE 
  DO: 
    FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND datum GE katpreis.startperiode 
      AND datum LE katpreis.endperiode 
      AND katpreis.betriebsnr = wd-array[WEEKDAY(datum)] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN     
    FIND FIRST katpreis WHERE katpreis.zikatnr = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND datum GE katpreis.startperiode 
      AND datum LE katpreis.endperiode 
      AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
  END. 
      
  IF AVAILABLE katpreis THEN new-rate = get-rackrate(reslin-list.erwachs, 
      reslin-list.kind1, reslin-list.kind2). 
  ELSE new-rate = 0. 


  IF NOT direct-change AND NOT rate-readonly THEN
  DO:
    IF current-rate NE 0 AND new-rate = 0 THEN
      ASSIGN new-rate = current-rate.
  END.  
END. 
 
