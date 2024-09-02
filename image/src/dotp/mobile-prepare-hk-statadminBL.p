DEF TEMP-TABLE t-zimkateg LIKE zimkateg.
DEF TEMP-TABLE z-list
    FIELD zinr              LIKE zimmer.zinr
    FIELD setup             LIKE zimmer.setup
    FIELD zikatnr           LIKE zimmer.zikatnr
    FIELD etage             LIKE zimmer.etage
    FIELD zistatus          LIKE zimmer.zistatus
    FIELD CODE              LIKE zimmer.CODE
    FIELD bediener-nr-stat  LIKE zimmer.bediener-nr-stat
    FIELD checkout          AS LOGICAL INITIAL NO
    FIELD str-reason        AS CHAR.

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE bline-list 
  FIELD zinr AS CHAR 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD bl-recid AS INTEGER. 

DEFINE TEMP-TABLE setup-list 
  FIELD nr AS INTEGER 
  FIELD CHAR AS CHAR FORMAT "x(1)". 

DEF INPUT  PARAMETER zinr AS CHAR.
DEF INPUT  PARAMETER floor AS INT.
DEF INPUT  PARAMETER dispsort AS INT.
DEF INPUT  PARAMETER statsort AS INT.
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR z-list.
DEF OUTPUT PARAMETER TABLE FOR om-list.
DEF OUTPUT PARAMETER TABLE FOR bline-list.
DEF OUTPUT PARAMETER TABLE FOR setup-list.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = fdate. 
 
RUN bed-setup.
RUN create-list. 

FOR EACH zimmer NO-LOCK:
    CREATE z-list.
    BUFFER-COPY zimmer TO z-list.
    IF zimmer.zistatus = 2 THEN 
    DO:
        FIND FIRST res-line WHERE res-line.resstatus = 8 
            AND res-line.zinr = zimmer.zinr
            AND res-line.abreise = ci-date NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN z-list.checkout = YES.
    END.
    
    /*ITA 030717*/
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
        AND outorder.betriebsnr LE 2 
        AND outorder.gespstart LE ci-date 
        AND outorder.gespende GE ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN 
        ASSIGN z-list.str-reason = ENTRY(1, outorder.gespgrund, "$").
    ELSE ASSIGN z-list.str-reason = " ".
END.

FOR EACH zimkateg:
    CREATE t-zimkateg.
    BUFFER-COPY zimkateg TO t-zimkateg.
END.
 
PROCEDURE bed-setup: 
DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO. 
/*  this record must exist !!! */ 
  CREATE setup-list. 
  ASSIGN
    setup-list.nr = 1
    setup-list.char = " "
  . 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK: 
    CREATE setup-list. 
    setup-list.nr = paramtext.txtnr - 9199. 
    setup-list.char = SUBSTR(paramtext.notes,1,1). 
    it-exist = YES. 
  END. 
END. 
 
PROCEDURE create-list: 
  FOR EACH zimmer NO-LOCK: 
 
    CREATE bline-list. 
    ASSIGN bline-list.zinr = zimmer.zinr. 
 
    create om-list. 
    om-list.zinr = zimmer.zinr. 
    om-list.ind = zimmer.zistatus + 1. 
  END. 
 
 /* SY 20 Sept 2015
 betriebsnr 
             0,1 : OOO HK, OOO ENG
             3,4 : OOS HK, OOS ENG
             2   : OM without reservation
 otherwise (xx)  : OM with res-line.resnr = xx 
                   and res-line.zinr = outorder.zinr
 lack here: 0 could be OOO ENG and also OM with res-line.resnr = 1
            but the chance is quite small
 */ 
                
  FOR EACH outorder WHERE outorder.betriebsnr GE 2 AND 
    outorder.gespstart LE ci-date AND outorder.gespende GE ci-date NO-LOCK: 
    FIND FIRST om-list WHERE om-list.zinr = outorder.zinr.
    IF outorder.betriebsnr = 3 OR outorder.betriebsnr = 4 THEN
        om-list.ind = 10. /* OOS */
    ELSE om-list.ind = 8. /* OM  */
  END. 
END. 
