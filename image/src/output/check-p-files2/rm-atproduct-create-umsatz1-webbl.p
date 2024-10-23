
DEFINE TEMP-TABLE rm-atproduct
  FIELD name          AS CHARACTER FORMAT "x(24)"
  FIELD room          AS CHARACTER FORMAT "x(3)"
  FIELD pax           AS CHARACTER FORMAT "x(3)"
  FIELD lodg          AS CHARACTER FORMAT "x(14)"
  FIELD proz          AS CHARACTER FORMAT "x(6)"
  FIELD rm-rate       AS CHARACTER FORMAT "x(14)"
  FIELD mtd-Room      AS CHARACTER FORMAT "x(6)"
  FIELD mtd-pax       AS CHARACTER FORMAT "x(6)"
  FIELD mtd-lodg      AS CHARACTER FORMAT "x(14)"
  FIELD mtdproz       AS CHARACTER FORMAT "x(6)"
  FIELD mtd-rm-rate   AS CHARACTER FORMAT "x(14)"
  FIELD ytd-Room      AS CHARACTER FORMAT "x(6)"
  FIELD ytd-pax       AS CHARACTER FORMAT "x(6)"
  FIELD ytd-lodg      AS CHARACTER FORMAT "x(14)"
  FIELD ytd-proz      AS CHARACTER FORMAT "x(6)"
  FIELD ytd-rm-rate   AS CHARACTER FORMAT "x(14)"
.

DEFINE TEMP-TABLE sales-list
  FIELD sales-id   AS CHAR
  FIELD sales-name AS CHAR.

DEFINE TEMP-TABLE to-list 
  FIELD sales-id   AS CHAR FORMAT "x(2)" 
  FIELD gastnr     AS INTEGER 
  FIELD name       AS CHAR FORMAT "x(24)" 
 
  FIELD room       AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD croom      AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD pax        AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD logis      AS DECIMAL FORMAT ">>>,>>>,>>9" INITIAL 0 
  FIELD proz       AS DECIMAL FORMAT ">>9.99" INITIAL 0 
  FIELD avrgrate   AS DECIMAL FORMAT ">>>,>>>,>>9" INITIAL 0 
 
  FIELD m-room     AS INTEGER FORMAT ">>,>>9" INITIAL 0 
  FIELD mc-room    AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD m-pax      AS INTEGER FORMAT ">>,>>9" INITIAL 0 
  FIELD m-logis    AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD m-proz     AS DECIMAL FORMAT ">>9.99" INITIAL 0 
  FIELD m-avrgrate AS DECIMAL FORMAT ">>>,>>>,>>9" INITIAL 0 
 
  FIELD y-room     AS INTEGER FORMAT ">>>,>>9" INITIAL 0 
  FIELD yc-room    AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD y-pax      AS INTEGER FORMAT ">>>,>>9" INITIAL 0 
  FIELD y-logis    AS DECIMAL FORMAT ">>,>>>,>>>,>>9" INITIAL 0 
  FIELD y-proz     AS DECIMAL FORMAT ">>9.99" INITIAL 0 
  FIELD y-avrgrate AS DECIMAL FORMAT ">>>,>>>,>>9" INITIAL 0. 

DEFINE INPUT PARAMETER ci-date                AS DATE.   
DEFINE INPUT PARAMETER tdate                  AS DATE.   
DEFINE INPUT PARAMETER to-date                AS DATE.   
DEFINE INPUT PARAMETER show-ftd               AS LOGICal.
DEFINE INPUT PARAMETER curr-id-screenvalue    AS CHAR.   
DEFINE INPUT PARAMETER currency-type          AS INT.
DEFINE INPUT PARAMETER cardtype               AS INT.
DEFINE INPUT PARAMETER fdate                  AS DATE.   
DEFINE OUTPUT PARAMETER TABLE FOR rm-atproduct.
DEFINE OUTPUT PARAMETER TABLE FOR sales-list.
/*
DEFINE VARIABLE ci-date                AS DATE INIT 01/14/19.   
DEFINE VARIABLE tdate                  AS DATE INIT ?.  
DEFINE VARIABLE to-date                AS DATE INIT 01/13/19.   
DEFINE VARIABLE show-ftd               AS LOGICAL INIT NO.
DEFINE VARIABLE curr-id-screenvalue    AS CHAR INIT "04 - HANUM".   
DEFINE VARIABLE currency-type          AS INT INIT 1.    
DEFINE VARIABLE cardtype               AS INT INIT 1.    
DEFINE VARIABLE fdate                  AS DATE INIT ?.   
*/

