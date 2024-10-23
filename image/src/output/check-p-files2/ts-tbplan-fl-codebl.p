
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1      AS INT.
DEF INPUT PARAMETER int2      AS INT.
DEF INPUT PARAMETER curr-room AS CHAR.

DEF OUTPUT PARAMETER room AS CHAR.

IF case-type = 1 THEN
DO :
  FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = /*MTvhp.h-bill.resnr*/ int1
    AND vhp.res-line.reslinnr = /*MTvhp.h-bill.reslinnr*/ int2 NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.res-line THEN room = vhp.res-line.zinr.
END.
ELSE IF case-type = 2 THEN
DO:
  FIND FIRST vhp.zimmer WHERE vhp.zimmer.zinr = curr-room 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.zimmer THEN room = curr-room.
END.
