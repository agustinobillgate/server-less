define TEMP-TABLE g-list like mc-types.

DEF INPUT PARAMETER TABLE FOR g-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST g-list.
IF case-type = 1 THEN
DO :
    CREATE mc-types.
    BUFFER-COPY g-list TO mc-types.
END.
ELSE IF case-type = 2 THEN
DO:
   FIND FIRST mc-types WHERE RECID(mc-types) = rec-id EXCLUSIVE-LOCK.  
   IF mc-types.nr NE g-list.nr THEN
   DO:
     FOR EACH mc-disc WHERE mc-disc.nr = mc-type.nr:
       mc-disc.nr = g-list.nr.
     END.
     FOR EACH mc-guest WHERE mc-guest.nr = mc-type.nr:
       mc-guest.nr = g-list.nr.
     END.
   END.
   BUFFER-COPY g-list TO mc-types.
END.
