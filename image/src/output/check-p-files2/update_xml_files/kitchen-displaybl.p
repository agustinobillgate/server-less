DEFINE TEMP-TABLE kds-list
    FIELD count-pos     AS INTEGER
    FIELD curr-flag     AS CHARACTER
    FIELD qhead-recid   AS INTEGER
    FIELD qline-recid   AS INTEGER
    FIELD recid-hbline  AS INTEGER
    FIELD bill-no       AS INTEGER
    FIELD dept-no       AS INTEGER
    FIELD table-no      AS INTEGER
    FIELD user-post-id  AS CHARACTER
    FIELD user-name     AS CHARACTER
    FIELD artikel-no    AS INTEGER
    FIELD artikel-qty   AS INTEGER
    FIELD artikel-name  AS CHARACTER    
    FIELD sp-request    AS CHARACTER
    FIELD post-date     AS DATE
    FIELD post-time     AS INTEGER
    FIELD post-timestr  AS CHARACTER
    FIELD status-order  AS CHAR
    FIELD void-menu     AS LOGICAL
    FIELD remain-qty    AS INTEGER
    FIELD dept-name     AS CHARACTER
    FIELD system-date   AS DATE
	FIELD served-time	AS CHARACTER
    /*FIELD void-nr       AS INTEGER*/
    .

DEFINE TEMP-TABLE summary-artlist
    FIELD artikel-no    AS INTEGER
    FIELD artikel-qty   AS INTEGER
    FIELD artikel-name  AS CHARACTER
    FIELD artikel-dept  AS INTEGER
    FIELD subgroup-no   AS INTEGER
    FIELD subgroup-name AS CHARACTER
    FIELD void-menu     AS LOGICAL
    .

DEFINE TEMP-TABLE summ-list
    FIELD artikel-no    AS INTEGER
    FIELD artikel-qty   AS INTEGER
    FIELD artikel-name  AS CHARACTER
    FIELD artikel-dept  AS INTEGER
    FIELD subgroup-no   AS INTEGER
    FIELD subgroup-name AS CHARACTER
    .


DEFINE TEMP-TABLE header-list
    FIELD rechnr    AS INT
    FIELD tablenr   AS INT
    FIELD zeit      AS INT
    FIELD waiters   AS CHAR
    FIELD datum     AS DATE
	FIELD rec-id	AS INT
	FIELD status-no AS INT
	FIELD dept-no	AS INT
    FIELD dept-name AS CHARACTER
    FIELD sysdate   AS DATE
    FIELD sysdatetime AS DATETIME
    .

DEFINE TEMP-TABLE order-list
    FIELD rechnr    AS INT
    FIELD tablenr   AS INT
    FIELD zeit      AS INT
    FIELD datum     AS DATE
    FIELD prod      AS CHAR
    FIELD note      AS CHAR
    FIELD qty       AS INT
    FIELD flag      AS LOGICAL
    FIELD status-no AS INT
    FIELD subgrpno  AS INT
    FIELD artno     AS INT
	FIELD rec-id	AS INT
    FIELD header-recid AS INT
    FIELD sysdate   AS DATE
	FIELD served-time	AS CHARACTER
    FIELD dept-no	AS INT
    .


DEFINE TEMP-TABLE done-list LIKE summary-artlist.
DEFINE TEMP-TABLE summary-list LIKE summary-artlist.
DEFINE TEMP-TABLE orderlist LIKE order-list.
DEFINE TEMP-TABLE hdr-list LIKE header-list.
/**/
DEFINE INPUT PARAMETER casetype     AS INT.
DEFINE INPUT PARAMETER dept-number  AS INTEGER.
DEFINE INPUT PARAMETER kp-number    AS INTEGER.

DEFINE OUTPUT PARAMETER TABLE FOR header-list.
DEFINE OUTPUT PARAMETER TABLE FOR orderlist.
DEFINE OUTPUT PARAMETER TABLE FOR summary-list.
/**/
/*
DEFINE VARIABLE casetype    AS INT      INIT 1.
DEFINE VARIABLE dept-number AS INTEGER  INIT 1.
DEFINE VARIABLE kp-number   AS INTEGER  INIT 98.
*/
MESSAGE "CASE=" + string(casetype) + "|DEPT=" + string(dept-number) "|KP=" + string(kp-number) VIEW-AS ALERT-BOX INFO BUTTONS OK.
RUN kitchen-display-getdata-cld_1bl.p (1,kp-number,
                                     OUTPUT TABLE kds-list, 
                                     OUTPUT TABLE summary-artlist, OUTPUT TABLE done-list).

