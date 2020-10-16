package com.example.myrssreader.BrowserModel;


import androidx.appcompat.app.AppCompatActivity;

import android.annotation.TargetApi;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import android.app.ProgressDialog;

import com.example.myrssreader.ConnectionReceiver;
import com.example.myrssreader.MainActivity;
import com.example.myrssreader.R;


public class WebViewBrowserModel extends AppCompatActivity {

    class BrowserClient extends WebViewClient {
        @TargetApi(Build.VERSION_CODES.N)
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            view.loadUrl(request.getUrl().toString());
            return true;
        }
    }

    private static WebView browser;
    private static boolean isFirstTime = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_browser);


        String url = getIntent().getStringExtra("url");
        isFirstTime = false;
        if (url.equals("")) {
            //Toast.makeText(this, "Тэставая спасылка", Toast.LENGTH_SHORT).show();
            super.onBackPressed();
        }

        browser = findViewById(R.id.web_view_browser);
        browser.setWebViewClient(new BrowserClient());

        //browser.getSettings().setAppCachePath(getApplicationContext().getCacheDir().getAbsolutePath());
        //browser.getSettings().setAllowFileAccess(false);
        //browser.getSettings().setAppCacheEnabled(true);

        //if (!ConnectionReceiver.connectivityMode(this).equals("Сеціва недаступна"))
            //MainActivity.updateCacheStatus(url);
        browser.getSettings().setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
        browser.loadUrl(url);

    }

    @Override
    public void onBackPressed()
    {
        if(browser.canGoBack())
            browser.goBack();
        else {
            //Intent data = new Intent();
            //data.putExtra(MainActivity.is_added, true);
            ///setResult(RESULT_OK, data); // калі дадалі, RESULT_OK = 1
            //finish();
            super.onBackPressed();
        }
    }

    public static void clearCache() {
        if(!isFirstTime)
            browser.clearCache(true);
    }
}
