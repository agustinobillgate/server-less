
DEFINE TEMP-TABLE ta-nat-stat
    FIELD nr            AS INTEGER
    FIELD ta-name       AS CHARACTER FORMAT "x(36)"
    FIELD nation        AS CHARACTER FORMAT "x(3)"
    FIELD rmnite        AS CHARACTER FORMAT "x(5)"
    FIELD logiumz       AS CHARACTER FORMAT "x(15)"
    FIELD argtumz       AS CHARACTER FORMAT "x(15)"
    FIELD ytd-rmnite    AS CHARACTER FORMAT "x(7)"
    FIELD ytd-logi      AS CHARACTER FORMAT "x(18)"
    FIELD ytd-argt      AS CHARACTER FORMAT "x(18)"
    .

DEFINE TEMP-TABLE tmp-list
    FIELD gastnr    AS INTEGER
    FIELD ta-name   AS CHAR 
    FIELD nation    AS CHAR
    FIELD rmnite    AS INTEGER
    FIELD argtumz   AS DECIMAL
    FIELD logiumz   AS DECIMAL

    FIELD ytd-rmnite AS INTEGER
    FIELD ytd-argt   AS DECIMAL
    FIELD ytd-logi   AS DECIMAL
    INDEX gastnr_ix gastnr
    INDEX nation_ix nation
.

DEFINE INPUT PARAMETER from-date AS CHAR.
DEFINE INPUT PARAMETER last-period AS CHAR.
DEFINE INPUT PARAMETER sorttype AS INT.
DEFINE INPUT PARAMETER text2 AS CHAR.
DEFINE INPUT PARAMETER text3 AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR ta-nat-stat.
/*
DEFINE variable from-date AS CHAR INIT "012019".
DEFINE variable last-period AS CHAR INIT "".
DEFINE variable sorttype AS INT INIT 1.
DEFINE variable text2 AS CHAR INIT "S u b t o t a l".
DEFINE variable text3 AS CHAR INIT "G R A N D  T O T A L".
*/
DEFINE VARIABLE sub-mrm         AS INTEGER NO-UNDO.
DEFINE VARIABLE sub-mlod        AS DECIMAL NO-UNDO.
DEFINE VARIABLE sub-margt       AS DECIMAL NO-UNDO.
DEFINE VARIABLE sub-yrm         AS INTEGER NO-UNDO.
DEFINE VARIABLE sub-ylod        AS DECIMAL NO-UNDO.
DEFINE VARIABLE sub-yargt       AS DECIMAL NO-UNDO.

DEFINE VARIABLE grand-mrm       AS INTEGER NO-UNDO.
DEFINE VARIABLE grand-mlod      AS DECIMAL NO-UNDO.
DEFINE VARIABLE grand-margt     AS DECIMAL NO-UNDO.
DEFINE VARIABLE grand-yrm       AS INTEGER NO-UNDO.
DEFINE VARIABLE grand-ylod      AS DECIMAL NO-UNDO.
DEFINE VARIABLE grand-yargt     AS DECIMAL NO-UNDO.

IF from-date NE last-period THEN RUN create-list.
IF sorttype = 1 THEN RUN create-browse.
ELSE RUN create-browse1.

PROCEDURE create-list:
DEFINE VARIABLE argt-ums AS DECIMAL NO-UNDO.
DEFINE VARIABLE nat AS CHAR NO-UNDO.
DEFINE VARIABLE yr AS INTEGER NO-UNDO.
DEFINE VARIABLE mm AS INTEGER NO-UNDO.
DEFINE VARIABLE status-vat AS LOGICAL NO-UNDO.

