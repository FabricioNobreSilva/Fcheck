import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import json

class Paciente:
    def __init__(self, nome: str, nascimento: str, cpf: str, sexo: str, altura: int, peso: int, imc: float, plano_de_saude: str):
        self.nome: str = nome
        self.nascimento: str = nascimento
        self.cpf: str = cpf
        self.sexo: str = sexo
        self.altura: int = altura
        self.peso: int = peso
        self.imc: float = imc
        self.plano_de_saude: str = plano_de_saude

pacientes = []
agendamentos = {}

def calcular_imc(peso: int, altura: int) -> float:
    altura_metros = altura / 100
    imc = peso / (altura_metros ** 2)
    return round(imc, 2)

def cadastrar_paciente():
    def on_cadastrar():
        nome = entry_nome.get()
        nascimento = entry_nascimento.get()
        cpf = entry_cpf.get()
        sexo = entry_sexo.get()
        altura = entry_altura.get()
        peso = entry_peso.get()

        try:
            altura = int(altura)
            peso = int(peso)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos para altura e peso.")
            return
        
        possui_plano = entry_plano.get().strip().lower()
        if possui_plano == 's':
            plano_de_saude = entry_nome_plano.get()
        else:
            plano_de_saude = "Particular"
        
        imc = calcular_imc(peso, altura)
        
        novo_paciente = Paciente(nome, nascimento, cpf, sexo, altura, peso, imc, plano_de_saude)
        pacientes.append(novo_paciente)
        messagebox.showinfo("Sucesso", f"Paciente {nome} cadastrado com sucesso!")
        
        popup.destroy()
        atualizar_tabela()

    popup = tk.Toplevel(root)
    popup.title("Cadastrar Paciente")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="Nome", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(popup)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Nascimento", bg="lightgreen").grid(row=1, column=0, padx=5, pady=5)
    entry_nascimento = tk.Entry(popup)
    entry_nascimento.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="CPF", bg="lightgreen").grid(row=2, column=0, padx=5, pady=5)
    entry_cpf = tk.Entry(popup)
    entry_cpf.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(popup, text="Sexo", bg="lightgreen").grid(row=3, column=0, padx=5, pady=5)
    entry_sexo = tk.Entry(popup)
    entry_sexo.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(popup, text="Altura (cm)", bg="lightgreen").grid(row=4, column=0, padx=5, pady=5)
    entry_altura = tk.Entry(popup)
    entry_altura.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(popup, text="Peso (kg)", bg="lightgreen").grid(row=5, column=0, padx=5, pady=5)
    entry_peso = tk.Entry(popup)
    entry_peso.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(popup, text="Possui plano de saúde? (s/n)", bg="lightgreen").grid(row=6, column=0, padx=5, pady=5)
    entry_plano = tk.Entry(popup)
    entry_plano.grid(row=6, column=1, padx=5, pady=5)
    
    tk.Label(popup, text="Nome do plano de saúde (se aplicável)", bg="lightgreen").grid(row=7, column=0, padx=5, pady=5)
    entry_nome_plano = tk.Entry(popup)
    entry_nome_plano.grid(row=7, column=1, padx=5, pady=5)
    
    btn_confirmar_cadastro = tk.Button(popup, text="Confirmar", command=on_cadastrar, bg="black", fg="lightgreen")
    btn_confirmar_cadastro.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

