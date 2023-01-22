Tests.Inter.Blocks {

  simple {
    test_fct : \x{
      a:add x 1;
      b:mul a 2;
      : add b 4440;
    };
    test_fct_4444 : test_fct 1;
    test_codeblock : \a(add {x : mul a 2; : add x x;} a);
    test_codeblock_25 : test_codeblock 5;
    test_codeblock_60 : test_codeblock 12;
  }

  
  fibo {
    fct : \n(
        if (or (eq n 0) (eq n 1)) 1 # if n=0 or n=1, return 1
        { # otherwise
            rec : fct (sub n 1) ;
            rec2 : fct (sub n 2) ;
            : add rec rec2 ;
        }
    );
    test_0: fct 0;
    test_1: fct 1;
    test_2: fct 2;
    test_3: fct 3;
    test_4: fct 4;
    test_5: fct 5;
    test_6: fct 6;
  }

  fast_pow {
    fct : \a(\b(
      if (eq b 0) 1 (
        if (eq (% b 2) 0)
          {rec : fct a (div b 2); : mul rec rec; }
          {rec : fct a (div (sub b 1) 2); : mul (mul rec rec) a; }
      )
    ));
    test_23 : fct 2 3; # result is 8
    test_24 : fct 2 4; # result is 16
    test_34 : fct 3 4; # result is 81
  }
}