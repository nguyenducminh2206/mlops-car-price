# Car Price Predictor iOS App

Native SwiftUI client for the Flask car price prediction API.

## Run the backend

From the repository root:

```bash
python app.py
```

The API runs at `http://127.0.0.1:5001`.

## Run the app

1. Open `CarPricePredictor.xcodeproj` in Xcode.
2. Select an iPhone Simulator.
3. Run the `CarPricePredictor` scheme.

The app uses `http://127.0.0.1:5001` by default, which works for the iOS Simulator when Flask is running on the same Mac. For a physical iPhone, change the `baseURL` in `APIClient.swift` to your computer's LAN IP address and run Flask on `0.0.0.0`.

