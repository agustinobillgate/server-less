DEFINE TEMP-TABLE res-log
  FIELD his-recid AS INTEGER 
  FIELD ankunft1  AS DATE    
  FIELD abreise1  AS DATE      
  FIELD qty1      AS INTEGER   FORMAT ">>9" 
  FIELD qty2      AS INTEGER   FORMAT ">>9"  
  FIELD Adult1    AS INTEGER   FORMAT ">9" 
  FIELD adult2    AS INTEGER   FORMAT ">9"  
  FIELD child1    AS INTEGER   FORMAT ">9" 
  FIELD child2    AS INTEGER   FORMAT ">9" 
  FIELD comp1     AS INTEGER   FORMAT ">9" 
  FIELD comp2     AS INTEGER   FORMAT ">9" 
  FIELD rmcat1    AS CHARACTER FORMAT "x(6)" 
  FIELD rmcat2    AS CHARACTER FORMAT "x(6)" 
  FIELD zinr1     AS CHARACTER FORMAT "x(5)" 
  FIELD zinr2     AS CHARACTER FORMAT "x(5)" 
  FIELD argt1     AS CHARACTER FORMAT "x(5)"  
  FIELD argt2     AS CHARACTER FORMAT "x(5)" 
  FIELD rate1     AS DECIMAL   FORMAT ">>>,>>>,>>9.99" 
  FIELD rate2     AS DECIMAL   FORMAT ">>>,>>>,>>9.99" 
  FIELD fixrate1  AS CHARACTER FORMAT "x(3)"  
  FIELD fixrate2  AS CHARACTER FORMAT "x(3)"  
  FIELD name1     AS CHARACTER FORMAT "x(16)" 
  FIELD name2     AS CHARACTER FORMAT "x(16)" 
  FIELD id1       AS CHARACTER FORMAT "x(4)" 
  FIELD id2       AS CHARACTER FORMAT "x(4)" 
  FIELD date1     AS DATE     
  FIELD date2     AS DATE     
  FIELD zeit      AS INTEGER
  FIELD resnr     AS INTEGER
  FIELD reslinnr  AS INTEGER
  FIELD resstatus AS INTEGER
  FIELD room-cat  AS CHAR
  FIELD rate-code AS CHAR
  FIELD night-stay AS INTEGER
  FIELD variance  AS DECIMAL
  /*FIELD bemerk   AS CHARACTER*/
  FIELD rsv-name  AS CHARACTER. /*MNA 230223 - #EFE2FE - add field rsv-name req by harper purwakarta*/ 


DEFINE INPUT  PARAMETER fDate               AS DATE.
DEFINE INPUT  PARAMETER tDate               AS DATE.
DEFINE INPUT  PARAMETER resno               AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR res-log.
   
DEFINE VARIABLE akuntf   AS CHARACTER.
DEFINE VARIABLE abreise  AS CHARACTER.
DEFINE VARIABLE date1    AS CHARACTER.
DEFINE VARIABLE date2    AS DATE.
DEFINE VARIABLE loopi    AS INTEGER.
DEFINE VARIABLE str      AS CHAR.

DEFINE BUFFER breslin FOR reslin-queasy.
DEFINE BUFFER tguest  FOR guest.

IF fdate NE ? AND tdate NE ? AND resno NE 0 THEN RUN create-list1.
ELSE IF fdate = ? AND tdate = ? AND resno NE 0 THEN RUN create-list2.
ELSE RUN create-list.
/************************ PROCEDURE ************************/  

