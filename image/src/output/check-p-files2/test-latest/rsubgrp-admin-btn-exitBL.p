DEFINE TEMP-TABLE wgrpdep-list LIKE wgrpdep
    FIELD bg-color   AS INTEGER LABEL "BG-Color"      FORMAT "99" 
    FIELD kiosk-flag AS LOGICAL LABEL "Used in Kiosk" INIT YES.

DEF INPUT PARAMETER TABLE FOR wgrpdep-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER dept AS INT.

FIND FIRST wgrpdep-list.
IF case-type = 1 THEN   /*MT add */
DO :
    CREATE wgrpdep.
    RUN fill-new-wgrpdep.
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST wgrpdep WHERE wgrpdep.departement = wgrpdep-list.departement
        AND wgrpdep.zknr = wgrpdep-list.zknr NO-LOCK NO-ERROR.
    IF AVAILABLE wgrpdep THEN
    DO:
      FIND CURRENT wgrpdep EXCLUSIVE-LOCK. 
      ASSIGN
        wgrpdep.bezeich    = wgrpdep-list.bezeich
        wgrpdep.betriebsnr = wgrpdep-list.betriebsnr
        /*wgrpdep.fibukonto  = wgrpdep-list.fibukonto*/
        wgrpdep.fibukonto = STRING(wgrpdep-list.bg-color) + ";" +
                            STRING(INT(wgrpdep-list.kiosk-flag)) + ";".
      . 
      FIND CURRENT wgrpdep NO-LOCK. 
    END.
END.

PROCEDURE fill-new-wgrpdep: 
  ASSIGN
    wgrpdep.departement = dept
    wgrpdep.zknr        = wgrpdep-list.zknr 
    wgrpdep.bezeich     = wgrpdep-list.bezeich 
    wgrpdep.betriebsnr  = wgrpdep-list.betriebsnr
    wgrpdep.fibukonto   = STRING(wgrpdep-list.bg-color) + ";"
             + STRING(INTEGER(wgrpdep-list.kiosk-flag)) + ";".
END. 
