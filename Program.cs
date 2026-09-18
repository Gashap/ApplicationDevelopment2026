using System;

class Program
{
    static int SumTwoNumbers()
    {
        Console.Write("Введите первое число: ");
        int a = int.Parse(Console.ReadLine());

        Console.Write("Введите второе число: ");
        int b = int.Parse(Console.ReadLine());

        return a + b;
    }

    static void Main()
    {
        int result = SumTwoNumbers();
        Console.WriteLine($"Сумма: {result}");
    }
}
