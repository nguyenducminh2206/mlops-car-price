import Foundation

struct OptionsResponse: Decodable {
    let brands: [String]
    let models: [String: [String]]
    let fuels: [String]
    let transmissions: [String]
    let years: [Int]
    let doors: [Int]
    let ownerCounts: [Int]
}

struct PredictionRequest: Encodable {
    let Brand: String
    let Model: String
    let Fuel: String
    let Transmission: String
    let Year: Int
    let EngineSize: Double
    let Mileage: Int
    let Doors: Int
    let OwnerCount: Int
}

struct PredictionResponse: Decodable {
    let prediction: Double
    let currency: String?
    let message: String
}

struct APIErrorResponse: Decodable {
    let error: String?
    let message: String?
}