def remover_paciente():
    def on_remover():
        cpf = entry_cpf_remover.get()
        global pacientes
        pacientes = [paciente for paciente in pacientes if paciente.cpf != cpf]
        if cpf in agendamentos:
            del agendamentos[cpf]
        messagebox.showinfo("Sucesso", f"Paciente com CPF {cpf} removido com sucesso!")
        popup.destroy()
        atualizar_tabela()

    popup = tk.Toplevel(root)
    popup.title("Remover Paciente")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente a ser removido", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_remover = tk.Entry(popup)
    entry_cpf_remover.grid(row=0, column=1, padx=5, pady=5)
    
    btn_confirmar_remocao = tk.Button(popup, text="Confirmar", command=on_remover, bg="black", fg="lightgreen")
    btn_confirmar_remocao.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def alterar_cadastro_paciente():
    def on_alterar():
        cpf = entry_cpf_alterar.get()
        for paciente in pacientes:
            if paciente.cpf == cpf:
                def on_confirmar_alteracao():
                    paciente.nome = entry_nome_alt.get() or paciente.nome
                    paciente.nascimento = entry_nascimento_alt.get() or paciente.nascimento
                    paciente.sexo = entry_sexo_alt.get() or paciente.sexo
                    altura = entry_altura_alt.get() or paciente.altura
                    peso = entry_peso_alt.get() or paciente.peso
                    try:
                        altura = int(altura)
                        peso = int(peso)
                    except ValueError:
                        messagebox.showerror("Erro", "Por favor, insira valores válidos para altura e peso.")
                        return
                    paciente.altura = altura
                    paciente.peso = peso
                    paciente.imc = calcular_imc(peso, altura)
                    possui_plano = entry_plano_alt.get().strip().lower()
                    if possui_plano == 's':
                        paciente.plano_de_saude = entry_nome_plano_alt.get() or paciente.plano_de_saude
                    else:
                        paciente.plano_de_saude = "Particular"
                    messagebox.showinfo("Sucesso", f"Cadastro do paciente com CPF {cpf} atualizado com sucesso!")
                    popup_alt.destroy()
                    atualizar_tabela()
                
                popup_alt = tk.Toplevel(root)
                popup_alt.title("Alterar Paciente")
                popup_alt.configure(bg="lightgreen")

                tk.Label(popup_alt, text="Nome", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
                entry_nome_alt = tk.Entry(popup_alt)
                entry_nome_alt.grid(row=0, column=1, padx=5, pady=5)
                entry_nome_alt.insert(0, paciente.nome)

                tk.Label(popup_alt, text="Nascimento", bg="lightgreen").grid(row=1, column=0, padx=5, pady=5)
                entry_nascimento_alt = tk.Entry(popup_alt)
                entry_nascimento_alt.grid(row=1, column=1, padx=5, pady=5)
                entry_nascimento_alt.insert(0, paciente.nascimento)

                tk.Label(popup_alt, text="Sexo", bg="lightgreen").grid(row=2, column=0, padx=5, pady=5)
                entry_sexo_alt = tk.Entry(popup_alt)
                entry_sexo_alt.grid(row=2, column=1, padx=5, pady=5)
                entry_sexo_alt.insert(0, paciente.sexo)

                tk.Label(popup_alt, text="Altura (cm)", bg="lightgreen").grid(row=3, column=0, padx=5, pady=5)
                entry_altura_alt = tk.Entry(popup_alt)
                entry_altura_alt.grid(row=3, column=1, padx=5, pady=5)
                entry_altura_alt.insert(0, paciente.altura)

                tk.Label(popup_alt, text="Peso (kg)", bg="lightgreen").grid(row=4, column=0, padx=5, pady=5)
                entry_peso_alt = tk.Entry(popup_alt)
                entry_peso_alt.grid(row=4, column=1, padx=5, pady=5)
                entry_peso_alt.insert(0, paciente.peso)

                tk.Label(popup_alt, text="Plano de saúde", bg="lightgreen").grid(row=5, column=0, padx=5, pady=5)
                entry_plano_alt = tk.Entry(popup_alt)
                entry_plano_alt.grid(row=5, column=1, padx=5, pady=5)
                entry_plano_alt.insert(0, paciente.plano_de_saude)
                
                tk.Label(popup_alt, text="Nome do plano de saúde (se aplicável)", bg="lightgreen").grid(row=6, column=0, padx=5, pady=5)
                entry_nome_plano_alt = tk.Entry(popup_alt)
                entry_nome_plano_alt.grid(row=6, column=1, padx=5, pady=5)
                
                btn_confirmar_alteracao = tk.Button(popup_alt, text="Confirmar", command=on_confirmar_alteracao, bg="black", fg="lightgreen")
                btn_confirmar_alteracao.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

                return
        messagebox.showerror("Erro", f"Paciente com CPF {cpf} não encontrado.")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Alterar Cadastro do Paciente")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente a ser alterado", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_alterar = tk.Entry(popup)
    entry_cpf_alterar.grid(row=0, column=1, padx=5, pady=5)
    
    btn_confirmar_cpf = tk.Button(popup, text="Confirmar", command=on_alterar, bg="black", fg="lightgreen")
    btn_confirmar_cpf.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def consultar_cadastro_paciente():
    def on_consultar():
        cpf = entry_cpf_consultar.get()
        for paciente in pacientes:
            if paciente.cpf == cpf:
                messagebox.showinfo("Consulta", f"Nome: {paciente.nome}\nNascimento: {paciente.nascimento}\nCPF: {paciente.cpf}\nSexo: {paciente.sexo}\nAltura: {paciente.altura}\nPeso: {paciente.peso}\nIMC: {paciente.imc}\nPlano de Saúde: {paciente.plano_de_saude}")
                popup.destroy()
                return
        messagebox.showerror("Erro", f"Paciente com CPF {cpf} não encontrado.")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Consultar Paciente")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente a ser consultado", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_consultar = tk.Entry(popup)
    entry_cpf_consultar.grid(row=0, column=1, padx=5, pady=5)
    
    btn_confirmar_consulta = tk.Button(popup, text="Confirmar", command=on_consultar, bg="black", fg="lightgreen")
    btn_confirmar_consulta.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def agendar_consulta():
    def on_agendar():
        cpf = entry_cpf_agendar.get()
        data = calendar_agendamento.get_date()
        horario = entry_horario.get()
        if cpf in agendamentos:
            agendamentos[cpf].append({'data': data, 'horario': horario})
        else:
            agendamentos[cpf] = [{'data': data, 'horario': horario}]
        messagebox.showinfo("Sucesso", f"Consulta agendada para {data} às {horario}!")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Agendar Consulta")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_agendar = tk.Entry(popup)
    entry_cpf_agendar.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Data da consulta", bg="lightgreen").grid(row=1, column=0, padx=5, pady=5)
    calendar_agendamento = DateEntry(popup, background='darkblue', foreground='white', borderwidth=2)
    calendar_agendamento.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="Horário (HH:MM)", bg="lightgreen").grid(row=2, column=0, padx=5, pady=5)
    entry_horario = tk.Entry(popup)
    entry_horario.grid(row=2, column=1, padx=5, pady=5)

    btn_confirmar_agendamento = tk.Button(popup, text="Confirmar", command=on_agendar, bg="black", fg="lightgreen")
    btn_confirmar_agendamento.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

