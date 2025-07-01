DEFINE TEMP-TABLE t-resline LIKE bk-reser.
DEF TEMP-TABLE waiting-list
    FIELD veran-nr  LIKE bk-reser.veran-nr
    FIELD NAME      LIKE guest.NAME
    FIELD von-zeit  LIKE bk-reser.von-zeit
    FIELD bis-zeit  LIKE bk-reser.bis-zeit
    FIELD raum      LIKE bk-reser.raum
    FIELD rec-id    AS INT.

DEFINE INPUT PARAMETER case-type        AS INT.
DEFINE INPUT PARAMETER curr-room        AS CHAR.
DEFINE INPUT PARAMETER curr-status      AS INT.
DEFINE INPUT PARAMETER curr-i           AS INT.
DEFINE INPUT PARAMETER language-code    AS INT.
DEFINE INPUT PARAMETER rml-resnr        AS INT.
DEFINE INPUT PARAMETER rml-reslinnr     AS INT.

DEFINE INPUT PARAMETER answer-msgstr2 AS LOGICAL.
DEFINE INPUT PARAMETER answer-msgstr3 AS LOGICAL.
DEFINE INPUT PARAMETER cancel-str       AS CHAR.
DEFINE INPUT PARAMETER user-init        AS CHAR.

DEFINE OUTPUT PARAMETER msg-str1    AS CHAR.
DEFINE OUTPUT PARAMETER msg-str2    AS CHAR.
DEFINE OUTPUT PARAMETER msg-str3     AS CHAR.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR waiting-list.
    
DEF VAR datum       AS DATE. 
DEF VAR raum        AS CHAR. 
DEF VAR von-zeit    AS CHAR. 
DEF VAR bis-zeit    AS CHAR. 
DEF VAR resstatus   AS INTEGER. 
DEF VAR b1-resnr    AS INTEGER. 
DEF VAR b1-reslinnr AS INTEGER. 
DEF VAR curr-resnr  AS INTEGER. 

IF user-init EQ ? OR user-init EQ "" THEN
DO:
    mess-result = "user init must be filled in".
    RETURN.
END.

IF case-type EQ 1 THEN
DO:
    IF curr-i GT 0 THEN
    DO: 
        RUN ba-plan-res-cancel1bl.p(language-code, rml-resnr, rml-reslinnr,
                                    OUTPUT msg-str1,OUTPUT msg-str2, OUTPUT msg-str3).

        mess-result = "get messages success".
        RETURN.
    END.
    ELSE
    DO:
        mess-result = "Select the reservation first. curr-i cannot using 0 value".
        RETURN.
    END.
END.
ELSE IF case-type EQ 2 THEN
DO:
    IF answer-msgstr2 EQ YES THEN
    DO:
        IF cancel-str EQ "" THEN
        DO:
            mess-result = "Cancel Reason Must be Filled In".
            RETURN.
        END.
        ELSE
        DO:
            b1-resnr    = rml-resnr. 
            b1-reslinnr = rml-reslinnr. 
            IF answer-msgstr3 EQ YES THEN
            DO:
                RUN ba-plan-res-cancel2bl.p (rml-resnr, rml-reslinnr,OUTPUT TABLE t-resline).
                
                FOR EACH t-resline NO-LOCK:
                      ASSIGN 
                          datum     = t-resline.datum 
                          raum      = t-resline.raum 
                          von-zeit  = t-resline.von-zeit 
                          bis-zeit  = t-resline.bis-zeit 
                          resstatus = t-resline.resstatus 
                          .
                      RUN ba-plan-res-cancel3bl.p (INPUT-OUTPUT b1-resnr, INPUT-OUTPUT b1-reslinnr,
                                     t-resline.veran-nr,t-resline.veran-resnr,datum, raum, cancel-str, user-init,
                                     OUTPUT curr-resnr).
                END.
                RUN check-waitinglist(datum, raum, von-zeit, bis-zeit, resstatus).
                mess-result = "Cancel Banquet Reservation Success".
            END.
            ELSE
            DO:
                RUN ba-plan-res-cancel4bl.p (INPUT-OUTPUT b1-resnr, INPUT-OUTPUT b1-reslinnr,
                                    rml-resnr, rml-reslinnr, cancel-str, user-init, 
                                    OUTPUT curr-resnr,OUTPUT datum, OUTPUT raum, 
                                    OUTPUT von-zeit, OUTPUT bis-zeit, OUTPUT resstatus).
                RUN check-waitinglist(datum, raum, von-zeit, bis-zeit, resstatus).
                mess-result = "Cancel Banquet Reservation Success".
            END.
        END.
    END.
    ELSE
    DO:
        mess-result = "no acction needed with this parameters".
        RETURN.
    END.
END.

PROCEDURE check-waitinglist: 
    DEF INPUT PARAMETER datum     AS DATE. 
    DEF INPUT PARAMETER raum      AS CHAR. 
    DEF INPUT PARAMETER von-zeit  AS CHAR. 
    DEF INPUT PARAMETER bis-zeit  AS CHAR. 
    DEF INPUT PARAMETER resstatus AS INTEGER. 
     
    DEF VAR avail-resline AS LOGICAL.
    RUN ba-plan-check-waitinglistbl.p (datum, raum, von-zeit, bis-zeit, resstatus, 
                                       OUTPUT avail-resline, OUTPUT TABLE waiting-list).
    IF NOT avail-resline THEN RETURN.
    /*
        q3-list.veran-nr COLUMN-LABEL "ResNo" 
        q3-list.NAME 
        q3-list.von-zeit COLUMN-LABEL "From Time" 
        q3-list.bis-zeit COLUMN-LABEL "To Time" 
        q3-list.raum     COLUMN-LABEL "Room" 
    */
END.
