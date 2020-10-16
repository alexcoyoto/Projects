package com.example.myapplication.Fragments;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.example.myapplication.R;

public class BasicButtons extends Fragment implements View.OnClickListener {

    public static final String TAG = "basicTAG";

    private int[] buttonIds = {
            R.id.button0,
            R.id.button1,
            R.id.button2,
            R.id.button3,
            R.id.button4,
            R.id.button5,
            R.id.button6,
            R.id.button7,
            R.id.button8,
            R.id.button9,
            R.id.buttonDot,
            R.id.rightBracket,
            R.id.leftBracket,
            R.id.buttonClear,
            R.id.buttonPlus,
            R.id.buttonSub,
            R.id.buttonMultiply,
            R.id.buttonDivide,
            R.id.buttonEqual,
            R.id.buttonBack
    };

    public interface OnBasicFragmentInteractionListener {
        void onBasicFragmentInteraction(String str);
    }

    private OnBasicFragmentInteractionListener mListener;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.basic_buttons, container, false);

        for (int id: buttonIds){
            view.findViewById(id).setOnClickListener(this);
        }

        return view;
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (context instanceof BasicButtons.OnBasicFragmentInteractionListener) {
            mListener = (OnBasicFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement onBasicFragmentInteraction");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    public void onClick(final View view) {
        Button button = (Button) view;

        if (mListener != null) {
            mListener.onBasicFragmentInteraction(button.getText().toString());
        }
    }
}
