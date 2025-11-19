package com.example.first.ui.dashboard.saleshistory;


import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.example.first.R;

import java.util.ArrayList;

public class SalesHistoryAdapter extends BaseAdapter {

    private Context context;
    private ArrayList<SalesItem> list;

    public SalesHistoryAdapter(Context context, ArrayList<SalesItem> list) {
        this.context = context;
        this.list = list;
    }

    @Override
    public int getCount() { return list.size(); }

    @Override
    public Object getItem(int i) { return list.get(i); }

    @Override
    public long getItemId(int i) { return i; }

    @Override
    public View getView(int i, View view, ViewGroup parent) {

        if (view == null) {
            view = LayoutInflater.from(context).inflate(R.layout.row_sales_item, parent, false);
        }

        TextView itemName = view.findViewById(R.id.txtItemName);
        TextView quantity = view.findViewById(R.id.txtQuantity);
        TextView date = view.findViewById(R.id.txtDate);

        SalesItem item = list.get(i);

        itemName.setText(item.itemName);
        quantity.setText("Qty: " + item.quantity);
        date.setText(item.date);

        return view;
    }
}
