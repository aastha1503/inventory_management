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
import com.example.first.adapters.AiReportsAdapter;
import com.example.first.models.AiSuggestion;

import java.util.ArrayList;

public class AiReportsFragment extends Fragment {

    private RecyclerView recyclerView;
    private AiReportsAdapter adapter;
    private ArrayList<AiSuggestion> suggestionsList;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_ai_reports, container, false);

        recyclerView = view.findViewById(R.id.recyclerAiReports);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));

        generateDummyAiSuggestions();

        adapter = new AiReportsAdapter(suggestionsList);
        recyclerView.setAdapter(adapter);

        return view;
    }

    // Dummy logic — Replace with real AI later
    private void generateDummyAiSuggestions() {
        suggestionsList = new ArrayList<>();

        suggestionsList.add(new AiSuggestion(
                "Rice Bag",
                "Low Stock",
                "Only 20 bags left. Based on last month's sales, restock at least 50 more bags."
        ));

        suggestionsList.add(new AiSuggestion(
                "Sugar Packets",
                "Overstocked",
                "You have 120 packets but only 15 sold last month. Stop buying more sugar for now."
        ));

        suggestionsList.add(new AiSuggestion(
                "Oil Bottles",
                "Good Inventory",
                "Stock level is perfect. No immediate action needed."
        ));

        suggestionsList.add(new AiSuggestion(
                "Wheat Flour",
                "High Demand",
                "Flour is selling very fast. Increase stock by 30% to avoid shortages."
        ));
    }
}
