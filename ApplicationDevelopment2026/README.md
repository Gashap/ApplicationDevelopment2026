Решение агента:
https://leetcode.com/problems/valid-parentheses/submissions/2179481667

Моё решение:
https://leetcode.com/problems/valid-parentheses/submissions/2179486883

Один проход по строке, поэтому время O(n), а память O(n) в худшем случае. 
Стек нужен потому, что закрывающая скобка всегда относится к последней ещё не закрытой открывающей. 
Последней открыли, первой закрыли: это LIFO.