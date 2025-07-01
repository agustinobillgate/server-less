DEFINE TEMP-TABLE f-list
    FIELD rstat AS CHAR FORMAT "x(9)"
    FIELD bname AS CHAR FORMAT "x(24)"
    FIELD room  AS CHAR FORMAT "x(24)"
    FIELD id    AS CHAR FORMAT "x(2)"
    FIELD event AS CHAR FORMAT "x(16)"
    FIELD cdate AS DATE FORMAT "99/99/99"
    FIELD pax   AS INTEGER FORMAT ">>>,>>9"
    FIELD rmrev AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD fbrev AS DECIMAL FORMAT " >>>,>>>,>>9.99"
    FIELD otrev AS DECIMAL FORMAT " >>>,>>>,>>9.99"
    FIELD totrev AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD cp     AS CHAR  FORMAT "x(16)"
    FIELD resnr  AS INTEGER FORMAT ">,>>>,>>9"
    FIELD date-book AS DATE FORMAT "99/99/99"
    FIELD in-sales  AS CHAR FORMAT "x(20)" /*naufal - add incharge id*/
    FIELD sales     AS CHAR FORMAT "x(20)"/*NA - add booking salesname*/
    FIELD ev-time   AS CHAR FORMAT "x(15)" /*FD Nov 24, 2021*/
    .

DEFINE TEMP-TABLE output-list
    FIELD flag AS CHAR
    FIELD bezeich  AS CHAR
    FIELD rstat AS CHAR
    FIELD room  AS CHAR
    FIELD id    AS CHAR
    FIELD ba-event AS CHAR
    FIELD datum AS DATE 
    FIELD pax   AS INTEGER
    FIELD rmrev AS DECIMAL
    FIELD fbrev AS DECIMAL
    FIELD othrev AS DECIMAL
    FIELD totrev AS DECIMAL
    FIELD cp     AS CHAR
    FIELD resnr  AS INTEGER
    FIELD date-book AS DATE
    FIELD in-sales  AS CHAR
    FIELD ev-time   AS CHAR.

DEF INPUT  PARAMETER checklist AS LOGICAL.
DEF INPUT  PARAMETER sorttype  AS INTEGER.
DEF INPUT  PARAMETER fdate     AS DATE.
DEF INPUT  PARAMETER tdate     AS DATE.
DEF INPUT  PARAMETER disp-flag AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER room  FOR bk-raum.
DEFINE BUFFER gast  FOR guest.
DEFINE BUFFER usr   FOR bediener.
DEFINE BUFFER event FOR ba-typ.

DEFINE VARIABLE cob         AS CHAR.
DEFINE VARIABLE str1        AS CHAR    INITIAL "".
DEFINE VARIABLE totrmrev    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" INITIAL 0.
DEFINE VARIABLE totfbrev    AS DECIMAL FORMAT ">>>,>>>,>>9.99"     INITIAL 0.
DEFINE VARIABLE totother    AS DECIMAL FORMAT ">>>,>>>,>>9.99"     INITIAL 0.
DEFINE VARIABLE totrev      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" INITIAL 0.
DEFINE VARIABLE totpax      AS INTEGER .
DEFINE VARIABLE subrmrev    AS DECIMAL INITIAL 0.
DEFINE VARIABLE subfbrev    AS DECIMAL INITIAL 0.
DEFINE VARIABLE subother    AS DECIMAL INITIAL 0.
DEFINE VARIABLE subrev      AS DECIMAL INITIAL 0.
DEFINE VARIABLE subpax      AS INTEGER.

RUN create-browse.

