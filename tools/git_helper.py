#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Helper - Automatização de commits e push para o Sage duEuler
Script interativo para facilitar atualizações no repositório
"""

import os
import subprocess
import sys
from datetime import datetime

class GitHelper:
    def __init__(self):
        self.repo_path = os.getcwd()
        self.commit_types = {
            '1': {'emoji': '📝', 'name': 'Documentação'},
            '2': {'emoji': '🐛', 'name': 'Correção de Bug'},
            '3': {'emoji': '✨', 'name': 'Nova Funcionalidade'},
            '4': {'emoji': '🚀', 'name': 'Melhoria de Performance'},
            '5': {'emoji': '📚', 'name': 'Adicionando Arquivos'},
            '6': {'emoji': '🔧', 'name': 'Refatoração'},
            '7': {'emoji': '🎨', 'name': 'Melhoria de UI/UX'},
            '8': {'emoji': '⚡', 'name': 'Otimização'},
            '9': {'emoji': '🔒', 'name': 'Segurança'},
            '0': {'emoji': '🎯', 'name': 'Outro'}
        }
    
    def run_command(self, command, capture_output=False):
        """Executa comando git e retorna resultado"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.repo_path)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                result = subprocess.run(command, shell=True, cwd=self.repo_path)
                return result.returncode == 0
        except Exception as e:
            print(f"❌ Erro ao executar comando: {e}")
            return False
    
    def check_git_status(self):
        """Verifica status do git"""
        print("🔍 Verificando status do repositório...")
        success, output, error = self.run_command("git status", capture_output=True)
        
        if not success:
            print("❌ Erro ao verificar status do git")
            return False
        
        if "nothing to commit" in output:
            print("✅ Nenhuma mudança para commitar!")
            return False
        
        print("📋 Mudanças detectadas:")
        print(output)
        return True
    
    def select_commit_type(self):
        """Permite selecionar tipo de commit"""
        print("\n🎯 Selecione o tipo de commit:")
        for key, value in self.commit_types.items():
            print(f"   {key}. {value['emoji']} {value['name']}")
        
        while True:
            choice = input("\nEscolha (1-9, 0 para outro): ").strip()
            if choice in self.commit_types:
                return self.commit_types[choice]
            print("❌ Opção inválida. Tente novamente.")
    
    def get_commit_message(self, commit_type):
        """Obtém mensagem de commit do usuário"""
        print(f"\n💬 Descreva a mudança ({commit_type['emoji']} {commit_type['name']}):")
        message = input("Mensagem: ").strip()
        
        if not message:
            print("❌ Mensagem não pode estar vazia!")
            return None
        
        return f"{commit_type['emoji']} {message}"
    
    def auto_commit(self):
        """Processo automático de commit"""
        print("🚀 Git Helper - Sage duEuler")
        print("=" * 50)
        
        # Verificar se há mudanças
        if not self.check_git_status():
            return False
        
        # Adicionar todas as mudanças
        print("\n📦 Adicionando mudanças...")
        if not self.run_command("git add ."):
            print("❌ Erro ao adicionar mudanças")
            return False
        
        # Selecionar tipo de commit
        commit_type = self.select_commit_type()
        
        # Obter mensagem
        message = self.get_commit_message(commit_type)
        if not message:
            return False
        
        # Fazer commit
        print(f"\n💾 Fazendo commit: {message}")
        if not self.run_command(f'git commit -m "{message}"'):
            print("❌ Erro ao fazer commit")
            return False
        
        # Perguntar se quer fazer push
        push_choice = input("\n🚀 Deseja fazer push para o GitHub? (s/n): ").strip().lower()
        
        if push_choice in ['s', 'sim', 'y', 'yes']:
            print("📤 Enviando para o GitHub...")
            if not self.run_command("git push"):
                print("❌ Erro ao fazer push")
                return False
            print("✅ Push realizado com sucesso!")
        else:
            print("ℹ️ Commit salvo localmente. Use 'git push' quando quiser enviar.")
        
        return True
    
    def quick_push(self):
        """Push rápido sem interação"""
        print("⚡ Push rápido...")
        
        if not self.run_command("git add ."):
            return False
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"🔄 Atualização automática - {timestamp}"
        
        if not self.run_command(f'git commit -m "{message}"'):
            return False
        
        if not self.run_command("git push"):
            return False
        
        print("✅ Push rápido realizado!")
        return True
    
    def show_status(self):
        """Mostra status detalhado"""
        print("📊 Status do Repositório:")
        print("=" * 30)
        
        # Status geral
        success, output, error = self.run_command("git status", capture_output=True)
        if success:
            print(output)
        
        # Últimos commits
        print("\n📜 Últimos commits:")
        success, output, error = self.run_command("git log --oneline -5", capture_output=True)
        if success:
            print(output)

def main():
    """Função principal"""
    helper = GitHelper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "push" or command == "p":
            helper.quick_push()
        elif command == "status" or command == "s":
            helper.show_status()
        elif command == "help" or command == "h":
            print("""
🔧 Git Helper - Comandos Disponíveis:

python tools/git_helper.py          # Modo interativo completo
python tools/git_helper.py push     # Push rápido automático
python tools/git_helper.py status   # Ver status do repositório
python tools/git_helper.py help     # Mostrar esta ajuda

💡 Dica: Use 'pull' para push rápido!
            """)
        else:
            print(f"❌ Comando desconhecido: {command}")
            print("💡 Use 'python tools/git_helper.py help' para ver opções")
    else:
        helper.auto_commit()

if __name__ == "__main__":
    main() 