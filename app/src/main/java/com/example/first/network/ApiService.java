package com.example.first.network;

import com.example.first.models.ApiResponse;
import com.example.first.models.Item;
import com.example.first.models.SignupRequest;
import com.example.first.models.SignupResponse;



import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

public interface ApiService {

    // -----------------------------
    // AUTH
    // -----------------------------
    @POST("register")
    Call<SignupResponse> registerUser(@Body SignupRequest request);

    @POST("login")
    Call<ApiResponse> login(@Body ApiResponse request);

    // -----------------------------
    // ITEMS
    // -----------------------------
    @GET("items")
    Call<List<Item>> getItems();

    @POST("items")
    Call<Item> createItem(@Body Item item);

    @PUT("items/{id}")
    Call<Item> updateItem(@Path("id") int id, @Body Item item);
}
