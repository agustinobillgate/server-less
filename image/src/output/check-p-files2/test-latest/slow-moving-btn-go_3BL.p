DEFINE TEMP-TABLE s-list 
  FIELD artnr       AS INTEGER FORMAT "9999999"         LABEL "ArtNo" 
  FIELD name        AS CHAR    FORMAT "x(36)"           LABEL "Name" 
  FIELD min-oh      AS DECIMAL FORMAT " >>>,>>9.99"     LABEL "Min Onhand" 
  FIELD curr-oh     AS DECIMAL FORMAT "->>>,>>9.99"     LABEL "Curr Onhand" 
  FIELD avrgprice   AS DECIMAL FORMAT ">>>,>>>,>>9.99"  LABEL "Avg Price" INITIAL 0 
  FIELD ek-aktuell  AS DECIMAL FORMAT ">>>,>>>,>>9.99"  LABEL "Actual Price" INITIAL 0 
  FIELD datum       AS DATE    FORMAT "99/99/9999"      LABEL "Last Purchase"
  FIELD content     AS DECIMAL FORMAT ">>>,>>9.99"      LABEL "Content"
  FIELD zwkum       LIKE l-artikel.zwkum
  FIELD endkum      LIKE l-artikel.endkum
  FIELD unit        AS CHAR    FORMAT "x(10)"           LABEL "Unit"
  FIELD datum2      AS DATE    FORMAT "99/99/9999"      LABEL "Last Consume".

DEF INPUT  PARAMETER storeNo    AS INT.
DEF INPUT  PARAMETER main-grp   AS INT.
DEF INPUT  PARAMETER tage       AS INT.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF INPUT  PARAMETER disptype   AS CHAR.
DEF OUTPUT PARAMETER str-flag   AS CHAR.    /*FD July 22, 2021*/
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE BUFFER lophis-buff FOR l-ophis.
DEFINE BUFFER buf-lop FOR l-op.
DEFINE BUFFER blophis FOR l-ophis.

DEFINE BUFFER bl-op    FOR l-op.
DEFINE BUFFER bl-ophis FOR l-ophis.
DEFINE BUFFER blop     FOR l-op.
DEFINE BUFFER bl-verbrauch FOR l-verbrauch. /* malik F1385A */

FOR EACH s-list: 
    DELETE s-list. 
END. 

IF disptype EQ "old" THEN
DO:
   RUN create-list.  
END.
ELSE IF disptype EQ "new" THEN
DO:
    RUN create-list2. 
END.
ELSE DO:
    RUN create-list3. 
END.