DEFINE BUFFER bsumlist FOR summary-artlist.
DEFINE BUFFER bsummary-list FOR summary-artlist.
DEFINE VAR subgrp   AS INT.

FOR EACH bsummary-list WHERE bsummary-list.void-menu EQ NO BY bsummary-list.subgroup-name:
    IF subgrp NE bsummary-list.subgroup-no THEN subgrp = bsummary-list.subgroup-no.
    FIND FIRST summary-list WHERE summary-list.subgroup-no EQ subgrp NO-ERROR.
    IF NOT AVAILABLE summary-list THEN
    DO:
        CREATE summary-list.
        summary-list.artikel-name =  CAPS(bsummary-list.subgroup-name).
    END.

    FOR EACH bsumlist WHERE bsumlist.subgroup-no EQ subgrp AND bsumlist.void-menu EQ NO NO-LOCK BY bsumlist.artikel-qty DESC:
        FIND FIRST summary-list WHERE summary-list.artikel-no EQ bsumlist.artikel-no NO-ERROR.
        IF NOT AVAILABLE summary-list THEN
        DO:
            CREATE summary-list.
            BUFFER-COPY bsumlist TO summary-list.
        END.
    END.
END.

DEF VAR qheadrecid AS INT.
FOR EACH kds-list:
    IF kds-list.curr-flag EQ "kds-header" THEN
    DO:
        CREATE header-list.
        ASSIGN 
            header-list.rechnr  = kds-list.bill-no  
            header-list.tablenr = kds-list.table-no  
            header-list.zeit    = kds-list.post-time  
            header-list.waiters = kds-list.user-name
            header-list.datum   = kds-list.post-date
			header-list.rec-id	= kds-list.qhead-recid
			header-list.dept-no = kds-list.dept-no
            header-list.dept-name = kds-list.dept-name
            header-list.sysdate = kds-list.system-date
            .           

        IF kds-list.status-order EQ "NEW" THEN header-list.status-no = 0.
        ELSE IF kds-list.status-order EQ "COOKING" THEN header-list.status-no = 1.
        ELSE IF kds-list.status-order EQ "DONE" THEN header-list.status-no = 2.
        ELSE IF kds-list.status-order EQ "SERVED" THEN header-list.status-no = 3.
        ELSE IF kds-list.status-order EQ "SERVEDBYSYSTEM" THEN header-list.status-no = 4.
    END.
    ELSE IF kds-list.curr-flag EQ "kds-line" THEN
    DO:
        CREATE order-list.
        ASSIGN 
            order-list.rechnr       = kds-list.bill-no   
            order-list.tablenr      = kds-list.table-no  
            order-list.zeit         = kds-list.post-time 
            order-list.datum        = kds-list.post-date 
            order-list.prod         = kds-list.artikel-name 
            order-list.note         = kds-list.sp-request
            order-list.qty          = kds-list.artikel-qty
            order-list.flag         = NO
            order-list.artno        = kds-list.artikel-no
			order-list.rec-id	    = kds-list.qline-recid
            order-list.header-recid = kds-list.qhead-recid
            order-list.sysdate      = kds-list.system-date
			order-list.served-time	= kds-list.served-time
            order-list.dept-no      = kds-list.dept-no
            .

        IF kds-list.status-order EQ "NEW" THEN order-list.status-no = 0.
        ELSE IF kds-list.status-order EQ "COOKING" THEN order-list.status-no = 1.
        ELSE IF kds-list.status-order EQ "DONE" THEN order-list.status-no = 2.
        ELSE IF kds-list.status-order EQ "SERVED" THEN order-list.status-no = 3.
        ELSE IF kds-list.status-order EQ "SERVEDBYSYSTEM" THEN order-list.status-no = 4.

        FIND FIRST h-artikel WHERE h-artikel.departement EQ kds-list.dept-no
            AND h-artikel.artnr EQ order-list.artno
            AND h-artikel.bondruckernr[1] EQ kp-number NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN order-list.subgrpno = h-artikel.zwkum.
    END.