PROCEDURE create-list:
    FOR EACH reslin-queasy WHERE key = "ResChanges" 
        AND reslin-queasy.date2 GE fDate AND reslin-queasy.date2 LE tDate NO-LOCK:
        IF reslin-queasy.char3 MATCHES("*;*") AND DECIMAL(ENTRY(19,reslin-queasy.char3,";")) NE DECIMAL(ENTRY(20,reslin-queasy.char3,";")) THEN DO:
            CREATE res-log.
            ASSIGN
                res-log.resnr       = reslin-queasy.resnr
                res-log.reslinnr    = reslin-queasy.reslinnr
                res-log.ankunft1    = DATE(INT(ENTRY(2, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(1, reslin-queasy.char3, ";"), "/")))
                                        /*INT(akuntf))*/
                /*res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(2, reslin-queasy.char3, ";"), "/")))*/
                /*geral 1B5CD8*/
                res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                      INT(ENTRY(1, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                      INT("20" + ENTRY(3, ENTRY(3, reslin-queasy.char3, ";"), "/")))
                                      /*INT(abreise))*/
                res-log.zinr1       = ENTRY(15,reslin-queasy.char3,";")
                res-log.rate1       = DECIMAL(ENTRY(19,reslin-queasy.char3,";"))
                res-log.rate2       = DECIMAL(ENTRY(20,reslin-queasy.char3,";"))
                res-log.name1       = ENTRY(25,reslin-queasy.char3,";")
                res-log.id1         = ENTRY(21,reslin-queasy.char3,";")
                res-log.id2         = ENTRY(22,reslin-queasy.char3,";")
                res-log.date1       = DATE(ENTRY(23,reslin-queasy.char3,";"))
                res-log.zeit        = number2
                res-log.date1       = reslin-queasy.date2
                res-log.variance    = res-log.rate1 - res-log.rate2
                res-log.night-stay  = res-log.abreise1 - res-log.ankunft1.

            FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr
                AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO: 
                ASSIGN res-log.resstatus = res-line.resstatus.

                FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN res-log.room-cat = zimkateg.kurzbez.
                  
                DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,6) = "$CODE$" THEN res-log.rate-code  = SUBSTR(str,7).
                END.

                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:
                    ASSIGN res-log.rsv-name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
                END.
                ELSE DO:
                    ASSIGN res-log.rsv-name = "".
                END.
            END.
        END.
        ELSE IF STRING(ENTRY(25,reslin-queasy.char3,";")) MATCHES "*CHG Fixrate TO*" THEN DO:
            FIND FIRST breslin WHERE breslin.key = "ResChanges" 
                AND breslin.resnr = reslin-queasy.resnr
                AND breslin.reslinnr = reslin-queasy.reslinnr
                AND breslin.date2 = reslin-queasy.date2 
                AND STRING(ENTRY(25,breslin.char3,";")) MATCHES "*CHG Fixrate FR*"
                AND breslin.number2 = reslin-queasy.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE breslin
                AND DECIMAL(ENTRY(2,ENTRY(26,reslin-queasy.char3,";"),"-")) NE DECIMAL(ENTRY(2,ENTRY(26,breslin.char3,";"),"-")) THEN 
            DO:
                CREATE res-log.
                ASSIGN
                    res-log.resnr       = reslin-queasy.resnr
                    res-log.reslinnr    = reslin-queasy.reslinnr
                    res-log.ankunft1    = DATE(INT(ENTRY(2, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(1, reslin-queasy.char3, ";"), "/")))
                                            /*INT(akuntf))*/
                    /*res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(2, reslin-queasy.char3, ";"), "/")))*/
                    /*geral 1B5CD8*/
                    res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                          INT(ENTRY(1, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                          INT("20" + ENTRY(3, ENTRY(3, reslin-queasy.char3, ";"), "/")))
                                          /*INT(abreise))*/
                    res-log.zinr1       = ENTRY(15,reslin-queasy.char3,";")
                    res-log.rate1       = DECIMAL(ENTRY(2,ENTRY(26,breslin.char3,";"),"-"))
                    res-log.rate2       = DECIMAL(ENTRY(2,ENTRY(26,reslin-queasy.char3,";"),"-"))
                    res-log.id1         = ENTRY(21,reslin-queasy.char3,";")
                    res-log.id2         = ENTRY(22,reslin-queasy.char3,";")
                    res-log.date1       = DATE(ENTRY(23,reslin-queasy.char3,";"))
                    res-log.zeit        = reslin-queasy.number2
                    res-log.date1       = reslin-queasy.date2
                    res-log.variance    = res-log.rate1 - res-log.rate2
                    res-log.night-stay  = res-log.abreise1 - res-log.ankunft1.
    
                FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
                    AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN ASSIGN res-log.name1 = guest.NAME.

                    ASSIGN res-log.resstatus = res-line.resstatus.

                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN ASSIGN res-log.room-cat = zimkateg.kurzbez.
                      
                    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                        IF SUBSTR(str,1,6) = "$CODE$" THEN res-log.rate-code  = SUBSTR(str,7).
                    END.

                    FIND FIRST tguest WHERE tguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE tguest THEN DO:
                        ASSIGN res-log.rsv-name = tguest.name + ", " + tguest.vorname1 + " " + tguest.anrede1 + tguest.anredefirma.
                    END.
                    ELSE DO:
                        ASSIGN res-log.rsv-name = "".
                    END.
                END.
            END.                             
        END.
    END.
END.


PROCEDURE create-list1:
    FOR EACH reslin-queasy WHERE key = "ResChanges" 
        AND reslin-queasy.date2 GE fDate 
        AND reslin-queasy.date2 LE tDate
        AND reslin-queasy.resnr = resno NO-LOCK:
        IF reslin-queasy.char3 MATCHES("*;*") AND DECIMAL(ENTRY(19,reslin-queasy.char3,";")) NE DECIMAL(ENTRY(20,reslin-queasy.char3,";")) THEN DO:
            CREATE res-log.
            ASSIGN
                res-log.resnr       = reslin-queasy.resnr
                res-log.reslinnr    = reslin-queasy.reslinnr
                res-log.ankunft1    = DATE(INT(ENTRY(2, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(1, reslin-queasy.char3, ";"), "/")))
                                        /*INT(akuntf))*/
                /*res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(2, reslin-queasy.char3, ";"), "/")))*/
                /*geral 1B5CD8*/
                res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(3, reslin-queasy.char3, ";"), "/")))
                                        /*INT(abreise))*/
                res-log.zinr1       = ENTRY(15,reslin-queasy.char3,";")
                res-log.rate1       = DECIMAL(ENTRY(19,reslin-queasy.char3,";"))
                res-log.rate2       = DECIMAL(ENTRY(20,reslin-queasy.char3,";"))
                res-log.name1       = ENTRY(25,reslin-queasy.char3,";")
                res-log.id1         = ENTRY(21,reslin-queasy.char3,";")
                res-log.id2         = ENTRY(22,reslin-queasy.char3,";")
                res-log.date1       = DATE(ENTRY(23,reslin-queasy.char3,";"))
                res-log.zeit        = number2
                res-log.date1       = reslin-queasy.date2
                res-log.variance    = res-log.rate1 - res-log.rate2
                res-log.night-stay  = res-log.abreise1 - res-log.ankunft1.

            FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr
                AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO:
                ASSIGN res-log.resstatus = res-line.resstatus.

                FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN res-log.room-cat = zimkateg.kurzbez.
                  
                DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,6) = "$CODE$" THEN res-log.rate-code  = SUBSTR(str,7).
                END.

                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:
                    ASSIGN res-log.rsv-name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
                END.
                ELSE DO:
                    ASSIGN res-log.rsv-name = "".
                END.
            END.                                                  
        END.
        ELSE IF STRING(ENTRY(25,reslin-queasy.char3,";")) MATCHES "*CHG Fixrate TO*" THEN DO:
            FIND FIRST breslin WHERE breslin.key = "ResChanges" 
                AND breslin.resnr = reslin-queasy.resnr
                AND breslin.reslinnr = reslin-queasy.reslinnr
                AND breslin.date2 = reslin-queasy.date2 
                AND STRING(ENTRY(25,breslin.char3,";")) MATCHES "*CHG Fixrate FR*"
                AND breslin.number2 = reslin-queasy.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE breslin
                AND DECIMAL(ENTRY(2,ENTRY(26,reslin-queasy.char3,";"),"-")) NE DECIMAL(ENTRY(2,ENTRY(26,breslin.char3,";"),"-")) THEN 
            DO:
                CREATE res-log.
                ASSIGN
                    res-log.resnr       = reslin-queasy.resnr
                    res-log.reslinnr    = reslin-queasy.reslinnr
                    res-log.ankunft1    = DATE(INT(ENTRY(2, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(1, reslin-queasy.char3, ";"), "/")))
                                            /*INT(akuntf))*/
                    /*res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(2, reslin-queasy.char3, ";"), "/")))*/
                    /*geral 1B5CD8*/
                    res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(3, reslin-queasy.char3, ";"), "/")))
                                            /*INT(abreise))*/
                    res-log.zinr1       = ENTRY(15,reslin-queasy.char3,";")
                    res-log.rate1       = DECIMAL(ENTRY(2,ENTRY(26,breslin.char3,";"),"-"))
                    res-log.rate2       = DECIMAL(ENTRY(2,ENTRY(26,reslin-queasy.char3,";"),"-"))
                    res-log.id1         = ENTRY(21,reslin-queasy.char3,";")
                    res-log.id2         = ENTRY(22,reslin-queasy.char3,";")
                    res-log.date1       = DATE(ENTRY(23,reslin-queasy.char3,";"))
                    res-log.zeit        = reslin-queasy.number2
                    res-log.date1       = reslin-queasy.date2
                    res-log.variance    = res-log.rate1 - res-log.rate2
                    res-log.night-stay  = res-log.abreise1 - res-log.ankunft1.
    
                FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
                    AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN ASSIGN res-log.name1 = guest.NAME.
                    
                    ASSIGN res-log.resstatus = res-line.resstatus.

                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN ASSIGN res-log.room-cat = zimkateg.kurzbez.
                      
                    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                       str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                       IF SUBSTR(str,1,6) = "$CODE$" THEN res-log.rate-code  = SUBSTR(str,7).
                    END.

                    FIND FIRST tguest WHERE tguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE tguest THEN DO:
                        ASSIGN res-log.rsv-name = tguest.name + ", " + tguest.vorname1 + " " + tguest.anrede1 + tguest.anredefirma.
                    END.
                    ELSE DO:
                        ASSIGN res-log.rsv-name = "".
                    END.
                END.
            END.                             
        END.
    END.
