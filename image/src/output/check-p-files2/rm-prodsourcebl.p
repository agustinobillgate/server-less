
DEFINE TEMP-TABLE output-list
    FIELD gname AS CHAR 
    FIELD flag  AS LOGICAL INITIAL NO
    FIELD NAME AS CHARACTER
    FIELD dlodge AS DECIMAL
    FIELD mlodge AS DECIMAL
    FIELD ylodge AS DECIMAL
    FIELD dnite AS INTEGER
    FIELD mnite AS INTEGER
    FIELD ynite AS INTEGER
    FIELD drate AS DECIMAL
    FIELD mrate AS DECIMAL
    FIELD yrate AS DECIMAL.

DEF TEMP-TABLE t-list
    FIELD natnr     AS INTEGER
    FIELD nat       AS CHAR FORMAT "x(24)"
    FIELD counts    AS INTEGER
    FIELD tot-nat   AS INTEGER
    FIELD flag      AS LOGICAL INITIAL NO
    FIELD gastnr    AS INTEGER
    FIELD NAME      AS CHAR FORMAT "x(24)"
    FIELD gname     AS CHAR FORMAT "x(32)"
    FIELD dlodge    AS DECIMAL 
    FIELD mlodge    AS DECIMAL 
    FIELD ylodge    AS DECIMAL 
    FIELD dnite     AS INTEGER 
    FIELD mnite     AS INTEGER 
    FIELD ynite     AS INTEGER 
    FIELD drate     AS DECIMAL 
    FIELD mrate     AS DECIMAL 
    FIELD yrate     AS DECIMAL 
    .
DEF INPUT PARAMETER source-name AS CHAR.
DEF INPUT  PARAMETER ytd-flag   AS LOGICAL.
DEF INPUT  PARAMETER incl-comp  AS LOGICAL.
DEF INPUT  PARAMETER fr-date    AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER flag       AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEF VAR tot-dlodge AS DECIMAL. 
DEF VAR tot-mlodge AS DECIMAL. 
DEF VAR tot-ylodge AS DECIMAL. 
DEF VAR tot-dnite  AS INTEGER. 
DEF VAR tot-mnite  AS INTEGER. 
DEF VAR tot-ynite  AS INTEGER. 
DEF VAR tot-drate  AS DECIMAL. 
DEF VAR tot-mrate  AS DECIMAL. 
DEF VAR tot-yrate  AS DECIMAL. 


DEF VAR tot1-dlodge AS DECIMAL. 
DEF VAR tot1-mlodge AS DECIMAL. 
DEF VAR tot1-ylodge AS DECIMAL. 
DEF VAR tot1-dnite  AS INTEGER. 
DEF VAR tot1-mnite  AS INTEGER. 
DEF VAR tot1-ynite  AS INTEGER. 
DEF VAR tot1-drate  AS DECIMAL. 
DEF VAR tot1-mrate  AS DECIMAL. 
DEF VAR tot1-yrate  AS DECIMAL. 

FIND FIRST sourccod WHERE sourccod.bezeich = source-name
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE sourccod THEN
FIND FIRST sourccod WHERE SUBSTR(sourccod.bezeich, 1, LENGTH(source-name))
    = source-name NO-LOCK NO-ERROR.
IF NOT AVAILABLE sourccod THEN
DO:
  flag = 1.
  RETURN.
END.

IF ytd-flag THEN RUN create-list1.
ELSE RUN create-list2.


PROCEDURE create-list1:

