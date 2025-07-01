DEFINE TEMP-TABLE cust-list-detail
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR    
    FIELD gname             AS CHAR
    FIELD gesamtumsatz      AS CHAR
    FIELD logiernachte      AS CHAR  
    FIELD argtumsatz        AS CHAR 
    FIELD f-b-umsatz        AS CHAR 
    FIELD sonst-umsatz      AS CHAR 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS CHAR 
    FIELD ly-rev            AS CHAR 
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS CHAR 
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER
    FIELD count-room        AS CHAR
    FIELD rm-sharer         AS CHAR
    FIELD arrival           AS DATE
    FIELD depart            AS DATE.

DEFINE TEMP-TABLE b-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR    
    FIELD gname             AS CHAR
    FIELD gesamtumsatz      AS CHAR
    FIELD logiernachte      AS CHAR  
    FIELD argtumsatz        AS CHAR 
    FIELD f-b-umsatz        AS CHAR 
    FIELD sonst-umsatz      AS CHAR 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS CHAR 
    FIELD ly-rev            AS CHAR 
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS CHAR 
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER
    FIELD count-room        AS CHAR
    FIELD rm-sharer         AS CHAR
    FIELD arrival           AS DATE
    FIELD depart            AS DATE.

DEFINE INPUT PARAMETER cardtype             AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sort-type            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER tdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER check-ftd            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER currency             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER excl-other           AS LOGICAL NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER curr-sort2    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR b-list.


DEFINE BUFFER t-genstat FOR genstat.

DEFINE VARIABLE bfast-art   AS INTEGER  NO-UNDO. 
DEFINE VARIABLE lunch-art   AS INTEGER  NO-UNDO. 
DEFINE VARIABLE dinner-art  AS INTEGER  NO-UNDO. 
DEFINE VARIABLE lundin-art  AS INTEGER  NO-UNDO. 

DEFINE VAR service          AS DECIMAL INITIAL 0.
DEFINE VAR vat              AS DECIMAL INITIAL 0.


DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE end-date AS DATE.


DEFINE VARIABLE net-lodg    AS DECIMAL.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL.

DEFINE VARIABLE tot-breakfast    AS DECIMAL.
DEFINE VARIABLE tot-Lunch        AS DECIMAL.
DEFINE VARIABLE tot-dinner       AS DECIMAL.
DEFINE VARIABLE tot-Other        AS DECIMAL.
DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.
DEFINE VARIABLE curr-i           AS INT.
DEFINE VARIABLE i                AS INT.
DEFINE VARIABLE found            AS LOGICAL INIT NO.
DEFINE VARIABLE ly-fdate         AS DATE.
DEFINE VARIABLE ly-tdate         AS DATE.
DEFINE VARIABLE ci-date          AS DATE.
DEFINE VARIABLE pos              AS INTEGER INIT 0.
DEFINE VARIABLE curr-gastnr      AS INTEGER.
DEFINE VARIABLE curr-resnr       AS INTEGER.
DEFINE VARIABLE curr-reslinnr    AS INTEGER.
DEFINE VARIABLE curr-gname       AS CHAR.
DEFINE VARIABLE curr-gastnr2     AS INTEGER.

DEFINE VARIABLE t-logiernachte  AS DECIMAL.
DEFINE VARIABLE t-argtumsatz    AS DECIMAL.
DEFINE VARIABLE t-fb-umsatz     AS DECIMAL.
DEFINE VARIABLE t-sonst-umsatz  AS DECIMAL.
DEFINE VARIABLE t-ba-umsatz     AS DECIMAL.
DEFINE VARIABLE t-gesamtumsatz  AS DECIMAL.
DEFINE VARIABLE t-lyear         AS DECIMAL.
DEFINE VARIABLE t-nofrm         AS DECIMAL.

DEFINE VARIABLE tot-logiernachte  AS DECIMAL.
DEFINE VARIABLE tot-argtumsatz    AS DECIMAL.
DEFINE VARIABLE tot-fb-umsatz     AS DECIMAL.
DEFINE VARIABLE tot-sonst-umsatz  AS DECIMAL.
DEFINE VARIABLE tot-ba-umsatz     AS DECIMAL.
DEFINE VARIABLE tot-gesamtumsatz  AS DECIMAL.
DEFINE VARIABLE tot-stayno        AS DECIMAL.
DEFINE VARIABLE tot-lyear         AS DECIMAL.
DEFINE VARIABLE tot-nofrm         AS DECIMAL.

DEFINE VARIABLE gt-logiernachte  AS DECIMAL.
DEFINE VARIABLE gt-argtumsatz    AS DECIMAL.
DEFINE VARIABLE gt-fb-umsatz     AS DECIMAL.
DEFINE VARIABLE gt-sonst-umsatz  AS DECIMAL.
DEFINE VARIABLE gt-ba-umsatz     AS DECIMAL.
DEFINE VARIABLE gt-gesamtumsatz  AS DECIMAL.
DEFINE VARIABLE gt-stayno        AS DECIMAL.
DEFINE VARIABLE gt-lyear         AS DECIMAL.
DEFINE VARIABLE gt-nofrm         AS DECIMAL.

DEFINE VARIABLE curr-resnr1    AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-reslinnr1 AS INTEGER NO-UNDO.
DEFINE VARIABLE found1         AS LOGICAL NO-UNDO.
DEFINE VARIABLE loopj          AS INTEGER NO-UNDO.

DEFINE VARIABLE exratenr AS INTEGER NO-UNDO.
DEFINE VARIABLE exrate   AS DECIMAL NO-UNDO.

DEFINE BUFFER blist FOR cust-list-detail.
DEFINE BUFFER glist FOR guest.
DEFINE BUFFER bguest FOR guest.
DEFINE BUFFER clist FOR cust-list-detail.
DEFINE BUFFER bline FOR bill-line.
DEFINE BUFFER bbuf  FOR bill.

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

FOR EACH b-list:
    DELETE b-list.
END.

RUN create-detail.

ASSIGN
    tot-logiernachte   = 0
    tot-argtumsatz     = 0
    tot-fb-umsatz      = 0
    tot-sonst-umsatz   = 0
    tot-ba-umsatz      = 0
    tot-gesamtumsatz   = 0
    tot-stayno         = 0
    tot-lyear          = 0
    tot-nofrm          = 0
    gt-logiernachte    = 0
    gt-argtumsatz      = 0
    gt-fb-umsatz       = 0
    gt-sonst-umsatz    = 0
    gt-ba-umsatz       = 0
    gt-gesamtumsatz    = 0
    gt-lyear           = 0
    gt-nofrm           = 0.

