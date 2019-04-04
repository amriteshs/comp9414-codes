/*
    COMP9414 Assignment-1
    Name: Amritesh Singh
    zID: z5211987
*/

% Q1.) sumsq_even(Numbers, Sum) sums the squares of only the even numbers in a list of integers.

sumsq_even(Numbers, Sum) :-
    Numbers = [],
    Sum = 0.

sumsq_even(Numbers, Sum) :-
    Numbers = [H | T],
    0 is H mod 2,
    sumsq_even(T, X),
    Sum is X + H * H.

sumsq_even(Numbers, Sum) :-
    Numbers = [H | T],
    1 is H mod 2,
    sumsq_even(T, X),
    Sum = X.

% Q2.) same_name(Person1,Person2) returns true if Person1 and Person2 have the same family name.

same_name(Person1, Person2) :-
    Person1 == Person2.

same_name(Person1, Person2) :-
    ancestor_male(Person1, Person2).

same_name(Person1, Person2) :-
    ancestor_male(Person2, Person1).

same_name(Person1, Person2) :-
    ancestor_male(X, Person1),
    ancestor_male(X, Person2).

ancestor_male(X, Y) :-
    parent(X, Y),
    male(X).

ancestor_male(X, Y) :-
    parent(Z, Y),
    male(Z),
    ancestor_male(X, Z).


% Q3.) sqrt_list(NumberList, ResultList) binds "ResultList" to the list of pairs consisting of a number and its square root, for each number in "NumberList".

sqrt_list(NumberList, ResultList) :-
    NumberList = [],
    ResultList = [].

sqrt_list(NumberList, ResultList) :-
    NumberList = [H | T],
    ResultList = [X | Y],
    H >= 0,
    Z is sqrt(H),
    X = [H, Z],
    sqrt_list(T, Y).

sqrt_list(NumberList, ResultList) :-
    NumberList = [H | T],
    ResultList = [X | Y],
    H < 0,
    X = [H, 'undefined'],
    sqrt_list(T, Y).

% Q4.) sign_runs(List, RunList) converts a list of numbers into the corresponding list of sign runs (a maximal sequence of consecutive negative or non-negative numbers).

sign_runs(List, RunList) :-
    List = [],
    RunList = [].

sign_runs(List, RunList) :-
    List = [H | _],
    RunList = [X | Y],
    H >= 0,
    subseqP(List, Z, R),
    sign_runs(R, Zs),
    X = Z,
    Y = Zs.

sign_runs(List, RunList) :-
    List = [H | _],
    RunList = [X | Y],
    H < 0,
    subseqN(List, Z, R),
    sign_runs(R, Zs),
    X = Z,
    Y = Zs.

subseqP([], [], []).

subseqP([H | T], Z, R) :-
    H >= 0,
    subseqP(T, Res, R),
    Z = [H | Res].

subseqP([H | T], [], [H | T]) :-
    H < 0.

subseqN([], [], []).

subseqN([H | T], Z, R) :-
    H < 0,
    subseqN(T, Res, R),
    Z = [H | Res].

subseqN([H | T], [], [H | T]) :-
    H >= 0.

% Q5.) is_heap(Tree) returns true if "Tree" satisfies heap property (i.e., for every non-leaf node in tree, the number stored at that node is less than or equal to the number stored at each of its children).

is_heap(empty).

is_heap(tree(L, Num, R)) :-
    L = empty,
    Num = _,
    R = empty.

is_heap(tree(L, Num, R)) :-
    L = tree(_, X, _),
    R = empty,
    X >= Num,
    is_heap(L).

is_heap(tree(L, Num, R)) :-
    L = empty,
    R = tree(_, Y, _),
    Y >= Num,
    is_heap(R).

is_heap(tree(L, Num, R)):-
    L = tree(_, X, _),
    R = tree(_, Y, _),
    X >= Num,
    Y >= Num,
    is_heap(L),
    is_heap(R).