DEF VAR b AS INTEGER NO-UNDO.
DEF VAR curr-nat AS INTEGER INITIAL 0.
DEF VAR do-it AS LOGICAL INITIAL YES.
DEF BUFFER gbuff FOR guest.
    
    FOR EACH genstat NO-LOCK WHERE genstat.datum GE fr-date 
        AND genstat.datum LE to-date       
        AND genstat.SOURCE EQ sourccod.source-code
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0
        AND genstat.nationnr NE 0
        AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */ 
        /*AND genstat.res-int[1] NE 13*/
        /*AND
        (genstat.erwachs + genstat.kind1) GT 0*/ :
         do-it = YES.
        
        IF NOT incl-comp THEN
        DO:
            IF (genstat.erwachs + genstat.kind1) GT 0 THEN
                do-it = YES.
            ELSE do-it = NO.
        END.

        IF do-it THEN
        DO:
            FIND FIRST t-list WHERE t-list.gastnr = genstat.gastnr 
                AND t-list.natnr = genstat.SOURCE   NO-LOCK NO-ERROR.
    
            IF NOT AVAIL t-list THEN
            DO:
                FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN DO: 
                        CREATE t-list.
                        ASSIGN 
                           t-list.gastnr = genstat.gastnr
                           t-list.name   = guest.NAME + ", " + guest.vorname1 + ", " 
                                         + guest.anrede1 + guest.anredefirma
                           t-list.gname  = gbuff.NAME + ", " + gbuff.vorname1 + ", " 
                                         + gbuff.anrede1 + gbuff.anredefirma
                           t-list.nat    =  sourccod.bezeich
                           t-list.natnr  = genstat.SOURCE
                        .
                    END.
                END.
            END.                   

            IF AVAILABLE t-list THEN
            DO:
                IF genstat.datum = to-date THEN
                DO:
                  ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis.
                  /*IF genstat.res-int[1] NE 13 THEN */
                  ASSIGN t-list.dnite  = t-list.dnite  + 1 .
                END.

                IF MONTH(genstat.datum) = MONTH(to-date) THEN
                DO:
                  ASSIGN t-list.mlodge = t-list.mlodge + genstat.logis.
                    /*IF genstat.res-int[1] NE 13 THEN */
                       ASSIGN t-list.mnite  = t-list.mnite  + 1.
                END.

                DO:
                  ASSIGN t-list.ylodge = t-list.ylodge + genstat.logis.
                     /*IF genstat.res-int[1] NE 13 THEN */
                        ASSIGN t-list.ynite  = t-list.ynite  + 1.      
                END.
            END.
        END.
    END. /*each genstat*/

    FOR EACH t-list:
      IF t-list.dnite NE 0 THEN ASSIGN t-list.drate = t-list.dlodge / t-list.dnite.
      IF t-list.mnite NE 0 THEN ASSIGN t-list.mrate = t-list.mlodge / t-list.mnite.
      IF t-list.ynite NE 0 THEN ASSIGN t-list.yrate = t-list.ylodge / t-list.ynite.
      
    END.

    RUN count-sub.

    CREATE output-list.
    ASSIGN 
        output-list.NAME = "--------------------------------------------------------------"
        output-list.gNAME = "------------------------>".

     CREATE output-list.
     ASSIGN   
         output-list.NAME   = "Total"
         output-list.dlodge = tot-dlodge
         output-list.mlodge = tot-mlodge
         output-list.ylodge = tot-ylodge
         output-list.dnite  = tot-dnite
         output-list.mnite  = tot-mnite
         output-list.ynite  = tot-ynite
         output-list.drate  = tot-drate
         output-list.mrate  = tot-mrate
         output-list.yrate  = tot-yrate.
   
END.

PROCEDURE create-list2:

