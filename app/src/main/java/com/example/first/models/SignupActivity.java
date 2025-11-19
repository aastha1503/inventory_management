package com.example.first.models;
import com.example.first.R;
import com.example.first.LoginActivity; // adjust package name






import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.first.models.SignupRequest;
import com.example.first.models.SignupResponse;
import com.example.first.network.ApiClient;
import com.example.first.network.ApiService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignupActivity extends AppCompatActivity {

    EditText etName, etEmail, etPassword;
    Button btnSignup;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.signup_activity);

        etName = findViewById(R.id.etName);
        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        btnSignup = findViewById(R.id.btnSignup);

        btnSignup.setOnClickListener(v -> {
            String name = etName.getText().toString().trim();
            String email = etEmail.getText().toString().trim();
            String password = etPassword.getText().toString().trim();

            if (name.isEmpty() || email.isEmpty() || password.isEmpty()) {
                Toast.makeText(SignupActivity.this, "All fields are required", Toast.LENGTH_SHORT).show();
                return;
            }

            // Make API call
            ApiService api = ApiClient.getApiService(this);
            SignupRequest request = new SignupRequest(name, email, password);

            Call<SignupResponse> call = api.registerUser(request);

            call.enqueue(new Callback<SignupResponse>() {
                @Override
                public void onResponse(Call<SignupResponse> call, Response<SignupResponse> response) {
                    if (response.isSuccessful() && response.body() != null) {

                        Toast.makeText(SignupActivity.this,
                                "Signup Successful!", Toast.LENGTH_SHORT).show();

                        startActivity(new Intent(SignupActivity.this, LoginActivity.class));
                        finish();

                    } else {
                        Toast.makeText(SignupActivity.this,
                                "Signup failed!", Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<SignupResponse> call, Throwable t) {
                    Toast.makeText(SignupActivity.this,
                            "Error: " + t.getMessage(), Toast.LENGTH_LONG).show();
                }
            });
        });
    }
}
