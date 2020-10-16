package com.example.lab3;

import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.SearchView;

import androidx.annotation.NonNull;

import java.util.ArrayList;
import java.util.Collections;

import com.muddzdev.styleabletoast.StyleableToast;

public class MainActivity extends Activity implements View.OnClickListener {
    private final String TAG = "MainActivity";

    public static MyArrayAdapter myArrayAdapter;
    private AdapterView adapterView;
    private MyRepository repository;
    Button addNote, sortList, sortRev;
    public boolean isSortedByDate = true;
    public boolean isReversed = false;
    public String searchText = "";
    String answer = "Sorted by Date";
    String reverseMessage = "Normal mode";

    static final String is_added = "is_added";
    private static  final int request_code = 1;

    private static String SORT_KEY = "100";
    private static String REVERSE_KEY = "101";
    private static String SEARCH_KEY = "110";



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if(savedInstanceState != null)
        {
            answer = savedInstanceState.getString(SORT_KEY);
            reverseMessage = savedInstanceState.getString(REVERSE_KEY);
            searchText = savedInstanceState.getString(SEARCH_KEY);
           // StyleableToast.makeText(this, searchText, R.style.materialToast).show();
        }

        setContentView(R.layout.activity_main);
        if (getActionBar() != null)
            getActionBar().hide();

        SearchView search = findViewById(R.id.search_view);
        addNote = findViewById(R.id.addNote);
        addNote.setOnClickListener(this);
        sortList = findViewById(R.id.sortType);
        sortList.setOnClickListener(this);
        sortRev = findViewById(R.id.reversedSort);
        sortRev.setOnClickListener(this);


        repository = new MyRepository(this);
        repository.open();

        ArrayList<Note> array = repository.getNotes();
        myArrayAdapter = new MyArrayAdapter(this, array); // зменная для апрацоўкі спісу

        if (searchText.equals(""))
        {
            Sort();
        }
        else
            myArrayAdapter.updateArray(repository.getNotesByTag(new Tag(searchText)));
        ReverseMethod();

        // арыентацыя
        if (getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT) {
            ListView listView = findViewById(R.id.listview);
            listView.setAdapter(myArrayAdapter);
            adapterView = listView;
        } else {
            GridView gridView = findViewById(R.id.gridview);
            gridView.setAdapter(myArrayAdapter);
            adapterView = gridView;

        }

        adapterView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view,
                                           int position, long id) {
                repository.removeNote(myArrayAdapter.getNoteId(position)); // выдаліць з БД
                myArrayAdapter.removeNote(position); // выдаліць з масіву
                myArrayAdapter.notifyDataSetChanged(); // апавяшчэнне аб выдаленні і заклік абнавіцца кожнаму View
                return true;
            }
        });

        adapterView.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id)
            {
                Note note = (Note)myArrayAdapter.getItem(position);

                if (note != null)
                {
                    // перахoд на старонку NoteActivity
                    Intent intent = new Intent(getApplicationContext(), NoteActivity.class);
                    intent.putExtra("_id", note.getId());
                    startActivityForResult(intent, request_code); // каб атрымаць вынік працы таго, што вышэй (апрцоўваецца праз onActivityResult ніжэй)
                }
            }
        });



        search.setOnCloseListener(new SearchView.OnCloseListener() {
            @Override
            public boolean onClose() {
                myArrayAdapter.updateArray(repository.getNotes());
                searchText = "";
                Sort();
                return false;
            }
        });

        // увод знакоў
        search.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            //  калі карыстач адпраўляе запыт
            @Override
            public boolean onQueryTextSubmit(String query) {
                return false;
            }

            @Override
            public boolean onQueryTextChange(String newText) {
                reverseMessage = "Normal mode";
                if (newText.equals("")) {
                    myArrayAdapter.updateArray(repository.getNotes());
                    Sort();
                }
                else
                    myArrayAdapter.updateArray(repository.getNotesByTag(new Tag(newText)));
                searchText = newText;
                return false;
            }
        });
    }

    @Override
    protected void onRestoreInstanceState(@NonNull Bundle savedInstanceState) {
        //ReverseMethod();
    }

    @Override
    protected void onSaveInstanceState(@NonNull Bundle outState) {

        outState.putString(SORT_KEY, answer);
        outState.putString(REVERSE_KEY, reverseMessage);
        outState.putString(SEARCH_KEY, searchText);
        //StyleableToast.makeText(this, answer, R.style.materialToast).show();
        super.onSaveInstanceState(outState);
    }

    public void onClick(View view) {
        switch(view.getId()) {
            case R.id.addNote:
                // пераход на новую старонку, але без дадзеных id
                Intent intent = new Intent(this, NoteActivity.class);
                startActivityForResult(intent, request_code);
                break;
            case R.id.sortType: // кнопка сартавання
                if (isSortedByDate) {
                    ArrayList<Note> n = myArrayAdapter.getArray();
                    Collections.sort(n, new NoteTitleComparator());
                    myArrayAdapter.updateArray(n);
                    answer = "Sorted by Text";
                    isSortedByDate = false;
                } else {
                    ArrayList<Note> n = myArrayAdapter.getArray();
                    Collections.sort(n, new NoteDateComparator());
                    myArrayAdapter.updateArray(n);
                    answer = "Sorted by Date";
                    isSortedByDate = true;
                }
                reverseMessage = "Normal mode"; // праблемны момант, з-за якога была памылка!
                break;
            case R.id.reversedSort:
                isReversed = !isReversed;
                ArrayList<Note> n = myArrayAdapter.getArray();
                Collections.reverse(n);
                myArrayAdapter.updateArray(n);
                reverseMessage = (reverseMessage.equals("Normal mode")) ? "Reversed" : "Normal mode";

        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        repository.close();
    }

    @Override
    //калі вяртаемся на старонку зноў пасля пераходу на NoteActivity. Аднаўляем усе дадзеныя
    public void onActivityResult(int requestCode, int resultCode, Intent data){
        if(requestCode == request_code){
            if(resultCode == RESULT_OK){
                MyRepository repository = new MyRepository(this);
                repository.open();
                ArrayList<Note> array = repository.getNotes();
                myArrayAdapter.updateArray(array);
                repository.close();
                //Sort();
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data); // інакш нічога не зменіцца (пусты бацькоўскі метад)
            //Sort();
        }
    }

    public void Sort()
    {
        if (answer.equals("Sorted by Text")) {
            ArrayList<Note> n = myArrayAdapter.getArray();
            Collections.sort(n, new NoteTitleComparator());
            myArrayAdapter.updateArray(n);
        } else if (answer.equals("Sorted by Date")) {
            ArrayList<Note> n = myArrayAdapter.getArray();
            Collections.sort(n, new NoteDateComparator());
            myArrayAdapter.updateArray(n);
        }
    }

    public void ReverseMethod()
    {
        //StyleableToast.makeText(this, reverseMessage, R.style.materialToast).show();
        if (!reverseMessage.equals("Normal mode"))
        {
            ArrayList<Note> n = myArrayAdapter.getArray();
            Collections.reverse(n);
            myArrayAdapter.updateArray(n);
        }
    }
}
