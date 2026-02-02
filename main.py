from src.drivers.http_requester import HttpRequester

print("Inicializando...")

if __name__ == "__main__":
    requester = HttpRequester()
    requester.request_from_page()