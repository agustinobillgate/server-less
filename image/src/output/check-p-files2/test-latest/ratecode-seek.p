/* get ratecode record if any */

DEFINE INPUT PARAMETER resnr        AS INTEGER.
DEFINE INPUT PARAMETER reslinnr     AS INTEGER.
DEFINE INPUT PARAMETER prcode       AS CHAR.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE OUTPUT PARAMETER s-recid     AS INTEGER INITIAL 0.

DEFINE VARIABLE ct                  AS CHAR    NO-UNDO.
DEFINE VARIABLE argtNo              AS INTEGER NO-UNDO.
DEFINE VARIABLE rmcatNo             AS INTEGER NO-UNDO.
DEFINE VARIABLE w-day               AS INTEGER NO-UNDO.
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE VAR tmp-date AS DATE. /* Malik serverless */
 

/***********************************************************************/

FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.reslinnr = reslinnr NO-LOCK.
FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement
    NO-LOCK NO-ERROR.

IF AVAILABLE arrangement THEN  /*FT*/
    argtNo  = arrangement.argtnr.
rmcatNo = res-line.zikatnr. 
/* Malik Serverless */
tmp-date = datum - 1.
w-day   = wd-array[WEEKDAY(tmp-date)].
/* w-day   = wd-array[WEEKDAY(datum - 1)]. */
/* END Malik */

ct = res-line.zimmer-wunsch.
IF ct MATCHES("*$CODE$*") THEN
DO:
  ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
  prcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
END.

FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = w-day AND ratecode.erwachs = res-line.erwachs
  AND ratecode.kind1 = res-line.kind1 AND ratecode.kind2 = res-line.kind2
  NO-LOCK NO-ERROR. 

FIND FIRST ratecode WHERE ratecode.code = prcode  /*FT*/
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = w-day AND ratecode.erwachs = res-line.erwachs
  AND ratecode.kind1 = res-line.kind1 AND ratecode.kind2 = res-line.kind2
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = 0 AND ratecode.erwachs = res-line.erwachs
  AND ratecode.kind1 = res-line.kind1 AND ratecode.kind2 = res-line.kind2
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN  /*FT*/
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = 0 AND ratecode.erwachs = res-line.erwachs
  AND ratecode.kind1 = res-line.kind1 AND ratecode.kind2 = res-line.kind2
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = w-day AND ratecode.erwachs = res-line.erwachs
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN  /*FT*/
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = w-day AND ratecode.erwachs = res-line.erwachs
  NO-LOCK NO-ERROR.
    
IF NOT AVAILABLE ratecode THEN
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = 0 AND ratecode.erwachs = res-line.erwachs
  NO-LOCK NO-ERROR.

IF NOT AVAILABLE ratecode THEN    /*FT*/
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = 0 AND ratecode.erwachs = res-line.erwachs
  NO-LOCK NO-ERROR. 

IF AVAILABLE ratecode THEN s-recid = RECID(ratecode).
