package com.example.first.ui.dashboard.models;


public class InventoryItem {

    private String name;
    private int quantity;
    private int sold;
    private int left;
    private double price;

    public InventoryItem(String name, int quantity, int sold, int left, double price) {
        this.name = name;
        this.quantity = quantity;
        this.sold = sold;
        this.left = left;
        this.price = price;
    }

    public String getName() { return name; }
    public int getQuantity() { return quantity; }
    public int getSold() { return sold; }
    public int getLeft() { return left; }
    public double getPrice() { return price; }
}
