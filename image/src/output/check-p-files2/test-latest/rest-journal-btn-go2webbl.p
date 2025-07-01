DEFINE TEMP-TABLE output-list
    FIELD date1         AS DATE
    FIELD tableNo       AS INTEGER FORMAT ">>>>9"
    FIELD billNo        AS INTEGER
    FIELD artNo         AS INTEGER
    FIELD bezeich       AS CHARACTER
    FIELD depart        AS CHARACTER
    FIELD qty           AS INTEGER
    FIELD amount        AS CHARACTER 
    FIELD zeit          AS INTEGER
    FIELD id            AS CHARACTER
    FIELD guestname     AS CHARACTER
    FIELD h-recid       AS INTEGER
    FIELD order-taker   AS CHAR. /* malik 3AFAC8 */

DEF INPUT PARAMETER od-taker    AS CHAR.
DEF INPUT PARAMETER from-art    AS INT.
DEF INPUT PARAMETER to-art      AS INT.
DEF INPUT PARAMETER from-dept   AS INT.
DEF INPUT PARAMETER to-dept     AS INT.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER sorttype    AS INT.
DEF INPUT PARAMETER long-digit  AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE disc-art1 AS INTEGER.
DEFINE VARIABLE disc-art2 AS INTEGER.
DEFINE VARIABLE disc-art3 AS INTEGER.
DEFINE VARIABLE curr-time AS INTEGER.
DEFINE VARIABLE counter AS INTEGER INITIAL 0.
DEFINE VARIABLE counter2 AS INTEGER INITIAL 0.

/*FD July 19, 2021*/
FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
disc-art2 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
disc-art3 = vhp.htparam.finteger.
 
RUN journal-list.

