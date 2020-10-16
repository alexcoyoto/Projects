package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.example.myapplication.Fragments.BasicButtons;
import com.example.myapplication.Fragments.SpecificButtons;

public class MainActivity extends AppCompatActivity implements
        BasicButtons.OnBasicFragmentInteractionListener {

    private PolishNotation polishNotation;
    Boolean isScientificRequested;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        if(getSupportActionBar()!=null) {
            this.getSupportActionBar().hide();
        }

        EditText editText = findViewById(R.id.edit_text);
        editText.setShowSoftInputOnFocus(false);

        isScientificRequested = false;
        polishNotation = new PolishNotation();
    }


    @Override
    public void onBasicFragmentInteraction(String str) {
        BasicButtons fragment = (BasicButtons) getSupportFragmentManager().findFragmentById(R.id.basicFragment);
        if (fragment != null && fragment.isInLayout()) {
            EditText edit = findViewById(R.id.edit_text);
            switch (str)
            {
                case "=":
                {
                    try {
                        String s = edit.getText().toString();
                        if (polishNotation.isCorrect(s)) {
                            edit.setText(Double.toString(polishNotation.Execute(s)));
                            edit.setSelection(edit.getText().length());
                        }
                    }
                    catch (ArithmeticException ex){
                        Toast.makeText(this, ex.getMessage(), Toast.LENGTH_LONG).show();
                    }
                    break;
                }
                case "\u232b":
                {
                    int pos = edit.getSelectionStart();
                    String s = edit.getText().toString();
                    if (pos >= 1)
                    {
                        s = s.substring(0, pos - 1) + s.substring(pos);
                        edit.setText(s);
                        edit.setSelection(pos - 1);
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
                {
                    int pos = edit.getSelectionStart();
                    String s = edit.getText().toString();
                    s = s.substring(0, pos) + str + s.substring(pos);
                    edit.setText(s);
                    edit.setSelection(pos + str.length());
                    break;
                }
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
