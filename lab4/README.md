# Задачи
В рамках данной работы нужно научиться формировать псевдошумовые битовые последовательности (коды Голда), изучить их автокорреляционные и взаимокорреляционные свойства. 
1) Написать программу на языке С++ для генерации последовательности Голда, используя схему, изображенную на рисунке 4.5 и порождающие полиномы x и y, при этом x – это ваш порядковый номер в журнале в двоичном формате (5 бит), а y – это x+7 (5 бит). Например, ваш номер 22, значит:
x = 1 0 1 1 0,
y = 1 1 1 0 1.

 ![image](https://github.com/user-attachments/assets/c1695e5b-94f9-4486-876d-66323409ddcc)

2) Вывести получившуюся последовательность на экран.
3) Сделать поэлементный циклический сдвиг последовательности и посчитать автокорреляцию исходной последовательности и сдвинутой. Сформировать таблицу с битовыми значениями последовательностей, в последнем столбце которой будет вычисленное значение автокорреляции, как показано в примере ниже.
 
 ![image](https://github.com/user-attachments/assets/d3b96ab7-7933-4687-af69-25f8e783ca0a)

4) Сформировать еще одну последовательность Голда, используя свою схему (рис. 4.5), такую что x=x+1, а y= у-5.
5) Вычислить значение взаимной корреляции исходной и новой последовательностей и выведите в терминал.
6) Проделать шаги 1-5 в Matlab. Использовать функции xcorr() и autocorr() для вычисления соответствующих корреляций. Сравнить результаты, полученные в Matlab и C/C++.
7) Вывести на график в Matlab функцию автокорреляции в зависимости от величины задержки (lag).

## Этапы выполнения работы
Последовательность Голда:

![image](https://github.com/user-attachments/assets/2ec31eca-c51f-452c-92d8-ec97dad787ba)

Сформировать таблицу с битовыми значениями последовательностей, в последнем столбце которой будет вычисленное значение автокорреляции:

![image](https://github.com/user-attachments/assets/8c48ddd2-e6e3-47f9-8c37-17a9623a7d6b)

Сформировать еще одну последовательность Голда, используя свою схему (рис. 4.5), такую что x=x+1, а y= у-5.

![image](https://github.com/user-attachments/assets/4ca442ae-3707-44a6-934b-0bbb07fefd69)

Вычислить значение взаимной корреляции исходной и новой последовательностей и выведите в терминал.

![image](https://github.com/user-attachments/assets/8cc12a7d-44bf-4767-93d7-c607cc7096be)

Вывести на график в Matlab функцию автокорреляции в зависимости от величины задержки (lag):

![image](https://github.com/user-attachments/assets/07569996-eb7a-44d2-ab38-1c7d66aea1b1)
