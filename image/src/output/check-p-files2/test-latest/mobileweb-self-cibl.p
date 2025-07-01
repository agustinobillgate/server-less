DEFINE TEMP-TABLE arrival-guest
    FIELD i-counter     AS INTEGER
    FIELD gastno        AS INTEGER
    FIELD resnr         AS INTEGER 
    FIELD reslinnr      AS INTEGER 
    FIELD gast          AS CHAR    COLUMN-LABEL "Guest Name"
    FIELD ci            AS DATE    COLUMN-LABEL "C/I Date"
    FIELD co            AS DATE    COLUMN-LABEL "C/O Date"
    FIELD rmtype        AS CHAR    COLUMN-LABEL "Room Type"
    FIELD zinr          AS CHAR    COLUMN-LABEL "Room No"
    FIELD argt          AS CHAR    COLUMN-LABEL "Argt"
    FIELD adult         AS CHAR COLUMN-LABEL "Adult"
    FIELD child         AS CHAR COLUMN-LABEL "Child"
    FIELD rmtype-str    AS CHAR
    FIELD room-sharer   AS LOGICAL INITIAL NO
    FIELD pre-checkin   AS LOGICAL INITIAL NO
    FIELD argt-str      AS CHAR
    FIELD preference    AS CHAR
    FIELD new-zinr      AS LOGICAL
    FIELD zikatnr       AS INTEGER
    FIELD l-selected    AS LOGICAL
    FIELD kontakt-nr    AS INTEGER
    FIELD room-stat     AS INTEGER INITIAL 0
    FIELD res-status    AS INTEGER INITIAL 0.


DEFINE TEMP-TABLE arrival-guestlist
    FIELD i-counter       AS INTEGER
    FIELD gastno          AS INTEGER
    FIELD resnr           AS INTEGER 
    FIELD reslinnr        AS INTEGER 
    FIELD gast            AS CHAR COLUMN-LABEL "Guest Name"
    FIELD ci              AS DATE COLUMN-LABEL "C/I Date"
    FIELD co              AS DATE COLUMN-LABEL "C/O Date"
    FIELD rmtype          AS CHAR COLUMN-LABEL "Room Type"
    FIELD zinr            AS CHAR COLUMN-LABEL "Room No"
    FIELD argt            AS CHAR COLUMN-LABEL "Argt"
    FIELD adult           AS CHAR COLUMN-LABEL "Adult"
    FIELD child           AS CHAR COLUMN-LABEL "Child"
    FIELD rmtype-str      AS CHAR
    FIELD room-sharer     AS LOGICAL INITIAL NO
    FIELD pre-checkin     AS LOGICAL INITIAL NO
    FIELD argt-str        AS CHAR
    FIELD preference      AS CHAR
    FIELD new-zinr        AS LOGICAL
    FIELD zikatnr         AS INTEGER
    FIELD l-selected      AS LOGICAL
    FIELD kontakt-nr      AS INTEGER
    FIELD guest-email     AS CHAR
    FIELD guest-phnumber  AS CHAR
    FIELD guest-nation    AS CHAR
    FIELD guest-country   AS CHAR
    FIELD guest-region    AS CHAR
    FIELD room-preference AS CHAR
    FIELD purposeofstay   AS CHAR
    FIELD room-status     AS CHAR
    FIELD image-flag      AS CHAR
    FIELD currency-usage  AS CHAR
    FIELD key-generated   AS LOGICAL INIT NO
    FIELD preAuth-flag    AS LOGICAL INIT NO
    FIELD res-status      AS CHAR
    FIELD ifdata-sent     AS LOGICAL INIT NO
    FIELD param-broadcast AS CHAR
    FIELD wifi-password   AS CHAR
    FIELD payment-method  AS CHAR
    FIELD payment-status  AS CHAR
    FIELD payment-channel  AS CHAR
    FIELD transid-merchant AS CHAR
    FIELD vehicle-number  AS CHAR
    FIELD smoking-room    AS LOGICAL
    /*FD*/
    FIELD amount-depo     AS DECIMAL
    FIELD depo-paid1      AS DECIMAL
    FIELD depo-paid2      AS DECIMAL
    FIELD depo-balance    AS DECIMAL
    .
/**/
DEFINE INPUT PARAMETER co-date    AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER book-code  AS CHAR    NO-UNDO.

