/*BL untuk mencari data breakfast berdasarkan room number
  hasil data di pisahkan oleh delimiter CHR(2), dengan urutan sebagai berikut:
  1 -> Pesan (Bisa pesan error atau sukses) [Jika sukses isi dengan "success"]
       dan lanjutkan dengan data berikut nya jika sukses, jika gagal langsung return saja
       keluar dari program ini dan di beri pesan mengapa error terjadi
  2 -> Untuk Nomor Reservasi
  3 -> Untuk Nomor Guest
  4 -> Untuk Nama Guest
  5 -> Untuk keterangan Arrangemet
  6 -> Untuk Guest Check-in date 
  7 -> Untuk Guest Check-out date
  8 -> Untuk jumlah Adult
  9 -> Untuk Compliment                              
  10-> untuk jumlah Child    
  11-> Untuk Consumed        
  12-> Untuk VIP Status      
  13-> Untuk nationality     
  14-> Untuk RSVComment      
  15-> untuk bill instruction
  Jika ada penambahan data bisa di sini dan nomor selanjutnya */

DEFINE INPUT PARAMETER inpRoomNumber AS CHARACTER.
DEFINE INPUT PARAMETER inpMealTime   AS CHARACTER.
DEFINE OUTPUT PARAMETER outStr          AS CHARACTER.

/*DEFINE VARIABLE inpRoomNumber AS CHARACTER INITIAL "625".
DEFINE VARIABLE outStr          AS CHARACTER.*/

DEFINE VARIABLE p-87        AS DATE         NO-UNDO.
DEFINE VARIABLE gastNr      AS INTEGER      NO-UNDO.
DEFINE VARIABLE guestName   AS CHARACTER    NO-UNDO.
DEFINE VARIABLE argt-bez    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE resNr       AS INTEGER      NO-UNDO.  
DEFINE VARIABLE ciDate      AS DATE         NO-UNDO.
DEFINE VARIABLE coDate      AS DATE         NO-UNDO.
DEFINE VARIABLE num-of-day  AS INTEGER NO-UNDO.
DEFINE VARIABLE i           AS INTEGER NO-UNDO.
DEFINE VARIABLE tmpStr      AS CHARACTER NO-UNDO.
DEFINE VARIABLE tmpInt      AS INTEGER NO-UNDO.
DEFINE VARIABLE vip-nr          AS INTEGER EXTENT 10.

DEFINE VARIABLE totAdult    AS INTEGER.
DEFINE VARIABLE totCompli   AS INTEGER.
DEFINE VARIABLE totChild    AS INTEGER.
DEFINE VARIABLE totConsumed AS INTEGER.

DEFINE VARIABLE VIPFlag         AS CHARACTER INITIAL "".
DEFINE VARIABLE nation          AS CHARACTER.
DEFINE VARIABLE rsv-comment     AS CHARACTER.
DEFINE VARIABLE bill-instruct   AS CHARACTER.

DEFINE VARIABLE artGrp-abf     AS INTEGER.
DEFINE VARIABLE artGrp-lunch   AS INTEGER.
DEFINE VARIABLE artGrp-dinner  AS INTEGER.
DEFINE VARIABLE artGrp-lundin  AS INTEGER.  

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK NO-ERROR. /*Breakfast*/
IF AVAILABLE htparam THEN artGrp-abf = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 227 NO-LOCK NO-ERROR. /*Lunch*/
IF AVAILABLE htparam THEN artGrp-lunch = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 228 NO-LOCK NO-ERROR. /*Dinner*/
IF AVAILABLE htparam THEN artGrp-dinner = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 229 NO-LOCK NO-ERROR. /*LUNCH-DINNER (HALF BOARD)*/
IF AVAILABLE htparam THEN artGrp-lundin = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-87 = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
vip-nr[1] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
vip-nr[2] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
vip-nr[3] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
vip-nr[4] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
vip-nr[5] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
vip-nr[6] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
vip-nr[7] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
vip-nr[8] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
vip-nr[9] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 712 NO-LOCK. 
vip-nr[10] = htparam.finteger. 

DEFINE BUFFER b-res-line FOR res-line.

