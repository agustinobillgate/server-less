DEF TEMP-TABLE adhoc
    FIELD acode     AS CHAR     FORMAT "x(10)"  COLUMN-LABEL "Adhoc Code"
    FIELD artnr     AS INTEGER  FORMAT ">>9"    COLUMN-LABEL "ArtNo"
    FIELD deptnr    AS INTEGER  FORMAT ">9"     COLUMN-LABEL "Dept"
    FIELD bezeich   AS CHAR     FORMAT "x(16)"  COLUMN-LABEL "Description"
    FIELD amount    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Adult"
    FIELD child1    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Child1"
    FIELD child2    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Child2"
    FIELD post-type AS INTEGER  FORMAT "9"      COLUMN-LABEL "N"
.

DEF TEMP-TABLE argt-list
    FIELD argt-artnr  LIKE argt-line.argt-artnr COLUMN-LABEL "ArtNo" 
    FIELD bezeich     LIKE artikel.bezeich      COLUMN-LABEL "Article Description" FORMAT "x(20)" 
    FIELD departement LIKE artikel.departement  COLUMN-LABEL "Dept" 
    FIELD deci1       AS DECIMAL                COLUMN-LABEL "Amount" FORMAT ">>>,>>>,>>9.99" 
    FIELD date1       AS DATE                   COLUMN-LABEL "FromDate" 
    FIELD date2       AS DATE                   COLUMN-LABEL "To Date " 
    FIELD deci2       AS DECIMAL                COLUMN-LABEL "Child1" FORMAT ">>>,>>>,>>9.99" 
    FIELD deci3       AS DECIMAL                COLUMN-LABEL "Child2" FORMAT ">>>,>>>,>>9.99" 
    FIELD post-type   AS CHAR FORMAT "x(12)"    COLUMN-LABEL "Post Type" 
    FIELD pers-type   AS CHAR FORMAT "x(6)"     COLUMN-LABEL "For"
    FIELD fakt-modus  AS INTEGER
    FIELD s-recid     AS INTEGER
.

DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER adhoc-code  AS CHAR    NO-UNDO.
DEF INPUT PARAMETER argtnr      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resnr       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinnr    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-date   AS DATE    NO-UNDO.
DEF INPUT PARAMETER to-date     AS DATE    NO-UNDO.
DEF INPUT PARAMETER TABLE FOR adhoc.
DEF OUTPUT PARAMETER TABLE FOR argt-list.

DEF VARIABLE post-type  AS CHAR FORMAT "x(12)" EXTENT 6 NO-UNDO.
DEF VARIABLE pers-type  AS CHAR FORMAT "x(6)" EXTENT 3  NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "argt-frate". 

ASSIGN
    post-type[1] = translateExtended("Daily",lvCAREA,"")
    post-type[2] = translateExtended("CI Day",lvCAREA,"")
    post-type[3] = translateExtended("2nd Day",lvCAREA,"")
    post-type[4] = translateExtended("Mon 1st Day",lvCAREA,"")
    post-type[5] = translateExtended("Mon LastDay",lvCAREA,"")
    post-type[6] = translateExtended("Special",lvCAREA,"").

ASSIGN
    pers-type[1] = translateExtended("Adult",lvCAREA,"")
    pers-type[2] = translateExtended("Child",lvCAREA,"")
    pers-type[3] = translateExtended("Ch2",lvCAREA,"").


RUN create-adhoc-argt.
RUN create-argt-list.

PROCEDURE create-adhoc-argt:
  FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "fargt-line"
    AND reslin-queasy.char1 = "" AND reslin-queasy.resnr = resnr
    AND reslin-queasy.number2 = argtnr 
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE reslin-queasy:
    FIND CURRENT reslin-queasy EXCLUSIVE-LOCK.
    DELETE reslin-queasy.
    RELEASE reslin-queasy.
    FIND NEXT reslin-queasy WHERE reslin-queasy.KEY = "fargt-line"
      AND reslin-queasy.char1 = "" AND reslin-queasy.resnr = resnr
      AND reslin-queasy.number2 = argtnr 
      AND reslin-queasy.reslinnr = reslinnr NO-LOCK NO-ERROR.
  END.

  FOR EACH adhoc WHERE adhoc.acode = adhoc-code NO-LOCK:
    RUN fill-adhoc-argt.
  END.
END.

PROCEDURE fill-adhoc-argt:
  CREATE reslin-queasy.
  ASSIGN
    reslin-queasy.key      = "fargt-line"
    reslin-queasy.number1  = adhoc.deptnr
    reslin-queasy.number2  = argtnr
    reslin-queasy.number3  = adhoc.artnr
    reslin-queasy.resnr    = resnr
    reslin-queasy.reslinnr = reslinnr 
    reslin-queasy.deci1    = adhoc.amount 
    reslin-queasy.date1    = from-date
    reslin-queasy.date2    = to-date
    reslin-queasy.deci2    = adhoc.child1 
    reslin-queasy.deci3    = adhoc.child2
  . 
END.

PROCEDURE create-argt-list: 
  FOR EACH reslin-queasy WHERE key = "fargt-line" 
    AND reslin-queasy.char1 = "" 
    AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.number2 =  argtnr 
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK, 
    FIRST argt-line WHERE argt-line.argtnr = reslin-queasy.number2 
      AND argt-line.argt-artnr = reslin-queasy.number3 
      AND argt-line.departement = reslin-queasy.number1 NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
      AND artikel.departement = argt-line.departement NO-LOCK 
    BY argt-line.argt-artnr BY reslin-queasy.date1:
    CREATE argt-list.
    ASSIGN
        argt-list.argt-artnr  = argt-line.argt-artnr
        argt-list.bezeich     = artikel.bezeich
        argt-list.departement = artikel.departement
        argt-list.deci1       = reslin-queasy.deci1
        argt-list.deci2       = reslin-queasy.deci2
        argt-list.deci3       = reslin-queasy.deci3
        argt-list.date1       = reslin-queasy.date1
        argt-list.date2       = reslin-queasy.date2
        argt-list.fakt-modus  = argt-line.fakt-modus
        argt-list.s-recid     = INTEGER(RECID(reslin-queasy))
        argt-list.post-type   = post-type[argt-line.fakt-modus]
        argt-list.pers-type   = pers-type[INTEGER(argt-line.vt-percnt) + 1]
    .
  END.
END. 
