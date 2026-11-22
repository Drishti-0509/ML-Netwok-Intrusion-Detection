import os
import pandas as pd


FEATURE_COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
]


def predict_dataset(
    file_path,
    model,
    scaler,
    protocol_encoder,
    service_encoder,
    flag_encoder,
):

    # ----------------------------
    # Read Dataset
    # ----------------------------

    if file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

    else:

        df = pd.read_csv(
            file_path,
            header=None
        )

    # ----------------------------
    # Add column names if TXT
    # ----------------------------

    if len(df.columns) == 43:

        df.columns = FEATURE_COLUMNS + [
            "label",
            "difficulty"
        ]

    # ----------------------------
    # Remove unnecessary columns
    # ----------------------------

    for col in ["label", "difficulty"]:

        if col in df.columns:

            df.drop(columns=col, inplace=True)

    # ----------------------------
    # Validate Features
    # ----------------------------

    missing = [
        c
        for c in FEATURE_COLUMNS
        if c not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

    # Keep exact feature order

    X = df[FEATURE_COLUMNS].copy()

    # ----------------------------
    # Encode categorical columns
    # ----------------------------

    X["protocol_type"] = protocol_encoder.transform(
        X["protocol_type"]
    )

    X["service"] = service_encoder.transform(
        X["service"]
    )

    X["flag"] = flag_encoder.transform(
        X["flag"]
    )

    # ----------------------------
    # Scale
    # ----------------------------

    X_scaled = scaler.transform(X)
        # ----------------------------
    # Predict
    # ----------------------------

    predictions = model.predict(X_scaled)

    # ----------------------------
    # Prediction Probability
    # ----------------------------

    probabilities = model.predict_proba(X_scaled)

    confidence = probabilities.max(axis=1) * 100

    # ----------------------------
    # Convert Labels
    # ----------------------------

    prediction_labels = []

    for pred in predictions:

        if str(pred).lower() == "normal":

            prediction_labels.append("Normal")

        elif pred == 0:

            prediction_labels.append("Normal")

        else:

            prediction_labels.append("Attack")

    # ----------------------------
    # Save Results
    # ----------------------------

    output_df = df.copy()

    output_df["Prediction"] = prediction_labels

    output_df["Confidence (%)"] = confidence.round(2)

    output_path = os.path.join(
        "outputs",
        "predictions.csv"
    )

    output_df.to_csv(
        output_path,
        index=False
    )

    # ----------------------------
    # Statistics
    # ----------------------------

    total_records = len(output_df)

    normal_count = (
        output_df["Prediction"] == "Normal"
    ).sum()

    attack_count = (
        output_df["Prediction"] == "Attack"
    ).sum()
    preview = output_df.head(10).to_dict(orient="records")

    return {

        "total": total_records,

        "normal": int(normal_count),

        "attack": int(attack_count),

        "output_file": output_path,

        "preview": preview

    }