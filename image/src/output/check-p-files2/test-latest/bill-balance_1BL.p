DEFINE TEMP-TABLE billbalance-list 
    FIELD flag         AS CHARACTER FORMAT "x(3)" LABEL "" 
    FIELD departnem   AS CHARACTER FORMAT "X(25)"  /*william CA63EA*/
    FIELD zinr         LIKE res-line.zinr 
    FIELD resstatus    AS INTEGER COLUMN-LABEL " S" FORMAT ">>" 
    FIELD zipreis      LIKE res-line.zipreis FORMAT ">>>,>>>,>>9.99" 
    FIELD rechnr       AS INTEGER FORMAT ">>>>>>>" LABEL "Bill No" 
    FIELD receiver     LIKE bill.name FORMAT "x(50)" COLUMN-LABEL "Bill Receiver" 
    FIELD ankunft      LIKE res-line.ankunft INITIAL ? 
    FIELD abreise      LIKE res-line.abreise INITIAL ? 
    FIELD saldo        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Balance" 
    FIELD name         LIKE res-line.name FORMAT "x(50)" COLUMN-LABEL "Guest Name"
    FIELD bill-inst    AS CHARACTER FORMAT "x(24)" COLUMN-LABEL "Guarantee of Payment"
    FIELD idcard       LIKE guest.ausweis-nr1
    FIELD nat          LIKE guest.nation1
    FIELD datum        AS DATE  COLUMN-LABEL "Date"
    FIELD fsort        AS CHARACTER  FORMAT "x(1)"
    FIELD remarks      AS CHARACTER  FORMAT "x(50)"
    FIELD bill-remark  AS CHARACTER FORMAT "x(50)" /*gerald 78ECFA*/  
    . 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER co-today             AS LOGICAL.
DEFINE INPUT PARAMETER room                 AS CHARACTER.
DEFINE INPUT PARAMETER zero-flag            AS LOGICAL.
DEFINE INPUT PARAMETER cash-basis           AS LOGICAL.
DEFINE INPUT PARAMETER gname                AS CHARACTER.
DEFINE INPUT PARAMETER menu-nsbill          AS LOGICAL.
DEFINE INPUT PARAMETER menu-msbill          AS LOGICAL.
DEFINE INPUT PARAMETER menu-fobill          AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR billbalance-list.

DEFINE VARIABLE tot-outstand AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it AS LOGICAL. 

