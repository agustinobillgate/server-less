
DEF INPUT PARAMETER q-order-nr  AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER billdate    AS DATE.


RUN del-po. 
/*MTRUN create-bediener.
RUN disp-it.*/

PROCEDURE del-po :
    DEFINE buffer fa-od  FOR fa-order. 
    DEFINE buffer fa-odhd  FOR fa-ordheader.

    FIND FIRST fa-odhd WHERE fa-odhd.order-nr = q-order-nr EXCLUSIVE-LOCK.
    ASSIGN fa-odhd.activeflag   = 2
           fa-odhd.Delete-By    = user-init /*bediener.username*/
           fa-odhd.Delete-Date  = billdate         
           fa-odhd.Delete-Time  = TIME.

    /*FIND CURRENT fa-odhd NO-LOCK. */
    RELEASE fa-odhd.

    FOR EACH fa-od WHERE fa-od.order-nr = fa-ordheader.order-nr AND fa-od.activeflag = 0 EXCLUSIVE-LOCK: 
        ASSIGN fa-od.activeflag   = 2
               fa-od.Delete-By    = user-init /*bediener.username*/           
               fa-od.Delete-Date  = billdate           
               fa-od.Delete-Time  = TIME.
    END. 
    RELEASE fa-od.
    /*FIND CURRENT fa-od NO-LOCK.*/  

END PROCEDURE.


