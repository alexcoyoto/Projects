package com.example.myrssreader;

import android.annotation.SuppressLint;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

import com.example.myrssreader.Models.DatabaseHelper;
import com.example.myrssreader.Models.RSSModel;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;

public class Repository {
    private DatabaseHelper DbHelper;
    private SQLiteDatabase database;

    public Repository(Context context)
    {
        DbHelper = new DatabaseHelper(context);
    }

    public void open()
    {
        try{
            database = DbHelper.getWritableDatabase(); }
        catch (android.database.sqlite.SQLiteException ex){
            database = DbHelper.getReadableDatabase();}
    }

    public void close()
    {
        DbHelper.close();
    }

    public long insertItem(RSSModel item)
    {
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_TITLE, item.getTitle());
        values.put(DatabaseHelper.COLUMN_PREVIEW, item.getPreview());
        values.put(DatabaseHelper.COLUMN_DATE, item.getDate());
        values.put(DatabaseHelper.COLUMN_LINK, item.getLink());
        values.put(DatabaseHelper.COLUMN_IMAGEURL, item.getImageurl());
        long answer = database.insert(DatabaseHelper.TABLE_RSSITEM, "_", values);

        if (item.getBitmap() != null)
        {
            ContentValues BitmapValue = new ContentValues();
            BitmapValue.put(DatabaseHelper.COLUMN_IMAGEURL, item.getImageurl());
            Bitmap bitmap = item.getBitmap();

            ByteArrayOutputStream BYTE_ARRAY_STREAM = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.PNG,100, BYTE_ARRAY_STREAM);
            String bitmapStr = Base64.encodeToString(BYTE_ARRAY_STREAM.toByteArray(), Base64.DEFAULT);
            BitmapValue.put(DatabaseHelper.COLUMN_BITMAPBYTES, bitmapStr);

            database.insert(DatabaseHelper.TABLE_BITMAP, "_", BitmapValue);
        }
        return answer;
    }

    public long updateCacheStatus(String url, String new_value)
    {
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_DATE, new_value);
        String where = DatabaseHelper.COLUMN_LINK + "=" + "\"" + url+ "\";";
        return database.update(DatabaseHelper.TABLE_RSSITEM, values, where, null);
    }

    public void insertItems(ArrayList<RSSModel> list) {
        for (RSSModel item: list)
            insertItem(item);
    }

    public void insertBitmap(Bitmap bitmap, String imageURL)
    {
        ContentValues BitmapValue = new ContentValues();
        ByteArrayOutputStream BYTE_ARRAY_STREAM = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG,100, BYTE_ARRAY_STREAM);
        String bitmapStr = Base64.encodeToString(BYTE_ARRAY_STREAM.toByteArray(), Base64.DEFAULT);
        BitmapValue.put(DatabaseHelper.COLUMN_BITMAPBYTES, bitmapStr);
        BitmapValue.put(DatabaseHelper.COLUMN_IMAGEURL, imageURL);
        database.insert(DatabaseHelper.TABLE_BITMAP, "_", BitmapValue);
    }

    public ArrayList<RSSModel> getItems()
    {
        String title, preview, link, imageURL, date;

        ArrayList<RSSModel> result = new ArrayList<>();
        Cursor cursor = database.query(DatabaseHelper.TABLE_RSSITEM, null, null, null, null, null, null);
        if (cursor.moveToFirst())
            do {
                title = cursor.getString(cursor.getColumnIndex("title"));
                preview = cursor.getString(cursor.getColumnIndex("preview"));
                date = cursor.getString(cursor.getColumnIndex("date"));
                link = cursor.getString(cursor.getColumnIndex("link"));
                imageURL = cursor.getString(cursor.getColumnIndex("imageurl"));

                RSSModel rssItem = new RSSModel(title, date, preview, link, imageURL);
             if (!imageURL.equals(""))
                    {
                        Cursor imageCursor = database.rawQuery("select * from bitmap where imageurl = \"" + imageURL + "\";", null);
                        if (imageCursor.moveToFirst())
                        {
                            String bitmapBytes = imageCursor.getString(imageCursor.getColumnIndex(DatabaseHelper.COLUMN_BITMAPBYTES));
                            byte [] encodeByte = Base64.decode(bitmapBytes,Base64.DEFAULT);
                            Bitmap bitmap = BitmapFactory.decodeByteArray(encodeByte, 0, encodeByte.length);
                            rssItem.setBitmap(bitmap);
                        }
                    }

                result.add((rssItem));
            }
            while(cursor.moveToNext());
        cursor.close();
        return result;
    }

    public void clear(){
        database.execSQL("delete from rssitem;");
        database.execSQL("delete from bitmap;");
    }

    public void clearImages(){
        database.execSQL("delete from bitmap;");
    }

    public String getLastUrl()
    {
        @SuppressLint("Recycle") Cursor cursor = database.query(DatabaseHelper.TABLE_LASTRSSURL, null, null, null, null, null, null);
        if (cursor.moveToFirst())
            return cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_LASTRSSURL));
        return "";
    }

    public void setLastUrl(String lastRSSURL)
    {
        database.execSQL("delete from lastrssurl;");
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_LASTRSSURL, lastRSSURL);
        database.insert(DatabaseHelper.TABLE_LASTRSSURL, "_", values);
    }
}

