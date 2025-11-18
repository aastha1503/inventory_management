package com.example.first.network;
import com.example.first.models.ApiResponse;
import com.example.first.models.Item;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

/**
 * ApiService defines all endpoints used by the Android frontend
 * to communicate with the Flask backend.
 */
public interface ApiService {

    // ✅ Login endpoint (for user authentication)
    @POST("login")
    Call<ApiResponse> login(@Body ApiResponse request);

    // ✅ Fetch all inventory items
    @GET("items")
    Call<List<Item>> getItems();

    // ✅ Create a new inventory item
    @POST("items")
    Call<Item> createItem(@Body Item item);

    // ✅ Update an existing inventory item
    @PUT("items/{id}")
    Call<Item> updateItem(@Path("id") int id, @Body Item item);
}
