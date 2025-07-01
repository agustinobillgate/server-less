DEFINE TEMP-TABLE t-list 
  FIELD flag       AS INTEGER 
  FIELD bezeich    AS CHAR    FORMAT "x(24)"
  FIELD anz        AS INTEGER FORMAT ">>9" 
  FIELD pax        AS INTEGER FORMAT ">>9"
  FIELD net        AS DECIMAL FORMAT "->>>,>>>,>>9.99"
  FIELD proz       AS DECIMAL FORMAT "->>9.99"
  FIELD manz       AS INTEGER FORMAT ">>,>>9" 
  FIELD mpax       AS INTEGER FORMAT ">>,>>9" 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD yanz       AS INTEGER FORMAT ">>>,>>9" 
  FIELD ypax       AS INTEGER FORMAT ">>>,>>9" 
  FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEF INPUT PARAMETER pvILanguage AS INTEGER              NO-UNDO.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER rmNo        AS CHAR.

DEF OUTPUT PARAMETER msg-str    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-list.


{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "rm-rev1". 


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
DEF VAR tot-dpax   AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR tot-mpax   AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR tot-ypax   AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR fdate      AS DATE              NO-UNDO.

DEFINE BUFFER t-genstat FOR genstat.

ASSIGN fdate = DATE(1,1, YEAR(to-date)).

    FOR EACH genstat WHERE genstat.datum GE from-date 
      AND genstat.datum LE to-date 
      AND genstat.zinr = rmNo 
      AND genstat.res-logic[2] EQ YES USE-INDEX date_ix NO-LOCK:
        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN
        DO:
            IF segment.betriebsnr EQ 2 /*OR (genstat.zipreis = 0 AND
                (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
                + genstat.kind2 + genstat.gratis = 0)))*/ THEN /*house use*/
            DO:
                FIND FIRST t-list WHERE t-list.flag = 3 NO-ERROR.
                IF NOT AVAILABLE t-list THEN
                DO:
                    CREATE t-list.
                    ASSIGN
                        t-list.flag = 3
                        t-list.bezeich = translateExtended("House Use",lvCAREA, "").
                END.
            END.    
            ELSE IF segment.betriebsnr = 1 OR (genstat.zipreis = 0 AND
                (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
                + genstat.kind2 + genstat.gratis = 0))) THEN
            DO:
                FIND FIRST t-list WHERE t-list.flag = 2 NO-ERROR.
                IF NOT AVAILABLE t-list THEN
                DO:
                    CREATE t-list.
                    ASSIGN
                        t-list.flag = 2
                        t-list.bezeich = translateExtended("Compliment",lvCAREA, "").
                END.
            END.
            ELSE
            DO:
                FIND FIRST t-list WHERE t-list.flag = 1 NO-ERROR.
                IF NOT AVAIL t-list THEN
                DO:
                    CREATE t-list.
                    ASSIGN t-list.flag   = 1
                           t-list.bezeich = translateExtended("Paying", lvCAREA, "")
                    .
                END.  
            END.
        END.
        ELSE
        DO:
            msg-str = msg-str + CHR(2) + "&W"
                    + translateExtended("Unable to find segmentcode ", lvCAREA, "")
                    + STRING(genstat.segmentcode).
            IF (genstat.zipreis = 0 AND
                (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
                + genstat.kind2 + genstat.gratis = 0))) THEN
            DO:
                FIND FIRST t-list WHERE t-list.flag = 2 NO-ERROR.
                IF NOT AVAILABLE t-list THEN
                DO:
                    CREATE t-list.
                    ASSIGN
                        t-list.flag = 2
                        t-list.bezeich = translateExtended("Compliment",lvCAREA, "").
                END.
            END.
            ELSE
            DO: 
                FIND FIRST t-list WHERE t-list.flag = 1 NO-ERROR.
                IF NOT AVAIL t-list THEN
                DO:
                    CREATE t-list.
                    ASSIGN t-list.flag   = 1
                           t-list.bezeich = translateExtended("Paying", lvCAREA, "")
                    .
                END.  
            END.
        END.
        
        IF genstat.datum = to-date THEN
        DO:
            ASSIGN
                t-list.anz     = t-list.anz  + 1
                t-list.pax     = t-list.pax  + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3
                t-list.net     = t-list.net  + genstat.logis
                tot-dnite      = tot-dnite   + 1
                tot-dlodge     = tot-dlodge  + genstat.logis
                tot-dpax       = tot-dpax    + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3.
        END.
        IF MONTH(genstat.datum) = MONTH(to-date) AND YEAR(genstat.datum) = 
            YEAR(to-date) THEN
        DO:
           ASSIGN
                t-list.manz     = t-list.manz  + 1
                t-list.mpax     = t-list.mpax  + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3
                t-list.mnet     = t-list.mnet  + genstat.logis
                tot-mnite       = tot-mnite    + 1
                tot-mlodge      = tot-mlodge   + genstat.logis
                tot-mpax        = tot-mpax     + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3.
        END.
        
        DO:
            ASSIGN
                t-list.yanz     = t-list.yanz  + 1
                t-list.ypax     = t-list.ypax  + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3
                t-list.ynet     = t-list.ynet  + genstat.logis
                tot-ynite       = tot-ynite   + 1
                tot-ylodge      = tot-ylodge  + genstat.logis
                tot-ypax        = tot-ypax    + genstat.erwachs + genstat.gratis 
                                 + genstat.kind1 + genstat.kind2 + genstat.kind3.
                 
        END.
    END.
    
    /*
    FOR EACH t-genstat WHERE t-genstat.datum GE fdate 
      AND t-genstat.datum LE to-date 
      AND t-genstat.zinr = rmNo 
      AND t-genstat.res-logic[2] USE-INDEX date_ix NO-LOCK:
   
        ASSIGN
            t-list.yanz     = t-list.yanz  + 1
            t-list.ypax     = t-list.ypax  + t-genstat.erwachs + t-genstat.gratis 
                             + t-genstat.kind1 + t-genstat.kind2 + t-genstat.kind3
            t-list.ynet     = t-list.ynet  + t-genstat.logis
            tot-ynite       = tot-ynite   + 1
            tot-ylodge      = tot-ylodge  + t-genstat.logis
            tot-ypax        = tot-ypax    + t-genstat.erwachs + t-genstat.gratis 
                             + t-genstat.kind1 + t-genstat.kind2 + t-genstat.kind3.
                 
    END.*/



    FOR EACH t-list:
      IF t-list.anz NE 0 THEN ASSIGN t-list.proz = t-list.net / tot-dlodge * 100.
      IF t-list.manz NE 0 THEN ASSIGN t-list.proz1 = t-list.mnet / tot-mlodge * 100.
      IF t-list.yanz NE 0 THEN ASSIGN t-list.proz2 = t-list.ynet / tot-ylodge * 100.
    END.
    CREATE t-list.
    ASSIGN t-list.bezeich  = translateExtended ("T O T A L",lvCAREA,"")
           t-list.flag     = 4
           t-list.anz      = tot-dnite
           t-list.pax      = tot-dpax
           t-list.net      = tot-dlodge
           t-list.manz     = tot-mnite
           t-list.mpax     = tot-mpax
           t-list.mnet     = tot-mlodge
           t-list.yanz     = tot-ynite
           t-list.ypax     = tot-ypax
           t-list.ynet     = tot-ylodge
           t-list.proz     = 100
           t-list.proz1    = 100
           t-list.proz2    = 100
    .
END.
