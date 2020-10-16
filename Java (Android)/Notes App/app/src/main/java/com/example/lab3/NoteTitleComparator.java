package com.example.lab3;

import java.util.Comparator;

public class NoteTitleComparator implements Comparator<Note> {

    @Override
    public int compare(Note o1, Note o2) {
        return o1.getTitle().compareTo(o2.getTitle());
    }
}
