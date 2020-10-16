package com.example.myrssreader.Models;

import android.graphics.Bitmap;

public class RSSModel {

    private String title, date, preview, link, imageUrl;
    private Bitmap bitmap;

    public RSSModel(String title, String date, String preview, String link, String imageUrl) {
        this.title = title;
        this.date = date;
        this.preview = preview;
        this.link = link;
        this.imageUrl = imageUrl;
    }

    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        this.title = title;
    }

    public String getDate() {
        return date;
    }
    public void setDate(String date) {
        this.date = date;
    }

    public String getPreview() {
        return preview;
    }
    public void setPreview(String preview) {
        this.preview = preview;
    }

    public String getLink() {
        return link;
    }
    public void setLink(String link) {
        this.link = link;
    }

    public String getImageurl() {
        return imageUrl;
    }
    public void setImageurl(String imageurl) {
        this.imageUrl = imageurl;
    }

    public Bitmap getBitmap() {
        return bitmap;
    }
    public void setBitmap(Bitmap bitmap) {
        this.bitmap = bitmap;
    }
}