DEF VAR b AS INTEGER NO-UNDO.
DEF VAR curr-nat AS INTEGER INITIAL 0.
DEF VAR do-it AS LOGICAL INITIAL YES.
DEF BUFFER gbuff FOR guest.
    
    FOR EACH genstat NO-LOCK WHERE genstat.datum GE fr-date 
        AND genstat.datum LE to-date       
        AND genstat.SOURCE EQ sourccod.source-code
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0
        AND genstat.nationnr NE 0
        AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */ 
        /*AND genstat.res-int[1] NE 13*/
        /*AND
        (genstat.erwachs + genstat.kind1) GT 0*/ :
         do-it = YES.
        
        IF NOT incl-comp THEN
        DO:
            IF (genstat.erwachs + genstat.kind1) GT 0 THEN
                do-it = YES.
            ELSE do-it = NO.
        END.

        IF do-it THEN
        DO:
            FIND FIRST t-list WHERE t-list.gastnr = genstat.gastnr 
                AND t-list.natnr = genstat.SOURCE   NO-LOCK NO-ERROR.
    
            IF NOT AVAIL t-list THEN
            DO:
                FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN DO: 
                        CREATE t-list.
                        ASSIGN 
                           t-list.gastnr = genstat.gastnr
                           t-list.name   = guest.NAME + ", " + guest.vorname1 + ", " 
                                         + guest.anrede1 + guest.anredefirma
                           t-list.gname  = gbuff.NAME + ", " + gbuff.vorname1 + ", " 
                                         + gbuff.anrede1 + gbuff.anredefirma
                           t-list.nat    =  sourccod.bezeich
                           t-list.natnr  = genstat.SOURCE
                        .
                    END.
                END.
            END.                   

            IF AVAILABLE t-list THEN
            DO:
                IF genstat.datum = to-date THEN
                DO:
                  ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis.
                  /*IF genstat.res-int[1] NE 13 THEN */
                  ASSIGN t-list.dnite  = t-list.dnite  + 1 .
                END.

                DO:
                  ASSIGN t-list.mlodge = t-list.mlodge + genstat.logis.
                    /*IF genstat.res-int[1] NE 13 THEN */
                       ASSIGN t-list.mnite  = t-list.mnite  + 1.
                END.

                DO:
                  ASSIGN t-list.ylodge = t-list.ylodge + genstat.logis.
                     /*IF genstat.res-int[1] NE 13 THEN */
                        ASSIGN t-list.ynite  = t-list.ynite  + 1.      
                END.
            END.
        END.
    END. /*each genstat*/

    FOR EACH t-list:
      IF t-list.dnite NE 0 THEN ASSIGN t-list.drate = t-list.dlodge / t-list.dnite.
      IF t-list.mnite NE 0 THEN ASSIGN t-list.mrate = t-list.mlodge / t-list.mnite.
      IF t-list.ynite NE 0 THEN ASSIGN t-list.yrate = t-list.ylodge / t-list.ynite.
      
    END.

    RUN count-sub.

    CREATE output-list.
    ASSIGN 
        output-list.NAME = "--------------------------------------------------------------"
        output-list.gNAME = "------------------------>".

     CREATE output-list.
     ASSIGN
         output-list.NAME   = "Total"
         output-list.dlodge = tot-dlodge
         output-list.mlodge = tot-mlodge
         output-list.ylodge = tot-ylodge
         output-list.dnite  = tot-dnite
         output-list.mnite  = tot-mnite
         output-list.ynite  = tot-ynite
         output-list.drate  = tot-drate
         output-list.mrate  = tot-mrate
         output-list.yrate  = tot-yrate.
END.

PROCEDURE count-sub:
    DEF VAR curr-nat AS INTEGER NO-UNDO INIT 0.
   
    FOR EACH t-list NO-LOCK BY t-list.natnr:
        CREATE output-list.
        ASSIGN 
            output-list.gname  = t-list.gname
            output-list.NAME   = t-list.name
            output-list.dlodge = t-list.dlodge
            output-list.mlodge = t-list.mlodge
            output-list.ylodge = t-list.ylodge
            output-list.dnite  = t-list.dnite
            output-list.mnite  = t-list.mnite
            output-list.ynite  = t-list.ynite
            output-list.drate  = t-list.drate
            output-list.mrate  = t-list.mrate
            output-list.yrate  = t-list.yrate.
           
        ASSIGN
            tot-dlodge    = tot-dlodge    + t-list.dlodge
            tot-dnite     = tot-dnite     + t-list.dnite
            tot-mlodge    = tot-mlodge    + t-list.mlodge
            tot-ylodge    = tot-ylodge    + t-list.ylodge
            tot-mnite     = tot-mnite     + t-list.mnite
            tot-ynite     = tot-ynite     + t-list.ynite
            tot-drate     = tot-drate     + t-list.drate
            tot-mrate     = tot-mrate     + t-list.mrate
            tot-yrate     = tot-yrate     + t-list.yrate
        .
        
    END.

    IF tot-dnite NE 0 THEN ASSIGN tot-drate = tot-dlodge / tot-dnite.
    IF tot-mnite NE 0 THEN ASSIGN tot-mrate = tot-mlodge / tot-mnite.
    IF tot-ynite NE 0 THEN ASSIGN tot-yrate = tot-ylodge / tot-ynite.
END.