PROCEDURE create-browse:
    DEFINE VARIABLE groupby     AS CHAR NO-UNDO.
    DEFINE VARIABLE line1       AS INTEGER INITIAL 0 NO-UNDO.

    FOR EACH output-list:
        DELETE output-list.
    END.

    RUN create-list.

    ASSIGN 
        totrmrev = 0
        totfbrev = 0
        totpax   = 0
        totrev   = 0
        totother = 0.

    IF NOT checklist THEN
    DO:
        IF sorttype = 0 THEN /*By Sales*/
        DO:
            /*Naufal - Add Validation for group by sales incharge Horrison Bekasi*/
            IF disp-flag = 1 THEN
            DO:
                FOR EACH f-list NO-LOCK BY f-list.sales BY f-list.cdate BY f-list.room:
                    line1 = line1 + 1.
                    
                    IF line1 = 1 THEN
                    DO:
                        groupby = f-list.sales. /*NA - Add sales name*/
                        RUN create-group ("SALES ID", groupby).
                    END.
                    
                    IF f-list.sales NE groupby THEN
                    DO:
                        RUN create-subtotal.
                        RUN create-group("SALES ID", f-list.sales). /*NA - Add sales name*/
                    END.
                    
                    RUN create-data.
                    groupby = f-list.sales. /*NA - Add sales name*/
                END.
            END.
            ELSE IF disp-flag = 2 THEN
            DO:
                FOR EACH f-list NO-LOCK BY f-list.in-sales BY f-list.cdate BY f-list.room:
                    line1 = line1 + 1.
                    
                    IF line1 = 1 THEN
                    DO:
                        groupby = f-list.in-sales.
                        RUN create-group ("SALES INCHARGE", groupby).
                    END.
                    
                    IF f-list.in-sales NE groupby THEN
                    DO:
                        RUN create-subtotal.
                        RUN create-group("SALES INCHARGE", f-list.in-sales).
                    END.
                    
                    RUN create-data.
                    groupby = f-list.in-sales.
                END.
            END.
            /*end*/
        END.
        ELSE IF sorttype = 1 THEN
        DO:
            FOR EACH f-list NO-LOCK BY f-list.room BY f-list.cdate:
                line1 = line1 + 1.
    
                IF line1 = 1 THEN
                DO:
                    groupby = f-list.room.
                    RUN create-group ("ROOM", groupby).
                END.
    
                IF f-list.room NE groupby THEN
                DO:
                    RUN create-subtotal.
                    RUN create-group ("ROOM", f-list.room).
                END.
    
                RUN create-data.
                groupby = f-list.room.
            END.
        END.
        ELSE
        DO:
            FOR EACH f-list NO-LOCK BY f-list.event BY f-list.cdate BY f-list.room:
                line1 = line1 + 1.
    
                IF line1 = 1 THEN
                DO:
                    groupby = f-list.event.
                    RUN create-group ("EVENT", groupby).
                END.
    
                IF f-list.event NE groupby THEN
                DO:
                    RUN create-subtotal.
                    RUN create-group ("EVENT", f-list.event).
                END.
    
                RUN create-data.
                groupby = f-list.event.
            END.
        END.
    
        FIND FIRST f-list NO-LOCK NO-ERROR.
        IF AVAILABLE f-list THEN
        DO:
            RUN create-subtotal.
        
            CREATE output-list.
            ASSIGN 
                output-list.flag = "TOTAL"
                output-list.bezeich = "T O T A L"
                output-list.pax = totpax
                output-list.rmrev = totrmrev
                output-list.fbrev = totfbrev
                output-list.othrev = totother
                output-list.totrev = totrev.
        END.
    END.
    ELSE
    DO:
        IF sorttype = 0 THEN /*By Sales*/
        DO:
            /*Naufal - Add Validation for group by sales incharge Horrison Bekasi*/
            IF disp-flag = 1 THEN
            DO:
                FOR EACH f-list NO-LOCK BY f-list.sales BY f-list.cdate BY f-list.room:
                    line1 = line1 + 1.
                    
                    IF line1 = 1 THEN
                    DO:
                        groupby = f-list.sales. /*NA - Add sales name*/
                        RUN create-group ("SALES ID", groupby).
                    END.
                
                    IF f-list.sales NE groupby THEN
                    DO:
                        RUN create-subtotal.
                        RUN create-group("SALES ID", f-list.sales). /*NA - Add sales name*/
                    END.

                    RUN create-data.
                    groupby = f-list.sales. /*NA - Add sales name*/
                END.
            END.
            ELSE IF disp-flag = 2 THEN
            DO:
                FOR EACH f-list NO-LOCK BY f-list.in-sales BY f-list.cdate BY f-list.room:
                    line1 = line1 + 1.
                    
                    IF line1 = 1 THEN
                    DO:
                        groupby = f-list.in-sales.
                        RUN create-group ("SALES INCHARGE", groupby).
                    END.
                
                    IF f-list.in-sales NE groupby THEN
                    DO:
                        RUN create-subtotal.
                        RUN create-group("SALES INCHARGE", f-list.in-sales).
                    END.
                
                    RUN create-data.
                    groupby = f-list.in-sales.
                END.
            END.
            /*end*/
        END.
        ELSE IF sorttype = 1 THEN
        DO:
            FOR EACH f-list NO-LOCK BY f-list.room BY f-list.cdate:
                line1 = line1 + 1.
    
                IF line1 = 1 THEN
                DO:
                    groupby = f-list.room.
                    RUN create-group ("ROOM", groupby).
                END.
    
                IF f-list.room NE groupby THEN
                DO:
                    RUN create-subtotal.
                    RUN create-group ("ROOM", f-list.room).
                END.
    
                RUN create-data.
                groupby = f-list.room.
            END.
        END.
        ELSE
        DO:
            FOR EACH f-list NO-LOCK BY f-list.event BY f-list.cdate BY f-list.room:
                line1 = line1 + 1.
    
                IF line1 = 1 THEN
                DO:
                    groupby = f-list.event.
                    RUN create-group ("EVENT", groupby).
                END.
    
                IF f-list.event NE groupby THEN
                DO:
                    RUN create-subtotal.
                    RUN create-group ("EVENT", f-list.event).
                END.
    
                RUN create-data.
                groupby = f-list.event.
            END.
        END.
    
        FIND FIRST f-list NO-LOCK NO-ERROR.
        IF AVAILABLE f-list THEN
        DO:
            RUN create-subtotal.
        
            CREATE output-list.
            ASSIGN 
                output-list.flag = "TOTAL"
                output-list.bezeich = "T O T A L"
                output-list.pax = totpax
                output-list.rmrev = totrmrev
                output-list.fbrev = totfbrev
                output-list.othrev = totother
                output-list.totrev = totrev.
        END.
    END.
