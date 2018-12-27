The algorithm of converting is taken from the paper:
* M. Kanazawa: A Generalization of Linear Indexed Grammars Equivalent to Simple Context-Free Tree Grammars. FG 2014 Proceedings of the 19th International Conference on Formal Grammar - Volume 8612, 86-103 (2014)

https://link.springer.com/chapter/10.1007/978-3-662-44121-3_6

Usage: `python cftg2iwg.py <path to the rules file>`
For example: `python cftg2iwg.py test.rules`

```
1. S -> A(a)
2. A -> A(g(C,x1))
3. A -> B(x1)
4. C -> a
5. B -> x1
6. B -> B(f(a,x1,x1))
Transformed:
1. S[] -> (1,e)[]
2. (1,1)[] -> a
3. (1,e)[] -> (2,e)[(1,e)]
4. (2,1.2)[(1,e)] -> (1,1)[]
5. (1,e)[] -> (3,e)[(1,e)]
6. (3,1)[(1,e)] -> (1,1)[]
7. (2,1.1)[] -> (4,e)[(2,1.1)]
8. (2,1)[] -> (2,1.1)[](2,1.2)[]
9. (2,e)[] -> (2,e)[(2,e)]
10. (2,1.2)[(2,e)] -> (2,1)[]
11. (2,e)[] -> (3,e)[(2,e)]
12. (3,1)[(2,e)] -> (2,1)[]
13. (3,e)[] -> (5,e)[(3,e)]
14. (5,e)[(3,e)] -> (3,1)[]
15. (3,e)[] -> (6,e)[(3,e)]
16. (6,1.2)[(3,e)] -> (3,1)[]
17. (6,1.3)[(3,e)] -> (3,1)[]
18. (4,e)[] -> a
19. (6,1.1)[] -> a
20. (6,1)[] -> (6,1.1)[](6,1.2)[](6,1.3)[]
21. (6,e)[] -> (5,e)[(6,e)]
22. (5,e)[(6,e)] -> (6,1)[]
23. (6,e)[] -> (6,e)[(6,e)]
24. (6,1.2)[(6,e)] -> (6,1)[]
25. (6,1.3)[(6,e)] -> (6,1)[]
```