def consultar_agendamentos():
    def on_consultar():
        cpf = entry_cpf_consultar_agendamentos.get()
        if cpf in agendamentos:
            agendamentos_paciente = agendamentos[cpf]
            agendamentos_texto = "\n".join([f"Data: {ag['data']} - Horário: {ag['horario']}" for ag in agendamentos_paciente])
            messagebox.showinfo("Agendamentos", f"Agendamentos para CPF {cpf}:\n{agendamentos_texto}")
        else:
            messagebox.showinfo("Agendamentos", f"Não há agendamentos para CPF {cpf}.")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Consultar Agendamentos")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_consultar_agendamentos = tk.Entry(popup)
    entry_cpf_consultar_agendamentos.grid(row=0, column=1, padx=5, pady=5)

    btn_confirmar_consulta_agendamentos = tk.Button(popup, text="Confirmar", command=on_consultar, bg="black", fg="lightgreen")
    btn_confirmar_consulta_agendamentos.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def remarcar_agendamento():
    def on_remarcar():
        cpf = entry_cpf_remarcar.get()
        data_antiga = calendar_remarcar_antiga.get_date()
        horario_antigo = entry_horario_antigo.get()
        nova_data = calendar_remarcar_nova.get_date()
        novo_horario = entry_novo_horario.get()
        
        if cpf in agendamentos:
            for agendamento in agendamentos[cpf]:
                if agendamento['data'] == data_antiga and agendamento['horario'] == horario_antigo:
                    agendamento['data'] = nova_data
                    agendamento['horario'] = novo_horario
                    messagebox.showinfo("Sucesso", f"Agendamento remarcado para {nova_data} às {novo_horario}!")
                    popup.destroy()
                    return
            messagebox.showerror("Erro", f"Agendamento não encontrado para {data_antiga} às {horario_antigo}.")
        else:
            messagebox.showerror("Erro", f"Não há agendamentos para CPF {cpf}.")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Remarcar Agendamento")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_remarcar = tk.Entry(popup)
    entry_cpf_remarcar.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Data antiga", bg="lightgreen").grid(row=1, column=0, padx=5, pady=5)
    calendar_remarcar_antiga = DateEntry(popup, background='darkblue', foreground='white', borderwidth=2)
    calendar_remarcar_antiga.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="Horário antigo (HH:MM)", bg="lightgreen").grid(row=2, column=0, padx=5, pady=5)
    entry_horario_antigo = tk.Entry(popup)
    entry_horario_antigo.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(popup, text="Nova data", bg="lightgreen").grid(row=3, column=0, padx=5, pady=5)
    calendar_remarcar_nova = DateEntry(popup, background='darkblue', foreground='white', borderwidth=2)
    calendar_remarcar_nova.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(popup, text="Novo horário (HH:MM)", bg="lightgreen").grid(row=4, column=0, padx=5, pady=5)
    entry_novo_horario = tk.Entry(popup)
    entry_novo_horario.grid(row=4, column=1, padx=5, pady=5)

    btn_confirmar_remarcacao = tk.Button(popup, text="Confirmar", command=on_remarcar, bg="black", fg="lightgreen")
    btn_confirmar_remarcacao.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

