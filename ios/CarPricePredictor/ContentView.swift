import SwiftUI

@MainActor
final class CarPriceViewModel: ObservableObject {
    @Published var options = OptionsResponse(
        brands: [],
        models: [:],
        fuels: [],
        transmissions: [],
        years: [],
        doors: [],
        ownerCounts: []
    )

    @Published var selectedBrand = ""
    @Published var selectedModel = ""
    @Published var selectedFuel = ""
    @Published var selectedTransmission = ""
    @Published var selectedYear = 2023
    @Published var engineSize = ""
    @Published var mileage = ""
    @Published var selectedDoors = 4
    @Published var selectedOwnerCount = 1
    @Published var predictionMessage: String?
    @Published var errorMessage: String?
    @Published var isLoading = false

    private let apiClient = APIClient()

    var availableModels: [String] {
        options.models[selectedBrand] ?? []
    }

    var canPredict: Bool {
        !selectedBrand.isEmpty &&
        !selectedModel.isEmpty &&
        !selectedFuel.isEmpty &&
        !selectedTransmission.isEmpty &&
        Double(engineSize) != nil &&
        Int(mileage) != nil &&
        !isLoading
    }

    func loadOptions() async {
        isLoading = true
        errorMessage = nil

        do {
            options = try await apiClient.fetchOptions()
            selectedBrand = options.brands.first ?? ""
            selectedModel = availableModels.first ?? ""
            selectedFuel = options.fuels.first ?? ""
            selectedTransmission = options.transmissions.first ?? ""
            selectedYear = options.years.last ?? 2023
            selectedDoors = options.doors.contains(4) ? 4 : (options.doors.first ?? 4)
            selectedOwnerCount = options.ownerCounts.first ?? 1
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func brandChanged() {
        selectedModel = availableModels.first ?? ""
        predictionMessage = nil
    }

    func predict() async {
        guard let engineSizeValue = Double(engineSize), let mileageValue = Int(mileage) else {
            errorMessage = "Enter a valid engine size and mileage."
            return
        }

        isLoading = true
        errorMessage = nil
        predictionMessage = nil

        let request = PredictionRequest(
            Brand: selectedBrand,
            Model: selectedModel,
            Fuel: selectedFuel,
            Transmission: selectedTransmission,
            Year: selectedYear,
            EngineSize: engineSizeValue,
            Mileage: mileageValue,
            Doors: selectedDoors,
            OwnerCount: selectedOwnerCount
        )

        do {
            let response = try await apiClient.predict(request)
            predictionMessage = response.message
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }
}

struct ContentView: View {
    @StateObject private var viewModel = CarPriceViewModel()

    var body: some View {
        NavigationStack {
            Form {
                Section("Vehicle") {
                    Picker("Brand", selection: $viewModel.selectedBrand) {
                        ForEach(viewModel.options.brands, id: \.self) { brand in
                            Text(brand).tag(brand)
                        }
                    }
                    .onChange(of: viewModel.selectedBrand) { _ in
                        viewModel.brandChanged()
                    }

                    Picker("Model", selection: $viewModel.selectedModel) {
                        ForEach(viewModel.availableModels, id: \.self) { model in
                            Text(model).tag(model)
                        }
                    }

                    Picker("Year", selection: $viewModel.selectedYear) {
                        ForEach(viewModel.options.years, id: \.self) { year in
                            Text(String(year)).tag(year)
                        }
                    }
                }

                Section("Drivetrain") {
                    Picker("Fuel", selection: $viewModel.selectedFuel) {
                        ForEach(viewModel.options.fuels, id: \.self) { fuel in
                            Text(fuel).tag(fuel)
                        }
                    }

                    Picker("Transmission", selection: $viewModel.selectedTransmission) {
                        ForEach(viewModel.options.transmissions, id: \.self) { transmission in
                            Text(transmission).tag(transmission)
                        }
                    }

                    TextField("Engine size", text: $viewModel.engineSize)
                        .keyboardType(.decimalPad)
                }

                Section("History") {
                    TextField("Mileage (KM)", text: $viewModel.mileage)
                        .keyboardType(.numberPad)

                    Picker("Doors", selection: $viewModel.selectedDoors) {
                        ForEach(viewModel.options.doors, id: \.self) { doors in
                            Text(String(doors)).tag(doors)
                        }
                    }

                    Picker("Owners", selection: $viewModel.selectedOwnerCount) {
                        ForEach(viewModel.options.ownerCounts, id: \.self) { owners in
                            Text(String(owners)).tag(owners)
                        }
                    }
                }

                Section {
                    Button {
                        Task {
                            await viewModel.predict()
                        }
                    } label: {
                        HStack {
                            Spacer()
                            if viewModel.isLoading {
                                ProgressView()
                            } else {
                                Text("Predict Price")
                                    .fontWeight(.semibold)
                            }
                            Spacer()
                        }
                    }
                    .disabled(!viewModel.canPredict)
                }

                if let prediction = viewModel.predictionMessage {
                    Section("Estimate") {
                        Text(prediction)
                            .font(.title3.weight(.semibold))
                            .foregroundStyle(.green)
                    }
                }

                if let error = viewModel.errorMessage {
                    Section("Error") {
                        Text(error)
                            .foregroundStyle(.red)
                    }
                }
            }
            .navigationTitle("Car Price")
            .task {
                if viewModel.options.brands.isEmpty {
                    await viewModel.loadOptions()
                }
            }
        }
    }
}

#Preview {
    ContentView()
}

