DEF TEMP-TABLE t-list LIKE tisch.

DEF INPUT PARAMETER TABLE FOR t-list.
DEF INPUT PARAMETER case-type AS INT.

FIND FIRST t-list.
IF case-type = 1 THEN   /*MT add */
DO :
    create tisch. 
    RUN fill-new-tisch. 
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO :
    FIND FIRST tisch WHERE tisch.departement = t-list.departement
        AND tisch.tischnr = t-list.tischnr NO-LOCK.
    IF AVAILABLE tisch THEN DO:
        FIND CURRENT tisch EXCLUSIVE-LOCK. 
        ASSIGN 
            tisch.bezeich     = t-list.bezeich 
            tisch.normalbeleg = t-list.normalbeleg
            tisch.roomcharge  = t-list.roomcharge.

        IF t-list.roomcharge THEN tisch.normalbeleg = 1.
        FIND CURRENT tisch NO-LOCK.
        RELEASE tisch.
    END.
END.

PROCEDURE fill-new-tisch: 
  BUFFER-COPY t-list TO tisch.
  IF tisch.roomcharge THEN tisch.normalbeleg = 1.
END.