DEFINE INPUT PARAMETER ch-name    AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER early-ci   AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER max-room   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER citime     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER groupFlag  AS LOGICAL NO-UNDO.

DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR arrival-guestlist.
/*
DEFINE VARIABLE co-date     AS DATE    NO-UNDO INIT 07/21/20.
DEFINE VARIABLE book-code   AS CHAR    NO-UNDO INIT "62295".
DEFINE VARIABLE ch-name     AS CHAR    NO-UNDO INIT " ".
DEFINE VARIABLE early-ci    AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE max-room    AS INTEGER NO-UNDO INIT 1.
DEFINE VARIABLE citime      AS CHAR    NO-UNDO INIT "14:10".
DEFINE VARIABLE groupFlag   AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE mess-result AS CHAR.
*/
DEFINE VARIABLE delete-it  AS INTEGER NO-UNDO.
DEFINE VARIABLE err-code   AS INTEGER NO-UNDO.
DEFINE VARIABLE ercode     AS INTEGER NO-UNDO.
DEFINE VARIABLE i          AS INTEGER.
DEFINE VARIABLE tmp-char   AS CHAR.
DEFINE VARIABLE ci-time    AS CHAR.
DEFINE VARIABLE depo-bal   AS DECIMAL NO-UNDO INITIAL 0. /*FD June 20, 2022*/
DEFINE VARIABLE res-flag   AS LOGICAL INITIAL NO.

DEFINE BUFFER buff-resline FOR res-line.

IF co-date EQ ? THEN
DO:
    mess-result = "99 - CheckOut Date Is Mandatory!".
    RETURN.
END.
IF citime EQ "" OR citime EQ ? THEN
DO:
    mess-result = "99 - CheckIn Time Is Mandatory! - HH:MM".
    RETURN.
END.
IF LENGTH(citime) NE 5 THEN
DO:
    mess-result = "99 - CheckIn Time Format Is Invalid, should be [HH:MM]".
    RETURN.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 AND queasy.number2 EQ 11 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    IF queasy.logi1 EQ YES THEN
    DO:
         ci-time = queasy.char3.
         IF citime LT ci-time THEN
         DO:
             mess-result = "9 - To Early For CheckIn your time is under of earliest checkin time at : " + ci-time + ", Please Go to Front-Desk!".
             RETURN.
         END.
    END.
    ELSE
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 AND queasy.number2 EQ 2 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN ci-time = queasy.char3.
        ELSE ci-time = "13:00".
        
        IF citime LT ci-time THEN
        DO:
            mess-result = "9 - Early CheckIn Not Possible in MCI, Please Go to Front-Desk!".
            RETURN.
        END.
    END.
END.


RUN search-reservationbl.p (co-date,book-code,ch-name,early-ci,1,
                     citime,groupFlag, OUTPUT delete-it, OUTPUT ercode,
                     OUTPUT TABLE arrival-guest). 

IF delete-it EQ 5 THEN
DO:
    mess-result = "5 - Group CheckIn Not Possible in MCI, Please Go to Front-Desk!".
    RETURN.
END.
IF delete-it EQ 2 THEN
DO:
    mess-result = "2 - Reservation Not Splitted Yet, CheckIn Not Possible in MCI, Please Go to Front-Desk!".
    RETURN.
END.
/**/
FIND FIRST arrival-guest NO-ERROR.
IF NOT AVAILABLE arrival-guest THEN
DO:
    mess-result = "1 - Reservation Not Found".
    RETURN.
END.


RUN iproom-assignmentbl.p (INPUT-OUTPUT TABLE arrival-guest, OUTPUT err-code).

IF err-code EQ 1 THEN
DO:
    mess-result = "01 - Room Not Available or Occupied with other reservation, Please Go to Front-Desk!".
END.
IF err-code EQ 2 THEN
DO:
    mess-result = "02 - Room Status still not available, Please Go to Front-Desk!".
END.
IF err-code EQ 0 AND delete-it EQ 0 THEN
DO:
    mess-result = "0 - Find Reservation Success With Room Assignment!".
END.

