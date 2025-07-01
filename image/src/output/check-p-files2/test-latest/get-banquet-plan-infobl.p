DEFINE TEMP-TABLE rsl 
  FIELD resnr       AS INTEGER 
  FIELD reslinnr    AS INTEGER 
  FIELD resstatus   AS INTEGER 
  FIELD sdate       AS DATE COLUMN-LABEL "Beg-Date" /*FONT 2 */
  FIELD ndate       AS DATE COLUMN-LABEL "End-Date" /*FONT 2 */
  FIELD stime       LIKE bk-reser.von-zeit COLUMN-LABEL "Start" /*FONT 2 */
  FIELD ntime       LIKE bk-reser.bis-zeit COLUMN-LABEL " End" /*FONT 2*/
  FIELD created-date AS DATE COLUMN-LABEL "Created" /*FONT 2*/
  FIELD venue       LIKE bk-raum.raum COLUMN-LABEL "Venue" /*FONT 2*/
  FIELD userinit    AS CHAR FORMAT "x(4)" COLUMN-LABEL "ID" /*FONT 2*/
. 
 
DEFINE INPUT PARAMETER curr-view    AS CHAR.
DEFINE INPUT PARAMETER rml-bezeich  AS CHAR.
DEFINE INPUT PARAMETER rml-raum     AS CHAR.
DEFINE INPUT PARAMETER rml-nr       AS INT.
DEFINE INPUT PARAMETER rml-blocked  AS INT.
DEFINE INPUT PARAMETER rml-resnr    AS INT.
DEFINE INPUT PARAMETER rml-reslinnr AS INT.
DEFINE INPUT PARAMETER curr-i       AS INT.
DEFINE INPUT PARAMETER from-date    AS DATE.

DEFINE OUTPUT PARAMETER mess-str AS CHAR.
DEFINE OUTPUT PARAMETER info1    AS CHAR.
DEFINE OUTPUT PARAMETER info2    AS CHAR.
DEFINE OUTPUT PARAMETER info3    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR rsl.

DEFINE VARIABLE curr-room   AS CHAR.
DEFINE VARIABLE curr-status AS INT.
DEFINE VARIABLE odate       AS DATE.
DEFINE VARIABLE b1-resnr    AS INT.
DEFINE VARIABLE b1-reslinnr AS INT.
DEFINE VARIABLE out-i       AS INT.

RUN mrl.

PROCEDURE mrl: 
    curr-room   = rml-raum. 
    curr-status = rml-nr. 
    RUN marking-rml2. 
END. 

PROCEDURE marking-rml2: 
    DEFINE VARIABLE old-room   LIKE bk-reser.raum. 
    DEFINE VARIABLE old-status LIKE bk-reser.resstatus. 
    
    IF rml-blocked NE 0 THEN 
    DO:   
        mess-str = "This is blocked Reservation!".
        RETURN.
    END.
    
    odate = from-date. 
    IF curr-view = "weekly"  THEN 
    DO:
        /*RUN box-clockUI.p(from-date,curr-i,rml.raum,rml.nr ,OUTPUT odate,OUTPUT out-i). 
        FIND FIRST rml WHERE rml.raum = curr-room AND rml.nr = curr-status NO-LOCK NO-ERROR. */
    END. 
    RUN marking-rml(curr-i). 
END. 

PROCEDURE marking-rml: 
    DEFINE INPUT PARAMETER i AS INTEGER. 
    
    RUN disp-resdata. 
    
    b1-resnr    = rml-resnr. 
    b1-reslinnr = rml-reslinnr. 
END. 

PROCEDURE init-info: 
    info1 = "". 
    info2 = "". 
    info3 = "". 
    EMPTY TEMP-TABLE rsl. 
END. 

PROCEDURE disp-resdata: 
    DEFINE VARIABLE b-time AS INTEGER. 
    DEFINE VARIABLE i AS INTEGER. 

    RUN init-info. 

    /*info1 = rml-bezeich  + chr(10). */
    RUN ba-plan-disp-resdatabl.p (rml-raum, rml-resnr, rml-reslinnr,
        OUTPUT info1, OUTPUT info2, OUTPUT info3, OUTPUT TABLE rsl).

    IF curr-view = "daily" THEN 
    DO: 
        b-time = round((curr-i / 2), 0) - 1. 
        info2  = "Date: " + STRING(from-date) + "  Time:". 
        IF ROUND((curr-i / 2) - 0.1, 0) * 2 LT curr-i THEN 
        info2 = info2 + STRING(b-time,"99") + ":00 - " + STRING(b-time,"99") + ":30". 
        ELSE 
        info2 = info2 + STRING(b-time,"99") + ":30 - " + STRING(b-time + 1,"99") + ":00". 
    END. 
    ELSE 
    DO: 
        info2 = "Date: " + STRING(odate) + "  Time:". 
        IF out-i GT 0 THEN 
        DO: 
            b-time = round((out-i / 2), 0) - 1. 
            IF round((out-i / 2) - 0.1, 0) * 2 LT out-i THEN 
            info2 = info2 + STRING(b-time,"99") + ":00 - " + STRING(b-time,"99") + ":30". 
            ELSE 
            info2 = info2 + STRING(b-time,"99") + ":30 - " + STRING(b-time + 1,"99") + ":00". 
        END. 
        ELSE 
        DO: 
            b-time = 0. 
            info2  = info2 + "00:00 - 00:00". 
        END. 
    END.
END. 
 

 
