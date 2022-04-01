# Convexity I - Sets and functions

## why convexity?

Simply put: because we can broadly **understand and solve** convex optimization problems

Nonconvex problems are mostly treated on a case by case basis

Reminder: a convex optimization problem is of the form

$$
\begin{array}{ll}
\min\_{x \in D} & f(x) \
\text { subject to } & g\_{i}(x) \leq 0, i=1, \ldots, m \
& h\_{j}(x)=0, j=1, \ldots, r
\end{array}
$$

where $f$ and $g\_i, i = 1,..., m$ are all *convex*, and $h\_j, j = 1,..., r$ are *affine*. Special property: **any local minimizer is a global minimizer**

## Convex sets

Convex set: $C \subseteq \mathbb{R}^{n}$ such that:

$$
x, y \in C \Longrightarrow t x+(1-t) y \in C \text { for all } 0 \leq t \leq 1
$$

In words, line segment joining any two elements lies entirely in set