PROCEDURE journal-list: 
    DEFINE VARIABLE last-dept   AS INTEGER INITIAL -1. 
    DEFINE VARIABLE qty         AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE takerNum    AS INTEGER INITIAL 0.
    DEFINE VARIABLE sub-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE curr-date   AS DATE. 
    DEFINE VARIABLE it-exist    AS LOGICAL. 
    DEFINE VARIABLE do-it       AS LOGICAL.
    
    DEFINE VARIABLE curr-guest  AS CHAR INITIAL "" NO-UNDO.
    DEFINE VARIABLE tot-qty AS INTEGER.
    DEFINE VARIABLE order-taker AS CHARACTER NO-UNDO. 

    DEFINE VARIABLE hotel-num   AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-time AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-artikel AS INTEGER NO-UNDO.

  FOR EACH output-list: 
    DELETE output-list. 
  END. 
 
  IF od-taker NE "" THEN
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 10 AND queasy.char2 = od-taker
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN takerNum = queasy.number1.
  END.
  IF from-art = 0 THEN DO:
        ASSIGN
            sub-tot     = 0 
            it-exist    = NO 
            qty         = 0. 
    
        IF sorttype = 0 THEN DO:
            FOR EACH h-journal WHERE h-journal.artnr = 0 AND h-journal.departement = hoteldpt.num 
                AND h-journal.bill-datum GE from-date
                AND h-journal.bill-datum LE to-date AND h-journal.artnr GT 0 AND h-journal.anzahl NE 0 NO-LOCK,
                FIRST hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num:
    
                IF hotel-num NE 0 AND hotel-num NE hoteldpt.num THEN DO:
                    IF it-exist THEN 
                    DO: 
                      CREATE output-list. 
                      IF long-digit = NO THEN
                      DO:
                            output-list.bezeich = "T O T A L ".
                            output-list.qty    = qty    .  
                            output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                       END.
                       ELSE
                       DO:
                            output-list.bezeich = "T O T A L ".
                            output-list.qty    = qty    .  
                            output-list.amount = STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
                       END.      
                    END. 
    
                    ASSIGN
                        sub-tot     = 0 
                        it-exist    = NO 
                        qty         = 0
                        hotel-num   = 0. 
                END.
    
                ASSIGN hotel-num = hoteldpt.num.
                /*RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker).*/
                RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* malik 3AFAC8 */
                curr-guest = "".
                FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr
                  AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                IF AVAILABLE h-bill THEN
                DO:
                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
                            AND res-line.reslinnr = h-bill.reslinnr
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN curr-guest = res-line.NAME.
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN
                    DO:
                      FIND FIRST guest WHERE h-bill.resnr = guest.gastnr
                        NO-LOCK NO-ERROR.
                      IF AVAILABLE guest THEN curr-guest = guest.NAME + "," + guest.vorname1.
                    END.
                    ELSE IF h-bill.resnr = 0 THEN DO: 
                        curr-guest = h-bill.bilname.
                    END.
                END.
                IF takerNum = 0 THEN do-it = YES.
                ELSE
                DO:
                  do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                END.
        
                /*FDL August 24, 2023 => Ticket No 4CB0EA*/
                IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                    OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN
                DO:
                    it-exist = YES.
                    do-it = NO.
                END.
        
                IF do-it THEN
                DO:
                  it-exist = YES. 
                  CREATE output-list. 
                  ASSIGN
                      output-list.guestname   = curr-guest
                      output-list.h-recid = RECID(h-journal)
                  . 
                      IF NOT long-digit THEN
                      DO:
                            output-list.date1       = h-journal.bill-datum. /* Malik Serverless 384 : bill-datum -> h-journal.bill-datum */ 
                            output-list.tableNo     = h-journal.tischnr.                      
                            output-list.billNo      = h-journal.rechnr.
                            output-list.artNo       = h-journal.artnr.
                            output-list.bezeich     = h-journal.bezeich.
                            output-list.depart      = hoteldpt.depart.
                            output-list.qty         = h-journal.anzahl.
                            output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                            output-list.zeit        = h-journal.zeit.
                            output-list.id          = STRING(h-journal.kellner-nr, "9999").
                            output-list.order-taker = order-taker. /* malik 3AFAC8 */
                      END.
                      ELSE
                      DO:
                            output-list.date1       = h-journal.bill-datum. /* Malik Serverless 384 : bill-datum -> h-journal.bill-datum */ 
                            output-list.tableNo     = h-journal.tischnr.                      
                            output-list.billNo      = h-journal.rechnr.
                            output-list.artNo       = h-journal.artnr.
                            output-list.bezeich     = h-journal.bezeich.
                            output-list.depart      = hoteldpt.depart.
                            output-list.qty         = h-journal.anzahl.
                            output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                            output-list.zeit        = h-journal.zeit.
                            output-list.id          = STRING(h-journal.kellner-nr, "9999").
                            output-list.order-taker = order-taker. /* malik 3AFAC8 */
                      END.
                  
                  qty = qty + h-journal.anzahl. 
                  sub-tot = sub-tot + h-journal.betrag. 
                  tot = tot + h-journal.betrag. 
                END.
            END.
        END.
        ELSE IF sorttype = 1 THEN DO:
            curr-time = TIME.
            FOR EACH h-journal WHERE h-journal.artnr = 0 AND h-journal.departement = hoteldpt.num 
                AND h-journal.bill-datum GE from-date
                AND h-journal.bill-datum LE to-date NO-LOCK,
                FIRST hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num:
    
                IF hotel-num NE 0 AND hotel-num NE hoteldpt.num THEN DO:
                    IF it-exist THEN 
                    DO: 
                      CREATE output-list. 
                      IF long-digit = NO THEN
                      DO:
                            output-list.bezeich = "T O T A L ".
                            output-list.qty    = qty    .  
                            output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                       END.
                       ELSE
                       DO:
                            output-list.bezeich = "T O T A L ".
                            output-list.qty    = qty    .  
                            output-list.amount = STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
                       END.      
                    END. 
    
                    ASSIGN
                        sub-tot     = 0 
                        it-exist    = NO 
                        qty         = 0
                        hotel-num   = 0. 
                END.
                ASSIGN hotel-num = hoteldpt.num.
    
                /*RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker).*/
                RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* malik 3AFAC8 */
                curr-guest = "".
                FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr
                  AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                IF AVAILABLE h-bill THEN
                DO:
                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
                            AND res-line.reslinnr = h-bill.reslinnr
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN curr-guest = res-line.NAME.
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN
                    DO:
                      FIND FIRST guest WHERE h-bill.resnr = guest.gastnr
                        NO-LOCK NO-ERROR.
                      IF AVAILABLE guest THEN curr-guest = guest.NAME + "," + guest.vorname1.
                    END.
                    ELSE IF h-bill.resnr = 0 THEN DO: 
                        curr-guest = h-bill.bilname.
                    END.
                END.
                IF takerNum = 0 THEN do-it = YES.
                ELSE
                DO:
                  do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                END.
                
                /*FDL August 24, 2023 => Ticket No 4CB0EA*/
                IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                    OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN
                DO:
                    it-exist = YES.
                    do-it = NO.
                END.
        
                IF do-it THEN
                DO:
                  it-exist = YES. 
                  CREATE output-list. 
                  ASSIGN
                      output-list.guestname   = curr-guest
                      output-list.h-recid = RECID(h-journal)
                  . 
                  IF long-digit = NO THEN
                    DO:
                        
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                      
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
                    ELSE
                    DO:
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                      
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag, "->>>,>>>,>>>,>>9").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                       
                    END.
                  qty = qty + h-journal.anzahl. 
                  sub-tot = sub-tot + h-journal.betrag. 
                 tot = tot + h-journal.betrag. 
                END.
                counter = counter + 1.
            END.
        END.
        ELSE DO:
            curr-time = TIME.
            FOR EACH h-journal WHERE h-journal.artnr = 0 AND h-journal.departement = hoteldpt.num 
                AND h-journal.bill-datum = from-date
                AND h-journal.bill-datum = to-date AND h-journal.artnr = 0 NO-LOCK,
                FIRST hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num:
    
                IF hotel-num NE 0 AND hotel-num NE hoteldpt.num THEN DO:
                    IF it-exist THEN 
                    DO: 
                      CREATE output-list. 
                      IF long-digit = NO THEN
                      DO:
                            output-list.bezeich = "T O T A L ".
                            output-list.qty    = qty    .  
                            output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                       END.
                       ELSE
                       DO:
                            output-list.bezeich = "T O T A L ".
                            output-list.qty    = qty    .  
                            output-list.amount = STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
                       END.      
                    END. 
    
                    ASSIGN
                        sub-tot     = 0 
                        it-exist    = NO 
                        qty         = 0
                        hotel-num   = 0. 
                END.
                ASSIGN hotel-num = hoteldpt.num.
                
                /*RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker).*/
                RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* malik 3AFAC8 */
                curr-guest = "".
                FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr
                  AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                IF AVAILABLE h-bill THEN
                DO:
                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
                            AND res-line.reslinnr = h-bill.reslinnr
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN curr-guest = res-line.NAME.
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN
                    DO:
                      FIND FIRST guest WHERE h-bill.resnr = guest.gastnr
                        NO-LOCK NO-ERROR.
                      IF AVAILABLE guest THEN curr-guest = guest.NAME + "," + guest.vorname1.
                    END.
                    ELSE IF h-bill.resnr = 0 THEN DO: 
                        curr-guest = h-bill.bilname.
                    END.
                END.
                IF takerNum = 0 THEN do-it = YES.
                ELSE
                DO:
                  do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                END.
                
                /*FDL August 24, 2023 => Ticket No 4CB0EA*/
                IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                    OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN
                DO:
                    it-exist = YES.
                    do-it = NO.
                END.
        
                IF do-it THEN
                DO:
                  it-exist = YES. 
                  CREATE output-list. 
                  ASSIGN
                      output-list.guestname   = curr-guest
                      output-list.h-recid = RECID(h-journal)
                  . 
                  IF long-digit = NO THEN
                    DO:
                        
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                            
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
                    ELSE
                    DO:
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                           
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag, "->>>,>>>,>>>,>>9").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
                  qty = qty + h-journal.anzahl. 
                  sub-tot = sub-tot + h-journal.betrag. 
                  tot = tot + h-journal.betrag. 
                END.
                counter = counter + 1.              
            END.
        END.
    
        IF it-exist THEN 
        DO: 
          CREATE output-list. 
          IF long-digit = NO THEN
          DO:
                output-list.bezeich = "T O T A L ".
                output-list.qty    = qty    .  
                output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
           END.
           ELSE
           DO:
                output-list.bezeich = "T O T A L ".
                output-list.qty    = qty    .  
                output-list.amount = STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
           END.      
        END. 
  END. /*end from-art = 0*/

  ASSIGN curr-time = TIME.
  last-dept = - 1. 
  ASSIGN 
    sub-tot     = 0 
    it-exist    = NO 
    qty         = 0. 

  IF sorttype = 0 THEN DO:
        FOR EACH h-journal WHERE h-journal.bill-datum GE from-date
            AND h-journal.bill-datum LE to-date 
            AND h-journal.artnr GT 0 
            AND h-journal.anzahl NE 0 USE-INDEX chrono_ix NO-LOCK,
            FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr
            AND h-artikel.departement = h-journal.departement
            AND h-artikel.artnr GE from-art AND h-artikel.artnr LE to-art 
            AND h-artikel.departement GE from-dept AND h-artikel.departement LE to-dept USE-INDEX depart_index NO-LOCK,
            FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
            AND h-bill.tischnr EQ h-journal.tischnr 
            AND h-bill.departement = h-journal.departement NO-LOCK, /*bernatd 98F717*/
            FIRST hoteldpt WHERE hoteldpt.num = h-artikel.departement NO-LOCK BY h-artikel.departement 
            BY h-artikel.artnr:
        
            IF curr-artikel NE 0 AND curr-artikel NE h-artikel.artnr THEN DO:
                IF it-exist THEN 
                DO: 
                  tot-qty = qty + tot-qty.
                  create output-list.
                   IF long-digit = NO THEN
                   DO:
                        output-list.bezeich = "T O T A L ".
                        output-list.qty    = qty    .  
                        output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                    END.
                    ELSE 
                    DO:
                        output-list.bezeich = "T O T A L ".
                        output-list.qty    = qty    .  
                        output-list.amount = STRING(sub-tot, "->>>,>>>,>>>,>>9"). 
                    END.              
                END.  
                
                ASSIGN 
                    sub-tot     = 0 
                    it-exist    = NO 
                    qty         = 0. 
            END.
            ASSIGN
                last-dept    = h-artikel.departement
                curr-artikel = h-artikel.artnr. 
           
           /* RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* malik 3AFAC8 */ */

            /*start bernatd 98F717*/
            FIND FIRST queasy WHERE queasy.KEY EQ 10 AND queasy.number1 EQ h-bill.betriebsnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN 
            DO:
               ASSIGN 
                 order-taker = queasy.char2.     
            END.
            IF NOT AVAILABLE queasy THEN
            DO:
                order-taker = "".  
            END.
            /*end bernatd 98F717*/

            curr-guest = "". 
            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
            DO:
                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
                    AND res-line.reslinnr = h-bill.reslinnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN curr-guest = res-line.NAME.
            END.
            ELSE IF h-bill.resnr GT 0 THEN
            DO:
              FIND FIRST guest WHERE h-bill.resnr = guest.gastnr
                NO-LOCK NO-ERROR.
              IF AVAILABLE guest THEN curr-guest = guest.NAME + "," + guest.vorname1.
            END.
            ELSE IF h-bill.resnr = 0 THEN DO: 
                curr-guest = h-bill.bilname.
            END.

            IF takerNum = 0 THEN do-it = YES.
            ELSE
            DO:
              do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
            END.
        
            /*FDL August 24, 2023 => Ticket No 4CB0EA*/
            IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN
            DO:
                it-exist = YES.
                do-it = NO.
            END.
                
            IF do-it THEN
            DO:
              it-exist = YES. 
              CREATE output-list. 
              ASSIGN
                  output-list.guestname   = curr-guest
                  output-list.h-recid = RECID(h-journal)
              . 
                  IF long-digit = NO THEN
                  DO:
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                          
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
                    ELSE
                    DO:
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                            
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag, "->>>,>>>,>>>,>>9").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
              
              qty       = qty + h-journal.anzahl. 
              sub-tot   = sub-tot + h-journal.betrag. 
              tot       = tot + h-journal.betrag. 
            END.
        END.
  END. 

  ELSE IF sorttype = 1 THEN DO:
        FOR EACH h-journal WHERE h-journal.bill-datum GE from-date
            AND h-journal.bill-datum LE to-date NO-LOCK,
            FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr
            AND h-artikel.departement = h-journal.departement
            AND h-artikel.artnr GE from-art AND h-artikel.artnr LE to-art 
            AND h-artikel.departement GE from-dept AND h-artikel.departement LE to-dept NO-LOCK,
            FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
            AND h-bill.tischnr EQ h-journal.tischnr 
            AND h-bill.departement = h-journal.departement NO-LOCK, /*bernatd 98F717*/
            FIRST hoteldpt WHERE hoteldpt.num = h-artikel.departement NO-LOCK BY h-artikel.departement 
            BY h-artikel.artnr:
    
            IF curr-artikel NE 0 AND curr-artikel NE h-artikel.artnr THEN DO:
                IF it-exist THEN 
                DO: 
                  tot-qty = qty + tot-qty.
                  create output-list.
                   IF long-digit = NO THEN
                   DO:
                        output-list.bezeich = "T O T A L ".
                        output-list.qty    = qty    .  
                        output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                    END.
                    ELSE 
                    DO:
                        output-list.bezeich = "T O T A L ".
                        output-list.qty    = qty    .  
                        output-list.amount = STRING(sub-tot, "->>>,>>>,>>>,>>9"). 
                    END.              
                END.  
                
                ASSIGN 
                    sub-tot     = 0 
                    it-exist    = NO 
                    qty         = 0. 
    
    
            END.
            ASSIGN
                last-dept    = h-artikel.departement
                curr-artikel = h-artikel.artnr. 
       
           /* RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* malik 3AFAC8 */ */

           /*start bernatd 98F717*/
           FIND FIRST queasy WHERE queasy.KEY EQ 10 AND queasy.number1 EQ h-bill.betriebsnr NO-LOCK NO-ERROR.
           IF AVAILABLE queasy THEN 
           DO:
             ASSIGN 
               order-taker = queasy.char2.     
           END.
           IF NOT AVAILABLE queasy THEN
           DO:
               order-taker = "".  
           END.
           /*end bernatd*/

            curr-guest = "".
               IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
               DO:
                    FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
                        AND res-line.reslinnr = h-bill.reslinnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN curr-guest = res-line.NAME.
                END.
                ELSE IF h-bill.resnr GT 0 THEN
                DO:
                  FIND FIRST guest WHERE h-bill.resnr = guest.gastnr
                    NO-LOCK NO-ERROR.
                  IF AVAILABLE guest THEN curr-guest = guest.NAME + "," + guest.vorname1.
                END.
                ELSE IF h-bill.resnr = 0 THEN DO: 
                    curr-guest = h-bill.bilname.
                END.

            IF takerNum = 0 THEN do-it = YES.
            ELSE
            DO:
              do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
            END.
        
            /*FDL August 24, 2023 => Ticket No 4CB0EA*/
            IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN
            DO:
                it-exist = YES.
                do-it = NO.
            END.
        
            IF do-it THEN
            DO:
              it-exist = YES. 
              CREATE output-list.
              ASSIGN
                  output-list.guestname = curr-guest
                  output-list.h-recid = RECID(h-journal)
              . 
               IF long-digit = NO THEN
                  DO:
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                            
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
                    ELSE
                    DO:
                        output-list.date1       = h-journal.bill-datum.  
                        output-list.tableNo     = h-journal.tischnr.                          
                        output-list.billNo      = h-journal.rechnr.
                        output-list.artNo       = h-journal.artnr.
                        output-list.bezeich     = h-journal.bezeich.
                        output-list.depart      = hoteldpt.depart.
                        output-list.qty         = h-journal.anzahl.
                        output-list.amount      = STRING(h-journal.betrag, "->>>,>>>,>>>,>>9").
                        output-list.zeit        = h-journal.zeit.
                        output-list.id          = STRING(h-journal.kellner-nr, "9999").
                        output-list.order-taker = order-taker. /* malik 3AFAC8 */
                        
                    END.
              qty = qty + h-journal.anzahl. 
              sub-tot = sub-tot + h-journal.betrag. 
              tot = tot + h-journal.betrag. 
            END.
        END.
  END.
  ELSE DO:
      FOR EACH h-journal WHERE h-journal.bill-datum GE from-date
        AND h-journal.bill-datum LE to-date AND h-journal.artnr = 0 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr
        AND h-artikel.departement = h-journal.departement
        AND h-artikel.artnr GE from-art AND h-artikel.artnr LE to-art 
        AND h-artikel.departement GE from-dept AND h-artikel.departement LE to-dept NO-LOCK, 
        FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
        AND h-bill.tischnr EQ h-journal.tischnr 
        AND h-bill.departement = h-journal.departement NO-LOCK, /*bernatd 98F717*/
        FIRST hoteldpt WHERE hoteldpt.num = h-artikel.departement NO-LOCK BY h-artikel.departement 
        BY h-artikel.artnr: 
    
        IF curr-artikel NE 0 AND curr-artikel NE h-artikel.artnr THEN DO:
            IF it-exist THEN 
            DO: 
              tot-qty = qty + tot-qty.
              create output-list.
               IF long-digit = NO THEN
               DO:
                    output-list.bezeich = "T O T A L ".
                    output-list.qty    = qty    .  
                    output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                END.
                ELSE 
                DO:
                    output-list.bezeich = "T O T A L ".
                    output-list.qty    = qty    .  
                    output-list.amount = STRING(sub-tot, "->>>,>>>,>>>,>>9"). 
                END.              
            END.  
            
            ASSIGN 
                sub-tot     = 0 
                it-exist    = NO 
                qty         = 0. 
    
    
        END.
        ASSIGN
            last-dept    = h-artikel.departement
            curr-artikel = h-artikel.artnr. 

       /* RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). */

       /*start bernatd 98F717*/
       FIND FIRST queasy WHERE queasy.KEY EQ 10 AND queasy.number1 EQ h-bill.betriebsnr NO-LOCK NO-ERROR.
       IF AVAILABLE queasy THEN 
       DO:
         ASSIGN 
           order-taker = queasy.char2.     
       END.
       IF NOT AVAILABLE queasy THEN
       DO:
           order-taker = "".  
       END.
       /*end bernatd*/

        curr-guest = "".
            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
            DO:
                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
                    AND res-line.reslinnr = h-bill.reslinnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN curr-guest = res-line.NAME.
            END.
            ELSE IF h-bill.resnr GT 0 THEN
            DO:
              FIND FIRST guest WHERE h-bill.resnr = guest.gastnr
                NO-LOCK NO-ERROR.
              IF AVAILABLE guest THEN curr-guest = guest.NAME + "," + guest.vorname1.
            END.
            ELSE IF h-bill.resnr = 0 THEN DO: 
                curr-guest = h-bill.bilname.
            END.

        IF takerNum = 0 THEN do-it = YES.
        ELSE
        DO:
          do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
        END.
    
        /*FDL August 24, 2023 => Ticket No 4CB0EA*/
        IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
            OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN
        DO:
            it-exist = YES.
            do-it = NO.
        END.
    
        IF do-it THEN
        DO:
          it-exist = YES. 
          CREATE output-list.
          ASSIGN
              output-list.guestname   = curr-guest
              output-list.h-recid = RECID(h-journal)
          . 
           IF long-digit = NO THEN
              DO:
                    output-list.date1       = h-journal.bill-datum.  
                    output-list.tableNo     = h-journal.tischnr.                           
                    output-list.billNo      = h-journal.rechnr.
                    output-list.artNo       = h-journal.artnr.
                    output-list.bezeich     = h-journal.bezeich.
                    output-list.depart      = hoteldpt.depart.
                    output-list.qty         = h-journal.anzahl.
                    output-list.amount      = STRING(h-journal.betrag,"->,>>>,>>>,>>9.99").
                    output-list.zeit        = h-journal.zeit.
                    output-list.id          = STRING(h-journal.kellner-nr, "9999").
                    output-list.order-taker = order-taker. /* malik 3AFAC8 */
                    
                END.
                ELSE
                DO:
                    output-list.date1       = h-journal.bill-datum.  
                    output-list.tableNo     = h-journal.tischnr.                           
                    output-list.billNo      = h-journal.rechnr.
                    output-list.artNo       = h-journal.artnr.
                    output-list.bezeich     = h-journal.bezeich.
                    output-list.depart      = hoteldpt.depart.
                    output-list.qty         = h-journal.anzahl.
                    output-list.amount      = STRING(h-journal.betrag, "->>>,>>>,>>>,>>9").
                    output-list.zeit        = h-journal.zeit.
                    output-list.id          = STRING(h-journal.kellner-nr, "9999").
                    output-list.order-taker = order-taker. /* malik 3AFAC8 */  
                END.
          qty       = qty + h-journal.anzahl. 
          sub-tot   = sub-tot + h-journal.betrag. 
          tot       = tot + h-journal.betrag.
        END.
      END.
  END.
    
  IF it-exist THEN 
  DO: 
      tot-qty = qty + tot-qty.
      create output-list.
       IF long-digit = NO THEN
       DO:
            output-list.bezeich = "T O T A L ".
            output-list.qty    = qty    .  
            output-list.amount = STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
        END.
        ELSE 
        DO:
            output-list.bezeich = "T O T A L ".
            output-list.qty    = qty    .  
            output-list.amount = STRING(sub-tot, "->>>,>>>,>>>,>>9"). 
        END.              
  END.  
  
  CREATE output-list. 
  IF NOT long-digit THEN
  DO:
      output-list.bezeich = "GRAND TOTAL ".
      output-list.qty    = tot-qty    .  
      output-list.amount = STRING(tot, "->,>>>,>>>,>>9.99"). 
  END.
  ELSE
  DO:
      output-list.bezeich = "GRAND TOTAL".
      output-list.qty    = tot-qty    .  
      output-list.amount = STRING(tot, "->>>,>>>,>>>,>>9"). 
  END.   
END. 


PROCEDURE search-ot:
    DEFINE INPUT PARAMETER r-nr AS INTEGER NO-UNDO.
    DEFINE INPUT PARAMETER t-nr AS INTEGER NO-UNDO.
    DEFINE OUTPUT PARAMETER order-taker AS CHARACTER NO-UNDO.
    FIND FIRST h-bill WHERE h-bill.rechnr EQ r-nr AND h-bill.tischnr EQ t-nr NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN FIND FIRST queasy WHERE queasy.KEY EQ 10 AND queasy.number1 EQ h-bill.betriebsnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO:
        ASSIGN 
            order-taker = queasy.char2.
            
    END.
        
END.