DEFINE VARIABLE vat     AS DECIMAL NO-UNDO.
DEFINE VARIABLE service AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat2    AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact    AS DECIMAL NO-UNDO.

    mm = INTEGER(STRING(SUBSTR(from-date, 1, 2), "99")).
    yr = INTEGER(STRING(SUBSTR(from-date, 3, 4), "9999")).

    FOR EACH tmp-list:
        DELETE tmp-list.
    END.

    FOR EACH genstat WHERE YEAR(genstat.datum) = yr AND MONTH(genstat.datum) LE mm
        AND genstat.zinr NE "" AND genstat.karteityp = 2 
        AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ 
        USE-INDEX DATE_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr 
            USE-INDEX gastnr_index NO-LOCK:
        
        FIND FIRST nation WHERE nation.kurzbez = guest.land USE-INDEX
            nationnr_ix NO-LOCK NO-ERROR.

        IF AVAILABLE nation THEN
            nat = nation.kurzbez.
        ELSE nat = "***".
         
        FIND FIRST tmp-list WHERE tmp-list.gastnr = genstat.gastnr AND
            tmp-list.nation = nat NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tmp-list THEN
        DO:
            CREATE tmp-list.
            ASSIGN
                tmp-list.gastnr  = genstat.gastnr
                tmp-list.ta-name = guest.NAME + ", " + guest.anredefirma
                tmp-list.nation  = guest.land.
            
        END.

        service = 0. 
        vat = 0. 
        FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK.
        status-vat = htparam.flogical. /* VAT includes in article price */
        FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt
            NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN
        FIND FIRST artikel WHERE artikel.artnr = arrangement.artnr-logis
            AND artikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel AND status-vat = YES THEN 
/*
           RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
           artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
*/
        /* SY AUG 13 2017 */
        DO:
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            genstat.datum, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.
        END.
       
        IF genstat.resstatus NE 13 THEN
            tmp-list.ytd-rmnite = tmp-list.ytd-rmnite + 1.
        tmp-list.ytd-logi = tmp-list.ytd-logi + genstat.logis.
        /* tmp-list.ytd-argt = tmp-list.argt + (genstat.ratelocal / (1 + vat + service)). */        /* Rulita 111124 | Fixing for serverless */
        tmp-list.ytd-argt = tmp-list.argtumz + (genstat.ratelocal / (1 + vat + service)).

        IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yr THEN
        DO:
             IF genstat.resstatus NE 13 THEN
                tmp-list.rmnite = tmp-list.rmnite + 1.
            tmp-list.logiumz = tmp-list.logiumz + genstat.logis.
            tmp-list.argtumz = tmp-list.argtumz + (genstat.ratelocal / (1 + vat + service)).
        END.                                                      
    END.

    /*FOR EACH guestat WHERE guestat.monat LE mm AND guestat.jahr = yr 
        NO-LOCK, FIRST guest WHERE guest.gastnr = guestat.gastnr
        AND guest.karteityp = 2 USE-INDEX typenam_ix NO-LOCK:

        FIND FIRST nation WHERE nation.nationnr = guestat.betriebsnr
            USE-INDEX nationnr_ix NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
            nat = nation.kurzbez.
        ELSE nat = "***".

        FIND FIRST tmp-list WHERE tmp-list.gastnr = guestat.gastnr AND
            tmp-list.nation = nat NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tmp-list THEN
        DO:
            CREATE tmp-list.
            ASSIGN
                tmp-list.gastnr  = guestat.gastnr
                tmp-list.ta-name = guest.NAME + ", " + guest.anredefirma
                tmp-list.nation  = nat.
        END.

        tmp-list.ytd-rmnite = tmp-list.ytd-rmnite + guestat.room-nights.
        tmp-list.ytd-argt   = tmp-list.ytd-argt + guestat.argtumsatz.
        tmp-list.ytd-logi   = tmp-list.ytd-logi + guestat.logisumsatz.

        IF guestat.monat = mm THEN
        DO:
            ASSIGN
                tmp-list.rmnite   = tmp-list.rmnite + guestat.room-nights
                tmp-list.argtumz  = tmp-list.argtumz + guestat.argtumsatz
                tmp-list.logiumz  = tmp-list.logiumz + guestat.logisumsatz.
        END.
    END.*/
END.

