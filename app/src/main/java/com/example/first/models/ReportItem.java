package com.example.first.models;


public class ReportItem {

    private String name;
    private int totalQty;
    private int soldQty;
    private int remainingQty;
    private String customerName;
    private String customerPhone;
    private String customerAddress;
    private String paymentMode;

    public ReportItem(String name, int totalQty, int soldQty, int remainingQty,
                      String customerName, String customerPhone, String customerAddress,
                      String paymentMode) {
        this.name = name;
        this.totalQty = totalQty;
        this.soldQty = soldQty;
        this.remainingQty = remainingQty;
        this.customerName = customerName;
        this.customerPhone = customerPhone;
        this.customerAddress = customerAddress;
        this.paymentMode = paymentMode;
    }

    public String getName() { return name; }
    public int getTotalQty() { return totalQty; }
    public int getSoldQty() { return soldQty; }
    public int getRemainingQty() { return remainingQty; }
    public String getCustomerName() { return customerName; }
    public String getCustomerPhone() { return customerPhone; }
    public String getCustomerAddress() { return customerAddress; }
    public String getPaymentMode() { return paymentMode; }
}
