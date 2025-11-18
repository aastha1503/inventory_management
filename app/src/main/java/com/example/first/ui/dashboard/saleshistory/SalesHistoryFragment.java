package com.example.first.ui.dashboard.saleshistory;


import android.app.AlertDialog;
import android.os.Bundle;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

import com.example.first.R;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class SalesHistoryFragment extends Fragment {

    private ListView listView;
    private ImageButton btnSort;

    private ArrayList<SalesItem> salesList;
    private SalesHistoryAdapter adapter;

    public SalesHistoryFragment() { }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_sales_history, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        listView = view.findViewById(R.id.salesListView);
        btnSort = view.findViewById(R.id.btnSort);

        loadDummyData();
        setupSorting();
    }

    private void loadDummyData() {
        salesList = new ArrayList<>();

        salesList.add(new SalesItem("Banana", "10", "2024-02-01"));
        salesList.add(new SalesItem("Orange", "5", "2024-02-15"));
        salesList.add(new SalesItem("Apple", "20", "2024-01-05"));
        salesList.add(new SalesItem("Tomato", "7", "2024-03-01"));
        salesList.add(new SalesItem("Mango", "12", "2023-12-20"));

        adapter = new SalesHistoryAdapter(getContext(), salesList);
        listView.setAdapter(adapter);
    }

    private void setupSorting() {

        btnSort.setOnClickListener(v -> {
            String[] options = {
                    "A - Z",
                    "Z - A",
                    "Newest First",
                    "Oldest First",
                    "Sort by Month",
                    "Sort by Year",
                    "Show All"
            };

            new AlertDialog.Builder(getContext())
                    .setTitle("Sort Sales History")
                    .setItems(options, (dialog, which) -> {

                        switch (which) {
                            case 0:  // A-Z
                                Collections.sort(salesList, Comparator.comparing(s -> s.itemName));
                                break;

                            case 1: // Z-A
                                Collections.sort(salesList, (a, b) -> b.itemName.compareTo(a.itemName));
                                break;

                            case 2: // Newest first
                                Collections.sort(salesList, (a, b) -> b.date.compareTo(a.date));
                                break;

                            case 3: // Oldest first
                                Collections.sort(salesList, Comparator.comparing(s -> s.date));
                                break;

                            case 4: // This month only
                                filterByMonth("2024-02");
                                return;

                            case 5: // This year only
                                filterByYear("2024");
                                return;

                            case 6: // Reset list
                                loadDummyData();
                                break;
                        }

                        adapter.notifyDataSetChanged();
                    })
                    .show();
        });
    }

    private void filterByMonth(String month) {
        ArrayList<SalesItem> filtered = new ArrayList<>();

        for (SalesItem item : salesList) {
            if (item.date.startsWith(month)) {
                filtered.add(item);
            }
        }

        if (filtered.isEmpty()) {
            Toast.makeText(getContext(), "No records found for this month", Toast.LENGTH_SHORT).show();
        }

        adapter = new SalesHistoryAdapter(getContext(), filtered);
        listView.setAdapter(adapter);
    }

    private void filterByYear(String year) {
        ArrayList<SalesItem> filtered = new ArrayList<>();

        for (SalesItem item : salesList) {
            if (item.date.startsWith(year)) {
                filtered.add(item);
            }
        }

        if (filtered.isEmpty()) {
            Toast.makeText(getContext(), "No records found for this year", Toast.LENGTH_SHORT).show();
        }

        adapter = new SalesHistoryAdapter(getContext(), filtered);
        listView.setAdapter(adapter);
    }
}
