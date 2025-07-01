
DEF TEMP-TABLE t-list
    FIELD flag      AS LOGICAL INITIAL NO
    FIELD gastnr    AS INTEGER
    FIELD gname     AS CHAR FORMAT "x(32)"
    FIELD dlodge    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD mlodge    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ylodge    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD dnite     AS INTEGER FORMAT ">>9"
    FIELD mnite     AS INTEGER FORMAT ">>,>>9"
    FIELD ynite     AS INTEGER FORMAT ">>>,>>9"
    FIELD drate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD mrate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD yrate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    .

DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER segmcode    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER jan-date    AS DATE    NO-UNDO.
DEF INPUT  PARAMETER to-date     AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE       FOR t-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rm-stat1". 

RUN create-list.

PROCEDURE create-list:
DEF VAR tot-dlodge AS DECIMAL INITIAL 0 NO-UNDO.
DEF VAR tot-mlodge AS DECIMAL INITIAL 0 NO-UNDO.
DEF VAR tot-ylodge AS DECIMAL INITIAL 0 NO-UNDO.
DEF VAR tot-dnite  AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR tot-mnite  AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR tot-ynite  AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR tot-drate  AS DECIMAL INITIAL 0 NO-UNDO.
DEF VAR tot-mrate  AS DECIMAL INITIAL 0 NO-UNDO.
DEF VAR tot-yrate  AS DECIMAL INITIAL 0 NO-UNDO.

     /*FOR EACH genstat NO-LOCK WHERE 
        genstat.datum GE jan-date      AND
        genstat.datum LE to-date       AND
        genstat.segmentcode = segmcode AND
        /*(genstat.erwachs + genstat.kind1) GT  AND0*/
        genstat.resstatus NE 13 AND
        genstat.nationnr NE 0 AND
        genstat.zinr NE "" AND
        genstat.gastnr GT 0 
        AND genstat.res-logic[2] EQ YES :*/

    /*gerald YTD rmrevenue tidak sama dengan gl Report 280121*/
    FOR EACH genstat NO-LOCK WHERE      
        genstat.datum GE jan-date      AND
        genstat.datum LE to-date       AND
        genstat.segmentcode = segmcode AND
        /*(genstat.erwachs + genstat.kind1) GT 0 AND*/
        genstat.resstatus NE 13 AND
        genstat.nationnr NE 0 AND
        genstat.zinr NE "" AND
        genstat.gastnr GT 0 
        AND genstat.res-logic[2] EQ YES :
        FIND FIRST t-list WHERE t-list.gastnr = genstat.gastnr NO-ERROR.
        IF NOT AVAIL t-list THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK
                NO-ERROR.
            CREATE t-list.
            ASSIGN t-list.gastnr = genstat.gastnr.
            IF AVAILABLE guest THEN
                   t-list.gname  = guest.NAME + ", " + guest.vorname1 + ", " 
                                 + guest.anrede1 + guest.anredefirma.
        END.  
        IF genstat.datum = to-date THEN
        DO:
          ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis
                 tot-dlodge    = tot-dlodge    + genstat.logis.
          /*ITA 071216*/
          /*IF genstat.res-int[1] NE 13 THEN 
          ASSIGN t-list.dnite  = t-list.dnite  + 1
                 tot-dnite     = tot-dnite     + 1.*/

          IF genstat.resstatus NE 13 THEN 
          ASSIGN t-list.dnite  = t-list.dnite  + 1
                 tot-dnite     = tot-dnite     + 1.
        END.
        IF MONTH(genstat.datum) = MONTH(to-date) THEN
        DO:
          ASSIGN t-list.mlodge = t-list.mlodge + genstat.logis
                 tot-mlodge    = tot-mlodge    + genstat.logis.
          /*ITA 071216*/
          /*IF genstat.res-int[1] NE 13 THEN 
          ASSIGN t-list.mnite  = t-list.mnite  + 1
                 tot-mnite     = tot-mnite     + 1.*/

          IF genstat.resstatus NE 13 THEN 
          ASSIGN t-list.mnite  = t-list.mnite  + 1
                 tot-mnite     = tot-mnite     + 1.
        END.
        DO:
          ASSIGN t-list.ylodge = t-list.ylodge + genstat.logis
                 tot-ylodge    = tot-ylodge    + genstat.logis.
          /*ITA 071216
          IF genstat.res-int[1] NE 13 THEN 
          ASSIGN t-list.ynite  = t-list.ynite  + 1
                 tot-ynite     = tot-ynite     + 1.*/

          IF genstat.resstatus NE 13 THEN 
          ASSIGN t-list.ynite  = t-list.ynite  + 1
                 tot-ynite     = tot-ynite     + 1.

        END.
    END.
    CREATE t-list.
    ASSIGN t-list.gname  = translateExtended ("T O T A L",lvCAREA,"")
           t-list.flag   = YES
           t-list.dlodge = tot-dlodge
           t-list.mlodge = tot-mlodge
           t-list.ylodge = tot-ylodge
           t-list.dnite  = tot-dnite
           t-list.mnite  = tot-mnite
           t-list.ynite  = tot-ynite
           t-list.drate  = tot-drate
           t-list.mrate  = tot-mrate
           t-list.yrate  = tot-yrate
    .
    FOR EACH t-list:
      IF t-list.dnite NE 0 THEN ASSIGN t-list.drate = t-list.dlodge / t-list.dnite.
      IF t-list.mnite NE 0 THEN ASSIGN t-list.mrate = t-list.mlodge / t-list.mnite.
      IF t-list.ynite NE 0 THEN ASSIGN t-list.yrate = t-list.ylodge / t-list.ynite.
    END.
    
END.