END.

PROCEDURE create-list2:
    FOR EACH reslin-queasy WHERE key = "ResChanges" 
        AND reslin-queasy.resnr = resno NO-LOCK:
        IF reslin-queasy.char3 MATCHES("*;*") AND DECIMAL(ENTRY(19,reslin-queasy.char3,";")) NE DECIMAL(ENTRY(20,reslin-queasy.char3,";")) THEN DO:
            CREATE res-log.
            ASSIGN
                res-log.resnr       = reslin-queasy.resnr
                res-log.reslinnr    = reslin-queasy.reslinnr
                res-log.ankunft1    = DATE(INT(ENTRY(2, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(1, reslin-queasy.char3, ";"), "/")))
                                        /*INT(akuntf))*/
                /*res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(2, reslin-queasy.char3, ";"), "/")))*/
                /*geral 1B5CD8*/
                res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                        INT(ENTRY(1, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                        INT("20" + ENTRY(3, ENTRY(3, reslin-queasy.char3, ";"), "/")))
                                    /*INT(abreise))*/
                res-log.zinr1       = ENTRY(15,reslin-queasy.char3,";")
                res-log.rate1       = DECIMAL(ENTRY(19,reslin-queasy.char3,";"))
                res-log.rate2       = DECIMAL(ENTRY(20,reslin-queasy.char3,";"))
                res-log.name1       = ENTRY(25,reslin-queasy.char3,";")
                res-log.id1         = ENTRY(21,reslin-queasy.char3,";")
                res-log.id2         = ENTRY(22,reslin-queasy.char3,";")
                res-log.date1       = DATE(ENTRY(23,reslin-queasy.char3,";"))
                res-log.zeit        = number2
                res-log.date1       = reslin-queasy.date2
                res-log.variance    = res-log.rate1 - res-log.rate2
                res-log.night-stay  = res-log.abreise1 - res-log.ankunft1.

            FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr
                AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO:
                ASSIGN res-log.resstatus = res-line.resstatus.

                FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN res-log.room-cat = zimkateg.kurzbez.
                  
                DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,6) = "$CODE$" THEN res-log.rate-code  = SUBSTR(str,7).
                END.

                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:
                    ASSIGN res-log.rsv-name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
                END.
                ELSE DO:
                    ASSIGN res-log.rsv-name = "".
                END.
            END.                                                  
        END.
        ELSE IF STRING(ENTRY(25,reslin-queasy.char3,";")) MATCHES "*CHG Fixrate TO*" THEN DO:
            FIND FIRST breslin WHERE breslin.key = "ResChanges" 
                AND breslin.resnr = reslin-queasy.resnr
                AND breslin.reslinnr = reslin-queasy.reslinnr
                AND breslin.date2 = reslin-queasy.date2 
                AND STRING(ENTRY(25,breslin.char3,";")) MATCHES "*CHG Fixrate FR*"
                AND breslin.number2 = reslin-queasy.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE breslin
                AND DECIMAL(ENTRY(2,ENTRY(26,reslin-queasy.char3,";"),"-")) NE DECIMAL(ENTRY(2,ENTRY(26,breslin.char3,";"),"-")) THEN 
            DO:
                CREATE res-log.
                ASSIGN
                    res-log.resnr       = reslin-queasy.resnr
                    res-log.reslinnr    = reslin-queasy.reslinnr
                    res-log.ankunft1    = DATE(INT(ENTRY(2, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(1, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(1, reslin-queasy.char3, ";"), "/")))
                                            /*INT(akuntf))*/
                    /*res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(2, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(2, reslin-queasy.char3, ";"), "/")))*/
                    /*geral 1B5CD8*/
                    res-log.abreise1    = DATE(INT(ENTRY(2, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                            INT(ENTRY(1, ENTRY(3, reslin-queasy.char3, ";"), "/")),
                                            INT("20" + ENTRY(3, ENTRY(3, reslin-queasy.char3, ";"), "/")))
                                            /*INT(abreise))*/
                    res-log.zinr1       = ENTRY(15,reslin-queasy.char3,";")
                    res-log.rate1       = DECIMAL(ENTRY(2,ENTRY(26,breslin.char3,";"),"-"))
                    res-log.rate2       = DECIMAL(ENTRY(2,ENTRY(26,reslin-queasy.char3,";"),"-"))
                    res-log.id1         = ENTRY(21,reslin-queasy.char3,";")
                    res-log.id2         = ENTRY(22,reslin-queasy.char3,";")
                    res-log.date1       = DATE(ENTRY(23,reslin-queasy.char3,";"))
                    res-log.zeit        = reslin-queasy.number2
                    res-log.date1       = reslin-queasy.date2
                    res-log.variance    = res-log.rate1 - res-log.rate2
                    res-log.night-stay  = res-log.abreise1 - res-log.ankunft1.
    
                FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
                    AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN ASSIGN res-log.name1 = guest.NAME.
                    
                    ASSIGN res-log.resstatus = res-line.resstatus.

                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN ASSIGN res-log.room-cat = zimkateg.kurzbez.
                      
                    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                        IF SUBSTR(str,1,6) = "$CODE$" THEN res-log.rate-code  = SUBSTR(str,7).
                    END.

                    FIND FIRST tguest WHERE tguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE tguest THEN DO:
                        ASSIGN res-log.rsv-name = tguest.name + ", " + tguest.vorname1 + " " + tguest.anrede1 + tguest.anredefirma.
                    END.
                    ELSE DO:
                        ASSIGN res-log.rsv-name = "".
                    END.
                END.
            END.                             
        END.
    END.
END.