FOR EACH arrival-guest:

    CREATE arrival-guestlist.
    ASSIGN arrival-guestlist.i-counter    = arrival-guest.i-counter     
           arrival-guestlist.gastno       = arrival-guest.gastno      
           arrival-guestlist.resnr        = arrival-guest.resnr       
           arrival-guestlist.reslinnr     = arrival-guest.reslinnr    
           arrival-guestlist.gast         = arrival-guest.gast        
           arrival-guestlist.ci           = arrival-guest.ci          
           arrival-guestlist.co           = arrival-guest.co          
           arrival-guestlist.rmtype       = arrival-guest.rmtype      
           arrival-guestlist.zinr         = arrival-guest.zinr        
           arrival-guestlist.argt         = arrival-guest.argt        
           arrival-guestlist.adult        = arrival-guest.adult       
           arrival-guestlist.child        = arrival-guest.child       
           arrival-guestlist.rmtype-str   = arrival-guest.rmtype-str  
           arrival-guestlist.room-sharer  = arrival-guest.room-sharer 
           arrival-guestlist.pre-checkin  = arrival-guest.pre-checkin 
           arrival-guestlist.argt-str     = arrival-guest.argt-str    
           arrival-guestlist.preference   = arrival-guest.preference  
           arrival-guestlist.new-zinr     = arrival-guest.new-zinr    
           arrival-guestlist.zikatnr      = arrival-guest.zikatnr     
           arrival-guestlist.l-selected   = arrival-guest.l-selected  
           arrival-guestlist.kontakt-nr   = arrival-guest.kontakt-nr. 

    IF arrival-guest.room-stat EQ 0 THEN arrival-guestlist.room-status = "0 Ready To Checkin".
    IF arrival-guest.room-stat EQ 1 THEN arrival-guestlist.room-status = "1 Room Already assign or Overlapping".
    IF arrival-guest.room-stat EQ 2 THEN arrival-guestlist.room-status = "2 Room Status Not Ready To Checkin".
    IF arrival-guest.room-stat EQ 3 THEN arrival-guestlist.room-status = "3 Room With Type Selected Not Available".

    FIND FIRST guestbook WHERE guestbook.gastnr EQ arrival-guest.gastno NO-LOCK NO-ERROR.
    IF AVAILABLE guestbook THEN 
         arrival-guestlist.image-flag = "0 image id already exist".
    ELSE arrival-guestlist.image-flag = "1 image id still empty".

    FIND FIRST res-line WHERE res-line.resnr EQ arrival-guestlist.resnr AND res-line.reslinnr EQ arrival-guestlist.reslinnr NO-LOCK NO-ERROR.
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK. 
    arrival-guestlist.currency-usage = waehrung.wabkurz.

    IF res-line.betrieb-gast NE 0 THEN arrival-guestlist.key-generated = YES.

    IF arrival-guest.res-status EQ 0 THEN arrival-guestlist.res-status = "0 - Guest Not Checkin".
    ELSE arrival-guestlist.res-status = "1 - Guest Already Checkin".
END.