CASE sort-type:
    WHEN 0 THEN DO: 
        FOR EACH cust-list-detail BY cust-list-detail.gastnr:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.


            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                /*IF tot-gesamtumsatz NE 0 THEN DO:*/
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                /*END.*/
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").


            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END.        
    END.
    WHEN 1 THEN DO: /*total revenue*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.gesamtumsatz DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).
            

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END.        
    END.
    WHEN 2 THEN DO:  /*room night*/

         FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.logiernachte DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            
            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 

    END.
    WHEN 3 THEN DO:  /*customer name*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.cust-name:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).
            

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 4 THEN DO:  /*Room Revenue*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.argtumsatz DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            
            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 

    END.
    WHEN 5 THEN DO:  /*FB Revenue*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.f-b-umsatz DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 

    END.
    WHEN 6 THEN DO:  /*Other Revenue*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.sonst-umsatz DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 7 THEN DO:  /*City*/
          FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.wohnort DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 8 THEN DO:  /*zip*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.plz DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 

    END.
    WHEN 9 THEN DO: /*country*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.land DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 10 THEN DO: /*stayno*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.resnr DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 

    END.
    WHEN 11 THEN DO: /*ly-rev*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.ly-rev DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 12 THEN DO: /*count-room*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.count-room DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 13 THEN DO: /*count-room*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.region:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.
    WHEN 14 THEN DO: /*banquet*/
        FOR EACH cust-list-detail BY cust-list-detail.gastnr BY cust-list-detail.ba-umsatz DESC:
            FIND FIRST guest WHERE guest.gastnr = cust-list-detail.gastnr NO-LOCK NO-ERROR.
            IF curr-gastnr = 0 THEN
            DO:
                CREATE b-list.
                ASSIGN b-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                          + guest.anredefirm).  
            END.

            IF curr-gastnr NE 0 AND curr-gastnr NE cust-list-detail.gastnr THEN DO:
                IF tot-gesamtumsatz NE 0 THEN DO:
                    CREATE b-list.
                    ASSIGN  
                        b-list.cust-name    = "T O T A L"  
                        b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                        b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                        b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                        b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                        b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99")
    
                        tot-logiernachte   = 0
                        tot-argtumsatz     = 0
                        tot-fb-umsatz      = 0
                        tot-sonst-umsatz   = 0
                        tot-ba-umsatz      = 0
                        tot-gesamtumsatz   = 0
                        tot-stayno         = 0
                        tot-lyear          = 0
                        tot-nofrm          = 0.
                END.
                
                CREATE b-list.

                CREATE b-list.
                ASSIGN b-list.cust-name    = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                             + guest.anredefirm).       
            END.
            
            IF cust-list-detail.resnr NE "" THEN
                ASSIGN
                    cust-list-detail.stayno = STRING(NUM-ENTRIES(cust-list-detail.resnr,";") - 1, ">>>,>>9")
                    tot-stayno              = tot-stayno + INTEGER(cust-list-detail.stayno)
                    gt-stayno               = gt-stayno + INTEGER(cust-list-detail.stayno).

            CREATE b-list.
            BUFFER-COPY cust-list-detail TO b-list.
            IF b-list.ly-rev = " " THEN ASSIGN b-list.ly-rev = STRING(0, "->>>,>>>,>>>,>>9.99").
            IF b-list.ba-umsatz = " " THEN ASSIGN b-list.ba-umsatz = STRING(0, "->>>,>>>,>>>,>>9.99").

            ASSIGN
                tot-logiernachte   = tot-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                tot-argtumsatz     = tot-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                tot-fb-umsatz      = tot-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                tot-sonst-umsatz   = tot-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                tot-ba-umsatz      = tot-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                tot-gesamtumsatz   = tot-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                tot-lyear          = tot-lyear         + DECIMAL(cust-list-detail.ly-rev)
                tot-nofrm          = tot-nofrm         + DECIMAL(cust-list-detail.count-room)
                 
                gt-logiernachte   = gt-logiernachte  + DECIMAL(cust-list-detail.logiernachte)
                gt-argtumsatz     = gt-argtumsatz    + DECIMAL(cust-list-detail.argtumsatz)
                gt-fb-umsatz      = gt-fb-umsatz     + DECIMAL(cust-list-detail.f-b-umsatz)
                gt-sonst-umsatz   = gt-sonst-umsatz  + DECIMAL(cust-list-detail.sonst-umsatz)
                gt-ba-umsatz      = gt-ba-umsatz     + DECIMAL(cust-list-detail.ba-umsatz)
                gt-gesamtumsatz   = gt-gesamtumsatz  + DECIMAL(cust-list-detail.gesamtumsatz)
                gt-lyear          = gt-lyear         + DECIMAL(cust-list-detail.ly-rev)
                gt-nofrm          = gt-nofrm         + DECIMAL(cust-list-detail.count-room)
                
                curr-gastnr       = cust-list-detail.gastnr.
            
        END.
        IF tot-gesamtumsatz NE 0 THEN DO:
             CREATE b-list.
             ASSIGN  
                b-list.cust-name    = "T O T A L"  
                b-list.f-b-umsatz   = STRING(tot-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.sonst-umsatz = STRING(tot-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.argtumsatz   = STRING(tot-argtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.gesamtumsatz = STRING(tot-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b-list.logiernachte = STRING(tot-logiernachte, ">>>,>>9")
                b-list.ba-umsatz    = STRING(tot-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                b-list.stayno       = STRING(tot-stayno, ">>>,>>9")
                b-list.count-room   = STRING(tot-nofrm, ">>,>>>,>>>,>>9")
                b-list.ly-rev       = STRING(tot-lyear, "->>>,>>>,>>>,>>9.99").
        END.

        IF gt-gesamtumsatz NE 0 THEN DO:
            CREATE b-list.
            ASSIGN  
                  b-list.cust-name    = "G R A N D  T O T A L"  
                  b-list.f-b-umsatz   = STRING(gt-fb-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.sonst-umsatz = STRING(gt-sonst-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.argtumsatz   = STRING(gt-argtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.gesamtumsatz = STRING(gt-gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.logiernachte = STRING(gt-logiernachte, ">>>,>>9")
                  b-list.ba-umsatz    = STRING(gt-ba-umsatz, "->>>,>>>,>>>,>>9.99")
                  b-list.stayno       = STRING(gt-stayno, ">>>,>>9")
                  b-list.count-room   = STRING(gt-nofrm, ">>,>>>,>>>,>>9")
                  b-list.ly-rev       = STRING(gt-lyear, "->>>,>>>,>>>,>>9.99").
        END. 
    END.

END CASE.


PROCEDURE create-detail:
    IF currency NE "" THEN DO:
        FIND FIRST waehrung WHERE waehrung.wabkurz = currency NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN 
            ASSIGN 
                exratenr = waehrung.waehrungsnr
                exrate   = waehrung.ankauf.
    END.

    IF cardtype = 3 THEN DO:
        IF NOT check-ftd THEN
        DO: 
            FOR EACH genstat WHERE genstat.segmentcode NE 0 
                AND genstat.nationnr NE 0
                AND genstat.zinr NE ""
                AND genstat.res-logic[2] EQ YES,
                FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK 
                BY genstat.gastnr BY guest.land BY genstat.resnr:
    
                
               FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
               FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                    /*AND cust-list-detail.resno = genstat.resnr*/
                    AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
               IF NOT AVAILABLE cust-list-detail THEN DO:
                    CREATE cust-list-detail.
                    ASSIGN cust-list-detail.gastnr     = genstat.gastnr 
                           cust-list-detail.resno      = genstat.resnr
                           cust-list-detail.reslinnr   = genstat.res-int[1]
                           cust-list-detail.gname      = bguest.NAME
                           cust-list-detail.arrival    = genstat.res-date[1]
                           cust-list-detail.depart     = genstat.res-date[2].
    
                    FIND FIRST glist WHERE glist.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE glist THEN DO:
                        ASSIGN cust-list-detail.cust-name  = glist.NAME + "," + glist.anredefirma + " " + glist.vorname1
                               cust-list-detail.plz        = glist.plz 
                               cust-list-detail.land       = glist.land
                               cust-list-detail.sales-id   = glist.phonetik3
                               cust-list-detail.wohnort    = glist.wohnort.
    
                        FIND FIRST nation WHERE nation.kurzbez = glist.land NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN
                        DO:
                            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                            IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                        END.
                        ELSE cust-list-detail.region = "UNKOWN".  
                        
                        IF cust-list-detail.sales-id = "" THEN
                            ASSIGN cust-list-detail.sales-id   = guest.phonetik3.

                    END.                
                    ELSE DO: 
                        ASSIGN 
                            cust-list-detail.cust-name  = guest.NAME + "," + guest.anredefirma + " " + guest.vorname1
                            cust-list-detail.plz        = guest.plz 
                            cust-list-detail.land       = guest.land
                            cust-list-detail.sales-id   = guest.phonetik3
                            cust-list-detail.wohnort    = guest.wohnort.   
    
                        FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN
                        DO:
                            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                            IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                        END.
                        ELSE cust-list-detail.region = "UNKOWN".                   
                    END.                
                END.
    
                ASSIGN found1 = NO.
                FIND FIRST clist WHERE clist.gastnr = genstat.gastnr
                    AND clist.gname = bguest.NAME NO-LOCK NO-ERROR.
                IF AVAILABLE clist THEN DO:
                    IF clist.resnr NE " "  THEN DO:
                        DO loopj = 1 TO NUM-ENTRIES(clist.resnr, ";"):
                            IF ENTRY(loopj, clist.resnr, ";") NE " " THEN DO:
                                IF INT(ENTRY(loopj, clist.resnr, ";")) = genstat.resnr THEN DO:
                                    ASSIGN found1 = YES.
                                    LEAVE.
                                END.
                            END.
                        END.
                        IF NOT found1 THEN
                            ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".    
                    END.
                    ELSE IF clist.resnr = " "  THEN ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".                     
                END.
    
                /*
                /*Revenue from outlet*/
                FIND FIRST guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
                    AND guest-queasy.date1 = genstat.datum
                    AND guest-queasy.number2 = genstat.resnr 
                    AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE guest-queasy:
                    ASSIGN
                        cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").
    
                    FIND NEXT guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
                        AND guest-queasy.date1 = genstat.datum
                        AND guest-queasy.number2 = genstat.resnr 
                        AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
                END.
    
                /*Revenue from other*/
                FIND FIRST bill-line WHERE bill-line.massnr = genstat.resnr
                    AND bill-line.billin-nr = genstat.res-int[1]
                    AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE bill-line:
                    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                        AND artikel.departement = bill-line.departement 
                        AND artikel.artart = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN 
                        ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99").
    
                    FIND NEXT bill-line WHERE bill-line.massnr = genstat.resnr
                        AND bill-line.billin-nr = genstat.res-int[1]
                        AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
                END.*/
                
                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                         ASSIGN
                           cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                           cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (genstat.res-deci[5] / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                           cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + (genstat.logis / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((genstat.logis + genstat.res-deci[2] 
                                                           + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                           cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + (genstat.res-deci[7] / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + genstat.res-deci[5], "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + genstat.logis + genstat.res-deci[2] 
                                                       + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5] , "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + genstat.res-deci[7], "->>>,>>>,>>>,>>9.99").
    
                IF genstat.resstatus NE 13 THEN 
                      ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) + 1, ">>>,>>9").
                ELSE ASSIGN cust-list-detail.rm-sharer = "*".
    
                /*Revenue from other*/
                IF curr-resnr1 NE genstat.resnr OR curr-reslinnr1 NE genstat.res-int[1] THEN DO:
                    ASSIGN
                        curr-resnr1 = genstat.resnr 
                        curr-reslinnr1 = genstat.res-int[1].
    
                    IF genstat.resstatus = 6 THEN DO:
                        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN
                            ASSIGN cust-list-detail.count-room = STRING(INTEGER(cust-list-detail.count-room) + res-line.zimmeranz, ">>,>>>,>>>,>>9"). 
                    END.
                    
                    IF excl-other = NO THEN DO:
                        FOR EACH bill WHERE bill.resnr = genstat.resnr 
                            AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
    
                            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                                AND bill-line.bill-datum = genstat.datum NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                    AND artikel.departement = bill-line.departement 
                                    AND artikel.artart = 0 NO-LOCK :
        
                                IF currency NE " " THEN DO:
                                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                    IF AVAILABLE exrate THEN 
                                            ASSIGN 
                                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                                END.
                                ELSE
                                    ASSIGN 
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                            END.

                             /*add bill
                            FIND FIRST bbuf WHERE bbuf.resnr = genstat.resnr 
                                AND bbuf.parent-nr = genstat.res-int[1]
                                AND bbuf.reslinnr NE genstat.res-int[1] NO-LOCK NO-ERROR.
                            IF AVAILABLE bbuf THEN DO:
                                FOR EACH bbuf WHERE bbuf.resnr = genstat.resnr 
                                    AND bbuf.parent-nr = genstat.res-int[1]
                                    AND bbuf.reslinnr NE genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
                
                                    FOR EACH bline WHERE bline.rechnr = bbuf.rechnr
                                        /*AND bline.bill-datum = genstat.datum*/ NO-LOCK,
                                        FIRST artikel WHERE artikel.artnr = bline.artnr 
                                            AND artikel.departement = bline.departement 
                                            AND artikel.artart = 0 NO-LOCK:
            
                                        IF currency NE " " THEN DO:
                                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                            IF AVAILABLE exrate THEN 
                                                    ASSIGN 
                                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                                        END.
                                        ELSE
                                            ASSIGN 
                                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99")
                                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99").
                                    END.
                                END.
                            END.*/
                        END.
                    END.
                    
        
                    /*FIND FIRST bill WHERE bill.resnr = genstat.resnr 
                        AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                END.
        
                /*IF AVAILABLE bill THEN DO:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = genstat.datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :

                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                    ASSIGN 
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                        END.
                        ELSE
                            ASSIGN 
                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                    END.
                END.   */     
            END.
            
            IF excl-other = NO THEN DO:
                /*Revenue from outlet*/
                FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
                    AND guest-queasy.date1 GE fdate
                    AND guest-queasy.date1 LE tdate NO-LOCK :
              
                    FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                        AND genstat.res-int[1] = guest-queasy.number3 
                        AND genstat.datum = guest-queasy.date1
                        AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
                    IF AVAILABLE genstat THEN DO:
                        FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                        FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                            /*AND cust-list-detail.resno = genstat.resnr*/
                            AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
                        IF AVAILABLE cust-list-detail THEN DO:
                            IF currency NE " " THEN DO:
                                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                IF AVAILABLE exrate THEN 
                                    ASSIGN
                                        cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (guest-queasy.deci3 / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((guest-queasy.deci1 + guest-queasy.deci2
                                                                        + guest-queasy.deci3) / exrate.betrag), "->>>,>>>,>>>,>>9.99").      
                            END.
                            ELSE
                                ASSIGN
                                    cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + guest-queasy.deci1 + guest-queasy.deci2
                                                                    + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").     
                        END.
                    END.                            
                END.
            END.
            
        END.
        ELSE RUN cr-ftd1.
    
        IF tdate NE ? AND tdate GE ci-date AND check-ftd THEN
           RUN create-forecast1.

    END.
    ELSE DO:
        IF NOT check-ftd THEN
        DO: 
            FOR EACH genstat WHERE genstat.segmentcode NE 0 
                AND genstat.nationnr NE 0
                AND genstat.zinr NE ""
                AND genstat.res-logic[2] EQ YES,
                FIRST guest WHERE guest.gastnr = genstat.gastnr
                AND guest.karteityp = cardtype NO-LOCK 
                BY genstat.gastnr BY guest.land BY genstat.resnr:
    
                
               FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
               FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                    /*AND cust-list-detail.resno = genstat.resnr*/
                    AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
               IF NOT AVAILABLE cust-list-detail THEN DO:
                    CREATE cust-list-detail.
                    ASSIGN cust-list-detail.gastnr     = genstat.gastnr 
                           cust-list-detail.resno      = genstat.resnr
                           cust-list-detail.reslinnr   = genstat.res-int[1]
                           cust-list-detail.gname      = bguest.NAME.
    
                    FIND FIRST glist WHERE glist.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE glist THEN DO:
                        ASSIGN cust-list-detail.cust-name  = glist.NAME + "," + glist.anredefirma + " " + glist.vorname1
                               cust-list-detail.plz        = glist.plz 
                               cust-list-detail.land       = glist.land
                               cust-list-detail.sales-id   = glist.phonetik3
                               cust-list-detail.wohnort    = glist.wohnort.
    
                        FIND FIRST nation WHERE nation.kurzbez = glist.land NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN
                        DO:
                            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                            IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                        END.
                        ELSE cust-list-detail.region = "UNKOWN".       

                        IF cust-list-detail.sales-id = "" THEN
                            ASSIGN cust-list-detail.sales-id   = guest.phonetik3.

                    END.                
                    ELSE DO: 
                        ASSIGN 
                            cust-list-detail.cust-name  = guest.NAME + "," + guest.anredefirma + " " + guest.vorname1
                            cust-list-detail.plz        = guest.plz 
                            cust-list-detail.land       = guest.land
                            cust-list-detail.sales-id   = guest.phonetik3
                            cust-list-detail.wohnort    = guest.wohnort.   
    
                        FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN
                        DO:
                            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                            IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                        END.
                        ELSE cust-list-detail.region = "UNKOWN".                   
                    END.                
                END.
    
                ASSIGN found1 = NO.
                FIND FIRST clist WHERE clist.gastnr = genstat.gastnr
                    AND clist.gname = bguest.NAME NO-LOCK NO-ERROR.
                IF AVAILABLE clist THEN DO:
                    IF clist.resnr NE " "  THEN DO:
                        DO loopj = 1 TO NUM-ENTRIES(clist.resnr, ";"):
                            IF ENTRY(loopj, clist.resnr, ";") NE " " THEN DO:
                                IF INT(ENTRY(loopj, clist.resnr, ";")) = genstat.resnr THEN DO:
                                    ASSIGN found1 = YES.
                                    LEAVE.
                                END.
                            END.
                        END.
                        IF NOT found1 THEN
                            ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".    
                    END.
                    ELSE IF clist.resnr = " "  THEN ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".                     
                END.
    
                /*
                /*Revenue from outlet*/
                FIND FIRST guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
                    AND guest-queasy.date1 = genstat.datum
                    AND guest-queasy.number2 = genstat.resnr 
                    AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE guest-queasy:
                    ASSIGN
                        cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").
    
                    FIND NEXT guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
                        AND guest-queasy.date1 = genstat.datum
                        AND guest-queasy.number2 = genstat.resnr 
                        AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
                END.
    
                /*Revenue from other*/
                FIND FIRST bill-line WHERE bill-line.massnr = genstat.resnr
                    AND bill-line.billin-nr = genstat.res-int[1]
                    AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE bill-line:
                    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                        AND artikel.departement = bill-line.departement 
                        AND artikel.artart = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN 
                        ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99").
    
                    FIND NEXT bill-line WHERE bill-line.massnr = genstat.resnr
                        AND bill-line.billin-nr = genstat.res-int[1]
                        AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
                END.*/

                IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                            ASSIGN
                               cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                               cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (genstat.res-deci[5] / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                               cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + (genstat.logis / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                               cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((genstat.logis + genstat.res-deci[2] 
                                                               + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                               cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + (genstat.res-deci[7] / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + genstat.res-deci[5], "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + genstat.logis + genstat.res-deci[2] 
                                                       + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5] , "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + genstat.res-deci[7], "->>>,>>>,>>>,>>9.99").
    
                IF genstat.resstatus NE 13 THEN 
                      ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) + 1, ">>>,>>9").
                ELSE ASSIGN cust-list-detail.rm-sharer = "*".
                
                /*Revenue from other*/
                IF curr-resnr1 NE genstat.resnr OR curr-reslinnr1 NE genstat.res-int[1] THEN DO:
                    ASSIGN
                        curr-resnr1 = genstat.resnr 
                        curr-reslinnr1 = genstat.res-int[1].
    
                    IF genstat.resstatus = 6 THEN DO:
                        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN
                            ASSIGN cust-list-detail.count-room = STRING(INTEGER(cust-list-detail.count-room) + res-line.zimmeranz, ">>,>>>,>>>,>>9"). 
                    END.

                    IF excl-other = NO THEN DO:
                        /*FIND FIRST bill WHERE bill.resnr = genstat.resnr 
                            AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                        FOR EACH bill WHERE bill.resnr = genstat.resnr 
                            AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
    
                            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                                AND bill-line.bill-datum = genstat.datum NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                    AND artikel.departement = bill-line.departement 
                                    AND artikel.artart = 0 NO-LOCK :
        
                                IF currency NE " " THEN DO:
                                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                    IF AVAILABLE exrate THEN 
                                            ASSIGN 
                                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                                END.
                                ELSE
                                    ASSIGN 
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                            END.

                             /*add bill
                            FIND FIRST bbuf WHERE bbuf.resnr = genstat.resnr 
                                AND bbuf.parent-nr = genstat.res-int[1]
                                AND bbuf.reslinnr NE genstat.res-int[1] NO-LOCK NO-ERROR.
                            IF AVAILABLE bbuf THEN DO:
                                FOR EACH bbuf WHERE bbuf.resnr = genstat.resnr 
                                    AND bbuf.parent-nr = genstat.res-int[1]
                                    AND bbuf.reslinnr NE genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
                
                                    FOR EACH bline WHERE bline.rechnr = bbuf.rechnr
                                        /*AND bline.bill-datum = genstat.datum*/ NO-LOCK,
                                        FIRST artikel WHERE artikel.artnr = bline.artnr 
                                            AND artikel.departement = bline.departement 
                                            AND artikel.artart = 0 NO-LOCK:
            
                                        IF currency NE " " THEN DO:
                                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                            IF AVAILABLE exrate THEN 
                                                    ASSIGN 
                                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                                        END.
                                        ELSE
                                            ASSIGN 
                                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99")
                                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99").
                                    END.
                                END.
                            END.*/
                        END.
                    END.
                    
                END.
        
                /*IF AVAILABLE bill THEN DO:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = genstat.datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                 ASSIGN 
                                    cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                        END.
                        ELSE
                            ASSIGN 
                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                    END.
                END.*/        
            END.
            
            IF excl-other = NO THEN DO:
                /*Revenue from outlet*/
                FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
                    AND guest-queasy.date1 GE fdate
                    AND guest-queasy.date1 LE tdate NO-LOCK :
              
                    FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                        AND genstat.res-int[1] = guest-queasy.number3 
                        AND genstat.datum = guest-queasy.date1
                        AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
                    IF AVAILABLE genstat THEN DO:
                        FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                        FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                            /*AND cust-list-detail.resno = genstat.resnr*/
                            AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
                        IF AVAILABLE cust-list-detail THEN DO:
                            IF currency NE " " THEN DO:
                                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                IF AVAILABLE exrate THEN 
                                    ASSIGN
                                        cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (guest-queasy.deci3 / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((guest-queasy.deci1 + guest-queasy.deci2
                                                                        + guest-queasy.deci3) / exrate.betrag), "->>>,>>>,>>>,>>9.99").      
                            END.
                            ELSE
                                ASSIGN
                                    cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + guest-queasy.deci1 + guest-queasy.deci2
                                                                    + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").      
                        END.                        
                    END.                            
                END.
            END.           
        END.
        ELSE RUN cr-ftd.
    
        IF tdate NE ? AND tdate GE ci-date AND check-ftd THEN
           RUN create-forecast.

    END.
    
END.

PROCEDURE cr-ftd:
  DEFINE VARIABLE t-argtumsatz  AS INT.
  DEFINE VARIABLE rate          AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE frate         AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE rmnite        AS INTEGER  NO-UNDO INIT 0.
  DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
  DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.
  DEFINE VARIABLE loopi         AS INTEGER NO-UNDO.
  DEFINE VARIABLE found         AS LOGICAL NO-UNDO.

  
  DEFINE BUFFER clist FOR cust-list-detail.
  FOR EACH genstat WHERE 
      genstat.datum GE fdate
      AND genstat.datum LE tdate
      /*AND genstat.resstatus NE 13*/
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES,
      FIRST guest WHERE guest.gastnr = genstat.gastnr 
      AND guest.karteityp = cardtype NO-LOCK 
      BY genstat.gastnr BY genstat.resnr BY genstat.res-int[1] BY guest.land:
       FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
       FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
            /*AND cust-list-detail.resno = genstat.resnr*/
            AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
       IF NOT AVAILABLE cust-list-detail THEN DO:
            CREATE cust-list-detail.
            ASSIGN cust-list-detail.gastnr     = genstat.gastnr 
                   cust-list-detail.resno      = genstat.resnr
                   cust-list-detail.reslinnr   = genstat.res-int[1]
                   cust-list-detail.gname      = bguest.NAME
                   cust-list-detail.arrival    = genstat.res-date[1]
                   cust-list-detail.depart     = genstat.res-date[2].

            FIND FIRST glist WHERE glist.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            IF AVAILABLE glist THEN DO:
                ASSIGN cust-list-detail.cust-name  = glist.NAME + "," + glist.anredefirma + " " + glist.vorname1
                       cust-list-detail.plz        = glist.plz 
                       cust-list-detail.land       = glist.land
                       cust-list-detail.sales-id   = glist.phonetik3
                       cust-list-detail.wohnort    = glist.wohnort.

                FIND FIRST nation WHERE nation.kurzbez = glist.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                END.
                ELSE cust-list-detail.region = "UNKOWN".        

                IF cust-list-detail.sales-id = "" THEN
                            ASSIGN cust-list-detail.sales-id   = guest.phonetik3.
            END.                
            ELSE DO: 
                ASSIGN 
                    cust-list-detail.cust-name  = guest.NAME + "," + guest.anredefirma + " " + guest.vorname1
                    cust-list-detail.plz        = guest.plz 
                    cust-list-detail.land       = guest.land
                    cust-list-detail.sales-id   = guest.phonetik3
                    cust-list-detail.wohnort    = guest.wohnort.   

                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                END.
                ELSE cust-list-detail.region = "UNKOWN".                   
            END.                
        END.

        
        ASSIGN found = NO.
        FIND FIRST clist WHERE clist.gastnr = genstat.gastnr AND clist.gname = bguest.NAME NO-LOCK NO-ERROR.
        IF AVAILABLE clist THEN DO:
            IF clist.resnr NE " "  THEN DO:
                DO loopi = 1 TO NUM-ENTRIES(clist.resnr, ";"):
                    IF ENTRY(loopi, clist.resnr, ";") NE " " THEN DO:
                        IF INT(ENTRY(loopi, clist.resnr, ";")) = genstat.resnr THEN DO:
                            ASSIGN found = YES.
                            LEAVE.
                        END.
                    END.
                END.
                IF NOT found THEN
                    ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".    
            END.
            ELSE IF clist.resnr = " "  THEN ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".                     
        END.
        
        /*
        /*Revenue from outlet*/
        FIND FIRST guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
            AND guest-queasy.date1 = genstat.datum
            AND guest-queasy.number2 = genstat.resnr AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest-queasy:
            ASSIGN
                cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").

            FIND NEXT guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
                AND guest-queasy.date1 = genstat.datum
                AND guest-queasy.number2 = genstat.resnr AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
        END.

        /*Revenue from other*/
        FIND FIRST bill-line WHERE bill-line.massnr = genstat.resnr
            AND bill-line.billin-nr = genstat.res-int[1]
            AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE bill-line:
            FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                AND artikel.departement = bill-line.departement 
                AND artikel.artart = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN 
                ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99").

            FIND NEXT bill-line WHERE bill-line.massnr = genstat.resnr
                AND bill-line.billin-nr = genstat.res-int[1]
                AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
        END.*/

        IF currency NE " " THEN DO:
            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
            IF AVAILABLE exrate THEN 
                ASSIGN
                   cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                   cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (genstat.res-deci[5] / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                   cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + (genstat.logis / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((genstat.logis + genstat.res-deci[2] 
                                                   + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                   cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + (genstat.res-deci[7] / exrate.betrag), "->>>,>>>,>>>,>>9.99").
        END.
        ELSE
            ASSIGN
               cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]), "->>>,>>>,>>>,>>9.99")
               cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + genstat.res-deci[5], "->>>,>>>,>>>,>>9.99")
               cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
               cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + genstat.logis + genstat.res-deci[2] 
                                               + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5] , "->>>,>>>,>>>,>>9.99")
               cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + genstat.res-deci[7], "->>>,>>>,>>>,>>9.99").
        
        IF genstat.resstatus NE 13 THEN 
              ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) + 1, ">>>,>>9").
        ELSE ASSIGN cust-list-detail.rm-sharer = "*".
        
        /*Revenue from other*/
        IF curr-resnr NE genstat.resnr OR curr-reslinnr NE genstat.res-int[1] THEN DO:
            ASSIGN
                curr-resnr = genstat.resnr 
                curr-reslinnr = genstat.res-int[1].

            IF genstat.resstatus = 6 THEN DO:
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                    ASSIGN cust-list-detail.count-room = STRING(INTEGER(cust-list-detail.count-room) + res-line.zimmeranz, ">>,>>>,>>>,>>9"). 
            END.
            
            IF excl-other = NO THEN DO:
                /*FIND FIRST bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                FOR EACH bill WHERE bill.resnr = genstat.resnr  /*bill utama*/
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = genstat.datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
    
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                    ASSIGN 
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                        END.
                        ELSE
                            ASSIGN 
                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                    END.
    
                     /*add bill
                    FIND FIRST bbuf WHERE bbuf.resnr = genstat.resnr 
                        AND bbuf.parent-nr = genstat.res-int[1]
                        AND bbuf.reslinnr NE genstat.res-int[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE bbuf THEN DO:
                        FOR EACH bbuf WHERE bbuf.resnr = genstat.resnr 
                            AND bbuf.parent-nr = genstat.res-int[1]
                            AND bbuf.reslinnr NE genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
        
                            FOR EACH bline WHERE bline.rechnr = bbuf.rechnr
                                /*AND bline.bill-datum = genstat.datum*/ NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bline.artnr 
                                    AND artikel.departement = bline.departement 
                                    AND artikel.artart = 0 NO-LOCK:
    
                                IF currency NE " " THEN DO:
                                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                    IF AVAILABLE exrate THEN 
                                            ASSIGN 
                                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                                END.
                                ELSE
                                    ASSIGN 
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99").
                            END.
                        END.
                    END. */          
                END.
            END.                                  
        END.

        /*
        IF AVAILABLE bill THEN DO:
            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                AND bill-line.bill-datum = genstat.datum NO-LOCK,
                FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                    AND artikel.artart = 0 NO-LOCK :
                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                        ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                               cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE
                    ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
            END.
        END.        */
  END.

  IF excl-other = NO THEN DO:
    /*Revenue from outlet*/
      FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK BY guest-queasy.number2:
      
            FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                AND genstat.res-int[1] = guest-queasy.number3 
                AND genstat.datum = guest-queasy.date1
                AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
            IF AVAILABLE genstat THEN DO:
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                    AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.            
                IF AVAILABLE cust-list-detail THEN DO:
                    IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                                ASSIGN
                                    cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (guest-queasy.deci3 / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                    cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((guest-queasy.deci1 + guest-queasy.deci2
                                                                    + guest-queasy.deci3) / exrate.betrag), "->>>,>>>,>>>,>>9.99").  
                    END.
                    ELSE
                        ASSIGN
                            cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + guest-queasy.deci1 + guest-queasy.deci2
                                                            + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").            
                END.
            END.
      END.
  END.

  
END.

PROCEDURE create-forecast:
    DEFINE VARIABLE do-it   AS LOGICAL INIT YES.
    DEFINE VARIABLE datum   AS DATE. 
    DEFINE VARIABLE datum1  AS DATE. 
    DEFINE VARIABLE datum2  AS DATE. 
    DEFINE VARIABLE d2      AS DATE.
    DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.
    DEFINE VARIABLE found         AS LOGICAL NO-UNDO.
    DEFINE VARIABLE loopi         AS INTEGER NO-UNDO.
    DEFINE VARIABLE count-rm      AS INTEGER NO-UNDO.

    IF fdate NE ci-date AND fdate LT ci-date THEN fdate = ci-date.
    datum1 = fdate. 
    IF tdate LT (ci-date - 1) THEN d2 = tdate.
    ELSE d2 = ci-date - 1. 
    d2 = d2 + 1. 

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT tdate) AND 
         NOT (res-line.abreise LE fdate)) 
         OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = cardtype 
        BY res-line.gastnr BY res-line.resnr BY res-line.reslinnr: /*MT 13/08/12 */
        
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.

        ASSIGN 
            curr-i = 0
            do-it = YES.

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        ASSIGN do-it = AVAILABLE segment AND segment.vip-level = 0.

        /*IF res-line.zinr NE "" THEN
        DO:
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN do-it = NO.
        END.*/

        IF do-it AND res-line.resstatus = 8 THEN
        DO:
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.

        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END.                                    

        IF do-it THEN
        DO:
            FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = res-line.gastnr
                AND cust-list-detail.gname = res-line.NAME NO-LOCK NO-ERROR.
            IF NOT AVAILABLE cust-list-detail THEN
            DO:
                CREATE cust-list-detail.
                ASSIGN cust-list-detail.gastnr     = res-line.gastnr 
                       cust-list-detail.resno      = res-line.resnr
                       cust-list-detail.reslinnr   = res-line.reslinnr
                       cust-list-detail.gname      = res-line.NAME
                       cust-list-detail.arrival    = res-line.ankunft
                       cust-list-detail.depart     = res-line.abreise.
    
                FIND FIRST glist WHERE glist.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE glist THEN DO:
                    ASSIGN cust-list-detail.cust-name  = glist.NAME + "," + glist.anredefirma + " " + glist.vorname1
                           cust-list-detail.plz        = glist.plz 
                           cust-list-detail.land       = glist.land
                           cust-list-detail.sales-id   = glist.phonetik3
                           cust-list-detail.wohnort    = glist.wohnort.
    
                    FIND FIRST nation WHERE nation.kurzbez = glist.land NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN
                    DO:
                        FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                    END.
                    ELSE cust-list-detail.region = "UNKOWN".  

                    IF cust-list-detail.sales-id = "" THEN
                            ASSIGN cust-list-detail.sales-id   = guest.phonetik3.
                END.                
                ELSE DO: 
                    ASSIGN 
                        cust-list-detail.cust-name  = guest.NAME + "," + guest.anredefirma + " " + guest.vorname1
                        cust-list-detail.plz        = guest.plz 
                        cust-list-detail.land       = guest.land
                        cust-list-detail.sales-id   = guest.phonetik3
                        cust-list-detail.wohnort    = guest.wohnort.   
    
                    FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN
                    DO:
                        FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                    END.
                    ELSE cust-list-detail.region = "UNKOWN".                   
                END.                
            END.

            
            ASSIGN found = NO.
            FIND FIRST clist WHERE clist.gastnr = res-line.gastnr
                AND clist.gname = res-line.NAME NO-LOCK NO-ERROR.
            IF AVAILABLE clist THEN DO:
                IF clist.resnr NE " "  THEN DO:
                    DO loopi = 1 TO NUM-ENTRIES(clist.resnr, ";"):
                        IF ENTRY(loopi, clist.resnr, ";") NE " " THEN DO:
                            IF INT(ENTRY(loopi, clist.resnr, ";")) = res-line.resnr THEN DO:
                                ASSIGN found = YES.
                                LEAVE.
                            END.
                        END.
                    END.
                    IF NOT found THEN
                        ASSIGN clist.resnr = clist.resnr + STRING(res-line.resnr) + ";".    
                END.
                ELSE IF clist.resnr = " "  THEN ASSIGN clist.resnr = clist.resnr + STRING(res-line.resnr) + ";".                     
            END.
            
            
            IF res-line.ankunft GT fdate THEN datum1 = res-line.ankunft. 
            ELSE datum1 = fdate.
            IF res-line.abreise LT tdate THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = tdate.

            
            DO datum = datum1 TO datum2:
                
                ASSIGN
                    curr-i        = curr-i + 1 
                    net-lodg      = 0
                    Fnet-lodg     = 0
                    tot-breakfast = 0
                    tot-lunch     = 0 
                    tot-dinner    = 0
                    tot-other     = 0
                    tot-rmrev     = 0
                    tot-vat       = 0
                    tot-service   = 0.
    
                RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, ci-date,
                    OUTPUT Fnet-lodg, OUTPUT net-lodg,
                    OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                    OUTPUT tot-dinner, OUTPUT tot-other,
                    OUTPUT tot-rmrev, OUTPUT tot-vat,
                    OUTPUT tot-service).


                /*
                /*Revenue from outlet*/
                FIND FIRST guest-queasy WHERE guest-queasy.gastnr = res-line.gastnrmember
                    AND guest-queasy.date1 = datum
                    AND guest-queasy.number2 = res-line.resnr AND guest-queasy.number3 = res-line.reslinnr NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE guest-queasy:
                    ASSIGN
                        cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").

                    FIND NEXT guest-queasy WHERE guest-queasy.gastnr = res-line.gastnrmember
                        AND guest-queasy.date1 = datum
                        AND guest-queasy.number2 = res-line.resnr AND guest-queasy.number3 = res-line.reslinnr NO-LOCK NO-ERROR.
                END.

                /*Revenue from other*/
                FIND FIRST bill-line WHERE bill-line.massnr = res-line.resnr
                    AND bill-line.billin-nr = res-line.reslinnr
                    AND bill-line.bill-datum = datum NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE bill-line:
                    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                        AND artikel.departement = bill-line.departement 
                        AND artikel.artart = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN 
                        ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99").

                    FIND NEXT bill-line WHERE bill-line.massnr = res-line.resnr
                        AND bill-line.billin-nr = res-line.reslinnr
                        AND bill-line.bill-datum = datum NO-LOCK NO-ERROR.
                END.*/

                 /*Revenue from other*/
                IF curr-resnr NE res-line.resnr OR curr-reslinnr NE res-line.reslinnr THEN DO:
                    ASSIGN
                        curr-resnr = res-line.resnr 
                        curr-reslinnr = res-line.reslinnr.
                    
                    IF curr-resnr NE 0 THEN DO:
                        IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) OR (res-line.ankunft = res-line.abreise) THEN 
                        DO: 
                             IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                                ASSIGN cust-list-detail.count-room = STRING(INTEGER(cust-list-detail.count-room) + res-line.zimmeranz, ">>,>>>,>>>,>>9")
                                       tot-nofrm                   = tot-nofrm + res-line.zimmeranz
                                       gt-nofrm                    = gt-nofrm + res-line.zimmeranz.                        
                        END.
                    END.
                    
                    IF excl-other = NO THEN DO:
                        /*FIND FIRST bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                        FOR EACH bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK:
                            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                                AND bill-line.bill-datum = datum NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                    AND artikel.departement = bill-line.departement 
                                    AND artikel.artart = 0 NO-LOCK :
                                IF currency NE " " THEN
                                    ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99")
                                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99").
                                ELSE
                                    ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                            END.
                             /*add bill
                            FIND FIRST bbuf WHERE bbuf.resnr = res-line.resnr 
                                AND bbuf.parent-nr = res-line.reslinnr
                                AND bbuf.reslinnr NE res-line.reslinnr NO-LOCK NO-ERROR.
                            IF AVAILABLE bbuf THEN DO:
                                FOR EACH bbuf WHERE bbuf.resnr = res-line.resnr 
                                    AND bbuf.parent-nr = res-line.reslinnr
                                    AND bbuf.reslinnr NE res-line.reslinnr USE-INDEX reserv_index NO-LOCK:
                
                                    FOR EACH bline WHERE bline.rechnr = bbuf.rechnr
                                        AND bline.bill-datum = datum NO-LOCK,
                                        FIRST artikel WHERE artikel.artnr = bline.artnr 
                                            AND artikel.departement = bline.departement 
                                            AND artikel.artart = 0 NO-LOCK:
            
                                        IF currency NE " " THEN
                                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99")
                                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99").
                                        ELSE
                                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                                    END.
                                END.
                            END.*/
                        END.
                    END.                                      
                END.
                
                /*
                IF AVAILABLE bill THEN DO:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN
                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99")
                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99").
                        ELSE
                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                    END.
                END.*/        

                IF currency NE " " THEN
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((tot-breakfast + tot-lunch + tot-dinner) / exrate), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (tot-other / exrate), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + (net-lodg / exrate), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((net-lodg + tot-breakfast 
                                                       + tot-lunch + tot-dinner + tot-other) / exrate) , "->>>,>>>,>>>,>>9.99").
                ELSE                   
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + tot-breakfast + tot-lunch + tot-dinner, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + tot-other, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + net-lodg, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + net-lodg + tot-breakfast 
                                                       + tot-lunch + tot-dinner + tot-other , "->>>,>>>,>>>,>>9.99").

                IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) OR (res-line.ankunft = res-line.abreise) THEN 
                DO: 
                     IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                        ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) + 1, ">>>,>>9").
                     ELSE IF res-line.resstatus = 11 OR res-line.resstatus = 13 THEN ASSIGN cust-list-detail.rm-sharer = "*".
                END.
            END.

            IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) OR (res-line.ankunft = res-line.abreise) THEN 
            DO: 
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                   ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) * res-line.zimmeranz, ">>>,>>9").
            END.
        END.
    END.

    IF excl-other = NO THEN DO:
    /*Revenue from outlet*/
        FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK :
      
            FIND FIRST res-line WHERE 
                res-line.resnr EQ guest-queasy.number2 AND
                res-line.reslinnr EQ guest-queasy.number3 NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO:
                FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = res-line.gastnr
                    AND cust-list-detail.resno = res-line.resnr
                    AND cust-list-detail.gname = res-line.NAME NO-LOCK NO-ERROR.
                IF AVAILABLE cust-list-detail THEN DO:
                    IF currency NE " " THEN
                            ASSIGN
                                cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate), "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (guest-queasy.deci3 / exrate), "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((guest-queasy.deci1 + guest-queasy.deci2
                                                                + guest-queasy.deci3) / exrate), "->>>,>>>,>>>,>>9.99").   
                    ELSE
                        ASSIGN
                            cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + guest-queasy.deci1 + guest-queasy.deci2
                                                            + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").                              
                END.         
            END.
        END.
    END.
    

    IF DAY(fdate) = 29 AND MONTH(fdate) = 2 THEN
        ly-fdate = DATE(MONTH(fdate),28,YEAR(fdate) - 1).
    ELSE ly-fdate = DATE(MONTH(fdate),DAY(fdate),YEAR(fdate) - 1).

    IF DAY(tdate) = 29 AND MONTH(tdate) = 2 THEN
        ly-tdate = DATE(MONTH(tdate),28,YEAR(tdate) - 1).
    ELSE ly-tdate = DATE(MONTH(tdate),DAY(tdate),YEAR(tdate) - 1).

    FOR EACH genstat WHERE 
        genstat.datum GE ly-fdate
        AND genstat.datum LE ly-tdate
        /*AND genstat.resstatus NE 13*/
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
        FIRST guest WHERE guest.gastnr = genstat.gastnr
        AND guest.karteityp = cardtype NO-LOCK 
        BY genstat.gastnr BY guest.land BY genstat.resnr :

            FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                AND cust-list-detail.resno = genstat.resnr
                AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
            IF AVAILABLE cust-list-detail THEN
            DO:
                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                        ASSIGN 
                            cust-list-detail.ly-rev = STRING(DECIMAL(cust-list-detail.ly-rev) + ((genstat.logis + genstat.res-deci[2] +
                                                      genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE 
                    ASSIGN 
                            cust-list-detail.ly-rev = STRING(DECIMAL(cust-list-detail.ly-rev) + genstat.logis + genstat.res-deci[2] +
                                                      genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5], "->>>,>>>,>>>,>>9.99").

            END.    
    END.
END.


PROCEDURE cr-ftd1:
  DEFINE VARIABLE t-argtumsatz  AS INT.
  DEFINE VARIABLE rate          AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE frate         AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE rmnite        AS INTEGER  NO-UNDO INIT 0.
  DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
  DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.
  DEFINE VARIABLE loopi         AS INTEGER NO-UNDO.
  DEFINE VARIABLE found         AS LOGICAL NO-UNDO.

  
  DEFINE BUFFER clist FOR cust-list-detail.
    
  FOR EACH genstat WHERE 
      genstat.datum GE fdate
      AND genstat.datum LE tdate
      /*AND genstat.resstatus NE 13*/
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES,
      FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK 
      BY genstat.gastnr BY genstat.resnr BY guest.land:

       FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
       FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
            /*AND cust-list-detail.resno = genstat.resnr*/
            AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
       IF NOT AVAILABLE cust-list-detail THEN DO:
            CREATE cust-list-detail.
            ASSIGN cust-list-detail.gastnr     = genstat.gastnr 
                   cust-list-detail.resno      = genstat.resnr
                   cust-list-detail.reslinnr   = genstat.res-int[1]
                   cust-list-detail.gname      = bguest.NAME
                   cust-list-detail.arrival    = genstat.res-date[1]
                   cust-list-detail.depart     = genstat.res-date[2].

            FIND FIRST glist WHERE glist.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            IF AVAILABLE glist THEN DO:
                ASSIGN cust-list-detail.cust-name  = glist.NAME + "," + glist.anredefirma + " " + glist.vorname1
                       cust-list-detail.plz        = glist.plz 
                       cust-list-detail.land       = glist.land
                       cust-list-detail.sales-id   = glist.phonetik3
                       cust-list-detail.wohnort    = glist.wohnort.

                FIND FIRST nation WHERE nation.kurzbez = glist.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                END.
                ELSE cust-list-detail.region = "UNKOWN".

                IF cust-list-detail.sales-id = "" THEN
                            ASSIGN cust-list-detail.sales-id   = guest.phonetik3.

            END.                
            ELSE DO: 
                ASSIGN 
                    cust-list-detail.cust-name  = guest.NAME + "," + guest.anredefirma + " " + guest.vorname1
                    cust-list-detail.plz        = guest.plz 
                    cust-list-detail.land       = guest.land
                    cust-list-detail.sales-id   = guest.phonetik3
                    cust-list-detail.wohnort    = guest.wohnort.   

                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                END.
                ELSE cust-list-detail.region = "UNKOWN".                   
            END.                
        END.

        
        ASSIGN found = NO.
        FIND FIRST clist WHERE clist.gastnr = genstat.gastnr AND clist.gname = bguest.NAME NO-LOCK NO-ERROR.
        IF AVAILABLE clist THEN DO:
            IF clist.resnr NE " "  THEN DO:
                DO loopi = 1 TO NUM-ENTRIES(clist.resnr, ";"):
                    IF ENTRY(loopi, clist.resnr, ";") NE " " THEN DO:
                        IF INT(ENTRY(loopi, clist.resnr, ";")) = genstat.resnr THEN DO:
                            ASSIGN found = YES.
                            LEAVE.
                        END.
                    END.
                END.
                IF NOT found THEN
                    ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".    
            END.
            ELSE IF clist.resnr = " "  THEN ASSIGN clist.resnr = clist.resnr + STRING(genstat.resnr) + ";".                     
        END.
        
        /*
        /*Revenue from outlet*/
        FIND FIRST guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
            AND guest-queasy.date1 = genstat.datum
            AND guest-queasy.number2 = genstat.resnr AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest-queasy:
            ASSIGN
                cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").

            FIND NEXT guest-queasy WHERE guest-queasy.gastnr = genstat.gastnrmember
                AND guest-queasy.date1 = genstat.datum
                AND guest-queasy.number2 = genstat.resnr AND guest-queasy.number3 = genstat.res-int[1] NO-LOCK NO-ERROR.
        END.

        /*Revenue from other*/
        FIND FIRST bill-line WHERE bill-line.massnr = genstat.resnr
            AND bill-line.billin-nr = genstat.res-int[1]
            AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE bill-line:
            FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                AND artikel.departement = bill-line.departement 
                AND artikel.artart = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN 
                ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99").

            FIND NEXT bill-line WHERE bill-line.massnr = genstat.resnr
                AND bill-line.billin-nr = genstat.res-int[1]
                AND bill-line.bill-datum = genstat.datum NO-LOCK NO-ERROR.
        END.*/

        IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (genstat.res-deci[5] / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + (genstat.logis / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((genstat.logis + genstat.res-deci[2] 
                                                       + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + (genstat.res-deci[7] / exrate.betrag), "->>>,>>>,>>>,>>9.99").
        END.
        ELSE
            ASSIGN
               cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + (genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]), "->>>,>>>,>>>,>>9.99")
               cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + genstat.res-deci[5], "->>>,>>>,>>>,>>9.99")
               cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
               cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + genstat.logis + genstat.res-deci[2] 
                                               + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5] , "->>>,>>>,>>>,>>9.99")
               cust-list-detail.ba-umsatz    = STRING(DECIMAL(cust-list-detail.ba-umsatz) + genstat.res-deci[7], "->>>,>>>,>>>,>>9.99").
        
        IF genstat.resstatus NE 13 THEN 
              ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) + 1, ">>>,>>9").
        ELSE ASSIGN cust-list-detail.rm-sharer = "*".
        
        
        /*Revenue from other*/
        IF curr-resnr NE genstat.resnr OR curr-reslinnr NE genstat.res-int[1] THEN DO:
            ASSIGN
                curr-resnr = genstat.resnr 
                curr-reslinnr = genstat.res-int[1].

            IF genstat.resstatus = 6 THEN DO:
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                    ASSIGN cust-list-detail.count-room = STRING(INTEGER(cust-list-detail.count-room) + res-line.zimmeranz, ">>,>>>,>>>,>>9"). 
            END.
            
            IF excl-other = NO THEN DO:
                /*FIND FIRST bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                FOR EACH bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
    
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = genstat.datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                        END.
                        ELSE
                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                    END.
    
                     /*add bill
                    FIND FIRST bbuf WHERE bbuf.resnr = genstat.resnr 
                        AND bbuf.parent-nr = genstat.res-int[1]
                        AND bbuf.reslinnr NE genstat.res-int[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE bbuf THEN DO:
                        FOR EACH bbuf WHERE bbuf.resnr = genstat.resnr 
                            AND bbuf.parent-nr = genstat.res-int[1]
                            AND bbuf.reslinnr NE genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
        
                            FOR EACH bline WHERE bline.rechnr = bbuf.rechnr
                                /*AND bline.bill-datum = genstat.datum*/ NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bline.artnr 
                                    AND artikel.departement = bline.departement 
                                    AND artikel.artart = 0 NO-LOCK:
    
                                IF currency NE " " THEN DO:
                                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                    IF AVAILABLE exrate THEN 
                                            ASSIGN 
                                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bline.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                                END.
                                ELSE
                                    ASSIGN 
                                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bline.betrag, "->>>,>>>,>>>,>>9.99").
                            END.
                        END.
                    END.*/
    
                END.
            END.
            
        END.

        /*
        IF AVAILABLE bill THEN DO:
            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                AND bill-line.bill-datum = genstat.datum NO-LOCK,
                FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                    AND artikel.artart = 0 NO-LOCK :
                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                        ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                               cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE
                    ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
            END.
        END.      */  
  END.

  IF excl-other = NO THEN DO:
    /*Revenue from outlet*/
      FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK BY guest-queasy.number2:
      
            FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                AND genstat.res-int[1] = guest-queasy.number3 
                AND genstat.datum = guest-queasy.date1
                AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
            IF AVAILABLE genstat THEN DO:
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                    AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.            
                IF AVAILABLE cust-list-detail THEN DO:
                    IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                            ASSIGN
                                cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (guest-queasy.deci3 / exrate.betrag), "->>>,>>>,>>>,>>9.99")
                                cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((guest-queasy.deci1 + guest-queasy.deci2
                                                                + guest-queasy.deci3) / exrate.betrag), "->>>,>>>,>>>,>>9.99").         
                    END.
                    ELSE
                        ASSIGN
                            cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + guest-queasy.deci1 + guest-queasy.deci2
                                                            + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").            
                END.
            END.
      END.
  END.  
