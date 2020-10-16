package com.example.myrssreader;

import androidx.appcompat.app.AppCompatActivity;

import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.res.Configuration;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.example.myrssreader.AsyncTasks.ImagesWorkAsync;
import com.example.myrssreader.AsyncTasks.ParsingAsync;
import com.example.myrssreader.BrowserModel.WebViewBrowserModel;
import com.example.myrssreader.Models.RSSModel;

import android.content.pm.ActivityInfo;

import java.util.ArrayList;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    RSSListAdapter myRSSListAdapter;
    Repository myRepository;

    private ParsingAsync task;
    private ImagesWorkAsync asyncImageLoad;

   // public static final String is_added = "is_added";
   // private static  final int request_code = 1;


    public void DebugMode(View view) {
        ArrayList<RSSModel> array = new ArrayList<>();
        RSSModel model;
        for (int i = 0; i < 10; i++) {
            model = new RSSModel(
                    "Note that the only valid version of the GPL as far as this project" +
                            " is concerned is _this_ particular version of the license (ie v2, not" +
                            " v2.2 or v3.x or whatever), unless explicitly otherwise stated.",
                    "10.10.2020",
                    "HOWEVER, in order to allow a migration to GPLv3 if that seems like" +
                            " a good idea, I also ask that people involved with the project make" +
                            "  might avoid issues. But we can also just decide to synchronize and" +
                            "  contact all copyright holders on record if/when the occasion arises.",
                    "",
                    "");
            array.add(model);
        }
        myRSSListAdapter = new RSSListAdapter(this, array);
        ListView rss_list = findViewById(R.id.rss_list);
        rss_list.setAdapter(myRSSListAdapter);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Objects.requireNonNull(getSupportActionBar()).hide();

        BroadcastReceiver networkReceiver = new ConnectionReceiver();
        registerReceiver(networkReceiver, new IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION));

        openRepository();
        //myRepository.clear();
        //myRepository.insertItem(new RSSModel("Test title", "24.01.2020", "Test preview", "https://www.wikipedia.org", ""));
        //myRepository.insertItem(new RSSModel("Test title2", "24.01.2020", "Test preview", "https://www.texterra.ru", ""));
        EditText edit = findViewById(R.id.edit_rss);
        edit.setText(myRepository.getLastUrl());

        ArrayList<RSSModel> array = myRepository.getItems();
        myRSSListAdapter = new RSSListAdapter(this, array);
        ListView rss_list = findViewById(R.id.rss_list);
        rss_list.setAdapter(myRSSListAdapter);
        rss_list.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                createWebViewByLink(((RSSModel) Objects.requireNonNull(myRSSListAdapter.
                        getItem(position))).getLink());
            }
        });

    }

    private void openRepository(){
        myRepository = new Repository(this);
        myRepository.open();
    }

    public void createWebViewByLink(String currentURL)
    {
        Intent intent = new Intent(this, WebViewBrowserModel.class);
        intent.putExtra("url", currentURL);
        startActivity(intent);
        //startActivityForResult(intent, request_code);
    }

    public void onClick(View view) {
        if (isNetworkAvailable())
        {
            task = new ParsingAsync(this);
            EditText edit = findViewById(R.id.edit_rss);
            String str = edit.getText().toString();
            if (!str.startsWith("https://") && !str.startsWith("http://"))
                str = "https://" + str;

            hideButtonsAndRotation();
            task.execute(str);
        }
        else
            Toast.makeText(this, "Сеціва недаступна", Toast.LENGTH_SHORT).show();
    }

    public void clearCache(View view)
        {
        createWebViewByLink("");
        WebViewBrowserModel.clearCache();
        Toast.makeText(this, "Кэш быў паспяхова выдалены", Toast.LENGTH_SHORT).show();
    }

    /*
    public static void updateCacheStatus(String url)
    {
        ArrayList<RSSModel> array = myRepository.getItems();
        for (RSSModel item: array)
            if (item.getLink().equals(url)) {
                myRepository.updateCacheStatus(url, "cached");
                break;
            }
    }
    */

    public  void hideButtonsAndRotation()
    {
        Button button = findViewById(R.id.load_button);
        button.setVisibility(View.INVISIBLE);
        button = findViewById(R.id.debug_button);
        button.setVisibility(View.INVISIBLE);

        if(getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT)
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        else
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

    }

    public  void showButtonsAndRotation()
    {
        Button button = findViewById(R.id.load_button);
        button.setVisibility(View.VISIBLE);
        button = findViewById(R.id.debug_button);
        button.setVisibility(View.VISIBLE);

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
    }

    private boolean isNetworkAvailable()
    {
        ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();
        return networkInfo != null && networkInfo.isConnectedOrConnecting();
    }

    ////

    public void onLoadFinished(ArrayList<RSSModel> result)
    {
        if (result != null)
        {
            myRSSListAdapter.setArray(result);
            ListView listView = findViewById(R.id.rss_list);

            asyncImageLoad = new ImagesWorkAsync(listView, this, myRepository);
            asyncImageLoad.execute(myRSSListAdapter.getItems());
        }
        else
        {
            Toast.makeText(this, "Адбылася памылка: пусты спіс на выхадзе", Toast.LENGTH_LONG).show();
            showButtonsAndRotation();
        }
    }

    public void saveToDatabase(ArrayList<RSSModel> result, String str) {
        myRepository.clear();
        myRepository.setLastUrl(str);
        myRepository.insertItems(result);
    }

    public void onSuccessfulParsing()
    {
        Toast.makeText(this, "Навіны паспяхова спампаваліся!", Toast.LENGTH_LONG).show();
        showButtonsAndRotation();
    }

    ////

    @Override
    protected void onDestroy() {
        //myRepository.close();
        if (task != null)
            task.cancel(true);
        if (asyncImageLoad != null)
            asyncImageLoad.cancel(true);
        super.onDestroy();
    }


    /*
    @Override
    //калі вяртаемся на старонку зноў пасля пераходу на NoteActivity. Аднаўляем усе дадзеныя
    public void onActivityResult(int requestCode, int resultCode, Intent data){
        if(requestCode == request_code){
            if(resultCode == RESULT_OK){
                myRSSListAdapter.notifyDataSetChanged();
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }
     */


}
