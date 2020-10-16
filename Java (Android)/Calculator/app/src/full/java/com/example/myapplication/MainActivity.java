package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.example.myapplication.Fragments.BasicButtons;
import com.example.myapplication.Fragments.SpecificButtons;

import java.text.DecimalFormat;

public class MainActivity extends AppCompatActivity implements
        SpecificButtons.OnFragmentInteractionListener,
        BasicButtons.OnBasicFragmentInteractionListener
{

    private PolishNotation polishNotation;
    Boolean isScientificRequested;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if(getSupportActionBar()!=null) {
            this.getSupportActionBar().hide();
        }

        EditText editText = findViewById(R.id.edit_text);
        editText.setShowSoftInputOnFocus(false); // каб нельга было нічога пiсаць

        isScientificRequested = false;
        polishNotation = new PolishNotation();
    }

    public void switchMode(View view)
    {
        View frag = (View) findViewById(R.id.basicFragment);
        FrameLayout frameLayout = findViewById(R.id.placeholder);
        if (isScientificRequested)
        {
            isScientificRequested = false;

            frag.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.MATCH_PARENT, 1));
            frameLayout.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.MATCH_PARENT, 0));
        }
        else
        {
            isScientificRequested = true;
            SpecificButtons fragment = new SpecificButtons();

            frag.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.MATCH_PARENT, 0));
            frameLayout.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.MATCH_PARENT, 1));

            FragmentManager manager = getSupportFragmentManager();
            FragmentTransaction transaction = manager.beginTransaction();
            transaction.add(R.id.placeholder, fragment, SpecificButtons.TAG).commit();
        }
    }

    @Override
    public void onFragmentInteraction(String str) {
        EditText edit = findViewById(R.id.edit_text);
        switch (str)
        {
            case "!":
            case "e":
            case "^":
            case "g":
            case "\u03c0": // лiк Пi
            {
                int pos = edit.getSelectionStart();
                String s = edit.getText().toString();
                if (str.equals("e"))
                    str = "2.71828";
                if (str.equals("g"))
                    str = "9.81";
                if (str.equals("\u03c0"))
                    str = "3.14159";
                s = s.substring(0, pos) + str + s.substring(pos);
                edit.setText(s);
                edit.setSelection(pos + str.length()); // пераводзiм курсор у канец
                break;
            }
            case "|x|":
            {
                int pos = edit.getSelectionStart();
                String s = edit.getText().toString();
                s = s.substring(0, pos) + "abs()" + s.substring(pos);
                edit.setText(s);
                edit.setSelection(pos + 4);
                break;
            }
            case "\u221a": // квадратны корань
            {
                int pos = edit.getSelectionStart();
                String s = edit.getText().toString();
                s = s.substring(0, pos) + "sqrt()" + s.substring(pos);
                edit.setText(s);
                edit.setSelection(pos + 5);
                break;
            }

            /*
            case "\u232b": // "Назад"
            {
                int pos = edit.getSelectionStart();
                String s = edit.getText().toString();
                if (pos >= 1)
                {
                    s = s.substring(0, pos - 1) + s.substring(pos);
                    edit.setText(s);
                    edit.setSelection(pos - 1);
                }
                // Toast.makeText(this, "aaa", Toast.LENGTH_LONG).show();

                break;
            }
            case "AC":
            {
                edit.setText("");
               // Toast.makeText(this, "bbb", Toast.LENGTH_LONG).show();
                break;
            }

             */

            default: // sin cos, tan, log, ln,
            {
                int pos = edit.getSelectionStart();
                String s = edit.getText().toString();
                s = s.substring(0, pos) + str + "()" + s.substring(pos);
                edit.setText(s);
                edit.setSelection(pos + str.length() + 1);
            }
        }
    }

    @Override
    public void onBasicFragmentInteraction(String str) {
        BasicButtons fragment = (BasicButtons) getSupportFragmentManager().findFragmentById(R.id.basicFragment); // getSupportFragmentManager для кіравання  фрагментамі праз FragmentManager
        if (fragment != null && fragment.isInLayout()) {
            EditText edit = findViewById(R.id.edit_text);
            switch (str)
            {
                case "=":
                {
                    String s = edit.getText().toString();
                    try{
                        if (polishNotation.isCorrect(s))
                        {
                            double result = polishNotation.Execute(s);
                            long ch = (long)result;
                            boolean check = Math.abs(result) - Math.abs(ch) == 0; // цi цэлы лiк ?
                            if (polishNotation.isCorrect(s)) {
                                if (check) {

                                    // DecimalFormat df = new DecimalFormat("#########.##########");

                                    // edit.setText(String.format("%d", ch));
                                    edit.setText(Long.toString(ch));
                                } else {
                                    //edit.setText(String.format("%.8f", result));
                                    edit.setText(Double.toString(result));
                                }
                                edit.setSelection(edit.getText().length());
                            }
                        }
                    }
                    catch (ArithmeticException ex){
                        Toast.makeText(this, ex.getMessage(), Toast.LENGTH_LONG).show();
                    }
                    break;
                }
                case "\u232b": // "Назад"
                {
                    // Toast.makeText(this, "Працуе!", Toast.LENGTH_LONG).show();

                    int pos = edit.getSelectionStart();
                    String s = edit.getText().toString();
                    if (pos >= 1) {
                        char temp = s.charAt(pos - 1);
                        if ((temp >= '0' && temp <= '9') || temp == '(' || temp == ')' ) {
                            s = s.substring(0, pos - 1) + s.substring(pos);
                            edit.setText(s);
                            edit.setSelection(pos - 1);
                        } else {
                            boolean start = false;
                            while (pos != 0) {
                                temp = s.charAt(pos - 1);
                                if ((temp >= '0' && temp <= '9') || temp == '(' || temp == ')') {
                                    if (start)
                                        break;
                                } else {
                                    start = true;
                                }
                                s = s.substring(0, pos - 1) + s.substring(pos);
                                edit.setText(s);
                                edit.setSelection(pos - 1);
                                pos--;
                            }
                        }
                    }
                    break;
                }
                case "AC":
                {
                    edit.setText("");
                    break;
                }
                case "(":
                case ")":
                default:
                {
                    int pos = edit.getSelectionStart();
                    String s = edit.getText().toString();
                    s = s.substring(0, pos) + str + s.substring(pos);
                    edit.setText(s);
                    edit.setSelection(pos + str.length());
                }
            }
        }
    }

}

