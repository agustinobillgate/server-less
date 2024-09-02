
DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

DEFINE TEMP-TABLE segm-list 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD segm AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE argt-list 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD argtnr AS INTEGER
  FIELD argt AS CHAR 
  FIELD bezeich AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE zikat-list 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD zikatnr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

/*ITA 290318*/
DEFINE TEMP-TABLE outlook-list
    FIELD SELECTED   AS LOGICAL INITIAL NO
    FIELD outlook-nr AS INTEGER
    FIELD bezeich    AS CHAR FORMAT "x(24)".

DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER vhp-limited     AS LOGICAL. 
DEFINE OUTPUT PARAMETER curr-date       AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR segm-list.
DEFINE OUTPUT PARAMETER TABLE FOR argt-list.
DEFINE OUTPUT PARAMETER TABLE FOR zikat-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-buff-queasy.
DEFINE OUTPUT PARAMETER TABLE FOR outlook-list.
DEFINE OUTPUT PARAMETER local-curr      AS CHAR NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "occ-fcast1".

DEF BUFFER buff-queasy FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
curr-date  = htparam.fdate. 

FIND FIRST buff-queasy WHERE buff-queasy.KEY = 140 AND buff-queasy.char1 = lvCarea NO-LOCK NO-ERROR.
IF AVAILABLE buff-queasy THEN
DO:
    CREATE t-buff-queasy.
    BUFFER-COPY buff-queasy TO t-buff-queasy.
END.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK.
ASSIGN local-curr = htparam.fchar.

RUN create-segm. 
RUN create-argt. 
RUN create-zikat. 
RUN create-outlook.

PROCEDURE create-outlook:
    FOR EACH paramtext WHERE paramtext.txtnr = 230 NO-LOCK:
        CREATE outlook-list.
        ASSIGN 
            outlook-list.outlook-nr = paramtext.sprachcode
            outlook-list.bezeich = paramtext.ptexte.
    END.
END.

PROCEDURE create-segm: 
  FOR EACH segment WHERE segment.betriebsnr LE 2
      AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 NO-LOCK 
    BY segment.segmentcode: 
    IF NOT vhp-limited OR (vhp-limited AND segment.vip-level = 0) THEN
    DO:
      CREATE segm-list. 
      ASSIGN 
        segm-list.segm = segment.segmentcode 
        segm-list.bezeich = STRING(segmentcode,">>9 ") + ENTRY(1, segment.bezeich, "$$0")
      .
    END.
  END. 
END. 
 
PROCEDURE create-argt: 
  FOR EACH arrangement WHERE arrangement.weeksplit = NO NO-LOCK 
      BY arrangement.arrangement: 
    CREATE argt-list. 
    ASSIGN 
      argt-list.argt = arrangement.arrangement 
      argt-list.bezeich = STRING(arrangement.arrangement,"x(5)") + " " 
        + arrangement.argt-bez. 
  END. 
END. 
 
PROCEDURE create-zikat: 
  FOR EACH zimkateg NO-LOCK BY zimkateg.bezeich: 
    CREATE zikat-list. 
    ASSIGN 
      zikat-list.zikatnr = zimkateg.zikatnr 
      zikat-list.bezeich = zimkateg.bezeich. 
  END. 
END. 

