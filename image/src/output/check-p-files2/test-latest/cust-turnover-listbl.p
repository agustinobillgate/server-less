DEFINE TEMP-TABLE cust-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR     
    FIELD gesamtumsatz      LIKE guest.gesamtumsatz 
    FIELD logiernachte      LIKE guest.logiernachte 
    FIELD argtumsatz        LIKE guest.argtumsatz 
    FIELD f-b-umsatz        LIKE guest.f-b-umsatz 
    FIELD sonst-umsatz      LIKE guest.sonst-umsatz 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS DECIMAL
    FIELD ly-rev            AS DECIMAL
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS INT
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER.

DEFINE TEMP-TABLE cust-list1
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR     
    FIELD gesamtumsatz      LIKE guest.gesamtumsatz 
    FIELD logiernachte      LIKE guest.logiernachte 
    FIELD argtumsatz        LIKE guest.argtumsatz 
    FIELD f-b-umsatz        LIKE guest.f-b-umsatz 
    FIELD sonst-umsatz      LIKE guest.sonst-umsatz 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS DECIMAL
    FIELD ly-rev            AS DECIMAL
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS INT
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER.

DEFINE INPUT PARAMETER cardtype             AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sort-type            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-sort1           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER tdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER check-ftd            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER currency             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER excl-other           AS LOGICAL NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER curr-sort2    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER sort1               AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR cust-list.

DEFINE VARIABLE t-lyrev AS DECIMAL INIT 0.
DEFINE VARIABLE t-gesamtumsatz AS DECIMAL INIT 0.
DEFINE VARIABLE t-logiernachte AS INT INIT 0.
DEFINE VARIABLE t-argtumsatz AS DECIMAL INIT 0.
DEFINE VARIABLE t-f-b-umsatz AS DECIMAL INIT 0.
DEFINE VARIABLE t-sonst-umsatz AS DECIMAL INIT 0.
DEFINE VARIABLE t-ba-umsatz AS DECIMAL INIT 0.
DEFINE VARIABLE t-stayno    AS INT INIT 0.

DEFINE VARIABLE tr-lyrev AS DECIMAL INIT 0.
DEFINE VARIABLE tr-gesamtumsatz AS DECIMAL INIT 0.
DEFINE VARIABLE tr-logiernachte AS INT INIT 0.
DEFINE VARIABLE tr-argtumsatz AS DECIMAL INIT 0.
DEFINE VARIABLE tr-f-b-umsatz AS DECIMAL INIT 0.
DEFINE VARIABLE tr-sonst-umsatz AS DECIMAL INIT 0.
DEFINE VARIABLE tr-ba-umsatz AS DECIMAL INIT 0.
DEFINE VARIABLE tr-stayno    AS INT INIT 0.

DEFINE VARIABLE counter AS INT.
DEFINE VARIABLE curr-region AS CHAR.

FOR EACH cust-list:
    DELETE cust-list.
END.

RUN cust-turnover_2bl.p (cardtype, sort-type, curr-sort1, 
                        fdate, tdate,check-ftd, currency, excl-other,
                        INPUT-OUTPUT curr-sort2, 
                        OUTPUT TABLE cust-list1).