END.
/*
FOR EACH order-list:
    FIND FIRST header-list WHERE header-list.rechnr EQ order-list.rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE header-list THEN
    DO:
        order-list.header-recid = header-list.rec-id.
    END.
END.
*/
DEFINE BUFFER order FOR order-list.
DEFINE VARIABLE tbno   AS INT.
DEFINE VARIABLE billno AS INT.

subgrp = 0.
billno = 0.
tbno   = 0.
/*
FOR EACH order-list :
    IF subgrp NE order-list.subgrpno THEN 
        ASSIGN 
        billno = order-list.rechnr 
        tbno   = order-list.tablenr
        subgrp = order-list.subgrpno.
    FIND FIRST orderlist WHERE orderlist.subgrpno EQ subgrp AND orderlist.rechnr EQ billno AND orderlist.tablenr EQ tbno NO-ERROR.
    IF NOT AVAILABLE orderlist THEN
    DO:
        FIND FIRST wgrpdep WHERE wgrpdep.departement EQ dept-number AND wgrpdep.zknr EQ subgrp NO-LOCK NO-ERROR.
        CREATE orderlist.
        orderlist.prod         = CAPS(wgrpdep.bezeich).
        orderlist.flag         = YES.
        orderlist.rechnr       = billno.
        orderlist.header-recid = order-list.header-recid.

        FOR EACH order WHERE order.rechnr EQ billno AND order.tablenr EQ tbno AND order.subgrpno EQ subgrp NO-LOCK:
            CREATE orderlist.
            BUFFER-COPY order TO orderlist.
        END.
    END.
END.
*/
FOR EACH order-list BY order-list.subgrp BY order-list.status-no:
    IF subgrp NE order-list.subgrpno THEN 
        ASSIGN 
        billno = order-list.rechnr 
        tbno   = order-list.tablenr
        subgrp = order-list.subgrpno.

    FIND FIRST orderlist WHERE orderlist.header-recid EQ order-list.header-recid AND orderlist.subgrp EQ subgrp NO-ERROR.
    IF NOT AVAILABLE orderlist THEN
    DO:
        FIND FIRST wgrpdep WHERE wgrpdep.departement EQ order-list.dept-no AND wgrpdep.zknr EQ subgrp NO-LOCK NO-ERROR.
        CREATE orderlist.
        orderlist.prod         = CAPS(wgrpdep.bezeich).
        orderlist.subgrpno     = wgrpdep.zknr.
        orderlist.flag         = YES.
        orderlist.rechnr       = billno.
        orderlist.header-recid = order-list.header-recid.
        orderlist.note         = "".
    END.
    CREATE orderlist.
    BUFFER-COPY order-list TO orderlist.
    DELETE order-list.
END.

FOR EACH header-list BY header-list.sysdate DESC BY header-list.zeit:
    FIND FIRST orderlist WHERE orderlist.header-recid EQ header-list.rec-id AND orderlist.artno NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE orderlist THEN
    DO:
        header-list.sysdate = orderlist.sysdate.
    END.

    IF header-list.dept-name EQ "" THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num EQ header-list.dept-no NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN
        DO:
            header-list.dept-name = hoteldpt.depart.
        END.
    END.

    CREATE hdr-list.
    BUFFER-COPY header-list TO hdr-list.
    hdr-list.sysdatetime = DATETIME(STRING(hdr-list.sysdate) + " " + STRING(hdr-list.zeit,"HH:MM")).
END.

EMPTY TEMP-TABLE header-list.
FOR EACH hdr-list BY hdr-list.sysdatetime:
    CREATE header-list.
    BUFFER-COPY hdr-list TO header-list.
END.
/*
CURRENT-WINDOW:WIDTH = 200.
FOR EACH header-list:
    DISP header-list WITH WIDTH 199.
END.

FOR EACH orderlist:
    DISP orderlist WITH WIDTH 199.
END.
*/
