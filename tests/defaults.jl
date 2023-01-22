Tests.Defaults {
    Int {
        test1 : add 25 75;
        test2 : sub 125 25;
        test3 : mul 25 4;
        test4 : div 6000 60;
        test5 : mod 69100 500;
    }
    Bool {
        test1 : true;
        test2 : false;
        test3 : not true;
        test4 : or false true;
        test5 : and true true;
        test6 : and false false;
        test7 : xor false true;
        test8 : xor true true;
    }
}