RUN create-umsatz1.

PROCEDURE create-umsatz1: 

DEFINE VARIABLE from-date   AS DATE. 
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE curr-date   AS DATE. 

DEFINE VARIABLE date1       AS DATE.
DEFINE VARIABLE date2       AS DATE.

DEFINE VARIABLE sales-id    AS CHAR.
DEFINE VARIABLE curr-sales  AS CHAR. 
DEFINE VARIABLE sales-name  AS CHAR. 

DEFINE VARIABLE mm          AS INTEGER. 
DEFINE VARIABLE yy          AS INTEGER. 
DEFINE VARIABLE s-pax       AS INTEGER. 
DEFINE VARIABLE s-mpax      AS INTEGER. 
DEFINE VARIABLE s-ypax      AS INTEGER. 
DEFINE VARIABLE s-room      AS INTEGER. 
DEFINE VARIABLE s-mroom     AS INTEGER. 
DEFINE VARIABLE s-yroom     AS INTEGER. 

DEFINE VARIABLE s-lodge     AS DECIMAL. 
DEFINE VARIABLE s-mlodge    AS DECIMAL. 
DEFINE VARIABLE s-ylodge    AS DECIMAL. 
DEFINE VARIABLE s-rate      AS DECIMAL. 
DEFINE VARIABLE s-mrate     AS DECIMAL. 
DEFINE VARIABLE s-yrate     AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL. 
 
DEFINE VARIABLE room       AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE croom      AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE pax        AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE logis      AS DECIMAL FORMAT ">>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE avrgrate   AS DECIMAL FORMAT ">>>,>>>,>>9". 

DEFINE VARIABLE m-room     AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE mc-room    AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE m-pax      AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE m-logis    AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-avrgrate AS DECIMAL FORMAT ">>>,>>>,>>9". 
 
DEFINE VARIABLE y-room     AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE yc-room    AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-pax      AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-logis    AS DECIMAL FORMAT ">>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-avrgrate AS DECIMAL FORMAT ">>>,>>>,>>9". 

DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ind             AS INTEGER. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE foreign-nr      AS INTEGER INITIAL 0 NO-UNDO. 