/* ragung*/
/*Gerald New Concept karna tidak sesuai last purchase datenya 9AF951*/
PROCEDURE create-list: 
  DEFINE VARIABLE n1 AS INTEGER. 
  DEFINE VARIABLE n2 AS INTEGER. 
  DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
  DEFINE VARIABLE transdate AS DATE.

  n1 = main-grp * 1000000. 
  n2 = (main-grp + 1) * 1000000 - 1. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  transdate = htparam.fdate. 

    FOR EACH s-list: 
        DELETE s-list. 
    END. 

    str-flag = "INN".
    
    FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 NO-LOCK :
          
      curr-best = 0. 
      FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-artikel.artnr 
          AND l-bestand.lager-nr EQ storeNo NO-LOCK NO-ERROR. 
      IF AVAILABLE l-bestand THEN curr-best = l-bestand.anz-anf-best 
          + l-bestand.anz-eingang - l-bestand.anz-ausgang.
      
      IF curr-best GT 0 THEN 
      DO:
        FOR EACH l-op WHERE l-op.artnr EQ l-artikel.artnr 
          AND l-op.loeschflag LE 1 
          AND l-op.op-art EQ 1
          AND l-op.lager-nr EQ storeNo
          AND l-op.datum LE transdate NO-LOCK BY l-op.datum DESC:
          
          IF l-op.datum LE (transdate - tage) THEN DO:
              FIND FIRST blop WHERE blop.artnr EQ l-op.artnr 
                    AND blop.op-art = l-op.op-art
                    AND blop.lager-nr = l-op.lager-nr
                    AND blop.datum GT l-op.datum NO-LOCK NO-ERROR.
              IF NOT AVAILABLE blop THEN DO:
                  FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                  IF NOT AVAILABLE s-list THEN
                  DO:
                    FOR EACH bl-op WHERE bl-op.artnr = l-op.artnr 
                       AND bl-op.loeschflag LE 1
                       AND bl-op.op-art EQ 1
                       AND bl-op.lager-nr EQ storeNo 
                       AND bl-op.datum LE (transdate - tage) NO-LOCK BY bl-op.datum DESCENDING:
                      
                       CREATE s-list. 
                       ASSIGN
                         s-list.artnr    = l-artikel.artnr
                         s-list.name     = l-artikel.bezeich 
                         s-list.min-oh   = l-artikel.min-bestand /*Alder - Serverless - Issue 669*/
                         s-list.curr-oh  = curr-best
                         s-list.content  = l-artikel.inhalt
                         s-list.zwkum    = l-artikel.zwkum
                         s-list.endkum   = l-artikel.endkum
                         s-list.unit     = l-artikel.masseinheit
                         s-list.datum    = bl-op.datum
                         . 
                       
                       IF show-price THEN 
                       DO: 
                         s-list.avrgprice    = l-artikel.vk-preis. 
                         s-list.ek-aktuell   = l-artikel.ek-aktuell. 
                       END.
                       LEAVE.
                    END.

                    FOR EACH bl-ophis WHERE bl-ophis.artnr = l-ophis.artnr
                    AND bl-ophis.op-art = 3 
                    AND bl-ophis.lager-nr EQ storeNo
                    AND bl-ophis.datum LE l-ophis.datum
                    AND NOT (bl-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK BY bl-ophis.datum DESCENDING:  
                    
                        ASSIGN s-list.datum2   = bl-ophis.datum.
                        LEAVE.
                    END.
                  END.   
              END.              
          END.          
        END.

        
        FOR EACH l-ophis WHERE l-ophis.artnr EQ l-artikel.artnr 
            AND l-ophis.op-art EQ 1 
            AND l-ophis.lager-nr EQ storeNo
            AND l-ophis.datum LE transdate
            AND NOT (l-ophis.fibukonto MATCHES "CANCELLED") NO-LOCK BY l-ophis.datum: 

            IF l-ophis.datum LE (transdate - tage) THEN DO:
                FIND FIRST l-op WHERE l-op.artnr EQ l-ophis.artnr 
                    AND l-op.op-art = l-ophis.op-art
                    AND l-op.lager-nr = l-ophis.lager-nr
                    AND l-op.datum GT l-ophis.datum NO-LOCK NO-ERROR.
                IF NOT AVAILABLE l-op THEN DO:
                    FIND FIRST blophis WHERE blophis.artnr EQ l-ophis.artnr 
                        AND blophis.op-art = l-ophis.op-art
                        AND blophis.lager-nr = l-ophis.lager-nr
                        AND blophis.datum GT l-ophis.datum NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE blophis THEN DO:
                        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE s-list THEN
                        DO:
                          FOR EACH bl-ophis WHERE bl-ophis.artnr = l-ophis.artnr
                            AND bl-ophis.op-art EQ 1
                            AND bl-ophis.lager-nr EQ storeNo
                            AND bl-ophis.datum LE (transdate - tage)
                            AND NOT (bl-ophis.fibukonto MATCHES "CANCELLED") NO-LOCK BY bl-ophis.datum DESCENDING: 
                            
                            CREATE s-list. 
                            ASSIGN
                               s-list.artnr    = l-artikel.artnr
                               s-list.name     = l-artikel.bezeich 
                               s-list.min-oh   = l-artikel.min-bestand /*Alder - Serverless - Issue 669*/
                               s-list.curr-oh  = curr-best
                               s-list.content  = l-artikel.inhalt
                               s-list.zwkum    = l-artikel.zwkum
                               s-list.endkum   = l-artikel.endkum
                               s-list.unit     = l-artikel.masseinheit
                               s-list.datum    = bl-ophis.datum
                               . 
                            
                            IF show-price THEN 
                            DO: 
                               s-list.avrgprice = l-artikel.vk-preis. 
                               s-list.ek-aktuell = l-artikel.ek-aktuell. 
                            END. 
                            LEAVE.
                          END.

                          FOR EACH bl-ophis WHERE bl-ophis.artnr = l-ophis.artnr
                          AND bl-ophis.op-art = 3 
                          AND bl-ophis.lager-nr EQ storeNo
                          AND bl-ophis.datum LE l-ophis.datum
                          AND NOT (bl-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK BY bl-ophis.datum DESCENDING:  
                          
                              ASSIGN s-list.datum2   = bl-ophis.datum.
                              LEAVE.
                          END.
                        END.
                    END.                    
                END.                
            END.
        END.
      END. 
    END.
END PROCEDURE. 

/*Gerald New Concept karna tidak sesuai last purchase datenya 9AF951*/
PROCEDURE create-list2: 
  DEFINE VARIABLE n1 AS INTEGER. 
  DEFINE VARIABLE n2 AS INTEGER. 
  DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
  DEFINE VARIABLE transdate AS DATE. 
  n1 = main-grp * 1000000. 
  n2 = (main-grp + 1) * 1000000 - 1.  
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  transdate = htparam.fdate. 

    FOR EACH s-list: 
        DELETE s-list. 
    END. 

    str-flag = "OUT".
    FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 
        NO-LOCK BY l-artikel.artnr: 

        curr-best = 0. 
        FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-artikel.artnr 
            AND l-bestand.lager-nr EQ storeNo NO-LOCK NO-ERROR. 
        IF AVAILABLE l-bestand THEN curr-best = l-bestand.anz-anf-best 
            + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
        
        IF curr-best GT 0 THEN 
        DO:                 
          FOR EACH l-op WHERE l-op.artnr EQ l-artikel.artnr 
              AND l-op.op-art EQ 3 
              AND l-op.loeschflag LE 1 
              AND l-op.lager-nr EQ storeNo
              AND l-op.datum LE transdate NO-LOCK BY l-op.datum DESC: 
            
              IF l-op.datum LE (transdate - tage) THEN DO:
                FIND FIRST blop WHERE blop.artnr EQ l-op.artnr 
                    AND blop.op-art = l-op.op-art
                    AND blop.lager-nr = l-op.lager-nr
                    AND blop.datum GT l-op.datum NO-LOCK NO-ERROR.
                IF NOT AVAILABLE blop THEN DO:
                    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE s-list THEN
                    DO:
                      FOR EACH bl-op WHERE bl-op.artnr = l-op.artnr 
                        AND bl-op.op-art EQ 3
                        AND bl-op.loeschflag LE 1
                        AND bl-op.lager-nr EQ storeNo
                        AND bl-op.datum LE (transdate - tage) NO-LOCK BY bl-op.datum DESCENDING:
                        
                        /* malik F1385A */
                        FIND LAST bl-verbrauch WHERE bl-verbrauch.artnr EQ bl-op.artnr NO-ERROR. 
                        IF AVAILABLE bl-verbrauch THEN
                        DO:
                            IF bl-verbrauch.datum EQ bl-op.datum THEN
                            DO:
                                CREATE s-list. 
                                ASSIGN
                                    s-list.artnr    = l-artikel.artnr
                                    s-list.name     = l-artikel.bezeich 
                                    s-list.min-oh   = l-artikel.min-bestand /*Alder - Serverless - Issue 669*/ 
                                    s-list.curr-oh  = curr-best
                                    s-list.content  = l-artikel.inhalt
                                    s-list.zwkum    = l-artikel.zwkum
                                    s-list.endkum   = l-artikel.endkum
                                    s-list.unit     = l-artikel.masseinheit
                                    s-list.datum2   = bl-op.datum
                                    . 
                                
                                IF show-price THEN 
                                DO: 
                                    s-list.avrgprice    = l-artikel.vk-preis. 
                                    s-list.ek-aktuell   = l-artikel.ek-aktuell. 
                                END. 
                                LEAVE.

                            END.
                        END. 
                        /* End malik */
                        
                      END.
                    END.
                END.                
            END.
          END. 
          
            FOR EACH l-ophis WHERE l-ophis.artnr EQ l-artikel.artnr 
                AND l-ophis.op-art EQ 3 
                AND l-ophis.lager-nr EQ storeNo
                AND l-ophis.datum LE transdate
                AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK BY l-ophis.datum DESC:

                IF l-ophis.datum LE (transdate - tage) THEN DO:
                  FIND FIRST l-op WHERE l-op.artnr EQ l-ophis.artnr 
                    AND l-op.op-art = l-ophis.op-art
                    AND l-op.lager-nr = l-ophis.lager-nr
                    AND l-op.datum GT l-ophis.datum NO-LOCK NO-ERROR.
                  IF NOT AVAILABLE l-op THEN DO:
                      FIND FIRST blophis WHERE blophis.artnr EQ l-ophis.artnr 
                        AND blophis.op-art = l-ophis.op-art
                        AND blophis.lager-nr = l-ophis.lager-nr
                        AND blophis.datum GT l-ophis.datum NO-LOCK NO-ERROR.
                      IF NOT AVAILABLE blophis THEN DO:
                          FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE s-list THEN
                          DO:
                            FOR EACH bl-ophis WHERE bl-ophis.artnr = l-ophis.artnr
                              AND bl-ophis.op-art = 3 
                              AND bl-ophis.lager-nr EQ storeNo
                              AND bl-ophis.datum LE (transdate - tage)
                              AND NOT (bl-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK BY bl-ophis.datum DESCENDING: 
                                /* malik F1385A */
                                FIND LAST bl-verbrauch WHERE bl-verbrauch.artnr EQ bl-ophis.artnr NO-ERROR.
                                IF AVAILABLE bl-verbrauch THEN
                                DO:
                                    IF bl-verbrauch.datum EQ bl-ophis.datum THEN
                                    DO:
                                          CREATE s-list. 
                                            ASSIGN
                                                s-list.artnr    = l-artikel.artnr
                                                s-list.name     = l-artikel.bezeich 
                                                s-list.min-oh   = l-artikel.min-bestand /*Alder - Serverless - Issue 669*/ 
                                                s-list.curr-oh  = curr-best
                                                s-list.content  = l-artikel.inhalt
                                                s-list.zwkum    = l-artikel.zwkum
                                                s-list.endkum   = l-artikel.endkum
                                                s-list.unit     = l-artikel.masseinheit
                                                s-list.datum2   = bl-ophis.datum
                                                . 
                                            IF show-price THEN 
                                            DO: 
                                                s-list.avrgprice = l-artikel.vk-preis. 
                                                s-list.ek-aktuell = l-artikel.ek-aktuell. 
                                            END.                         
                                            LEAVE. 
  
                                    END.
                                END.  
                                /* End malik*/
                            END.
                          END.
                      END.                       
                  END.                  
              END.                            
            END.
        END. 
    END. 
END PROCEDURE.


PROCEDURE create-list3: 
  DEFINE VARIABLE n1 AS INTEGER. 
  DEFINE VARIABLE n2 AS INTEGER. 
  DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
  DEFINE VARIABLE transdate AS DATE. 
  n1 = main-grp * 1000000. 
  n2 = (main-grp + 1) * 1000000 - 1. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  transdate = htparam.fdate. 

    FOR EACH s-list: 
        DELETE s-list. 
    END. 

    DEFINE VARIABLE curr-time AS INTEGER.

    str-flag = "IN-OUT".
    FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 
        NO-LOCK BY l-artikel.artnr: 

        curr-best = 0. 
        FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-artikel.artnr 
            AND l-bestand.lager-nr EQ storeNo NO-LOCK NO-ERROR. 
        IF AVAILABLE l-bestand THEN curr-best = l-bestand.anz-anf-best 
            + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
        
        IF curr-best GT 0 THEN 
        DO:          
          FOR EACH l-op WHERE l-op.artnr EQ l-artikel.artnr 
              AND (l-op.op-art EQ 1 OR l-op.op-art EQ 3)
              AND l-op.loeschflag LE 1 
              AND l-op.lager-nr EQ storeNo
              AND l-op.datum LE transdate NO-LOCK:

          
          /*FIND FIRST l-op WHERE l-op.artnr EQ l-artikel.artnr 
              AND (l-op.op-art EQ 1 OR l-op.op-art EQ 3)
              AND l-op.loeschflag LE 1 
              AND l-op.lager-nr EQ storeNo
              AND l-op.datum LE transdate NO-LOCK NO-ERROR. 
          DO WHILE AVAILABLE l-op : FT serverless*/
            IF l-op.datum LE (transdate - tage) THEN DO:   
                ASSIGN curr-time = TIME.

                IF l-op.docu-nr MATCHES "T*" AND l-op.stornogrund EQ ""  THEN .
                ELSE DO:
                    FIND FIRST blop WHERE blop.artnr EQ l-op.artnr 
                        AND blop.op-art = l-op.op-art
                        AND blop.lager-nr = l-op.lager-nr
                        AND blop.datum GT l-op.datum NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE blop THEN DO:
                        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE s-list THEN
                        DO:
                          FOR EACH bl-op WHERE bl-op.artnr = l-op.artnr 
                            AND bl-op.op-art EQ 1
                            AND bl-op.loeschflag LE 1
                            AND bl-op.lager-nr EQ storeNo
                            AND bl-op.datum LE l-op.datum NO-LOCK BY bl-op.datum DESCENDING:
                          
                            CREATE s-list. 
                            ASSIGN
                                s-list.artnr    = l-artikel.artnr
                                s-list.name     = l-artikel.bezeich 
                                s-list.min-oh   = l-artikel.min-bestand /*Alder - Serverless - Issue 669*/ 
                                s-list.curr-oh  = curr-best
                                s-list.content  = l-artikel.inhalt
                                s-list.zwkum    = l-artikel.zwkum
                                s-list.endkum   = l-artikel.endkum
                                s-list.unit     = l-artikel.masseinheit
                                s-list.datum    = bl-op.datum
                                . 
                            
                            IF show-price THEN 
                            DO: 
                                ASSIGN                               
                                    s-list.avrgprice    = l-artikel.vk-preis 
                                    s-list.ek-aktuell   = l-artikel.ek-aktuell. 
                            END. 
                            LEAVE.
                          END.                    
    
                          FOR EACH bl-op WHERE bl-op.artnr = l-op.artnr 
                            AND bl-op.op-art EQ 3
                            AND bl-op.loeschflag LE 1
                            AND bl-op.lager-nr EQ storeNo
                            AND bl-op.datum LE l-op.datum NO-LOCK BY bl-op.datum DESCENDING:
                      
                            ASSIGN s-list.datum2   = bl-op.datum.
                            LEAVE.
                          END.
                        END.
                    END.                                                            
                END.
            END.
            /*FIND NEXT l-op WHERE l-op.artnr EQ l-artikel.artnr 
                  AND l-op.loeschflag LE 1 
                  AND l-op.op-art EQ 1    
                  AND l-op.lager-nr EQ storeNo
                  AND l-op.datum LE transdate NO-LOCK NO-ERROR. */
          END.

           
          DO:            
            FOR EACH l-ophis WHERE l-ophis.artnr EQ l-artikel.artnr 
                AND (l-ophis.op-art EQ 1 OR l-ophis.op-art EQ 3)
                AND l-ophis.lager-nr EQ storeNo
                AND l-ophis.datum LE transdate
                AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK:
            /*FIND FIRST l-ophis WHERE l-ophis.artnr EQ l-artikel.artnr 
                AND (l-ophis.op-art EQ 1 OR l-ophis.op-art EQ 3)
                AND l-ophis.lager-nr EQ storeNo
                AND l-ophis.datum LE transdate
                AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK NO-ERROR. 
            DO WHILE AVAILABLE l-ophis :*/
              IF l-ophis.datum LE (transdate - tage) THEN DO:
                  FIND FIRST l-op WHERE l-op.artnr EQ l-ophis.artnr 
                    /*AND l-op.op-art = l-ophis.op-art*/
                    AND l-op.lager-nr = l-ophis.lager-nr
                    AND l-op.datum GT l-ophis.datum NO-LOCK NO-ERROR.
                  IF NOT AVAILABLE l-op THEN DO:
                      FIND FIRST blophis WHERE blophis.artnr EQ l-ophis.artnr 
                        /*AND blophis.op-art = l-ophis.op-art*/
                        AND blophis.lager-nr = l-ophis.lager-nr
                        AND blophis.datum GT l-ophis.datum NO-LOCK NO-ERROR.
                      IF NOT AVAILABLE blophis THEN DO:
                          FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE s-list THEN
                          DO:
                            FOR EACH bl-ophis WHERE bl-ophis.artnr = l-ophis.artnr
                              AND bl-ophis.op-art = 1 
                              AND bl-ophis.lager-nr EQ storeNo
                              AND bl-ophis.datum LE l-ophis.datum
                              AND NOT (bl-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK BY bl-ophis.datum DESCENDING:  
                            
                              CREATE s-list. 
                              ASSIGN
                                  s-list.artnr    = l-artikel.artnr
                                  s-list.name     = l-artikel.bezeich 
                                  s-list.min-oh   = l-artikel.min-bestand /*Alder - Serverless - Issue 669*/ 
                                  s-list.curr-oh  = curr-best
                                  s-list.content  = l-artikel.inhalt
                                  s-list.zwkum    = l-artikel.zwkum
                                  s-list.endkum   = l-artikel.endkum
                                  s-list.unit     = l-artikel.masseinheit
                                  s-list.datum    = bl-ophis.datum
                                  . 
                              IF show-price THEN 
                              DO: 
                                  s-list.avrgprice = l-artikel.vk-preis. 
                                  s-list.ek-aktuell = l-artikel.ek-aktuell. 
                              END. 
                            
                              LEAVE.    
                            END.

                            FOR EACH bl-ophis WHERE bl-ophis.artnr = l-ophis.artnr
                                  AND bl-ophis.op-art = 3 
                                  AND bl-ophis.lager-nr EQ storeNo
                                  AND bl-ophis.datum LE l-ophis.datum
                                  AND NOT (bl-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK BY bl-ophis.datum DESCENDING:  
                            
                                ASSIGN s-list.datum2   = bl-ophis.datum.
                                LEAVE.
                            END.
                          END.
                      END.                       
                  END.
              END.
              
              /*FIND NEXT l-ophis WHERE l-ophis.artnr EQ l-artikel.artnr 
                AND (l-ophis.op-art EQ 1 OR l-ophis.op-art EQ 3 )
                AND l-ophis.lager-nr EQ storeNo
                AND l-ophis.datum LE transdate
                AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") NO-LOCK NO-ERROR. */
            END.
          END.
        END. 
    END. 
END PROCEDURE.


