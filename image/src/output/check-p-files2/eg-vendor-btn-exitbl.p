
DEFINE TEMP-TABLE vendor LIKE eg-vendor.
DEF BUFFER queasy1 FOR eg-vendor.

DEF INPUT PARAMETER TABLE FOR vendor.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST vendor.
IF case-type = 1 THEN
DO :
    CREATE eg-vendor.
    RUN fill-new-vendor.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST eg-vendor WHERE RECID(eg-vendor) = rec-id.
    FIND FIRST queasy1 WHERE queasy1.vendor-nr = vendor.vendor-nr AND ROWID(queasy1) NE ROWID(eg-vendor) NO-LOCK NO-ERROR.
    IF AVAILABLE queasy1 THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        FIND CURRENT eg-vendor EXCLUSIVE-LOCK.  
        eg-vendor.vendor-nr = vendor.vendor-nr.
        eg-vendor.bezeich = vendor.bezeich.
        eg-vendor.address = vendor.address.
        eg-vendor.phone = vendor.phone.
        eg-vendor.website = vendor.website.
        eg-vendor.email = vendor.email.
        eg-vendor.fax = vendor.fax.
        eg-vendor.contact-person = vendor.contact-person.

        FIND CURRENT eg-vendor NO-LOCK . 
        RELEASE eg-vendor.
    END.
END.

PROCEDURE fill-new-vendor:
    eg-vendor.vendor-nr = vendor.vendor-nr.
    eg-vendor.bezeich   = vendor.bezeich.
    eg-vendor.address   = vendor.address.
    eg-vendor.phone     = vendor.phone.
    eg-vendor.website   = vendor.website.
    eg-vendor.email     = vendor.email.
    eg-vendor.fax       = vendor.fax.
    eg-vendor.contact-person = vendor.contact-person .
END.  