DEFINE BUFFER bediener1 FOR bediener. 

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
END. 

  ASSIGN
    room    = 0 
    croom   = 0 
    pax     = 0 
    logis   = 0 
    m-room  = 0 
    mc-room = 0 
    m-pax   = 0 
    m-logis = 0 
    y-room  = 0 
    yc-room = 0 
    y-pax   = 0 
    y-logis = 0 
 
    mm        = MONTH(to-date)
    yy        = YEAR(to-date)
    from-date = DATE(1,1,yy)
    curr-date = ?
  . 
  
  IF show-ftd THEN 
      ASSIGN 
        to-date   = tdate.

  FOR EACH rm-atproduct:
    DELETE rm-atproduct.
  END.

  FOR EACH to-list: 
    DELETE to-list. 
  END. 
  
  sales-id = "".
  IF curr-id-screenvalue NE ? THEN
      sales-id = TRIM(ENTRY(1, curr-id-screenvalue, "-")).
  
  IF from-date LT ci-date THEN
  DO:
    date1 = from-date.
    IF to-date LT ci-date THEN date2 = to-date.
    ELSE date2 = ci-date - 1.

    FOR EACH guestat1 WHERE guestat1.datum GE date1
      AND guestat1.datum LE date2
      AND guestat1.logis GT 0 NO-LOCK BY guestat1.datum:
      exchg-rate = 1. 
      IF curr-date NE guestat1.datum AND currency-type = 2 THEN
      DO:
        IF foreign-nr NE 0 THEN 
        DO:    
          FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
            AND exrate.datum = datum NO-LOCK NO-ERROR. 
          IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
        END.
      END.
      FIND FIRST guest WHERE guest.gastnr = guestat1.gastnr NO-LOCK.
      IF cardtype = 3 THEN do-it = YES.
      ELSE do-it = (guest.karteityp = cardtype).
      IF do-it AND sales-id NE "" THEN
        do-it = sales-id = guest.phonetik3.
      
      IF do-it THEN
      DO:
        FIND FIRST to-list WHERE to-list.gastnr = guest.gastnr 
          AND to-list.sales-id = guest.phonetik3 NO-ERROR. 
        IF NOT AVAILABLE to-list THEN 
        DO: 
          CREATE to-list. 
          ASSIGN
            to-list.sales-id = guest.phonetik3
            to-list.gastnr   = guest.gastnr
            to-list.name     = guest.name + ", " + guest.vorname1 + " " 
                             + guest.anrede1 + guest.anredefirma
          . 
        END. 
        IF guestat1.datum = to-date THEN        
          ASSIGN 
            to-list.room   = to-list.room  + guestat1.zimmeranz
            to-list.croom  = to-list.croom + guestat1.betriebsnr 
            to-list.pax    = to-list.pax   + guestat1.persanz
            to-list.logis  = to-list.logis + guestat1.logis / exchg-rate 
            room           = room  + guestat1.zimmeranz 
            croom          = croom + guestat1.betriebsnr 
            pax            = pax   + guestat1.persanz 
            logis          = logis + guestat1.logis / exchg-rate 
          . 
                
        /*5 Jan 09, request BW Medan, fromdate todate*/
        IF (NOT show-ftd AND month(guestat1.datum) = mm AND year(guestat1.datum) = yy)
          OR (show-ftd AND guestat1.datum GE fdate AND guestat1.datum LE to-date) THEN        
          ASSIGN 
            to-list.m-room  = to-list.m-room  + guestat1.zimmeranz 
            to-list.mc-room = to-list.mc-room + guestat1.betriebsnr 
            to-list.m-pax   = to-list.m-pax   + guestat1.persanz
            to-list.m-logis = to-list.m-logis + guestat1.logis / exchg-rate 
            m-room          = m-room  + guestat1.zimmeranz 
            mc-room         = mc-room + guestat1.betriebsnr 
            m-pax           = m-pax   + guestat1.persanz
            m-logis         = m-logis + guestat1.logis / exchg-rate
          .             

        ASSIGN
          to-list.y-room  = to-list.y-room  + guestat1.zimmeranz 
          to-list.yc-room = to-list.yc-room + guestat1.betriebsnr 
          to-list.y-pax   = to-list.y-pax   + guestat1.persanz
          to-list.y-logis = to-list.y-logis + guestat1.logis / exchg-rate 
          y-room          = y-room  + guestat1.zimmeranz 
          yc-room         = yc-room + guestat1.betriebsnr 
          y-pax           = y-pax   + guestat1.persanz
          y-logis         = y-logis + guestat1.logis / exchg-rate 
        .
      END.
    END.
  END.

  IF to-date GE ci-date THEN
  DO:
    IF from-date GE ci-date THEN date1 = from-date.
    ELSE date1 = ci-date.
    date2 = to-date.
  END.
 
  FOR EACH to-list: 
    IF to-list.y-logis = 0 AND to-list.y-room = 0 THEN DELETE to-list. 
    ELSE 
    DO: 
      IF (to-list.room - to-list.croom) NE 0 THEN 
        to-list.avrgrate = to-list.logis / (to-list.room - to-list.croom). 
      IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
        to-list.m-avrgrate = to-list.m-logis / 
          (to-list.m-room - to-list.mc-room). 
      IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
        to-list.y-avrgrate = to-list.y-logis / 
          (to-list.y-room - to-list.yc-room). 
      IF logis NE 0 THEN 
        to-list.proz = to-list.logis / logis * 100. 
     IF m-logis NE 0 THEN 
        to-list.m-proz = to-list.m-logis / m-logis * 100. 
      IF y-logis NE 0 THEN 
        to-list.y-proz = to-list.y-logis / y-logis * 100. 
    END. 
  END. 
 
  curr-sales = "UNKNOWN". 
  FOR EACH to-list NO-LOCK BY to-list.sales-id BY to-list.name: 
    FIND FIRST sales-list WHERE sales-list.sales-id = to-list.sales-id NO-ERROR.
    IF NOT AVAILABLE sales-list THEN
    DO:
      FIND FIRST bediener1 WHERE bediener1.userinit = to-list.sales-id 
        NO-LOCK NO-ERROR. 
      CREATE sales-list.
      ASSIGN sales-list.sales-id = to-list.sales-id.
      IF AVAILABLE bediener1 THEN 
        ASSIGN sales-list.sales-name = bediener1.username.
    END.
    IF sales-id = "" 
       OR (ENTRY(1,curr-id-screenvalue,"-") = to-list.sales-id) THEN
    DO:
      IF curr-sales = "UNKNOWN" THEN 
      DO: 
        s-pax = 0. 
        s-mpax = 0. 
        s-ypax = 0. 
        s-room = 0. 
        s-mroom = 0. 
        s-yroom = 0. 
        s-lodge = 0. 
        s-mlodge = 0. 
        s-ylodge = 0. 
        s-rate = 0. 
        s-mrate = 0. 
        s-yrate = 0. 
        curr-sales = to-list.sales-id. 
        FIND FIRST bediener1 WHERE bediener1.userinit = to-list.sales-id 
          NO-LOCK NO-ERROR. 
        sales-name = STRING(curr-sales,"x(2)") + " - ". 
        IF AVAILABLE bediener1 THEN sales-name = sales-name + bediener1.username. 
        ELSE sales-name = sales-name + "Undefined". 
        CREATE rm-atproduct. 
        rm-atproduct.NAME = STRING(sales-name, "x(24)"). 
      END. 
      IF curr-sales NE to-list.sales-id THEN 
      DO:         
        IF s-room NE 0 THEN s-rate = s-lodge / s-room. 
        IF s-mroom NE 0 THEN s-mrate = s-mlodge / s-mroom. 
        IF s-yroom NE 0 THEN s-yrate = s-ylodge / s-yroom. 
        CREATE rm-atproduct. 
        IF price-decimal = 0 AND currency-type = 1 THEN 
        DO:
          ASSIGN
            rm-atproduct.NAME        = STRING(("Total Sales - " + curr-sales), "x(24)")
            rm-atproduct.room        = STRING(s-room, ">>9")             
            rm-atproduct.pax         = STRING(s-pax, ">>9")              
            rm-atproduct.lodg        = STRING(s-lodge,">>,>>>,>>>,>>9") 
            rm-atproduct.proz        = STRING(0, ">>>>>>")               
            rm-atproduct.rm-rate     = STRING(s-rate, ">>,>>>,>>>,>>9")  
            rm-atproduct.mtd-Room    = STRING(s-mroom, ">>,>>9")         
            rm-atproduct.mtd-pax     = STRING(s-mpax, ">>,>>9")          
            rm-atproduct.mtd-lodg    = STRING(s-mlodge, ">>,>>>,>>>,>>9")
            rm-atproduct.mtdproz     = STRING(0, ">>>>>>")               
            rm-atproduct.mtd-rm-rate = STRING(s-mrate, ">>,>>>,>>>,>>9")    
            rm-atproduct.ytd-Room    = STRING(s-yroom, ">>>,>>9")        
            rm-atproduct.ytd-pax     = STRING(s-ypax, ">>>,>>9")         
            rm-atproduct.ytd-lodg    = STRING(s-ylodge, ">>,>>>,>>>,>>9")
            rm-atproduct.ytd-proz    = STRING(0, ">>>>>>")               
            rm-atproduct.ytd-rm-rate = STRING(s-yrate, ">>,>>>,>>>,>>9")
          .
        END.
        ELSE 
        DO:
          ASSIGN                      
            rm-atproduct.NAME        = STRING(("Total Sales - " + curr-sales), "x(24)")
            rm-atproduct.room        = STRING(s-room, ">>9")               
            rm-atproduct.pax         = STRING(s-pax, ">>9")                
            rm-atproduct.lodg        = STRING(s-lodge, ">>>,>>>,>>9.99")   
            rm-atproduct.proz        = STRING(0, ">>>>>>")                 
            rm-atproduct.rm-rate     = STRING(s-rate, ">>>,>>>,>>9.99")    
            rm-atproduct.mtd-Room    = STRING(s-mroom, ">>,>>9")           
            rm-atproduct.mtd-pax     = STRING(s-mpax, ">>,>>9")            
            rm-atproduct.mtd-lodg    = STRING(s-mlodge, ">,>>>,>>>,>>9.99")
            rm-atproduct.mtdproz     = STRING(0, ">>>>>>")                 
            rm-atproduct.mtd-rm-rate = STRING(s-mrate, ">>>,>>>,>>9.99")   
            rm-atproduct.ytd-Room    = STRING(s-yroom, ">>>,>>9")          
            rm-atproduct.ytd-pax     = STRING(s-ypax, ">>>,>>9")           
            rm-atproduct.ytd-lodg    = STRING(s-ylodge, ">>>,>>>,>>9.99")  
            rm-atproduct.ytd-proz    = STRING(0, ">>>>>>")                 
            rm-atproduct.ytd-rm-rate = STRING(s-yrate, ">>>,>>>,>>9.99")  
          .
        END.        
        CREATE rm-atproduct. 
        curr-sales = to-list.sales-id. 
        FIND FIRST bediener1 WHERE bediener1.userinit = to-list.sales-id 
          NO-LOCK NO-ERROR. 
        sales-name = STRING(curr-sales,"x(2)") + " - ". 
        IF AVAILABLE bediener1 THEN sales-name = sales-name + bediener1.username. 
        ELSE sales-name = sales-name + "Undefined". 
        CREATE rm-atproduct. 
        rm-atproduct.NAME = STRING(sales-name, "x(24)"). 
        s-pax = 0. 
        s-mpax = 0. 
        s-ypax = 0. 
        s-room = 0. 
        s-mroom = 0. 
        s-yroom = 0. 
        s-lodge = 0. 
        s-mlodge = 0. 
        s-ylodge = 0. 
        s-rate = 0. 
        s-mrate = 0. 
        s-yrate = 0. 
      END. 
      s-pax = s-pax + to-list.pax. 
      s-mpax = s-mpax + to-list.m-pax. 
      s-ypax = s-ypax + to-list.y-pax. 
      s-room = s-room + to-list.room. 
      s-mroom = s-mroom + to-list.m-room. 
      s-yroom = s-yroom + to-list.y-room. 
      s-lodge = s-lodge + to-list.logis. 
      s-mlodge = s-mlodge + to-list.m-logis. 
      s-ylodge = s-ylodge + to-list.y-logis. 
 
      CREATE rm-atproduct. 
      IF price-decimal = 0 AND currency-type = 1 THEN
      DO:
        ASSIGN                      
          rm-atproduct.NAME        = STRING(to-list.name, "x(24)")
          rm-atproduct.room        = STRING(to-list.room, ">>9")                  
          rm-atproduct.pax         = STRING(to-list.pax, ">>9")                   
          rm-atproduct.lodg        = STRING(to-list.logis, ">>,>>>,>>>,>>9")      
          rm-atproduct.proz        = STRING(to-list.proz, ">>9.99")               
          rm-atproduct.rm-rate     = STRING(to-list.avrgrate, ">>,>>>,>>>,>>9")   
          rm-atproduct.mtd-Room    = STRING(to-list.m-room, ">>,>>9")             
          rm-atproduct.mtd-pax     = STRING(to-list.m-pax, ">>,>>9")              
          rm-atproduct.mtd-lodg    = STRING(to-list.m-logis, ">>,>>>,>>>,>>9")    
          rm-atproduct.mtdproz     = STRING(to-list.m-proz, ">>9.99")             
          rm-atproduct.mtd-rm-rate = STRING(to-list.m-avrgrate, ">>,>>>,>>>,>>9") 
          rm-atproduct.ytd-Room    = STRING(to-list.y-room, ">>>,>>9")            
          rm-atproduct.ytd-pax     = STRING(to-list.y-pax, ">>>,>>9")             
          rm-atproduct.ytd-lodg    = STRING(to-list.y-logis, ">>,>>>,>>>,>>9")    
          rm-atproduct.ytd-proz    = STRING(to-list.y-proz, ">>9.99")             
          rm-atproduct.ytd-rm-rate = STRING(to-list.y-avrgrate, ">>,>>>,>>>,>>9")
        .
      END.      
      ELSE 
      DO:
        ASSIGN                      
          rm-atproduct.NAME        = STRING(to-list.name, "x(24)")
          rm-atproduct.room        = STRING(to-list.room, ">>9")                  
          rm-atproduct.pax         = STRING(to-list.pax, ">>9")                   
          rm-atproduct.lodg        = STRING(to-list.logis, ">>>,>>>,>>9.99")      
          rm-atproduct.proz        = STRING(to-list.proz, ">>9.99")               
          rm-atproduct.rm-rate     = STRING(to-list.avrgrate, ">>>,>>>,>>9.99")   
          rm-atproduct.mtd-Room    = STRING(to-list.m-room, ">>,>>9")             
          rm-atproduct.mtd-pax     = STRING(to-list.m-pax, ">>,>>9")              
          rm-atproduct.mtd-lodg    = STRING(to-list.m-logis, ">,>>>,>>>,>>9.99")  
          rm-atproduct.mtdproz     = STRING(to-list.m-proz, ">>9.99")             
          rm-atproduct.mtd-rm-rate = STRING(to-list.m-avrgrate, ">>>,>>>,>>9.99") 
          rm-atproduct.ytd-Room    = STRING(to-list.y-room, ">>>,>>9")            
          rm-atproduct.ytd-pax     = STRING(to-list.y-pax, ">>>,>>9")             
          rm-atproduct.ytd-lodg    = STRING(to-list.y-logis, ">>>,>>>,>>9.99") 
          rm-atproduct.ytd-proz    = STRING(to-list.y-proz, ">>9.99")             
          rm-atproduct.ytd-rm-rate = STRING(to-list.y-avrgrate, ">>>,>>>,>>9.99")
        .
      END.
    END.
  END.

  IF s-room NE 0 THEN s-rate = s-lodge / s-room. 
  IF s-mroom NE 0 THEN s-mrate = s-mlodge / s-mroom. 
  IF s-yroom NE 0 THEN s-yrate = s-ylodge / s-yroom. 
  CREATE rm-atproduct. 
  IF price-decimal = 0 AND currency-type = 1 THEN
  DO:
    ASSIGN                      
      rm-atproduct.NAME        = STRING(("Total Sales - " + curr-sales), "x(24)")
      rm-atproduct.room        = STRING(s-room, ">>9")             
      rm-atproduct.pax         = STRING(s-pax, ">>9")              
      rm-atproduct.lodg        = STRING(s-lodge, ">>,>>>,>>>,>>9") 
      rm-atproduct.proz        = STRING(0, ">>>>>>")               
      rm-atproduct.rm-rate     = STRING(s-rate, ">>,>>>,>>>,>>9")  
      rm-atproduct.mtd-Room    = STRING(s-mroom, ">>,>>9")         
      rm-atproduct.mtd-pax     = STRING(s-mpax, ">>,>>9")          
      rm-atproduct.mtd-lodg    = STRING(s-mlodge, ">>,>>>,>>>,>>9")
      rm-atproduct.mtdproz     = STRING(0, ">>>>>>")               
      rm-atproduct.mtd-rm-rate = STRING(s-mrate, ">>,>>>,>>>,>>9") 
      rm-atproduct.ytd-Room    = STRING(s-yroom, ">>>,>>9")        
      rm-atproduct.ytd-pax     = STRING(s-ypax, ">>>,>>9")         
      rm-atproduct.ytd-lodg    = STRING(s-ylodge, ">>,>>>,>>>,>>9")
      rm-atproduct.ytd-proz    = STRING(0, ">>>>>>")               
      rm-atproduct.ytd-rm-rate = STRING(s-yrate, ">>,>>>,>>>,>>9")
    .                           
  END.
  ELSE 
  DO:
    ASSIGN                      
      rm-atproduct.NAME        = STRING(("Total Sales - " + curr-sales), "x(24)") 
      rm-atproduct.room        = STRING(s-room, ">>9")               
      rm-atproduct.pax         = STRING(s-pax, ">>9")                
      rm-atproduct.lodg        = STRING(s-lodge, ">>>,>>>,>>9.99")   
      rm-atproduct.proz        = STRING(0, ">>>>>>")                 
      rm-atproduct.rm-rate     = STRING(s-rate, ">>>,>>>,>>9.99")    
      rm-atproduct.mtd-Room    = STRING(s-mroom, ">>,>>9")           
      rm-atproduct.mtd-pax     = STRING(s-mpax, ">>,>>9")            
      rm-atproduct.mtd-lodg    = STRING(s-mlodge, ">,>>>,>>>,>>9.99")
      rm-atproduct.mtdproz     = STRING(0, ">>>>>>")                 
      rm-atproduct.mtd-rm-rate = STRING(s-mrate, ">>>,>>>,>>9.99")   
      rm-atproduct.ytd-Room    = STRING(s-yroom, ">>>,>>9")          
      rm-atproduct.ytd-pax     = STRING(s-ypax, ">>>,>>9")           
      rm-atproduct.ytd-lodg    = STRING(s-ylodge, ">>>,>>>,>>9.99")  
      rm-atproduct.ytd-proz    = STRING(0, ">>>>>>")                 
      rm-atproduct.ytd-rm-rate = STRING(s-yrate, ">>>,>>>,>>9.99") 
    .                           
  END.
 
  avrgrate = 0. 
  IF (room - croom) NE 0 THEN avrgrate = logis / (room - croom). 
  m-avrgrate = 0. 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  y-avrgrate = 0. 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 
  create rm-atproduct. 
  create rm-atproduct. 
  IF price-decimal = 0 AND currency-type = 1 THEN 
  DO:
    ASSIGN                      
      rm-atproduct.NAME        = STRING("Grand Total Sales", "x(24)")
      rm-atproduct.room        = STRING(room, ">>9")                  
      rm-atproduct.pax         = STRING(pax, ">>9")                   
      rm-atproduct.lodg        = STRING(logis, ">>,>>>,>>>,>>9")      
      rm-atproduct.proz        = STRING(100, ">>9.99")                
      rm-atproduct.rm-rate     = STRING(avrgrate, ">>,>>>,>>>,>>9")   
      rm-atproduct.mtd-Room    = STRING(m-room, ">>,>>9")             
      rm-atproduct.mtd-pax     = STRING(m-pax, ">>,>>9")              
      rm-atproduct.mtd-lodg    = STRING(m-logis, ">>,>>>,>>>,>>9")    
      rm-atproduct.mtdproz     = STRING(100, ">>9.99")                
      rm-atproduct.mtd-rm-rate = STRING(m-avrgrate, ">>,>>>,>>>,>>9") 
      rm-atproduct.ytd-Room    = STRING(y-room, ">>>,>>9")            
      rm-atproduct.ytd-pax     = STRING(y-pax, ">>>,>>9")             
      rm-atproduct.ytd-lodg    = STRING(y-logis, ">>,>>>,>>>,>>9")    
      rm-atproduct.ytd-proz    = STRING(100, ">>9.99")                
      rm-atproduct.ytd-rm-rate = STRING(y-avrgrate, ">>,>>>,>>>,>>9")
    .                           
  END.
  ELSE 
  DO:
    ASSIGN                      
      rm-atproduct.NAME        = STRING("T o t a l", "x(24)")
      rm-atproduct.room        = STRING(room, ">>9")                 
      rm-atproduct.pax         = STRING(pax, ">>9")                  
      rm-atproduct.lodg        = STRING(logis, ">>>,>>>,>>9.99")     
      rm-atproduct.proz        = STRING(100, ">>9.99")               
      rm-atproduct.rm-rate     = STRING(avrgrate, ">>>,>>>,>>9.99")  
      rm-atproduct.mtd-Room    = STRING(m-room, ">>,>>9")            
      rm-atproduct.mtd-pax     = STRING(m-pax, ">>,>>9")             
      rm-atproduct.mtd-lodg    = STRING(m-logis, ">,>>>,>>>,>>9.99") 
      rm-atproduct.mtdproz     = STRING(100, ">>9.99")               
      rm-atproduct.mtd-rm-rate = STRING(m-avrgrate, ">>>,>>>,>>9.99")
      rm-atproduct.ytd-Room    = STRING(y-room, ">>>,>>9")           
      rm-atproduct.ytd-pax     = STRING(y-pax, ">>>,>>9")            
      rm-atproduct.ytd-lodg    = STRING(y-logis, ">>>,>>>,>>9.99")   
      rm-atproduct.ytd-proz    = STRING(100, ">>9.99")               
      rm-atproduct.ytd-rm-rate = STRING(y-avrgrate, ">>>,>>>,>>9.99")
    .
  END.
END. 


