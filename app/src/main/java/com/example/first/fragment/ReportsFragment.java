package com.example.first.fragment;

import android.os.Bundle;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.first.R;
import com.example.first.models.ReportItem;
import com.example.first.adapters.ReportsAdapter;

import java.util.ArrayList;

public class ReportsFragment extends Fragment {

    private RecyclerView recyclerView;
    private ReportsAdapter adapter;
    private ArrayList<ReportItem> reportList;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_reports, container, false);

        recyclerView = view.findViewById(R.id.recyclerReports);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));

        loadDummyReports();

        adapter = new ReportsAdapter(reportList);
        recyclerView.setAdapter(adapter);

        return view;
    }

    // Dummy data (replace with API later)
    private void loadDummyReports() {
        reportList = new ArrayList<>();

        reportList.add(new ReportItem(
                "Rice Bag",
                50,
                30,
                20,
                "Rahul Sharma",
                "9876543210",
                "Delhi, India",
                "UPI"
        ));

        reportList.add(new ReportItem(
                "Sugar Packets",
                100,
                45,
                55,
                "Meena Traders",
                "9988776655",
                "Mumbai",
                "Cash"
        ));
    }
}