def remover_agendamento():
    def on_remover():
        cpf = entry_cpf_remover_agendamento.get()
        data = calendar_remover.get_date()
        horario = entry_horario_remover.get()
        
        if cpf in agendamentos:
            for agendamento in agendamentos[cpf]:
                if agendamento['data'] == data and agendamento['horario'] == horario:
                    agendamentos[cpf].remove(agendamento)
                    if not agendamentos[cpf]:
                        del agendamentos[cpf]
                    messagebox.showinfo("Sucesso", f"Agendamento removido com sucesso!")
                    popup.destroy()
                    return
            messagebox.showerror("Erro", f"Agendamento não encontrado para {data} às {horario}.")
        else:
            messagebox.showerror("Erro", f"Não há agendamentos para CPF {cpf}.")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Remover Agendamento")
    popup.configure(bg="lightgreen")

    tk.Label(popup, text="CPF do paciente", bg="lightgreen").grid(row=0, column=0, padx=5, pady=5)
    entry_cpf_remover_agendamento = tk.Entry(popup)
    entry_cpf_remover_agendamento.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Data da consulta", bg="lightgreen").grid(row=1, column=0, padx=5, pady=5)
    calendar_remover = DateEntry(popup, background='darkblue', foreground='white', borderwidth=2)
    calendar_remover.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="Horário (HH:MM)", bg="lightgreen").grid(row=2, column=0, padx=5, pady=5)
    entry_horario_remover = tk.Entry(popup)
    entry_horario_remover.grid(row=2, column=1, padx=5, pady=5)

    btn_confirmar_remocao_agendamento = tk.Button(popup, text="Confirmar", command=on_remover, bg="black", fg="lightgreen")
    btn_confirmar_remocao_agendamento.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

def atualizar_tabela():
    for row in tabela.get_children():
        tabela.delete(row)
    for paciente in pacientes:
        tabela.insert("", "end", values=(paciente.nome, paciente.nascimento, paciente.cpf, paciente.sexo, paciente.altura, paciente.peso, paciente.imc, paciente.plano_de_saude))

root = tk.Tk()
root.title("Sistema de Gerenciamento de Pacientes")
root.configure(bg="lightgreen")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_cadastrar = tk.Button(frame, text="Cadastrar", command=cadastrar_paciente, bg="black", fg="lightgreen")
btn_cadastrar.grid(row=0, column=0, padx=5)

btn_remover = tk.Button(frame, text="Remover", command=remover_paciente, bg="black", fg="lightgreen")
btn_remover.grid(row=0, column=1, padx=5)

btn_alterar = tk.Button(frame, text="Alterar", command=alterar_cadastro_paciente, bg="black", fg="lightgreen")
btn_alterar.grid(row=0, column=2, padx=5)

btn_consultar = tk.Button(frame, text="Consultar", command=consultar_cadastro_paciente, bg="black", fg="lightgreen")
btn_consultar.grid(row=0, column=3, padx=5)

btn_agendar = tk.Button(frame, text="Agendar Consulta", command=agendar_consulta, bg="black", fg="lightgreen")
btn_agendar.grid(row=0, column=4, padx=5)

btn_consultar_agendamentos = tk.Button(frame, text="Consultar Agendamentos", command=consultar_agendamentos, bg="black", fg="lightgreen")
btn_consultar_agendamentos.grid(row=0, column=5, padx=5)

btn_remarcar = tk.Button(frame, text="Remarcar Agendamento", command=remarcar_agendamento, bg="black", fg="lightgreen")
btn_remarcar.grid(row=0, column=6, padx=5)

btn_remover_agendamento = tk.Button(frame, text="Remover Agendamento", command=remover_agendamento, bg="black", fg="lightgreen")
btn_remover_agendamento.grid(row=0, column=7, padx=5)

tabela = ttk.Treeview(root, columns=("Nome", "Nascimento", "CPF", "Sexo", "Altura", "Peso", "IMC", "Plano de Saúde"), show="headings")
tabela.heading("Nome", text="Nome")
tabela.heading("Nascimento", text="Nascimento")
tabela.heading("CPF", text="CPF")
tabela.heading("Sexo", text="Sexo")
tabela.heading("Altura", text="Altura (cm)")
tabela.heading("Peso", text="Peso (kg)")
tabela.heading("IMC", text="IMC")
tabela.heading("Plano de Saúde", text="Plano de Saúde")

tabela.pack(pady=10)

atualizar_tabela()

root.mainloop()
