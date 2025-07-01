DEFINE TEMP-TABLE print-list
    FIELD resnr         AS INTEGER
    FIELD reslinnr      AS INTEGER
    FIELD gastnr        AS INTEGER
    FIELD resname       AS CHARACTER FORMAT "x(36)"
    FIELD guesttitle    AS CHARACTER FORMAT "x(36)"
    FIELD guestfname    AS CHARACTER FORMAT "x(36)"
    FIELD guestlname    AS CHARACTER FORMAT "x(36)"
    FIELD guestemail    AS CHARACTER FORMAT "x(36)"
    FIELD guesttelp     AS CHARACTER FORMAT "x(14)"
    FIELD checkin       AS DATE FORMAT "99/99/9999"
    FIELD checkout      AS DATE FORMAT "99/99/9999"
    FIELD roomtype      AS CHARACTER FORMAT "x(4)"
    FIELD roomtypebez   AS CHARACTER FORMAT "x(30)"
    FIELD roomrate      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"
    FIELD currency      AS CHARACTER
    FIELD username      AS CHARACTER FORMAT "x(20)"
    FIELD rescomment    AS CHARACTER FORMAT "x(100)"
    FIELD maincomment   AS CHARACTER FORMAT "x(100)"
    FIELD contactname   AS CHARACTER FORMAT "x(50)"
    FIELD contacttelp   AS CHARACTER FORMAT "x(50)"
    FIELD contactemail  AS CHARACTER FORMAT "x(50)"
    FIELD totalroom     AS INTEGER INIT 0
    FIELD pax           AS INTEGER
    FIELD checkintime   AS CHARACTER FORMAT "x(5)"
    FIELD checkouttime  AS CHARACTER FORMAT "x(5)"
    FIELD billinstuct   AS CHARACTER FORMAT "x(25)"
    FIELD creditcard    AS CHARACTER FORMAT "x(25)"
    FIELD total-rate     AS DECIMAL
    FIELD room-night    AS INTEGER INIT 0 
    FIELD argt          AS CHARACTER FORMAT "x(3)" 
    FIELD tot-pay       AS DECIMAL     
    FIELD flight-nr     AS CHARACTER 
    FIELD kind1         AS INTEGER
    FIELD depositgef    AS DECIMAL
    FIELD depositbez    AS DECIMAL
    FIELD address       AS CHAR
    FIELD bedsetup      AS CHARACTER
    FIELD all-rmtype    AS CHAR FORMAT "x(150)"
    FIELD all-rmrate    AS CHAR FORMAT "x(150)"
    FIELD all-totrate   AS CHAR FORMAT "x(150)"
    FIELD bedsetup-rate AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    FIELD all-guest     AS CHAR FORMAT "x(250)"
    FIELD cutoff-days   AS INTEGER
    FIELD all-total     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    .

DEFINE TEMP-TABLE setup-list
    FIELD nr     AS INTEGER
    FIELD CHAR   AS CHAR FORMAT "x(1)"
    FIELD ptexte AS CHAR.


DEFINE INPUT PARAMETER resnumber AS INTEGER.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR print-list.

/*      
DEFINE VARIABLE resnumber AS INT INIT 14708.
DEFINE VARIABLE user-init AS CHAR INIT "01".
*/

DEFINE VARIABLE room AS INT INIT 0.
DEFINE VARIABLE rmtype AS CHAR FORMAT "x(150)".
DEFINE VARIABLE pricerm AS CHAR FORMAT "x(150)".
DEFINE VARIABLE tot-rm  AS CHAR FORMAT "x(150)".
DEFINE VARIABLE allgst  AS CHAR FORMAT "x(150)".
DEFINE VARIABLE all-total AS DECIMAL.
DEFINE VARIABLE night   AS INT.
DEFINE VARIABLE co AS INT.
DEFINE BUFFER t-guest FOR guest.
DEFINE BUFFER t-zim   FOR zimkateg.
DEFINE BUFFER t-res   FOR res-line.

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.

FOR EACH paramtext WHERE paramtext.txtnr GE 9201   
    AND paramtext.txtnr LE 9299 NO-LOCK:   
    CREATE setup-list.   
    setup-list.nr = paramtext.txtnr - 9199.   
    setup-list.char = SUBSTR(paramtext.notes,1,1). 
    setup-list.ptexte = paramtext.ptexte.
END.   

