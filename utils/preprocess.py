from sklearn.preprocessing import LabelEncoder, StandardScaler
def preprocess_data(df_orders, df_riders, df_deliveries):
    # Convert categorical variables
    label_encoder = LabelEncoder()
    df_orders["Restaurant_ID"] = label_encoder.fit_transform(df_orders["Restaurant_ID"])
    df_orders["Customer_ID"] = label_encoder.fit_transform(df_orders["Customer_ID"])

    # Normalize numerical features
    scaler = StandardScaler()
    df_orders[["Food_Prep_Time", "Packaging_Time", "Order_Value"]] = scaler.fit_transform(
        df_orders[["Food_Prep_Time", "Packaging_Time", "Order_Value"]]
    )

    return df_orders, df_riders, df_deliveries
