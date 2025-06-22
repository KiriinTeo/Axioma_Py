import os

class Node:
    def __init__(self, titulo, autor, anoPublicacao, editora, cod_Isbn, proximoNo=None):
        self.item = {
            "titulo": titulo,
            "autor": autor,
            "publicacao": anoPublicacao,
            "editora": editora,
            "isbn": cod_Isbn,
        }
        self.next = proximoNo

class CircularLinkedList:
    def __init__(self):
        self.final = None
        self.count = 0

    def EstaVazia(self):
        return self.final is None

    def AdicionarPrimeiro(self, titulo, autor, anoPublicacao, editora, cod_Isbn):
        novoNo = Node(titulo, autor, anoPublicacao, editora, cod_Isbn)
        if not self.EstaVazia():
            novoNo.next = self.final.next
            self.final.next = novoNo
        else:
            novoNo.next = novoNo
            self.final = novoNo
        self.count += 1

    def AdicionarUltimo(self, titulo, autor, anoPublicacao, editora, cod_Isbn):
        self.AdicionarPrimeiro(titulo, autor, anoPublicacao, editora, cod_Isbn)
        self.final = self.final.next

    def RemoverPrimeiro(self):
        if self.EstaVazia():
            raise Exception("Lista vazia")
        if self.count == 1:
            self.final = None
        else:
            self.final.next = self.final.next.next
        self.count -= 1

    def RemoverUltimo(self):
        if self.EstaVazia():
            raise Exception("Lista vazia")
        if self.count == 1:
            self.final = None
        else:
            aux = self.final.next
            while aux.next != self.final:
                aux = aux.next
            aux.next = self.final.next
            self.final = aux
        self.count -= 1

    def Remover(self, item):
        if self.EstaVazia():
            raise Exception("Lista vazia")
        aux = self.final.next
        anterior = self.final

        while aux != self.final and aux.item != item:
            anterior = aux
            aux = aux.next

        if aux.item != item:
            return False

        if aux == aux.next:
            self.final = None
        else:
            anterior.next = aux.next
            if aux == self.final:
                self.final = anterior

        self.count -= 1
        return True

    def ImprimirLista(self):
        if self.EstaVazia():
            print("Lista vazia")
            return
        aux = self.final.next
        while True:
            print(aux.item, end=" -> \n")
            aux = aux.next
            if aux == self.final.next:
                break
        print()

    def limparSaida(self):
        os.system('cls' if os.name == 'nt' else 'clear')


cll = CircularLinkedList()
