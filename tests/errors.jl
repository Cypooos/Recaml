Tests.errors {
    wrongType {
        # error_1: or 3 true;
        # error_2: add 3 false;
    }
    trace {
        a : \n(add n 10);
        b : \n(a n);
        c : \n(b n);
        d : \n(c n);
        # error : d true;
    }
    recursive {
        rec : \n(if (eq n 0)
                    (add true 1) 
                    (rec (sub n 1))
                );
        # error : rec 4;
        # stack_overflow : rec -1;
    }
    double_recursive {
        a : \n(b n);
        b : \n(a n);
        # error : a 0;
    }
    syntax {
        # test }
    }
}