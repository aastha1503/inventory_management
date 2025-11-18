package com.example.first.adapters;


import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.first.R;
import com.example.first.models.AiSuggestion;

import java.util.ArrayList;

public class AiReportsAdapter extends RecyclerView.Adapter<AiReportsAdapter.ViewHolder> {

    private ArrayList<AiSuggestion> list;

    public AiReportsAdapter(ArrayList<AiSuggestion> list) {
        this.list = list;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_ai_suggestion, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        AiSuggestion item = list.get(position);

        holder.txtItemName.setText(item.getItemName());
        holder.txtStatus.setText(item.getStatus());
        holder.txtSuggestion.setText(item.getSuggestion());
    }

    @Override
    public int getItemCount() { return list.size(); }

    public static class ViewHolder extends RecyclerView.ViewHolder {

        TextView txtItemName, txtStatus, txtSuggestion;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            txtItemName = itemView.findViewById(R.id.txtItemName);
            txtStatus = itemView.findViewById(R.id.txtStatus);
            txtSuggestion = itemView.findViewById(R.id.txtSuggestion);
        }
    }
}