DEFINE VARIABLE ci-date         AS DATE NO-UNDO.
DEFINE BUFFER gast FOR guest.
{supertransbl.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "bill-balance". 

/*****************************************************************************/

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
IF NOT cash-basis THEN
DO:
    IF NOT co-today THEN 
    DO: 
        IF room = "" THEN 
        DO: 
            IF menu-nsbill THEN 
                FOR EACH bill WHERE bill.flag = 0 AND bill.resnr = 0  /* Non Stay */ 
                NO-LOCK BY bill.name: 
                    do-it = NO. 
                    
                    IF (zero-flag AND bill.datum NE ? AND bill.NAME NE "") /*FD 221019*/
                        OR bill.saldo NE 0 THEN do-it = YES. 
                    /*Use Available and No-Error for this do-it*/
                    IF do-it THEN 
                    DO: 
                        CREATE billbalance-list.

                        FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN
                        DO: 
                            
                            ASSIGN  
                                billbalance-list.flag = "NS" 
                                /*MT
                                billbalance-list.receiver = guest.name + ", " + guest.vorname1 + " " 
                                                    + guest.anrede1 + guest.anredefirma*/
                                billbalance-list.receiver = bill.name
                                /*M 241111 -> before cl-list.name = "" */
                                billbalance-list.name = guest.name + ", " + guest.vorname1 + " " 
                                                    + guest.anrede1 + guest.anredefirma 
                                billbalance-list.rechnr  = bill.rechnr 
                                billbalance-list.saldo   = bill.saldo 
                                billbalance-list.ankunft = ? 
                                billbalance-list.abreise = ? 
                                billbalance-list.idcard  = guest.ausweis-nr1
                                billbalance-list.NAT     = guest.nation1
                                billbalance-list.datum   = bill.datum
                                billbalance-list.fsort   = "0"
                                billbalance-list.bill-remark = bill.vesrdepot.         /*gerald 78ECFA*/
                                
                            /* change by damen 27/03/23 7C7906*/
                            FIND FIRST hoteldpt WHERE hoteldpt.num = bill.billtyp NO-LOCK NO-ERROR.
                            IF AVAILABLE hoteldpt THEN
                            DO:
                                billbalance-list.departnem  = hoteldpt.depart. /*william CA63EA*/
                            END.
                            FIND FIRST reservation WHERE reservation.gastnr = bill.gastnr NO-LOCK NO-ERROR.
                            IF AVAILABLE reservation THEN
                            DO:
                                billbalance-list.remarks = guest.bemerkung  + reservation.bemerk  + bill.vesrdepot.                            
                            END.
                            ELSE
                            DO:
                                billbalance-list.remarks = guest.bemerkung + bill.vesrdepot.                            
                            END.
                        END.              
                        tot-outstand = tot-outstand + bill.saldo. 
                    END. 
                END. 
        END. 
    
        IF room = "" AND menu-msbill THEN
            FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
            AND bill.reslinnr = 0 NO-LOCK BY bill.name: 
                do-it = NO. 
    
                IF zero-flag OR bill.saldo NE 0 THEN do-it = YES. 
                /*Use Available and No-Error for this do-it*/
                IF do-it THEN 
                DO: 
                    CREATE billbalance-list.

                    FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
                        AND res-line.resstatus LE 8 NO-LOCK NO-ERROR.
                    /*FIND FIRST gast WHERE gast.gastnr = bill.gastnr NO-LOCK .*/ 
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR. 
                    IF AVAILABLE guest THEN
                    DO:
                        
                        ASSIGN 
                            billbalance-list.flag = "M" 
                            /*MT
                            billbalance-list.receiver = gast.NAME + ", " + gast.vorname1 + " " 
                                                + gast.anrede1 + gast.anredefirma*/
                            billbalance-list.receiver = bill.name
                            billbalance-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                                + guest.anrede1 + guest.anredefirma 
                            billbalance-list.name = "" 
                            billbalance-list.rechnr = bill.rechnr 
                            billbalance-list.saldo = bill.saldo 
                            billbalance-list.idcard  = guest.ausweis-nr1
                            billbalance-list.NAT     = guest.nation1
                            billbalance-list.datum  = bill.datum
                            billbalance-list.fsort  = "0"
                            billbalance-list.bill-remark = bill.vesrdepot.         /*gerald 78ECFA*/
                            
                    END.
                    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr.
                    FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE hoteldpt THEN
                    DO:
                        billbalance-list.departnem  = hoteldpt.depart. /*william CA63EA*/
                    END.

                    IF AVAILABLE res-line THEN 
                    DO:
                        ASSIGN 
                            billbalance-list.ankunft = res-line.ankunft 
                            billbalance-list.abreise = res-line.abreise
                            billbalance-list.resstatus = res-line.resstatus /*FD 221019*/
                            billbalance-list.remarks = guest.bemerkung  + res-line.bemerk  + bill.vesrdepot. /*FD 221019*/

                        FIND FIRST queasy WHERE queasy.KEY = 9 AND queasy.number1 = INTEGER(res-line.code)
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN
                            billbalance-list.bill-inst = queasy.char1.
                                                
                    END.
                    ELSE 
                    DO:
                        FIND FIRST history WHERE history.resnr = bill.resnr
                            AND history.reslinnr LT 999 AND history.zi-wechsel = NO
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE history THEN
                            ASSIGN   billbalance-list.ankunft = history.ankunft 
                                     billbalance-list.abreise = history.abreise
                                 .
                    END.

                tot-outstand = tot-outstand + bill.saldo. 
                END. 
            END. 
    END. 
    
    IF co-today THEN 
    DO: 
        IF menu-fobill THEN
        FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
            AND bill.zinr NE "" AND bill.zinr GE room NO-LOCK, 
            FIRST res-line WHERE res-line.resnr = bill.resnr 
            AND res-line.reslinnr = bill.reslinnr 
            AND res-line.abreise = ci-date NO-LOCK 
            BY bill.zinr BY bill.reslinnr: 
    
            do-it = NO. 
            IF zero-flag OR bill.saldo NE 0 THEN do-it = YES. 
            IF gname NE "" THEN 
            DO: 
                FIND FIRST reservation WHERE reservation.groupname = gname 
                    AND reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE reservation THEN do-it = NO. 
            END. 
    
            IF do-it THEN 
            DO: 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                
                CREATE billbalance-list. 
                billbalance-list.zinr = bill.zinr. 
                billbalance-list.resstatus = res-line.resstatus. 
                
                IF res-line.resstatus NE 12 THEN billbalance-list.name = res-line.name. 
                ELSE billbalance-list.name = translateExtended ("** Extra Bill",lvCAREA,""). 
                
                /*MT
                billbalance-list.receiver = guest.name + ", " + guest.vorname1 + " " 
                                    + guest.anrede1 + guest.anredefirma.*/
                billbalance-list.receiver = bill.name.
                billbalance-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                                + guest.anrede1 + guest.anredefirma. /*willi add name 7f1cb5*/ 
                billbalance-list.zipreis = res-line.zipreis. 
                billbalance-list.rechnr = bill.rechnr. 
                billbalance-list.saldo = bill.saldo. 
                billbalance-list.ankunft = res-line.ankunft. 
                billbalance-list.abreise = res-line.abreise. 
                billbalance-list.idcard  = guest.ausweis-nr1.
                billbalance-list.nat     = guest.nation1.
                billbalance-list.datum  = bill.datum.
                billbalance-list.fsort  = "0".
                billbalance-list.remarks = guest.bemerkung  + res-line.bemerk  + bill.vesrdepot. /*FD 221019*/
                billbalance-list.bill-remark = bill.vesrdepot.         /*gerald 78ECFA*/
                
                FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr.
                FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN
                DO:
                    billbalance-list.departnem  = hoteldpt.depart. /*william CA63EA*/
                END.
    
                FIND FIRST queasy WHERE queasy.KEY = 9 AND queasy.number1 = INTEGER(res-line.code)
                    NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                    billbalance-list.bill-inst = queasy.char1.
    
                tot-outstand = tot-outstand + bill.saldo. 
            END. 
        END. 
    END. 
    ELSE /* ALL FO guest bills */
    IF menu-fobill THEN
        FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
        AND bill.zinr NE "" AND bill.zinr GE room 
        NO-LOCK BY bill.zinr BY bill.reslinnr: 
            FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
                AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE res-line THEN
                FIND FIRST history WHERE history.resnr = bill.resnr 
                AND history.reslinnr = bill.reslinnr 
                AND NOT history.zi-wechsel NO-LOCK NO-ERROR. 
            do-it = NO. 
            IF zero-flag OR bill.saldo NE 0 THEN do-it = YES. 
            IF gname NE "" THEN 
            DO: 
                FIND FIRST reservation WHERE reservation.groupname = gname 
                    AND reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE reservation THEN do-it = NO. 
            END. 

            IF do-it THEN 
            DO: 
                IF AVAILABLE res-line THEN
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
                ELSE 
                    FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK. 

                
                CREATE billbalance-list. 
                IF AVAILABLE res-line AND res-line.resstatus NE 12 THEN billbalance-list.name = res-line.name. 
                ELSE billbalance-list.name = translateExtended ("** Extra Bill",lvCAREA,""). 
                
                ASSIGN  billbalance-list.zinr = bill.zinr                        
                        /*MT
                        billbalance-list.receiver = guest.name + ", " + guest.vorname1 + " " 
                                            + guest.anrede1 + guest.anredefirma*/
                        billbalance-list.receiver = bill.name
                        billbalance-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                                + guest.anrede1 + guest.anredefirma /*willi add name 7f1cb5*/ 
                        billbalance-list.rechnr = bill.rechnr
                        billbalance-list.saldo = bill.saldo
                        billbalance-list.idcard = guest.ausweis-nr1
                        billbalance-list.nat = guest.nation1
                        billbalance-list.datum  = bill.datum
                        billbalance-list.fsort  = "0"
                        billbalance-list.bill-remark = bill.vesrdepot.         /*gerald 78ECFA*/
                
                FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr.
                FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN
                DO:
                    billbalance-list.departnem  = hoteldpt.depart. /*william CA63EA*/
                END.
                        

                IF AVAILABLE res-line THEN
                DO:
                    ASSIGN  billbalance-list.ankunft = res-line.ankunft
                            billbalance-list.abreise = res-line.abreise 
                            billbalance-list.zipreis = res-line.zipreis
                            billbalance-list.resstatus = res-line.resstatus /*FD 221019*/
                            billbalance-list.remarks = /*guest.bemerkung  +*/ res-line.bemerk  + bill.vesrdepot. /*FD 221019*/

                    FIND FIRST queasy WHERE queasy.KEY = 9 AND queasy.number1 = INTEGER(res-line.code)
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                        billbalance-list.bill-inst = queasy.char1.
                END.
                ELSE IF AVAILABLE history THEN
                    ASSIGN  billbalance-list.ankunft = history.ankunft
                            billbalance-list.abreise = history.abreise 
                            billbalance-list.zipreis = history.zipreis.

                tot-outstand = tot-outstand + bill.saldo. 
            END. 
        END. 
END.

ELSE
DO:
    IF co-today THEN 
    DO:
       IF menu-fobill THEN
       FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
        AND bill.zinr NE "" AND bill.zinr GE room NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.reslinnr = bill.reslinnr 
        AND res-line.abreise = ci-date NO-LOCK 
        BY bill.zinr BY bill.reslinnr: 
        FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = 
           INTEGER(res-line.code) NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy AND queasy.logi1 THEN 
        DO:
            do-it = NO. 
            IF zero-flag OR bill.saldo NE 0 THEN do-it = YES. 
            IF gname NE "" THEN 
            DO: 
                FIND FIRST reservation WHERE reservation.groupname = gname 
                    AND reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE reservation THEN do-it = NO. 
            END. 
    
            IF do-it THEN 
            DO: 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                
                CREATE billbalance-list. 
                billbalance-list.zinr = bill.zinr. 
                billbalance-list.resstatus = res-line.resstatus. 
                
                IF res-line.resstatus NE 12 THEN billbalance-list.name = res-line.name. 
                ELSE billbalance-list.name = translateExtended ("** Extra Bill",lvCAREA,""). 
                
                /*MT
                billbalance-list.receiver  = guest.name + ", " + guest.vorname1 + " " 
                                             + guest.anrede1 + guest.anredefirma.*/
                billbalance-list.NAME      = res-line.name. /*willi add name 7f1cb5*/ 
                billbalance-list.receiver  = bill.name.
                billbalance-list.zipreis   = res-line.zipreis. 
                billbalance-list.rechnr    = bill.rechnr. 
                billbalance-list.saldo     = bill.saldo. 
                billbalance-list.ankunft   = res-line.ankunft. 
                billbalance-list.abreise   = res-line.abreise. 
                billbalance-list.idcard    = guest.ausweis-nr1.
                billbalance-list.nat       = guest.nation1.
                billbalance-list.datum     = bill.datum.
                billbalance-list.fsort     = "0".
                billbalance-list.remarks = /*guest.bemerkung  +*/ res-line.bemerk  + bill.vesrdepot. /*FD 221019*/
                billbalance-list.bill-remark = bill.vesrdepot.         /*gerald 78ECFA*/

               FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr.
               FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
               IF AVAILABLE hoteldpt THEN
               DO:
                   billbalance-list.departnem  = hoteldpt.depart. /*william CA63EA*/
               END. 
               
    
                FIND FIRST queasy WHERE queasy.KEY = 9 AND queasy.number1 = INTEGER(res-line.code)
                    NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                    billbalance-list.bill-inst = queasy.char1.
    
                tot-outstand = tot-outstand + bill.saldo. 
            END. 
        END.
       END. 
    END.
    ELSE
    DO:
       IF menu-fobill THEN
       FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
            AND bill.zinr NE "" AND bill.zinr GE room 
            NO-LOCK BY bill.zinr BY bill.reslinnr:
            do-it = NO. 
            IF zero-flag OR bill.saldo NE 0 THEN do-it = YES. 
            FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
                AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
            FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = 
                INTEGER(res-line.code) NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy AND queasy.logi1 THEN 
            DO:
              IF do-it THEN
              DO:
                  FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR.
                  
                  CREATE billbalance-list. 
                  ASSIGN  
                    billbalance-list.resstatus = res-line.resstatus /*FD 221019*/
                    billbalance-list.zinr       = bill.zinr
                    /*MT
                    billbalance-list.receiver   = guest.name + ", " + guest.vorname1 + " " 
                                                  + guest.anrede1 + guest.anredefirma*/
                    billbalance-list.NAME       = res-line.name /*willi add name 7f1cb5*/ 
                    billbalance-list.receiver   = bill.name
                    billbalance-list.rechnr     = bill.rechnr
                    billbalance-list.saldo      = bill.saldo
                    billbalance-list.idcard     = guest.ausweis-nr1
                    billbalance-list.nat        = guest.nation1
                    billbalance-list.datum      = bill.datum
                    billbalance-list.fsort      = "0"
                    billbalance-list.ankunft    = res-line.ankunft
                    billbalance-list.abreise    = res-line.abreise 
                    billbalance-list.zipreis    = res-line.zipreis
                    billbalance-list.bill-inst  = queasy.char1
                    billbalance-list.remarks = guest.bemerkung + res-line.bemerk + bill.vesrdepot /*FD 221019*/
                    billbalance-list.bill-remark = bill.vesrdepot.         /*gerald 78ECFA*/

                    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr.
                    FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE hoteldpt THEN
                    DO:
                        billbalance-list.departnem  = hoteldpt.depart. /*william CA63EA*/
                    END.
              END.
            END.
          END.
    END.
END.

CREATE billbalance-list. 
billbalance-list.receiver = "T o t a l". 
billbalance-list.saldo = tot-outstand. 
billbalance-list.fsort  = "1".


