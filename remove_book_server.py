from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class BookServerHandler(BaseHTTPRequestHandler):
    json_file = "db.json"

    def __init__(self, *args, **kwargs):
        self.books = []
        self.load_books()
        super().__init__(*args, **kwargs)

    def load_books(self):
        try:
            with open(self.json_file, 'r') as file:
                self.books = json.load(file)
        except FileNotFoundError:
            self.books = []
    
    def save_books(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.books, file)

    def do_POST(self):
        print("Recebendo solicitação para deletar livro...")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
    
        try:
            data = json.loads(post_data)
            title_to_delete = data.get('titleDelete')

            if title_to_delete:
                print("deletando livro:", title_to_delete)   

                book_to_delete = next((book for book in self.books if book["title"] == title_to_delete), None)
                
                if book_to_delete:
                    self.books.remove(book_to_delete)
                    self.save_books()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"status": "success", "message": "Livro removido com sucesso"}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    print("Livro removido:", title_to_delete)
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"status": "error", "message": "Livro não encontrado"}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    print("Livro não encontrado:", title_to_delete)
                return
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": "Erro ao decodificar JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Erro ao decodificar JSON")


def run(server_class=HTTPServer, handler_class=BookServerHandler, port=5001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor rodando na porta {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()