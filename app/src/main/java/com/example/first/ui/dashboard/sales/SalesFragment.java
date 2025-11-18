package com.example.first.ui.dashboard.sales;


import android.graphics.Color;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.first.R;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.Description;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;

import java.util.ArrayList;

public class SalesFragment extends Fragment {

    LineChart lineChart;

    public SalesFragment() { }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_sales, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        lineChart = view.findViewById(R.id.salesChart);

        setupChart();
    }

    private void setupChart() {

        ArrayList<Entry> entries = new ArrayList<>();
        entries.add(new Entry(1, 15));
        entries.add(new Entry(2, 18));
        entries.add(new Entry(3, 25));
        entries.add(new Entry(4, 22));
        entries.add(new Entry(5, 35));
        entries.add(new Entry(6, 28));

        LineDataSet dataSet = new LineDataSet(entries, "Monthly Sales");
        dataSet.setColor(Color.parseColor("#5A7FFF")); // nice soft blue
        dataSet.setLineWidth(3f);
        dataSet.setCircleColor(Color.parseColor("#4CAF50")); // green dots
        dataSet.setCircleRadius(5f);
        dataSet.setValueTextSize(12f);
        dataSet.setDrawFilled(true);
        dataSet.setFillColor(Color.parseColor("#C3D4FF")); // soft light blue fill

        LineData lineData = new LineData(dataSet);
        lineChart.setData(lineData);

        // Remove chart description
        Description d = new Description();
        d.setText("");
        lineChart.setDescription(d);

        // X Axis styling
        XAxis xAxis = lineChart.getXAxis();
        xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
        xAxis.setTextColor(Color.DKGRAY);
        xAxis.setTextSize(12f);

        // Y Axis styling
        YAxis yAxisLeft = lineChart.getAxisLeft();
        yAxisLeft.setTextColor(Color.DKGRAY);
        lineChart.getAxisRight().setEnabled(false); // disable right Y axis

        // Animation
        lineChart.animateX(800);

        lineChart.invalidate(); // refresh
    }
}
