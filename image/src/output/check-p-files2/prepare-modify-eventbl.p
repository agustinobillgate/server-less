DEFINE TEMP-TABLE room-list
    FIELD room-id   AS CHAR
    FIELD room-name AS CHAR.

DEFINE TEMP-TABLE table-setup
    FIELD room-id       AS CHAR
    FIELD seating       AS CHAR
    FIELD max-person    AS INT
    FIELD assign-person AS INT.

DEF TEMP-TABLE rsv-table LIKE bk-reser
    FIELD rec-id AS INT
    FIELD t-vorbereit LIKE bk-raum.vorbereit.
DEF TEMP-TABLE t-bk-reser  LIKE bk-reser
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE bset      LIKE bk-rset.
DEFINE TEMP-TABLE bsetup    LIKE bk-setup.
DEFINE TEMP-TABLE braum     LIKE bk-raum
    FIELD rmflag    AS LOGICAL.
DEFINE TEMP-TABLE bfunc     LIKE bk-func.
DEFINE TEMP-TABLE breser    LIKE bk-reser.
DEFINE BUFFER broom         FOR braum.

DEFINE INPUT PARAMETER rml-resnr    AS INT. 
DEFINE INPUT PARAMETER rml-reslinnr AS INT.
DEFINE INPUT-OUTPUT PARAMETER curr-date AS DATE.
DEFINE OUTPUT PARAMETER begin-time  AS CHAR.
DEFINE OUTPUT PARAMETER ending-time AS CHAR.
DEFINE OUTPUT PARAMETER begin-i2    AS INT.
DEFINE OUTPUT PARAMETER ending-i2   AS INT.
DEFINE OUTPUT PARAMETER sorttype    AS INT.
DEFINE OUTPUT PARAMETER bk-reser-resstatus AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER chg-date    AS DATE.
DEFINE OUTPUT PARAMETER begin-i     AS INT.
DEFINE OUTPUT PARAMETER ending-i    AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.
DEFINE OUTPUT PARAMETER TABLE FOR table-setup.
DEFINE OUTPUT PARAMETER TABLE FOR rsv-table.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-reser.
DEFINE OUTPUT PARAMETER TABLE FOR breser.

/*DEFINE VARIABLE begin-i   LIKE bk-reser.von-i.  
DEFINE VARIABLE ending-i  LIKE bk-reser.bis-i. */
DEFINE VARIABLE update-ok AS LOGICAL. 
DEFINE VARIABLE msg AS INT.
DEFINE VARIABLE ci-date AS DATE.
DEFINE VARIABLE r-recid AS INTEGER.
DEFINE BUFFER rl FOR bk-reser. 

FIND FIRST rl WHERE rl.veran-nr EQ rml-resnr AND rl.veran-seite EQ rml-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE rl THEN r-recid = RECID(rl).

RUN prepare-chg-start-end-cldbl.p
    (rml-resnr, rml-reslinnr, curr-date, OUTPUT chg-date, OUTPUT ci-date,
    OUTPUT update-ok, OUTPUT begin-i2, OUTPUT ending-i2,
    OUTPUT begin-time, OUTPUT begin-i, OUTPUT ending-time,
    OUTPUT ending-i, OUTPUT msg, OUTPUT TABLE rsv-table,
    OUTPUT TABLE t-bk-reser).

RUN prepare-chg-bastatus-linebl.p (r-recid, OUTPUT sorttype, OUTPUT bk-reser-resstatus).

RUN prepare-chg-roombl.p (OUTPUT TABLE braum, OUTPUT TABLE bset, 
                          OUTPUT TABLE bsetup, OUTPUT TABLE bfunc, 
                          OUTPUT TABLE breser).
FOR EACH bset NO-LOCK:
    FIND FIRST braum WHERE braum.raum EQ bset.raum NO-LOCK NO-ERROR.
    FIND FIRST bsetup WHERE bsetup.setup-id EQ bset.setup-id NO-LOCK NO-ERROR.
    FIND FIRST bfunc WHERE bfunc.veran-nr EQ rml-resnr AND bfunc.veran-seite EQ rml-reslinnr NO-LOCK NO-ERROR. 
    CREATE table-setup.
    ASSIGN
        table-setup.room-id       = braum.raum
        table-setup.seating       = bsetup.bezeich
        table-setup.max-person    = bset.personen 
        table-setup.assign-person = bfunc.rpersonen[1].
END.

FOR EACH braum:
    CREATE room-list.
    ASSIGN 
        room-list.room-id   = braum.raum   
        room-list.room-name = braum.bezeich.
END.
