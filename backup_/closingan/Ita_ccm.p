session:data-entry-return = true.
define variable from-date as date initial 01/01/18.
define variable to-date as date initial 01/31/18.
define button btn-go   label "    &OK        ".
define button btn-cancel label "  &CANCEL  ".
define variable answer as logical.

/*****************************  DEFINE FRAMES ********************************/
  DEFINE FRAME frame3
    "    INSERT ACCOUNTING PERIOD    "
      bgcolor 2 fgcolor 15 at row 2 column 2.3
    from-date at row 3.5 column 2 label "From Date"
    to-date at row 4.5 column 4.4 label "To Date"
    btn-go at row 6 column 6
    btn-cancel skip(0.5)
    WITH SIDE-LABELS centered overlay WIDTH 36 THREE-D
    view-as dialog-box title "Cancel Close Month".

/**************************  DEFINE TRIGGERS **********************************/

  on choose of btn-go
  do:
    assign from-date to-date.
    hide message no-pause.
    message "Do you really want to cancel close month?" view-as alert-box 
       question buttons yes-no update answer.
    if answer then 
    do:
        FOR EACH gl-jouhdr WHERE datum GE from-date AND datum LE to-date:
            UPDATE gl-jouhdr.activeflag = 0 gl-jouhdr.BATCH = NO.
            FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr :
                gl-journal.activeflag = 0.
            END.
        END.
        FOR EACH gl-jouhdr WHERE datum GE from-date AND datum LE to-date AND jtype = 0:
            UPDATE gl-jouhdr.BATCH = NO.
        END.
        FOR EACH gl-acct:
            FIND FIRST htparam WHERE paramnr = 597. /* Current Closing Period */
            htparam.fdate = to-date.
            FIND FIRST htparam WHERE paramnr = 558. /* Last Closing Period */
            htparam.fdate = from-date - 1.
        END.
    END.
  end.

  on end-error of current-window or window-close of current-window anywhere
  do:
    apply "choose" to btn-cancel in frame frame3.
  end.

/**************************  MAIN LOGIC ***************************************/

  view frame frame3.
  disp from-date to-date with frame frame3.
  enable all WITH FRAME frame3.
  APPLY "entry" TO btn-go.
  ASSIGN from-date:READ-ONLY IN FRAME frame3 = YES.
      to-date:READ-ONLY IN FRAME frame3 = YES.

  status input "".
  WAIT-FOR CHOOSE OF btn-go, btn-cancel.



