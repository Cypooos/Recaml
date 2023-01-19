Tests {
  simple {
    a:30;
    b:45;
    c:+ a b;
  }

  Parser.Simple1 {
    Tree {
      in.inner {
        a:4;
        b:30;
      }
      in {
        c:200;
      }
      d:1000;
    }
    Tree.in.inner {
      result:+ (+ (+ a b) c) d;
    }
    Tree.in.inner {
      result2:+ (+ (+ a b) c) d;
    }
  }

  Parser.Weird1 {
    a {
      a {
        b:10;
        :30;
      }
      b:20;
    }
    a {
      res20 : add b 2;
    }
    a.a {
      res10 : add b 1;
    }
    res: add a.a. 3;
  }
  Inter.Functions {

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
    weird {
      cste:\a(\x(a));
      result:add (cste 2 3) (cste 10 add);
    }
    recursive.factorial {
      fact: \a(if (eq a 0) (1) (mul a (fact (sub a 1))));
      fact_1: fact 1;
      fact_2: fact 2;
      fact_3: fact 3;
      fact_4: fact 4;
      fact_5: fact 5;
      # 6 is over the (raisable) 30 recursion limit. So 6 correspond to around 30, so
      #      real recursion is around 5*program_rec 
      # python limit is around 300
    }
    recursive.fibo {
      fibo: \n(if (or (eq n 0) (eq n 1)) 1 (add (fibo (sub n 1)) (fibo (sub n 2))));
      fibo_0: fibo 0;
      fibo_1: fibo 1;
      fibo_2: fibo 2;
      fibo_3: fibo 3;
      fibo_4: fibo 4;
      fibo_5: fibo 5;
      fibo_6: fibo 6;
      # fibo_7: fibo 7; (above the recursion limit)
    }
    recursive.pow {
      pow : \a(\b(if (eq b 0) 1 (mul a (pow a (sub b 1)))));
      pow_23 : pow 2 3;
      pow_24 : pow 2 4;
      pow_34 : pow 3 4;
      fast_pow : \a(\b(
          if (eq b 0) 1 (
            if (eq (% b 2) 0)
              (mul (fast_pow a (div b 2)) (fast_pow a (div b 2)))
              (mul a (mul (fast_pow a (div (sub b 1) 2)) (fast_pow a (div (sub b 1) 2)))
            )
          )));
      fast_pow_23 : fast_pow 2 3;
      fast_pow_24 : fast_pow 2 4;
      fast_pow_34 : fast_pow 3 4;
    }
  }
  Inter.context {
    simple {
      test1 : \x{
        a:add x 1;
        b:mul x 2;
        : add x 4440
      };
      test_4444 : test1 1;
    }
  }
}