FOR EACH cust-list1 BY cust-list1.curr-pos BY cust-list1.region:
    counter = counter + 1.
    IF cust-list1.resnr NE "" THEN
        cust-list1.stayno = NUM-ENTRIES(cust-list1.resnr,";") - 1.
    
    ASSIGN
        t-lyrev        = t-lyrev + cust-list1.ly-rev
        t-gesamtumsatz = t-gesamtumsatz + cust-list1.gesamtumsatz
        t-logiernachte = t-logiernachte + cust-list1.logiernachte
        t-argtumsatz   = t-argtumsatz + cust-list1.argtumsatz
        t-f-b-umsatz   = t-f-b-umsatz + cust-list1.f-b-umsatz
        t-sonst-umsatz = t-sonst-umsatz + cust-list1.sonst-umsatz
        t-ba-umsatz    = t-ba-umsatz + cust-list1.ba-umsatz
        t-stayno       = t-stayno    + cust-list1.stayno.   
    
    IF counter = 1 THEN 
        ASSIGN
            curr-region = cust-list1.region
            cust-list1.region1 = curr-region.
    
    IF curr-region NE cust-list1.region THEN
    DO:
        cust-list1.region1 = cust-list1.region.
        CREATE cust-list.
        ASSIGN
            cust-list.cust-name = "T O T A L"
            cust-list.ly-rev       = tr-lyrev
            cust-list.gesamtumsatz = tr-gesamtumsatz
            cust-list.logiernachte = tr-logiernachte
            cust-list.argtumsatz   = tr-argtumsatz
            cust-list.f-b-umsatz   = tr-f-b-umsatz
            cust-list.sonst-umsatz = tr-sonst-umsatz
            cust-list.ba-umsatz    = tr-ba-umsatz
            cust-list.stayno       = tr-stayno
            cust-list.region       = "zzr"
            cust-list.counter      = counter
    
            tr-lyrev        = cust-list1.ly-rev
            tr-gesamtumsatz = cust-list1.gesamtumsatz
            tr-logiernachte = cust-list1.logiernachte
            tr-argtumsatz   = cust-list1.argtumsatz
            tr-f-b-umsatz   = cust-list1.f-b-umsatz
            tr-sonst-umsatz = cust-list1.sonst-umsatz
            tr-ba-umsatz    = cust-list1.ba-umsatz
            tr-stayno       = cust-list1.stayno
    
            counter = counter + 1
            curr-region = cust-list1.region
    
        .
    END.
    ELSE
        ASSIGN
            tr-lyrev        = tr-lyrev + cust-list1.ly-rev
            tr-gesamtumsatz = tr-gesamtumsatz + cust-list1.gesamtumsatz
            tr-logiernachte = tr-logiernachte + cust-list1.logiernachte
            tr-argtumsatz   = tr-argtumsatz + cust-list1.argtumsatz
            tr-f-b-umsatz   = tr-f-b-umsatz + cust-list1.f-b-umsatz
            tr-sonst-umsatz = tr-sonst-umsatz + cust-list1.sonst-umsatz
            tr-ba-umsatz    = tr-ba-umsatz + cust-list1.ba-umsatz
            tr-stayno       = tr-stayno    + cust-list1.stayno
        .
    
    
    CREATE cust-list.
    BUFFER-COPY cust-list1 TO cust-list.
    cust-list.counter = counter.
        
END.

counter = counter + 1.

CREATE cust-list.
ASSIGN
    cust-list.cust-name = "T O T A L"
    cust-list.ly-rev       = tr-lyrev
    cust-list.gesamtumsatz = tr-gesamtumsatz
    cust-list.logiernachte = tr-logiernachte
    cust-list.argtumsatz   = tr-argtumsatz
    cust-list.f-b-umsatz   = tr-f-b-umsatz
    cust-list.sonst-umsatz = tr-sonst-umsatz
    cust-list.ba-umsatz    = tr-ba-umsatz
    cust-list.stayno       = tr-stayno
    cust-list.region       = "zzr"
    cust-list.counter      = counter.

counter = counter + 1.

CREATE cust-list.
ASSIGN
    cust-list.cust-name    = "T  O  T  A  L"
    cust-list.ly-rev       = t-lyrev
    cust-list.gesamtumsatz = t-gesamtumsatz
    cust-list.logiernachte = t-logiernachte
    cust-list.argtumsatz   = t-argtumsatz
    cust-list.f-b-umsatz   = t-f-b-umsatz
    cust-list.sonst-umsatz = t-sonst-umsatz
    cust-list.ba-umsatz    = t-ba-umsatz
    cust-list.stayno       = t-stayno
    cust-list.region       = "zz"
    cust-list.counter      = counter
    cust-list.counterall   = 1.

ASSIGN  
    sort1 = sort-type
    curr-region = "".
