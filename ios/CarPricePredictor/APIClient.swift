import Foundation

final class APIClient {
    private let baseURL: URL
    private let session: URLSession

    init(
        baseURL: URL = URL(string: "http://127.0.0.1:5001")!,
        session: URLSession = .shared
    ) {
        self.baseURL = baseURL
        self.session = session
    }

    func fetchOptions() async throws -> OptionsResponse {
        let url = baseURL.appending(path: "api/options")
        let (data, response) = try await session.data(from: url)
        try validate(response: response, data: data)
        return try JSONDecoder().decode(OptionsResponse.self, from: data)
    }

    func predict(_ request: PredictionRequest) async throws -> PredictionResponse {
        let url = baseURL.appending(path: "api/predict")
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.httpBody = try JSONEncoder().encode(request)

        let (data, response) = try await session.data(for: urlRequest)
        try validate(response: response, data: data)
        return try JSONDecoder().decode(PredictionResponse.self, from: data)
    }

    private func validate(response: URLResponse, data: Data) throws {
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        guard (200..<300).contains(httpResponse.statusCode) else {
            let apiError = try? JSONDecoder().decode(APIErrorResponse.self, from: data)
            throw APIClientError.server(
                apiError?.error ?? apiError?.message ?? "Request failed with status \(httpResponse.statusCode)."
            )
        }
    }
}

enum APIClientError: LocalizedError {
    case invalidResponse
    case server(String)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "The server returned an invalid response."
        case .server(let message):
            return message
        }
    }
}

