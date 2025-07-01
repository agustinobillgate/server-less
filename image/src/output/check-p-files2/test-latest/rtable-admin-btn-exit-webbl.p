DEF TEMP-TABLE t-list LIKE tisch.

DEF INPUT PARAMETER TABLE FOR t-list.
DEF INPUT PARAMETER case-type AS INT.
DEFINE OUTPUT PARAMETER result-message AS CHAR.

result-message = "".

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
        FIND FIRST queasy WHERE queasy.key EQ 31 AND queasy.number1 EQ tisch.departement
        AND queasy.number2 EQ tisch.tischnr AND queasy.betriebsnr EQ 0 
        AND queasy.deci3 EQ tisch.betriebsnr AND queasy.deci3 NE t-list.betriebsnr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            DELETE queasy.
            result-message = "Saved table position deleted - " + STRING(tisch.tischnr,"99") + " ".
        END.

        FIND CURRENT tisch EXCLUSIVE-LOCK. 
        ASSIGN 
            tisch.bezeich     = t-list.bezeich 
            tisch.normalbeleg = t-list.normalbeleg
            tisch.roomcharge  = t-list.roomcharge
            tisch.betriebsnr  = t-list.betriebsnr
        .

        IF t-list.roomcharge THEN tisch.normalbeleg = 1.
        FIND CURRENT tisch NO-LOCK.
        RELEASE tisch.
        result-message = result-message + "Success".
    END.
END.

PROCEDURE fill-new-tisch: 
  BUFFER-COPY t-list TO tisch.
  IF tisch.roomcharge THEN tisch.normalbeleg = 1.
END.