END.

PROCEDURE create-group:
    DEFINE INPUT PARAMETER bezeich AS CHAR.
    DEFINE INPUT PARAMETER bezeich1 AS CHAR.

    CREATE output-list.
    output-list.flag = "GROUP".
    IF bezeich EQ "SALES ID" OR bezeich EQ "SALES INCHARGE" THEN
    DO:
        output-list.bezeich = bezeich1.
    END.
    ELSE
    DO:
        output-list.bezeich = bezeich + " : " + bezeich1.
    END.
END.

PROCEDURE create-data:
 /*MESSAGE STRING(f-list.rstat, "x(1)") VIEW-AS ALERT-BOX.*/
    CREATE output-list.
    ASSIGN 
        output-list.bezeich = f-list.bname
        output-list.room = f-list.room
        output-list.id = f-list.ID
        output-list.ba-event = f-list.EVENT
        output-list.datum = f-list.cDATE
        output-list.pax = f-list.pax
        output-list.rmrev = f-list.rmrev
        output-list.fbrev = f-list.fbrev
        output-list.othrev = f-list.otrev
        output-list.totrev = f-list.totrev
        output-list.resnr = f-list.resnr
        output-list.cp = f-list.cp
        output-list.rstat = f-list.rstat
        output-list.date-book = f-list.date-book
        output-list.in-sales = f-list.in-sales
        output-list.ev-time = f-list.ev-time.
    
    ASSIGN
        subpax   = subpax + f-list.pax
        subrmrev = subrmrev + f-list.rmrev
        subfbrev = subfbrev + f-list.fbrev
        subother = subother + f-list.otrev
        subrev   = subrev + f-list.totrev
        totpax   = totpax + f-list.pax
        totrmrev = totrmrev + f-list.rmrev
        totfbrev = totfbrev + f-list.fbrev
        totother = totother + f-list.otrev
        totrev   = totrev + f-list.totrev
    .
