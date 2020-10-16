package com.example.lab3;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Toolbar;

import com.muddzdev.styleabletoast.StyleableToast;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;

public class NoteActivity extends Activity {
    private Note note;
    private MyRepository repository;
    private boolean isNew;
    boolean isAdded;
    private int _id;
    private TagAdapter tagAdapter;

    private static final String TAG = "note_activity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_note);

        //Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        //setSupportActionBar(toolbar);

        isAdded = false;
        repository = new MyRepository(getApplicationContext());
        repository.open();

        ListView listView = findViewById(R.id.tag_list);
        EditText title = findViewById(R.id.edit_title);
        EditText body = findViewById(R.id.edit_body);
        TextView date = findViewById(R.id.edit_date);

        ArrayList<Tag> taglist = new ArrayList<>();

        Bundle extras = getIntent().getExtras(); // атрыманыя дадзеныя
        if (extras != null) {
            isNew = false;
            _id = extras.getInt("_id");
            note = repository.getNote(_id);
            if (note != null) {
                title.setText(note.getTitle());
                body.setText(note.getBody());
                date.setText(note.getDate());

                Log.d(TAG, "Атрымліваем спіс тэгаў");
                taglist = repository.getTags(note);
            } else {
                isNew = true;
                StyleableToast.makeText(this, "Не знаходжу запіс па id: " + _id, R.style.materialToast).show();
            }
        } else {
            isNew = true;
            SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy ' ' HH:mm", Locale.getDefault());
            String currentDate = sdf.format(new Date());
            date.setText(currentDate);
        }

        tagAdapter = new TagAdapter(this, taglist);
        listView.setAdapter(tagAdapter);
        listView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view,
                                           int position, long id) { // выдаленне тэгаў
                Tag tag = (Tag)tagAdapter.getItem(position);
                tagAdapter.removeTag(position);
                return true;
            }
        });
    }

    // націснулі на кнопку
    public void addTag(View view)
    {
        EditText editText = findViewById(R.id.tag_name);
        if (editText.getText().toString().equals("")) {
            StyleableToast.makeText(this, "Увядзіце назву тэга", R.style.materialToast).show();
            return;
        }
        else {
            Tag tag = new Tag(editText.getText().toString());
            if (!tagAdapter.contains(tag)) { // калі няма тэга з такой назвай
                if (repository.contains(tag)) { // можна потым апрацаваць
                    tag = repository.getTag(tag.getName());
                }

                long id = repository.insert(tag);
                tag.setId((int)id);
                tagAdapter.addTag(tag);
                editText.setText("");
            }
            else
                StyleableToast.makeText(this, "Тэг з назвай " + tag.getName() + " ужо прысутнічае!", R.style.materialToast).show();
        }
    }


    public void save(View view)
    {
        SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy ' ' HH:mm", Locale.getDefault());
        String currentDate = sdf.format(new Date());

        EditText title = findViewById(R.id.edit_title);
        EditText body = findViewById(R.id.edit_body);
        TextView date = findViewById(R.id.edit_date);
        date.setText(currentDate);
        if (title.getText().toString().equals("")) // калі нічога не напісалі, выводзім дату
            title.setText(date.getText());

        if (isNew) {
            note = new Note(title.getText().toString(), body.getText().toString(), date.getText().toString(), null);
            long id = repository.insert(note);
            note.setId((int)id);
        } else {
            note.setTitle(title.getText().toString());
            note.setBody(body.getText().toString());
            note.setDate(date.getText().toString());
            repository.updateNote(note);
        }
        isAdded = true;
        repository.removeLinks(note);
        repository.insert(note, tagAdapter.getArray());
        goHome();
    }

    public void back(View view)
    {
        isAdded = false;
        goHome();
    }

    private void goHome(){
        Intent data = new Intent();
        data.putExtra(MainActivity.is_added, isAdded); // ці дадалі новы запіс?
        setResult(RESULT_OK, data); // калі дадалі, RESULT_OK = 1
        finish();
    }


    @Override
    public void onDestroy()
    {
        super.onDestroy();
        Log.d(TAG, "onDestroy");

        repository.close();
    }

}
