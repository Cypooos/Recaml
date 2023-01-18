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
    }
    weird {
      cste:\a(\x(a));
      result:add (cste 2 3) (cste 10 add);
    }
    recursive {
      fact: \a(if (eq a 0) (1) (mul a (fact (sub a 1))));
      fact_2: fact 3;
    }
  }
}