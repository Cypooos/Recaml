Tests.Parser.Simple {
  a:30;
  b:45;
  c:+ a b; # Calculate 30 + 45 = 75
}

Tests.Parser.Scope1 {
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
    result:+ (+ (+ a b) c) d; # = 1234
  }
  Tree.in.inner {
    result2:+ (+ (+ a b) c) d; # = 1234
  }
}

Tests.Parser.Scope2 {
  a {
    a {
      b:10;
      :30;
    }
    b:20;
  }
  a {
    res20 : add b 2; # this b is Parser.Weird1.a.b = 20, so the result is 22
  }
  a.a {
    res10 : add b 1; # this b is Parser.Weird1.a.b = 10, so the result is 11
  }
  res: add a.a 3; # this a is Parser.Weird1.a.a. = 30
}

Tests.Parser.LastKey { # The last key doesn't need a ';'
  test1 {
    a:10;
    b:20
  }
  test2:30
}


Tests.Parser.EmptyKey { # Setting the empty key `:value` will give a value to the category
  test1 {
    a : 1000;
    : add a 111 
  }
  : test1
}

tests.Parser.EmptyExpression { # for randomly placed ";"
  ;test1 {
    ;; ;   ; a : 10;  ;    
    ;

    ;
  };;
}