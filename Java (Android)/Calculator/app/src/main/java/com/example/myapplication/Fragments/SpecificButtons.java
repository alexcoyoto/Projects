package com.example.myapplication.Fragments;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.fragment.app.Fragment;

import com.example.myapplication.R;

public class SpecificButtons extends Fragment implements View.OnClickListener{

    public static final String TAG = "specificTAG";

    private final int[] buttonId = {
            R.id.buttonSin,
            R.id.buttonCos,
            R.id.buttonTan,
            R.id.buttonLog,
            R.id.buttonLn,
            R.id.buttonE,
            R.id.buttonG,
            R.id.buttonPI,
            R.id.buttonSqrt,
            R.id.buttonAbs,
            R.id.buttonPower,
            R.id.buttonFactorial
    };

    private OnFragmentInteractionListener mListener;

    public interface OnFragmentInteractionListener {
        void onFragmentInteraction(String str);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.specific_buttons, container, false);

        for (int id: buttonId){
            view.findViewById(id).setOnClickListener(this);
        }

        return view;
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (context instanceof OnFragmentInteractionListener) {
            mListener = (OnFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    public void onClick(final View view)
    {
        if (mListener != null) {
            mListener.onFragmentInteraction(((Button)view).getText().toString());
        }
    }
}
