package com.example.first;


import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.first.models.Item;
import com.example.first.network.ApiClient;
import com.example.first.network.ApiService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ItemFormActivity extends AppCompatActivity {

    private EditText editName, editQuantity;
    private Button btnSave;
    private int itemId = -1; // -1 means new item

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_item_form);

        editName = findViewById(R.id.editName);
        editQuantity = findViewById(R.id.editQuantity);
        btnSave = findViewById(R.id.btnSave);

        // Check if we’re editing an existing item
        if (getIntent().hasExtra("item_id")) {
            itemId = getIntent().getIntExtra("item_id", -1);
            editName.setText(getIntent().getStringExtra("item_name"));
            editQuantity.setText(String.valueOf(getIntent().getIntExtra("item_quantity", 0)));
        }

        btnSave.setOnClickListener(v -> saveItem());
    }

    private void saveItem() {
        String name = editName.getText().toString().trim();
        String qtyText = editQuantity.getText().toString().trim();

        if (TextUtils.isEmpty(name) || TextUtils.isEmpty(qtyText)) {
            Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
            return;
        }

        int quantity = Integer.parseInt(qtyText);
        Item item = new Item(itemId, name, quantity);
        ApiService apiService = ApiClient.getApiService(this);


        Call<Item> call;
        if (itemId == -1) {
            // POST → add new item
            call = apiService.createItem(item);
        } else {
            // PUT → update existing
            call = apiService.updateItem(itemId, item);
        }

        call.enqueue(new Callback<Item>() {
            @Override
            public void onResponse(Call<Item> call, Response<Item> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(ItemFormActivity.this, "Saved successfully!", Toast.LENGTH_SHORT).show();
                    finish(); // close form
                } else {
                    Toast.makeText(ItemFormActivity.this, "Failed to save item", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Item> call, Throwable t) {
                Toast.makeText(ItemFormActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}