PROCEDURE create-browse:
    DEF VAR i           AS INTEGER INITIAL 0 NO-UNDO.
    DEF VAR curr-gastnr AS INTEGER INITIAL 0 NO-UNDO.
    DEF VAR it-exists   AS LOGICAL INITIAL NO NO-UNDO.
    DEF VAR s           AS CHAR    INITIAL "" NO-UNDO.

    FOR EACH ta-nat-stat:
        DELETE ta-nat-stat.
    END.

    ASSIGN
        sub-mrm     = 0
        sub-mlod    = 0
        sub-margt   = 0
        sub-yrm     = 0
        sub-ylod    = 0
        sub-yargt   = 0
        grand-mrm   = 0
        grand-mlod  = 0
        grand-margt = 0
        grand-yrm   = 0
        grand-ylod  = 0
        grand-yargt = 0
        .

    FOR EACH tmp-list NO-LOCK BY tmp-list.gastnr:
        IF curr-gastnr NE 0 AND curr-gastnr NE tmp-list.gastnr THEN
        DO:
            i = i + 1.
            CREATE ta-nat-stat.
            ASSIGN ta-nat-stat.nr = i.

            i = i + 1.
            CREATE ta-nat-stat.
            ASSIGN    
                ta-nat-stat.nr         = i
                ta-nat-stat.ta-name    = text2    
                ta-nat-stat.rmnite     = STRING(sub-mrm, ">,>>9")               
                ta-nat-stat.logiumz    = STRING(sub-mlod, "->>>,>>>,>>9.99")    
                ta-nat-stat.argtumz    = STRING(sub-margt, "->>>,>>>,>>9.99")   
                ta-nat-stat.ytd-rmnite = STRING(sub-yrm, ">>>,>>9")             
                ta-nat-stat.ytd-logi   = STRING(sub-ylod, "->>,>>>,>>>,>>9.99") 
                ta-nat-stat.ytd-argt   = STRING(sub-yargt, "->>,>>>,>>>,>>9.99")
            .          

            i = i + 1.
            CREATE ta-nat-stat.       
            ASSIGN ta-nat-stat.nr = i.

            ASSIGN
                sub-mrm     = 0
                sub-mlod    = 0
                sub-margt   = 0
                sub-yrm     = 0
                sub-ylod    = 0
                sub-yargt   = 0
                .
        END.

        i = i + 1.
        CREATE ta-nat-stat.
        ASSIGN
            ta-nat-stat.nr         = i
            ta-nat-stat.ta-name    = STRING(tmp-list.ta-name, "x(36)")              
            ta-nat-stat.nation     = STRING(tmp-list.nation, "x(3)")                
            ta-nat-stat.rmnite     = STRING(tmp-list.rmnite, ">,>>9")               
            ta-nat-stat.logiumz    = STRING(tmp-list.logiumz, "->>>,>>>,>>9.99")    
            ta-nat-stat.argtumz    = STRING(tmp-list.argtumz, "->>>,>>>,>>9.99")    
            ta-nat-stat.ytd-rmnite = STRING(tmp-list.ytd-rmnite, ">>>,>>9")         
            ta-nat-stat.ytd-logi   = STRING(tmp-list.ytd-logi, "->>,>>>,>>>,>>9.99")
            ta-nat-stat.ytd-argt   = STRING(tmp-list.ytd-argt, "->>,>>>,>>>,>>9.99")
        .       

        ASSIGN
            sub-mrm     = sub-mrm     + tmp-list.rmnite
            sub-mlod    = sub-mlod    + tmp-list.logiumz
            sub-margt   = sub-margt   + tmp-list.argtumz
            sub-yrm     = sub-yrm     + tmp-list.ytd-rmnite
            sub-ylod    = sub-ylod    + tmp-list.ytd-logi
            sub-yargt   = sub-yargt   + tmp-list.ytd-argt
            grand-mrm   = grand-mrm   + tmp-list.rmnite
            grand-mlod  = grand-mlod  + tmp-list.logiumz
            grand-margt = grand-margt + tmp-list.argtumz
            grand-yrm   = grand-yrm   + tmp-list.ytd-rmnite
            grand-ylod  = grand-ylod  + tmp-list.ytd-logi
            grand-yargt = grand-yargt + tmp-list.ytd-argt
            it-exists = YES
            curr-gastnr = tmp-list.gastnr.
        .                             
    END.

    IF it-exists THEN
    DO:
        i = i + 1.
        CREATE ta-nat-stat.       
        ASSIGN ta-nat-stat.nr = i.

        i = i + 1.
        CREATE ta-nat-stat.                                                 
        ASSIGN                                                              
            ta-nat-stat.nr         = i                                      
            ta-nat-stat.ta-name    = text2                                  
            ta-nat-stat.rmnite     = STRING(sub-mrm, ">,>>9")               
            ta-nat-stat.logiumz    = STRING(sub-mlod, "->>>,>>>,>>9.99")    
            ta-nat-stat.argtumz    = STRING(sub-margt, "->>>,>>>,>>9.99")   
            ta-nat-stat.ytd-rmnite = STRING(sub-yrm, ">>>,>>9")             
            ta-nat-stat.ytd-logi   = STRING(sub-ylod, "->>,>>>,>>>,>>9.99") 
            ta-nat-stat.ytd-argt   = STRING(sub-yargt, "->>,>>>,>>>,>>9.99")
        .                                                                           
        
        i = i + 1.
        CREATE ta-nat-stat.        
        ASSIGN ta-nat-stat.nr = i. 

        i = i + 1.
        CREATE ta-nat-stat.                                                 
        ASSIGN
            ta-nat-stat.nr         = i
            ta-nat-stat.ta-name    = text3
            ta-nat-stat.rmnite     = STRING(grand-mrm, ">,>>9")               
            ta-nat-stat.logiumz    = STRING(grand-mlod, "->>>,>>>,>>9.99")    
            ta-nat-stat.argtumz    = STRING(grand-margt, "->>>,>>>,>>9.99")   
            ta-nat-stat.ytd-rmnite = STRING(grand-yrm, ">>>,>>9")             
            ta-nat-stat.ytd-logi   = STRING(grand-ylod, "->>,>>>,>>>,>>9.99") 
            ta-nat-stat.ytd-argt   = STRING(grand-yargt, "->>,>>>,>>>,>>9.99")
        .       
    END.
