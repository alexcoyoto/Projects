package com.example.myapplication;

import android.content.Context;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PolishNotation
{
    private String[] operators = {"sin", "cos", "sqrt", "ln", "log", "tan", "abs"};

    private int getPriority(String operand) {
        switch (operand) {
            case "+":
            case "-": {
                return 2;
            }
            case "*":
            case "/": {
                return 3;
            }
            case "%":
            case "^":
            case "sin":
            case "cos":
            case "tan":
            case "ln":
            case "sqrt":
            case "log":
            case "abs":
            case "m":{
                return 4;
            }
            case "(":
            case ")":{
                return 1;
            }
            case "!": {
                return 0;
            }
            default: {
                try {
                    throw new Exception("Нявыкананая аперацыя");
                } catch (Exception e) { }
                return 0;
            }
        }

    }

    private String replace(String s) // скарочаннае множанне і адмоўныя лікі
    {
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '-') {
                if (i == 0 || s.charAt(i - 1) == '(')
                    s = s.substring(0, i) + 'm' + s.substring(i + 1);
            }
        }
        for (int i = 1; i < s.length(); i++)
        {
            if ((Character.isDigit(s.charAt(i - 1)) && s.charAt(i) == '(') ||
                    (s.charAt(i - 1) == ')' && Character.isDigit(s.charAt(i))) ||
                    (s.charAt(i - 1) == ')' && s.charAt(i) == '('))
            {
                s = s.substring(0, i) + '*' + s.substring(i);
            }
        }

        return s;
    }


    public Queue<String> parseToQueue(String str) {
        Queue<String> queue = new LinkedList<>();
        Pattern double_pattern = Pattern.compile("^\\d+(\\.\\d+)?");
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == '+' || str.charAt(i) == '-' || str.charAt(i) == '*' || str.charAt(i) == '/' || str.charAt(i) == '!' || str.charAt(i) == '(' || str.charAt(i) == ')' || str.charAt(i) == '^' || str.charAt(i) == 'm') {
                queue.add("" + str.charAt(i));
            }
            else if (str.charAt(i) == 'e')
                queue.add(Double.toString(Math.E));
            else if (str.charAt(i) == '\u03c0')
                queue.add(Double.toString(Math.PI));
            else if (str.charAt(i) == 'g')
                queue.add(Double.toString(9.8));

            else if (Character.isDigit(str.charAt(i))) {
                String s = str.substring(i);
                Matcher matcher = double_pattern.matcher(s); // для інтэрпрэтацыі шаблону Pattern
                if (matcher.find()) {
                    queue.add(matcher.group());
                    i = i + matcher.group().length() - 1;
                }
            }
            else {
                String s = str.substring(i);
                for (String op : operators) {
                    Pattern pattern = Pattern.compile("^" + op);
                    Matcher matcher = pattern.matcher((s));
                    if (matcher.find()) {
                        queue.add(matcher.group());
                        i = i + matcher.group().length() - 1;
                        break;
                    }
                }
            }
        }
        return queue;
    }

    public Queue<String> toReverseNotation(Queue<String> inf) {
        Pattern num_pattern = Pattern.compile("^\\d+(\\.\\d+)?");
        Queue<String> reverse = new LinkedList<>();
        Stack<String> operators = new Stack<>();
        String next = inf.remove();
        while (inf.size() >= 0) {
            if (num_pattern.matcher(next).matches())
                reverse.add(next);
            else if (next.equals("!"))
                reverse.add(next);
            else if (next.equals("sin") || next.equals("cos") || next.equals("sqrt") || next.equals("tan") || next.equals("ln") || next.equals("log") || next.equals("abs") || next.equals("m"))
                operators.push(next);
            else if (next.equals("("))
            {
                operators.push(next);
            }
            else if (next.equals(")")) {
                String top = operators.pop();
                while (!top.equals("(")) {
                    reverse.add(top);
                    top = operators.pop();
                }
            }
            else {
                while (operators.size() > 0 && getPriority(operators.peek()) >= getPriority(next)) // рeek() вяртае аб'ект з вяршыні стэка без яго выдалення
                    reverse.add(operators.pop());
                operators.push(next);

            }

            if (inf.size() > 0) {
                next = inf.remove();
            } else {
                while (operators.size() > 0)
                    reverse.add(operators.pop());
                break;
            }
        }
        return reverse;
    }

    public double getResult(Queue<String> queue) throws ArithmeticException
    {
        Stack<Double> stack = new Stack<>();
        String next = queue.remove();
        double temp = 0;
        while(queue.size() >= 0)
        {
            switch (next)
            {
                case "+":
                {
                    double a = stack.pop(), b = stack.pop();
                    temp = a + b;
                    stack.push(temp);
                    break;
                }
                case "-":
                {
                    double a = stack.pop(), b = stack.pop();
                    temp = b - a;
                    stack.push(temp);
                    break;
                }
                case "*":
                {
                    double a = stack.pop(), b = stack.pop();
                    temp = a * b;
                    stack.push(temp);
                    break;
                }
                case "^":
                {
                    double a = stack.pop(), b = stack.pop();
                    temp = Math.pow(b, a);
                    stack.push(temp);
                    break;
                }
                case "/":
                {
                    double a = stack.pop(), b = stack.pop();
                       if (b/a == Double.POSITIVE_INFINITY)
                            throw new ArithmeticException("На нуль дзяліць нельга!");
                        temp = b / a;
                    stack.push(temp);
                    break;
                }
                case "!":
                {
                    long a = (long)(stack.pop()).doubleValue();
                        if (a < 0)
                            throw new ArithmeticException("Фактарыял адмоўнага ліку!");
                    if (a >= 16)
                        a++;
                    else
                    {
                        long t = 1;
                        for (int i = 1; i <= a; i++)
                            t *= i;
                        stack.push((double)t);
                    }
                    break;
                }
                case "sin":
                {
                    double a = stack.pop();
                    temp = Math.sin(a);
                    stack.push(temp);
                    break;
                }
                case "cos":
                {
                    double a = stack.pop();
                    temp = Math.cos(a);
                    stack.push(temp);
                    break;
                }
                case "tan": {
                    double a = stack.pop();
                    temp = Math.tan(a);
                    stack.push(temp);
                    break;
                }
                case "sqrt":
                {
                    double a = stack.pop();
                        if (a < 0)
                            throw new ArithmeticException("Квадратны корань з адмоўнага ліку!");

                    temp = Math.sqrt(a);
                    stack.push(temp);
                    break;
                }
                case "ln":
                {
                    double a = stack.pop();
                        if (a <= 0)
                            throw new ArithmeticException("Абсяг вызнаэння лагарыфму: х > 0!");
                    temp = Math.log(a);
                    stack.push(temp);
                    break;
                }
                case "log":
                {
                    double a  = stack.pop();
                        if (a <= 0)
                            throw new ArithmeticException("Абсяг вызнаэння лагарыфму: х>0");
                    temp = Math.log10(a);
                    stack.push(temp);
                    break;
                }
                case "abs":
                {
                    double a  = stack.pop();
                    temp = Math.abs(a);
                    stack.push(temp);
                    break;
                }
                case "m":
                {
                    stack.push(-stack.pop());
                    break;
                }
                default:
                {
                    stack.push(Double.parseDouble(next));
                    break;
                }
            }
            if (queue.size() == 0)
                return stack.pop();
            else
                next = queue.remove();
        }
        if (stack.size() > 0)
                throw new ArithmeticException("Аператары і аперанды не супадаюць");
        return temp;
    }

    public double Execute(String str) throws ArithmeticException
    {
        double res = 0;
        res = getResult(toReverseNotation(parseToQueue(replace(str))));
        return res;
    }


    public Boolean isCorrect (String s)
    {
        int im = s.length() - 1;
        if (s.charAt(im) == '+' || s.charAt(im) == '-' || s.charAt(im) == '*' || s.charAt(im) == '/' || s.charAt(im) == '(' || s.charAt(im) == '^' )
            throw new ArithmeticException("Аператары і аперанды не супадаюць!");

        for (int i = 0; i < s.length(); i++)
        {
            if (s.charAt(i) == '(' && s.charAt(i+1) == ')') {
                throw new ArithmeticException("Пустыя '()'");
            }
        }

        int cnt = 0;
        for (int i = 0; i < s.length(); i++)
        {
            if (cnt < 0)
            {
                throw new ArithmeticException("')' перад '('");
            }
            if (s.charAt(i) == ')')
                cnt--;
            if (s.charAt(i) == '(')
                cnt++;
        }
        if (cnt != 0)
        {
            throw new ArithmeticException("Розная колькасць '(' і ')'");
            //throw new ArithmeticException(Integer.toString(cnt));
        }
        for (int i = 0; i < s.length(); i++)
        {
            if (Character.isDigit(s.charAt(i)) || s.charAt(i) == '.')
            {
                if (s.charAt(i) == '.')
                    cnt++;
            }
            else
            {
                cnt = 0;
            }
            if (cnt > 1) {
                throw new ArithmeticException("Праверце напісанне няцэлых лікаў!");
            }
        }

        for (int i = 1; i < s.length(); i++)
        {
            if (isOperation(s.charAt(i - 1)) && isOperation(s.charAt(i)))
            {
                throw new ArithmeticException("Дзве аперацыі запар!");
            }
        }

        return true;
    }

    private Boolean isOperation(char ch)
    {
        return ch == '^' || ch == '/' || ch == '*' || ch == '-' || ch == '+' || ch == '!';
    }
}