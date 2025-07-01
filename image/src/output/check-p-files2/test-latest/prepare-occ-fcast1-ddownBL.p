.
DEFINE TEMP-TABLE segm-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD segm                AS INTEGER 
  FIELD bezeich             AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE argt-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD argtnr              AS INTEGER
  FIELD argt                AS CHAR 
  FIELD bezeich             AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE zikat-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD zikatnr             AS INTEGER 
  FIELD bezeich             AS CHAR FORMAT "x(24)". 

DEF OUTPUT PARAMETER ci-date AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR segm-list.
DEF OUTPUT PARAMETER TABLE FOR argt-list.
DEF OUTPUT PARAMETER TABLE FOR zikat-list.

DEF VARIABLE vhp-limited AS LOGICAL NO-UNDO INIT NO.

RUN htpdate.p(87, OUTPUT ci-date).
RUN create-segm.
RUN create-argt.
RUN create-zikat.

PROCEDURE create-segm: 
  FOR EACH segment WHERE segment.betriebsnr LE 2 NO-LOCK 
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
  FOR EACH arrangement NO-LOCK BY arrangement.arrangement: 
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

