package com.example.myrssreader.Models;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String NAME = "my_database.db";
    private static final int SCHEMA = 2;

    public DatabaseHelper(Context context)
    {
        super(context, NAME, null, SCHEMA);
    }

    public static final String TABLE_RSSITEM = "rssitem",
            COLUMN_ID = "_id",
            COLUMN_TITLE = "title",
            COLUMN_PREVIEW = "preview",
            COLUMN_DATE = "date",
            COLUMN_LINK = "link",
            COLUMN_IMAGEURL = "imageurl";

    public static final String TABLE_BITMAP = "bitmap",
            COLUMN_BITMAPBYTES = "bitmapbytes";

    public static final String TABLE_LASTRSSURL = "lastrssurl",
            COLUMN_LASTRSSURL = "last";

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("create table if not exists rssitem (_id integer primary key autoincrement," +
                " title String, preview String, date String, link String, imageurl String);");
        db.execSQL("create table if not exists bitmap (_id integer primary key autoincrement," +
                " imageurl String, bitmapbytes String);");
        db.execSQL("create table if not exists lastrssurl (_id integer primary key autoincrement," +
                " last String);");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("drop table if exists rssitem");
        onCreate(db);
    }
}
