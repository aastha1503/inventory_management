package com.example.first.models;

/**
 * ApiResponse is a general-purpose data model
 * used to send and receive JSON data from the Flask backend.
 *
 * It is used for login requests/responses and any general API responses.
 */
public class ApiResponse {

    // --- Fields for login ---
    private String username;
    private String password;

    // --- Fields returned from the backend ---
    private String token;       // JWT token or session token
    private boolean success;    // True if operation succeeded
    private String message;     // Any message from backend (optional)

    // --- Constructors ---
    public ApiResponse() {
        // Default constructor needed for Retrofit/Gson
    }

    public ApiResponse(String username, String password) {
        this.username = username;
        this.password = password;
    }

    // --- Getters and Setters ---
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
