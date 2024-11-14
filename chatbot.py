import customtkinter as ctk
import csv


class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Artemis")
        master.geometry("600x500")
       

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        # Modo e tema de aparência
        ctk.set_appearance_mode("dark")  # "light" ou "dark"
       

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Olá! Eu sou a Artemis, sua assistente virtual. Como posso te ajudar hoje?\n\n")
        self.text_area.configure(state="disabled", text_color="#00FF00")  # definir cor de texto para global

        # edição de inputs
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite sua pergunta aqui...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)  

        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)


    def process_input(self, event=None):
        user_input = self.entry.get().lower().strip() 
        if not user_input:
            return  

       
        self.text_area.configure(state="normal")  
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n\n")
        self.text_area.configure(text_color="#00FF00")  

        # Respostas específicas para entradas definidas
        if user_input in ['olá', 'oi', 'olá artemis', 'oi artemis']:
            self.text_area.insert(ctk.END, "Artemis: Olá! Como posso te ajudar hoje?\n\n")
        elif user_input == 'tchau':
            self.text_area.insert(ctk.END, "Artemis: Até logo! Volte quando precisar.\n\n")
        elif user_input == 'ajuda':
            self.text_area.insert(ctk.END, "Artemis: Claro! Pergunte-me sobre conceitos de física como velocidade, aceleração, etc.\n\n")
        else:
            # Buscar dados e exibir a resposta
            data_response = self.fetch_data(user_input)  # Chama a função de busca passando a entrada do usuário
            if data_response:
                self.text_area.insert(ctk.END, f"Artemis:\n\n--- {data_response['concept_title']} ---\n\n")
                self.text_area.insert(ctk.END, f"{data_response['concept']}\n\n")
                self.text_area.insert(ctk.END, f"--- Fórmula ---\n\n{data_response['formula']}\n\n")
                self.text_area.insert(ctk.END, f"--- Referência ---\n\n{data_response['reference']}\n\n")
            else:
                self.text_area.insert(ctk.END, "Desculpe, não encontrei informações sobre esse conceito.\n\n")
                self.text_area.configure(text_color="purple")

        self.text_area.configure(state="disabled") 
        self.entry.delete(0, ctk.END)  

    def fetch_data(self, user_input):
        """Busca dados do CSV com base na entrada do usuário e retorna a resposta."""
        file_path = './venv/data/fisica.csv'  # Caminho do arquivo CSV
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Pula o cabeçalho, se houver
                next(reader)
                for row in reader:
                    if user_input in row[0].lower():  
                        return {
                            'concept_title': row[0],  # Título do conceito
                            'concept': row[1],         # Conceito
                            'formula': row[2],         # Fórmula
                            'reference': row[3]        # Referência
                        }
            return None  # Caso não encontre o conceito
        except Exception as e:
            return f"Erro ao buscar dados: {str(e)}"


if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
