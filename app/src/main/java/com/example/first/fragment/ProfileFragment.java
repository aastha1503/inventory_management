package com.example.first.fragment;


import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.first.LoginActivity;
import com.example.first.R;

public class ProfileFragment extends Fragment {

    private TextView txtName, txtPhone, txtInventoryCount, txtSalesCount;
    private Button btnLogout;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_profile, container, false);

        txtName = view.findViewById(R.id.txtProfileName);
        txtPhone = view.findViewById(R.id.txtProfilePhone);
        txtInventoryCount = view.findViewById(R.id.txtProfileInventory);
        txtSalesCount = view.findViewById(R.id.txtProfileSales);
        btnLogout = view.findViewById(R.id.btnLogout);

        loadUserData();

        btnLogout.setOnClickListener(v -> logoutUser());

        return view;
    }

    private void loadUserData() {
        SharedPreferences prefs = requireActivity().getSharedPreferences("MyAppPrefs", 0);

        String name = prefs.getString("name", "User");
        String phone = prefs.getString("phone", "N/A");

        int inventory = prefs.getInt("inventory_count", 120);
        int sales = prefs.getInt("sales_count", 45);

        txtName.setText(name);
        txtPhone.setText(phone);
        txtInventoryCount.setText(String.valueOf(inventory));
        txtSalesCount.setText(String.valueOf(sales));
    }

    private void logoutUser() {
        SharedPreferences prefs = requireActivity().getSharedPreferences("MyAppPrefs", 0);
        prefs.edit().clear().apply();

        Toast.makeText(getContext(), "Logged out", Toast.LENGTH_SHORT).show();

        startActivity(new Intent(getActivity(), LoginActivity.class));
        requireActivity().finish();
    }
}
