DEFINE TEMP-TABLE payload-list
    FIELD frm-grp    AS INTEGER
    FIELD to-grp     AS INTEGER
    FIELD storage-no AS INTEGER
    FIELD frm-date   AS DATE
    FIELD to-date    AS DATE
    FIELD case-type  AS INTEGER
.

DEFINE TEMP-TABLE print-list
    FIELD datum     AS DATE
    FIELD t-amount  AS DECIMAL.

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR print-list.

DEFINE VARIABLE frm-grp     AS INTEGER.
DEFINE VARIABLE to-grp      AS INTEGER.
DEFINE VARIABLE storage-no  AS INTEGER.
DEFINE VARIABLE frm-date    AS DATE.
DEFINE VARIABLE to-date     AS DATE.

DEFINE VARIABLE tot-amount  AS DECIMAL.
DEFINE VARIABLE temp-date   AS DATE.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        frm-grp    = payload-list.frm-grp   
        to-grp     = payload-list.to-grp    
        storage-no = payload-list.storage-no
        frm-date   = payload-list.frm-date  
        to-date    = payload-list.to-date   
    .

    IF case-type EQ 1 THEN
    DO:
        IF storage-no EQ 0 THEN
        DO:
            FOR EACH l-op WHERE l-op.datum GE frm-date 
                AND l-op.datum LE to-date 
                AND l-op.lief-nr GT 0
                AND l-op.loeschflag LE 1
                AND l-op.op-art EQ 1
                NO-LOCK USE-INDEX lief_ix, 
                FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
                AND l-artikel.endkum GE frm-grp
                AND l-artikel.endkum LE to-grp 
                NO-LOCK, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK
                BY l-op.datum:

                IF temp-date NE l-op.datum THEN
                DO:
                    CREATE print-list.
                    print-list.datum = l-op.datum.

                    temp-date = l-op.datum.
                END.

                tot-amount = tot-amount + l-op.warenwert.
                print-list.t-amount = print-list.t-amount + l-op.warenwert.
            END.
        END.
        ELSE
        DO:
            FOR EACH l-op WHERE l-op.datum GE frm-date 
                AND l-op.datum LE to-date 
                AND l-op.lief-nr GT 0
                AND l-op.loeschflag LE 1
                AND l-op.op-art EQ 1
                AND l-op.lager-nr EQ storage-no 
                NO-LOCK USE-INDEX lief_ix, 
                FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
                AND l-artikel.endkum GE frm-grp
                AND l-artikel.endkum LE to-grp 
                NO-LOCK, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK
                BY l-op.datum:

                IF temp-date NE l-op.datum THEN
                DO:
                    CREATE print-list.
                    print-list.datum = l-op.datum.

                    temp-date = l-op.datum.
                END.

                tot-amount = tot-amount + l-op.warenwert.
                print-list.t-amount = print-list.t-amount + l-op.warenwert.
            END.
        END.

        CREATE print-list.
        ASSIGN
            print-list.datum    = ?
            print-list.t-amount = tot-amount
        .
    END.
    ELSE IF case-type EQ 2 THEN
    DO:
        IF storage-no EQ 0 THEN
        DO:
            FOR EACH l-ophis WHERE l-ophis.datum GE frm-date 
                AND l-ophis.datum LE to-date 
                AND l-ophis.lief-nr GT 0 
                AND l-ophis.op-art EQ 1 
                AND l-ophis.anzahl NE 0 
                AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
                AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
                NO-LOCK USE-INDEX lief-op-dat_ix, 
                FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
                AND l-artikel.endkum GE frm-grp
                AND l-artikel.endkum LE to-grp
                NO-LOCK,
                FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK
                BY l-ophis.datum:

                IF temp-date NE l-ophis.datum THEN
                DO:
                    CREATE print-list.
                    print-list.datum = l-ophis.datum.

                    temp-date = l-ophis.datum.
                END.

                tot-amount = tot-amount + l-ophis.warenwert.
                print-list.t-amount = print-list.t-amount + l-ophis.warenwert.
            END.
        END.
        ELSE
        DO:
            FOR EACH l-ophis WHERE l-ophis.datum GE frm-date 
                AND l-ophis.datum LE to-date 
                AND l-ophis.lief-nr GT 0  
                AND l-ophis.op-art EQ 1 
                AND l-ophis.anzahl NE 0 
                AND l-ophis.lager-nr EQ storage-no 
                AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
                AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
                NO-LOCK USE-INDEX lief-op-dat_ix, 
                FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
                AND l-artikel.endkum GE frm-grp
                AND l-artikel.endkum LE to-grp
                NO-LOCK,
                FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK
                BY l-ophis.datum:

                IF temp-date NE l-ophis.datum THEN
                DO:
                    CREATE print-list.
                    print-list.datum = l-ophis.datum.

                    temp-date = l-ophis.datum.
                END.

                tot-amount = tot-amount + l-ophis.warenwert.
                print-list.t-amount = print-list.t-amount + l-ophis.warenwert.
            END.
        END.

        CREATE print-list.
        ASSIGN
            print-list.datum    = ?
            print-list.t-amount = tot-amount
        .
    END.
END.
