package com.example.first;

import android.os.Bundle;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;   // <-- correct import for ViewGroup

public class ReportsFragment extends Fragment {

    public ReportsFragment() { }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the fragment layout (make sure res/layout/fragment_reports.xml exists)
        return inflater.inflate(R.layout.fragment_reports, container, false);
    }
}

