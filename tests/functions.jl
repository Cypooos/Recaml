
Test.Inter.Functions {

  # test for multiple arguments functions
  multiple_arg {
    multiple: \a(\b(\c(add a (add b c))));
    multiple_test: multiple 1 20 300;
    multiple_test2_:multiple 1 20;
    multiple_test2:multiple_test2_ 300;
    multiple_test3_:multiple 1;
    multiple_test3:multiple_test3_ 20 300;

    argument_order:\a(\b(\a(\b(add a b)))) 99 99 1 10;
    argument_order2:\a(\b(\a(\b(add a b))));
    argument_order2_test:\z(\y(\x(\x(argument_order2 x x y z)))) 10 1 -1000 99;; 
  }

  # the constant function
  constant {
    cste:\a(\x(a));
    result:add (cste 2 3) (cste 10 add);
  }

  # The factorial function
  recursive.factorial {
    fct: \a(if (eq a 0) (1) (mul a (fct (sub a 1))));
    test_1: fct 1;
    test_2: fct 2;
    test_3: fct 3;
    test_4: fct 4;
    test_5: fct 5;
    # 6 is over the (raisable) 30 recursion limit. So 6 recursion in Recaml correspond to around 30 python recursion, so
    #      real recursion is around 5*program_rec 
    # python limit is around 300, so the Recaml maximum is around 60
  }

  # fibonachi
  recursive.fibo {
    fct: \n(if (or (eq n 0) (eq n 1)) 1 (add (fct (sub n 1)) (fct (sub n 2))));
    test_0: fct 0;
    test_1: fct 1;
    test_2: fct 2;
    test_3: fct 3;
    test_4: fct 4;
    test_5: fct 5;
    test_6: fct 6;
    # test_7: fct 7; (above the recursion limit)
  }

  # the naive version of the pow function
  recursive.pow {
    fct : \a(\b(if (eq b 0) 1 (mul a (fct a (sub b 1)))));
    test_23 : fct 2 3; # result is 8
    test_24 : fct 2 4; # result is 16
    test_34 : fct 3 4; # result is 81
  }

  # the fast divide and rule version
  recursive.fast_pow {
    fct : \a(\b(
        if (eq b 0) 1 (
          if (eq (% b 2) 0)
            (mul (fct a (div b 2)) (fct a (div b 2)))
            (mul a (mul (fct a (div (sub b 1) 2)) (fct a (div (sub b 1) 2)))
          )
        )));
    test_23 : fct 2 3; # result is 8
    test_24 : fct 2 4; # result is 16
    test_34 : fct 3 4; # result is 81
  }
}