package com.example.lab3;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.util.Log;

import java.util.ArrayList;


public class MyRepository {

    public static final String TAG = "repository";

    private DatabaseHelper dbhelper;
    private SQLiteDatabase db;


    public MyRepository(Context context) {
        dbhelper = new DatabaseHelper(context);
    }

    public void open() {
        try {
            db = dbhelper.getWritableDatabase();
        } catch (SQLiteException ex) {
            db = dbhelper.getReadableDatabase();
        }
    }

    public void close() {
        dbhelper.close();
    }

    public Note getNote(int id) {
        Log.d(TAG, "SELECT * FROM " + DatabaseHelper.TABLE_NOTE + " WHERE _id = " + id + ";");
        Cursor cursor = db.rawQuery("SELECT * FROM " + DatabaseHelper.TABLE_NOTE + " WHERE _id = " + id + ";", null); // запыт у бд

        if (cursor.moveToFirst()) { // ці мае вынік аперацыя ?
            int _id = cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_ID_NOTE));
            String title = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_TITLE_NOTE));
            String body = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_BODY_NOTE));
            String date = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_DATE_NOTE));

            return new Note(_id, title, body, date, null);
        } else
            return null;
    }

    public ArrayList<Note> getNotes() {
        ArrayList<Note> list = new ArrayList<>();

        Cursor cursor = db.query(DatabaseHelper.TABLE_NOTE, null, null, null, null, null, null); // ??
        if (cursor.moveToFirst()) {
            do {
                int id = cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_ID_NOTE));
                String title = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_TITLE_NOTE));
                String body = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_BODY_NOTE));
                String date = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_DATE_NOTE));

                Note note = new Note(id, title, body, date, null);

                Log.d(TAG, "id: " + note.getId() + " title: " + note.getTitle() + " body: " + note.getBody() + " date " + note.getDate());
                list.add(note);
            } while (cursor.moveToNext());
        }
        cursor.close();
        return list;
    }

    public long insert(Note note) {
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_TITLE_NOTE, note.getTitle());
        values.put(DatabaseHelper.COLUMN_BODY_NOTE, note.getBody());
        values.put(DatabaseHelper.COLUMN_DATE_NOTE, note.getDate());
        return db.insert(DatabaseHelper.TABLE_NOTE, "_", values);
    }

    public void removeNote(int _id) {
        Log.d(TAG, "Removing note " + _id);
        db.delete(DatabaseHelper.TABLE_NOTE, "_id = ?", new String[]{Integer.toString(_id)});
    }

    public void updateNote(Note note) {
        Log.d(TAG, "Updating note " + note.getId());
        ContentValues cv = new ContentValues();
        cv.put(DatabaseHelper.COLUMN_TITLE_NOTE, note.getTitle());
        cv.put(DatabaseHelper.COLUMN_BODY_NOTE, note.getBody());
        cv.put(DatabaseHelper.COLUMN_DATE_NOTE, note.getDate());
        db.update(DatabaseHelper.TABLE_NOTE, cv, "_id = ?", new String[]{Integer.toString(note.getId())});
    }

    public long insert(Tag tag) {
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_NAME_TAG, tag.getName());
        return db.insert(DatabaseHelper.TABLE_TAG, "_", values);
    }

    public void removeLinks(Note note) {
        String query = String.format("DELETE FROM %s WHERE %s = %d", DatabaseHelper.TABLE_LINK, DatabaseHelper.COLUMN_IDNOTE_LINK, note.getId());
        Log.d(TAG, query);
        db.execSQL(query);
    }


    public ArrayList<Tag> getTags(Note note) {
        ArrayList<Tag> list = new ArrayList<>();

        String query = String.format("SELECT * FROM %s JOIN %s ON ((%s.%s = %d) AND (%s.%s = %s.%s )) ;", DatabaseHelper.TABLE_LINK, DatabaseHelper.TABLE_TAG, DatabaseHelper.TABLE_LINK, DatabaseHelper.COLUMN_IDNOTE_LINK, note.getId(), DatabaseHelper.TABLE_LINK, DatabaseHelper.COLUMN_IDTAG_LINK, DatabaseHelper.TABLE_TAG, DatabaseHelper.COLUMN_ID_TAG);
        Log.d(TAG, query);
        Cursor cursor = db.rawQuery(query, null);
        if (cursor.moveToFirst())
            do {
                int id = cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_ID_TAG));
                String name = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_NAME_TAG));

                Tag tag = new Tag(id, name);

                Log.d(TAG, "Getting tag: id: " + tag.getId() + " name: " + tag.getName());
                list.add(tag);
            }
            while (cursor.moveToNext());

        cursor.close();
        return list;
    }


    public boolean contains(Tag tag) {
        Cursor cursor = db.rawQuery("SELECT * FROM " + DatabaseHelper.TABLE_TAG + " WHERE " + DatabaseHelper.COLUMN_NAME_TAG + " = '" + tag.getName() + "';", null);
        if (cursor.moveToFirst())
            return true;
        return false;
    }

    public Tag getTag(String name) {
        Cursor cursor = db.rawQuery("SELECT * FROM " + DatabaseHelper.TABLE_TAG + " WHERE " + DatabaseHelper.COLUMN_NAME_TAG + " = '" + name + "';", null);
        if (cursor.moveToFirst()) {
            int id = cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_ID_NOTE));
            return new Tag(id, name);
        } else return null;

    }

    public void insert(Note note, Tag[] tags) // зрабіць сувязь
    {
        for (Tag tag : tags) {
            ContentValues values = new ContentValues();
            values.put(DatabaseHelper.COLUMN_IDNOTE_LINK, note.getId());
            values.put(DatabaseHelper.COLUMN_IDTAG_LINK, tag.getId());
            Log.d(TAG, String.format("insert into table link idnote = %d idtag = %d", note.getId(), tag.getId()));
            db.insert(DatabaseHelper.TABLE_LINK, "_", values);
        }
    }

    public ArrayList<Note> getNotesByTag(Tag tag) {
        ArrayList<Note> list = new ArrayList<>();

        String query = String.format("SELECT note._id, note.title, note.body, note.date FROM %s JOIN %s ON (%s.%s = %s.%s) JOIN %s ON ((%s.%s = %s.%s) AND (%s.%s = '%s')) ;", DatabaseHelper.TABLE_NOTE, DatabaseHelper.TABLE_LINK, DatabaseHelper.TABLE_NOTE, DatabaseHelper.COLUMN_ID_NOTE, DatabaseHelper.TABLE_LINK, DatabaseHelper.COLUMN_IDNOTE_LINK, DatabaseHelper.TABLE_TAG, DatabaseHelper.TABLE_LINK, DatabaseHelper.COLUMN_IDTAG_LINK, DatabaseHelper.TABLE_TAG, DatabaseHelper.COLUMN_ID_TAG, DatabaseHelper.TABLE_TAG, DatabaseHelper.COLUMN_NAME_TAG, tag.getName());
        Log.d(TAG, query);
        Cursor cursor = db.rawQuery(query, null);
        if (cursor.moveToFirst())
            do {
                int id = cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_ID_NOTE));
                String title = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_TITLE_NOTE));
                String body = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_BODY_NOTE));
                String date = cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_DATE_NOTE));

                Note note = new Note(id, title, body, date, null);

                Log.d(TAG, "id: " + note.getId() + " title: " + note.getTitle() + " body: " + note.getBody() + " date " + note.getDate());
                list.add(note);
            } while (cursor.moveToNext());
        cursor.close();

        return list;
    }
}