END.

PROCEDURE create-list:
    DEF VAR salesid     AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR salesid2    AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR roomDesc    AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR bname       AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR other-rev   AS DECIMAL INITIAL 0  NO-UNDO.
    DEF VAR fb-rev      AS DECIMAL INITIAL 0  NO-UNDO.
    DEF VAR in-sales    AS CHAR    INITIAL "" NO-UNDO. /*naufal - add incharge id*/
    DEF VAR in-sales1   AS CHAR.
    DEF VAR in-sales2   AS CHAR.

    DEFINE VARIABLE datum AS DATE NO-UNDO. /*FD*/
    DEFINE VARIABLE found-chr2 AS LOGICAL.
    DEFINE VARIABLE count-i AS INTEGER.
    DEFINE VARIABLE bq-resnr AS INTEGER.
    DEFINE VARIABLE bq-reslinnr AS INTEGER.
    
    FOR EACH f-list:
        DELETE f-list.
    END.
    
    IF NOT checklist THEN
    DO:
        DO datum = fdate TO tdate:
            FIND FIRST bk-func WHERE bk-func.datum = datum NO-LOCK NO-ERROR.
            IF AVAILABLE bk-func THEN
            DO:
              FOR EACH bk-func WHERE bk-func.datum /*GE fdate AND bk-func.datum LE tdate*/ = datum
                  AND bk-func.resstatus = 1 USE-INDEX datum_ix NO-LOCK,
                FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK
                BY bk-func.datum:
                
                fb-rev = 0.
                other-rev = 0.

                FIND FIRST room WHERE room.raum = bk-func.raeume[1] USE-INDEX raum-ix NO-LOCK NO-ERROR.
                IF AVAILABLE room THEN roomDesc = room.bezeich.
                ELSE roomDesc = "Not defined".
                
                FIND FIRST gast WHERE gast.gastnr = bk-veran.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gast THEN bname = gast.name + ", " + gast.vorname1 + " " 
                    + gast.anrede1 + gast.anredefirma.
                ELSE bname = "Not defined".
                /* FDL Comment
                FIND FIRST usr WHERE usr.nr = bk-veran.bediener-nr NO-LOCK NO-ERROR.
                IF AVAILABLE usr THEN
                DO:
                    salesid     = usr.userinit.
                    salesid2    = salesid + " - " + usr.username. /*NA - Add sales name*/
                END. 
                ELSE 
                DO: 
                    salesid     = "**".
                    salesid2    = "".
                END.
                
                FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                    bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                    other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                END.
                */
                /*FDL May 14, 2024 => Ticket #49764B*/
                FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                    bk-rart.veran-seite = bk-func.veran-seite NO-LOCK,
                    FIRST artikel WHERE artikel.artnr EQ bk-rart.veran-artnr
                    AND artikel.departement EQ bk-rart.departement NO-LOCK:

                    IF (artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 6) THEN
                    DO:
                        fb-rev = fb-rev + (bk-rart.preis * bk-rart.anzahl).
                    END.
                    ELSE IF artikel.umsatzart EQ 4 THEN other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                END.
                
                /*naufal - add sales incharge
                in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                in-sales2 = SUBSTR(in-sales1, 1, LENGTH(in-sales1) - 1).
                
                FIND FIRST usr WHERE usr.userinit EQ in-sales2 NO-LOCK NO-ERROR.
                IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                ELSE in-sales = "**".
                /*end*/
                */

                /*FDL May 14, 2024 => Ticket #49764B*/
                in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                DO count-i = 1 TO LENGTH(in-sales1):
                    IF SUBSTR(in-sales1,count-i,1) EQ CHR(2) THEN
                    DO:
                        found-chr2 = YES.
                        LEAVE.
                    END.
                END.
                IF found-chr2 THEN
                DO:
                    FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                    IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                    ELSE in-sales = "**".

                    FIND FIRST usr WHERE usr.userinit EQ ENTRY(2,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                    IF AVAILABLE usr THEN salesid2 = STRING(usr.userinit + " - " + usr.username).
                    ELSE salesid2 = "**".
                END.
                ELSE
                DO:
                    FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                    IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                    ELSE in-sales = "**".
                END.
                found-chr2 = NO.

                CREATE f-list.
                ASSIGN
                    f-list.bname = bname
                    f-list.room  = roomDesc
                    f-list.ID    = salesID
                    f-list.event = bk-func.zweck[1]
                    f-list.cdate = bk-func.datum
                    f-list.pax   = bk-func.rpersonen[1]
                    f-list.rmrev = bk-func.rpreis[1]
                    f-list.fbrev = (bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev
                    f-list.otrev = other-rev
                    f-list.totrev = bk-func.rpreis[1] + other-rev + fb-rev +
                        (bk-func.rpreis[7] * bk-func.rpersonen[1])
                    f-list.resnr = bk-func.veran-nr
                    f-list.cp    = bk-func.kontaktperson[1]
                    f-list.rstat = "F"
                    f-list.date-book = bk-func.auf_datum
                    f-list.in-sales = in-sales /*naufal - add sales incharge*/
                    f-list.sales = salesid2 /*NA - add booking salesname*/
                    f-list.ev-time = bk-func.uhrzeit
                    .                    
              END.  
            END.
            ELSE
            DO:
              /*FD September 21, 2020 --> get History Banquet Reservation Horizon Bekasi*/
              FOR EACH b-history WHERE b-history.datum /*GE fdate AND b-history.datum LE tdate*/ = datum
                  AND b-history.resstatus = 1 USE-INDEX resnr_ix NO-LOCK,
                  FIRST bk-veran WHERE bk-veran.veran-nr = b-history.veran-nr NO-LOCK
                  BY b-history.datum:
              
                  fb-rev = 0.
                  other-rev = 0.

                  FIND FIRST room WHERE room.raum = b-history.raeume[1] USE-INDEX raum-ix NO-LOCK NO-ERROR.
                  IF AVAILABLE room THEN roomDesc = room.bezeich.
                  ELSE roomDesc = "Not defined".
              
                  FIND FIRST gast WHERE gast.gastnr = bk-veran.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                  IF AVAILABLE gast THEN bname = gast.name + ", " + gast.vorname1 + " " 
                      + gast.anrede1 + gast.anredefirma.
                  ELSE bname = "Not defined".
              
                  /* FDL Comment
                  FIND FIRST usr WHERE usr.nr = bk-veran.bediener-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE usr THEN
                  DO:
                      salesid     = usr.userinit.
                      salesid2    = salesid + " - " + usr.username. /*NA - Add sales name*/
                  END. 
                  ELSE 
                  DO: 
                      salesid     = "**".
                      salesid2    = "".
                  END.
                  

                  FOR EACH bk-rart WHERE bk-rart.veran-nr = b-history.veran-nr AND
                      bk-rart.veran-seite = b-history.veran-seite NO-LOCK:
                      other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                  END.
                  */
                  /*FDL May 14, 2024 => Ticket #49764B*/
                  FOR EACH bk-rart WHERE bk-rart.veran-nr = b-history.veran-nr AND
                      bk-rart.veran-seite = b-history.veran-seite NO-LOCK,
                      FIRST artikel WHERE artikel.artnr EQ bk-rart.veran-artnr
                      AND artikel.departement EQ bk-rart.departement NO-LOCK:
                  
                      IF (artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 6) THEN
                      DO:
                          fb-rev = fb-rev + (bk-rart.preis * bk-rart.anzahl).
                      END.
                      ELSE IF artikel.umsatzart EQ 4 THEN other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                  END.
                   
                  /*naufal - add sales incharge
                  in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                  in-sales2 = SUBSTR(in-sales1, 1, LENGTH(in-sales1) - 1).
              
                  FIND FIRST usr WHERE usr.userinit EQ in-sales2 NO-LOCK NO-ERROR.
                  IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                  ELSE in-sales = "**".
                  /*end*/*/

                  /*FDL May 14, 2024 => Ticket #49764B*/
                  in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                  DO count-i = 1 TO LENGTH(in-sales1):
                      IF SUBSTR(in-sales1,count-i,1) EQ CHR(2) THEN
                      DO:
                          found-chr2 = YES.
                          LEAVE.
                      END.
                  END.
                  IF found-chr2 THEN
                  DO:
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                      ELSE in-sales = "**".
                  
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(2,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN salesid2 = STRING(usr.userinit + " - " + usr.username).
                      ELSE salesid2 = "**".
                  END.
                  ELSE
                  DO:
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                      ELSE in-sales = "**".
                  END.
                  found-chr2 = NO.
                 
                  CREATE f-list.
                  ASSIGN
                      f-list.bname = bname
                      f-list.room  = roomDesc
                      f-list.ID    = salesID
                      f-list.event = b-history.zweck[1]
                      f-list.cdate = b-history.datum
                      f-list.pax   = b-history.rpersonen[1]
                      f-list.rmrev = b-history.rpreis[1]
                      f-list.fbrev = (b-history.rpreis[7] * b-history.rpersonen[1]) + fb-rev
                      f-list.otrev = other-rev
                      f-list.totrev = b-history.rpreis[1] + other-rev + fb-rev +
                          (b-history.rpreis[7] * b-history.rpersonen[1])
                      f-list.resnr = b-history.veran-nr
                      f-list.cp    = b-history.kontaktperson[1]
                      f-list.rstat = "F"
                      f-list.date-book = b-history.auf_datum
                      f-list.in-sales = in-sales /*naufal - add sales incharge*/
                      f-list.sales = salesid2 /*NA - add booking salesname*/
                      f-list.ev-time = b-history.uhrzeit
                      .                  
              END.              
              /*End FD*/
            END.
        END.               
    END.
    ELSE
    DO:
        DO datum = fdate TO tdate:
            FIND FIRST bk-func WHERE bk-func.datum = datum NO-LOCK NO-ERROR.
            IF AVAILABLE bk-func THEN
            DO:
              FOR EACH bk-func WHERE bk-func.datum /*GE fdate AND bk-func.datum LE tdate*/ = datum
                  /*AND (bk-func.resstatus = 2 OR bk-func.resstatus = 3 OR bk-func.resstatus = 1)*/ AND bk-func.resstatus NE 9 USE-INDEX datum_ix NO-LOCK, /*ragung EE8478*/
                  FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK
                  BY bk-func.datum:
              
                  fb-rev = 0.
                  other-rev = 0.

                  FIND FIRST room WHERE room.raum = bk-func.raeume[1] USE-INDEX raum-ix NO-LOCK NO-ERROR.
                  IF AVAILABLE room THEN roomDesc = room.bezeich.
                  ELSE roomDesc = "Not defined".
              
                  FIND FIRST gast WHERE gast.gastnr = bk-veran.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                  IF AVAILABLE gast THEN bname = gast.name + ", " + gast.vorname1 + " " 
                      + gast.anrede1 + gast.anredefirma.
                  ELSE bname = "Not defined".
              
                  /* FDL Comment
                  FIND FIRST usr WHERE usr.nr = bk-veran.bediener-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE usr THEN 
                  DO:
                      salesid     = usr.userinit.
                      salesid2    = salesid + " - " + usr.username. /*NA - Add sales name*/
                  END. 
                  ELSE 
                  DO: 
                      salesid     = "**".
                      salesid2    = "".
                  END.
              
                  FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                      bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                      other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                  END.
                  */
                  /*FDL May 14, 2024 => Ticket #49764B*/
                  FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                      bk-rart.veran-seite = bk-func.veran-seite NO-LOCK,
                      FIRST artikel WHERE artikel.artnr EQ bk-rart.veran-artnr
                      AND artikel.departement EQ bk-rart.departement NO-LOCK:
                  
                      IF (artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 6) THEN
                      DO:
                          fb-rev = fb-rev + (bk-rart.preis * bk-rart.anzahl).
                      END.
                      ELSE IF artikel.umsatzart EQ 4 THEN other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                  END.

                  /*naufal - add sales incharge
                  in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                  in-sales2 = SUBSTR(in-sales1, 1, LENGTH(in-sales1) - 1).
              
                  FIND FIRST usr WHERE usr.userinit EQ in-sales2 NO-LOCK NO-ERROR.
                  IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                  ELSE in-sales = "**".
                  /*end*/
                  */

                  /*FDL May 14, 2024 => Ticket #49764B*/
                  in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                  DO count-i = 1 TO LENGTH(in-sales1):
                      IF SUBSTR(in-sales1,count-i,1) EQ CHR(2) THEN
                      DO:
                          found-chr2 = YES.
                          LEAVE.
                      END.
                  END.
                  IF found-chr2 THEN
                  DO:
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                      ELSE in-sales = "**".
                  
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(2,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN salesid2 = STRING(usr.userinit + " - " + usr.username).
                      ELSE salesid2 = "**".
                  END.
                  ELSE
                  DO:
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                      ELSE in-sales = "**".
                  END.
                  found-chr2 = NO.

                  IF bk-func.resstatus = 1 THEN
                      ASSIGN cob = "F".
                  ELSE IF bk-func.resstatus = 2 THEN
                      ASSIGN cob = "T".
                  ELSE
                      ASSIGN cob = "W".
              
                  CREATE f-list.
                  ASSIGN
                      f-list.rstat = cob
                      f-list.bname = bname
                      f-list.room  = roomDesc
                      f-list.ID    = salesID
                      f-list.event = bk-func.zweck[1]
                      f-list.cdate = bk-func.datum
                      f-list.pax   = bk-func.rpersonen[1]
                      f-list.rmrev = bk-func.rpreis[1]
                      f-list.fbrev = (bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev
                      f-list.otrev = other-rev
                      f-list.totrev = bk-func.rpreis[1] + other-rev + fb-rev +
                          (bk-func.rpreis[7] * bk-func.rpersonen[1])
                      f-list.resnr = bk-func.veran-nr
                      f-list.cp    = bk-func.kontaktperson[1]
                      f-list.date-book = bk-func.auf_datum
                      f-list.in-sales = in-sales  /*naufal - add sales incharge*/
                      f-list.sales = salesid2     /*NA - add booking salesname*/
                      f-list.ev-time = bk-func.uhrzeit
                      .                  
              END.
            END.
            ELSE
            DO:
              /*FD September 21, 2020 --> get History Banquet Reservation Horizon Bekasi*/
              FOR EACH b-history WHERE b-history.datum /*GE fdate AND b-history.datum LE tdate*/ = datum
                  AND b-history.resstatus NE 9 USE-INDEX resnr_ix NO-LOCK,                                    /* Rulita 140425 | Fixing ragung EE8478 from AND bk-func.resstatus NE 9 to AND b-history.resstatus NE 9 issue git 585  */
                  FIRST bk-veran WHERE bk-veran.veran-nr = b-history.veran-nr NO-LOCK
                  BY b-history.datum:
              
                  fb-rev = 0.
                  other-rev = 0.

                  FIND FIRST room WHERE room.raum = b-history.raeume[1] USE-INDEX raum-ix NO-LOCK NO-ERROR.
                  IF AVAILABLE room THEN roomDesc = room.bezeich.
                  ELSE roomDesc = "Not defined".
              
                  FIND FIRST gast WHERE gast.gastnr = bk-veran.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                  IF AVAILABLE gast THEN bname = gast.name + ", " + gast.vorname1 + " " 
                      + gast.anrede1 + gast.anredefirma.
                  ELSE bname = "Not defined".
              
                  /* FDL Comment
                  FIND FIRST usr WHERE usr.nr = bk-veran.bediener-nr NO-LOCK NO-ERROR.
                  IF AVAILABLE usr THEN 
                  DO:
                      salesid     = usr.userinit.
                      salesid2    = salesid + " - " + usr.username. /*NA - Add sales name*/
                  END. 
                  ELSE 
                  DO: 
                      salesid     = "**".
                      salesid2    = "".
                  END.
              
                  FOR EACH bk-rart WHERE bk-rart.veran-nr = b-history.veran-nr AND
                      bk-rart.veran-seite = b-history.veran-seite NO-LOCK:
                      other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                  END.
                  */
                  /*FDL May 14, 2024 => Ticket #49764B*/
                  FOR EACH bk-rart WHERE bk-rart.veran-nr = b-history.veran-nr AND
                      bk-rart.veran-seite = b-history.veran-seite NO-LOCK,
                      FIRST artikel WHERE artikel.artnr EQ bk-rart.veran-artnr
                      AND artikel.departement EQ bk-rart.departement NO-LOCK:
                  
                      IF (artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 6) THEN
                      DO:
                          fb-rev = fb-rev + (bk-rart.preis * bk-rart.anzahl).
                      END.
                      ELSE IF artikel.umsatzart EQ 4 THEN other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
                  END.

                  /*naufal - add sales incharge
                  in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                  in-sales2 = SUBSTR(in-sales1, 1, LENGTH(in-sales1) - 1).
              
                  FIND FIRST usr WHERE usr.userinit EQ in-sales2 NO-LOCK NO-ERROR.
                  IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                  ELSE in-sales = "**".
                  /*end*/
                  */

                  /*FDL May 14, 2024 => Ticket #49764B*/
                  in-sales1 = TRIM(bk-veran.payment-userinit[9]).
                  DO count-i = 1 TO LENGTH(in-sales1):
                      IF SUBSTR(in-sales1,count-i,1) EQ CHR(2) THEN
                      DO:
                          found-chr2 = YES.
                          LEAVE.
                      END.
                  END.
                  IF found-chr2 THEN
                  DO:
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                      ELSE in-sales = "**".
                  
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(2,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN salesid2 = STRING(usr.userinit + " - " + usr.username).
                      ELSE salesid2 = "**".
                  END.
                  ELSE
                  DO:
                      FIND FIRST usr WHERE usr.userinit EQ ENTRY(1,in-sales1,CHR(2)) NO-LOCK NO-ERROR.
                      IF AVAILABLE usr THEN in-sales = STRING(usr.userinit + " - " + usr.username).
                      ELSE in-sales = "**".
                  END.
                  found-chr2 = NO.

                  IF b-history.resstatus = 1 THEN
                      ASSIGN cob = "F".
                  ELSE IF b-history.resstatus = 2 THEN
                      ASSIGN cob = "T".
                  ELSE
                      ASSIGN cob = "W".
              
                  CREATE f-list.
                  ASSIGN
                      f-list.rstat = cob
                      f-list.bname = bname
                      f-list.room  = roomDesc
                      f-list.ID    = salesID
                      f-list.event = b-history.zweck[1]
                      f-list.cdate = b-history.datum
                      f-list.pax   = b-history.rpersonen[1]
                      f-list.rmrev = b-history.rpreis[1]
                      f-list.fbrev = (b-history.rpreis[7] * b-history.rpersonen[1]) + fb-rev
                      f-list.otrev = other-rev
                      f-list.totrev = b-history.rpreis[1] + other-rev + fb-rev +
                          (b-history.rpreis[7] * b-history.rpersonen[1])
                      f-list.resnr = b-history.veran-nr
                      f-list.cp    = b-history.kontaktperson[1]
                      f-list.date-book = b-history.auf_datum
                      f-list.in-sales = in-sales  /*naufal - add sales incharge*/
                      f-list.sales = salesid2     /*NA - add booking salesname*/
                      f-list.ev-time = b-history.uhrzeit
                      .
              END.       
              /*End FD*/
            END.
        END.                  
    END.
END.

PROCEDURE create-subtotal:
    CREATE output-list.
    ASSIGN
        output-list.flag = "LINE".

    CREATE output-list.
    ASSIGN
        output-list.flag    = "SUB"     
        output-list.bezeich = "Subtotal"
        output-list.pax     = subpax
        output-list.rmrev   = subrmrev
        output-list.fbrev   = subfbrev
        output-list.othrev  = subother
        output-list.totrev  = subrev.
        
    CREATE output-list.
         output-list.flag = "SPACE".
         

    ASSIGN
        subpax   = 0
        subrmrev = 0
        subfbrev = 0
        subother = 0
        subrev   = 0.
END.