FIND FIRST res-line WHERE res-line.zinr = inpRoomNumber AND res-line.resstatus = 6
    AND p-87 GE res-line.ankunft AND p-87 LE res-line.abreise NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN DO:
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr.
    IF NOT AVAILABLE reservation THEN do:
        outStr = "Main Reservation data not found".
        RETURN.
    END.
    IF NOT AVAILABLE guest THEN FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN tmpStr = nation.bezeich.
    ELSE tmpStr = "".
    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement AND AVAILABLE guest THEN DO:
        ASSIGN
            resNr       = res-line.resnr
            gastNr      = guest.gastnr
            guestName   = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
            ciDate      = res-line.ankunft
            coDate      = res-line.abreise
            argt-bez    = " " + arrangement.arrangement + " : " + arrangement.argt-bez
            rsv-comment = reservation.bemerk + CHR(10) + res-line.bemerk
            nation      = ENTRY(1, tmpStr, ";")
            guestName   = guestName + " [" + nation + "]" 
            .

        FOR EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember:
            DO i = 1 TO EXTENT(vip-nr):
                IF guestseg.segmentcode = vip-nr[i] THEN DO:
                    vipFlag = "VIP " + STRING(i).
                    i = 100.
                    LEAVE.
                END.
            END.
            IF i = 100 THEN LEAVE.
        END.

        FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr:
            IF argt-line.argt-artnr = artGrp-abf AND inpMealTime = "Breakfast" THEN DO:
               /* IF argt-line.betriebsnr = 1 THEN  do: /*Quantity always 1*/
                    IF argt-line.fakt-modus = 3 AND (p-87 - res-line.ankunft EQ 1) THEN DO: /*Second day of stay*/
                        totAdult = 1.
                        totCompli = 1.
                    END.
                    ELSE IF argt-line.fakt-modus = 6 AND (p-87 - res-line.ankunft LE argt-line.intervall) THEN DO: /*Special*/
                        totAdult = 1.
                        totCompli = 1.
                    END.
                    ELSE IF argt-line.fakt-modus NE 3 AND argt-line.fakt-modus NE 6 THEN DO: /*Daily or others*/
                        totAdult = 1.
                        totCompli = 1.
                    END.
                    
                    IF res-line.erwachs EQ 0 THEN totAdult = 0.
                    IF res-line.gratis EQ 0 THEN totCompli = 0.

                    /*Mencari list umur anak*/
                    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                        IF ENTRY(i, res-line.zimmer-wunsch, ";") EQ "ChAge" THEN
                            tmpStr = ENTRY(i, res-line.zimmer-wunsch, ";").
                    END.

                    DO i = 1 TO res-line.kind1:
                        IF i > NUM-ENTRIES(tmpStr, ",") THEN LEAVE.
                        IF INT(ENTRY(i, tmpStr, ",")) GT 12 THEN tmpInt = tmpInt + 1.
                    END.
                    IF tmpInt GT 0 THEN totAdult = 1.
                    totChild = res-line.kind1 - tmpInt.
                END.
                ELSE DO: /*Not Quantity always one*/*/
                    IF argt-line.fakt-modus = 3 AND (p-87 - res-line.ankunft EQ 1) THEN DO: /*Second day of stay*/
                        totAdult = res-line.erwachs.
                        totCompli = res-line.gratis.
                    END.
                    ELSE IF argt-line.fakt-modus = 6 AND (p-87 - res-line.ankunft LE argt-line.intervall) THEN DO: /*Special*/
                        totAdult = res-line.erwachs.
                        totCompli = res-line.gratis.
                    END.
                    ELSE IF argt-line.fakt-modus NE 3 AND argt-line.fakt-modus NE 6 THEN DO: /*Daily or others*/
                        totAdult = res-line.erwachs.
                        totCompli = res-line.gratis.
                    END.

                    /*Mencari list umur anak, jika lebih dari 12 tahun di anggap adult*/
                    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                        IF ENTRY(i, res-line.zimmer-wunsch, ";") MATCHES "*ChAge*" THEN
                            tmpStr = SUBSTR(ENTRY(i, res-line.zimmer-wunsch, ";"),6).
                    END.

                    DO i = 1 TO res-line.kind1:
                        IF i > NUM-ENTRIES(tmpStr, ",") THEN LEAVE.
                        IF INT(ENTRY(i, tmpStr, ",")) GT 12 THEN tmpInt = tmpInt + 1.
                    END.

                    totAdult = totAdult + tmpInt.
                    totChild = res-line.kind1 - tmpInt.

                /*END.*/
            END.
            ELSE IF argt-line.argt-artnr = artGrp-lunch AND inpMealTime = "Lunch" THEN DO:

            
            END.
            ELSE IF argt-line.argt-artnr = artGrp-dinner AND inpMealTime = "Dinner" THEN DO:

            END.
        END.
    END.   