FOR EACH arrival-guestlist:
    FIND FIRST guest WHERE guest.gastnr EQ arrival-guestlist.gastno NO-LOCK NO-ERROR.
    FIND FIRST res-line WHERE res-line.resnr EQ arrival-guestlist.resnr AND res-line.reslinnr EQ arrival-guestlist.reslinnr NO-LOCK NO-ERROR.

    ASSIGN arrival-guestlist.guest-email     = guest.email-adr
           arrival-guestlist.guest-phnumber  = guest.mobil-telefon
           arrival-guestlist.guest-nation    = guest.nation1
           arrival-guestlist.guest-country   = guest.land
           arrival-guestlist.guest-region    = guest.geburt-ort2.


    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
        tmp-char = ENTRY(i,res-line.zimmer-wunsch,";").
        IF tmp-char MATCHES "*ROOMREF*" THEN
        DO:
            arrival-guestlist.room-preference = ENTRY(4,tmp-char,"|").
            arrival-guestlist.room-preference = ENTRY(2,room-preference,"=").
        END.

        IF tmp-char MATCHES "*SEGM_PUR*" THEN
        DO:
            arrival-guestlist.purposeofstay = SUBSTRING(tmp-char,9,1).
            FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.number1 EQ INT(arrival-guestlist.purposeofstay) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            arrival-guestlist.purposeofstay = queasy.char3.
        END.

        IF tmp-char MATCHES "*VN=*" THEN
        DO:
            arrival-guestlist.vehicle-number = ENTRY(2,tmp-char,"=").
        END.

        /*IF tmp-char MATCHES "*PREAUTHCC*" THEN arrival-guestlist.preAuth-flag = YES.*/
    END.

    FIND FIRST INTERFACE WHERE INTERFACE.KEY EQ 50 AND INTERFACE.resnr EQ arrival-guestlist.resnr
         AND INTERFACE.reslinnr EQ arrival-guestlist.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE INTERFACE THEN arrival-guestlist.ifdata-sent = YES. 

    FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 AND queasy.number2 EQ 12 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        IF queasy.logi1 EQ YES THEN
        DO:
            ASSIGN 
                arrival-guestlist.wifi-password = guest.NAME.
        END.
    END.

    FIND FIRST queasy WHERE queasy.KEY EQ 223 AND queasy.number1 EQ arrival-guestlist.resnr
         AND queasy.number2 EQ arrival-guestlist.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        arrival-guestlist.payment-status = queasy.char1.

        IF NUM-ENTRIES(queasy.char2,"|") GT 1 THEN 
        DO:
            arrival-guestlist.transid-merchant = ENTRY(1,queasy.char2,"|"). 
            arrival-guestlist.payment-channel  = ENTRY(2,queasy.char2,"|").
        END.
        ELSE arrival-guestlist.transid-merchant = queasy.char2.

        IF queasy.number3 EQ 1 THEN arrival-guestlist.payment-method = "DOKU".
        ELSE IF queasy.number3 EQ 2 THEN arrival-guestlist.payment-method = "QRIS".
    END.
    ELSE
    DO:
        arrival-guestlist.payment-status = "PENDING".
        /*IF queasy.number3 EQ 1 THEN arrival-guestlist.payment-method = "DOKU".
        ELSE IF queasy.number3 EQ 2 THEN arrival-guestlist.payment-method = "QRIS".*/
    END.    

    /**/
    FIND FIRST reservation WHERE reservation.resnr EQ arrival-guestlist.resnr NO-LOCK.
    IF AVAILABLE reservation THEN
    DO:
        /*FD June 20, 2022*/
        depo-bal = reservation.depositgef - reservation.depositbez - reservation.depositbez2.
        ASSIGN
            arrival-guestlist.amount-depo   = reservation.depositgef
            arrival-guestlist.depo-paid1    = reservation.depositbez
            arrival-guestlist.depo-paid2    = reservation.depositbez2
            arrival-guestlist.depo-balance  = depo-bal
        .

        /* FD Comment
        IF reservation.depositbez NE 0 THEN
        DO:
            arrival-guestlist.payment-status = "SUCCESS".
        END.
        */
    END.
    
    /*FD June 20, 2022*/
    IF arrival-guestlist.res-status EQ "1 - Guest Already Checkin" THEN
    DO:
        FIND FIRST reservation WHERE reservation.resnr EQ arrival-guestlist.resnr NO-LOCK.
        IF AVAILABLE reservation THEN
        DO:
            arrival-guestlist.payment-status = "SUCCESS".
        END.
    END.
    ELSE
    DO:
        FOR EACH buff-resline WHERE buff-resline.resnr EQ arrival-guestlist.resnr NO-LOCK:
            
            IF buff-resline.resstatus EQ 6 OR buff-resline.resstatus EQ 13 THEN res-flag = YES.            
            LEAVE.
        END.

        IF res-flag THEN
        DO:
            arrival-guestlist.payment-status = "SUCCESS".
        END.

        res-flag = NO.
    END.
    
    IF arrival-guestlist.payment-status EQ "SUCCESS" THEN arrival-guestlist.preAuth-flag = YES.

    FIND FIRST zimmer WHERE zimmer.zinr EQ arrival-guestlist.zinr NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
        IF himmelsr MATCHES "*smoking*" THEN arrival-guestlist.smoking-room = YES.
        ELSE IF himmelsr MATCHES "*no smoking*" THEN arrival-guestlist.smoking-room = NO.
        ELSE IF himmelsr MATCHES "*non smoking*" THEN arrival-guestlist.smoking-room = NO.   
        ELSE smoking-room = NO. 
    END.

    FIND CURRENT res-line.
    RELEASE res-line.
END.
