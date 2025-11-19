package com.example.first;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import com.example.first.utils.PreferenceManager;

public class DashboardActivity extends AppCompatActivity {

    Button btnInventory, btnAddItem, btnLogout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        btnInventory = findViewById(R.id.btnInventory);
        btnAddItem = findViewById(R.id.btnAddItem);
        btnLogout = findViewById(R.id.btnLogout);

        // Go to inventory list
        btnInventory.setOnClickListener(v -> {
            Intent intent = new Intent(DashboardActivity.this, InventoryListActivity.class);
            startActivity(intent);
        });

        // Go to add item form
        btnAddItem.setOnClickListener(v -> {
            Intent intent = new Intent(DashboardActivity.this, ItemFormActivity.class);
            startActivity(intent);
        });

        // Logout
        btnLogout.setOnClickListener(v -> {
            PreferenceManager.clearToken(this);
            Intent intent = new Intent(DashboardActivity.this, LoginActivity.class);
            startActivity(intent);
            finish();
        });
    }
}