END.
ELSE DO:
    outStr = "No InHouse guest in selected room".
    RETURN.
END.

num-of-day = p-87 - res-line.ankunft.
IF num-of-day GT 32 THEN num-of-day = num-of-day - 32.

IF num-of-day = 0 THEN DO:
    outStr = "If guest checked-in today, a breakfast voucher will be available on the next day".
    RETURN.
END.

IF totAdult + totChild + totCompli GT 0 AND AVAILABLE res-line THEN DO: /*Check data di mealcoup terlebih dahulu*/
    FOR EACH mealcoup WHERE mealcoup.resnr = res-line.resnr 
        AND mealcoup.zinr = res-line.zinr AND mealcoup.NAME = inpMealTime NO-LOCK:
        totConsumed = mealcoup.verbrauch[num-of-day].
    END.
END.

FOR EACH b-res-line WHERE b-res-line.resnr = res-line.resnr AND 
    b-res-line.zinr = res-line.zinr AND b-res-line.resstatus GT 6
    AND b-res-line.kontakt-nr NE 0:
    FIND FIRST guest WHERE guest.gastnr = b-res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN DO:
        tmpStr = "".
        FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN tmpStr = nation.bezeich.
        guestName = guestName + CHR(10) + guest.NAME + ", " + 
            guest.vorname1 + " " + guest.anrede1 + " [" + ENTRY(1, tmpStr, ";") + "]".
    END.
END.

/*Mencari billing instruction*/
FIND FIRST queasy WHERE queasy.KEY = 9 
    AND queasy.number1 = INT(res-line.CODE) NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
    bill-instruct = queasy.char1.
END.

/*
  1 -> Pesan (Bisa pesan error atau sukses) [Jika sukses isi dengan "success"]
       dan lanjutkan dengan data berikut nya jika sukses, jika gagal langsung return saja
       keluar dari program ini dan di beri pesan mengapa error terjadi
  2 -> Untuk Nomor Reservasi
  3 -> Untuk Nomor Guest
  4 -> Untuk Nama Guest
  5 -> Untuk keterangan Arrangemet
  6 -> Untuk Guest Check-in date 
  7 -> Untuk Guest Check-out date
  8 -> Untuk jumlah Adult
  9 -> Untuk Compliment                              
  10-> untuk jumlah Child    
  11-> Untuk Consumed        
  12-> Untuk VIP Status      
  13-> Untuk nationality     
  14-> Untuk RSVComment      
  15-> untuk bill instruction
  Jika ada penambahan data bisa di sini dan nomor selanjutnya */

outStr = "success"                      + CHR(2) + /*1*/
         STRING(resNr)                  + CHR(2) + /*2*/
         STRING(gastNr)                 + CHR(2) + /*3*/
         guestName                      + CHR(2) + /*4*/
         argt-bez                       + CHR(2) + /*5*/
         STRING(ciDate, "99/99/9999")   + CHR(2) + /*6*/
         STRING(coDate, "99/99/9999")   + CHR(2) + /*7*/
         STRING(totAdult)               + CHR(2) + /*8*/
         STRING(totCompli)              + CHR(2) + /*9*/
         STRING(totChild)               + CHR(2) + /*10*/
         STRING(totConsumed)            + CHR(2) + /*11*/
         VIPflag                        + CHR(2) + /*12*/
         nation                         + CHR(2) + /*13*/
         rsv-comment                    + CHR(2) + /*14*/
         bill-instruct                             /*15*/     
    .
         
