package com.example.first.models;

public class SignupRequest {

    private String name;
    private String email;
    private String password;

    // Constructor
    public SignupRequest(String name, String email, String password) {
        this.name = name;
        this.email = email;
        this.password = password;
    }

    // Optional getters
    public String getName() { return name; }
    public String getEmail() { return email; }
    public String getPassword() { return password; }
}
