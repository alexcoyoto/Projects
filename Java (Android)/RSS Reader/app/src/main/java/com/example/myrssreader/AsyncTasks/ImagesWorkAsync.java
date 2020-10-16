package com.example.myrssreader.AsyncTasks;


import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.view.View;
import android.widget.ImageView;
import android.widget.ListView;

import com.example.myrssreader.MainActivity;
import com.example.myrssreader.Models.RSSModel;
import com.example.myrssreader.R;
import com.example.myrssreader.Repository;

import java.net.URL;
import java.util.ArrayList;

public class ImagesWorkAsync extends AsyncTask<ArrayList<RSSModel>, Integer, ArrayList<RSSModel>>{
    private  ListView listView;
    private  int current;

    private MainActivity mainActivity;
    private Repository repository;

    public ImagesWorkAsync(ListView listView, MainActivity mainActivity, Repository repository) {
        this.listView = listView;
        this.mainActivity = mainActivity;
        this.repository = repository;
        current = 0;
    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
    }

    @SafeVarargs
    @Override
    protected final ArrayList<RSSModel> doInBackground(ArrayList<RSSModel>... arrayLists) {
        ArrayList<RSSModel> list = arrayLists[0];
        String url = "";
        Bitmap bmp;
        try {
            for (RSSModel item : list) {
                url = item.getImageurl();
                bmp = BitmapFactory.decodeStream(new URL(url).openConnection().getInputStream());
                item.setBitmap(bmp);
                publishProgress(current);
                current++;
            }
        }
        catch (Exception ex)
        {
            ex.printStackTrace();
        }

        saveImagesToDatabase(list);

        return list;
    }

    private void saveImagesToDatabase(ArrayList<RSSModel> list)
    {
        repository.clearImages();
        for (RSSModel item: list)
        {
            if (item.getBitmap() != null)
            {
                repository.insertBitmap(item.getBitmap(), item.getImageurl());
            }
        }

    }

    @Override
    protected void onProgressUpdate(Integer... values) {
        View itemView = getViewByPosition(values[0]);
        ImageView imageView = itemView.findViewById(R.id.image_view);
        imageView.setImageBitmap(((RSSModel)(listView.getAdapter().getItem(values[0]))).getBitmap());
        //repository.insertBitmap(((RSSModel)(listView.getAdapter().getItem(values[0]))).getBitmap() , ((RSSModel)(listView.getAdapter().getItem(values[0]))).getImageurl());

    }

    private View getViewByPosition(int pos) {
        final int firstListItemPosition = listView.getFirstVisiblePosition();
        final int lastListItemPosition = firstListItemPosition + listView.getChildCount() - 1;

        if (pos < firstListItemPosition || pos > lastListItemPosition ) {
            return listView.getAdapter().getView(pos, null, listView);
        } else {
            final int childIndex = pos - firstListItemPosition;
            return listView.getChildAt(childIndex);
        }
    }

    @Override
    protected void onPostExecute(ArrayList<RSSModel> list) {
        mainActivity.onSuccessfulParsing();
        super.onPostExecute(list);
    }
}