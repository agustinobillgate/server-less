DEF TEMP-TABLE str-list
    FIELD s AS CHAR FORMAT "x(135)".

DEF TEMP-TABLE art-list
    FIELD datum AS CHARACTER
    FIELD devnote AS CHARACTER
    FIELD qty AS CHARACTER
    FIELD val AS CHARACTER
    FIELD in-qty AS CHARACTER
    FIELD in-val AS CHARACTER
    FIELD out-qty AS CHARACTER
    FIELD out-val AS CHARACTER
    FIELD note AS CHARACTER.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER s-artnr AS INT.
DEF INPUT  PARAMETER mm AS INT.
DEF INPUT  PARAMETER yy AS INT.
DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager AS INT.
DEF INPUT  PARAMETER show-price AS LOGICAL.

DEF OUTPUT PARAMETER anfDate     AS DATE NO-UNDO.
DEF OUTPUT PARAMETER endDate     AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR art-list.
/*
DEF VAR pvILanguage    AS INTEGER  INIT 1.
DEF VAR s-artnr AS INT INIT 1101001.
DEF VAR mm AS INT INIT 12.
DEF VAR yy AS INT INIT 2018.
DEF VAR from-lager AS INT INIT 1.
DEF VAR to-lager AS INT INIT 99.
DEF VAR show-price AS LOGICAL INIT YES.

DEF VAR anfDate     AS DATE NO-UNDO.
DEF VAR endDate     AS DATE NO-UNDO.    */

RUN stock-hmovelist-create-listbl.p
    (pvILanguage, s-artnr, mm, yy, from-lager, to-lager, show-price,
    OUTPUT anfDate, OUTPUT endDate, OUTPUT TABLE str-list).

FOR EACH str-list:
    CREATE art-list.
    ASSIGN
        art-list.datum = SUBSTRING(str-list.s,1,8)
        art-list.devnote = SUBSTRING(str-list.s,9,16)
        art-list.qty = SUBSTRING(str-list.s,25,11)
        art-list.val = SUBSTRING(str-list.s,36,15)
        art-list.in-qty = SUBSTRING(str-list.s,51,13)
        art-list.in-val = SUBSTRING(str-list.s,64,14)
        art-list.out-qty = SUBSTRING(str-list.s,78,13)
        art-list.out-val = SUBSTRING(str-list.s,91,14)
        art-list.note = SUBSTRING(str-list.s,116,16).
END.
/*
FOR EACH str-list:
    DISP SUBSTR(str-list.s,1,78) FORMAT "x(78)".
END.

FOR EACH art-list.
    DISP art-list.devnote art-list.qty art-list.in-val FORMAT "x(15)".
END.*/


          

