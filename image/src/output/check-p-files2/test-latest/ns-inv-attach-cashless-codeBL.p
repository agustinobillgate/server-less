
DEF TEMP-TABLE b1-list
    FIELD resnr         LIKE bill.resnr
    FIELD rechnr        LIKE bill.rechnr
    FIELD name          LIKE guest.name
    FIELD vorname1      LIKE guest.vorname1
    FIELD anrede1       LIKE guest.anrede1
    FIELD saldo         LIKE bill.saldo
    FIELD printnr       LIKE bill.printnr
    FIELD datum         LIKE bill.datum
    FIELD b-recid       AS INTEGER
    FIELD adresse1      LIKE guest.adresse1
    FIELD wohnort       LIKE guest.wohnort
    FIELD bemerk        LIKE guest.bemerk
    FIELD plz           LIKE guest.plz
    FIELD bill-datum    LIKE bill-line.bill-datum
    FIELD qr-code       AS CHARACTER
    .  

DEFINE INPUT PARAMETER bil-flag  AS INTEGER.
DEFINE INPUT PARAMETER sorttype  AS INTEGER.
DEFINE INPUT PARAMETER gastname  AS CHARACTER.
DEFINE INPUT PARAMETER dept      AS INTEGER.
DEFINE INPUT PARAMETER ba-dept   AS INTEGER.
DEFINE INPUT PARAMETER rechnr    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

DEFINE VARIABLE fr-name AS CHAR INITIAL "".
DEFINE VARIABLE to-name AS CHAR. 
DEFINE BUFFER guest1 FOR guest. 

FOR EACH b1-list:
    DELETE b1-list.
END.

IF bil-flag = 0 THEN RUN disp-bill-list0.

/************************************ PROCEDURE ************************************/
PROCEDURE disp-bill-list0:
    IF sorttype = 1 AND gastname = "" THEN 
    DO: 
        FOR EACH bill WHERE bill.flag EQ bil-flag 
            AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 AND bill.billtyp EQ dept,            
            FIRST guest1 WHERE guest1.gastnr EQ bill.gastnr NO-LOCK 
            BY bill.name BY bill.rechnr DESCENDING:

            RUN cr-table.
        END.
    END. 
    ELSE IF sorttype = 1 AND gastname NE "" THEN 
    DO: 
        IF gastname = "*" THEN to-name = "zz". 
        ELSE 
        DO: 
            fr-name = gastname. 
            to-name = chr(asc(SUBSTR(gastname,1,1)) + 1). 
        END. 

        FOR EACH bill WHERE bill.flag EQ bil-flag 
            AND bill.name GE fr-name AND bill.name LE to-name 
            AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 AND bill.billtyp EQ dept,
            FIRST guest1 WHERE guest1.gastnr EQ bill.gastnr NO-LOCK 
            BY bill.name BY bill.rechnr DESCENDING:
              
            RUN cr-table.
        END.
    END. 
    ELSE IF sorttype = 2 AND rechnr = 0 THEN 
    DO: 
        FOR EACH bill WHERE bill.flag EQ bil-flag 
            AND bill.rechnr GE rechnr AND bill.resnr EQ 0 
            AND bill.reslinnr EQ 1 AND bill.billtyp EQ dept,
            FIRST guest1 WHERE guest1.gastnr EQ bill.gastnr NO-LOCK BY bill.rechnr:
              
            RUN cr-table.
        END.
    END. 
    ELSE IF sorttype = 2 AND rechnr GT 0 THEN 
    DO: 
        FOR EACH bill WHERE bill.flag EQ bil-flag 
            AND bill.rechnr EQ rechnr AND bill.resnr EQ 0 
            AND bill.reslinnr EQ 1 AND bill.billtyp EQ dept,
            FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.rechnr:
              
            RUN cr-table.
        END.
        
        FIND FIRST b1-list NO-ERROR.
        IF NOT AVAILABLE b1-list THEN 
        FOR EACH bill WHERE bill.flag EQ bil-flag 
            AND bill.rechnr GE rechnr AND bill.rechnr LE (rechnr + 1000) 
            AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 AND bill.billtyp EQ dept,
            FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.rechnr:
              
            RUN cr-table.
        END.
    END.
END.

PROCEDURE cr-table:
    CREATE b1-list.
    ASSIGN
        b1-list.resnr         = bill.resnr
        b1-list.rechnr        = bill.rechnr
        b1-list.name          = guest1.name
        b1-list.vorname1      = guest1.vorname1
        b1-list.anrede1       = guest1.anrede1
        b1-list.saldo         = bill.saldo
        b1-list.printnr       = bill.printnr
        b1-list.datum         = bill.datum
        b1-list.b-recid       = RECID(bill)
        b1-list.adresse1      = guest1.adresse1
        b1-list.wohnort       = guest1.wohnort
        b1-list.bemerk        = guest1.bemerk
        b1-list.plz           = guest1.plz        
        b1-list.qr-code       = bill.vesrdepot2
    .
END.

