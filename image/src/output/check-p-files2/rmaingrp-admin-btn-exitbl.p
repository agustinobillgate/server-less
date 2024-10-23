
DEFINE TEMP-TABLE wgrpgen-list LIKE wgrpgen. 

DEF INPUT PARAMETER TABLE FOR wgrpgen-list.
DEF INPUT PARAMETER case-type AS INT.

FIND FIRST wgrpgen-list.
IF case-type = 1 THEN   /*MT add */
DO :
    CREATE wgrpgen.
    RUN fill-new-wgrpgen.
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST wgrpgen WHERE wgrpgen.eknr = wgrpgen-list.eknr NO-LOCK NO-ERROR.
    IF AVAILABLE wgrpgen THEN
    DO:
      FIND CURRENT wgrpdep EXCLUSIVE-LOCK. 
      ASSIGN
          wgrpgen.bezeich = wgrpgen-list.bezeich.
    END.
END.

PROCEDURE fill-new-wgrpgen: 
  wgrpgen.eknr = wgrpgen-list.eknr. 
  wgrpgen.bezeich = wgrpgen-list.bezeich. 
END. 

