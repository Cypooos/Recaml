# Recaml
This is a simple programming language, based on non-typed lambda calculi.

It support recursive functions, non-normalizing expressions, code block to define temporary variables inside of functions and a folder-type architecture.
By being made in python, the maximal recursion depth is around 30 max.


## Syntax

A program is a tree of variables.
Each variable get calculated from top to bottom.

Two main operation exists :
 - `a b` calculate `a(b)`
 - `\x(expression)` create a function that to x associate an expression

For example, here's the code to the factorial function :
```jl
factorial : \n(
  if (eq n 0) 1 (mul n (factorial (sub n 1)))
)
```
So the variable factorial is a function that to `n`:
 - if `n` is `0`, it asssociate `1`
 - else it associate `n*(factorial n-1)`

A program might look like this :
```jl
GroupA {
  classA {
    fieldA : 45 ;
    fieldB : add fieldA 55 ;
    : 42 ; # Give a value to GroupA.classA directly
  }
  classB {
    should_be_true : eq classA.fieldB 100 ;
  }
}
variable_999 : if GroupA.classB.should_be_true 999 0 ;
variable_49 : GroupA.classA ;
```

An empty key give a value to the whole class (as shown by `variable_49` that fetch `GroupA.classA` defined by an empty key)

Variables can be overwrite

By default, the process print the value of the empty key expression.

## Default functions and types

Default types include :
 - `int` with function `add`, `mul`, `sub`, `div`, `mod` with aliases `+`, `*`, `-`, `/`, `%`
 - `bool` with constants `true` and `false` and functions `and`, `or`, `xor`, `not` with aliases `&&`, `||`, `^^`, `!`

Default functions include :
 - `if a b c` with `a` a bool, `b` the value to resturn if `a` is `true`, and `c` otherwise
 - `eq a b` that returns true if `a` and `b` is the same value
 - `type_eq a b` that returns `true` if `a` and `b` are of the same type

If `a b` failed for the reasons of a not being a function, the interpretor will try to execute `b a`.

That allowed `1 + 2` to be interpreted as `+ a b`
