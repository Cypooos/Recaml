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
  res: add a.a. 3; # this a is Parser.Weird1.a.a. = 30
}