
DEFINE TEMP-TABLE adhoc
    FIELD acode     AS CHAR     FORMAT "x(10)"  COLUMN-LABEL "Adhoc Code"
    FIELD artnr     AS INTEGER  FORMAT ">>9"    COLUMN-LABEL "ArtNo"
    FIELD deptnr    AS INTEGER  FORMAT ">9"     COLUMN-LABEL "Dept"
    FIELD bezeich   AS CHAR     FORMAT "x(16)"  COLUMN-LABEL "Description"
    FIELD amount    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Adult"
    FIELD child1    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Child1"
    FIELD child2    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Child2"
    FIELD post-type AS INTEGER  FORMAT "9"      COLUMN-LABEL "N".

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
    FIELD vt-percnt   AS INTEGER
    FIELD s-recid     AS INTEGER
.

DEF INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER resnr           AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER reslinnr        AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER argt            AS CHAR     NO-UNDO.
DEF INPUT PARAMETER ankunft         AS DATE     NO-UNDO.
DEF INPUT PARAMETER abreise         AS DATE     NO-UNDO.

DEF OUTPUT PARAMETER argtnr  AS INTEGER         NO-UNDO.
DEF OUTPUT PARAMETER TABLE   FOR adhoc.
DEF OUTPUT PARAMETER TABLE   FOR argt-list.

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

FIND FIRST arrangement WHERE arrangement.arrangement = argt NO-LOCK.
ASSIGN argtnr = arrangement.argtnr.

RUN create-browseb2.
RUN create-argt-list.

PROCEDURE create-browseb2:
DEF VAR from-date AS DATE       NO-UNDO.
DEF VAR to-date   AS DATE       NO-UNDO.
DEF VAR i         AS INTEGER    NO-UNDO INITIAL 0.

    FOR EACH artprice WHERE artprice.artnr = argtnr NO-LOCK:
        from-date = DATE(INTEGER(SUBSTR(STRING(start-time), 5,2)), 
                     INTEGER(SUBSTR(STRING(start-time), 7, 2)),
                     INTEGER(SUBSTR(STRING(start-time), 1,4))).
        to-date = DATE(INTEGER(SUBSTR(STRING(end-time), 5,2)), 
                     INTEGER(SUBSTR(STRING(end-time), 7, 2)),
                     INTEGER(SUBSTR(STRING(end-time), 1,4))).
        IF from-date LE ankunft AND to-date GE abreise THEN
        DO:
            DO i = 2 TO (NUM-ENTRIES(artprice.bezeich, ";") - 1):
                CREATE adhoc.
                ASSIGN
                    adhoc.acode = ENTRY(1, artprice.bezeich, ";")
                    adhoc.artnr = INTEGER(ENTRY(2, ENTRY(i, artprice.bezeich, ";"), ","))
                    adhoc.deptnr = INTEGER(ENTRY(1, ENTRY(i, artprice.bezeich, ";"), ","))
                    adhoc.amount = INTEGER(ENTRY(3, ENTRY(i, artprice.bezeich, ";"), ",")) / 100
                    adhoc.child1 = INTEGER(ENTRY(4, ENTRY(i, artprice.bezeich, ";"), ",")) / 100
                    adhoc.child2 = INTEGER(ENTRY(5, ENTRY(i, artprice.bezeich, ";"), ",")) / 100
                    adhoc.post-type = INTEGER(ENTRY(6, ENTRY(i, artprice.bezeich, ";"), ",")) .
                FIND FIRST artikel WHERE artikel.artnr = adhoc.artnr
                    AND artikel.departement = adhoc.deptnr NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                    adhoc.bezeich = artikel.bezeich.
            END.
        END.
    END.
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
        argt-list.vt-percnt   = /*argt-line.vt-percnt*/ INT(reslin-queasy.char2)
        argt-list.s-recid     = INTEGER(RECID(reslin-queasy))
        argt-list.post-type   = post-type[argt-line.fakt-modus].
        IF reslin-queasy.deci1 NE 0 THEN
        argt-list.pers-type   = "Adult".
        ELSE IF reslin-queasy.deci1 eq 0 AND reslin-queasy.deci2 NE 0 AND reslin-queasy.deci3 NE 0 THEN
        argt-list.pers-type   = "Child".
        ELSE IF reslin-queasy.deci1 eq 0 AND reslin-queasy.deci2 EQ 0 AND reslin-queasy.deci3 NE 0 THEN
        argt-list.pers-type   = "Child2".
  END.
END. 
