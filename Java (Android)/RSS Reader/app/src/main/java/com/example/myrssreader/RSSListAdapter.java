package com.example.myrssreader;

import android.annotation.SuppressLint;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.myrssreader.Models.RSSModel;

import java.util.ArrayList;

public class RSSListAdapter extends ArrayAdapter
{
    private final Context context;
    private ArrayList<RSSModel> items;

    public RSSListAdapter (@NonNull Context context, ArrayList<RSSModel> items) {
        super(context, R.layout.rss_container, items);
        this.context = context;
        this.items = items;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent)
    {
        LayoutInflater inflater = (LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        assert inflater != null;
        @SuppressLint("ViewHolder") View view = inflater.inflate(R.layout.rss_container, parent, false);

        RSSModel item = items.get(position);

        TextView title =
                view.findViewById(R.id.title_view);
        TextView date  =
                view.findViewById(R.id.date_view);
        TextView preview =
                view.findViewById(R.id.preview_view);
        ImageView image =
                view.findViewById(R.id.image_view);

        title.setText(item.getTitle());
        date.setText(item.getDate());
        preview.setText(item.getPreview());

        if (item.getBitmap() != null)
            image.setImageBitmap(item.getBitmap());
        return view;
    }

    public ArrayList<RSSModel> getItems() {
        return items;
    }

    public void setArray(ArrayList<RSSModel> list)
    {
        items.clear();
        items.addAll(list);
        notifyDataSetChanged();
    }
}
