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
        print("Recebendo solicitação para adicionar livro...")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
    

        try:
            self.load_books()
            data = json.loads(post_data)
            book_title = data.get('title')
            book_author = data.get('author')
            book_year = data.get('year')
    
    
            if not book_title or not book_author or not book_year:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "error", "message": "Dados do livro incompletos"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print("Erro: Dados do livro incompletos")
                return
    
            self.books.append({
                "title": book_title,
                "author": book_author,
                "year": book_year
            })
            print(f"Livro adicionado: {data}")

            self.save_books()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "Livro adicionado com sucesso"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Resposta enviada com sucesso")
    
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": "Erro ao decodificar JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Erro ao decodificar JSON")

        print(self.books)

def run(server_class=HTTPServer, handler_class=BookServerHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor rodando na porta {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