/*gerald penambahan active-flag karna cancel tetap kehitung FE48BC*/
/*gerald penambahan validasi resstatus 7CA981*/
/*ragung penambahan variable dan grouping 6768D3*/
/*ragung penambahan variable untuk show all guest D8E38F*/
FOR EACH res-line WHERE res-line.resnr EQ resnumber AND res-line.active-flag LE 1 
    AND res-line.resstatus NE 11 NO-LOCK:
     FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1 NO-LOCK NO-ERROR.
     FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
     FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
     FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ res-line.zikatnr NO-LOCK NO-ERROR.
     FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ res-line.betriebsnr NO-LOCK NO-ERROR.
    
    IF AVAILABLE waehrung THEN
    DO: 
        CREATE print-list.
        ASSIGN 
        print-list.resnr         = res-line.resnr
        print-list.reslinnr      = res-line.reslinnr
        print-list.gastnr        = res-line.gastnrmember
        print-list.resname       = res-line.resname
        /*print-list.resname       = reservation.NAME   */      
        print-list.guesttitle    = guest.anrede1
        print-list.guestfname    = guest.vorname1
        print-list.guestlname    = guest.NAME 
        print-list.guestemail    = guest.email-adr
        print-list.guesttelp     = guest.mobil-telefon
        print-list.checkin       = res-line.ankunft
        print-list.checkout      = res-line.abreise
        print-list.roomtype      = zimkateg.kurzbez
        print-list.roomtypebez   = zimkateg.bezeichnung 
        print-list.currency      = waehrung.wabkurz
        print-list.username      = bediener.username
        print-list.rescomment    = res-line.bemerk
        print-list.maincomment   = reservation.bemerk
        print-list.totalroom     = res-line.zimmeranz
        print-list.pax           = res-line.erwachs + res-line.gratis + res-line.kind1 +
                                  res-line.kind2 + res-line.l-zuordnung[4]
        print-list.checkintime   = STRING(res-line.ankzeit, "HH:MM") 
        print-list.checkouttime  = STRING(res-line.abreisezeit, "HH:MM")  
        print-list.creditcard    = guest.ausweis-nr2
        /*print-list.total-rate     = res-line.anztage * res-line.zipreis*/   /* Gerald 200220 */
        /*gerald 130820*/       
        print-list.room-night    = (res-line.abreise - res-line.ankunft) * res-line.zimmeranz
        print-list.argt          = res-line.arrangement
        print-list.flight-nr     = res-line.flight-nr
        print-list.kind1         = res-line.kind1
        print-list.depositgef    = reservation.depositgef
        print-list.depositbez    = reservation.depositbez + reservation.depositbez2
        print-list.address       = guest.adresse1 + guest.adresse2
        print-list.bedsetup      = setup-list.ptexte
        print-list.cutoff-days   = reservation.point
        .
        
        FIND FIRST fixleist WHERE fixleist.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE fixleist THEN DO:
            print-list.bedsetup-rate = fixleist.betrag.
        END.
        ELSE DO:
            print-list.bedsetup-rate = 0.
        END.

        /* Add by Gerald RoomRate untuk OTA jadi 0*/
        FIND FIRST t-guest WHERE t-guest.gastnr EQ res-line.gastnr NO-ERROR.
        IF t-guest.karteityp = 2 THEN
        DO:
            print-list.roomrate   = 0.
            print-list.total-rate = 0.
        END.
        ELSE
        DO:
            print-list.roomrate   = res-line.zipreis.
            print-list.total-rate = (res-line.zipreis * print-list.room-night) +  print-list.bedsetup-rate. /* * print-list.totalroom */
        END. 
        
        FIND FIRST queasy WHERE queasy.KEY = 9 AND queasy.number1 EQ INT(res-line.CODE) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            print-list.billinstuct  = queasy.char1.
        END.

        FIND FIRST akt-kon WHERE akt-kon.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE akt-kon THEN DO:
            print-list.contactname  = akt-kon.NAME. 
            print-list.contacttelp  = akt-kon.telefon.
            print-list.contactemail = akt-kont.email-adr.
        END.
        ELSE DO:
            print-list.contactname  = "".
            print-list.contacttelp  = "".
            print-list.contactemail = "".
        END.                
    END.
    
    /*gerald tot-pay*/
    FOR EACH reslin-queasy WHERE reslin-queasy.resnr EQ res-line.resnr 
        AND reslin-queasy.reslinnr EQ res-line.reslinnr AND reslin-queasy.deci1 NE 0
        NO-LOCK.
        ASSIGN 
        print-list.tot-pay = print-list.tot-pay + reslin-queasy.deci1.
        
        IF (reslin-queasy.date2 - reslin-queasy.date1) EQ 0 THEN night = 1.
        ELSE night = (reslin-queasy.date2 - reslin-queasy.date1) + 1.
        pricerm = pricerm + STRING(DECIMAL(reslin-queasy.deci1),"->,>>>,>>>,>>>,>>9.99") + ":".
        tot-rm  = tot-rm + STRING(DECIMAL(reslin-queasy.deci1 * night),"->,>>>,>>>,>>>,>>9.99") + ":".
        all-total = all-total + (reslin-queasy.deci1 * night). 
    END.
    /*end gerald*/

    /*ragung*/                                                                                          
    FOR EACH t-zim WHERE t-zim.zikatnr EQ res-line.zikatnr NO-LOCK:                                     
        rmtype = rmtype + t-zim.bezeichnung + ":".                                                      
    END.

    FOR EACH t-guest WHERE t-guest.gastnr EQ res-line.gastnr NO-LOCK:
        IF t-guest.karteityp = 2 THEN
        DO:
            pricerm = "".
            tot-rm  = "".
        END.
        /*ELSE
        DO:
            pricerm = pricerm + STRING(DECIMAL(res-line.zipreis),"->,>>>,>>>,>>>,>>9.99") + ":".
            tot-rm  = tot-rm + STRING(DECIMAL(res-line.zipreis * print-list.room-night),"->,>>>,>>>,>>>,>>9.99") + ":".
        END.*/
    END.
    
    FOR EACH t-res WHERE t-res.resnr EQ res-line.resnr NO-LOCK:
        allgst = allgst + t-res.NAME + " : ".
    END.
    
    IF pricerm NE "" THEN print-list.all-rmrate   = pricerm.
    ELSE print-list.all-rmrate = STRING(DECIMAL(print-list.roomrate),"->,>>>,>>>,>>>,>>9.99").
    
    IF tot-rm NE "" THEN print-list.all-totrate  = tot-rm.
    ELSE print-list.all-totrate  =  STRING(DECIMAL(print-list.total-rate),"->,>>>,>>>,>>>,>>9.99").
    
    print-list.all-total    = all-total.
    print-list.all-rmtype   = rmtype.
    print-list.all-guest    = allgst.
    
END.
