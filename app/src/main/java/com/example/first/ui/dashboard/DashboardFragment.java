package com.example.first.ui.dashboard;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.first.R;
import com.example.first.ui.dashboard.adapters.InventoryAdapter;
import com.example.first.ui.dashboard.models.InventoryItem;

import java.util.ArrayList;

public class DashboardFragment extends Fragment {

    private EditText searchBar;
    private RecyclerView recyclerView;
    private InventoryAdapter adapter;
    private ArrayList<InventoryItem> itemList = new ArrayList<>();
    private ArrayList<InventoryItem> filteredList = new ArrayList<>();

    public DashboardFragment() { }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_dashboard, container, false);

        searchBar = view.findViewById(R.id.searchBar);
        recyclerView = view.findViewById(R.id.inventoryList);

        loadSampleData();
        setupRecycler();
        setupSearch();

        return view;
    }

    private void loadSampleData() {
        itemList.add(new InventoryItem("Rice", 120, 20, 100, 45.0));
        itemList.add(new InventoryItem("Sugar", 80, 10, 70, 35.0));
        itemList.add(new InventoryItem("Oil", 50, 5, 45, 120.0));
        itemList.add(new InventoryItem("Flour", 200, 35, 165, 30.0));

        filteredList.addAll(itemList);
    }

    private void setupRecycler() {
        adapter = new InventoryAdapter(filteredList);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
    }

    private void setupSearch() {
        searchBar.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) { }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) { }
            @Override
            public void afterTextChanged(Editable s) {
                filter(s.toString());
            }
        });
    }

    private void filter(String query) {
        filteredList.clear();

        for (InventoryItem item : itemList) {
            if (item.getName().toLowerCase().contains(query.toLowerCase())) {
                filteredList.add(item);
            }
        }

        adapter.notifyDataSetChanged();
    }
}

