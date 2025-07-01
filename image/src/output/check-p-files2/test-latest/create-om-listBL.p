DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID" 
  FIELD ind AS INTEGER INITIAL 0
  FIELD reason      AS CHAR     /*MT 11/12/12 */
  FIELD gespstart   AS DATE     /*MT 11/12/12 */
  FIELD gespende    AS DATE.    /*MT 11/12/12 */

DEFINE INPUT  PARAMETER fdate AS DATE.
DEFINE INPUT  PARAMETER tdate AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR om-list.

DEF VAR datum AS DATE.

IF fdate NE ? AND tdate NE ? THEN
DO datum = fdate TO tdate:
    FOR EACH outorder WHERE 
      (outorder.gespstart GE datum AND outorder.gespstart LE datum) OR 
      (outorder.gespstart LE datum AND outorder.gespende GE datum) NO-LOCK:
      FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK
        NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
        /*MT 11/12/12 */
        IF NUM-ENTRIES(outorder.gespgrund, "$") GE 1 THEN
            FIND FIRST bediener WHERE bediener.nr = INT(ENTRY(2, outorder.gespgrund, "$"))
            NO-LOCK NO-ERROR.
        ELSE
        FIND FIRST bediener WHERE bediener.nr = zimmer.bediener-nr-stat 
          NO-LOCK NO-ERROR.

        create om-list. 
        om-list.zinr = outorder.zinr. 
        om-list.ind = outorder.betriebsnr + 1.
        om-list.gespstart = outorder.gespstart.       /*MT 11/12/12 */
        om-list.gespende = outorder.gespende.         /*MT 11/12/12 */
        IF om-list.ind GE 6 THEN om-list.ind = 3.
        IF AVAILABLE bediener THEN om-list.userinit = bediener.userinit. 

        /*MT 11/12/12 */
        IF NUM-ENTRIES(outorder.gespgrund, "$") GE 1 THEN
            om-list.reason = ENTRY(1, outorder.gespgrund, "$").
        ELSE om-list.reason = outorder.gespgrund.
      END.
    END.
END.
ELSE
DO:
    FOR EACH outorder /*MT 20/05/13WHERE 
    
        outorder.gespstart GE ci-date NO-LOCK:
        
        outorder.gespstart LE ci-date AND outorder.gespende GE ci-date*/ NO-LOCK:
      FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK
          NO-ERROR. 
        /*MT 11/12/12
        FIND FIRST bediener WHERE bediener.nr = zimmer.bediener-nr-stat 
          NO-LOCK NO-ERROR.
        */
      IF AVAILABLE zimmer THEN
      DO:
        /*MT 11/12/12 */
        IF NUM-ENTRIES(outorder.gespgrund, "$") GE 1 THEN
            FIND FIRST bediener WHERE bediener.nr = INT(ENTRY(2, outorder.gespgrund, "$"))
            NO-LOCK NO-ERROR.
        ELSE
        FIND FIRST bediener WHERE bediener.nr = zimmer.bediener-nr-stat 
          NO-LOCK NO-ERROR.
    
        create om-list. 
        om-list.zinr = outorder.zinr. 
        om-list.ind = outorder.betriebsnr + 1.
        om-list.gespstart = outorder.gespstart.       /*MT 11/12/12 */
        om-list.gespende = outorder.gespende.         /*MT 11/12/12 */
        IF om-list.ind GE 6 THEN om-list.ind = 3.
        IF AVAILABLE bediener THEN om-list.userinit = bediener.userinit. 
    
        /*MT 11/12/12 */
        IF NUM-ENTRIES(outorder.gespgrund, "$") GE 1 THEN
            om-list.reason = ENTRY(1, outorder.gespgrund, "$").
        ELSE om-list.reason = outorder.gespgrund.
      END. 
    END.
END.


/*
FOR EACH outorder NO-LOCK: 
  FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK. 
  FIND FIRST bediener WHERE bediener.nr = zimmer.bediener-nr-stat 
    NO-LOCK NO-ERROR. 
  create om-list. 
  om-list.zinr = outorder.zinr. 
  om-list.ind = outorder.betriebsnr + 1. 
  IF om-list.ind GE 6 THEN om-list.ind = 3.
  IF AVAILABLE bediener THEN om-list.userinit = bediener.userinit. 
END. 
*/
