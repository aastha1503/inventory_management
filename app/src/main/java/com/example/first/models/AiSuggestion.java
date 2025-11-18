package com.example.first.models;


public class AiSuggestion {

    private String itemName;
    private String status;
    private String suggestion;

    public AiSuggestion(String itemName, String status, String suggestion) {
        this.itemName = itemName;
        this.status = status;
        this.suggestion = suggestion;
    }

    public String getItemName() { return itemName; }
    public String getStatus() { return status; }
    public String getSuggestion() { return suggestion; }
}
