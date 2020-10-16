package com.example.myrssreader;

import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.widget.Toast;


public class ConnectionReceiver extends BroadcastReceiver {

    Boolean isFirstTime = true;

    @SuppressLint("UnsafeProtectedBroadcastReceiver")
    @Override
    public void onReceive(final Context context, final Intent intent)
    {
        String status = connectivityMode(context);
        if (!(isFirstTime && (status.equals("Злучэнне адноўлена") || status.equals("Далучана да Wifi"))))
            Toast.makeText(context, status, Toast.LENGTH_LONG).show();
        isFirstTime = false;
    }

    public static String connectivityMode(Context context)
    {
        ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        if (null != activeNetwork)
        {
            if(activeNetwork.getType() == ConnectivityManager.TYPE_WIFI)
                return "Далучана да Wifi";

            if(activeNetwork.getType() == ConnectivityManager.TYPE_MOBILE)
                return "Злучэнне адноўлена";
        }
        return "Сеціва недаступна";
    }
}