END.

PROCEDURE create-forecast1:
    DEFINE VARIABLE do-it   AS LOGICAL INIT YES.
    DEFINE VARIABLE datum   AS DATE. 
    DEFINE VARIABLE datum1  AS DATE. 
    DEFINE VARIABLE datum2  AS DATE. 
    DEFINE VARIABLE d2      AS DATE.
    DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.
    DEFINE VARIABLE found         AS LOGICAL NO-UNDO.
    DEFINE VARIABLE loopi         AS INTEGER NO-UNDO.
    DEFINE VARIABLE count-rm      AS INTEGER NO-UNDO.

    IF fdate NE ci-date AND fdate LT ci-date THEN fdate = ci-date.
    datum1 = fdate. 
    IF tdate LT (ci-date - 1) THEN d2 = tdate.
    ELSE d2 = ci-date - 1. 
    d2 = d2 + 1. 

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT tdate) AND 
         NOT (res-line.abreise LE fdate)) 
         OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnr 
        BY res-line.gastnr BY res-line.resnr BY res-line.reslinnr: /*MT 13/08/12 */


        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.

        ASSIGN 
            curr-i = 0
            do-it = YES.

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        ASSIGN do-it = AVAILABLE segment AND segment.vip-level = 0.

        /*IF res-line.zinr NE "" THEN
        DO:
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN do-it = NO.
        END.*/

        IF do-it AND res-line.resstatus = 8 THEN
        DO:
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.

        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END.                                    

        IF do-it THEN
        DO:
            FOR EACH cust-list-detail WHERE cust-list-detail.resno = 4523:
                MESSAGE "1" cust-list-detail.gastnr cust-list-detail.gname VIEW-AS ALERT-BOX INFO.
            END.

            FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = res-line.gastnr
                /*AND cust-list-detail.resno = res-line.resnr*/
                AND cust-list-detail.gname = res-line.NAME NO-LOCK NO-ERROR.
            IF NOT AVAILABLE cust-list-detail THEN
            DO:
                IF res-line.resnr = 4523 THEN
                    MESSAGE "2" res-line.gastnr res-line.NAME VIEW-AS ALERT-BOX INFO.
                CREATE cust-list-detail.
                ASSIGN cust-list-detail.gastnr     = res-line.gastnr 
                       cust-list-detail.resno      = res-line.resnr
                       cust-list-detail.reslinnr   = res-line.reslinnr
                       cust-list-detail.gname      = res-line.NAME
                       cust-list-detail.arrival    = res-line.ankunft
                       cust-list-detail.depart     = res-line.abreise.
    
                FIND FIRST glist WHERE glist.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE glist THEN DO:
                    ASSIGN cust-list-detail.cust-name  = glist.NAME + "," + glist.anredefirma + " " + glist.vorname1
                           cust-list-detail.plz        = glist.plz 
                           cust-list-detail.land       = glist.land
                           cust-list-detail.sales-id   = glist.phonetik3
                           cust-list-detail.wohnort    = glist.wohnort.
    
                    FIND FIRST nation WHERE nation.kurzbez = glist.land NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN
                    DO:
                        FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                    END.
                    ELSE cust-list-detail.region = "UNKOWN". 

                    IF cust-list-detail.sales-id = "" THEN
                            ASSIGN cust-list-detail.sales-id   = guest.phonetik3.

                END.                
                ELSE DO: 
                    ASSIGN 
                        cust-list-detail.cust-name  = guest.NAME + "," + guest.anredefirma + " " + guest.vorname1
                        cust-list-detail.plz        = guest.plz 
                        cust-list-detail.land       = guest.land
                        cust-list-detail.sales-id   = guest.phonetik3
                        cust-list-detail.wohnort    = guest.wohnort.   
    
                    FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN
                    DO:
                        FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN cust-list-detail.region = queasy.char1.
                    END.
                    ELSE cust-list-detail.region = "UNKOWN".                   
                END.                
            END.

            
            ASSIGN found = NO.
            FIND FIRST clist WHERE clist.gastnr = res-line.gastnr
                AND clist.gname = res-line.NAME NO-LOCK NO-ERROR.
            IF AVAILABLE clist THEN DO:
                IF clist.resnr NE " "  THEN DO:
                    DO loopi = 1 TO NUM-ENTRIES(clist.resnr, ";"):
                        IF ENTRY(loopi, clist.resnr, ";") NE " " THEN DO:
                            IF INT(ENTRY(loopi, clist.resnr, ";")) = res-line.resnr THEN DO:
                                ASSIGN found = YES.
                                LEAVE.
                            END.
                        END.
                    END.
                    IF NOT found THEN
                        ASSIGN clist.resnr = clist.resnr + STRING(res-line.resnr) + ";".    
                END.
                ELSE IF clist.resnr = " "  THEN ASSIGN clist.resnr = clist.resnr + STRING(res-line.resnr) + ";".                     
            END.
            
            
            IF res-line.ankunft GT fdate THEN datum1 = res-line.ankunft. 
            ELSE datum1 = fdate.
            IF res-line.abreise LT tdate THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = tdate.

            
            DO datum = datum1 TO datum2:
                
                ASSIGN
                    curr-i        = curr-i + 1 
                    net-lodg      = 0
                    Fnet-lodg     = 0
                    tot-breakfast = 0
                    tot-lunch     = 0 
                    tot-dinner    = 0
                    tot-other     = 0
                    tot-rmrev     = 0
                    tot-vat       = 0
                    tot-service   = 0.
    
                RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, ci-date,
                    OUTPUT Fnet-lodg, OUTPUT net-lodg,
                    OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                    OUTPUT tot-dinner, OUTPUT tot-other,
                    OUTPUT tot-rmrev, OUTPUT tot-vat,
                    OUTPUT tot-service).


                /*
                /*Revenue from outlet*/
                FIND FIRST guest-queasy WHERE guest-queasy.gastnr = res-line.gastnrmember
                    AND guest-queasy.date1 = datum
                    AND guest-queasy.number2 = res-line.resnr AND guest-queasy.number3 = res-line.reslinnr NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE guest-queasy:
                    ASSIGN
                        cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                        cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").

                    FIND NEXT guest-queasy WHERE guest-queasy.gastnr = res-line.gastnrmember
                        AND guest-queasy.date1 = datum
                        AND guest-queasy.number2 = res-line.resnr AND guest-queasy.number3 = res-line.reslinnr NO-LOCK NO-ERROR.
                END.

                /*Revenue from other*/
                FIND FIRST bill-line WHERE bill-line.massnr = res-line.resnr
                    AND bill-line.billin-nr = res-line.reslinnr
                    AND bill-line.bill-datum = datum NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE bill-line:
                    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                        AND artikel.departement = bill-line.departement 
                        AND artikel.artart = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN 
                        ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) +  bill-line.betrag, "->>>,>>>,>>>,>>9.99").

                    FIND NEXT bill-line WHERE bill-line.massnr = res-line.resnr
                        AND bill-line.billin-nr = res-line.reslinnr
                        AND bill-line.bill-datum = datum NO-LOCK NO-ERROR.
                END.*/

                 /*Revenue from other*/
                IF curr-resnr NE res-line.resnr OR curr-reslinnr NE res-line.reslinnr THEN DO:
                    ASSIGN
                        curr-resnr = res-line.resnr 
                        curr-reslinnr = res-line.reslinnr.
                    
                    IF curr-resnr NE 0 THEN DO:
                        IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) OR (res-line.ankunft = res-line.abreise) THEN 
                        DO: 
                             IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                                ASSIGN cust-list-detail.count-room = STRING(INTEGER(cust-list-detail.count-room) + res-line.zimmeranz, ">>,>>>,>>>,>>9")
                                       tot-nofrm                   = tot-nofrm + res-line.zimmeranz
                                       gt-nofrm                    = gt-nofrm + res-line.zimmeranz.                        
                        END.
                    END.
                           
                    IF excl-other = NO THEN DO:
                        /*FIND FIRST bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                        FOR EACH bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK:
                            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                                AND bill-line.bill-datum = datum NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                    AND artikel.departement = bill-line.departement 
                                    AND artikel.artart = 0 NO-LOCK :
                                IF currency NE " " THEN DO:
                                    ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99")
                                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99").
                                END.
                                ELSE
                                    ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                           cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                            END.
    
                              /*add bill
                            FIND FIRST bbuf WHERE bbuf.resnr = res-line.resnr 
                                AND bbuf.parent-nr = res-line.reslinnr
                                AND bbuf.reslinnr NE res-line.reslinnr NO-LOCK NO-ERROR.
                            IF AVAILABLE bbuf THEN DO:
                                FOR EACH bbuf WHERE bbuf.resnr = res-line.resnr 
                                    AND bbuf.parent-nr = res-line.reslinnr
                                    AND bbuf.reslinnr NE res-line.reslinnr USE-INDEX reserv_index NO-LOCK:
                
                                    FOR EACH bline WHERE bline.rechnr = bbuf.rechnr
                                        AND bline.bill-datum = datum NO-LOCK,
                                        FIRST artikel WHERE artikel.artnr = bline.artnr 
                                            AND artikel.departement = bline.departement 
                                            AND artikel.artart = 0 NO-LOCK:
            
                                        IF currency NE " " THEN
                                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99")
                                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99").
                                        ELSE
                                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                                    END.
                                END.
                            END.*/
                        END.
                    END.
                   
                END.
                /*
                IF AVAILABLE bill THEN DO:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN DO:
                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99")
                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + (bill-line.betrag / exrate), "->>>,>>>,>>>,>>9.99").
                        END.
                        ELSE
                            ASSIGN cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99")
                                   cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + bill-line.betrag, "->>>,>>>,>>>,>>9.99").
                    END.
                END.        */

                IF currency NE " " THEN DO:
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((tot-breakfast + tot-lunch + tot-dinner) / exrate) , "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (tot-other / exrate), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + (net-lodg / exrate), "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((net-lodg + tot-breakfast 
                                                       + tot-lunch + tot-dinner + tot-other) / exrate), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE
                    ASSIGN
                       cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + tot-breakfast + tot-lunch + tot-dinner, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + tot-other, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.argtumsatz   = STRING(DECIMAL(cust-list-detail.argtumsatz) + net-lodg, "->>>,>>>,>>>,>>9.99")
                       cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + net-lodg + tot-breakfast 
                                                       + tot-lunch + tot-dinner + tot-other , "->>>,>>>,>>>,>>9.99").

                IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) OR (res-line.ankunft = res-line.abreise) THEN 
                DO: 
                     IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                        ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) + 1, ">>>,>>9").
                     ELSE IF res-line.resstatus = 11 OR res-line.resstatus = 13 THEN ASSIGN cust-list-detail.rm-sharer = "*".
                END.
            END.

            IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) OR (res-line.ankunft = res-line.abreise) THEN 
            DO: 
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                   ASSIGN cust-list-detail.logiernachte = STRING(INTEGER(cust-list-detail.logiernachte) * res-line.zimmeranz, ">>>,>>9").
            END.
        END.
    END.

    IF excl-other = NO THEN DO:
        /*Revenue from outlet*/
        FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK :
      
            FIND FIRST res-line WHERE 
                res-line.resnr EQ guest-queasy.number2 AND
                res-line.reslinnr EQ guest-queasy.number3 NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO:
                FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = res-line.gastnr
                    AND cust-list-detail.resno = res-line.resnr
                    AND cust-list-detail.gname = res-line.NAME NO-LOCK NO-ERROR.
                IF AVAILABLE cust-list-detail THEN DO:
                    IF currency NE " " THEN 
                        ASSIGN
                            cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate), "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + (guest-queasy.deci3 / exrate), "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + ((guest-queasy.deci1 + guest-queasy.deci2
                                                                + guest-queasy.deci3) / exrate), "->>>,>>>,>>>,>>9.99").
                    ELSE
                        ASSIGN
                            cust-list-detail.f-b-umsatz   = STRING(DECIMAL(cust-list-detail.f-b-umsatz) + guest-queasy.deci1 + guest-queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.sonst-umsatz = STRING(DECIMAL(cust-list-detail.sonst-umsatz) + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust-list-detail.gesamtumsatz = STRING(DECIMAL(cust-list-detail.gesamtumsatz) + guest-queasy.deci1 + guest-queasy.deci2
                                                            + guest-queasy.deci3, "->>>,>>>,>>>,>>9.99").                              
                END.         
            END.
        END.
    END.
    

    IF DAY(fdate) = 29 AND MONTH(fdate) = 2 THEN
        ly-fdate = DATE(MONTH(fdate),28,YEAR(fdate) - 1).
    ELSE ly-fdate = DATE(MONTH(fdate),DAY(fdate),YEAR(fdate) - 1).

    IF DAY(tdate) = 29 AND MONTH(tdate) = 2 THEN
        ly-tdate = DATE(MONTH(tdate),28,YEAR(tdate) - 1).
    ELSE ly-tdate = DATE(MONTH(tdate),DAY(tdate),YEAR(tdate) - 1).

    FOR EACH genstat WHERE 
        genstat.datum GE ly-fdate
        AND genstat.datum LE ly-tdate
        /*AND genstat.resstatus NE 13*/
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
        FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK 
        BY genstat.gastnr BY guest.land BY genstat.resnr :

            FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            FIND FIRST cust-list-detail WHERE cust-list-detail.gastnr = genstat.gastnr
                AND cust-list-detail.resno = genstat.resnr
                AND cust-list-detail.gname = bguest.NAME NO-LOCK NO-ERROR.
            IF AVAILABLE cust-list-detail THEN
            DO:
                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                        ASSIGN 
                            cust-list-detail.ly-rev = STRING(DECIMAL(cust-list-detail.ly-rev) + ((genstat.logis + genstat.res-deci[2] +
                                                      genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag), "->>>,>>>,>>>,>>9.99").
                END.
                ELSE
                    ASSIGN 
                        cust-list-detail.ly-rev = STRING(DECIMAL(cust-list-detail.ly-rev) + genstat.logis + genstat.res-deci[2] +
                                                  genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5], "->>>,>>>,>>>,>>9.99").

            END.    
    END.
END.




