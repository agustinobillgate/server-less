DEFINE TEMP-TABLE segm1-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD segm     AS INTEGER 
    FIELD bezeich  AS CHAR FORMAT "x(24)"
    FIELD bezeich1 AS CHAR FORMAT "x(24)"
  .

DEFINE TEMP-TABLE argt-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD argtnr   AS INTEGER
    FIELD argt     AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(24)"
    .

DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(24)"
    . 

DEFINE OUTPUT PARAMETER TABLE FOR segm1-list.
DEFINE OUTPUT PARAMETER TABLE FOR argt-list.
DEFINE OUTPUT PARAMETER TABLE FOR zikat-list.

RUN create-segm. 
RUN create-argt. 
RUN create-zikat. 

PROCEDURE create-segm: 
    FOR EACH segment WHERE segment.betriebsnr LE 2 NO-LOCK BY segment.segmentcode:
        CREATE segm1-list. 
        ASSIGN 
            segm1-list.segm = segment.segmentcode 
            segm1-list.bezeich = STRING(segmentcode,">>9 ") + ENTRY(1, segment.bezeich, "$$0"). 
            segm1-list.bezeich1 =  ENTRY(1, segment.bezeich, "$$0").
    END. 
END. 
 
PROCEDURE create-argt: 
    FOR EACH arrangement NO-LOCK BY arrangement.arrangement: 
        CREATE argt-list. 
        ASSIGN 
            argt-list.argt = arrangement.arrangement 
            argt-list.bezeich = STRING(arrangement.arrangement,"x(5)") + " " + arrangement.argt-bez. 
    END. 
END. 
 
PROCEDURE create-zikat: 
    FOR EACH zimkateg NO-LOCK BY zimkateg.kurzbez: 
        CREATE zikat-list. 
        ASSIGN 
            zikat-list.zikatnr = zimkateg.zikatnr 
            zikat-list.kurzbez = zimkateg.kurzbez 
            zikat-list.bezeich = zimkateg.bezeich. 
    END. 
END. 

