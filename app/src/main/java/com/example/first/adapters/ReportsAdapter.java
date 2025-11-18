package com.example.first.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.first.R;
import com.example.first.models.ReportItem;

import java.util.ArrayList;

public class ReportsAdapter extends RecyclerView.Adapter<ReportsAdapter.ViewHolder> {

    private ArrayList<ReportItem> list;

    public ReportsAdapter(ArrayList<ReportItem> list) {
        this.list = list;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_report, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        ReportItem item = list.get(position);

        holder.txtName.setText(item.getName());
        holder.txtTotal.setText("Total Qty: " + item.getTotalQty());
        holder.txtSold.setText("Sold: " + item.getSoldQty());
        holder.txtLeft.setText("Remaining: " + item.getRemainingQty());

        holder.txtCustomer.setText("Customer: " + item.getCustomerName());
        holder.txtPhone.setText("Phone: " + item.getCustomerPhone());
        holder.txtAddress.setText("Address: " + item.getCustomerAddress());
        holder.txtPayment.setText("Payment: " + item.getPaymentMode());
    }

    @Override
    public int getItemCount() { return list.size(); }

    public static class ViewHolder extends RecyclerView.ViewHolder {

        TextView txtName, txtTotal, txtSold, txtLeft, txtCustomer, txtPhone, txtAddress, txtPayment;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            txtName = itemView.findViewById(R.id.txtName);
            txtTotal = itemView.findViewById(R.id.txtTotal);
            txtSold = itemView.findViewById(R.id.txtSold);
            txtLeft = itemView.findViewById(R.id.txtLeft);
            txtCustomer = itemView.findViewById(R.id.txtCustomer);
            txtPhone = itemView.findViewById(R.id.txtPhone);
            txtAddress = itemView.findViewById(R.id.txtAddress);
            txtPayment = itemView.findViewById(R.id.txtPayment);
        }
    }
}