END.

PROCEDURE create-browse1:
    DEF VAR s AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR i AS INTEGER INITIAL 0 NO-UNDO.
    DEF VAR curr-nat    AS CHAR INITIAL "" NO-UNDO.
    DEF VAR it-exists   AS LOGICAL INITIAL NO NO-UNDO.

    FOR EACH ta-nat-stat:
        DELETE ta-nat-stat.
    END.

    ASSIGN
        sub-mrm     = 0
        sub-mlod    = 0
        sub-margt   = 0
        sub-yrm     = 0
        sub-ylod    = 0
        sub-yargt   = 0
        grand-mrm   = 0
        grand-mlod  = 0
        grand-margt = 0
        grand-yrm   = 0
        grand-ylod  = 0
        grand-yargt = 0
        .

    FOR EACH tmp-list NO-LOCK BY tmp-list.nation:
        IF curr-nat NE ""  AND curr-nat NE tmp-list.nation THEN
        DO:
            i = i + 1.
            CREATE ta-nat-stat.       
            ASSIGN ta-nat-stat.nr = i.

            i = i + 1.
            CREATE ta-nat-stat.
            ASSIGN    
                ta-nat-stat.nr         = i
                ta-nat-stat.ta-name    = text2    
                ta-nat-stat.rmnite     = STRING(sub-mrm, ">,>>9")               
                ta-nat-stat.logiumz    = STRING(sub-mlod, "->>>,>>>,>>9.99")    
                ta-nat-stat.argtumz    = STRING(sub-margt, "->>>,>>>,>>9.99")   
                ta-nat-stat.ytd-rmnite = STRING(sub-yrm, ">>>,>>9")             
                ta-nat-stat.ytd-logi   = STRING(sub-ylod, "->>,>>>,>>>,>>9.99") 
                ta-nat-stat.ytd-argt   = STRING(sub-yargt, "->>,>>>,>>>,>>9.99")
            . 
                                                                                
            i = i + 1.
            CREATE ta-nat-stat.       
            ASSIGN ta-nat-stat.nr = i.

            ASSIGN
                sub-mrm     = 0
                sub-mlod    = 0
                sub-margt   = 0
                sub-yrm     = 0
                sub-ylod    = 0
                sub-yargt   = 0
                .
        END.

        i = i + 1.
        CREATE ta-nat-stat.                                                          
        ASSIGN                                                                       
            ta-nat-stat.nr         = i                                               
            ta-nat-stat.ta-name    = STRING(tmp-list.ta-name, "x(36)")               
            ta-nat-stat.nation     = STRING(tmp-list.nation, "x(3)")                 
            ta-nat-stat.rmnite     = STRING(tmp-list.rmnite, ">,>>9")                
            ta-nat-stat.logiumz    = STRING(tmp-list.logiumz, "->>>,>>>,>>9.99")     
            ta-nat-stat.argtumz    = STRING(tmp-list.argtumz, "->>>,>>>,>>9.99")     
            ta-nat-stat.ytd-rmnite = STRING(tmp-list.ytd-rmnite, ">>>,>>9")          
            ta-nat-stat.ytd-logi   = STRING(tmp-list.ytd-logi, "->>,>>>,>>>,>>9.99") 
            ta-nat-stat.ytd-argt   = STRING(tmp-list.ytd-argt, "->>,>>>,>>>,>>9.99") 
        .                                                                                    
        
        ASSIGN
            sub-mrm     = sub-mrm     + tmp-list.rmnite
            sub-mlod    = sub-mlod    + tmp-list.logiumz
            sub-margt   = sub-margt   + tmp-list.argtumz
            sub-yrm     = sub-yrm     + tmp-list.ytd-rmnite
            sub-ylod    = sub-ylod    + tmp-list.ytd-logi
            sub-yargt   = sub-yargt   + tmp-list.ytd-argt
            grand-mrm   = grand-mrm   + tmp-list.rmnite
            grand-mlod  = grand-mlod  + tmp-list.logiumz
            grand-margt = grand-margt + tmp-list.argtumz
            grand-yrm   = grand-yrm   + tmp-list.ytd-rmnite
            grand-ylod  = grand-ylod  + tmp-list.ytd-logi
            grand-yargt = grand-yargt + tmp-list.ytd-argt
            it-exists = YES
            curr-nat = tmp-list.nation.
            .                             
    END.

    IF it-exists THEN
    DO:
        i = i + 1.
        CREATE ta-nat-stat.        
        ASSIGN ta-nat-stat.nr = i. 

        i = i + 1.
        CREATE ta-nat-stat.        
        ASSIGN
            ta-nat-stat.nr         = i                                      
            ta-nat-stat.ta-name    = text2                                  
            ta-nat-stat.rmnite     = STRING(sub-mrm, ">,>>9")               
            ta-nat-stat.logiumz    = STRING(sub-mlod, "->>>,>>>,>>9.99")    
            ta-nat-stat.argtumz    = STRING(sub-margt, "->>>,>>>,>>9.99")   
            ta-nat-stat.ytd-rmnite = STRING(sub-yrm, ">>>,>>9")             
            ta-nat-stat.ytd-logi   = STRING(sub-ylod, "->>,>>>,>>>,>>9.99") 
            ta-nat-stat.ytd-argt   = STRING(sub-yargt, "->>,>>>,>>>,>>9.99")
        .
        
        i = i + 1.
        CREATE ta-nat-stat.       
        ASSIGN ta-nat-stat.nr = i.

        i = i + 1.
        CREATE ta-nat-stat.                                                 
        ASSIGN
            ta-nat-stat.nr         = i
            ta-nat-stat.ta-name    = text3
            ta-nat-stat.rmnite     = STRING(grand-mrm, ">,>>9")               
            ta-nat-stat.logiumz    = STRING(grand-mlod, "->>>,>>>,>>9.99")    
            ta-nat-stat.argtumz    = STRING(grand-margt, "->>>,>>>,>>9.99")   
            ta-nat-stat.ytd-rmnite = STRING(grand-yrm, ">>>,>>9")             
            ta-nat-stat.ytd-logi   = STRING(grand-ylod, "->>,>>>,>>>,>>9.99") 
            ta-nat-stat.ytd-argt   = STRING(grand-yargt, "->>,>>>,>>>,>>9.99")
        .        
    END.
END.



